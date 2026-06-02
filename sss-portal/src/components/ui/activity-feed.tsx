import { cn, timeAgo } from '@/lib/utils'
import type { AuditFields, Severity } from '@/types'
import type { ATRecord } from '@/types'

const SEVERITY_DOT: Record<Severity, string> = {
  INFO: 'bg-[#505050]',
  WARNING: 'bg-amber-400',
  ERROR: 'bg-red-400',
  CRITICAL: 'bg-red-500 animate-pulse',
}

function f(record: ATRecord, key: string) {
  return record.fields[key] as string | undefined
}

export function ActivityFeedItem({ record }: { record: ATRecord }) {
  const severityRaw = f(record, 'Severity Level') ?? 'INFO'
  const severity = (['INFO', 'WARNING', 'ERROR', 'CRITICAL'].includes(severityRaw)
    ? severityRaw
    : 'INFO') as Severity
  const eventType = f(record, 'Action Type') ?? 'Event'
  const details = f(record, 'Log Entry') ?? f(record, 'Payload Summary')
  const actor = f(record, 'Actor')
  const created = f(record, 'Timestamp') ?? record.createdTime

  return (
    <div className="flex gap-3 py-3 border-b border-[#1a1a1a] last:border-0">
      <div className="flex-shrink-0 mt-1.5">
        <div className={cn('h-2 w-2 rounded-full', SEVERITY_DOT[severity])} />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <span className="text-sm text-[#f0ede8] font-medium">
            {eventType.replace(/_/g, ' ')}
          </span>
          <span className="text-xs text-[#404040] flex-shrink-0">{timeAgo(created)}</span>
        </div>
        {details && <p className="text-xs text-[#606060] mt-0.5 truncate">{details}</p>}
        {actor && <p className="text-xs text-[#404040] mt-0.5">{actor}</p>}
      </div>
    </div>
  )
}

export function ActivityFeedSkeleton() {
  return (
    <div className="space-y-0">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="flex gap-3 py-3 border-b border-[#1a1a1a]">
          <div className="h-2 w-2 rounded-full bg-[#1c1c1c] animate-pulse mt-1.5 flex-shrink-0" />
          <div className="flex-1 space-y-1.5">
            <div className="h-3 w-32 bg-[#1c1c1c] rounded animate-pulse" />
            <div className="h-3 w-48 bg-[#1c1c1c] rounded animate-pulse" />
          </div>
        </div>
      ))}
    </div>
  )
}
