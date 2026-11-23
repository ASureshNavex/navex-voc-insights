---
name: bug-fix
description: Fixes a defect by reproducing it as a failing test first, finding the cause in the code, fixing it with the least change, then verifying and pruning. Use when something behaves differently from docs/01-product/requirements.md or a test, an error is reported, or asked to fix a bug; use sgivp instead when the fix needs a design choice.
---

# Bug fix

A defect is behaviour that differs from what `docs/01-product/requirements.md`,
a decision record or an existing test says. A wish for new behaviour is not a
defect: that goes through `sgivp` (P1).

1. **State it.** Expected (cite the requirement id, record or test) against
   actual, and how to trigger it. No customer data in the report or the test;
   use synthetic values (N1).
2. **Reproduce it as a failing test** at the lowest level that shows it
   (`test-design`): a module test when one function is wrong, a functionality
   test when the behaviour crosses modules. Name it for the requirement id and
   the defect. See it fail for the stated reason.
3. **Find the cause.** `harness context search` for where it is handled,
   `harness context refs` and `harness context impact` for what else depends
   on it. Fix the cause, not the symptom. When the cause is unclear, or fixing
   it means choosing between behaviours, stop and give the person the
   options; that is now an `sgivp` change.
4. **Fix it** with the least change that makes the test pass. Load the area
   skill from `AGENTS.md`.
5. **Verify:** the gate from `AGENTS.md` "Commands" for each half touched, the
   new test and every existing one passing, then `navex-security-code-review`
   over the diff. A test is never weakened or skipped to pass (N3).
6. **Prune:** anything the fix made unused goes (N10); run the gate again.
7. **Report:** the cause in one line, the test that now guards it, the gate
   output. If the defect came from a wrong assumption in
   `docs/01-product/open-items.md`, hand it to `open-item-settlement`.

## Refuses

- Fixing before a failing test reproduces the defect.
- Changing a test's expectation to match the bug.
- Widening the fix into new behaviour.
