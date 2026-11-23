# Coding standards

The standards are the skills in `.harness-records/skills/` (Claude Code reaches them through pointers in `.claude/skills/`). They are written for an AI harness and read equally well as a checklist for a developer or reviewer.

| Skill | Applies to |
|---|---|
| `clean-lean-architecture-code` | Every file: lean code, SOLID, loose coupling, comments that explain why, no AI chatter in source |
| `navex-voc-frontend-architecture` | `apps/web`: stack, folder structure, Corp AD sign-in, the HTTP client, permissions and route guards, query keys |
| `react-tailwind-shadcn-scss-dashboard` | `apps/web`: Tailwind, shadcn/ui, SCSS partials, loaders, responsive layout |
| `navex-fastapi-rest-apis` | `services/experience-api`: structure, contracts, scope binding, pagination |
| `navex-agentcore-runtime` | `services/account-scoring-agent`: graph structure, Jinja2 prompts, structured output, tool ports |
| `navex-security-code-review` | Every pull request: the blocking checks |
| `sgivp`, `test-design`, `open-item-settlement`, `bug-fix`, `pr-ready`, `release-check`, `knowledge-refresh`, `session-handoff` | How work is done, tested, reviewed, released and handed over: see `AGENTS.md` "How to work" |

## Project-specific rules on top of the skills

| Rule | Detail |
|---|---|
| Native controls | Buttons, inputs and dropdowns are native `button`, `input` and `select` elements styled with the shadcn/ui recipes in `components/ui`. Do not build custom dropdown or button widgets |
| No inline styles | Styling is Tailwind classes or classes from `src/styles`. No `style={{ }}` |
| No hex colours in components | Use the theme tokens: `bg-background`, `text-muted-foreground`, `bg-rating-red`, and so on |
| Permission checks | `<Can perform="...">` or `usePermission`. Never compare a role name in a component |
| Query keys | Include the data scope and the filters: `["accounts", dataScope, filters]` |
| Scope binding | Every API service function takes `CurrentUser` and applies `scope_filter` |
| Prompts | Only in `.j2` files, each with a context model and a render test |
| Requirement IDs | Name the requirement in the pull request title, for example `ACC-06 filter bar` |
| Copy | Take labels and messages from the latest prototype. No em dashes, emojis or decorative symbols |
| Shared schema | New tables and columns go in `packages/voc-data` with an Alembic revision |

## Quality gate

Run before every push. CI runs the same commands.

| Area | Command |
|---|---|
| Python lint and format | `uv run ruff check .` and `uv run ruff format --check .` |
| Python types | `uv run mypy` |
| Python tests | `uv run pytest` |
| Python dependencies | `uv run pip-audit` |
| Web types | `npm run typecheck` in `apps/web` |
| Web lint | `npm run lint` |
| Web tests | `npm test` |
| Web build | `npm run build` |
| Containers | `trivy image` on each built image; images run as a non-root user |

## Tests that must exist

| Area | Test |
|---|---|
| Access | A user cannot read an account outside scope by ID, list filter or export |
| Permissions | Each guarded endpoint rejects a role without the permission |
| Pagination | `limit` above the cap is rejected; ordering is stable |
| Token | Wrong audience, wrong issuer and an expired token are each rejected |
| Prompts | Every `.j2` file renders with its context model |
| Graph | The refresh graph runs end to end on fakes and publishes |
| Idempotency | A notification is not sent twice |
| UI guards | `<Can>` hides content without the permission |
