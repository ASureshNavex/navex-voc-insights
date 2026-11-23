import type { ComponentProps } from "react";

import { cn } from "@/lib/utils";

export function Label({ className, ...props }: ComponentProps<"label">) {
  return (
    <label
      className={cn("text-[0.8125rem] font-medium text-secondary-foreground", className)}
      {...props}
    />
  );
}
