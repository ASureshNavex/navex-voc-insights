from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.entitlements import CurrentUser, require_permission
from app.core.exceptions import NotBuilt
from app.core.pagination import Page, PageParams, page_params
from app.domains.accounts import service
from app.domains.accounts.schemas import AccountBrief, AccountDetail, AccountFilters, AccountRow

router = APIRouter(prefix="/accounts", tags=["accounts"])

Reader = Annotated[CurrentUser, Depends(require_permission("scorecard:read"))]
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("")
async def list_accounts(
    user: Reader,
    session: Session,
    filters: Annotated[AccountFilters, Query()],
    page: Annotated[PageParams, Depends(page_params)],
) -> Page[AccountRow]:
    return await service.list_accounts(session, user, filters, page)


@router.get("/export.xlsx", response_class=Response)
async def export_accounts(
    user: Annotated[CurrentUser, Depends(require_permission("scorecard:export"))],
    filters: Annotated[AccountFilters, Query()],
) -> Response:
    raise NotBuilt("EXP-01: Excel download of the filtered scorecard.")


@router.get("/{sfdc_account_id}")
async def get_account(sfdc_account_id: str, user: Reader, session: Session) -> AccountDetail:
    return await service.get_account(session, user, sfdc_account_id)


@router.get("/{sfdc_account_id}/brief")
async def get_account_brief(
    sfdc_account_id: str,
    user: Annotated[CurrentUser, Depends(require_permission("account_brief:generate"))],
) -> AccountBrief:
    raise NotBuilt("ACC-13: account brief from the published run.")
