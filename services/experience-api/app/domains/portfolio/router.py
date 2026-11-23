from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.entitlements import CurrentUser, require_permission
from app.core.exceptions import NotBuilt
from app.domains.portfolio import service
from app.domains.portfolio.schemas import PortfolioSummary, PortfolioTrend

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/summary")
async def get_summary(
    user: Annotated[CurrentUser, Depends(require_permission("scorecard:read"))],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PortfolioSummary:
    return await service.get_summary(session, user)


@router.get("/trend")
async def get_trend(
    user: Annotated[CurrentUser, Depends(require_permission("scorecard:trend"))],
    weeks: Annotated[int, Query(ge=2, le=12)] = 2,
) -> PortfolioTrend:
    raise NotBuilt("SCR-07: week-over-week share from weekly snapshots.")
