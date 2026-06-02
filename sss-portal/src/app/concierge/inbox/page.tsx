import type { Metadata } from 'next'
import { Mail, Key, Shield, Link2, GitBranch } from 'lucide-react'

export const metadata: Metadata = { title: 'Inbox' }

function Step({
  n,
  title,
  children,
}: {
  n: number
  title: string
  children: React.ReactNode
}) {
  return (
    <div className="flex gap-4">
      <div className="flex-shrink-0 h-6 w-6 rounded-full bg-[#1c1c1c] border border-[#303030] flex items-center justify-center mt-0.5">
        <span className="text-xs font-medium text-[#c9a96e]">{n}</span>
      </div>
      <div>
        <div className="text-sm font-medium text-[#f0ede8] mb-1">{title}</div>
        <div className="text-sm text-[#606060] space-y-1">{children}</div>
      </div>
    </div>
  )
}

function EnvRow({ name, description }: { name: string; description: string }) {
  return (
    <div className="flex items-start gap-3 py-2 border-b border-[#1a1a1a] last:border-0">
      <code className="text-xs text-[#c9a96e] bg-[#0f0f0f] px-2 py-0.5 rounded font-mono flex-shrink-0">
        {name}
      </code>
      <span className="text-xs text-[#606060]">{description}</span>
    </div>
  )
}

export default function InboxPage() {
  return (
    <div className="p-8 max-w-[700px]">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <Mail className="h-5 w-5 text-[#c9a96e]" />
          <h1 className="text-2xl font-light text-[#f0ede8] tracking-tight">Concierge Inbox</h1>
        </div>
        <p className="text-sm text-[#505050]">Email integration for concierge@shesaidsail.com</p>
      </div>

      {/* Not connected banner */}
      <div className="bg-[#1a1408] border border-[#3d2e12] rounded-xl p-5 mb-8">
        <div className="flex items-center gap-2 mb-2">
          <Mail className="h-4 w-4 text-[#c9a96e]" />
          <span className="text-sm font-medium text-[#c9a96e]">Gmail not connected</span>
        </div>
        <p className="text-sm text-[#8a6f42]">
          This page requires a Gmail API integration to display emails. See the setup plan below.
          No credentials are hardcoded — OAuth must be configured in Vercel environment variables.
        </p>
      </div>

      {/* Recommended approach */}
      <div className="bg-[#141414] border border-[#252525] rounded-xl p-5 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <GitBranch className="h-4 w-4 text-[#c9a96e]" />
          <h2 className="text-sm font-medium text-[#f0ede8]">Recommended Approach: Make.com First</h2>
        </div>
        <p className="text-sm text-[#606060] mb-4">
          Before building a direct Gmail API integration, consider having Make.com handle email ingestion.
          This is safer, requires no OAuth in the portal, and avoids storing Gmail tokens in Vercel.
        </p>
        <div className="space-y-2 text-sm text-[#606060]">
          <div className="flex gap-2"><span className="text-emerald-400">✓</span><span>Make.com watches concierge@shesaidsail.com via Gmail module</span></div>
          <div className="flex gap-2"><span className="text-emerald-400">✓</span><span>New email arrives → Make matches sender email to Airtable lead</span></div>
          <div className="flex gap-2"><span className="text-emerald-400">✓</span><span>Make creates an entry in a new Emails table in Airtable</span></div>
          <div className="flex gap-2"><span className="text-emerald-400">✓</span><span>Portal reads from that Airtable table — no direct Gmail access needed</span></div>
          <div className="flex gap-2"><span className="text-emerald-400">✓</span><span>No Google OAuth scopes required in portal environment</span></div>
        </div>
      </div>

      {/* Direct Gmail API plan */}
      <div className="bg-[#141414] border border-[#252525] rounded-xl p-5 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Key className="h-4 w-4 text-[#c9a96e]" />
          <h2 className="text-sm font-medium text-[#f0ede8]">Direct Gmail API Integration Plan</h2>
        </div>
        <div className="space-y-5">
          <Step n={1} title="Create Google Cloud Project">
            <p>Go to console.cloud.google.com → New Project → Enable Gmail API</p>
          </Step>
          <Step n={2} title="Configure OAuth Consent Screen">
            <p>Set app name, support email, and scopes. For internal Google Workspace use, set User Type to &quot;Internal&quot; to avoid verification delays.</p>
          </Step>
          <Step n={3} title="Create OAuth 2.0 Credentials">
            <p>Credentials → OAuth client ID → Web application. Add authorized redirect URIs:</p>
            <code className="block mt-1 text-xs bg-[#0f0f0f] px-3 py-2 rounded text-[#c9a96e] font-mono">
              https://your-domain.vercel.app/api/auth/gmail/callback
            </code>
          </Step>
          <Step n={4} title="Required OAuth Scopes">
            <div className="space-y-1">
              {[
                ['gmail.readonly', 'Read emails (minimum required)'],
                ['gmail.labels', 'Read label metadata'],
                ['gmail.metadata', 'Fetch headers without body (privacy-preserving option)'],
              ].map(([scope, desc]) => (
                <div key={scope} className="flex gap-2">
                  <code className="text-xs text-[#c9a96e] font-mono">{scope}</code>
                  <span className="text-xs text-[#505050]">— {desc}</span>
                </div>
              ))}
            </div>
          </Step>
          <Step n={5} title="Store Tokens in Vercel (not Airtable)">
            <p>After OAuth flow, store the refresh token as a Vercel environment variable. Never commit tokens to git.</p>
          </Step>
          <Step n={6} title="Link Emails to Leads">
            <p>Match <code className="text-[#c9a96e] font-mono">from</code> email address against the Email field in the Requests table. Display matched lead name and link.</p>
          </Step>
        </div>
      </div>

      {/* Required env vars */}
      <div className="bg-[#141414] border border-[#252525] rounded-xl p-5 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Shield className="h-4 w-4 text-[#c9a96e]" />
          <h2 className="text-sm font-medium text-[#f0ede8]">Required Environment Variables</h2>
        </div>
        <div>
          <EnvRow name="GOOGLE_CLIENT_ID" description="OAuth 2.0 client ID from Google Cloud Console" />
          <EnvRow name="GOOGLE_CLIENT_SECRET" description="OAuth 2.0 client secret" />
          <EnvRow name="GMAIL_REFRESH_TOKEN" description="Long-lived refresh token for concierge@shesaidsail.com (obtained after first OAuth flow)" />
          <EnvRow name="GMAIL_INBOX_ADDRESS" description="concierge@shesaidsail.com — the inbox to read" />
        </div>
      </div>

      {/* Security notes */}
      <div className="bg-[#141414] border border-[#252525] rounded-xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <Link2 className="h-4 w-4 text-[#c9a96e]" />
          <h2 className="text-sm font-medium text-[#f0ede8]">Security Considerations</h2>
        </div>
        <div className="space-y-2 text-sm text-[#606060]">
          <div className="flex gap-2"><span className="text-amber-400">⚠</span><span>Use <code className="text-[#c9a96e] font-mono">gmail.readonly</code> scope only — never request send/modify unless needed</span></div>
          <div className="flex gap-2"><span className="text-amber-400">⚠</span><span>Only the concierge inbox should be connected — not personal accounts</span></div>
          <div className="flex gap-2"><span className="text-amber-400">⚠</span><span>Never display raw email body without stripping HTML/scripts</span></div>
          <div className="flex gap-2"><span className="text-amber-400">⚠</span><span>Refresh tokens expire if unused 6 months — add monitoring alert</span></div>
          <div className="flex gap-2"><span className="text-emerald-400">✓</span><span>The Make.com approach avoids all of the above risks</span></div>
        </div>
      </div>
    </div>
  )
}
