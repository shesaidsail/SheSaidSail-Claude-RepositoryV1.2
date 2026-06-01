import type { Metadata } from 'next'
import Link from 'next/link'
import { Users, ChevronRight } from 'lucide-react'
import { leads } from '@/lib/airtable'
import { StatusBadge } from '@/components/ui/badge'
import { fmtDate, timeAgo } from '@/lib/utils'

export const metadata: Metadata = { title: 'Lead Board' }

function leadName(f: Record<string, unknown>): string {
  const first = (f['First Name'] as string) ?? ''
  const last = (f['Last Name'] as string) ?? ''
  return [first, last].filter(Boolean).join(' ') || 'Unknown'
}

function selectName(v: unknown): string {
  if (!v) return ''
  if (typeof v === 'string') return v
  if (typeof v === 'object' && v !== null && 'name' in v) return (v as { name: string }).name
  return ''
}

export default async function LeadBoardPage() {
  const allLeads = await leads.getActive()

  const sorted = allLeads.sort(
    (a, b) => new Date(b.createdTime).getTime() - new Date(a.createdTime).getTime()
  )

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Users className="h-5 w-5 text-[#c9a96e]" />
            <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Lead Board</h1>
          </div>
          <p className="text-sm text-[#505050]">
            {allLeads.length} active lead{allLeads.length !== 1 ? 's' : ''}
          </p>
        </div>
      </div>

      {allLeads.length === 0 ? (
        <div className="bg-[#141414] border border-[#252525] rounded-xl px-8 py-16 text-center">
          <p className="text-sm text-[#505050]">No active leads at the moment.</p>
        </div>
      ) : (
        <div className="bg-[#141414] border border-[#252525] rounded-xl overflow-hidden">
          <div className="grid grid-cols-[1fr_auto_auto_auto] gap-4 px-5 py-3 border-b border-[#1e1e1e] text-xs font-medium uppercase tracking-widest text-[#404040]">
            <span>Lead</span>
            <span className="text-right">Preferred Date</span>
            <span className="text-right">Status</span>
            <span />
          </div>

          {sorted.map((record) => {
            const f = record.fields
            const status = (f.Status as string) ?? ''
            const attention = f['🔔 Response Needed'] as boolean | undefined

            return (
              <Link
                key={record.id}
                href={`/concierge/leads/${record.id}`}
                className="grid grid-cols-[1fr_auto_auto_auto] gap-4 items-center px-5 py-3.5 border-b border-[#1a1a1a] last:border-0 hover:bg-[#161616] transition-colors group"
              >
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    {attention && (
                      <div className="h-1.5 w-1.5 rounded-full bg-red-400 flex-shrink-0" />
                    )}
                    <span className="text-sm font-medium text-[#f0ede8] truncate">
                      {leadName(f)}
                    </span>
                  </div>
                  <div className="text-xs text-[#505050] mt-0.5">
                    {(f.Experience as string) ?? '—'} ·{' '}
                    {(f['Guest Count'] as number)
                      ? `${f['Guest Count']} guests`
                      : '—'}{' '}
                    · {timeAgo(record.createdTime)}
                  </div>
                </div>
                <span className="text-sm text-[#808080] text-right">
                  {fmtDate(f['Preferred Date'] as string)}
                </span>
                <div className="flex justify-end">
                  <StatusBadge status={status || 'NEW'} />
                </div>
                <ChevronRight className="h-4 w-4 text-[#303030] group-hover:text-[#606060] transition-colors" />
              </Link>
            )
          })}
        </div>
      )}
    </div>
  )
}
