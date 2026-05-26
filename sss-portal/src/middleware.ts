import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getToken } from 'next-auth/jwt'
import type { Role } from '@/types'

const PROTECTED: Record<string, Role[]> = {
  '/owner': ['Owner'],
  '/operations': ['Owner', 'Operations'],
  '/concierge': ['Owner', 'Concierge'],
  '/marketing': ['Owner', 'Marketing'],
}

const ROLE_HOME: Record<Role, string> = {
  Owner: '/owner/dashboard',
  Operations: '/operations/charters',
  Concierge: '/concierge/leads',
  Marketing: '/marketing',
}

// ─── TEMPORARY QA BYPASS ─────────────────────────────────────────────────────
// Auth is disabled for staging review. To re-enable: delete the 4 lines below
// and uncomment the original auth logic (see git history: commit 602d259).
export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl
  if (pathname === '/' || pathname === '/login') {
    const url = req.nextUrl.clone()
    url.pathname = '/owner/dashboard'
    return NextResponse.redirect(url)
  }
  return NextResponse.next()
}
// ─────────────────────────────────────────────────────────────────────────────

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
