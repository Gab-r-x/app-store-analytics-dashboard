"use client"

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts"
import { Card, CardContent } from "@/components/ui/card"

interface Props {
  data: { category: string; mrr_per_download: number | null }[]
}

function formatCompactNumber(num: number): string {
  if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1).replace(/\.0$/, "")}M`
  if (num >= 1_000) return `${(num / 1_000).toFixed(1).replace(/\.0$/, "")}K`
  return num.toString()
}

export default function MrrPerDownloadChart({ data }: Props) {
  const cleanData = data.filter(item => typeof item.mrr_per_download === "number")
  const maxValue = Math.max(...cleanData.map(item => item.mrr_per_download || 0))

  const calculateYAxisMax = (value: number) => {
    const magnitude = Math.pow(10, Math.floor(Math.log10(value)))
    return Math.ceil(value / magnitude) * magnitude
  }

  const yAxisMax = calculateYAxisMax(maxValue)

  return (
    <Card>
      <CardContent className="p-2 space-y-2">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={cleanData}
            margin={{ top: 10, right: 30, left: 5, bottom: 25 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="category"
              angle={-45}
              textAnchor="end"
              interval={0}
              height={90}
              tick={{ fontSize: 12 }}
            />
            <YAxis
              tickFormatter={formatCompactNumber}
              domain={[0, yAxisMax]}
              tick={{ fontSize: 12 }}
            />
            <Tooltip formatter={(value: number) => formatCompactNumber(value)} />
            <Bar dataKey="mrr_per_download" fill="#facc15" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
