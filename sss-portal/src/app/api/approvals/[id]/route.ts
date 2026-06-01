import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'
import { approvals } from '@/lib/airtable'

export async function POST(req: NextRequest, { params }: { params: { id: string } }) {
  const session = await getServerSession(authOptions)
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  if (session.user.role !== 'Owner') return NextResponse.json({ error: 'Forbidden' }, { status: 403 })

  let body: { approved: boolean; note?: string }
  try {
    body = await req.json()
  } catch {
    return NextResponse.json({ error: 'Invalid body' }, { status: 400 })
  }

  const actor = session.user.name ?? session.user.email

  try {
    await approvals.decide(params.id, body.approved, actor, body.note)
    return NextResponse.json({ ok: true })
  } catch (err) {
    console.error('POST /api/approvals/[id]', err)
    return NextResponse.json({ error: 'Decision failed' }, { status: 500 })
  }
}
