'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import { Save } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

export function CharterNoteForm({
  bookingId,
  currentNote,
}: {
  bookingId: string
  currentNote: string
}) {
  const router = useRouter()
  const [note, setNote] = useState(currentNote)
  const [saving, setSaving] = useState(false)

  async function save() {
    setSaving(true)
    try {
      const res = await fetch(`/api/bookings/${bookingId}/notes`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes: note }),
      })
      if (!res.ok) throw new Error()
      toast.success('Notes saved')
      router.refresh()
    } catch {
      toast.error('Save failed')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-3">
      <Textarea
        value={note}
        onChange={(e) => setNote(e.target.value)}
        placeholder="Add charter notes..."
        rows={4}
      />
      <Button variant="secondary" size="sm" onClick={save} loading={saving}>
        <Save className="h-4 w-4" />
        Save Notes
      </Button>
    </div>
  )
}
