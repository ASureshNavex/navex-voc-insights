import type { Rating } from "@/types/api";

/** Wire shapes of the accounts and portfolio endpoints, as the API returns them. */

export type AccountSort = "priority" | "arr" | "renewal";

export interface AccountFilters {
  status: Rating[];
  q: string;
  sort: AccountSort;
  segment?: string;
  arr_tier?: "50k_plus" | "under_50k";
  region?: string;
  exec_sponsor?: string;
  account_executive?: string;
  super_product_family?: string;
  theme?: string;
  issue_status?: string;
  renewal_window?: "within_180" | "beyond_180";
  new_only?: boolean;
  cxm?: string;
  team?: string;
}

export const DEFAULT_FILTERS: AccountFilters = { status: ["R", "Y", "G"], q: "", sort: "priority" };

export interface ThemeChip {
  theme_id: string;
  name: string;
  path: string;
  negative_volume: number;
  is_primary: boolean;
}

export interface Verbatim {
  verbatim_id: string;
  text: string;
  source: string;
  feedback_date: string;
  product: string | null;
}

export interface AccountRow {
  sfdc_account_id: string;
  name: string;
  rating: Rating;
  previous_rating: Rating | null;
  status_tag: "new_red" | "repeat_red" | "new_yellow" | null;
  churn_language: boolean;
  arr: string;
  region: string;
  segment: string;
  cxm: string | null;
  exec_sponsor: string | null;
  account_executive: string | null;
  next_renewal_date: string | null;
  rule: { code: string; text: string };
  issue_status: string | null;
  nps: { category: string; date: string | null } | null;
  products: string[];
  explanation: string | null;
  themes: ThemeChip[];
  top_verbatim: Verbatim | null;
}

export interface AccountRef {
  sfdc_account_id: string;
  name: string;
  arr: string;
}

export interface RatingCard {
  count: number;
  arr: string;
  new_this_week: AccountRef[];
  repeat: AccountRef[];
}

export interface PortfolioSummary {
  total_accounts: number;
  red: RatingCard;
  yellow: RatingCard;
  last_refresh_at: string | null;
  next_refresh_at: string | null;
}
