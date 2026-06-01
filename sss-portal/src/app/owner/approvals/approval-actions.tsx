'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import { CheckCircle, XCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

export function ApprovalActions({ approvalId }: { approvalId: string }) {
  const router = useRouter()
  const [note, setNote] = useState('')
  const [loading, setLoading] = useState<'approve' | 'deny' | null>(null)

  async function decide(approved: boolean) {
    setLoading(approved ? 'approve' : 'deny')
    try {
      const res = await fetch(`/api/approvals/${approvalId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ approved, note: note.trim() || undefined }),
      })
      if (!res.ok) throw new Error()
      toast.success(approved ? 'Approved' : 'Denied')
      router.refresh()
    } catch {
      toast.error('Decision failed')
    } finally {
      setLoading(null)
    }
  }

  return (
    <div className="border-t border-[#1e1e1e] pt-4 space-y-3">
      <div>
        <label className="text-xs font-medium uppercase tracking-widest text-[#505050] block mb-1.5">
          Decision Note (optional)
        </label>
        <Textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Add context for your decision..."
          rows={2}
        />
      </div>
      <div className="flex gap-3">
        <Button
          variant="default"
          size="sm"
          onClick={() => decide(true)}
          loading={loading === 'approve'}
          disabled={loading !== null}
          className="flex-1"
        >
          <CheckCircle className="h-4 w-4" />
          Approve
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={() => decide(false)}
          loading={loading === 'deny'}
          disabled={loading !== null}
          className="flex-1"
        >
          <XCircle className="h-4 w-4" />
          Deny
        </Button>
      </div>
    </div>
  )
}
