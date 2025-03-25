"use client";
import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"

interface App {
  id: string
  apple_id: string
  name: string
  subtitle: string
  developer: string
  category: string
  monthly_revenue_estimate: number
  monthly_downloads_estimate: number
  icon_url: string
}

export default function Dashboard() {
  const [apps, setApps] = useState<App[]>([])
  const [search, setSearch] = useState("")
  const [filteredApps, setFilteredApps] = useState<App[]>([])
  const [sortField, setSortField] = useState<"monthly_downloads_estimate" | "monthly_revenue_estimate">("monthly_downloads_estimate")
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc")

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/apps`)
      .then(res => res.json())
      .then(data => {
        setApps(data)
        setFilteredApps(data)
      })
  }, [])

  useEffect(() => {
    let filtered = apps.filter(app =>
      app.name.toLowerCase().includes(search.toLowerCase()) ||
      app.developer.toLowerCase().includes(search.toLowerCase())
    )

    filtered = filtered.sort((a, b) => {
      const aVal = a[sortField] || 0
      const bVal = b[sortField] || 0
      return sortOrder === "asc" ? aVal - bVal : bVal - aVal
    })

    setFilteredApps(filtered)
  }, [search, sortField, sortOrder, apps])

  return (
    <div className="p-6 space-y-4">
      <Card>
        <CardContent className="p-4 flex flex-col gap-4">
          <div className="flex gap-2">
            <Input
              placeholder="Search apps or developers..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <Button onClick={() => setSortField("monthly_downloads_estimate")}>Sort by Downloads</Button>
            <Button onClick={() => setSortField("monthly_revenue_estimate")}>Sort by Revenue</Button>
            <Button onClick={() => setSortOrder(o => (o === "asc" ? "desc" : "asc"))}>
              {sortOrder === "asc" ? "⬆️" : "⬇️"}
            </Button>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Icon</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Developer</TableHead>
                <TableHead>Category</TableHead>
                <TableHead className="text-right">Downloads</TableHead>
                <TableHead className="text-right">Revenue</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredApps.map(app => (
                <TableRow key={app.id}>
                  <TableCell>
                    <img src={app.icon_url} alt="icon" className="w-10 h-10 rounded-xl" />
                  </TableCell>
                  <TableCell>{app.name}</TableCell>
                  <TableCell>{app.developer}</TableCell>
                  <TableCell>{app.category}</TableCell>
                  <TableCell className="text-right">
                    {(app.monthly_downloads_estimate ?? 'No info.').toLocaleString()}
                    </TableCell>
                  <TableCell className="text-right">
                    ${ (app.monthly_revenue_estimate ?? ' -').toLocaleString() }
                  </TableCell>

                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
