import type { Metadata } from 'next'
import Link from 'next/link'
import { ArrowRight, Zap } from 'lucide-react'
import { getDashboardStats, getActionItems, activity } from '@/lib/airtable'
import { StatCard } from '@/components/ui/stat-card'
import { ActionItemRow } from '@/components/ui/action-item-row'
import { ActivityFeedItem } from '@/components/ui/activity-feed'
import { fmt$ } from '@/lib/utils'

export const metadata: Metadata = { title: 'Dashboard' }

export default async function OwnerDashboardPage() {
  const [statsRes, actionRes, activityRes] = await Promise.allSettled([
    getDashboardStats(),
    getActionItems(),
    activity.getRecent(20),
  ])

  const stats = statsRes.status === 'fulfilled'
    ? statsRes.value
    : { activeLeads: 0, attentionRequired: 0, activeBookings: 0, pendingApprovals: 0, openIssues: 0, monthRevenue: 0 }
  const actionItems = actionRes.status === 'fulfilled' ? actionRes.value : []
  const recentActivity = activityRes.status === 'fulfilled' ? activityRes.value : []

  const topActions = actionItems.slice(0, 5)

  return (
    <div className="p-8 max-w-[1200px]">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Dashboard</h1>
        <p className="text-sm text-[#505050] mt-1">
          {new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
          })}
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3 mb-8">
        <StatCard
          label="Active Leads"
          value={stats.activeLeads}
          accent="default"
          className="col-span-1"
        />
        <StatCard
          label="Attention Req'd"
          value={stats.attentionRequired}
          accent={stats.attentionRequired > 0 ? 'red' : 'default'}
          className="col-span-1"
        />
        <StatCard
          label="Active Bookings"
          value={stats.activeBookings}
          accent="gold"
          className="col-span-1"
        />
        <StatCard
          label="Month Revenue"
          value={fmt$(stats.monthRevenue)}
          accent="green"
          className="col-span-1"
        />
        <StatCard
          label="Pending Approvals"
          value={stats.pendingApprovals}
          accent={stats.pendingApprovals > 0 ? 'yellow' : 'default'}
          className="col-span-1"
        />
        <StatCard
          label="Open Issues"
          value={stats.openIssues}
          accent={stats.openIssues > 0 ? 'red' : 'default'}
          className="col-span-1"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Action Center preview */}
        <div className="lg:col-span-2">
          <div className="bg-[#141414] border border-[#252525] rounded-xl overflow-hidden">
            <div className="flex items-center justify-between px-5 py-4 border-b border-[#1e1e1e]">
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4 text-[#c9a96e]" />
                <h2 className="text-sm font-medium text-[#f0ede8]">Action Center</h2>
                {actionItems.length > 0 && (
                  <span className="text-xs bg-[#c9a96e] text-[#0a0a0a] rounded-full px-1.5 py-0.5 font-medium">
                    {actionItems.length}
                  </span>
                )}
              </div>
              <Link
                href="/owner/action-center"
                className="flex items-center gap-1 text-xs text-[#505050] hover:text-[#c9a96e] transition-colors"
              >
                View all <ArrowRight className="h-3 w-3" />
              </Link>
            </div>

            {topActions.length === 0 ? (
              <div className="px-5 py-10 text-center">
                <p className="text-sm text-[#404040]">All clear — no items need attention.</p>
              </div>
            ) : (
              <div>
                {topActions.map((item) => (
                  <ActionItemRow key={item.id} item={item} />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Activity Feed */}
        <div>
          <div className="bg-[#141414] border border-[#252525] rounded-xl overflow-hidden">
            <div className="flex items-center justify-between px-5 py-4 border-b border-[#1e1e1e]">
              <h2 className="text-sm font-medium text-[#f0ede8]">Activity</h2>
              <Link
                href="/owner/activity"
                className="flex items-center gap-1 text-xs text-[#505050] hover:text-[#c9a96e] transition-colors"
              >
                View all <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
            <div className="px-5 py-2 max-h-[420px] overflow-y-auto">
              {recentActivity.length === 0 ? (
                <p className="text-sm text-[#404040] py-6 text-center">No recent activity.</p>
              ) : (
                recentActivity.map((record) => (
                  <ActivityFeedItem key={record.id} record={record} />
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
