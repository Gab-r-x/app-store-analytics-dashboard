"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Home, Package, BarChart2, LineChart } from "lucide-react"

const pages = [
  { name: "HOME", href: "/", icon: <Home size={16} /> },
  { name: "COMPARE", href: "/compare", icon: <Package size={16} /> },
  { name: "ANALYSIS", href: "/analysis", icon: <BarChart2 size={16} /> },
]

export function AppHeader() {
  const pathname = usePathname()

  return (
    <div className="w-full pt-8 px-4">
      <div className="mx-auto max-w-[1400px]">
        <header className="bg-card border rounded-lg shadow-sm p-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            {/* Esquerda: Título  */}
            <div className="flex items-center gap-3">
              <div className="bg-primary rounded-full p-2 flex items-center justify-center">
                <LineChart className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold">App Metrics Dashboard</h1>
                <p className="text-xs text-muted-foreground">Find your favorite app information</p>
              </div>
            </div>

            {/* Direita: Menu */}
            <nav className="flex gap-1 flex-wrap justify-start sm:justify-end">
              {pages.map((page) => {
                const isActive = pathname === page.href
                return (
                  <Link key={page.href} href={page.href}>
                    <Button
                      variant="ghost"
                      className={`flex items-center gap-2 text-sm transition-colors ${
                        isActive 
                          ? 'bg-primary text-white pointer-events-none'
                          : 'hover:bg-primary/10 hover:text-primary'
                      }`}
                      size="sm"
                    >
                      {page.icon}
                      {page.name}
                    </Button>
                  </Link>
                )
              })}
            </nav>
          </div>
        </header>
      </div>
    </div>
  )
}