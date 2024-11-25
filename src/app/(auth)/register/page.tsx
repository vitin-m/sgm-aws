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
import register from "./_actions/register"

export default function Register() {
  return (
    <div className="bg-background h-screen flex items-center justify-center">
      <Card className="mx-auto max-w-sm bg-background border-primary">
        <CardHeader>
          <CardTitle className="text-3xl text-zinc-50">Faça seu cadastro
          </CardTitle>
          <CardDescription>
            Cadastre suas informações para criar sua conta.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form action={register}>
            <div className="grid gap-4">
              <div className="grid gap-2">
                <Label className="text-zinc-50" htmlFor="email">Name</Label>
                <Input
                  className="border-zinc-700 text-zinc-300"
                  id="name"
                  name="name"
                  type="text"
                  placeholder="Digite seu nome"
                  required
                />
                <Label className="text-zinc-50" htmlFor="email">Email</Label>
                <Input
                  className="border-zinc-700 text-zinc-300"
                  id="email"
                  name="email"
                  type="email"
                  placeholder="m@example.com"
                  required
                />
                <Label className="text-zinc-50 " htmlFor="password">Password</Label>
                <Input 
                  className="border-zinc-700 text-zinc-300" 
                  placeholder="Senha" 
                  id="password" 
                  name="password"
                  type="password" 
                  required 
                />
              </div>
              <Button type="submit" className="w-full mt-5">
                Cadastrar-se
              </Button>
            </div>
          </form>
          <div className="mt-4 text-center text-sm text-zinc-50">
            Já possue login?{" "}
            <Link href="/login" className="underline">
              Login
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
