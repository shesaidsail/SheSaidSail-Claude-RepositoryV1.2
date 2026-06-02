import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth/next'
import { authOptions } from '@/lib/auth'
import { leads } from '@/lib/airtable'
import type { LeadStatus } from '@/types'

const VALID_STATUSES: LeadStatus[] = ['NEW', 'QUALIFIED', 'BOOKED', 'CLOSED']

export async function PATCH(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getServerSession(authOptions)
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  if (!['Owner', 'Concierge'].includes(session.user.role)) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
  }

  let body: { status?: string; notes?: string; probability?: number }
  try {
    body = await req.json()
  } catch {
    return NextResponse.json({ error: 'Invalid body' }, { status: 400 })
  }

  if (body.status !== undefined && !VALID_STATUSES.includes(body.status as LeadStatus)) {
    return NextResponse.json({ error: 'Invalid status value' }, { status: 400 })
  }
  if (body.probability !== undefined && (body.probability < 0 || body.probability > 100)) {
    return NextResponse.json({ error: 'Probability must be between 0 and 100' }, { status: 400 })
  }
  if (body.notes !== undefined && body.notes.length > 5000) {
    return NextResponse.json({ error: 'Notes must be 5000 characters or fewer' }, { status: 400 })
  }

  const actor = session.user.name ?? session.user.email

  try {
    const updates: Promise<unknown>[] = []

    if (body.status) {
      updates.push(leads.updateStatus(params.id, body.status, actor))
    }
    if (body.notes !== undefined) {
      updates.push(leads.saveNote(params.id, body.notes, actor))
    }
    if (body.probability !== undefined) {
      updates.push(leads.setProbability(params.id, body.probability, actor))
    }

    await Promise.all(updates)
    return NextResponse.json({ ok: true })
  } catch (err) {
    console.error('PATCH /api/leads/[id]', err)
    return NextResponse.json({ error: 'Update failed' }, { status: 500 })
  }
}
