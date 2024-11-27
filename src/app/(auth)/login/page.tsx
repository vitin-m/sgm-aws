import Link from 'next/link'

import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import loginAuth from './_actions/loginAuth'
import { Suspense } from 'react'
import Loading from './loading'

export default function Login() {
  return (
    <div className="bg-background h-screen flex items-center justify-center">
      <Card className="mx-auto max-w-sm bg-background border-primary">
        <CardHeader>
          <CardTitle className="text-3xl text-zinc-50">Login</CardTitle>
          <CardDescription>
            Entre com seu email e senha para acessar a conta.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form action={loginAuth}>
            <div className="grid gap-4">
              <div className="grid gap-2">
                <Label className="text-zinc-50" htmlFor="email">
                  Email
                </Label>
                <Input
                  className="border-zinc-700 text-zinc-300"
                  id="email"
                  name="email"
                  type="email"
                  placeholder="m@example.com"
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex">
                  <Label className="text-zinc-50 " htmlFor="password">
                    Password
                  </Label>
                  <Link
                    href="#"
                    className="text-muted-foreground ml-auto inline-block text-xs underline"
                  >
                    Esqueceu sua senha?
                  </Link>
                </div>
                <Input
                  className="bord  er-zinc-700 text-zinc-300"
                  placeholder="Senha"
                  id="password"
                  name='password'
                  type="password"
                  required
                />
              </div>
              <Suspense fallback={<Loading />}>
                <Button type="submit" className="w-full mt-5">
                  Login
                </Button>
              </Suspense>
            </div>
          </form>
          <div className="mt-4 text-center text-sm text-zinc-50">
            Não possue conta?{' '}
            <Link href="/register" className="underline">
              Cadastre-se
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
