import { cn } from "@/lib/utils";
import type { Rating } from "@/types/api";

const RATINGS: Record<Rating, { label: string; badge: string; dot: string }> = {
  R: { label: "Red", badge: "bg-rating-red-weak text-rating-red-ink", dot: "bg-rating-red" },
  Y: { label: "Yellow", badge: "bg-rating-yellow-weak text-rating-yellow-ink", dot: "bg-rating-yellow" },
  G: { label: "Green", badge: "bg-rating-green-weak text-rating-green-ink", dot: "bg-rating-green" },
};

/** The rating in text as well as colour, so it never depends on colour alone. */
export function RatingBadge({ rating }: { rating: Rating }) {
  const { label, badge, dot } = RATINGS[rating];
  return (
    <span className={cn("inline-flex items-center gap-1.5 rounded-md px-2 py-0.5 text-[0.8125rem] font-bold", badge)}>
      <span className={cn("size-2 rounded-full", dot)} aria-hidden="true" />
      {label}
    </span>
  );
}
