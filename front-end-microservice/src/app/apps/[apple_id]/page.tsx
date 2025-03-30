import { notFound } from "next/navigation"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"
import ExpandableDescription from "../_components/expandable-description"
import ExpandableReview from "../_components/expandable-review"
import { Download, DollarSign, Star } from "lucide-react"

interface AppDetail {
  id: string
  name: string
  developer: string
  subtitle: string
  category: string
  category_rank: string
  list_type: string
  icon_url: string
  screenshots: string[]
  rating_summary: string
  description: string
  reviews: any[]
  monthly_downloads_estimate: number
  monthly_revenue_estimate: number
  url: string
  general_info: Record<string, string>
}

function formatCompactNumber(num: number): string {
  if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`
  if (num >= 1_000) return `${(num / 1_000).toFixed(0)}K`
  return num.toString()
}

function getStarRating(rating: string): number {
  const match = rating.match(/\d+(\.\d+)?/)
  return match ? parseFloat(match[0]) : 0
}

function GeneralInfoCard({ info }: { info: Record<string, string> }) {
  return (
    <Card>
      <CardContent className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
        {Object.entries(info).map(([key, value]) => (
          <div key={key} className="flex flex-col">
            <span className="text-muted-foreground text-xs uppercase tracking-wide font-medium">
              {key}
            </span>
            <span className="text-sm text-foreground">{value}</span>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}

export default async function AppDetailPage({ params, }: { params: { apple_id: string | null } }) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/apps/${params.apple_id}`, {
    next: { revalidate: 60 }
  })

  if (!res.ok) {
    notFound()
  }

  const app: AppDetail = await res.json()
  const rating = getStarRating(app.rating_summary)

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-8">

      <div className="flex items-center gap-6">
        <img src={app.icon_url} alt={app.name} className="w-20 h-20 rounded-2xl" />
        <div>
          <h1 className="text-2xl font-bold">{app.name}</h1>
          <p className="text-muted-foreground">{app.subtitle}</p>
          <div className="flex flex-wrap gap-2 mt-2">
            <Badge variant="outline">{app.category}</Badge>
            <Badge variant="secondary">{app.list_type}</Badge>
            {app.category_rank && <Badge>Rank: {app.category_rank}</Badge>}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card>
          <CardContent className="px-2 py-1 sm:px-4 sm:py-4 flex flex-col items-center">
            <Download className="mb-2 text-green-600 w-5 h-5 sm:w-6 sm:h-6" />
            <p className="text-xl sm:text-3xl font-semibold">
              {formatCompactNumber(app.monthly_downloads_estimate ?? 0)} 
            </p>
            <p className="text-muted-foreground text-xs sm:text-sm text-center">Monthly Downloads Estimate</p>
          </CardContent>
        </Card>


        <Card>
          <CardContent className="px-2 py-1 sm:px-4 sm:py-4 flex flex-col items-center">
            <DollarSign className="mb-2 text-green-600 w-5 h-5 sm:w-6 sm:h-6" />
            <p className="text-xl sm:text-3xl font-semibold">
              {app.monthly_revenue_estimate
                ? formatCompactNumber(app.monthly_revenue_estimate)
                : "-"}
            </p>
            <p className="text-muted-foreground text-sm">Monthly Revenue Estimate</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="px-2 py-1 sm:px-4 sm:py-4 flex flex-col items-center">
            <div className="flex gap-1 mb-2">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  size={24}
                  fill={i < Math.round(rating) ? "#facc15" : "none"}
                  stroke="#facc15"
                />
              ))}
            </div>
            <p className="text-xl sm:text-3xl font-semibold">{rating}/5</p>
            <p className="text-muted-foreground text-sm">{app.rating_summary}</p>
          </CardContent>
        </Card>
      </div>

      <Separator />

      {app.screenshots?.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Screenshots</h2>
          <Carousel className="w-full max-w-5xl">
            <CarouselContent>
              {app.screenshots.map((url, i) => (
                <CarouselItem key={i} className="basis-3/4 sm:basis-1/2 md:basis-1/3">
                  <img
                    src={url}
                    alt={`screenshot-${i}`}
                    className="rounded-xl shadow-md w-full h-auto object-cover"
                  />
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>
      )}

      <div className="space-y-2">
        <h2 className="text-lg font-semibold">Description</h2>
        {app.description ? (
          <ExpandableDescription text={app.description} />
        ) : (
          <p className="text-sm text-muted-foreground">No description available.</p>
        )}
      </div>

      {app.general_info && <GeneralInfoCard info={app.general_info} />}

      {app.reviews.slice(0, 5).map((review, i) => {
        const initials = review.author
          ? review.author
              .split(" ")
              .map((word: string) => word[0])
              .join("")
              .toUpperCase()
          : "?"

        const rating = (() => {
          const match = review.rating?.match(/\d+(\.\d+)?/)
          return match ? parseFloat(match[0]) : 0
        })()


        return (
          <div key={i} className="border-b pb-4 flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-muted flex items-center justify-center text-sm font-medium text-foreground">
              {initials}
            </div>

            <div className="flex-1 space-y-1">
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold">{review.title}</p>
                <div className="flex gap-0.5">
                  {[...Array(5)].map((_, j) => (
                    <Star
                      key={j}
                      size={14}
                      fill={j < rating ? "#facc15" : "none"}
                      stroke="#facc15"
                    />
                  ))}
                </div>
              </div>
              <p className="text-xs text-muted-foreground">
                {review.author} - {review.date}
              </p>
              <ExpandableReview text={review.body} />
            </div>
          </div>
        )
      })}

    </div>
  )
}
