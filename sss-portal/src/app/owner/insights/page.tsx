import type { Metadata } from 'next'
import { TrendingUp, AlertCircle, Users, Anchor, DollarSign, Target, Clock } from 'lucide-react'
import { leads, bookings, approvals, issues } from '@/lib/airtable'
import { fmt$, fmtDate } from '@/lib/utils'

export const metadata: Metadata = { title: 'Insights' }

function safe(v: unknown, fallback = '—'): string {
  if (v === null || v === undefined || v === '') return fallback
  return String(v)
}

function safeNum(v: unknown): number {
  const n = Number(v)
  return isNaN(n) ? 0 : n
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

function MetricCard({
  label,
  value,
  sub,
  accent = 'default',
}: {
  label: string
  value: string | number
  sub?: string
  accent?: 'default' | 'gold' | 'green' | 'red' | 'amber'
}) {
  const valueColor = {
    default: 'text-[#f0ede8]',
    gold: 'text-[#c9a96e]',
    green: 'text-emerald-400',
    red: 'text-red-400',
    amber: 'text-amber-400',
  }[accent]

  return (
    <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
      <div className="text-xs text-[#505050] uppercase tracking-widest mb-2">{label}</div>
      <div className={`text-2xl font-light ${valueColor}`}>{value}</div>
      {sub && <div className="text-xs text-[#404040] mt-1">{sub}</div>}
    </div>
  )
}

function SectionHeader({ icon, title }: { icon: React.ReactNode; title: string }) {
  return (
    <div className="flex items-center gap-2 mb-3">
      <span className="text-[#c9a96e]">{icon}</span>
      <h2 className="text-sm font-medium text-[#f0ede8] uppercase tracking-widest">{title}</h2>
    </div>
  )
}

function Row({ label, value, highlight }: { label: string; value: string; highlight?: boolean }) {
  return (
    <div className="flex items-start justify-between py-2.5 border-b border-[#1a1a1a] last:border-0 gap-4">
      <span className="text-sm text-[#606060] flex-shrink-0">{label}</span>
      <span className={`text-sm text-right ${highlight ? 'text-amber-400' : 'text-[#f0ede8]'}`}>{value}</span>
    </div>
  )
}

export default async function InsightsPage() {
  const [leadsRes, bookingsRes, approvalsRes, issuesRes] = await Promise.allSettled([
    leads.getActive(),
    bookings.getActive(),
    approvals.getPending(),
    issues.getOpen(),
  ])

  const allLeads = leadsRes.status === 'fulfilled' ? leadsRes.value : []
  const allBookings = bookingsRes.status === 'fulfilled' ? bookingsRes.value : []
  const pendingApprovals = approvalsRes.status === 'fulfilled' ? approvalsRes.value : []
  const openIssues = issuesRes.status === 'fulfilled' ? issuesRes.value : []

  // ── Lead analytics ──────────────────────────────────────────────────────────
  const leadsByStatus = allLeads.reduce<Record<string, number>>((acc, r) => {
    const s = safe(r.fields.Status, 'UNKNOWN')
    acc[s] = (acc[s] ?? 0) + 1
    return acc
  }, {})

  const leadsBySource = allLeads.reduce<Record<string, number>>((acc, r) => {
    const s = selectName(r.fields['Lead Source']) || 'Unknown'
    acc[s] = (acc[s] ?? 0) + 1
    return acc
  }, {})

  const hotLeads = allLeads.filter((r) => r.fields['🔔 Response Needed'])
  const newLeads = allLeads.filter((r) => r.fields.Status === 'NEW')
  const qualifiedLeads = allLeads.filter((r) => r.fields.Status === 'QUALIFIED')
  const bookedLeads = allLeads.filter((r) => r.fields.Status === 'BOOKED')
  const closedLeads = allLeads.filter((r) => r.fields.Status === 'CLOSED')

  const totalLeadCount = allLeads.length + closedLeads.length
  const closeRate = totalLeadCount > 0
    ? Math.round((bookedLeads.length / totalLeadCount) * 100)
    : 0

  // Leads missing follow-up data (no Preferred Date)
  const missingDate = allLeads.filter((r) => !r.fields['Preferred Date'])

  // ── Booking analytics ───────────────────────────────────────────────────────
  const bookedRevenue = allBookings.reduce((sum, r) => sum + safeNum(r.fields['Package Price']), 0)
  const avgBookingValue = allBookings.length > 0
    ? Math.round(bookedRevenue / allBookings.length)
    : 0

  const charters_missing_client = allBookings.filter((r) => {
    const cn = r.fields['Client Name']
    return !cn || (Array.isArray(cn) && cn.length === 0)
  })
  const charters_missing_price = allBookings.filter((r) => !safeNum(r.fields['Package Price']))
  const charters_flagged = allBookings.filter((r) => r.fields['Emergency_Flag'])

  // ── Issues analytics ────────────────────────────────────────────────────────
  const criticalIssues = openIssues.filter((r) => selectName(r.fields.Severity) === 'Critical')
  const highIssues = openIssues.filter((r) => selectName(r.fields.Severity) === 'High')

  // ── Today's priority list ───────────────────────────────────────────────────
  const todayPriorities: { text: string; level: 'critical' | 'warning' | 'info' }[] = []

  if (criticalIssues.length > 0)
    todayPriorities.push({ text: `${criticalIssues.length} critical issue${criticalIssues.length > 1 ? 's' : ''} open`, level: 'critical' })
  if (pendingApprovals.length > 0)
    todayPriorities.push({ text: `${pendingApprovals.length} approval${pendingApprovals.length > 1 ? 's' : ''} awaiting decision`, level: 'warning' })
  if (hotLeads.length > 0)
    todayPriorities.push({ text: `${hotLeads.length} lead${hotLeads.length > 1 ? 's' : ''} flagged for immediate response`, level: 'warning' })
  if (charters_flagged.length > 0)
    todayPriorities.push({ text: `${charters_flagged.length} charter${charters_flagged.length > 1 ? 's' : ''} flagged for attention`, level: 'warning' })
  if (highIssues.length > 0)
    todayPriorities.push({ text: `${highIssues.length} high-severity issue${highIssues.length > 1 ? 's' : ''} open`, level: 'info' })
  if (missingDate.length > 0)
    todayPriorities.push({ text: `${missingDate.length} lead${missingDate.length > 1 ? 's' : ''} missing preferred date`, level: 'info' })
  if (charters_missing_price.length > 0)
    todayPriorities.push({ text: `${charters_missing_price.length} booking${charters_missing_price.length > 1 ? 's' : ''} missing package price`, level: 'info' })
  if (todayPriorities.length === 0)
    todayPriorities.push({ text: 'All clear — no urgent actions today', level: 'info' })

  const priorityColor = { critical: 'text-red-400', warning: 'text-amber-400', info: 'text-[#606060]' }
  const priorityDot = { critical: 'bg-red-400', warning: 'bg-amber-400', info: 'bg-[#404040]' }

  return (
    <div className="p-8 max-w-[1100px]">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <TrendingUp className="h-5 w-5 text-[#c9a96e]" />
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Smart Insights</h1>
        </div>
        <p className="text-sm text-[#505050]">Live view of your business from Airtable data</p>
      </div>

      {/* Today's Priorities */}
      <div className="bg-[#0f0f0f] border border-[#252525] rounded-xl p-5 mb-8">
        <SectionHeader icon={<Target className="h-4 w-4" />} title="Today's Priority Actions" />
        <div className="space-y-2">
          {todayPriorities.map((p, i) => (
            <div key={i} className="flex items-center gap-3">
              <div className={`h-1.5 w-1.5 rounded-full flex-shrink-0 ${priorityDot[p.level]}`} />
              <span className={`text-sm ${priorityColor[p.level]}`}>{p.text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Revenue Metrics */}
      <div className="mb-8">
        <SectionHeader icon={<DollarSign className="h-4 w-4" />} title="Revenue" />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <MetricCard label="Booked Revenue" value={fmt$(bookedRevenue)} accent="green" sub="Active bookings" />
          <MetricCard label="Active Bookings" value={allBookings.length} accent="gold" />
          <MetricCard label="Avg Booking Value" value={avgBookingValue > 0 ? fmt$(avgBookingValue) : 'Needs data'} accent="default" />
          <MetricCard label="Close Rate" value={closeRate > 0 ? `${closeRate}%` : 'Needs data'} accent="default" sub="Booked / total leads" />
        </div>
      </div>

      {/* Lead Metrics */}
      <div className="mb-8">
        <SectionHeader icon={<Users className="h-4 w-4" />} title="Leads" />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-4">
          <MetricCard label="Total Active" value={allLeads.length} />
          <MetricCard label="Needs Response" value={hotLeads.length} accent={hotLeads.length > 0 ? 'amber' : 'default'} />
          <MetricCard label="Qualified" value={qualifiedLeads.length} accent="gold" />
          <MetricCard label="Missing Date" value={missingDate.length} accent={missingDate.length > 0 ? 'amber' : 'default'} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* By Status */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
            <div className="text-xs text-[#505050] uppercase tracking-widest mb-3">By Status</div>
            {Object.keys(leadsByStatus).length === 0 ? (
              <p className="text-sm text-[#404040]">Needs data</p>
            ) : (
              Object.entries(leadsByStatus)
                .sort((a, b) => b[1] - a[1])
                .map(([s, n]) => <Row key={s} label={s} value={String(n)} />)
            )}
          </div>
          {/* By Source */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
            <div className="text-xs text-[#505050] uppercase tracking-widest mb-3">By Source</div>
            {Object.keys(leadsBySource).length === 0 ? (
              <p className="text-sm text-[#404040]">Needs data</p>
            ) : (
              Object.entries(leadsBySource)
                .sort((a, b) => b[1] - a[1])
                .map(([s, n]) => <Row key={s} label={s || 'Unknown'} value={String(n)} />)
            )}
          </div>
        </div>

        {/* Hot leads list */}
        {hotLeads.length > 0 && (
          <div className="bg-[#141414] border border-amber-950 rounded-xl p-4 mt-4">
            <div className="text-xs text-amber-400 uppercase tracking-widest mb-3">Hot Leads — Immediate Response Needed</div>
            {hotLeads.slice(0, 10).map((r) => {
              const name = [r.fields['First Name'], r.fields['Last Name']].filter(Boolean).join(' ') || 'Unknown'
              return (
                <div key={r.id} className="flex items-center justify-between py-2 border-b border-[#1a1a1a] last:border-0">
                  <span className="text-sm text-[#f0ede8]">{name}</span>
                  <span className="text-xs text-[#505050]">{safe(r.fields['Preferred Date'], 'No date')}</span>
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Charters */}
      <div className="mb-8">
        <SectionHeader icon={<Anchor className="h-4 w-4" />} title="Charters at Risk" />
        {charters_flagged.length === 0 && charters_missing_price.length === 0 && charters_missing_client.length === 0 ? (
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5 text-center">
            <p className="text-sm text-[#404040]">No data gaps detected in active bookings.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
              <div className="text-xs text-[#505050] uppercase tracking-widest mb-3">Flagged</div>
              <div className="text-2xl font-light text-red-400">{charters_flagged.length}</div>
              <div className="text-xs text-[#404040] mt-1">Emergency flag set</div>
            </div>
            <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
              <div className="text-xs text-[#505050] uppercase tracking-widest mb-3">Missing Price</div>
              <div className={`text-2xl font-light ${charters_missing_price.length > 0 ? 'text-amber-400' : 'text-[#f0ede8]'}`}>{charters_missing_price.length}</div>
              <div className="text-xs text-[#404040] mt-1">No Package Price set</div>
            </div>
            <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
              <div className="text-xs text-[#505050] uppercase tracking-widest mb-3">Missing Client</div>
              <div className={`text-2xl font-light ${charters_missing_client.length > 0 ? 'text-amber-400' : 'text-[#f0ede8]'}`}>{charters_missing_client.length}</div>
              <div className="text-xs text-[#404040] mt-1">No client linked</div>
            </div>
          </div>
        )}
      </div>

      {/* Issues & Approvals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div>
          <SectionHeader icon={<AlertCircle className="h-4 w-4" />} title="Open Issues" />
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
            {openIssues.length === 0 ? (
              <p className="text-sm text-[#404040] text-center py-4">No open issues.</p>
            ) : (
              openIssues.slice(0, 8).map((r) => (
                <div key={r.id} className="flex items-center justify-between py-2 border-b border-[#1a1a1a] last:border-0">
                  <span className="text-sm text-[#f0ede8]">{safe(r.fields.Incident_ID, r.id.slice(-6))}</span>
                  <span className={`text-xs ${selectName(r.fields.Severity) === 'Critical' ? 'text-red-400' : selectName(r.fields.Severity) === 'High' ? 'text-amber-400' : 'text-[#505050]'}`}>
                    {selectName(r.fields.Severity) || 'Unknown'}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>

        <div>
          <SectionHeader icon={<Clock className="h-4 w-4" />} title="Pending Approvals" />
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-4">
            {pendingApprovals.length === 0 ? (
              <p className="text-sm text-[#404040] text-center py-4">No pending approvals.</p>
            ) : (
              pendingApprovals.slice(0, 8).map((r) => (
                <div key={r.id} className="flex items-center justify-between py-2 border-b border-[#1a1a1a] last:border-0">
                  <span className="text-sm text-[#f0ede8] truncate">{safe(r.fields['Request Title'], 'Approval')}</span>
                  <span className={`text-xs flex-shrink-0 ml-2 ${selectName(r.fields.Urgency) === 'IMMEDIATE' ? 'text-red-400' : selectName(r.fields.Urgency) === 'TODAY' ? 'text-amber-400' : 'text-[#505050]'}`}>
                    {selectName(r.fields.Urgency) || '—'}
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {leadsRes.status === 'rejected' || bookingsRes.status === 'rejected' ? (
        <p className="text-xs text-[#404040] text-center mt-4">Some data could not be loaded from Airtable — partial results shown.</p>
      ) : null}
    </div>
  )
}
