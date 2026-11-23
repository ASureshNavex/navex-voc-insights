# Project constitution

## The rules this repository never breaks; the install numbers them P1 to P13

- Parity first. Do not add a feature, field, screen or filter that is not in `docs/01-product/requirements.md`. Propose it instead.
- Every API query takes `CurrentUser` and applies `scope_filter`. An account outside scope is `404`.
- The UI checks permissions with `<Can>` or `usePermission`, never role names.
- No user management, role selector or persona switcher in the product. Identity comes from SSO.
- Tokens stay in memory. Nothing sensitive in `localStorage`, `sessionStorage` or logs.
- Buttons, inputs and dropdowns are native `button`, `input` and `select` elements styled with the shadcn/ui recipes. No inline styles; no hex colours in components.
- Notifications open from the bell icon in the top bar.
- Prompts live only in `.j2` files with a typed context model and a render test. Customer text is passed as delimited data.
- Ratings come from code and the versioned rule set. A model writes explanations only.
- Parameterized SQL only. Lists are paged with a cap and a stable order.
- No secrets, keys or tokens in the repository. AWS access uses the `navexsso` profile, never static keys.
- Copy comes from the prototype. No em dashes, emojis or decorative symbols.
- Source files contain no placeholder comments, change notes or narration.
