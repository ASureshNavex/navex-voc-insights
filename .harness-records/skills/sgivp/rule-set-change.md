# Changing a rating rule or threshold through SGIVP

Read by `sgivp` when the intent changes how an account is rated. Ratings come
from code and the versioned rule set; a model writes explanations only (P9).

Where things are:

- Rule files: `services/account-scoring-agent/src/account_scoring_agent/rules/`
  (today `placeholder-v0.yaml`).
- The rules applied: `services/account-scoring-agent/src/account_scoring_agent/domain/scoring.py`.
- The rules as the sources define them, with exact thresholds:
  `.harness-records/knowledge/voc-insights/sections/11-rygg-account-scoring.md`
  and `10a-product-domain-scoring.md`. The rating model is an open conflict
  there (rules and four ratings against a 0-100 score in `docs/`); settle it
  with `open-item-settlement` before the first real rule set.

Steps:

- Name the source of every value: who supplied it and in which document. A
  threshold with no source is not written (N8).
- Add a new versioned file. An issued version is never edited; a test fails if
  its bytes change.
- Extend the expected-ratings table for the new version: account inputs, the
  rating, the rules that fired. Every earlier version's table still passes.
- Record the version on each rating the code produces.
- No person sign-off is needed for the new version or its expected ratings;
  the tests are the proof.

Done when: pytest passes for every version's table, the issued-file test
passes, and no model call sits in the rating path.
