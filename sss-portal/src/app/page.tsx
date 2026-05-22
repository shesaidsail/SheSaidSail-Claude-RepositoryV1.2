import { redirect } from 'next/navigation'

export default function Home() {
  // STAGING ONLY: DISABLE_PORTAL_AUTH=true skips login for QA
  if (process.env.DISABLE_PORTAL_AUTH === 'true') {
    redirect('/owner/dashboard')
  }
  redirect('/login')
}
