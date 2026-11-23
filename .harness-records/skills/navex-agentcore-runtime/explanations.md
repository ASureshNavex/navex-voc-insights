# Changing a prompt or an explanation

Read with this skill, and by `sgivp`, when a `.j2` template, its context model
or the text a model writes about a rating changes. The rating itself never
comes from the model (P9).

- Templates live in `services/account-scoring-agent/src/account_scoring_agent/prompts/`.
  Change the `.j2` file and its typed context model together; keep the render
  test in `tests/test_prompts.py` passing. Customer text stays delimited data
  (P8).
- Keep a small frozen set of synthetic inputs (an account's facts, its coded
  rating, its triggers, its verbatim ids), never real customer text (N1).
- Deterministic checks on every output, with a fake model in CI:
  - every cited verbatim id is one of the ids supplied;
  - the rating word in the text matches the coded rating;
  - the length is within its cap;
  - no em dashes, emojis or decorative symbols (P12).
- When Bedrock is reachable, run the same inputs through the real model and
  put the old and new outputs side by side in the plan, for the person to read
  before the change lands.

Done when the render test and the deterministic checks pass.
