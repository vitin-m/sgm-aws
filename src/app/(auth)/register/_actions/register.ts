'use server'

import db from '@/lib/db'; 
import { hashSync } from "bcrypt-ts";
import { redirect } from 'next/navigation';

export default async function (formData : FormData){
  const { name , email, password } = Object.fromEntries(formData.entries()) as { [key: string]: string }
  
  if (!name || !email || !password) {
    throw new Error("Preencha todos os campos");
  }

  const userIsUnique = await db.user.findUnique({
    where: { email },
  });

  if (userIsUnique) {
    throw new Error("Este email já está em uso");
  }

  const user = await db.user.create({
    data: {
      name,
      email,
      password: hashSync(password, 10),
    },
  })

  redirect("/dashboard")
}