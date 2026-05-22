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

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl

  // STAGING ONLY — set DISABLE_PORTAL_AUTH=true in Vercel env vars to bypass login for QA.
  // Read inline per-request so Vercel runtime env changes take effect without a rebuild.
  // Remove this variable (or set to false) before going to production.
  if (process.env.DISABLE_PORTAL_AUTH === 'true') {
    if (pathname === '/login' || pathname === '/') {
      const url = req.nextUrl.clone()
      url.pathname = '/owner/dashboard'
      return NextResponse.redirect(url)
    }
    return NextResponse.next()
  }

  const token = await getToken({ req, secret: process.env.NEXTAUTH_SECRET })

  if (!token) {
    if (pathname === '/login') return NextResponse.next()
    const url = req.nextUrl.clone()
    url.pathname = '/login'
    url.searchParams.set('callbackUrl', pathname)
    return NextResponse.redirect(url)
  }

  const role = token.role as Role

  for (const [prefix, allowed] of Object.entries(PROTECTED)) {
    if (pathname.startsWith(prefix)) {
      if (!allowed.includes(role)) {
        const url = req.nextUrl.clone()
        url.pathname = ROLE_HOME[role]
        return NextResponse.redirect(url)
      }
    }
  }

  if (pathname === '/login') {
    const url = req.nextUrl.clone()
    url.pathname = ROLE_HOME[role]
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
