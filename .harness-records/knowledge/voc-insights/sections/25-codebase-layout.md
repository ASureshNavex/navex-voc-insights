# Codebase layout

Sources: `navex-voc-platform-scaffold.zip` (scaffold, 3 Nov 2026: `README.md`, `STRUCTURE.md`, `infra/`, `option-a-python/`, `frontend/`); `NAVEX VoC - Technical Architecture and Sizing.pptx` (Arch deck slide 5); skeleton repository top level, `AGENTS.md`, `.github/workflows/ci.yml`.

## Already in docs/ (read there, not here)

- Skeleton tree and what each folder holds: `docs/02-architecture/overview.md` "Repository layout".
- Module boundaries (features, `ports/`, `adapters/`, `tools/`, `.j2` prompts, schema owner): `overview.md` "Module boundaries".
- Monorepo, uv workspace, shared `packages/voc-data`: `docs/02-architecture/decisions.md` 1-2.
- Skill per code area and rules never broken: `AGENTS.md`. Quality gate commands: `docs/03-engineering/coding-standards.md` "Quality gate".
- Tech stack (React 19, TS 5, Vite, FastAPI, Pydantic v2, SQLAlchemy, Alembic, LangGraph, uv, Ruff, mypy, pytest, pip-audit, Trivy): Arch deck slide 5 matches `overview.md` "Components" and `ci.yml`.

## Scaffold layout (older reference)

| Path | Holds |
|---|---|
| `aidlc/` | Methodology workspace only, six "spaces" (platform-core, data-sources, intelligence, experience, workers, knowledge), each with intents and unit lists U01-U22 |
| `option-a-python/backend/` | One Python package `src/voc/` with `domain/` (incl. `scoring/`), `application/` (`ports/`, `security/`, `usecases/`), `adapters/` (classification, distribution, entitlement, feedback_data, inference, knowledge, live_data), `api/` (`routers/`, `security/`), `composition/` (DI container), `observability/`, `worker/`; `config/` (`ports.yaml`, `security.yaml`, `rules/`); `tests/` (`unit`, `contract`, `evaluation`); `.importlinter` |
| `option-b-dotnet/backend/` | .NET 8 alternative with the same contract; "delete the one not chosen" |
| `frontend/src/` | `api/`, `auth/` (AuthProvider, NotOnboarded, signOut), `charts/`, `features/accounts/`, `observability/`, `shared/` |
| `infra/` | `otel/collector-config.yaml` (strips verbatim text and SQL before export), `pipelines/ci.yaml`; README also names `pipelines/cd.yaml` and `environments/`, which are not in the zip |
| Root docs | `STRUCTURE.md`, `TREE.md`, `SSO.md`, `PLATFORM-SWAP.md`, `VOC-PRACTICES.md` |

Scaffold layer rules (enforced by import linting): domain imports only domain; application imports domain and declares ports; adapters import application and domain, nothing imports adapters; api never imports adapters; only composition names a concrete adapter.

## Scaffold versus skeleton

| Aspect | Scaffold | Skeleton (as of 19 Nov 2026) | Match |
|---|---|---|---|
| Backend language | Python or .NET, choose one | Python 3.13 only | Choice made |
| Backend shape | One package, layered by domain/application/adapters/api | Four deployable services under `services/` (`experience-api`, `ingestion`, `account-scoring-agent`, `notifications`) plus shared `packages/voc-data`; uv workspace members `packages/*`, `services/*` | Differs |
| Web app | `frontend/` | `apps/web/` (Vite, Tailwind, shadcn `components.json`, PostCSS) | Same role, renamed |
| Agent | `worker/` run control; inference behind a port | Dedicated LangGraph service for AgentCore Runtime | Differs |
| Vendor isolation | `adapters/<port>/<vendor>/` and DI composition root | `ports/` (API), `adapters/` (ingestion), `tools/` (agent) per service | Same idea, lighter form |
| Infra | OTel collector config, CI and CD pipelines, per-env settings | `infra/README.md` only: an environment contract; NAVEX IT provisions | Differs |
| CI | `infra/pipelines/ci.yaml`: ruff + mypy, `lint-imports`, unit, port contract tests, evaluation gate with thresholds; web lint/test/build | `.github/workflows/ci.yml`: python (ruff check and format, mypy, pytest, pip-audit), web (typecheck, lint, test, build, `npm audit` high), images (docker build of 4 services, Trivy CRITICAL) | Partly: no import-lint, contract or evaluation gate in skeleton; skeleton adds format, audits, image scan |
| Method folder | `aidlc/` | None; `docs/` knowledge base and `.claude/skills/`; `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` | Differs |
| Local DB | Not present | `docker-compose.yml` with PostgreSQL 16 | Skeleton only |
| Other root | | `.editorconfig`, `.gitattributes` (LF), `.python-version` 3.13, `.vscode`, `scripts/aws-config.example`, `uv.lock` | Skeleton only |

## Conflicts with docs/

| # | Topic | Sources | docs/ |
|---|---|---|---|
| 1 | Infrastructure as code | Arch deck slide 5 "Delivery: Infrastructure as code"; scaffold `infra/` has pipelines and environments | `infra/README.md`: "This repository holds no infrastructure code" |
| 2 | Root folder name | Scaffold `navex-voc-platform-scaffold/` | `overview.md` tree root is `navex-voc-platform/`; the repository is `navex-voc-insights` |
| 3 | Evaluation gate | Scaffold CI has an evaluation gate (U10 evaluation-service); Roadmap png lists Evaluation in MVP | Definition of done gate lists ruff, mypy, pytest, tsc, eslint, vitest, build (`units-of-work.md`); no evaluation step |
| 4 | Deploy pipeline | Scaffold names `pipelines/cd.yaml` (deploy, smoke test, rollback) | Deploy workflow is unit OPS-01, Blocked on NAVEX IT (`units-of-work.md`) |
| 5 | Notification image | HLD 6 and deck slide 7: same image as the refresh task | Own Dockerfile and CI image matrix entry (`infra/README.md`, `ci.yml`) |

## Open questions

- Will import-boundary linting (scaffold `lint-imports`) or port contract tests be added to the skeleton gate?
- Where IaC for VoC resources lives, if anywhere (NAVEX IT repository or none).
- Whether an OpenTelemetry collector (with the verbatim and SQL scrubbing the scaffold relies on) sits between services and Dynatrace.
