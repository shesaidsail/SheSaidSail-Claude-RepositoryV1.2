import type { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import bcrypt from 'bcryptjs'
import { users } from '@/lib/airtable'
import type { Role } from '@/types'

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

        if (!record.fields.Active) return null

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
