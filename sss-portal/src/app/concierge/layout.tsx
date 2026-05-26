import { SidebarLayout } from '@/components/nav/Sidebar'

// TEMPORARY QA BYPASS — auth check removed for staging. Restore before production.
export default async function ConciergeLayout({ children }: { children: React.ReactNode }) {
  return <SidebarLayout>{children}</SidebarLayout>
}
