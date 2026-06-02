import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { leads } from '@/lib/airtable'
import { StatusBadge } from '@/components/ui/badge'
import { fmtDate } from '@/lib/utils'
import { LeadActions } from './lead-actions'

export const metadata: Metadata = { title: 'Lead Detail' }

function selectName(v: unknown): string {
  if (!v) return '—'
  if (typeof v === 'string') return v
  if (typeof v === 'object' && v !== null && 'name' in v) return (v as { name: string }).name
  return '—'
}

export default async function LeadDetailPage({ params }: { params: { id: string } }) {
  let record
  try {
    record = await leads.getById(params.id)
  } catch {
    notFound()
  }

  const f = record.fields
  const fullName = [f['First Name'], f['Last Name']].filter(Boolean).join(' ') || 'Unknown Lead'
  const status = (f.Status as string) ?? 'NEW'

  return (
    <div className="p-8 max-w-[900px]">
      <Link
        href="/concierge/leads"
        className="inline-flex items-center gap-1.5 text-sm text-[#505050] hover:text-[#f0ede8] transition-colors mb-6"
      >
        <ArrowLeft className="h-4 w-4" />
        Lead Board
      </Link>

      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">{fullName}</h1>
          <p className="text-sm text-[#505050] mt-1">{(f.Email as string) ?? ''}</p>
        </div>
        <div className="flex items-center gap-2">
          <StatusBadge status={status} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-5">
          {/* Charter details */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Request Details
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <Detail label="Experience" value={(f.Experience as string) ?? '—'} />
              <Detail label="Preferred Date" value={fmtDate(f['Preferred Date'] as string)} />
              <Detail
                label="Guest Count"
                value={(f['Guest Count'] as number)?.toString() ?? '—'}
              />
              <Detail label="Duration" value={(f.Duration as string) ?? '—'} />
              <Detail label="Lead Source" value={selectName(f['Lead Source'])} />
              <Detail label="Occasion" value={(f.Occasion as string) ?? '—'} />
            </div>
          </div>

          {/* Pricing */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Pricing
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <Detail label="Base Price" value={f['Base Price'] ? `$${f['Base Price']}` : '—'} />
              <Detail label="Add-Ons Total" value={f['Add-Ons Total'] ? `$${f['Add-Ons Total']}` : '—'} />
              <Detail label="Quoted Price" value={f['Quoted Price'] ? `$${f['Quoted Price']}` : '—'} />
              <Detail label="Payment Received" value={f['Payment Received'] ? 'Yes' : 'No'} />
            </div>
          </div>

          {/* Contact */}
          <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
            <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-4">
              Contact
            </h2>
            <div className="grid grid-cols-2 gap-4">
              <Detail label="Email" value={(f.Email as string) ?? '—'} />
              <Detail label="Phone" value={(f.Phone as string) ?? '—'} />
              <Detail label="Referred By" value={(f['Referred By'] as string) ?? '—'} />
              <Detail label="Submitted" value={fmtDate(record.createdTime)} />
            </div>
          </div>

          {/* Special requests */}
          {f['Special Requests'] ? (
            <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
              <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-3">
                Special Requests
              </h2>
              <p className="text-sm text-[#a09a90] whitespace-pre-wrap leading-relaxed">
                {f['Special Requests'] as string}
              </p>
            </div>
          ) : null}

          {/* Notes */}
          {f.Notes ? (
            <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
              <h2 className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-3">
                Notes
              </h2>
              <p className="text-sm text-[#a09a90] whitespace-pre-wrap leading-relaxed">
                {f.Notes as string}
              </p>
            </div>
          ) : null}
        </div>

        <div>
          <LeadActions
            leadId={record.id}
            currentStatus={status}
            currentNotes={(f.Notes as string) ?? ''}
          />
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
