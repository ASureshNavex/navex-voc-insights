from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.entitlements import CurrentUser, require_permission
from app.core.exceptions import NotBuilt
from app.core.pagination import Page, PageParams, page_params
from app.domains.leadership.schemas import FrictionReportRow, ManagerSummary, ReportTemplate

router = APIRouter(prefix="/leadership", tags=["leadership"])

Reporter = Annotated[CurrentUser, Depends(require_permission("custom_reports:manage"))]
Paging = Annotated[PageParams, Depends(page_params)]


@router.get("/summary")
async def get_manager_summary(
    user: Annotated[CurrentUser, Depends(require_permission("manager_summary:read"))],
) -> ManagerSummary:
    raise NotBuilt("LDR-01 to LDR-03: manager summary and team performance.")


@router.get("/report-templates")
async def list_report_templates(user: Reporter, page: Paging) -> Page[ReportTemplate]:
    raise NotBuilt("LDR-04: custom report templates.")


@router.post("/report-templates/{template_id}/run")
async def run_report_template(
    template_id: UUID, user: Reporter, page: Paging
) -> Page[FrictionReportRow]:
    raise NotBuilt("LDR-04: run a custom report template.")


@router.get("/friction-report")
async def get_friction_report(user: Reporter, page: Paging) -> Page[FrictionReportRow]:
    raise NotBuilt("LDR-05: weekly friction report.")
