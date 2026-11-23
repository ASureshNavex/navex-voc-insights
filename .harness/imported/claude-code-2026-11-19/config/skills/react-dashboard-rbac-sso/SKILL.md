---
name: react-dashboard-rbac-sso
description: Enforces React best practices, folder structure, JWT API integration, and architectural patterns for dashboards with RBAC and SSO.
---

# React Dashboard Architecture (RBAC, SSO & JWT APIs)

When generating, refactoring, or reviewing code for this React dashboard, strictly adhere to the following folder layout, authentication flows, RBAC patterns, and API conventions.

## 1. Codebase & Folder Structure
Organize code by domain/feature rather than technical file type so related components, hooks, and API calls stay colocated.

```text
src/
├── assets/               # Static images, fonts, global styles
├── components/           # Shared, dumb UI primitives (Buttons, Modals, DataTable, Layout)
├── features/             # Domain-specific modules (keep feature logic isolated here)
│   ├── auth/             # AuthProvider, useAuth, usePermission, <Can />, <ProtectedRoute />
│   ├── analytics/        # Feature components, chart widgets, and analytics API queries
│   ├── users/            # User management views and role assignment APIs
│   └── settings/         # User profile and preferences
├── lib/                  # Third-party library configurations (Axios instance, QueryClient, SSO config)
├── routes/               # AppRouter, route definitions, lazy-loaded route wrappers
├── types/                # Shared global TypeScript interfaces (JWT claims, API response wrappers)
└── App.tsx               # Top-level providers (SSO -> QueryClient -> AuthProvider -> AppRouter)
```

- **Isolation Rule:** Features in `src/features/` must not import internal components or hooks directly from sibling features. Share cross-feature logic via `src/components/` or `src/lib/`.

## 2. Authentication & SSO Rules
- **Use Official SDKs:** Always delegate OIDC/SAML flows to the chosen Identity Provider's official React SDK (e.g., `@auth0/auth0-react`, `@clerk/clerk-react`, `react-oidc-context`). Never write custom JWT parsing or manual OAuth2 token exchange flows.
- **Token Security:** Never store JWT access tokens or refresh tokens in `localStorage` or `sessionStorage`. Retrieve tokens dynamically in memory from the SSO SDK or rely on `HttpOnly` cookies via a Backend-for-Frontend (BFF).
- **Initialization Guards:** Always check the SDK's `isLoading` or `isInitializing` state before rendering protected routes to prevent UI flickering or premature login redirects.

## 3. JWT API Access & Interceptor Rules
- **Centralized HTTP Client:** Route all backend API calls through a single configured HTTP client in `src/lib/apiClient.ts` (e.g., Axios or a typed `fetch` wrapper). Never call raw `fetch` with manual headers inside components.
- **Dynamic Bearer Token Injection:** Use a request interceptor to retrieve the current JWT asynchronously from the SSO SDK and attach it to every outgoing request:
  ```ts
  // Pattern: Request Interceptor in src/lib/apiClient.ts
  apiClient.interceptors.request.use(async (config) => {
    const token = await getAccessTokenSilently(); // Provided by SSO SDK
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
  ```
- **Global 401 & 403 Handling:** Use a response interceptor to handle JWT expiration and authorization failures uniformly:
  - **401 Unauthorized:** Attempt a single silent token refresh via the SSO SDK; if refresh fails, clear local session state and redirect to SSO login.
  - **403 Forbidden:** Do not log the user out. Surface a global "Access Denied" toast/banner or redirect to `/403`.
- **Never Trust Decoded JWTs Alone for UI Truth:** While JWT claims can hold basic identity info (`sub`, `email`), fetch authoritative RBAC permissions from a dedicated `/api/me` endpoint (cached via TanStack Query) if roles/permissions change frequently.

## 4. Role-Based Access Control (RBAC)
- **Permission-Based Over Role-Based:** Never hardcode role checks inside UI components (e.g., avoid `user.role === 'admin'`). Always check granular permissions (e.g., `hasPermission('billing:write')`).
- **Declarative UI Guards:** Use a centralized `<Can perform="permission:name">` wrapper component and a `usePermission()` hook for conditional UI rendering.
- **Route-Level Protection:** Protect routes at the router level using a `<ProtectedRoute />` wrapper that verifies both authentication and required permissions, redirecting unauthorized access to `/403` or `/login`.
- **Bundle Splitting:** Lazy-load role-specific or heavy admin views using `React.lazy()` and `<Suspense>` so standard users do not download restricted code.

## 5. State Management Rules
- **Do Not Use Redux:** Do not install or suggest Redux or Redux Toolkit unless explicitly requested for complex, high-frequency client state.
- **Server State:** Use **TanStack Query (React Query)** or **SWR** for all backend data fetching, caching, dashboard metrics, and fetching user permission profiles (`/api/me`).
- **Global Client State:** Keep global client state minimal. Use React Context for auth/RBAC state and `useState` or **Zustand** strictly for lightweight UI state (e.g., sidebar toggles, active theme).
