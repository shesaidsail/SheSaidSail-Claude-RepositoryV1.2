import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'
import { bookings } from '@/lib/airtable'

export async function POST(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getServerSession(authOptions)
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  if (!['Owner', 'Operations'].includes(session.user.role)) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
  }

  let body: { reason: string }
  try {
    body = await req.json()
    if (!body.reason?.trim()) throw new Error('reason required')
  } catch {
    return NextResponse.json({ error: 'reason is required' }, { status: 400 })
  }

  if (body.reason.trim().length > 500) {
    return NextResponse.json({ error: 'reason must be 500 characters or fewer' }, { status: 400 })
  }

  const actor = session.user.name ?? session.user.email

  try {
    await bookings.flag(params.id, body.reason.trim(), actor)
    return NextResponse.json({ ok: true })
  } catch (err) {
    console.error('POST /api/bookings/[id]/flag', err)
    return NextResponse.json({ error: 'Flag failed' }, { status: 500 })
  }
}
