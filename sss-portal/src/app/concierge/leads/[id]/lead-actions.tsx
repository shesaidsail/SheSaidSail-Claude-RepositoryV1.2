'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import { CheckCircle, Save } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from '@/components/ui/dialog'

const STATUSES = ['NEW', 'QUALIFIED', 'BOOKED', 'CLOSED']

interface LeadActionsProps {
  leadId: string
  currentStatus: string
  currentNotes: string
}

export function LeadActions({
  leadId,
  currentStatus,
  currentNotes,
}: LeadActionsProps) {
  const router = useRouter()
  const [status, setStatus] = useState(currentStatus)
  const [notes, setNotes] = useState(currentNotes)
  const [saving, setSaving] = useState(false)
  const [qualifying, setQualifying] = useState(false)
  const [qualifyOpen, setQualifyOpen] = useState(false)

  async function saveChanges() {
    setSaving(true)
    try {
      const res = await fetch(`/api/leads/${leadId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, notes }),
      })
      if (!res.ok) throw new Error()
      toast.success('Saved')
      router.refresh()
    } catch {
      toast.error('Save failed')
    } finally {
      setSaving(false)
    }
  }

  async function handleQualify() {
    setQualifying(true)
    try {
      const res = await fetch(`/api/leads/${leadId}/qualify`, { method: 'POST' })
      if (!res.ok) throw new Error()
      toast.success('Lead qualified — booking creation triggered')
      setQualifyOpen(false)
      router.refresh()
    } catch {
      toast.error('Qualify failed')
    } finally {
      setQualifying(false)
    }
  }

  const canQualify = !['BOOKED', 'CLOSED'].includes(status)

  return (
    <div className="space-y-4">
      {/* QUALIFY button */}
      {canQualify && (
        <div className="bg-[#1a1408] border border-[#3d2e12] rounded-xl p-4">
          <div className="flex items-start gap-2 mb-3">
            <CheckCircle className="h-4 w-4 text-[#c9a96e] flex-shrink-0 mt-0.5" />
            <div>
              <div className="text-sm font-medium text-[#c9a96e]">Ready to qualify?</div>
              <div className="text-xs text-[#8a6f42] mt-0.5">
                Sets status to Availability Confirmed and triggers booking creation in Make.
              </div>
            </div>
          </div>
          <Button
            variant="default"
            size="sm"
            className="w-full"
            onClick={() => setQualifyOpen(true)}
          >
            Qualify Lead
          </Button>
        </div>
      )}

      {/* Status */}
      <div className="bg-[#141414] border border-[#252525] rounded-xl p-4 space-y-4">
        <div className="space-y-1.5">
          <label className="text-xs font-medium uppercase tracking-widest text-[#505050]">
            Status
          </label>
          <Select value={status} onValueChange={setStatus}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {STATUSES.map((s) => (
                <SelectItem key={s} value={s}>
                  {s.replace(/_/g, ' ')}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-medium uppercase tracking-widest text-[#505050]">
            Notes
          </label>
          <Textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            rows={5}
            placeholder="Add notes..."
          />
        </div>

        <Button
          variant="secondary"
          size="sm"
          className="w-full"
          onClick={saveChanges}
          loading={saving}
        >
          <Save className="h-4 w-4" />
          Save Changes
        </Button>
      </div>

      {/* Qualify confirmation dialog */}
      <Dialog open={qualifyOpen} onOpenChange={setQualifyOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Qualify this lead?</DialogTitle>
            <DialogDescription>
              This will set the status to <strong>AVAILABILITY_CONFIRMED</strong> and trigger the
              booking creation flow in Make. This cannot be undone automatically.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setQualifyOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleQualify} loading={qualifying}>
              <CheckCircle className="h-4 w-4" />
              Confirm & Qualify
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
