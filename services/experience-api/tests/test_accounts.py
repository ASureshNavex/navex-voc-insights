from voc_data.enums import DataScope, Role

from tests.conftest import CXM_ONE, LEAD, make_user

CXM = make_user(CXM_ONE, Role.CXM, DataScope.OWN_BOOK)
LEADER = make_user(LEAD, Role.CXM_LEADERSHIP, DataScope.TEAM)
ADMIN = make_user("admin@navex.com", Role.VOC_ADMIN, DataScope.ALL)


async def test_cxm_lists_only_their_own_accounts(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(CXM)
    body = (await client.get("/accounts")).json()
    assert body["total"] == 2
    assert {row["sfdc_account_id"] for row in body["items"]} == {"001A", "001B"}


async def test_default_sort_puts_red_with_churn_language_first(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(LEADER)
    ids = [row["sfdc_account_id"] for row in (await client.get("/accounts")).json()["items"]]
    assert ids == ["001A", "001C", "001B", "001D"]


async def test_rows_carry_themes_verbatim_and_status_tag(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(CXM)
    row = (await client.get("/accounts", params={"status": "R"})).json()["items"][0]
    assert row["status_tag"] == "new_red"
    assert row["themes"][0]["name"] == "Report accuracy"
    assert row["top_verbatim"]["source"] == "Support case"


async def test_account_outside_scope_is_not_found(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(CXM)
    assert (await client.get("/accounts/001C")).status_code == 404
    assert (await client.get("/accounts/001A")).status_code == 200


async def test_cxm_filter_cannot_widen_scope(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(CXM)
    body = (await client.get("/accounts", params={"cxm": "cxm2@navex.com"})).json()
    assert body["total"] == 0


async def test_page_size_is_capped(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(LEADER)
    assert (await client.get("/accounts", params={"limit": 201})).status_code == 422
    page = (await client.get("/accounts", params={"limit": 1, "offset": 1})).json()
    assert [row["sfdc_account_id"] for row in page["items"]] == ["001C"]


async def test_role_without_permission_is_forbidden(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(ADMIN)
    response = await client.get("/accounts")
    assert response.status_code == 403
    assert response.headers["content-type"] == "application/problem+json"


async def test_summary_counts_follow_scope(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(CXM)
    summary = (await client.get("/portfolio/summary")).json()
    assert summary["red"]["count"] == 1
    assert summary["red"]["new_this_week"][0]["sfdc_account_id"] == "001A"
    assert summary["yellow"]["count"] == 1
    assert summary["yellow"]["new_this_week"] == []


async def test_saved_view_names_are_unique_per_user(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(CXM)
    body = {"name": "Red only", "filters": {"status": ["R"]}}
    assert (await client.post("/saved-views", json=body)).status_code == 201
    assert (await client.post("/saved-views", json=body)).status_code == 409
    assert len((await client.get("/saved-views")).json()) == 1


async def test_entitlements_report_role_scope_and_size(client_for) -> None:  # type: ignore[no-untyped-def]
    client = await client_for(LEADER)
    body = (await client.get("/me/entitlements")).json()
    assert body["role"] == "CXM_LEADERSHIP"
    assert body["data_scope"] == "TEAM"
    assert body["scope_size"] == 4
    assert "manager_summary:read" in body["permissions"]
