"use client"

import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  ZAxis,
  CartesianGrid,
} from "recharts"
import { Card, CardContent } from "@/components/ui/card"

interface ClusterPoint {
  category: string
  cluster: number
  app_count: number
  avg_downloads: number
  avg_revenue: number
}

interface Props {
  data: ClusterPoint[]
}

function formatCompactNumber(num: number): string {
  if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1).replace(/\.0$/, "")}M`
  if (num >= 1_000) return `${(num / 1_000).toFixed(1).replace(/\.0$/, "")}K`
  return num.toString()
}

function groupByCategory(data: ClusterPoint[]): ClusterPoint[] {
  const grouped: Record<string, {
    category: string
    app_count: number
    totalDownloads: number
    totalRevenue: number
  }> = {}

  data.forEach(item => {
    const key = item.category
    if (!grouped[key]) {
      grouped[key] = {
        category: key,
        app_count: 0,
        totalDownloads: 0,
        totalRevenue: 0
      }
    }
    grouped[key].app_count += item.app_count
    grouped[key].totalDownloads += item.avg_downloads * item.app_count
    grouped[key].totalRevenue += item.avg_revenue * item.app_count
  })

  return Object.values(grouped).map(item => ({
    category: item.category,
    cluster: 0,
    app_count: item.app_count,
    avg_downloads: item.totalDownloads / item.app_count,
    avg_revenue: item.totalRevenue / item.app_count
  }))
}

export default function ClusterChart({ data }: Props) {
  const groupedData = groupByCategory(data)

  const maxDownloads = Math.max(...groupedData.map(d => d.avg_downloads || 0))
  const maxRevenue = Math.max(...groupedData.map(d => d.avg_revenue || 0))

  const calculateAxisMax = (value: number) => {
    const magnitude = Math.pow(10, Math.floor(Math.log10(value)))
    return Math.ceil(value / magnitude) * magnitude
  }

  return (
    <Card>
      <CardContent className="p-2 space-y-2">
        <ResponsiveContainer width="100%" height={400}>
          <ScatterChart
            margin={{ top: 20, right: 20, bottom: 40, left: 20 }}
          >
            <CartesianGrid />
            <XAxis
              dataKey="avg_downloads"
              name="Avg Downloads"
              tickFormatter={formatCompactNumber}
              domain={[0, calculateAxisMax(maxDownloads)]}
              tick={{ fontSize: 12 }}
              label={{ value: "Avg Downloads", position: "insideBottom", offset: -20 }}
            />
            <YAxis
              dataKey="avg_revenue"
              name="Avg Revenue"
              tickFormatter={formatCompactNumber}
              domain={[0, calculateAxisMax(maxRevenue)]}
              tick={{ fontSize: 12 }}
              label={{ value: "Avg Revenue", angle: -90, position: "insideLeft" }}
            />
            <ZAxis
              dataKey="app_count"
              range={[60, 400]}
              name="Number of Apps"
            />
            <Tooltip
              cursor={{ strokeDasharray: "3 3" }}
              formatter={(value: number, name: string) => {
                if (name === "app_count") return [`${value}`, "Apps"]
                return [formatCompactNumber(value), name]
              }}
              labelFormatter={(label: any, payload: any) => {
                const p = payload[0]?.payload
                return p?.category ?? ""
              }}
            />
            <Scatter
              name="Clusters"
              data={groupedData}
              fill="#6366f1"
            />
          </ScatterChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
