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
import { ArrowUpDown } from "lucide-react"

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
  const [totalApps, setTotalApps] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [sortBy, setSortBy] = useState<string>("")
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc")

  const totalPages = Math.ceil(totalApps / PAGE_SIZE)

  const fetchApps = async () => {
    const url = new URL(`${process.env.NEXT_PUBLIC_API_URL}/apps`)
    url.searchParams.set("limit", PAGE_SIZE.toString())
    url.searchParams.set("skip", ((currentPage - 1) * PAGE_SIZE).toString())
    if (selectedCategory) url.searchParams.append("category", selectedCategory)
    if (listType) url.searchParams.append("list_type", listType)
    if (sortBy) url.searchParams.append("sort_by", sortBy)
    if (sortOrder) url.searchParams.append("sort_order", sortOrder)
    if (search) {
      url.pathname = "/apps/search"
      url.searchParams.set("q", search)
    }

    const res = await fetch(url.toString())
    const data = await res.json()

    if (search) {
      setApps(data)
      setTotalApps(data.length)
    } else {
      setApps(data.apps)
      setTotalApps(data.total)
    }
  }

  useEffect(() => {
    fetchApps()
  }, [selectedCategory, listType, currentPage, search, sortBy, sortOrder])

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/apps/filters/categories`)
      .then(res => res.json())
      .then(setCategories)
  }, [])

  const toggleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(prev => (prev === "asc" ? "desc" : "asc"))
    } else {
      setSortBy(field)
      setSortOrder("desc")
    }
  }

  const renderPagination = () => {
    const pageNumbers = []
    const startPage = Math.max(1, currentPage - 2)
    const endPage = Math.min(totalPages, currentPage + 2)

    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push(i)
    }

    return (
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationLink href="#" onClick={() => setCurrentPage(1)}>&laquo;</PaginationLink>
          </PaginationItem>
          <PaginationItem>
            <PaginationPrevious href="#" onClick={() => setCurrentPage(p => Math.max(p - 1, 1))} />
          </PaginationItem>

          {pageNumbers.map(i => (
            <PaginationItem key={i}>
              <PaginationLink href="#" isActive={i === currentPage} onClick={() => setCurrentPage(i)}>
                {i}
              </PaginationLink>
            </PaginationItem>
          ))}

          <PaginationItem>
            <PaginationNext href="#" onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))} />
          </PaginationItem>
          <PaginationItem>
            <PaginationLink href="#" onClick={() => setCurrentPage(totalPages)}>&raquo;</PaginationLink>
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    )
  }

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
                <TableHead>
                  <Button variant="ghost" size="sm" onClick={() => toggleSort("rank")} className="flex items-center gap-1">
                    Rank <ArrowUpDown size={14} />
                  </Button>
                </TableHead>
                <TableHead>
                  <Button variant="ghost" size="sm" onClick={() => toggleSort("name")} className="flex items-center gap-1">
                    Name <ArrowUpDown size={14} />
                  </Button>
                </TableHead>
                <TableHead>Developer</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>List</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>
                  <Button variant="ghost" size="sm" onClick={() => toggleSort("downloads")} className="flex items-center gap-1">
                    Downloads <ArrowUpDown size={14} />
                  </Button>
                </TableHead>
                <TableHead>
                  <Button variant="ghost" size="sm" onClick={() => toggleSort("revenue")} className="flex items-center gap-1">
                    Revenue <ArrowUpDown size={14} />
                  </Button>
                </TableHead>
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
                  <TableCell>{app.rank ? `# ${app.rank}` : "-"}</TableCell>
                  <TableCell>{app.name}</TableCell>
                  <TableCell>{app.developer}</TableCell>
                  <TableCell>{app.category}</TableCell>
                  <TableCell>{app.list_type}</TableCell>
                  <TableCell>{app.list_type === "Top Paid" ? app.price : "-"}</TableCell>
                  <TableCell className="text-right">
                    {(app.monthly_downloads_estimate ?? 0).toLocaleString()}
                  </TableCell>
                  <TableCell className="text-right">
                    {app.monthly_revenue_estimate ? `$${app.monthly_revenue_estimate.toLocaleString()}` : "-"}
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
