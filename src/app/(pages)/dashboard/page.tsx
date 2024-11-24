import { auth } from '@/../../auth'
import { redirect } from 'next/navigation'

export default async function Dashboard (){
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div className="dark bg-background">
      <h1>Dashboard</h1>
      <p>Welcome to the dashboard!</p>
    </div>
  )
}