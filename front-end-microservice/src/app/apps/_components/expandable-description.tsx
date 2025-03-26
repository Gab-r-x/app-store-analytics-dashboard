"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"

interface Props {
  text: string
  maxParagraphs?: number
}

export default function ExpandableDescription({ text, maxParagraphs = 4 }: Props) {
  const [expanded, setExpanded] = useState(false)
  const paragraphs = text.split("\t")

  const visibleParagraphs = expanded ? paragraphs : paragraphs.slice(0, maxParagraphs)

  return (
    <div className="space-y-3 text-sm leading-relaxed">
      {visibleParagraphs.map((p, i) => (
        <p key={i}>{p}</p>
      ))}

      {paragraphs.length > maxParagraphs && (
        <Button
          variant="link"
          size="sm"
          onClick={() => setExpanded(!expanded)}
          className="p-0 text-primary"
        >
          {expanded ? "View less" : "View more..."}
        </Button>
      )}
    </div>
  )
}
