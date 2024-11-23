import Link from "next/link"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function Login() {
  return (
    <div className="bg-zinc-950 h-screen flex items-center justify-center">
      <Card className="mx-auto max-w-sm bg-zinc-950 border-zinc-700">
        <CardHeader>
          <CardTitle className="text-3xl text-zinc-50">Login</CardTitle>
          <CardDescription>
            Entre com seu email e senha para acessar a conta.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label className="text-zinc-50" htmlFor="email">Email</Label>
              <Input
                className="border-zinc-700 text-zinc-300"
                id="email"
                type="email"
                placeholder="m@example.com"
                required
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label className="text-zinc-50 " htmlFor="password">Password</Label>
                <Link href="#" className="text-muted-foreground ml-auto inline-block text-xs underline">
                  Esqueceu sua senha?
                </Link>
              </div>
              <Input className="border-zinc-700 text-zinc-300" placeholder="Senha" id="password" type="password" required />
            </div>
            <Button type="submit" className="w-full mt-5">
              Login
            </Button>
          </div>
          <div className="mt-4 text-center text-sm text-zinc-50">
            Não possue conta?{" "}
            <Link href="/register" className="underline">
              Cadastre-se
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
