"""Corp AD (Microsoft Entra ID) access token verification."""

import asyncio
from collections.abc import Callable
from functools import lru_cache
from typing import Annotated, Any

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings
from app.core.exceptions import Unauthorized

KeyResolver = Callable[[str], Any]

_bearer = HTTPBearer(auto_error=False)


class TokenClaims(BaseModel):
    upn: str = Field(alias="preferred_username")
    name: str = ""
    roles: list[str] = []
    groups: list[str] = []


class TokenVerifier:
    def __init__(self, issuer: str, audiences: list[str], resolve_key: KeyResolver) -> None:
        self._issuer = issuer
        self._audiences = audiences
        self._resolve_key = resolve_key

    def verify(self, token: str) -> TokenClaims:
        try:
            payload = jwt.decode(
                token,
                self._resolve_key(token),
                algorithms=["RS256"],
                audience=self._audiences,
                issuer=self._issuer,
                options={"require": ["exp", "iss", "aud"]},
            )
            return TokenClaims.model_validate(payload)
        except (jwt.PyJWTError, ValueError) as exc:
            raise Unauthorized("The access token is not valid.") from exc


@lru_cache
def _entra_verifier(tenant_id: str, audience: str) -> TokenVerifier:
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    # PyJWKClient caches the signing keys in this process and refetches on an unknown key ID.
    jwks = jwt.PyJWKClient(f"{authority}/discovery/v2.0/keys", cache_keys=True, timeout=5)
    return TokenVerifier(
        issuer=f"{authority}/v2.0",
        audiences=[audience, f"api://{audience}"],
        resolve_key=lambda token: jwks.get_signing_key_from_jwt(token).key,
    )


def get_token_verifier(settings: Annotated[Settings, Depends(get_settings)]) -> TokenVerifier:
    return _entra_verifier(settings.entra_tenant_id, settings.entra_api_audience)


async def get_token_claims(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    verifier: Annotated[TokenVerifier, Depends(get_token_verifier)],
) -> TokenClaims:
    if credentials is None:
        raise Unauthorized()
    # Key lookup can make a blocking HTTPS call the first time a key ID is seen.
    return await asyncio.to_thread(verifier.verify, credentials.credentials)
