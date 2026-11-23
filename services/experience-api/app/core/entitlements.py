"""Role, permission and data-scope resolution. Policy is in docs/01-product/roles-and-access.md."""

from collections.abc import Awaitable, Callable
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from voc_data.enums import DataScope, Ownership, Role
from voc_data.scope import AccessScope

from app.core.config import RoleMapping, Settings, get_settings
from app.core.exceptions import Forbidden
from app.core.security import TokenClaims, get_token_claims

_SHARED = {"notifications:read"}
_SCORECARD = {
    "scorecard:read",
    "scorecard:export",
    "saved_views:manage",
    "digest_preferences:manage",
}

PERMISSIONS: dict[Role, frozenset[str]] = {
    Role.CXM: frozenset(_SHARED | _SCORECARD | {"account_brief:generate"}),
    Role.CXM_LEADERSHIP: frozenset(
        _SHARED
        | _SCORECARD
        | {
            "scorecard:filter_team",
            "scorecard:trend",
            "manager_summary:read",
            "custom_reports:manage",
        }
    ),
    Role.VOC_ADMIN: frozenset(
        _SHARED
        | {
            "admin_home:read",
            "weekly_changes:read",
            "weekly_changes:email",
            "knowledge_hub:upload",
            "knowledge_hub:approve",
            "source_health:read",
            "source_health:check",
            "usage_audit:read",
            "digests:manage",
            "access_list:read",
        }
    ),
    # Modules for these roles are still to be decided with NAVEX.
    Role.ELT: frozenset(),
    Role.ACCOUNT_EXECUTIVE: frozenset(),
}


class CurrentUser(BaseModel):
    model_config = ConfigDict(frozen=True)

    upn: str
    name: str
    role: Role
    data_scope: DataScope
    permissions: frozenset[str]

    @property
    def access_scope(self) -> AccessScope:
        ownership = (
            Ownership.ACCOUNT_EXECUTIVE if self.role is Role.ACCOUNT_EXECUTIVE else Ownership.CXM
        )
        return AccessScope(upn=self.upn, data_scope=self.data_scope, ownership=ownership)

    def can(self, permission: str) -> bool:
        return permission in self.permissions


def resolve_user(claims: TokenClaims, role_map: dict[str, RoleMapping]) -> CurrentUser:
    mapping = next(
        (role_map[value] for value in (*claims.roles, *claims.groups) if value in role_map),
        None,
    )
    if mapping is None:
        raise Forbidden("Your account is not assigned to a VoC Insights role.")
    return CurrentUser(
        upn=claims.upn.lower(),
        name=claims.name,
        role=mapping.role,
        data_scope=mapping.scope,
        permissions=PERMISSIONS[mapping.role],
    )


async def get_current_user(
    claims: Annotated[TokenClaims, Depends(get_token_claims)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> CurrentUser:
    return resolve_user(claims, settings.voc_role_map)


def require_permission(permission: str) -> Callable[[CurrentUser], Awaitable[CurrentUser]]:
    async def guard(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if not user.can(permission):
            raise Forbidden("Your role does not include this action.")
        return user

    return guard
