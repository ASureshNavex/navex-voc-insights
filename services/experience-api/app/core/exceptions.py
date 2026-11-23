"""Domain errors and their RFC 7807 problem responses. Stack traces never reach the client."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    status_code = 500
    title = "Internal error"

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(detail or self.title)
        self.detail = detail or self.title


class Unauthorized(AppError):
    status_code = 401
    title = "Sign-in required"


class Forbidden(AppError):
    status_code = 403
    title = "Access denied"


class NotFound(AppError):
    status_code = 404
    title = "Not found"


class Conflict(AppError):
    status_code = 409
    title = "Conflict"


class NotBuilt(AppError):
    """The contract is published; the unit of work that implements it is still open."""

    status_code = 501
    title = "Not built yet"


def _problem(status: int, title: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"type": "about:blank", "title": title, "status": status, "detail": detail},
        media_type="application/problem+json",
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return _problem(exc.status_code, exc.title, exc.detail)

    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error", exc_info=exc)
        return _problem(500, AppError.title, "The request could not be completed.")
