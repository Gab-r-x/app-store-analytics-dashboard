"use client"

import { useEffect, useState } from "react"
import {
  Card,
  CardContent,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"

interface App {
  id: string
  apple_id: string
  name: string
  subtitle: string
  developer: string
  category: string
  list_type: string
  price: string
  rank: number
  monthly_revenue_estimate: number
  monthly_downloads_estimate: number
  icon_url: string
}

const PAGE_SIZE = 20

export default function Dashboard() {
  const [apps, setApps] = useState<App[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState("")
  const [listType, setListType] = useState("")
  const [search, setSearch] = useState("")
  const [totalPages, setTotalPages] = useState(1)
  const [currentPage, setCurrentPage] = useState(1)

  const fetchApps = async () => {
    const baseUrl = search
      ? `${process.env.NEXT_PUBLIC_API_URL}/apps/search?q=${encodeURIComponent(search)}&limit=${PAGE_SIZE}&skip=${(currentPage - 1) * PAGE_SIZE}`
      : `${process.env.NEXT_PUBLIC_API_URL}/apps?limit=${PAGE_SIZE}&skip=${(currentPage - 1) * PAGE_SIZE}`

    const url = new URL(baseUrl)
    if (selectedCategory) url.searchParams.append("category", selectedCategory)
    if (listType) url.searchParams.append("list_type", listType)

    const res = await fetch(url.toString())
    const data = await res.json()
    setApps(data)
  }

  useEffect(() => {
    fetchApps()
  }, [selectedCategory, listType, currentPage, search])

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/apps/filters/categories`)
      .then(res => res.json())
      .then(setCategories)
  }, [])

  const totalPagesDummy = totalPages || 10 // substitua com valor real se disponível

  const renderPagination = () => (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            href="#"
            onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
          />
        </PaginationItem>

        {[...Array(totalPagesDummy)].map((_, i) => (
          <PaginationItem key={i}>
            <PaginationLink
              href="#"
              isActive={i + 1 === currentPage}
              onClick={() => setCurrentPage(i + 1)}
            >
              {i + 1}
            </PaginationLink>
          </PaginationItem>
        ))}

        <PaginationItem>
          <PaginationNext
            href="#"
            onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPagesDummy))}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )

  return (
    <div className="p-6 space-y-4">
      <Card>
        <CardContent className="p-4 flex flex-col gap-4">
          <div className="flex flex-wrap gap-2 items-center">
            <Input
              placeholder="Search apps or developers..."
              value={search}
              onChange={(e) => {
                setCurrentPage(1)
                setSearch(e.target.value)
              }}
              className="max-w-sm"
            />

            <Select onValueChange={setSelectedCategory} value={selectedCategory}>
              <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Filter by Category" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select onValueChange={setListType} value={listType}>
              <SelectTrigger className="w-[150px]">
                <SelectValue placeholder="List Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Top Free">Top Free</SelectItem>
                <SelectItem value="Top Paid">Top Paid</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Icon</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Developer</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>List</TableHead>
                <TableHead>Rank</TableHead>
                <TableHead>Price</TableHead>
                <TableHead className="text-right">Downloads</TableHead>
                <TableHead className="text-right">Revenue</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {apps.map((app) => (
                <TableRow key={app.id}>
                  <TableCell>
                    <img
                      src={app.icon_url}
                      alt="icon"
                      className="w-10 h-10 rounded-xl"
                    />
                  </TableCell>
                  <TableCell>{app.name}</TableCell>
                  <TableCell>{app.developer}</TableCell>
                  <TableCell>{app.category}</TableCell>
                  <TableCell>{app.list_type}</TableCell>
                  <TableCell>{app.rank ?? "-"}</TableCell>
                  <TableCell>{app.list_type === "Top Paid" ? app.price : "-"}</TableCell>
                  <TableCell className="text-right">
                    {(app.monthly_downloads_estimate ?? 0).toLocaleString()}
                  </TableCell>
                  <TableCell className="text-right">
                    ${(app.monthly_revenue_estimate ?? 0).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {renderPagination()}
        </CardContent>
      </Card>
    </div>
  )
}
