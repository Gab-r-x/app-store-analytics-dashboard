import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "@/components/ui/popover"
  import {
    Button
  } from "@/components/ui/button"
  import {
    Input
  } from "@/components/ui/input"
  import {
    Slider
  } from "@/components/ui/slider"
  import {
    Checkbox
  } from "@/components/ui/checkbox"
  import {
    Label
  } from "@/components/ui/label"
  import { SlidersHorizontal } from "lucide-react"
  import { useEffect, useState } from "react"
  
  interface FiltersProps {
    filters: any
    setFilters: (filters: any) => void
  }
  
  export function AppFilters({ filters, setFilters }: FiltersProps) {
    const [labels, setLabels] = useState<string[]>([])
  
    useEffect(() => {
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/apps/filters/labels`)
        .then(res => res.json())
        .then(setLabels)
    }, [])
  
    const handleChange = (field: string, value: any) => {
      setFilters({ ...filters, [field]: value })
    }
  
    const resetFilters = () => {
      setFilters({})
    }
  
    return (
      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline" size="sm" className="flex gap-2">
            <SlidersHorizontal size={16} /> Filters
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[300px] space-y-4">
          <div className="flex flex-col gap-2">
            <Label>Labels</Label>
            {labels.map(label => (
              <div key={label} className="flex items-center gap-2">
                <Checkbox
                  checked={filters.label === label}
                  onCheckedChange={() => handleChange("label", label)}
                  id={label}
                />
                <Label htmlFor={label}>{label}</Label>
              </div>
            ))}
          </div>
  
          <div className="flex items-center justify-between gap-2">
            <Label>Revenue Min</Label>
            <Input
              type="number"
              className="w-24"
              value={filters.revenue_min || ""}
              onChange={(e) => handleChange("revenue_min", Number(e.target.value))}
            />
          </div>
  
          <div className="flex items-center justify-between gap-2">
            <Label>Downloads Min</Label>
            <Input
              type="number"
              className="w-24"
              value={filters.downloads_min || ""}
              onChange={(e) => handleChange("downloads_min", Number(e.target.value))}
            />
          </div>
  
          <div className="flex items-center justify-between gap-2">
            <Label>Rating Min</Label>
            <Input
              type="number"
              className="w-24"
              step="0.1"
              max={5}
              min={0}
              value={filters.rating_min || ""}
              onChange={(e) => handleChange("rating_min", Number(e.target.value))}
            />
          </div>
  
          <div className="flex items-center gap-2">
            <Checkbox
              checked={filters.has_in_app_purchases || false}
              onCheckedChange={(val) => handleChange("has_in_app_purchases", val)}
              id="iap"
            />
            <Label htmlFor="iap">Has In-App Purchases</Label>
          </div>
  
          <Button variant="ghost" size="sm" className="w-full mt-4" onClick={resetFilters}>
            Reset Filters
          </Button>
        </PopoverContent>
      </Popover>
    )
  }
  