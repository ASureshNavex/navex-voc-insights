import type { NavItem } from "@/components/shared/AppShell";

/** Main navigation in display order. An item shows only when the user holds its permission. */
export const NAVIGATION: NavItem[] = [
  { to: "/accounts", label: "Scorecard", permission: "scorecard:read" },
  { to: "/leadership/summary", label: "Manager summary", permission: "manager_summary:read" },
  { to: "/leadership/reports", label: "Custom reports", permission: "custom_reports:manage" },
  { to: "/admin/home", label: "Admin home", permission: "admin_home:read" },
  { to: "/admin/weekly-changes", label: "Weekly changes", permission: "weekly_changes:read" },
  { to: "/knowledge-hub", label: "Knowledge hub", permission: "knowledge_hub:upload" },
  { to: "/admin/source-health", label: "Data source health", permission: "source_health:read" },
  { to: "/admin/usage", label: "Usage and audit", permission: "usage_audit:read" },
  { to: "/admin/digests", label: "Scheduled digests", permission: "digests:manage" },
];
