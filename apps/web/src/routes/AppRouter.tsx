import { lazy, Suspense, type ComponentType, type LazyExoticComponent } from "react";
import { createBrowserRouter, RouterProvider } from "react-router";

import { AccessDenied } from "@/components/shared/AccessDenied";
import { AppShell } from "@/components/shared/AppShell";
import { PageLoader } from "@/components/shared/PageLoader";
import { ProtectedRoute, type Permission } from "@/features/auth";
import { NotificationsPage } from "@/features/notifications";

import { LandingRedirect } from "./LandingRedirect";
import { NAVIGATION } from "./navigation";

// Each feature is its own bundle, so a user never downloads screens their role cannot open.
const ScorecardPage = lazy(() => import("@/features/accounts").then((m) => ({ default: m.ScorecardPage })));
const ManagerSummaryPage = lazy(() => import("@/features/leadership").then((m) => ({ default: m.ManagerSummaryPage })));
const CustomReportsPage = lazy(() => import("@/features/leadership").then((m) => ({ default: m.CustomReportsPage })));
const AdminHomePage = lazy(() => import("@/features/admin").then((m) => ({ default: m.AdminHomePage })));
const WeeklyChangesPage = lazy(() => import("@/features/admin").then((m) => ({ default: m.WeeklyChangesPage })));
const SourceHealthPage = lazy(() => import("@/features/admin").then((m) => ({ default: m.SourceHealthPage })));
const UsageAuditPage = lazy(() => import("@/features/admin").then((m) => ({ default: m.UsageAuditPage })));
const KnowledgeHubPage = lazy(() => import("@/features/knowledge-hub").then((m) => ({ default: m.KnowledgeHubPage })));
const DigestsPage = lazy(() => import("@/features/digests").then((m) => ({ default: m.DigestsPage })));

function guarded(permission: Permission, Page: LazyExoticComponent<ComponentType> | ComponentType) {
  return (
    <ProtectedRoute permission={permission}>
      <Suspense fallback={<PageLoader />}>
        <Page />
      </Suspense>
    </ProtectedRoute>
  );
}

const router = createBrowserRouter([
  {
    element: <AppShell navigation={NAVIGATION} />,
    children: [
      { index: true, element: <LandingRedirect /> },
      { path: "accounts", element: guarded("scorecard:read", ScorecardPage) },
      // Deep link from an alert email or a Gainsight CTA: the scorecard with this account opened.
      { path: "accounts/:sfdcAccountId", element: guarded("scorecard:read", ScorecardPage) },
      { path: "notifications", element: guarded("notifications:read", NotificationsPage) },
      { path: "leadership/summary", element: guarded("manager_summary:read", ManagerSummaryPage) },
      { path: "leadership/reports", element: guarded("custom_reports:manage", CustomReportsPage) },
      { path: "admin/home", element: guarded("admin_home:read", AdminHomePage) },
      { path: "admin/weekly-changes", element: guarded("weekly_changes:read", WeeklyChangesPage) },
      { path: "admin/source-health", element: guarded("source_health:read", SourceHealthPage) },
      { path: "admin/usage", element: guarded("usage_audit:read", UsageAuditPage) },
      { path: "admin/digests", element: guarded("digests:manage", DigestsPage) },
      { path: "knowledge-hub", element: guarded("knowledge_hub:upload", KnowledgeHubPage) },
      { path: "403", element: <AccessDenied /> },
      { path: "*", element: <LandingRedirect /> },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
