import { LoaderCircle } from "lucide-react";
import type { ComponentProps } from "react";

import { Button } from "@/components/ui/button";

type ButtonLoaderProps = ComponentProps<typeof Button> & { pending: boolean; pendingText: string };

/** A button for mutations: disabled with a spinner and active text while the request runs. */
export function ButtonLoader({ pending, pendingText, children, ...props }: ButtonLoaderProps) {
  return (
    <Button disabled={pending} {...props}>
      {pending && <LoaderCircle className="animate-spin" aria-hidden="true" />}
      {pending ? pendingText : children}
    </Button>
  );
}
