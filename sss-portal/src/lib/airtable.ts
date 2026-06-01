import type { ATRecord, ActionItem, SLAStatus } from '@/types'

const BASE = process.env.AIRTABLE_BASE_ID!
const TOKEN = process.env.AIRTABLE_PAT!
const API = 'https://api.airtable.com/v0'

const T = {
  REQUESTS: process.env.AT_TABLE_REQUESTS!,
  BOOKINGS: process.env.AT_TABLE_BOOKINGS!,
  CLIENTS: process.env.AT_TABLE_CLIENTS!,
  AUDIT_LOG: process.env.AT_TABLE_AUDIT_LOG!,
  APPROVALS: process.env.AT_TABLE_APPROVALS!,
  ISSUES: process.env.AT_TABLE_ISSUES!,
  USERS: process.env.AT_TABLE_USERS!,
  CHECKLISTS: process.env.AT_TABLE_CHECKLISTS!,
}

function headers(): HeadersInit {
  return {
    Authorization: `Bearer ${TOKEN}`,
    'Content-Type': 'application/json',
  }
}

function url(tableId: string, params?: Record<string, string | string[]>): string {
  const base = `${API}/${BASE}/${tableId}`
  if (!params) return base
  const q = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (Array.isArray(v)) v.forEach((val) => q.append(k, val))
    else q.append(k, v)
  }
  return `${base}?${q}`
}

// ─── Core ────────────────────────────────────────────────────────────────────

async function getAll(
  tableId: string,
  params?: Record<string, string | string[]>
): Promise<ATRecord[]> {
  const records: ATRecord[] = []
  let offset: string | undefined

  do {
    const p: Record<string, string | string[]> = { ...params }
    if (offset) p.offset = offset

    const res = await fetch(url(tableId, p), {
      headers: headers(),
      cache: 'no-store',
    })

    if (!res.ok) {
      const err = await res.text()
      throw new Error(`Airtable getAll ${tableId}: ${res.status} ${err}`)
    }

    const data = await res.json()
    records.push(...(data.records ?? []))
    offset = data.offset
  } while (offset)

  return records
}

async function getOne(tableId: string, recordId: string): Promise<ATRecord> {
  const res = await fetch(`${API}/${BASE}/${tableId}/${recordId}`, {
    headers: headers(),
    cache: 'no-store',
  })
  if (!res.ok) {
    const err = await res.text()
    throw new Error(`Airtable getOne ${tableId}/${recordId}: ${res.status} ${err}`)
  }
  return res.json()
}

async function patch(
  tableId: string,
  recordId: string,
  fields: Record<string, unknown>
): Promise<ATRecord> {
  const res = await fetch(`${API}/${BASE}/${tableId}/${recordId}`, {
    method: 'PATCH',
    headers: headers(),
    body: JSON.stringify({ fields }),
  })
  if (!res.ok) {
    const err = await res.text()
    throw new Error(`Airtable patch ${tableId}/${recordId}: ${res.status} ${err}`)
  }
  return res.json()
}

async function create(tableId: string, fields: Record<string, unknown>): Promise<ATRecord> {
  const res = await fetch(`${API}/${BASE}/${tableId}`, {
    method: 'POST',
    headers: headers(),
    body: JSON.stringify({ fields }),
  })
  if (!res.ok) {
    const err = await res.text()
    throw new Error(`Airtable create ${tableId}: ${res.status} ${err}`)
  }
  return res.json()
}

// ─── Audit Log ───────────────────────────────────────────────────────────────

async function log(
  eventType: string,
  entity: string,
  entityId: string,
  actor: string,
  details?: string,
  severity = 'INFO'
): Promise<void> {
  try {
    await create(T.AUDIT_LOG, {
      Event_Type: eventType,
      Entity: entity,
      Entity_ID: entityId,
      Actor: actor,
      Severity: severity,
      Details: details ?? '',
    })
  } catch {
    // best-effort — never block the main operation
  }
}

// ─── Leads (Requests table) ───────────────────────────────────────────────────
// Real field names: "First Name", "Last Name", "Email", "Phone", "Status",
// "Notes", "Experience" (destination), "Preferred Date" (charter date),
// "Guest Count" (group size), "Lead Source" (singleSelect), "🔔 Response Needed"

export const leads = {
  async getActive(): Promise<ATRecord[]> {
    return getAll(T.REQUESTS, {
      filterByFormula: `NOT({Status}="CLOSED")`,
      'sort[0][field]': 'Submission Date',
      'sort[0][direction]': 'desc',
    })
  },

  async getActionRequired(): Promise<ATRecord[]> {
    return getAll(T.REQUESTS, {
      filterByFormula: `AND({🔔 Response Needed}=1,NOT({Status}="CLOSED"))`,
    })
  },

  async getById(id: string): Promise<ATRecord> {
    return getOne(T.REQUESTS, id)
  },

  async qualify(id: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.REQUESTS, id, { Status: 'BOOKED' })
    await log('QUALIFY', 'Lead', id, actor, 'Status set to BOOKED', 'INFO')
    return record
  },

  async updateStatus(id: string, status: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.REQUESTS, id, { Status: status })
    await log('STATUS_CHANGE', 'Lead', id, actor, `Status → ${status}`)
    return record
  },

  async saveNote(id: string, note: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.REQUESTS, id, { Notes: note })
    await log('NOTE_SAVED', 'Lead', id, actor)
    return record
  },

  async setProbability(_id: string, _probability: number, _actor: string): Promise<ATRecord> {
    // Probability field does not exist in Requests table — no-op to avoid API errors
    return getOne(T.REQUESTS, _id)
  },
}

// ─── Bookings ────────────────────────────────────────────────────────────────
// Real field names: "Booking ID" (formula), "Client Name" (lookup array),
// "Yacht Name" (formula), "Port of Call" (formula), "Charter Date" (dateTime),
// "Package Price" (currency), "Status"

export const bookings = {
  async getActive(): Promise<ATRecord[]> {
    return getAll(T.BOOKINGS, {
      filterByFormula: `NOT(OR({Status}="COMPLETE",{Status}="CANCELLED"))`,
    })
  },

  async getActionRequired(): Promise<ATRecord[]> {
    return getAll(T.BOOKINGS, {
      filterByFormula: `AND({Emergency_Flag}=1,NOT(OR({Status}="COMPLETE",{Status}="CANCELLED")))`,
    })
  },

  async getById(id: string): Promise<ATRecord> {
    return getOne(T.BOOKINGS, id)
  },

  async flag(id: string, reason: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.BOOKINGS, id, {
      Emergency_Flag: true,
      Charter_Notes: reason,
    })
    await log('BOOKING_FLAGGED', 'Booking', id, actor, reason, 'WARNING')
    return record
  },

  async updateField(
    id: string,
    fields: Record<string, unknown>,
    actor: string
  ): Promise<ATRecord> {
    const record = await patch(T.BOOKINGS, id, fields)
    await log('BOOKING_UPDATED', 'Booking', id, actor, JSON.stringify(fields))
    return record
  },
}

// ─── Activity Feed ────────────────────────────────────────────────────────────

export const activity = {
  async getRecent(limit = 50): Promise<ATRecord[]> {
    return getAll(T.AUDIT_LOG, {
      'sort[0][field]': 'Created',
      'sort[0][direction]': 'desc',
      maxRecords: String(limit),
    })
  },

  async getUnresolved(): Promise<ATRecord[]> {
    return getAll(T.AUDIT_LOG, {
      filterByFormula: `AND({Resolved}=0,OR({Severity}="ERROR",{Severity}="CRITICAL"))`,
    })
  },

  async resolve(id: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.AUDIT_LOG, id, { Resolved: true })
    await log('ISSUE_RESOLVED', 'AuditLog', id, actor)
    return record
  },
}

// ─── Approvals (Founder Decisions table) ─────────────────────────────────────
// Real field names: "Request Title", "Context", "Proposed Action",
// "Request Type", "Urgency", "Decision" (PENDING/APPROVED/DENIED/MODIFIED),
// "Decision Note", "Submitted At", "SLA Breached", "Hours Pending"

export const approvals = {
  async getPending(): Promise<ATRecord[]> {
    return getAll(T.APPROVALS, {
      filterByFormula: `OR({Decision}="PENDING",{Decision}="")`,
      'sort[0][field]': 'Urgency',
      'sort[0][direction]': 'asc',
    })
  },

  async decide(id: string, approved: boolean, actor: string, note?: string): Promise<ATRecord> {
    const decision = approved ? 'APPROVED' : 'DENIED'
    const record = await patch(T.APPROVALS, id, {
      Decision: decision,
      'Decision Note': note ?? '',
      'Founder Name': actor,
      'Decided At': new Date().toISOString(),
    })
    await log('APPROVAL_DECISION', 'Approval', id, actor, `${decision}${note ? ': ' + note : ''}`)
    return record
  },
}

// ─── Issues (Incident_Reports table) ─────────────────────────────────────────
// Real field names: "Incident_ID", "Type", "Severity", "Description",
// "City", "Incident_Date", "Will_Notes", "Resolved_At", "Booking_ID"

export const issues = {
  async getOpen(): Promise<ATRecord[]> {
    return getAll(T.ISSUES, {
      filterByFormula: `{Resolved_At}=""`,
      'sort[0][field]': 'Severity',
      'sort[0][direction]': 'desc',
    })
  },

  async resolve(id: string, note: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.ISSUES, id, {
      Resolved_At: new Date().toISOString().split('T')[0],
      Will_Notes: note,
    })
    await log('ISSUE_RESOLVED', 'Incident', id, actor, note)
    return record
  },

  async saveNote(id: string, note: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.ISSUES, id, { Will_Notes: note })
    await log('ISSUE_NOTE_SAVED', 'Incident', id, actor)
    return record
  },
}

// ─── Users ───────────────────────────────────────────────────────────────────

export const users = {
  async findByEmail(email: string): Promise<ATRecord | null> {
    const records = await getAll(T.USERS, {
      filterByFormula: `{Email}="${email.toLowerCase()}"`,
      maxRecords: '1',
    })
    return records[0] ?? null
  },

  async touchLogin(id: string): Promise<void> {
    await patch(T.USERS, id, { Last_Login: new Date().toISOString() }).catch(() => {})
  },
}

// ─── Action Center ───────────────────────────────────────────────────────────

function slaScore(sla: string | undefined): number {
  if (sla === 'BREACHED') return 100
  if (sla === 'WARNING') return 50
  return 0
}

function leadName(f: Record<string, unknown>): string {
  const first = (f['First Name'] as string) ?? ''
  const last = (f['Last Name'] as string) ?? ''
  return [first, last].filter(Boolean).join(' ') || 'Unknown Lead'
}

function selectName(v: unknown): string {
  if (!v) return ''
  if (typeof v === 'string') return v
  if (typeof v === 'object' && v !== null && 'name' in v) return (v as { name: string }).name
  return ''
}

function lookupFirst(v: unknown): string {
  if (Array.isArray(v)) return (v[0] as string) ?? ''
  if (typeof v === 'string') return v
  return ''
}

export async function getActionItems(): Promise<ActionItem[]> {
  const [leadsRes, bookingsRes, approvalsRes, issuesRes] = await Promise.allSettled([
    leads.getActionRequired(),
    bookings.getActionRequired(),
    approvals.getPending(),
    issues.getOpen(),
  ])

  const items: ActionItem[] = []

  if (leadsRes.status === 'fulfilled') {
    for (const r of leadsRes.value) {
      const f = r.fields
      items.push({
        id: r.id,
        source: 'lead',
        priority: 60,
        title: leadName(f),
        subtitle: [selectName(f['Lead Source']), f.Experience, f['Preferred Date']]
          .filter(Boolean)
          .join(' · '),
        sla: 'WARNING',
        href: `/concierge/leads/${r.id}`,
        badge: selectName(f['Lead Source']) || undefined,
      })
    }
  }

  if (bookingsRes.status === 'fulfilled') {
    for (const r of bookingsRes.value) {
      const f = r.fields
      items.push({
        id: r.id,
        source: 'booking',
        priority: 70,
        title: (f['Booking ID'] as string) ?? r.id.slice(-6).toUpperCase(),
        subtitle: [lookupFirst(f['Client Name']), f['Charter Date']]
          .filter(Boolean)
          .join(' · '),
        sla: 'WARNING',
        href: `/operations/charters/${r.id}`,
        badge: 'FLAGGED',
      })
    }
  }

  if (approvalsRes.status === 'fulfilled') {
    for (const r of approvalsRes.value) {
      const f = r.fields
      const urgency = selectName(f.Urgency)
      const sla: SLAStatus = urgency === 'IMMEDIATE' ? 'BREACHED' : urgency === 'TODAY' ? 'WARNING' : 'GREEN'
      items.push({
        id: r.id,
        source: 'approval',
        priority: sla === 'BREACHED' ? 90 : sla === 'WARNING' ? 80 : 50,
        title: (f['Request Title'] as string) ?? 'Approval Required',
        subtitle: (f.Context as string) ?? '',
        sla,
        href: `/owner/approvals`,
        badge: 'APPROVAL',
      })
    }
  }

  if (issuesRes.status === 'fulfilled') {
    for (const r of issuesRes.value) {
      const f = r.fields
      const severity = selectName(f.Severity)
      const sla: SLAStatus =
        severity === 'Critical' ? 'BREACHED' : severity === 'High' ? 'WARNING' : 'GREEN'
      items.push({
        id: r.id,
        source: 'issue',
        priority: sla === 'BREACHED' ? 85 : sla === 'WARNING' ? 65 : 35,
        title: (f.Incident_ID as string) ?? 'Incident',
        subtitle: [selectName(f.Type), selectName(f.City), f.Incident_Date]
          .filter(Boolean)
          .join(' · '),
        sla,
        href: `/owner/issues`,
        badge: severity || undefined,
      })
    }
  }

  return items.sort((a, b) => b.priority - a.priority)
}

// ─── Stats for Owner Dashboard ───────────────────────────────────────────────

export interface DashboardStats {
  activeLeads: number
  attentionRequired: number
  activeBookings: number
  pendingApprovals: number
  openIssues: number
  monthRevenue: number
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const [leadsRes, bookingsRes, approvalsRes, issuesRes] = await Promise.allSettled([
    leads.getActive(),
    bookings.getActive(),
    approvals.getPending(),
    issues.getOpen(),
  ])

  const activeLeads = leadsRes.status === 'fulfilled' ? leadsRes.value.length : 0
  const attentionRequired =
    leadsRes.status === 'fulfilled'
      ? leadsRes.value.filter((r) => r.fields['🔔 Response Needed']).length
      : 0

  const activeBookings = bookingsRes.status === 'fulfilled' ? bookingsRes.value.length : 0
  const monthRevenue =
    bookingsRes.status === 'fulfilled'
      ? bookingsRes.value.reduce(
          (sum, r) => sum + ((r.fields['Package Price'] as number) ?? 0),
          0
        )
      : 0

  const pendingApprovals = approvalsRes.status === 'fulfilled' ? approvalsRes.value.length : 0
  const openIssues = issuesRes.status === 'fulfilled' ? issuesRes.value.length : 0

  return {
    activeLeads,
    attentionRequired,
    activeBookings,
    pendingApprovals,
    openIssues,
    monthRevenue,
  }
}
