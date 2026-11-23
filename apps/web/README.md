# Web app

React 19, TypeScript 5, Vite, Tailwind CSS, shadcn/ui recipes on native elements, SCSS theme partials, TanStack Query and Table, MSAL.

```bash
cp .env.example .env      # fill in the Entra values from NAVEX IT
npm install
npm run dev               # http://localhost:5173, proxies /api to localhost:8000
```

| Command | Purpose |
|---|---|
| `npm run typecheck` | Strict TypeScript |
| `npm run lint` | ESLint, including the rules below |
| `npm test` | Vitest |
| `npm run build` | Production build into `dist/` |

## Structure

```text
src/
├── assets/              NAVEX logo
├── components/ui/       shadcn-style primitives on native button, input, select, table
├── components/shared/   AppShell, Can, PageHeader, loaders, Notice, RatingBadge
├── features/            One folder per capability; each exports through index.ts
├── lib/                 authConfig, msal, apiClient, queryClient, utils
├── routes/              AppRouter, navigation, landing redirect
├── styles/              SCSS partials: variables, themes, mixins, loaders, shell
└── types/               Shared wire types
```

## Rules the linter enforces

- No inline `style` attribute and no raw HTML rendering.
- No `fetch` outside `src/lib/apiClient.ts`.
- A feature is imported through its `index.ts`, never its internal files.

## Adding a shadcn/ui primitive

`components.json` is in place, so `npx shadcn@latest add <component>` works. Buttons, inputs and dropdowns stay native elements: restyle the generated file to wrap `button`, `input` or `select` if it does not already.

## What is built

Sign-in, entitlements, permission guards, the app shell with the notification bell, and the scorecard reference slice. Every other screen is a placeholder that names its unit of work. See each feature's `README.md` and `docs/04-delivery/units-of-work.md`.
