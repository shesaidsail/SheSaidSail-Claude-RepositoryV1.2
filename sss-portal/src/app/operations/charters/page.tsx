import type { Metadata } from 'next'
import Link from 'next/link'
import { Anchor } from 'lucide-react'
import { bookings } from '@/lib/airtable'
import { StatusBadge } from '@/components/ui/badge'
import { fmtDate, fmt$ } from '@/lib/utils'
import { FlagBookingButton } from './flag-booking-button'

export const metadata: Metadata = { title: 'Charter Board' }

function lookupFirst(v: unknown): string {
  if (Array.isArray(v)) return (v[0] as string) ?? '—'
  if (typeof v === 'string') return v
  return '—'
}

export default async function CharterBoardPage() {
  const activeBookings = await bookings.getActive()

  const sorted = [...activeBookings].sort((a, b) => {
    const dateA = new Date((a.fields['Charter Date'] as string) ?? 0).getTime()
    const dateB = new Date((b.fields['Charter Date'] as string) ?? 0).getTime()
    return dateA - dateB
  })

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Anchor className="h-5 w-5 text-[#c9a96e]" />
            <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Charter Board</h1>
          </div>
          <p className="text-sm text-[#505050]">
            {activeBookings.length} active booking{activeBookings.length !== 1 ? 's' : ''}
          </p>
        </div>
      </div>

      {activeBookings.length === 0 ? (
        <div className="bg-[#141414] border border-[#252525] rounded-xl px-8 py-16 text-center">
          <p className="text-sm text-[#505050]">No active bookings.</p>
        </div>
      ) : (
        <div className="bg-[#141414] border border-[#252525] rounded-xl overflow-hidden">
          <div className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-4 px-5 py-3 border-b border-[#1e1e1e] text-xs font-medium uppercase tracking-widest text-[#404040]">
            <span>Booking</span>
            <span className="text-right">Charter Date</span>
            <span className="text-right">Value</span>
            <span className="text-right">Status</span>
            <span />
          </div>

          {sorted.map((record) => {
            const f = record.fields
            const flagged = f.Emergency_Flag as boolean | undefined

            return (
              <Link
                key={record.id}
                href={`/operations/charters/${record.id}`}
                className="grid grid-cols-[1fr_auto_auto_auto_auto] gap-4 items-center px-5 py-3.5 border-b border-[#1a1a1a] last:border-0 hover:bg-[#161616] transition-colors group"
              >
                <div className="min-w-0">
                  <div className="text-sm font-medium text-[#f0ede8]">
                    {(f['Booking ID'] as string) ?? record.id.slice(-6).toUpperCase()}
                  </div>
                  <div className="text-xs text-[#505050] mt-0.5">
                    {lookupFirst(f['Client Name'])} · {(f['Yacht Name'] as string) ?? '—'} ·{' '}
                    {(f['Port of Call'] as string) ?? '—'}
                  </div>
                  {flagged && f.Charter_Notes ? (
                    <div className="text-xs text-red-400 mt-0.5">⚑ {f.Charter_Notes as string}</div>
                  ) : null}
                </div>
                <span className="text-sm text-[#808080] text-right">
                  {fmtDate(f['Charter Date'] as string)}
                </span>
                <span className="text-sm text-[#808080] text-right">
                  {fmt$(f['Package Price'] as number)}
                </span>
                <div className="flex justify-end">
                  <StatusBadge status={(f.Status as string) ?? 'ACTIVE'} />
                </div>
                <FlagBookingButton bookingId={record.id} alreadyFlagged={!!flagged} />
              </Link>
            )
          })}
        </div>
      )}
    </div>
  )
}
