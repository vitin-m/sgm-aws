import NextAuth, { Session } from "next-auth"
import Credentials from "next-auth/providers/credentials"

import db from "@/lib/db"
import { compareSync } from "bcrypt-ts"

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      name: string;
      email: string;
      avatar: string;
    }
  }
}

export const {
  handlers,
  auth,
  signIn,
  signOut,
} = NextAuth({
  pages: {
    signIn: "/login",
    newUser: "/register",
  },
  providers: [Credentials({
    credentials: {
      email: {},
      password: {}
    },
    async authorize(credentials){
      if (!credentials) {
        return null;
      }
      const email = credentials.email as string
      const password = credentials.password as string
      
      if (!email || !password) {
        return null
      }
      
      const user = await db.user.findUnique({
        where: { email },
      })

      if (!user) {
        return null
      }

      if (compareSync(password, user.password)) {
        return { 
          id: user.id,
          name: user.name,
          email: user.email,
          password: user.password,
          avatar: user.avatar,
        }
      }
      return null
    }
  })],
  callbacks: {
    async session({ session, token, user }) {
      // Busque os dados adicionais do usuário no banco de dados
      const userData = await db.user.findUnique({
        where: { email: session.user.email },
      });

      // Adicione os dados adicionais à sessão
      if (userData) {
        session.user.id = userData.id;
        session.user.avatar = userData.avatar ?? '';
      }

      return session;
    },
  },
});