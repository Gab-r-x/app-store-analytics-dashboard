import { Suspense } from "react"
import AnalysisDashboard from "./_components/analysis-dashboard"

export default function AnalysisPage() {
  return (
    <div className="p-6 space-y-6">
      <Suspense fallback={<div className="text-muted-foreground text-sm">Loading charts...</div>}>
        <AnalysisDashboard />
      </Suspense>
    </div>
  )
}
