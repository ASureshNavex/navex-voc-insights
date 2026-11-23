import { cva, type VariantProps } from "class-variance-authority";
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

const noticeVariants = cva("rounded-md border border-l-[3px] px-3.5 py-2.5 text-sm", {
  variants: {
    tone: {
      info: "border-link/25 border-l-link bg-link-weak text-link",
      caution: "border-rating-yellow/50 border-l-rating-yellow bg-rating-yellow-weak text-rating-yellow-ink",
      error: "border-rating-red/30 border-l-rating-red bg-rating-red-weak text-rating-red-ink",
    },
  },
  defaultVariants: { tone: "info" },
});

type NoticeProps = VariantProps<typeof noticeVariants> & { children: ReactNode; className?: string };

export function Notice({ tone, children, className }: NoticeProps) {
  return (
    <div role={tone === "error" ? "alert" : "note"} className={cn(noticeVariants({ tone }), className)}>
      {children}
    </div>
  );
}
