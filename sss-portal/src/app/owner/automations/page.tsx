import type { Metadata } from 'next'
import { Workflow, AlertTriangle, CheckCircle, HelpCircle } from 'lucide-react'

export const metadata: Metadata = { title: 'Automation Registry' }

type AutoStatus = 'active' | 'needs-test' | 'missing'
type Risk = 'low' | 'medium' | 'high'

interface Automation {
  id: string
  name: string
  trigger: string
  portalAction: string
  tablesRead: string[]
  tablesWritten: string[]
  payloadFields: string[]
  status: AutoStatus
  risk: Risk
  notes: string
  lastTested?: string
}

const AUTOMATIONS: Automation[] = [
  {
    id: 'lead-qualify',
    name: 'Lead Qualification → Booking Creation',
    trigger: 'POST /api/leads/[id]/qualify',
    portalAction: 'Qualify Lead button on Lead Detail page',
    tablesRead: ['Requests (tblTlSB9CO4dTGodg)'],
    tablesWritten: ['Requests → Status=BOOKED', 'Audit Log (entry created)'],
    payloadFields: ['leadId', 'actor'],
    status: 'needs-test',
    risk: 'high',
    notes: 'Triggers booking creation flow in Make. Status set to BOOKED in Airtable. Confirm Make scenario watches for Status=BOOKED on Requests table.',
    lastTested: undefined,
  },
  {
    id: 'lead-status',
    name: 'Lead Status Change',
    trigger: 'PATCH /api/leads/[id] { status }',
    portalAction: 'Status dropdown + Save on Lead Detail page',
    tablesRead: ['Requests (tblTlSB9CO4dTGodg)'],
    tablesWritten: ['Requests → Status field', 'Audit Log'],
    payloadFields: ['status', 'actor'],
    status: 'active',
    risk: 'low',
    notes: 'Only writes Status field. Does not trigger Make webhook directly — Make should watch Airtable for Status changes.',
  },
  {
    id: 'lead-notes',
    name: 'Lead Notes Save',
    trigger: 'PATCH /api/leads/[id] { notes }',
    portalAction: 'Notes field + Save on Lead Detail page',
    tablesRead: ['Requests (tblTlSB9CO4dTGodg)'],
    tablesWritten: ['Requests → Notes field', 'Audit Log'],
    payloadFields: ['notes', 'actor'],
    status: 'active',
    risk: 'low',
    notes: 'Saves to Notes field only.',
  },
  {
    id: 'booking-flag',
    name: 'Charter Emergency Flag',
    trigger: 'POST /api/bookings/[id]/flag { reason }',
    portalAction: 'Flag button on Charters list',
    tablesRead: ['Bookings (tbl72omPibBkn2hZL)'],
    tablesWritten: ['Bookings → Emergency_Flag=true, Charter_Notes', 'Audit Log → BOOKING_FLAGGED WARNING'],
    payloadFields: ['reason', 'actor'],
    status: 'needs-test',
    risk: 'medium',
    notes: 'Sets Emergency_Flag checkbox and writes reason to Charter_Notes. Make should watch Emergency_Flag for alerts.',
  },
  {
    id: 'booking-notes',
    name: 'Charter Notes Update',
    trigger: 'PATCH /api/bookings/[id]/notes { notes }',
    portalAction: 'Charter Notes form on Charter Detail page',
    tablesRead: ['Bookings (tbl72omPibBkn2hZL)'],
    tablesWritten: ['Bookings → Charter Notes field', 'Audit Log'],
    payloadFields: ['notes', 'actor'],
    status: 'active',
    risk: 'low',
    notes: 'Writes to Charter Notes text field.',
  },
  {
    id: 'approval-decide',
    name: 'Founder Decision (Approve/Deny)',
    trigger: 'POST /api/approvals/[id] { approved, note }',
    portalAction: 'Approve / Deny buttons on Approvals page',
    tablesRead: ['Founder Decisions (tblFCE26qDwfp4Jwd)'],
    tablesWritten: ['Founder Decisions → Decision, Decision Note, Founder Name, Decided At', 'Audit Log → APPROVAL_DECISION'],
    payloadFields: ['approved', 'note', 'actor'],
    status: 'needs-test',
    risk: 'high',
    notes: 'Sets Decision to APPROVED or DENIED plus timestamp. Make should watch Decision field to trigger downstream flows (contracts, notifications, etc.).',
  },
  {
    id: 'issue-resolve',
    name: 'Issue Resolution',
    trigger: 'PATCH /api/issues/[id] { action: "resolve", note }',
    portalAction: 'Mark Resolved button on Issues page',
    tablesRead: ['Incident_Reports (tblO22Hh9lSTnhuu7)'],
    tablesWritten: ['Incident_Reports → Resolved_At, Will_Notes', 'Audit Log → ISSUE_RESOLVED'],
    payloadFields: ['note', 'actor'],
    status: 'needs-test',
    risk: 'medium',
    notes: 'Sets Resolved_At to today\'s date. Make should watch Resolved_At to send closure notifications.',
  },
  {
    id: 'issue-note',
    name: 'Issue Note Save',
    trigger: 'PATCH /api/issues/[id] { action: "note", note }',
    portalAction: 'Save Note button on Issues page',
    tablesRead: ['Incident_Reports (tblO22Hh9lSTnhuu7)'],
    tablesWritten: ['Incident_Reports → Will_Notes', 'Audit Log → ISSUE_NOTE_SAVED'],
    payloadFields: ['note', 'actor'],
    status: 'active',
    risk: 'low',
    notes: 'Saves Will_Notes field only.',
  },
]

const STATUS_ICON = {
  active: <CheckCircle className="h-4 w-4 text-emerald-400" />,
  'needs-test': <HelpCircle className="h-4 w-4 text-amber-400" />,
  missing: <AlertTriangle className="h-4 w-4 text-red-400" />,
}

const STATUS_LABEL = {
  active: 'Active',
  'needs-test': 'Needs Test',
  missing: 'Missing',
}

const RISK_COLOR: Record<Risk, string> = {
  low: 'text-[#505050] bg-[#1a1a1a]',
  medium: 'text-amber-400 bg-amber-950',
  high: 'text-red-400 bg-red-950',
}

export default function AutomationsPage() {
  const active = AUTOMATIONS.filter((a) => a.status === 'active').length
  const needsTest = AUTOMATIONS.filter((a) => a.status === 'needs-test').length

  return (
    <div className="p-8 max-w-[1000px]">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <Workflow className="h-5 w-5 text-[#c9a96e]" />
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Automation Registry</h1>
        </div>
        <p className="text-sm text-[#505050]">
          Read-only map of portal actions and their Airtable/Make.com integrations
        </p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-3 mb-8">
        <div className="bg-[#141414] border border-[#252525] rounded-xl p-4 text-center">
          <div className="text-2xl font-light text-[#f0ede8]">{AUTOMATIONS.length}</div>
          <div className="text-xs text-[#505050] mt-1">Total automations mapped</div>
        </div>
        <div className="bg-[#141414] border border-[#252525] rounded-xl p-4 text-center">
          <div className="text-2xl font-light text-emerald-400">{active}</div>
          <div className="text-xs text-[#505050] mt-1">Active</div>
        </div>
        <div className="bg-[#141414] border border-amber-950 rounded-xl p-4 text-center">
          <div className="text-2xl font-light text-amber-400">{needsTest}</div>
          <div className="text-xs text-[#505050] mt-1">Need verification</div>
        </div>
      </div>

      <div className="space-y-4">
        {AUTOMATIONS.map((a) => (
          <div key={a.id} className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <div className="flex items-start justify-between gap-4 mb-3">
              <div className="flex items-center gap-2">
                {STATUS_ICON[a.status]}
                <h2 className="text-sm font-medium text-[#f0ede8]">{a.name}</h2>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${RISK_COLOR[a.risk]}`}>
                  {a.risk} risk
                </span>
                <span className="text-xs text-[#505050]">{STATUS_LABEL[a.status]}</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2 text-xs mb-3">
              <div>
                <span className="text-[#404040] uppercase tracking-widest">Trigger</span>
                <p className="text-[#606060] mt-0.5 font-mono">{a.trigger}</p>
              </div>
              <div>
                <span className="text-[#404040] uppercase tracking-widest">Portal Action</span>
                <p className="text-[#606060] mt-0.5">{a.portalAction}</p>
              </div>
              <div>
                <span className="text-[#404040] uppercase tracking-widest">Tables Read</span>
                <p className="text-[#606060] mt-0.5">{a.tablesRead.join(', ')}</p>
              </div>
              <div>
                <span className="text-[#404040] uppercase tracking-widest">Tables Written</span>
                <p className="text-[#606060] mt-0.5">{a.tablesWritten.join(', ')}</p>
              </div>
              <div>
                <span className="text-[#404040] uppercase tracking-widest">Payload Fields</span>
                <p className="text-[#606060] mt-0.5 font-mono">{a.payloadFields.join(', ')}</p>
              </div>
              {a.lastTested && (
                <div>
                  <span className="text-[#404040] uppercase tracking-widest">Last Tested</span>
                  <p className="text-[#606060] mt-0.5">{a.lastTested}</p>
                </div>
              )}
            </div>

            {a.notes && (
              <div className="bg-[#0f0f0f] border border-[#1e1e1e] rounded-lg px-3 py-2">
                <p className="text-xs text-[#505050]">{a.notes}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      <p className="text-xs text-[#303030] text-center mt-8">
        This page is read-only. Webhook URLs and payloads are not modified here.
        To update Make.com scenarios, use the Make.com dashboard.
      </p>
    </div>
  )
}
