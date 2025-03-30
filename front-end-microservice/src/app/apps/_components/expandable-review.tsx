"use client"

import { useState } from "react"

export default function ExpandableReview({ text }: { text: string }) {
  const [expanded, setExpanded] = useState(false)
  const MAX_LINES = 4

  return (
    <div className="text-sm leading-relaxed">
      <div
        className={`overflow-hidden transition-all duration-300 ${
          expanded ? "" : "line-clamp-4"
        }`}
      >
        {text}
      </div>
      {text.length > 100 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-primary underline mt-1"
        >
          {expanded ? "Show less" : "View more..."}
        </button>
      )}
    </div>
  )
}
