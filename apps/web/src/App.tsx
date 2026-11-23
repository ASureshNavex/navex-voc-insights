import { QueryClientProvider } from "@tanstack/react-query";

import { AuthProvider, EntitlementProvider } from "@/features/auth";
import { queryClient } from "@/lib/queryClient";
import { AppRouter } from "@/routes/AppRouter";

export function App() {
  return (
    <AuthProvider>
      <QueryClientProvider client={queryClient}>
        <EntitlementProvider>
          <AppRouter />
        </EntitlementProvider>
      </QueryClientProvider>
    </AuthProvider>
  );
}
