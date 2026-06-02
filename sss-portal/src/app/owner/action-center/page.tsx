import type { Metadata } from 'next'
import { Zap } from 'lucide-react'
import { getActionItems } from '@/lib/airtable'
import { ActionItemRow } from '@/components/ui/action-item-row'

export const metadata: Metadata = { title: 'Action Center' }

export default async function ActionCenterPage() {
  const items = await getActionItems().catch(() => [])

  const breached = items.filter((i) => i.sla === 'BREACHED')
  const warning = items.filter((i) => i.sla === 'WARNING')
  const onTrack = items.filter((i) => i.sla === 'GREEN')

  return (
    <div className="p-8 max-w-[900px]">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <Zap className="h-5 w-5 text-[#c9a96e]" />
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Action Center</h1>
        </div>
        <p className="text-sm text-[#505050]">
          {items.length} item{items.length !== 1 ? 's' : ''} require attention
        </p>
      </div>

      {items.length === 0 ? (
        <div className="bg-[#141414] border border-[#252525] rounded-xl px-8 py-16 text-center">
          <div className="h-10 w-10 rounded-full bg-emerald-950 border border-emerald-900 flex items-center justify-center mx-auto mb-4">
            <span className="text-emerald-400 text-lg">✓</span>
          </div>
          <h3 className="text-base font-medium text-[#f0ede8] mb-1">All clear</h3>
          <p className="text-sm text-[#505050]">
            No items require your attention right now.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Breached */}
          {breached.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2 px-1">
                <div className="h-2 w-2 rounded-full bg-red-400" />
                <span className="text-xs font-medium uppercase tracking-widest text-red-400">
                  SLA Breached ({breached.length})
                </span>
              </div>
              <div className="bg-[#141414] border border-red-950 rounded-xl overflow-hidden">
                {breached.map((item) => (
                  <ActionItemRow key={item.id} item={item} />
                ))}
              </div>
            </div>
          )}

          {/* Warning */}
          {warning.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2 px-1">
                <div className="h-2 w-2 rounded-full bg-amber-400" />
                <span className="text-xs font-medium uppercase tracking-widest text-amber-400">
                  Warning ({warning.length})
                </span>
              </div>
              <div className="bg-[#141414] border border-amber-950 rounded-xl overflow-hidden">
                {warning.map((item) => (
                  <ActionItemRow key={item.id} item={item} />
                ))}
              </div>
            </div>
          )}

          {/* On Track */}
          {onTrack.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2 px-1">
                <div className="h-2 w-2 rounded-full bg-[#505050]" />
                <span className="text-xs font-medium uppercase tracking-widest text-[#505050]">
                  Needs Review ({onTrack.length})
                </span>
              </div>
              <div className="bg-[#141414] border border-[#252525] rounded-xl overflow-hidden">
                {onTrack.map((item) => (
                  <ActionItemRow key={item.id} item={item} />
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
