'use client'

import Link from "next/link"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { IoClose } from "react-icons/io5";

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import register from "./_actions/register"
import { BackgroundLines } from "@/components/ui/background-lines"
import { Textarea } from "@/components/ui/textarea"
import { useState } from "react"

export default function Register() {
  const [profileImage, setProfileImage] = useState<string | null>(null);

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setProfileImage(null);
  };

  return (
    <BackgroundLines className="bg-transparent">
      <div className=" h-screen flex items-center justify-center">
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
                  <Label className="text-zinc-50" htmlFor="fullname">Nome completo</Label>
                  <Input
                    className="border-zinc-700 text-zinc-300"
                    id="fullname"
                    name="fullname"
                    type="text"
                    placeholder="Informe seu nome..."
                    required
                  />
                  <Label className="text-zinc-50" htmlFor="username">Username</Label>
                  <Input
                    className="border-zinc-700 text-zinc-300"
                    id="username"
                    name="username"
                    type="text"
                    placeholder="Username..."
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
                  <Label className="text-zinc-50" htmlFor="description">Descrição</Label>
                  <Textarea 
                    placeholder="Descrição do usuário."
                    id="description" 
                    name="description"
                  />
                  <Label className="text-zinc-50" htmlFor="profileImage">Foto de Perfil</Label>
                  <div className="flex items-center justify-center gap-2">
                    <Input
                      className="border-zinc-700 text-zinc-300 cursor-pointer "
                      id="profileImage"
                      name="profileImage"
                      type="file"
                      accept="image/*"
                      onChange={handleImageChange}
                    />
                    {profileImage && (
                      <Button type="button" onClick={handleRemoveImage}>
                       <IoClose />
                      </Button>
                    )}
                  </div>

                  {profileImage && (
                    <div className="flex flex-col items-center justify-between">
                      <img src={profileImage} alt="Profile" className="mt-2 w-20 h-20 rounded-full" />
                    </div>
                  )}
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
    </BackgroundLines>
  )
}
