---
name: react-tailwind-shadcn-scss-dashboard
description: Styling for the web app - Tailwind, shadcn/ui primitives, parameterized SCSS theme partials, no inline styles or hex colours, the top-bar shell, responsive grids and tables, and the three standard loaders. Use when styling or laying out anything under apps/web/src, adding a shadcn component, or touching apps/web/src/styles.
---

# React Dashboard UI Styling (Tailwind CSS + shadcn/ui + Parameterized SCSS)

When building, styling, or refactoring UI components in this React dashboard, strictly combine **Tailwind CSS**, **shadcn/ui** (MIT-licensed), and **parameterized SCSS partials** according to the rules below.

## 1. Zero Inline Styles & Class-Based Styling
- **Strictly Forbidden:** Never use inline `style={{ ... }}` attributes on JSX elements. All styling must be applied via Tailwind utility classes or semantic SCSS classes.
- **Dynamic Values via CSS Variables:** If a component requires dynamic values (such as chart bar widths, progress percentages, or dynamic grid spans), bind them to CSS custom properties in SCSS or use Tailwind arbitrary utility classes (`w-full`, `data-[state=active]:...`) rather than inline React style objects.
- **Class Merging Convention:** Always use the `cn()` utility (`src/lib/utils.ts`, combining `clsx` and `tailwind-merge`) to compose conditional classes cleanly.

## 2. Parameterized SCSS & Theme Partials Architecture
Organize custom styles and theme parameters in a dedicated `src/styles/` folder using SCSS partials (`_filename.scss`) that feed directly into shadcn/ui's CSS variables:

```text
src/styles/
|-- _variables.scss       # Parameterized SCSS theme variables (\$brand-hue, radius-base, top-bar height)
|-- _themes.scss          # Maps SCSS parameters to shadcn/ui CSS custom properties (:root and .dark)
|-- _mixins.scss          # Reusable responsive and layout mixins (@mixin card-surface, @mixin truncate)
|-- _loaders.scss         # Keyframe animations and class-based skeleton/spinner styles
`-- main.scss             # Entry file importing Tailwind (@import "tailwindcss";) and all partials
```

- **Parameterized Theme Tweaking:** Define core brand knobs as SCSS variables in `_variables.scss` (e.g., `$primary-hsl: 221.2 83.2% 53.3%;`, `$border-radius: 0.5rem;`, `$top-bar-height: 3.5rem;`) and inject them into `:root` and `.dark` inside `_themes.scss` so changing a single SCSS parameter updates the entire shadcn/ui and Tailwind theme.
- **Scoped Component Classes:** When complex animations, scrollbars, or multi-state transitions are too verbose for Tailwind utilities, define semantic BEM-style classes (e.g., `.dashboard-shell__viewport`, `.metric-card--highlight`) inside SCSS partials using `@apply` or CSS variables.

## 3. Component Architecture & Ownership
- **Use shadcn/ui Primitives First:** Check `src/components/ui/` before creating custom UI controls. Add primitives via CLI (`npx shadcn@latest add <component>`).
- **Keep `src/components/ui/` Pure:** Never put API calls, business logic, or RBAC hooks (`usePermission`) inside `src/components/ui/`. Compose domain-specific widgets inside `src/features/`.

## 4. Standardized Loaders & Async States
Never leave blank screens or build ad-hoc loading spinners per component. Use a standardized three-tier loader pattern:
1. **Route / Page Loader (`<PageLoader />`):** Used inside `<Suspense>` boundaries for lazy-loaded RBAC routes. Renders a centered, branded CSS spinner (`.loader-spinner`) defined in `_loaders.scss`.
2. **Layout Skeletons (`<Skeleton />`):** Used for initial TanStack Query data loads on KPI cards, charts, and tables. Always match the exact height and grid layout of the resolved content to prevent Cumulative Layout Shift (CLS).
3. **Inline Action Loaders (`<ButtonLoader />`):** For form submissions or export actions, disable the shadcn `<Button>` and render a class-styled spinning icon (`animate-spin mr-2 h-4 w-4`) alongside active text (e.g., `"Saving..."`).

## 5. Responsive Dashboard Shell & Breakpoints
- **Mobile-First Breakpoints:** Write base mobile classes first, scaling up with `sm:`, `md:`, `lg:`, and `xl:`.
- **Responsive App Shell:** A sticky top bar with tabs, matching the latest prototype (open item 14), and a scrollable main area (`flex-1 overflow-y-auto p-4 md:p-6`). The tabs scroll horizontally on small screens. Only `components/shared/AppShell.tsx` knows the layout.
- **Responsive Grids & Tables:**
  - KPI Grid: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4`
  - Tables: Always wrap shadcn `<Table>` in `rounded-md border overflow-x-auto`, hide secondary columns on small viewports (`hidden md:table-cell`), and apply `tabular-nums` to all numeric columns.

## 6. Accessibility (a11y)
- Maintain WCAG AA contrast across all parameterized theme variants.
- Every icon-only `<Button variant="ghost" size="icon">` must include an `aria-label` or `<span className="sr-only">` label.
