import { getServerSession } from 'next-auth/next'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth'
import { SidebarLayout } from '@/components/nav/Sidebar'

// TEMPORARY QA BYPASS — auth check removed for staging. Restore before production.
export default async function OwnerLayout({ children }: { children: React.ReactNode }) {
  return <SidebarLayout>{children}</SidebarLayout>
}
