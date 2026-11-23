import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { useEntitlements } from "@/features/auth";
import { apiRequest } from "@/lib/apiClient";
import type { Page } from "@/types/api";

import type { AccountFilters, AccountRow, PortfolioSummary } from "./types";

const PAGE_SIZE = 50;

// The data scope is part of every key, so cached rows can never cross a scope change.

export function usePortfolioSummary() {
  const { dataScope, upn } = useEntitlements();
  return useQuery({
    queryKey: ["portfolio", "summary", dataScope, upn],
    queryFn: () => apiRequest<PortfolioSummary>("/portfolio/summary"),
  });
}

export function useAccounts(filters: AccountFilters, page: number) {
  const { dataScope, upn } = useEntitlements();
  return useQuery({
    queryKey: ["accounts", dataScope, upn, filters, page],
    queryFn: ({ signal }) =>
      apiRequest<Page<AccountRow>>("/accounts", {
        query: { ...filters, limit: PAGE_SIZE, offset: page * PAGE_SIZE },
        signal,
      }),
    placeholderData: keepPreviousData,
  });
}
