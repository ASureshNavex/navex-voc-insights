import { QueryClient } from "@tanstack/react-query";

import { ApiError } from "./apiClient";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      refetchOnWindowFocus: false,
      // Retrying cannot fix a missing permission, an unknown record or an unbuilt endpoint.
      retry: (failures, error) =>
        !(error instanceof ApiError && error.status < 500) && !isNotBuilt(error) && failures < 2,
    },
  },
});

function isNotBuilt(error: unknown): boolean {
  return error instanceof ApiError && error.status === 501;
}
