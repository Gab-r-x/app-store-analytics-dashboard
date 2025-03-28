"use client"

import { useEffect, useState } from "react"
import DownloadChart from "./download-chart"
import RevenueChart from "./revenue-chart"
import MrrPerDownloadChart from "./mrr-download-chart"

export default function AnalysisDashboard() {
  const [downloads, setDownloads] = useState([])
  const [revenue, setRevenue] = useState([])
  const [mrr, setMrr] = useState([])

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/analysis/downloads`)
      .then(res => res.json())
      .then(setDownloads)

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/analysis/revenue`)
      .then(res => res.json())
      .then(setRevenue)

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/analysis/mrr-downloads`)
      .then(res => res.json())
      .then(setMrr)
  }, [])

  return (
    <div className="space-y-6 text-center">
      <div>
        <h1 className="text-2xl font-bold">Category Performance Analysis</h1>
        <p className="text-muted-foreground">
          Compare app categories based on total downloads, revenue, and MRR/download rate.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-lg font-semibold mb-1">Download Analysis</h2>
          <p className="text-sm text-muted-foreground mb-2">
            Shows which categories are driving the most downloads.
          </p>
          <DownloadChart data={downloads} title="Download Analysis" />
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-1">Revenue per Category</h2>
          <p className="text-sm text-muted-foreground mb-2">
            Highlights the revenue distribution across app categories.
          </p>
          <RevenueChart data={revenue} />
        </div>

        <div>
          <h2 className="text-lg font-semibold mb-1">MRR / Download Rate</h2>
          <p className="text-sm text-muted-foreground mb-2">
            Measures monetization efficiency by category (MRR per download).
          </p>
          <MrrPerDownloadChart data={mrr} />
        </div>
      </div>
    </div>
  )
}
