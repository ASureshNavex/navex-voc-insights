---
name: test-design
description: Designs and verifies tests at two levels, module and functionality, and reports which requirement checks have a passing test. Use when planning or writing tests, when a plan needs its test list, when asked whether a change is covered, or when adding code under services/*/tests, packages/*/tests or apps/web/src.
---

# Test design: module and functionality level

Every test exists to prove one thing a reader can name. Two levels, and every
change gets both where both apply.

## Module level: does this unit of code keep its own contract

One test file per module, beside the existing ones:

| Code | Test with | Where |
| --- | --- | --- |
| API domain (`app/domains/<x>/service.py`, router) | pytest, FastAPI `TestClient` | `services/experience-api/tests/test_<x>.py` |
| Agent domain, graph, prompt | pytest | `services/account-scoring-agent/tests/test_domain.py`, `test_graphs.py`, `test_prompts.py` |
| Ingestion, notifications, data package | pytest | that package's `tests/` |
| Web feature or shared component | vitest with Testing Library | beside the file, `<Name>.test.tsx` |

For each module, test: the normal case; each boundary the code states (caps,
empty input, the last page, a threshold's edge); each error path it promises
(the exception or status it raises); and nothing about another module's
internals. Use fakes at the ports, never the network or a real model.

## Functionality level: does the product do what the requirement says

Source: the "Done when" checks of each requirement row in
`docs/01-product/requirements.md` that the change touches.

- One or more tests per check. The test name carries the requirement id and
  says the check in words, for example
  `test_acc_02_account_outside_scope_is_404` or
  `it("SCR-04 hides export without scorecard:export")`.
- An API check is tested through the HTTP surface with `TestClient`, as a user
  of the stated role: scope (P2), permission, paging cap and stable order
  (P10).
- A screen check is tested at component level with Testing Library: what the
  role sees, the empty, loading and denied states, labels from the prototype
  (P12), permission through `<Can>` or `usePermission` (P3).
- A rating check is tested against the expected-ratings table of the rule set
  version in force (P9).
- A check no automated test can prove is written as a demo step in the plan,
  and says why.

No browser end-to-end tests yet: functionality is proven at the API and
component levels.

## Verify: the coverage report

After the gate passes, report a table for the change:

| Requirement | "Done when" check | Test (file and name) or demo step | Result |
| --- | --- | --- | --- |

A check with no row is a gap and the change is not done. A test is never
skipped, weakened or retried until it passes; a quarantined test is named
with its reason (N3).

## Refuses

- A test that asserts nothing a reader can name, or only that code ran.
- Real customer text, account names or credentials in fixtures; fixtures are
  synthetic (N1).
- A model call in a test; use a fake.
