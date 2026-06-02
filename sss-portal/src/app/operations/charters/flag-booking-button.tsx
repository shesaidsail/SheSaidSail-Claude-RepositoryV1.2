'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import { Flag } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { Textarea } from '@/components/ui/textarea'

export function FlagBookingButton({
  bookingId,
  alreadyFlagged,
}: {
  bookingId: string
  alreadyFlagged: boolean
}) {
  const router = useRouter()
  const [open, setOpen] = useState(false)
  const [reason, setReason] = useState('')
  const [loading, setLoading] = useState(false)

  if (alreadyFlagged) {
    return <Flag className="h-4 w-4 text-red-400" />
  }

  async function handleFlag() {
    if (!reason.trim()) return
    setLoading(true)
    try {
      const res = await fetch(`/api/bookings/${bookingId}/flag`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason }),
      })
      if (!res.ok) throw new Error()
      toast.success('Booking flagged')
      setOpen(false)
      router.refresh()
    } catch {
      toast.error('Flag failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Button
        variant="ghost"
        size="icon-sm"
        onClick={(e) => { e.preventDefault(); e.stopPropagation(); setOpen(true) }}
        className="text-[#404040] hover:text-red-400"
        title="Flag booking"
      >
        <Flag className="h-3.5 w-3.5" />
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Flag this booking</DialogTitle>
          </DialogHeader>
          <div className="space-y-1.5">
            <label className="text-xs font-medium uppercase tracking-widest text-[#505050]">
              Reason
            </label>
            <Textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="Describe the issue..."
              rows={3}
              autoFocus
            />
          </div>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button variant="destructive" onClick={handleFlag} loading={loading} disabled={!reason.trim()}>
              <Flag className="h-4 w-4" />
              Flag Booking
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}
