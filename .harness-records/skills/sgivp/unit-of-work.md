# A unit from units-of-work.md through SGIVP

Read by `sgivp` when the intent is a unit id such as `API-03` or `WEB-05`.

- Refuse a unit whose status is **Blocked**; name the input it waits on.
- Search starts at the unit row in `docs/04-delivery/units-of-work.md`: its
  requirement ids, its code paths, its status. Then each requirement row in
  `docs/01-product/requirements.md`, with its "Done when" checks, and the
  matching screen in `docs/reference/prototype/voc-insights-workspace-latest.html`.
- The plan's test list is the unit's "Done when" checks, one or more tests
  each, from `test-design`.
- The unit's definition of done in `units-of-work.md` is the Verify step's
  checklist: tests per check, the gate, no security blocker, prototype copy,
  README and `api-contract.md` updated.
- On finishing, set the unit's status in `units-of-work.md` and the
  requirement's status in `requirements.md` in the same change.
- Draft the pull request body to `.github/pull_request_template.md`. Do not
  push (N9).
