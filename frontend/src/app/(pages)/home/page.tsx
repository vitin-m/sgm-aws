'use client'

import { redirect } from "next/navigation"
// import { auth } from "../../../../auth"
import { useUser } from "@/contexts/context-user"

export default async function Home() {
  const session  = useUser()

  console.log(session)

  if (!session) {
    redirect("/login")
  }
  
  return (
    <div className="flex flex-col items-center justify-center h-[94vh]">
      {/* <h1 className="text-4xl font-bold">Seja bem vindo! {session.user?.name}</h1> */}
      <p className="mt-4 text-lg text-center">
        <code>Home Page {session.user?.user_name}</code>
      </p>
    </div>
  )
}