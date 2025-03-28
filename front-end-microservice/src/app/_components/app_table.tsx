"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import {
  Card,
  CardContent,
} from "@/components/ui/card"
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
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination"
import { ArrowUpDown } from "lucide-react"
import SearchHero from "./search-hero"

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

function formatCompactNumber(num: number): string {
  if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`
  if (num >= 1_000) return `${(num / 1_000).toFixed(0)}K`
  return num.toString()
}

const PAGE_SIZE = 20

export default function Dashboard() {
  const [apps, setApps] = useState<App[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState("Business")
  const [listType, setListType] = useState("Top Free")
  const [search, setSearch] = useState("")
  const [totalApps, setTotalApps] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [sortBy, setSortBy] = useState<string>("rank")
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc")
  const [filters] = useState<any>({})

  const totalPages = Math.ceil(totalApps / PAGE_SIZE)

  const fetchApps = async () => {
    const baseUrl = search
      ? `${process.env.NEXT_PUBLIC_API_URL}/apps/search`
      : `${process.env.NEXT_PUBLIC_API_URL}/apps`

    const url = new URL(baseUrl)
    url.searchParams.set("limit", PAGE_SIZE.toString())
    url.searchParams.set("skip", ((currentPage - 1) * PAGE_SIZE).toString())

    url.searchParams.append("category", selectedCategory)
    url.searchParams.append("list_type", listType)
    url.searchParams.append("sort_by", sortBy)
    url.searchParams.append("sort_order", sortOrder)
    if (search) url.searchParams.set("q", search)

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== "") {
        url.searchParams.append(key, String(value))
      }
    })

    const res = await fetch(url.toString())
    const data = await res.json()

    setApps(data?.apps ?? [])
    setTotalApps(data?.total ?? 0)
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

  const router = useRouter()

  return (
    
    <div className="p-6 space-y-2">
      <SearchHero
        onSearch={(val) => {
            setSearch(val)
            setCurrentPage(1)
        }}
        defaultValue={search}
      />
      <Card>
        <CardContent className="p-4 flex flex-col gap-4">
          <div className="flex flex-wrap gap-2 items-center">


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
                <TableRow key={app.id}
                  onClick={() => router.push(`/apps/${app.apple_id}`)}
                  className="cursor-pointer hover:bg-muted"
                >
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
                    {formatCompactNumber(app.monthly_downloads_estimate ?? 0)}
                  </TableCell>
                  <TableCell className="text-right">
                    {app.monthly_revenue_estimate ? formatCompactNumber(app.monthly_revenue_estimate) : "-"}
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
