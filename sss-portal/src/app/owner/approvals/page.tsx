import type { Metadata } from 'next'
import { CheckSquare } from 'lucide-react'
import { approvals } from '@/lib/airtable'
import { Badge } from '@/components/ui/badge'
import { fmtDate } from '@/lib/utils'
import { ApprovalActions } from './approval-actions'

export const metadata: Metadata = { title: 'Approvals' }

function selectName(v: unknown): string {
  if (!v) return ''
  if (typeof v === 'string') return v
  if (typeof v === 'object' && v !== null && 'name' in v) return (v as { name: string }).name
  return ''
}

const URGENCY_COLOR: Record<string, 'red' | 'yellow' | 'default'> = {
  IMMEDIATE: 'red',
  TODAY: 'yellow',
  THIS_WEEK: 'default',
}

export default async function ApprovalsPage() {
  const pending = await approvals.getPending().catch(() => [])

  return (
    <div className="p-8 max-w-[900px]">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <CheckSquare className="h-5 w-5 text-[#c9a96e]" />
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Approvals</h1>
        </div>
        <p className="text-sm text-[#505050]">
          {pending.length} pending decision{pending.length !== 1 ? 's' : ''}
        </p>
      </div>

      {pending.length === 0 ? (
        <div className="bg-[#141414] border border-[#252525] rounded-xl px-8 py-16 text-center">
          <div className="h-10 w-10 rounded-full bg-emerald-950 border border-emerald-900 flex items-center justify-center mx-auto mb-4">
            <span className="text-emerald-400 text-lg">✓</span>
          </div>
          <h3 className="text-base font-medium text-[#f0ede8] mb-1">All clear</h3>
          <p className="text-sm text-[#505050]">No pending approvals.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {pending.map((record) => {
            const f = record.fields
            const urgency = selectName(f.Urgency)
            const reqType = selectName(f['Request Type'])
            const hoursP = f['Hours Pending'] as number | undefined
            const slaBreached = f['SLA Breached'] as boolean | undefined

            return (
              <div
                key={record.id}
                className={`bg-[#141414] border rounded-xl p-6 ${
                  slaBreached ? 'border-red-900' : urgency === 'TODAY' ? 'border-amber-900' : 'border-[#252525]'
                }`}
              >
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <h3 className="text-base font-medium text-[#f0ede8]">
                        {(f['Request Title'] as string) ?? 'Untitled Request'}
                      </h3>
                      {urgency && (
                        <Badge variant={URGENCY_COLOR[urgency] ?? 'default'}>
                          {urgency}
                        </Badge>
                      )}
                      {reqType && (
                        <Badge variant="default">{reqType}</Badge>
                      )}
                    </div>
                    <div className="text-xs text-[#505050]">
                      Submitted by {(f['Created By'] as string) ?? '—'}
                      {f['Submitted At'] ? ` · ${fmtDate(f['Submitted At'] as string)}` : ''}
                      {hoursP !== undefined ? ` · ${Math.round(hoursP)}h pending` : ''}
                    </div>
                  </div>
                </div>

                {f.Context ? (
                  <div className="mb-3">
                    <div className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-1">Context</div>
                    <p className="text-sm text-[#a09a90] leading-relaxed">{f.Context as string}</p>
                  </div>
                ) : null}

                {f['Proposed Action'] ? (
                  <div className="mb-4">
                    <div className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-1">Proposed Action</div>
                    <p className="text-sm text-[#a09a90] leading-relaxed">{f['Proposed Action'] as string}</p>
                  </div>
                ) : null}

                {f['Financial Impact'] ? (
                  <div className="mb-4">
                    <div className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-1">Financial Impact</div>
                    <p className="text-sm text-[#c9a96e]">${(f['Financial Impact'] as number).toLocaleString()}</p>
                  </div>
                ) : null}

                <ApprovalActions approvalId={record.id} />
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
