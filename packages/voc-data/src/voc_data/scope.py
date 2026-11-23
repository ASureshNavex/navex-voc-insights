"""The one place that turns a user's data scope into a SQL condition on `account`."""

from dataclasses import dataclass

from sqlalchemy import ColumnElement, false, literal, select, true
from voc_data.enums import DataScope, Ownership
from voc_data.models import Account, Person


@dataclass(frozen=True, slots=True)
class AccessScope:
    upn: str
    data_scope: DataScope
    ownership: Ownership
    region: str | None = None


def _team_upns(upn: str) -> ColumnElement[str]:
    """The user and everyone below them in the org chart. UNION stops on a reporting loop."""
    team = select(literal(upn).label("upn")).cte("team", recursive=True)
    reports = select(Person.upn).join(team, Person.manager_upn == team.c.upn)
    return team.union(reports).c.upn


def scope_filter(scope: AccessScope) -> ColumnElement[bool]:
    owner = (
        Account.ae_owner_upn
        if scope.ownership is Ownership.ACCOUNT_EXECUTIVE
        else Account.cxm_owner_upn
    )
    match scope.data_scope:
        case DataScope.ALL:
            return true()
        case DataScope.OWN_BOOK:
            return owner == scope.upn
        case DataScope.TEAM:
            return owner.in_(select(_team_upns(scope.upn)))
        case DataScope.REGION:
            return Account.region == scope.region if scope.region else false()
