import type { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import bcrypt from 'bcryptjs'
import { users } from '@/lib/airtable'
import type { Role } from '@/types'

if (process.env.NODE_ENV === 'production') {
  if (!process.env.NEXTAUTH_SECRET || process.env.NEXTAUTH_SECRET.length < 32) {
    throw new Error('NEXTAUTH_SECRET must be set to at least 32 characters in production. Run: openssl rand -base64 32')
  }
  // Vercel sets VERCEL_URL automatically — use it as fallback if NEXTAUTH_URL isn't set
  if (!process.env.NEXTAUTH_URL && process.env.VERCEL_URL) {
    process.env.NEXTAUTH_URL = `https://${process.env.VERCEL_URL}`
  }
}

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null

        const record = await users.findByEmail(credentials.email)
        if (!record) return null

        const hash = record.fields.Password_Hash as string | undefined
        if (!hash) return null

        const valid = await bcrypt.compare(credentials.password, hash)
        if (!valid) return null

        await users.touchLogin(record.id)

        return {
          id: record.id,
          name: (record.fields.Name as string) ?? credentials.email,
          email: credentials.email,
          role: (record.fields.Role as Role) ?? 'Concierge',
          airtableId: record.id,
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role
        token.airtableId = user.airtableId
      }
      return token
    },
    async session({ session, token }) {
      if (token && session.user) {
        session.user.id = token.sub ?? ''
        session.user.role = token.role as Role
        session.user.airtableId = token.airtableId as string
      }
      return session
    },
  },
  pages: {
    signIn: '/login',
    error: '/login',
  },
  session: {
    strategy: 'jwt',
    maxAge: 86400,
  },
}
