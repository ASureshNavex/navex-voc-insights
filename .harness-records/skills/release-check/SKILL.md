---
name: release-check
description: Checks readiness to release the MVP or a later phase and reports each check as pass, fail or unknown with the evidence for it - units of work, requirement coverage, the CI gate, blocking open items, security findings and current docs. Changes nothing. Use before a go-live or phase review, or when asked whether the product is ready to release.
---

# Release check

Reports; never fixes. Each row ends pass, fail or unknown, with the command
or file that shows it. Unknown is never reported as pass.

| Check | Pass when | Evidence |
| --- | --- | --- |
| Units | Every unit in scope for the release in `docs/04-delivery/units-of-work.md` is Done | the unit table; list any Open or Blocked |
| Requirements | Every requirement in scope in `docs/01-product/requirements.md` is built, each "Done when" check has a passing test or recorded demo step | the `test-design` coverage report |
| Gate | The full gate from `AGENTS.md` "Commands" passes on the release commit, plus `pip-audit` and `npm audit --audit-level=high` | the command output |
| Images | Each service's Docker image builds | `docker build` per service, as CI does |
| Open items | No row in `docs/01-product/open-items.md` blocks a requirement in scope; any still open runs on its stated assumption | the open-items table |
| Conflicts | No unresolved conflict in `.harness-records/knowledge/voc-insights/SPEC.md` touches a requirement in scope | the SPEC conflict list |
| Security | `navex-security-code-review` over the release diff has no blocker | the review |
| Docs | `requirements.md` statuses, `api-contract.md` build status and each service README match the code | a spot check per service |
| Environments | DEV, QA, Staging and Prod as `adr/0001` sets, in us-west-2 (`adr/0002`) | `infra/README.md`, the deploy configuration |

The MVP go-live is 8 December 2026 (`AGENTS.md`). The release scope is the
milestone's units in `units-of-work.md`; ask the person when it is not clear.

End with one line: ready, or not ready with the failing and unknown rows.
Release notes, when asked, are drafted from the requirement ids the release
completed, in the prototype's wording, and shown before anything is sent
(N2).
