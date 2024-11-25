import { auth } from '@/../../auth'
import { redirect } from 'next/navigation'

export default async function Dashboard (){
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div className='h-[95vh] bg-background px-20 pt-5'>
      <h1 className='text-xl font-bold pb-4'>Informações sobre usuário</h1>
      <p className='text-zinc-100'>Nome: {session.user?.name}</p>
      <p>Email: {session.user?.email}</p>
    </div>
  )
}