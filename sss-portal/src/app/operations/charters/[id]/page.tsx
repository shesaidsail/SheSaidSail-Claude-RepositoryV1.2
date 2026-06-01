import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, Flag } from 'lucide-react'
import { bookings, activity } from '@/lib/airtable'
import { StatusBadge, Badge } from '@/components/ui/badge'
import { fmtDate, fmt$ } from '@/lib/utils'
import { ActivityFeedItem } from '@/components/ui/activity-feed'
import { CharterNoteForm } from './charter-note-form'

export const metadata: Metadata = { title: 'Charter Detail' }

function lookupFirst(v: unknown): string {
  if (Array.isArray(v)) return (v[0] as string) ?? '—'
  if (typeof v === 'string') return v
  return '—'
}

function lookupAll(v: unknown): string {
  if (Array.isArray(v)) return (v as string[]).join(', ') || '—'
  if (typeof v === 'string') return v
  return '—'
}

export default async function CharterDetailPage({ params }: { params: { id: string } }) {
  let record
  try {
    record = await bookings.getById(params.id)
  } catch {
    notFound()
  }

  const f = record.fields
  const flagged = f.Emergency_Flag as boolean | undefined

  // Fetch related activity log entries that reference this booking
  const recentActivity = await activity.getRecent(100).catch(() => [])
  const relatedActivity = recentActivity.filter(
    (r) => r.fields.Entity_ID === record.id || r.fields.Entity_ID === f['Booking ID']
  )

  return (
    <div className="p-8 max-w-[1000px]">
      <Link
        href="/operations/charters"
        className="inline-flex items-center gap-1.5 text-sm text-[#505050] hover:text-[#f0ede8] transition-colors mb-6"
      >
        <ArrowLeft className="h-4 w-4" />
        Charter Board
      </Link>

      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <div className="flex items-center gap-2 mb-1">
            {flagged && <Flag className="h-4 w-4 text-red-400" />}
            <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">
              {(f['Booking ID'] as string) ?? record.id.slice(-8).toUpperCase()}
            </h1>
          </div>
          <p className="text-sm text-[#505050]">
            {lookupFirst(f['Client Name'])} · {fmtDate(f['Charter Date'] as string)}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {flagged && <Badge variant="red">FLAGGED</Badge>}
          <StatusBadge status={(f.Status as string) ?? 'ACTIVE'} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-5">
          {/* Charter details */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Charter Details
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <Detail label="Charter Date" value={fmtDate(f['Charter Date'] as string)} />
              <Detail label="Yacht" value={(f['Yacht Name'] as string) ?? '—'} />
              <Detail label="Port of Call" value={(f['Port of Call'] as string) ?? '—'} />
              <Detail label="Guest Count" value={(f['Guest Count'] as number)?.toString() ?? '—'} />
              <Detail label="Lead Source" value={(f['Lead Source'] as { name?: string })?.name ?? '—'} />
              <Detail label="Brand" value={(f.Brand as { name?: string })?.name ?? '—'} />
              <Detail label="Occasion" value={(f.Occasion as { name?: string })?.name ?? '—'} />
              <Detail label="HV Booking" value={f['HV Booking'] ? 'Yes' : 'No'} />
            </div>
          </div>

          {/* Client */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Client
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <Detail label="Name" value={lookupAll(f['Client Name'])} />
              <Detail label="Email" value={lookupAll(f['Client Email'])} />
              <Detail label="Phone" value={lookupAll(f['Client Phone'])} />
              <Detail label="Referred By" value={(f['Referred By'] as string) ?? '—'} />
            </div>
          </div>

          {/* Financials */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Financials
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <Detail label="Package Price" value={fmt$(f['Package Price'] as number)} />
              <Detail label="Total Cost" value={fmt$(f['Total Cost'] as number)} />
              <Detail label="Net Profit" value={fmt$(f['Net Profit'] as number)} />
              <Detail label="Deposit Amount" value={fmt$(f['Deposit Amount'] as number)} />
              <Detail label="Balance Paid" value={f['Balance Paid'] ? 'Yes' : 'No'} />
              <Detail
                label="Balance Due"
                value={f['Balance Due Date'] ? fmtDate(f['Balance Due Date'] as string) : '—'}
              />
            </div>
          </div>

          {/* Operations checklist */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Operations
            </h2>
            <div className="grid grid-cols-2 gap-3">
              <CheckItem label="Agreement Sent" checked={f['Agreement_Sent'] as boolean} />
              <CheckItem label="Agreement Signed" checked={f['Agreement_Signed'] as boolean} />
              <CheckItem label="Confirmation Sent" checked={f['Confirmation_Sent'] as boolean} />
              <CheckItem label="Concierge Assigned" checked={f['Concierge_Assigned'] as boolean} />
              <CheckItem label="T7 Confirmed" checked={f['T7_Confirmed'] as boolean} />
              <CheckItem label="T48 Captain Confirmed" checked={f['T48_Captain_Confirmed'] as boolean} />
              <CheckItem label="Charter Brief Sent" checked={f['Charter_Brief_Sent'] as boolean} />
              <CheckItem label="Balance Paid" checked={f['Balance Paid'] as boolean} />
            </div>
          </div>

          {/* Charter notes */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Charter Notes
            </h2>
            {f['Charter Notes'] ? (
              <p className="text-sm text-[#a09a90] whitespace-pre-wrap leading-relaxed mb-4">
                {f['Charter Notes'] as string}
              </p>
            ) : null}
            <CharterNoteForm bookingId={record.id} currentNote={(f['Charter Notes'] as string) ?? ''} />
          </div>

          {f['Flagged'] || flagged ? (
            <div className="bg-red-950/30 border border-red-900 rounded-xl p-5">
              <h2 className="text-xs font-medium uppercase tracking-widest text-red-400 mb-3">
                ⚑ Flag Notes
              </h2>
              <p className="text-sm text-[#a09a90]">{(f.Charter_Notes as string) ?? '—'}</p>
            </div>
          ) : null}
        </div>

        {/* Sidebar */}
        <div className="space-y-5">
          {/* Broker */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-3">
              Broker
            </h2>
            <p className="text-sm text-[#f0ede8]">
              {(f['Broker Name'] as string) ?? lookupAll(f.Broker) ?? '—'}
            </p>
          </div>

          {/* Add-ons */}
          {f['Add-ons'] && Array.isArray(f['Add-ons']) && (f['Add-ons'] as string[]).length > 0 ? (
            <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
              <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-3">
                Add-ons
              </h2>
              <div className="flex flex-wrap gap-1.5">
                {(f['Add-ons'] as Array<{ name: string }>).map((a, i) => (
                  <Badge key={i} variant="default">
                    {typeof a === 'string' ? a : a.name}
                  </Badge>
                ))}
              </div>
            </div>
          ) : null}

          {/* Activity log */}
          {relatedActivity.length > 0 ? (
            <div className="bg-[#141414] border border-[#252525] rounded-xl overflow-hidden">
              <div className="px-5 py-4 border-b border-[#1e1e1e]">
                <h2 className="text-sm font-medium text-[#f0ede8]">Activity</h2>
              </div>
              <div className="px-5 py-2 max-h-[300px] overflow-y-auto">
                {relatedActivity.map((r) => (
                  <ActivityFeedItem key={r.id} record={r} />
                ))}
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-xs text-[#505050] mb-0.5">{label}</div>
      <div className="text-sm text-[#f0ede8]">{value}</div>
    </div>
  )
}

function CheckItem({ label, checked }: { label: string; checked: boolean | undefined }) {
  return (
    <div className="flex items-center gap-2">
      <div
        className={`h-4 w-4 rounded flex items-center justify-center flex-shrink-0 ${
          checked ? 'bg-emerald-900 text-emerald-400' : 'bg-[#1c1c1c] border border-[#303030]'
        }`}
      >
        {checked && <span className="text-[10px]">✓</span>}
      </div>
      <span className={`text-xs ${checked ? 'text-[#808080]' : 'text-[#505050]'}`}>{label}</span>
    </div>
  )
}
