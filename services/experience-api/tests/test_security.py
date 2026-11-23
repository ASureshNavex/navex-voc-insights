from datetime import UTC, datetime, timedelta

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from voc_data.enums import DataScope, Role

from app.core.config import RoleMapping
from app.core.entitlements import resolve_user
from app.core.exceptions import Forbidden, Unauthorized
from app.core.security import TokenClaims, TokenVerifier

ISSUER = "https://login.microsoftonline.com/tenant/v2.0"
AUDIENCE = "api-client-id"
KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
VERIFIER = TokenVerifier(ISSUER, [AUDIENCE], lambda _: KEY.public_key())
ROLE_MAP = {"VoC.CXM": RoleMapping(role=Role.CXM, scope=DataScope.OWN_BOOK)}


def _token(**overrides: object) -> str:
    claims = {
        "iss": ISSUER,
        "aud": AUDIENCE,
        "exp": datetime.now(UTC) + timedelta(minutes=5),
        "preferred_username": "Lindsay@navex.com",
        "name": "Lindsay",
        "roles": ["VoC.CXM"],
        **overrides,
    }
    return jwt.encode(claims, KEY, algorithm="RS256")


def test_valid_token_yields_claims() -> None:
    claims = VERIFIER.verify(_token())
    assert claims.upn == "Lindsay@navex.com"
    assert claims.roles == ["VoC.CXM"]


@pytest.mark.parametrize(
    "overrides",
    [
        {"aud": "another-api"},
        {"iss": "https://login.microsoftonline.com/other/v2.0"},
        {"exp": datetime.now(UTC) - timedelta(minutes=1)},
    ],
)
def test_wrong_audience_issuer_or_expiry_is_rejected(overrides: dict[str, object]) -> None:
    with pytest.raises(Unauthorized):
        VERIFIER.verify(_token(**overrides))


def test_token_signed_by_another_key_is_rejected() -> None:
    other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    forged = jwt.encode(
        {"iss": ISSUER, "aud": AUDIENCE, "exp": datetime.now(UTC) + timedelta(minutes=5)},
        other,
        algorithm="RS256",
    )
    with pytest.raises(Unauthorized):
        VERIFIER.verify(forged)


def test_mapped_role_resolves_with_lowercase_upn() -> None:
    user = resolve_user(VERIFIER.verify(_token()), ROLE_MAP)
    assert (user.upn, user.role, user.data_scope) == ("lindsay@navex.com", Role.CXM, "OWN_BOOK")
    assert user.can("scorecard:read")


def test_user_without_a_mapped_role_is_forbidden() -> None:
    claims = TokenClaims(preferred_username="x@navex.com", roles=["Something.Else"])
    with pytest.raises(Forbidden):
        resolve_user(claims, ROLE_MAP)
