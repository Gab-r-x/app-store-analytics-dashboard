"use client"

import { Input } from "@/components/ui/input"
import { useState } from "react"
import { Search } from "lucide-react"

interface Props {
  onSearch: (value: string) => void
  defaultValue?: string
}

export default function SearchHero({ onSearch, defaultValue = "" }: Props) {
  const [value, setValue] = useState(defaultValue)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    onSearch(value)
  }

  return (
    <div className="w-full flex flex-col items-center justify-center py-12 space-y-4">
      <h1 className="text-3xl font-bold text-center">Explore App Store Rankings</h1>
      <p className="text-muted-foreground text-center">
        Find and analyze apps by category, revenue, downloads, and more
      </p>

      <form
        onSubmit={handleSearch}
        className="w-full max-w-xl mt-4 relative"
      >
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground" size={20} />
        <Input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Search apps or developers..."
          className="h-14 text-lg pl-12 pr-4"
        />
      </form>
    </div>
  )
}
