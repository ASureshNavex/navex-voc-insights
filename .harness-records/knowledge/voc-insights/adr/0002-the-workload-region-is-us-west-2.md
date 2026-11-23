# ADR 0002: the workload region is us-west-2

Status: accepted. Date: 2026-11-19.

## Context
The deck and the cost workbook price in us-east-1; `docs/` and `.env` assume us-west-2 (`docs/01-product/open-items.md` item 13; sections/21, conflict 2).

## Decision
The platform runs in us-west-2.

## Consequences
The cost figures (ADR 0003) are us-east-1 list prices and are read as estimates for us-west-2. Snowflake connectivity must be confirmed for us-west-2.
