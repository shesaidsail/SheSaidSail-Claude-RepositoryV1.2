import type { Metadata } from 'next'
import { Activity } from 'lucide-react'
import { activity } from '@/lib/airtable'
import { ActivityFeedItem } from '@/components/ui/activity-feed'

export const metadata: Metadata = { title: 'Activity' }

export default async function ActivityPage() {
  const records = await activity.getRecent(100).catch(() => [])

  return (
    <div className="p-8 max-w-[700px]">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <Activity className="h-5 w-5 text-[#c9a96e]" />
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Activity Log</h1>
        </div>
        <p className="text-sm text-[#505050]">{records.length} recent events</p>
      </div>

      <div className="bg-[#141414] border border-[#252525] rounded-xl px-5">
        {records.length === 0 ? (
          <p className="text-sm text-[#404040] py-10 text-center">No activity recorded yet.</p>
        ) : (
          records.map((record) => <ActivityFeedItem key={record.id} record={record} />)
        )}
      </div>
    </div>
  )
}
