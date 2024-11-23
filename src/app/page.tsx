import Image from "next/image";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex items-center flex-col gap-4 justify-center h-screen bg-zinc-950">
      <h1 className="text-5xl font-bold text-zinc-300">Using nextAuth for autentication.</h1>

      <Link href={'/login'}>
        <Button className="font-bold p-5">Redirect Login</Button>
      </Link>
    </div>
  );
}
