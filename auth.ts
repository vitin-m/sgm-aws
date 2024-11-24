import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"

import db from "@/lib/db"
import { compareSync } from "bcrypt-ts"

export const {
  handlers,
  auth,
  signIn,
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
          password: user.password 
        }
      }
      return null
    }
  })],
});