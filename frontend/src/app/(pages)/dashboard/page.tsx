import { auth } from '@/../../auth'
import { redirect } from 'next/navigation'
import { getSession } from 'next-auth/react'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'

import { VscKey } from "react-icons/vsc";
import { PiUserCircleGear } from "react-icons/pi";

export default async function Dashboard() {
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div className="h-[94vh] bg-background px-20 pb-10 pt-5 flex flex-1 gap-5">
      <div className="p-8 border rounded-md w-full">
        <h1 className="text-xl font-bold pb-4 text-primary flex items-center justify-center gap-2">
          <PiUserCircleGear size={23}/>
          Alterar informações do usuário
        </h1>
        <form className="flex flex-col" action="">
          <div className="flex flex-col justify-center items-center gap-1 p-4 rounded-md ">
            <Avatar className="rounded-full h-20 w-20">
              <AvatarImage
                src={session?.user.avatar || ''}
                alt={session?.user.avatar || 'foto usuário'}
              />
              <AvatarFallback className="rounded-lg">CN</AvatarFallback>
            </Avatar>
            <Button variant={'link'}>Editar foto</Button>
          </div>
          <div className="flex flex-col gap-1">
            <label htmlFor="email">Nome completo:</label>
            <input
              className="bg-muted border rounded-md h-8 px-3"
              type="email"
              id="email"
              name="email"
              placeholder={session.user.name}            />
            <label htmlFor="password">Email:</label>
            <input
              className="bg-muted border rounded-md h-8 px-3"
              type="email"
              id="email"
              placeholder={session.user.email}
            />
          </div>
          <Button className="mt-6">Salvar edição</Button>
        </form>
      </div>
      <div className="p-8 border rounded-md flex flex-col w-full">
        <h1 className="text-xl font-bold pb-4 text-primary flex items-center justify-center gap-2">
          <VscKey />
        Alterar senha
        </h1>
        <form className="flex flex-col" action="">
          <div className="flex flex-col gap-1">
            <label htmlFor="current-password">Senha atual:</label>
            <input
              className="bg-muted border rounded-md h-8 px-3"
              type="password"
              id="current-password"
              name="current-password"
            />
            <label htmlFor="password">Nova senha:</label>
            <input
              className="bg-muted border rounded-md h-8 px-3"
              type="password"
              id="new-password"
              name="new-password"
            />
            <label htmlFor="password">Confirmação:</label>
            <input
              className="bg-muted border rounded-md h-8 px-3"
              type="password"
              id="verify-password"
              name="verify-password"
            />
          </div>

          <Button className="mt-6">Salvar edição</Button>
        </form>
      </div>
    </div>
  )
}
