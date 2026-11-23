import type { ReactNode } from "react";
import { Navigate } from "react-router";

import { usePermission } from "./entitlementContext";
import type { Permission } from "./permissions";

/** Route-level guard. The API enforces the same permission; this only avoids a dead screen. */
export function ProtectedRoute({ permission, children }: { permission: Permission; children: ReactNode }) {
  return usePermission(permission) ? children : <Navigate to="/403" replace />;
}
