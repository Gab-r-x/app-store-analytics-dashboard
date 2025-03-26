"use client"

import { useState } from "react"

interface Props {
  text: string
  maxChars?: number
}

export default function ExpandableDescription({ text, maxChars = 400 }: Props) {
  const [expanded, setExpanded] = useState(false)

  const shouldTruncate = text.length > maxChars
  const visibleText = expanded || !shouldTruncate ? text : text.slice(0, maxChars) + "..."

  return (
    <div className="text-sm leading-relaxed space-y-2">
      <p className="whitespace-pre-line">{visibleText}</p>

      {shouldTruncate && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-sm text-blue-600 hover:underline"
        >
          {expanded ? "View less" : "View more..."}
        </button>
      )}
    </div>
  )
}
