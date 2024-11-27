import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { UserProvider } from "../contexts/context-user"
 
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="w-full flex flex-col">
      <SidebarTrigger />
        <main className="w-full bg-background border-t-[1.5px] border-zinc-800">
          {children}
        </main>
      </div>
    </SidebarProvider>
  )
}