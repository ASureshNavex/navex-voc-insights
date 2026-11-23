from typing import Annotated, Literal

from fastapi import APIRouter, Depends, status

from app.core.entitlements import CurrentUser, require_permission
from app.core.exceptions import NotBuilt
from app.core.pagination import Page, PageParams, page_params
from app.domains.admin.schemas import (
    AccessRow,
    AdminHome,
    AuditEntry,
    LeadershipEmail,
    RefreshRunRow,
    SourceHealth,
    UsageHighlights,
    UsageRow,
    WeeklyChanges,
)

router = APIRouter(prefix="/admin", tags=["admin"])

Paging = Annotated[PageParams, Depends(page_params)]
SourceReader = Annotated[CurrentUser, Depends(require_permission("source_health:read"))]
UsageReader = Annotated[CurrentUser, Depends(require_permission("usage_audit:read"))]


@router.get("/home")
async def get_home(
    user: Annotated[CurrentUser, Depends(require_permission("admin_home:read"))],
) -> AdminHome:
    raise NotBuilt("ADM-01: admin home.")


@router.get("/weekly-changes")
async def get_weekly_changes(
    user: Annotated[CurrentUser, Depends(require_permission("weekly_changes:read"))],
) -> WeeklyChanges:
    raise NotBuilt("ADM-02: new red and repeat red against the previous week.")


@router.post("/weekly-changes/email", status_code=status.HTTP_202_ACCEPTED)
async def email_leadership(
    user: Annotated[CurrentUser, Depends(require_permission("weekly_changes:email"))],
    body: LeadershipEmail,
) -> None:
    raise NotBuilt("ADM-03: email CXM leadership; recipients limited to allowed domains.")


@router.get("/source-health")
async def get_source_health(user: SourceReader) -> list[SourceHealth]:
    raise NotBuilt("ADM-04: data source health.")


@router.post("/source-health/check", status_code=status.HTTP_202_ACCEPTED)
async def run_health_check(
    user: Annotated[CurrentUser, Depends(require_permission("source_health:check"))],
) -> None:
    raise NotBuilt("ADM-04: run the health check on demand.")


@router.get("/refresh-runs")
async def list_refresh_runs(user: SourceReader, page: Paging) -> Page[RefreshRunRow]:
    raise NotBuilt("ADM-05: refresh runs.")


@router.get("/usage/highlights")
async def get_usage_highlights(user: UsageReader) -> UsageHighlights:
    raise NotBuilt("ADM-06: usage highlights.")


@router.get("/usage")
async def get_usage(
    user: UsageReader,
    page: Paging,
    group_by: Literal["person", "team", "segment", "region"] = "person",
) -> Page[UsageRow]:
    raise NotBuilt("ADM-07: usage along the org chart.")


@router.get("/audit")
async def list_audit(user: UsageReader, page: Paging) -> Page[AuditEntry]:
    raise NotBuilt("ADM-08: audit log, newest first.")


@router.get("/access")
async def list_access(
    user: Annotated[CurrentUser, Depends(require_permission("access_list:read"))],
    page: Paging,
) -> Page[AccessRow]:
    raise NotBuilt("ADM-09: read-only access list.")
