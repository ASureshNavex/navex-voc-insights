---
name: open-item-settlement
description: Settles an open item or a conflict between docs/ and the knowledge base, changing the assumption in its one place, updating docs and recording the decision. Use when NAVEX answers a question in docs/01-product/open-items.md, when the person settles a conflict listed in .harness-records/knowledge/voc-insights/, or when sgivp's Ground step finds two sources that disagree.
---

# Settling an open item or a conflict

An open item is built to its stated assumption in one place. A settlement
replaces that assumption with the answer, everywhere it shows, once.

1. **The answer has a source.** Who answered and where (a meeting, a message,
   a document). No source, no settlement: keep the item open (N8).
2. **Find every place.** The row in `docs/01-product/open-items.md` names where
   the assumption lives. Confirm with `harness context search` that no second
   copy exists.
3. **Change it in that one place,** with a test that proves the new behaviour
   (`test-design`).
4. **Update `docs/`,** which wins for what to build: the requirement row and its
   status, and any architecture or engineering page the answer changes.
5. **Record the decision** under `.harness-records/knowledge/voc-insights/adr/`,
   numbered after the highest there, at most 250 words: the decision as the
   title, then Context, Decision, Consequences, with the answer's source in
   Context.
6. **Clear the trail:** remove the open-items row, mark the conflict
   **Resolved** in the knowledge section that lists it, pointing at the record,
   and add the record to the "Decisions settled" table in `SPEC.md`.
7. **Verify:** the gate passes, and a search finds no trace of the old
   assumption.

## Refuses

- Picking a side with no recorded answer.
- Editing an accepted decision record; a new record supersedes it.
- Leaving the old assumption anywhere after the change.
