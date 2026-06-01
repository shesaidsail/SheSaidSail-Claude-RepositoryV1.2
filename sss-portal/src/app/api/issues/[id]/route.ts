import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'
import { issues } from '@/lib/airtable'

export async function PATCH(req: NextRequest, { params }: { params: { id: string } }) {
  const session = await getServerSession(authOptions)
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  if (session.user.role !== 'Owner') return NextResponse.json({ error: 'Forbidden' }, { status: 403 })

  let body: { resolve?: boolean; note?: string }
  try {
    body = await req.json()
  } catch {
    return NextResponse.json({ error: 'Invalid body' }, { status: 400 })
  }

  const actor = session.user.name ?? session.user.email

  try {
    if (body.resolve) {
      await issues.resolve(params.id, body.note ?? '', actor)
    } else if (body.note !== undefined) {
      await issues.saveNote(params.id, body.note, actor)
    }
    return NextResponse.json({ ok: true })
  } catch (err) {
    console.error('PATCH /api/issues/[id]', err)
    return NextResponse.json({ error: 'Update failed' }, { status: 500 })
  }
}
