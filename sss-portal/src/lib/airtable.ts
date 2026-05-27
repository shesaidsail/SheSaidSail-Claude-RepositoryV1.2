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
      'Action Type': eventType,
      'Changed Table': entity,
      'Scenario ID': entityId,
      Actor: actor,
      'Severity Level': severity,
      'Payload Summary': details ?? '',
    })
  } catch {
    // best-effort — never block the main operation
  }
}

// ─── Leads ───────────────────────────────────────────────────────────────────

export const leads = {
  async getActive(): Promise<ATRecord[]> {
    return getAll(T.REQUESTS, {
      filterByFormula: `NOT(OR({Status}="CLOSED_WON",{Status}="CLOSED_LOST"))`,
      'sort[0][field]': 'Submission Date',
      'sort[0][direction]': 'desc',
    })
  },

  async getActionRequired(): Promise<ATRecord[]> {
    return getAll(T.REQUESTS, {
      filterByFormula: `AND({🔔 Response Needed}=1,NOT(OR({Status}="CLOSED_WON",{Status}="CLOSED_LOST")))`,
    })
  },

  async getById(id: string): Promise<ATRecord> {
    return getOne(T.REQUESTS, id)
  },

  async qualify(id: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.REQUESTS, id, { Status: 'AVAILABILITY_CONFIRMED' })
    await log('QUALIFY', 'Lead', id, actor, 'Status set to AVAILABILITY_CONFIRMED', 'INFO')
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

  async setProbability(id: string, probability: number, actor: string): Promise<ATRecord> {
    const record = await patch(T.REQUESTS, id, { Probability: probability })
    await log('PROBABILITY_SET', 'Lead', id, actor, `Probability → ${probability}%`)
    return record
  },
}

// ─── Bookings ────────────────────────────────────────────────────────────────

export const bookings = {
  async getActive(): Promise<ATRecord[]> {
    return getAll(T.BOOKINGS, {
      filterByFormula: `NOT(OR({Status}="COMPLETED",{Status}="CANCELLED"))`,
    })
  },

  async getActionRequired(): Promise<ATRecord[]> {
    return getAll(T.BOOKINGS, {
      filterByFormula: `AND({🔔 Action Due Today}=1,NOT(OR({Status}="COMPLETED",{Status}="CANCELLED")))`,
    })
  },

  async getById(id: string): Promise<ATRecord> {
    return getOne(T.BOOKINGS, id)
  },

  async flag(id: string, reason: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.BOOKINGS, id, { Flagged: true, Flag_Reason: reason })
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
      'sort[0][field]': 'Timestamp',
      'sort[0][direction]': 'desc',
      maxRecords: String(limit),
    })
  },

  async getUnresolved(): Promise<ATRecord[]> {
    return getAll(T.AUDIT_LOG, {
      filterByFormula: `AND({Follow-up Required}=1,OR({Severity Level}="ERROR",{Severity Level}="CRITICAL"))`,
    })
  },

  async resolve(id: string, actor: string): Promise<ATRecord> {
    const record = await patch(T.AUDIT_LOG, id, { 'Follow-up Required': false })
    await log('ISSUE_RESOLVED', 'AuditLog', id, actor)
    return record
  },
}

// ─── Approvals ───────────────────────────────────────────────────────────────

export const approvals = {
  async getPending(): Promise<ATRecord[]> {
    return getAll(T.APPROVALS, {
      filterByFormula: `{Status/Outcome}="PENDING"`,
    })
  },

  async decide(id: string, approved: boolean, actor: string, note?: string): Promise<ATRecord> {
    const status = approved ? 'APPROVED' : 'REJECTED'
    const record = await patch(T.APPROVALS, id, {
      'Status/Outcome': status,
      'Founder Name': actor,
      'Decision Note': note ?? '',
    })
    await log('APPROVAL_DECISION', 'Approval', id, actor, `${status}${note ? ': ' + note : ''}`)
    return record
  },
}

// ─── Issues ──────────────────────────────────────────────────────────────────

export const issues = {
  async getOpen(): Promise<ATRecord[]> {
    return getAll(T.ISSUES, {
      filterByFormula: `NOT({Status}="RESOLVED")`,
    })
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
      const sla: SLAStatus = 'GREEN'
      const firstName = (f['First Name'] as string) ?? ''
      const lastName = (f['Last Name'] as string) ?? ''
      const fullName = `${firstName} ${lastName}`.trim() || 'Unnamed Lead'
      items.push({
        id: r.id,
        source: 'lead',
        priority: slaScore(sla) + 10,
        title: fullName,
        subtitle: `${f.Status ?? ''} · ${f['Preferred Date'] ?? ''}`.replace(/^ · | · $/g, ''),
        sla,
        href: `/concierge/leads/${r.id}`,
        badge: f['Lead Source'] as string | undefined,
      })
    }
  }

  if (bookingsRes.status === 'fulfilled') {
    for (const r of bookingsRes.value) {
      const f = r.fields
      const sla: SLAStatus = 'GREEN'
      items.push({
        id: r.id,
        source: 'booking',
        priority: slaScore(sla) + 20,
        title: (f['Booking ID'] as string) ?? 'Booking',
        subtitle: `${f['Client Name'] ?? ''} · ${f['Charter Date'] ?? ''}`.replace(/^ · | · $/g, ''),
        sla,
        href: `/operations/charters`,
        badge: f['Emergency_Flag'] ? 'FLAGGED' : undefined,
      })
    }
  }

  if (approvalsRes.status === 'fulfilled') {
    for (const r of approvalsRes.value) {
      const f = r.fields
      items.push({
        id: r.id,
        source: 'approval',
        priority: 80,
        title: (f['Request Title'] as string) ?? 'Approval Required',
        subtitle: (f['Context'] as string) ?? '',
        sla: 'WARNING',
        href: `/owner/dashboard`,
        badge: 'APPROVAL',
      })
    }
  }

  if (issuesRes.status === 'fulfilled') {
    for (const r of issuesRes.value) {
      const f = r.fields
      const severity = f.Severity as string | undefined
      items.push({
        id: r.id,
        source: 'issue',
        priority: severity === 'CRITICAL' ? 90 : severity === 'HIGH' ? 70 : 40,
        title: (f.Title as string) ?? 'Open Issue',
        subtitle: (f.Description as string) ?? '',
        sla: severity === 'CRITICAL' ? 'BREACHED' : severity === 'HIGH' ? 'WARNING' : 'GREEN',
        href: `/operations/charters`,
        badge: severity,
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
      ? bookingsRes.value.reduce((sum, r) => sum + ((r.fields['Total Cost'] as number) ?? 0), 0)
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
