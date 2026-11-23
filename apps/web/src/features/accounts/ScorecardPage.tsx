import { useState } from "react";

import { Notice } from "@/components/shared/Notice";
import { PageHeader } from "@/components/shared/PageHeader";
import { useEntitlements } from "@/features/auth";

import { AccountsTable } from "./AccountsTable";
import { useAccounts, usePortfolioSummary } from "./api";
import { FilterBar } from "./FilterBar";
import { RatingCards } from "./RatingCards";
import { DEFAULT_FILTERS } from "./types";

const timeOfDay = new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit" });

function refreshText(last: string | null, next: string | null): string {
  if (!last) return "Insights have not been refreshed yet.";
  const refreshed = `Insights refreshed at ${timeOfDay.format(new Date(last))}.`;
  return next ? `${refreshed} Next refresh at ${timeOfDay.format(new Date(next))}.` : refreshed;
}

/** The one view (SCR and ACC requirements). Reference slice for the remaining scorecard units. */
export function ScorecardPage() {
  const { name, scopeSize } = useEntitlements();
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const summary = usePortfolioSummary();
  const accounts = useAccounts(filters, 0);

  return (
    <>
      <PageHeader
        title="Scorecard"
        description={`${name}. ${scopeSize} ${scopeSize === 1 ? "account" : "accounts"} in view, sorted with red accounts that use churn language first, then by ARR.`}
      />
      {summary.data && (
        <Notice>{refreshText(summary.data.last_refresh_at, summary.data.next_refresh_at)}</Notice>
      )}
      {(summary.error ?? accounts.error) && (
        <Notice tone="error">{(summary.error ?? accounts.error)?.message}</Notice>
      )}
      <RatingCards summary={summary.data} />
      <FilterBar filters={filters} onChange={setFilters} />
      <AccountsTable accounts={accounts.data?.items} total={accounts.data?.total ?? 0} />
    </>
  );
}
