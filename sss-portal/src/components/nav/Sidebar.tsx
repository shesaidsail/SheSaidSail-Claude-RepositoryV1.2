'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { signOut, useSession } from 'next-auth/react'
import {
  LayoutDashboard,
  Zap,
  Users,
  Anchor,
  TrendingUp,
  LogOut,
  Activity,
  CheckSquare,
  AlertTriangle,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import type { Role } from '@/types'

interface NavItem {
  label: string
  href: string
  icon: React.ReactNode
  roles: Role[]
}

const NAV: NavItem[] = [
  {
    label: 'Dashboard',
    href: '/owner/dashboard',
    icon: <LayoutDashboard className="h-4 w-4" />,
    roles: ['Owner'],
  },
  {
    label: 'Action Center',
    href: '/owner/action-center',
    icon: <Zap className="h-4 w-4" />,
    roles: ['Owner'],
  },
  {
    label: 'Lead Board',
    href: '/concierge/leads',
    icon: <Users className="h-4 w-4" />,
    roles: ['Owner', 'Concierge'],
  },
  {
    label: 'Charters',
    href: '/operations/charters',
    icon: <Anchor className="h-4 w-4" />,
    roles: ['Owner', 'Operations'],
  },
  {
    label: 'Approvals',
    href: '/owner/approvals',
    icon: <CheckSquare className="h-4 w-4" />,
    roles: ['Owner'],
  },
  {
    label: 'Issues',
    href: '/owner/issues',
    icon: <AlertTriangle className="h-4 w-4" />,
    roles: ['Owner'],
  },
  {
    label: 'Activity',
    href: '/owner/activity',
    icon: <Activity className="h-4 w-4" />,
    roles: ['Owner'],
  },
  {
    label: 'Marketing',
    href: '/marketing',
    icon: <TrendingUp className="h-4 w-4" />,
    roles: ['Owner', 'Marketing'],
  },
]

export function Sidebar() {
  const pathname = usePathname()
  const { data: session } = useSession()
  const role = session?.user?.role as Role | undefined
  const name = session?.user?.name ?? ''

  const visibleItems = NAV.filter((item) => !role || item.roles.includes(role))

  return (
    <aside className="w-56 min-h-screen bg-[#0d0d0d] border-r border-[#1a1a1a] flex flex-col fixed top-0 left-0 z-40">
      {/* Logo */}
      <div className="px-5 py-6 border-b border-[#1a1a1a]">
        <div className="flex items-center gap-2.5">
          <div className="h-7 w-7 rounded-full bg-gradient-to-br from-[#c9a96e] to-[#8a6f42] flex items-center justify-center flex-shrink-0">
            <Anchor className="h-3.5 w-3.5 text-[#0a0a0a]" />
          </div>
          <div>
            <div className="text-sm font-semibold text-[#f0ede8] leading-tight">She Said Sail</div>
            <div className="text-xs text-[#505050]">Operations Portal</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 py-4 space-y-0.5">
        {visibleItems.map((item) => {
          const active = pathname === item.href || pathname.startsWith(item.href + '/')
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors',
                active
                  ? 'bg-[#1c1c1c] text-[#f0ede8]'
                  : 'text-[#606060] hover:text-[#f0ede8] hover:bg-[#161616]'
              )}
            >
              <span className={cn(active ? 'text-[#c9a96e]' : '')}>{item.icon}</span>
              {item.label}
            </Link>
          )
        })}
      </nav>

      {/* User footer */}
      <div className="px-2 pb-4 border-t border-[#1a1a1a] pt-4">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="h-7 w-7 rounded-full bg-[#1c1c1c] border border-[#252525] flex items-center justify-center flex-shrink-0">
            <span className="text-xs font-medium text-[#c9a96e]">
              {name.charAt(0).toUpperCase()}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-xs font-medium text-[#f0ede8] truncate">{name}</div>
            <div className="text-xs text-[#505050]">{role}</div>
          </div>
          <button
            onClick={() => signOut({ callbackUrl: '/login' })}
            className="text-[#404040] hover:text-[#808080] transition-colors"
            title="Sign out"
          >
            <LogOut className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>
    </aside>
  )
}

export function SidebarLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-[#0a0a0a]">
      <Sidebar />
      <main className="ml-56 flex-1 min-h-screen">{children}</main>
    </div>
  )
}
