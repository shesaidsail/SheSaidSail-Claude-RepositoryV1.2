import { Suspense } from 'react'
import type { Metadata } from 'next'
import { LoginForm } from './login-form'

export const metadata: Metadata = { title: 'Sign In' }

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center px-4">
      {/* Subtle background grain */}
      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          backgroundImage:
            'radial-gradient(ellipse 80% 60% at 50% -20%, rgba(201,169,110,0.06) 0%, transparent 70%)',
        }}
      />

      <div className="w-full max-w-sm relative z-10">
        {/* Logo mark */}
        <div className="flex flex-col items-center mb-10">
          <div className="h-12 w-12 rounded-full bg-gradient-to-br from-[#c9a96e] to-[#8a6f42] flex items-center justify-center mb-5">
            <svg viewBox="0 0 24 24" className="h-6 w-6 fill-[#0a0a0a]" aria-hidden>
              <path d="M12 2L8 9H4l8 13 8-13h-4L12 2zm0 3.5L14.5 9h-5L12 5.5z" />
            </svg>
          </div>
          <h1 className="text-xl font-medium text-[#f0ede8] tracking-tight">She Said Sail</h1>
          <p className="text-sm text-[#505050] mt-1">Operations Portal</p>
        </div>

        {/* Form card — Suspense required because LoginForm reads useSearchParams */}
        <div className="bg-[#141414] border border-[#252525] rounded-2xl p-8">
          <Suspense fallback={<div className="h-[200px]" />}>
            <LoginForm />
          </Suspense>
        </div>

        <p className="text-center text-xs text-[#303030] mt-6">
          Authorized personnel only
        </p>
      </div>
    </div>
  )
}
