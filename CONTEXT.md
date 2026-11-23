# CONTEXT.md

Handoff between sessions: only what the next task cannot derive. Prune an
entry once its task is done.

## 2026-11-19: harness installed, knowledge built, layers removed by hand

- The harness is installed for Claude Code only, with no git (so no git
  hooks), from a build of the harness repository's main. Telemetry is off and
  no measurement service is configured; Jira is cleared; VCS is GitHub with
  organization and project still empty.
- The upstream Navex layer and the harness's shipped skills were removed from
  `.claude` by hand, on purpose. `harness init --install` puts them back: after
  any reinstall, remove them again (keep the 7 skills in
  `.harness/imported/claude-code-2026-11-19/config/skills`, `harness-commands`
  and the `harness-context` server; no hooks at all, telemetry hooks included)
  and restore the edited lines in `.harness/HARNESS.md`. The payload behind
  them is gone from `.harness` too (`upstream/`, `skills/`, `agents/`,
  `evals/`, `config.default.toml`), and `.harness/MANIFEST.toml` was rewritten
  to the five files left, so doctor's hashes check still means something. A
  reinstall brings all of it back, and `harness skills` and `harness eval`
  have nothing to work on here.
- Doctor fails three rows because of that, all expected: `mms` (no url,
  telemetry is off), `hooks` (the telemetry hooks were removed on purpose) and
  `addenda` (the team skills carry no Navex addendum).
- The project's rules are P1 to P13 in `.harness/project-constitution.md`.
- Knowledge: `.harness-records/knowledge/voc-insights/SPEC.md`. Four decisions
  settled 2026-11-19 are under its `adr/`. Still open: the rating model (rules
  and four ratings in the sources, a 0-100 score in `docs/`), the account join
  key, and Snowflake Cortex versus Bedrock AgentCore.
- `docs/` was pruned: the duplicate MVP requirements file, the full FRD copy
  and the SSO PDF are gone; references now name the originals as held outside
  the repository.
- This repository's own workflow skills are built: `sgivp` (person-started;
  stops at the options and the plan), `test-design` (module and functionality
  level, coverage by requirement id) and `open-item-settlement`. Reference
  files: `sgivp/unit-of-work.md`, `sgivp/rule-set-change.md`,
  `navex-fastapi-rest-apis/building-an-endpoint.md`,
  `navex-agentcore-runtime/explanations.md`. `react-dashboard-rbac-sso` was
  merged into `navex-voc-frontend-architecture`, and both web skills now say
  top bar, not sidebar (open item 14). Decided: Claude Code only, no hooks, no
  browser end-to-end tests yet, prune with existing linters plus
  `harness context refs`, synthetic test fixtures, rule-set versions need no
  person sign-off. Also built, replacing the useful parts of the removed
  skills: `bug-fix`, `pr-ready`, `release-check`, `knowledge-refresh`,
  `session-handoff`. Every skill's body, with its reference files, is in
  `.harness-records/skills/<name>/`; `.claude/skills/<name>/SKILL.md` is a
  pointer only (front matter plus one line). A reinstall would put the
  original 7 team skills back into `.claude/skills` as full copies from the
  restore point: delete those copies and keep the pointers. The Jira and
  grooming skills were not replaced: scope
  lives in `requirements.md` and `units-of-work.md`. None of these has been
  tried on a real change: run `/sgivp` on one Open unit first and adjust.
