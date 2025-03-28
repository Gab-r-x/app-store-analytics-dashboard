"use client"

import { Input } from "@/components/ui/input"
import { useEffect, useState } from "react"
import { Search } from "lucide-react"

interface Props {
  onSearch: (value: string) => void
  defaultValue?: string
}

export default function SearchHero({ onSearch, defaultValue = "" }: Props) {
  const [value, setValue] = useState(defaultValue)
  const [debouncedValue, setDebouncedValue] = useState(defaultValue)

  // Debounce effect: atualiza debouncedValue após 400ms sem digitar
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, 300)

    return () => clearTimeout(timer)
  }, [value])

  // Quando debouncedValue muda, dispara a busca
  useEffect(() => {
    onSearch(debouncedValue)
  }, [debouncedValue, onSearch])

  return (
    <div className="w-full flex flex-col items-center justify-center mt-[-2.5rem]">
      <div>
        <h1 className="text-2xl font-bold text-center">
          Explore App Store Rankings
        </h1>
        <p className="text-muted-foreground text-center">
          Find and analyze apps by category, revenue, downloads, and more...
        </p>
      </div>
      <div className="w-full max-w-xl mt-4 relative pt-4 pb-6">
        <Search
          className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground"
          size={20}
        />
        <Input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Search apps or developers..."
          className="h-14 text-lg pl-12 pr-4"
        />
      </div>
    </div>
  )
}
