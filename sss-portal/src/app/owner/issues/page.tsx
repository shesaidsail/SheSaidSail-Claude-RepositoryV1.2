import type { Metadata } from 'next'
import { AlertTriangle } from 'lucide-react'
import { issues } from '@/lib/airtable'
import { Badge } from '@/components/ui/badge'
import { fmtDate } from '@/lib/utils'
import { IssueActions } from './issue-actions'

export const metadata: Metadata = { title: 'Issues' }

function selectName(v: unknown): string {
  if (!v) return ''
  if (typeof v === 'string') return v
  if (typeof v === 'object' && v !== null && 'name' in v) return (v as { name: string }).name
  return ''
}

const SEVERITY_COLOR: Record<string, 'red' | 'yellow' | 'default'> = {
  Critical: 'red',
  High: 'red',
  Medium: 'yellow',
  Low: 'default',
}

export default async function IssuesPage() {
  const open = await issues.getOpen().catch(() => [])

  return (
    <div className="p-8 max-w-[900px]">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <AlertTriangle className="h-5 w-5 text-[#c9a96e]" />
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Issues</h1>
        </div>
        <p className="text-sm text-[#505050]">
          {open.length} open issue{open.length !== 1 ? 's' : ''}
        </p>
      </div>

      {open.length === 0 ? (
        <div className="bg-[#141414] border border-[#252525] rounded-xl px-8 py-16 text-center">
          <div className="h-10 w-10 rounded-full bg-emerald-950 border border-emerald-900 flex items-center justify-center mx-auto mb-4">
            <span className="text-emerald-400 text-lg">✓</span>
          </div>
          <h3 className="text-base font-medium text-[#f0ede8] mb-1">All clear</h3>
          <p className="text-sm text-[#505050]">No open issues.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {open.map((record) => {
            const f = record.fields
            const severity = selectName(f.Severity)
            const type = selectName(f.Type)
            const city = selectName(f.City)

            return (
              <div
                key={record.id}
                className={`bg-[#141414] border rounded-xl p-6 ${
                  severity === 'Critical' || severity === 'High'
                    ? 'border-red-900'
                    : severity === 'Medium'
                    ? 'border-amber-900'
                    : 'border-[#252525]'
                }`}
              >
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <h3 className="text-base font-medium text-[#f0ede8]">
                        {(f.Incident_ID as string) ?? 'Incident'}
                      </h3>
                      {severity && (
                        <Badge variant={SEVERITY_COLOR[severity] ?? 'default'}>{severity}</Badge>
                      )}
                      {type && <Badge variant="default">{type}</Badge>}
                    </div>
                    <div className="text-xs text-[#505050]">
                      {city ? `${city} · ` : ''}
                      {f.Incident_Date ? fmtDate(f.Incident_Date as string) : ''}
                      {f.Booking_ID ? ` · Booking ${f.Booking_ID}` : ''}
                      {f.Reported_By ? ` · Reported by ${f.Reported_By}` : ''}
                    </div>
                  </div>
                </div>

                {f.Description ? (
                  <div className="mb-3">
                    <div className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-1">
                      Description
                    </div>
                    <p className="text-sm text-[#a09a90] leading-relaxed whitespace-pre-wrap">
                      {f.Description as string}
                    </p>
                  </div>
                ) : null}

                {f.Persons_Involved ? (
                  <div className="mb-3">
                    <div className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-1">
                      Persons Involved
                    </div>
                    <p className="text-sm text-[#a09a90]">{f.Persons_Involved as string}</p>
                  </div>
                ) : null}

                <div className="flex gap-4 mb-4">
                  {f.Legal_Flag ? (
                    <Badge variant="red">⚑ Legal Flag</Badge>
                  ) : null}
                  {f.Police_Called ? (
                    <Badge variant="red">Police Called</Badge>
                  ) : null}
                  {f.Medical_Response ? (
                    <Badge variant="yellow">Medical Response</Badge>
                  ) : null}
                </div>

                {f.Will_Notes ? (
                  <div className="mb-4 bg-[#1a1a1a] rounded-lg p-3">
                    <div className="text-xs font-medium uppercase tracking-widest text-[#505050] mb-1">
                      Your Notes
                    </div>
                    <p className="text-sm text-[#f0ede8] whitespace-pre-wrap">{f.Will_Notes as string}</p>
                  </div>
                ) : null}

                <IssueActions issueId={record.id} currentNote={(f.Will_Notes as string) ?? ''} />
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
