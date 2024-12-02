import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { UserProvider } from "../../contexts/context-user"
import { Button } from "@/components/ui/button"
import { TbHome } from "react-icons/tb";
import Link from "next/link";
import { BackgroundLines } from "@/components/ui/background-lines";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <BackgroundLines className="bg-transparent">
      <SidebarProvider>
        <AppSidebar />
        <div className="w-full flex flex-col">
        <div className="flex justify-between items-center mr-2">
          <SidebarTrigger />
          <Link href={"/home"}>
            <Button variant="outline" className="h-6 w-3">
              <TbHome/>
            </Button>
          </Link>
        </div>
          <main className="w-full bg-background border-t-[1.5px] border-zinc-800">
            {children}
          </main>
        </div>
      </SidebarProvider>
    </BackgroundLines>
  )
}