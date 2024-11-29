'use server'

import { redirect } from "next/navigation"
import { auth } from "../../../../auth"

export default async function Home() {
  const session = await auth()

  if (!session) {
    redirect("/login")
  }
  
  return (
    <div className="flex flex-col items-center justify-center h-[94vh]">
      <h1 className="text-4xl font-bold">Seja bem vindo! {session.user?.name}</h1>
      <p className="mt-4 text-lg text-center">
        <code>Home Page</code>
      </p>
    </div>
  )
}