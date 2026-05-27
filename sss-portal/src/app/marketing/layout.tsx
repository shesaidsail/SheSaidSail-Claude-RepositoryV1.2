import { getServerSession } from 'next-auth/next'
import { redirect } from 'next/navigation'
import { authOptions } from '@/lib/auth'
import { SidebarLayout } from '@/components/nav/Sidebar'

export default async function MarketingLayout({ children }: { children: React.ReactNode }) {
  const session = await getServerSession(authOptions)
  if (!session || !['Owner', 'Marketing'].includes(session.user.role)) {
    redirect('/login')
  }
  return <SidebarLayout>{children}</SidebarLayout>
}
