import type { ReactNode } from "react";

import { usePermission, type Permission } from "@/features/auth";

interface CanProps {
  perform: Permission;
  children: ReactNode;
  fallback?: ReactNode;
}

/** Renders its children only when the signed-in user holds the permission. */
export function Can({ perform, children, fallback = null }: CanProps) {
  return usePermission(perform) ? children : fallback;
}
