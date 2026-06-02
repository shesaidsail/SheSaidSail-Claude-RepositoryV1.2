import 'next-auth'

export type Role = 'Owner' | 'Marketing' | 'Operations' | 'Concierge'
export type SLAStatus = 'GREEN' | 'WARNING' | 'BREACHED'
export type Severity = 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL'
export type LeadStatus = 'NEW' | 'QUALIFIED' | 'BOOKED' | 'CLOSED'

export interface ATRecord {
  id: string
  createdTime: string
  fields: Record<string, unknown>
}

export interface LeadFields {
  Name?: string
  Email?: string
  Phone?: string
  Status?: LeadStatus
  SLA_Status?: SLAStatus
  Attention_Required?: boolean
  Charter_Date?: string
  Destination?: string
  Group_Size?: number
  Budget_Range?: string
  Notes?: string
  Probability?: number
  Source?: string
  Assigned_To?: string
  Last_Contact?: string
  Follow_Up_Date?: string
  Created?: string
}

export interface BookingFields {
  Booking_Reference?: string
  Client_Name?: string
  Charter_Date?: string
  Charter_End?: string
  Vessel?: string
  Destination?: string
  Status?: string
  SLA_Status?: SLAStatus
  Attention_Required?: boolean
  Total_Value?: number
  Deposit_Paid?: boolean
  Balance_Due?: string
  Special_Requests?: string
  Flagged?: boolean
  Flag_Reason?: string
  Assigned_To?: string
}

export interface AuditFields {
  Event_Type?: string
  Entity?: string
  Entity_ID?: string
  Actor?: string
  Severity?: Severity
  Details?: string
  Resolved?: boolean
  Created?: string
}

export interface ActionItem {
  id: string
  source: 'lead' | 'booking' | 'approval' | 'issue' | 'audit'
  priority: number
  title: string
  subtitle: string
  sla: SLAStatus
  href: string
  badge?: string
}

declare module 'next-auth' {
  interface User {
    role: Role
    airtableId: string
  }
  interface Session {
    user: {
      id: string
      name: string
      email: string
      role: Role
      airtableId: string
    }
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    role: Role
    airtableId: string
  }
}
