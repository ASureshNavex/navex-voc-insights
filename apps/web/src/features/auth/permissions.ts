/** Permission names issued by GET /me/entitlements. Policy: docs/01-product/roles-and-access.md. */
export type Permission =
  | "scorecard:read"
  | "scorecard:filter_team"
  | "scorecard:trend"
  | "scorecard:export"
  | "account_brief:generate"
  | "saved_views:manage"
  | "digest_preferences:manage"
  | "notifications:read"
  | "manager_summary:read"
  | "custom_reports:manage"
  | "admin_home:read"
  | "weekly_changes:read"
  | "weekly_changes:email"
  | "knowledge_hub:upload"
  | "knowledge_hub:approve"
  | "source_health:read"
  | "source_health:check"
  | "usage_audit:read"
  | "digests:manage"
  | "access_list:read";

export type Role = "CXM" | "CXM_LEADERSHIP" | "ACCOUNT_EXECUTIVE" | "ELT" | "VOC_ADMIN";
export type DataScope = "OWN_BOOK" | "TEAM" | "REGION" | "ALL";

export interface Entitlements {
  upn: string;
  name: string;
  role: Role;
  dataScope: DataScope;
  permissions: ReadonlySet<Permission>;
  scopeSize: number;
}
