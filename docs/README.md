# Knowledge base

Everything a developer or an AI harness needs to understand what this platform is, what the MVP must do, and how the code is meant to be built. Start at the top and stop when you have enough for your task.

| Read this | To learn |
|---|---|
| `01-product/overview.md` | What the application is, who uses it, the phases and the MVP definition of done |
| `01-product/requirements.md` | The MVP build list: every requirement with acceptance checks and code location |
| `01-product/roles-and-access.md` | Roles, permissions, data scopes and how Corp AD maps to them |
| `01-product/open-items.md` | Decisions waiting on NAVEX and the assumption the code makes meanwhile |
| `01-product/glossary.md` | Terms used in the scorecard and in this repository |
| `02-architecture/overview.md` | Components, runtime flows and where each lives in the repository |
| `02-architecture/decisions.md` | Architecture decisions and their reasons |
| `02-architecture/hld.md`, `lld.md` | High and low level design v0.3: data dictionary, endpoints, algorithms |
| `03-engineering/local-setup.md` | Tools, first run, commands |
| `03-engineering/sso-and-aws-access.md` | Corp AD sign-in for the app and AWS SSO for developers |
| `03-engineering/coding-standards.md` | The seven skills and the quality gate |
| `03-engineering/api-contract.md` | Endpoint list with build status |
| `04-delivery/units-of-work.md` | The MVP split into units, each with requirements, paths and a done check |
| `reference/` | Source material the build reads directly: NAVEX feedback, phase scope workbook, the latest prototype. The full FRD and the AWS SSO guide are held outside the repository; what the build needs from them is in this folder and `.harness-records/knowledge/voc-insights/` |

## Keeping it current

- A change to scope or behaviour updates `requirements.md` in the same pull request as the code.
- A NAVEX decision moves its row out of `open-items.md` and updates the requirement's status.
- Files under `reference/` are source documents and are not edited. When a new version arrives, add it beside the old one and update the precedence list in `requirements.md`.
