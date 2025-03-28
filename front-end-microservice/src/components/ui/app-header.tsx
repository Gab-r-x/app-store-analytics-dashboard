"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { AppWindow, Verified } from "lucide-react"

const pages = [
  { name: "HOME", href: "/", icon: <AppWindow size={16} /> },
  { name: "COMPARE APPS", href: "/compare", icon: <Verified size={16} /> },
  { name: "CATEGORY ANALYSIS", href: "/analysis", icon: <Verified size={16} /> },

  // Adicione mais páginas aqui se quiser
]

export function AppHeader() {
  const pathname = usePathname()

  return (
    <header className="w-full border-b bg-background shadow-sm">
      <div className="container mx-auto px-16 py-5 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        {/* Esquerda: Título */}
        <div className="text-left">
          <h1 className="text-2xl font-bold">App Metrics Dashboard</h1>
          <p className="text-sm text-muted-foreground">Find your favorite app information</p>
        </div>

        {/* Direita: Menu */}
        <nav className="flex gap-3 flex-wrap justify-start sm:justify-end">
          {pages.map((page) => {
            const isActive = pathname === page.href
            return (
              <Link key={page.href} href={page.href}>
                <Button
                  variant={isActive ? "ghost" : "ghost"}
                  className="flex items-center gap-2 text-sm"
                >
                  {page.name}
                </Button>
              </Link>
            )
          })}
        </nav>
      </div>
    </header>
  )
}
