---
name: pr-ready
description: Gets a branch ready for a pull request - what the change reaches, which tests prove it, the security review, and the PR body drafted to .github/pull_request_template.md with its requirement ids. Never pushes. Use when a change is finished and about to be committed or opened as a pull request, or when asked to review a diff before it goes out.
---

# Ready for a pull request

1. **What changed and what it reaches.** List the changed files. For each
   changed module, `harness context impact <path>` names its dependents; a
   dependent in another service or in `apps/web` is listed as a risk.
2. **Which tests prove it.** The tests that cover the changed modules and
   their dependents, found with `harness context refs`, plus every
   functionality test named for a requirement id the change touches
   (`test-design`). Run those first for fast feedback, then the full gate
   from `AGENTS.md` "Commands", which is what CI runs (`ruff`, `ruff format`,
   `mypy`, `pytest`, `pip-audit`; `typecheck`, `lint`, `test`, `build`,
   `npm audit`).
3. **Security review:** `navex-security-code-review` over the diff. A blocker
   stops here.
4. **Scope:** every behaviour change maps to a row in
   `docs/01-product/requirements.md` (P1); docs changed in the same change
   (requirement status, `api-contract.md`, unit status, README).
5. **Draft the PR body** to `.github/pull_request_template.md`: the requirement
   ids and names, what changed in a few lines, and the checklist ticked only
   for what was actually run, with the result. Show it to the person; do not
   open the pull request or push unless asked (N2, N9).

## Refuses

- Ticking a checklist item that was not run.
- A pull request whose change maps to no requirement, without saying so.
- Pushing or opening the pull request on its own.
