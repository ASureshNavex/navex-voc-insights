import { createContext, useContext } from "react";

import type { Entitlements, Permission } from "./permissions";

export const EntitlementContext = createContext<Entitlements | null>(null);

export function useEntitlements(): Entitlements {
  const entitlements = useContext(EntitlementContext);
  if (!entitlements) throw new Error("useEntitlements must be used inside EntitlementProvider.");
  return entitlements;
}

export function usePermission(permission: Permission): boolean {
  return useEntitlements().permissions.has(permission);
}
