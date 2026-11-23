# auth

Corp AD sign-in and entitlements. Requirements AUT-01 to AUT-09.

| File | Purpose |
|---|---|
| `AuthProvider.tsx` | MSAL provider; redirects to Entra when there is no session |
| `EntitlementProvider.tsx` | Loads role, permissions and data scope from `GET /me/entitlements` |
| `entitlementContext.ts` | `useEntitlements`, `usePermission` |
| `ProtectedRoute.tsx` | Route guard by permission |
| `permissions.ts` | Permission, role and scope types; keep in step with the API's `core/entitlements.py` |

This is the one feature other features may import, always through `index.ts`.
