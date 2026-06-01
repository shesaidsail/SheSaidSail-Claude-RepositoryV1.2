import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'
import { bookings } from '@/lib/airtable'

export async function PATCH(req: NextRequest, { params }: { params: { id: string } }) {
  const session = await getServerSession(authOptions)
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  if (!['Owner', 'Operations'].includes(session.user.role)) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
  }

  let body: { notes: string }
  try {
    body = await req.json()
  } catch {
    return NextResponse.json({ error: 'Invalid body' }, { status: 400 })
  }

  const actor = session.user.name ?? session.user.email

  try {
    await bookings.updateField(params.id, { 'Charter Notes': body.notes }, actor)
    return NextResponse.json({ ok: true })
  } catch (err) {
    console.error('PATCH /api/bookings/[id]/notes', err)
    return NextResponse.json({ error: 'Update failed' }, { status: 500 })
  }
}
