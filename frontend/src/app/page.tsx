'use server'

import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";

import { auth } from "../../auth";
import { redirect } from "next/navigation";

export default async function App() {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }   
  redirect("/home");
}
