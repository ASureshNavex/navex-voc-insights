# ADR 0001: the environments are DEV, QA, Staging and Prod

Status: accepted. Date: 2026-11-19.

## Context
The architecture deck names Dev, UAT and Prod; the cost workbook, `docs/02-architecture/overview.md` and `infra/README.md` name DEV, QA, Staging and Prod (sections/21, conflict 1).

## Decision
The environments are DEV, QA, Staging and Prod, the NAVEX standard shared environments. Dev/UAT/Prod in the deck is superseded; its UAT sizing is read as Staging.

## Consequences
Config, pipelines and docs name these four. Revisit only if NAVEX changes its environment standard.
