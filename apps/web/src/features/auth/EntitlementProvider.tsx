import { useQuery } from "@tanstack/react-query";
import type { ReactNode } from "react";

import { AccessDenied } from "@/components/shared/AccessDenied";
import { PageLoader } from "@/components/shared/PageLoader";
import { apiRequest } from "@/lib/apiClient";

import { EntitlementContext } from "./entitlementContext";
import type { DataScope, Entitlements, Permission, Role } from "./permissions";

interface EntitlementsResponse {
  upn: string;
  name: string;
  role: Role;
  data_scope: DataScope;
  permissions: Permission[];
  scope_size: number;
}

function toEntitlements(response: EntitlementsResponse): Entitlements {
  return {
    upn: response.upn,
    name: response.name,
    role: response.role,
    dataScope: response.data_scope,
    permissions: new Set(response.permissions),
    scopeSize: response.scope_size,
  };
}

/** Loads role, permissions and data scope from the API. The UI never derives them from the token. */
export function EntitlementProvider({ children }: { children: ReactNode }) {
  const { data, error, isPending } = useQuery({
    queryKey: ["me", "entitlements"],
    queryFn: () => apiRequest<EntitlementsResponse>("/me/entitlements"),
    select: toEntitlements,
    staleTime: Infinity,
  });

  if (isPending) return <PageLoader />;
  if (error) {
    return (
      <div className="p-6">
        <AccessDenied detail={error.message} />
      </div>
    );
  }
  return <EntitlementContext.Provider value={data}>{children}</EntitlementContext.Provider>;
}
