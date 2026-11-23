# Building an endpoint from a "Contract only" row

Read with this skill, and by `sgivp`, when an endpoint moves from "Contract
only" to "Built" in `docs/03-engineering/api-contract.md`.

- The route, permission guard and schemas already exist; the handler returns
  `501` naming its requirement (`app/core/exceptions.py`). Replace that line;
  do not add a second route.
- The service function takes `CurrentUser` and applies `scope_filter`, as
  `app/domains/accounts/service.py` does. An account outside scope is `404`
  (P2).
- Lists take a `limit` with a cap and a stable order (P10). SQL is
  parameterized.
- A response field an open item blocks returns what that item's assumption
  says, from the one place it names.
- When the response shape departs from the prototype handover, raise it as an
  option in `sgivp`; the conflicts are listed in
  `.harness-records/knowledge/voc-insights/sections/33-react-handover.md`.

Tests, at least: outside scope is `404`; the wrong permission is refused;
`limit` above the cap is refused; the order is stable across pages; plus each
"Done when" check of the requirement (`test-design`).

Done when those pass, the row in `api-contract.md` says Built, and the service
README names the endpoint.
