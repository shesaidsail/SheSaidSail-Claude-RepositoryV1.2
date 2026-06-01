'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import { CheckCircle, Save } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

export function IssueActions({
  issueId,
  currentNote,
}: {
  issueId: string
  currentNote: string
}) {
  const router = useRouter()
  const [note, setNote] = useState(currentNote)
  const [loading, setLoading] = useState<'save' | 'resolve' | null>(null)

  async function saveNote() {
    setLoading('save')
    try {
      const res = await fetch(`/api/issues/${issueId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ note }),
      })
      if (!res.ok) throw new Error()
      toast.success('Note saved')
      router.refresh()
    } catch {
      toast.error('Save failed')
    } finally {
      setLoading(null)
    }
  }

  async function resolve() {
    setLoading('resolve')
    try {
      const res = await fetch(`/api/issues/${issueId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resolve: true, note }),
      })
      if (!res.ok) throw new Error()
      toast.success('Issue resolved')
      router.refresh()
    } catch {
      toast.error('Resolve failed')
    } finally {
      setLoading(null)
    }
  }

  return (
    <div className="border-t border-[#1e1e1e] pt-4 space-y-3">
      <div>
        <label className="text-xs font-medium uppercase tracking-widest text-[#505050] block mb-1.5">
          Internal Notes
        </label>
        <Textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Add notes..."
          rows={3}
        />
      </div>
      <div className="flex gap-3">
        <Button
          variant="secondary"
          size="sm"
          onClick={saveNote}
          loading={loading === 'save'}
          disabled={loading !== null}
        >
          <Save className="h-4 w-4" />
          Save Note
        </Button>
        <Button
          variant="default"
          size="sm"
          onClick={resolve}
          loading={loading === 'resolve'}
          disabled={loading !== null}
        >
          <CheckCircle className="h-4 w-4" />
          Mark Resolved
        </Button>
      </div>
    </div>
  )
}
