import { Navigate } from "react-router";

import { PageHeader } from "@/components/shared/PageHeader";
import { useEntitlements } from "@/features/auth";

import { NAVIGATION } from "./navigation";

/** Sends each role to its first permitted page. Roles without modules yet see a holding page. */
export function LandingRedirect() {
  const { permissions } = useEntitlements();
  const landing = NAVIGATION.find((item) => permissions.has(item.permission));
  if (landing) return <Navigate to={landing.to} replace />;
  return (
    <PageHeader
      title="VoC Insights"
      description="You are signed in. The modules for your role are still being decided, so there is nothing to show yet."
    />
  );
}
