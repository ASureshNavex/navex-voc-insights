from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_session
from app.core.exceptions import register_exception_handlers
from app.core.telemetry import configure_telemetry
from app.domains.accounts.router import router as accounts_router
from app.domains.admin.router import router as admin_router
from app.domains.digests.router import router as digests_router
from app.domains.knowledge_hub.router import router as knowledge_hub_router
from app.domains.leadership.router import router as leadership_router
from app.domains.me.router import router as me_router
from app.domains.notifications.router import router as notifications_router
from app.domains.portfolio.router import router as portfolio_router
from app.domains.saved_views.router import router as saved_views_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="VoC Insights Workspace Experience API", version="0.1.0")
    configure_telemetry(app, settings)
    register_exception_handlers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    v1 = APIRouter(prefix="/api/v1")
    for router in (
        me_router,
        portfolio_router,
        accounts_router,
        saved_views_router,
        notifications_router,
        leadership_router,
        knowledge_hub_router,
        digests_router,
        admin_router,
    ):
        v1.include_router(router)
    app.include_router(v1)

    @app.get("/health", include_in_schema=False)
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready", include_in_schema=False)
    async def ready(session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, str]:
        await session.execute(text("SELECT 1"))
        return {"status": "ready"}

    return app


app = create_app()
