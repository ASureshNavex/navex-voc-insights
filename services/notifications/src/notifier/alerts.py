"""Change-of-status alerts: one batched email per owner per run, never sent twice."""

import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from voc_data.enums import DeliveryStatus, Urgency
from voc_data.models import (
    Account,
    AccountTheme,
    Notification,
    StatusChangeEvent,
    Theme,
)

from notifier.ports import Mailer
from notifier.rendering import render

logger = logging.getLogger(__name__)

CHANNEL = "email"
TOP_THEMES = 3
_LABEL = {"R": "Red", "Y": "Yellow", "G": "Green"}


@dataclass(frozen=True, slots=True)
class Change:
    event_id: UUID
    name: str
    from_label: str
    to_label: str
    arr: str
    renewal: str | None
    themes: list[str]
    link: str
    action_needed: bool


async def _changes_by_owner(
    session: AsyncSession, run_id: UUID, base_url: str
) -> dict[str, list[Change]]:
    rows = await session.execute(
        select(StatusChangeEvent, Account)
        .join(Account, Account.account_id == StatusChangeEvent.account_id)
        .where(StatusChangeEvent.run_id == run_id)
        .order_by(Account.arr.desc(), Account.account_id)
    )
    by_owner: dict[str, list[Change]] = defaultdict(list)
    for event, account in rows:
        if not account.cxm_owner_upn:
            continue
        themes = await session.scalars(
            select(Theme.name)
            .join(AccountTheme, AccountTheme.theme_id == Theme.theme_id)
            .where(AccountTheme.account_id == account.account_id, AccountTheme.run_id == run_id)
            .order_by(AccountTheme.rank)
            .limit(TOP_THEMES)
        )
        renewal = account.next_renewal_date
        by_owner[account.cxm_owner_upn].append(
            Change(
                event_id=event.event_id,
                name=account.name,
                from_label=_LABEL[event.from_status],
                to_label=_LABEL[event.to_status],
                arr=f"${account.arr:,.0f}",
                renewal=f"{renewal:%d %b %Y}" if renewal else None,
                themes=list(themes),
                link=f"{base_url}/accounts/{account.sfdc_account_id}"
                f"?src=alert&event={event.event_id}",
                action_needed=event.urgency == Urgency.ACTION_NEEDED,
            )
        )
    return by_owner


async def _unsent(session: AsyncSession, owner: str, changes: list[Change]) -> list[Change]:
    """Changes this owner has not been emailed about. A rerun of the task skips the rest."""
    sent = set(
        await session.scalars(
            select(Notification.event_id).where(
                Notification.recipient_upn == owner,
                Notification.channel == CHANNEL,
                Notification.delivery_status == DeliveryStatus.SENT,
                Notification.event_id.in_([change.event_id for change in changes]),
            )
        )
    )
    return [change for change in changes if change.event_id not in sent]


def _subject(changes: list[Change]) -> str:
    prefix = "Action needed" if any(change.action_needed for change in changes) else "FYI"
    noun = "account" if len(changes) == 1 else "accounts"
    return f"{prefix}: {len(changes)} {noun} changed VoC status"


async def send_status_alerts(
    session: AsyncSession, mailer: Mailer, run_id: UUID, base_url: str
) -> int:
    emails_sent = 0
    for owner, changes in (await _changes_by_owner(session, run_id, base_url)).items():
        pending = await _unsent(session, owner, changes)
        if not pending:
            continue
        subject = _subject(pending)
        context = {"heading": subject, "changes": pending}
        try:
            mailer.send(
                owner,
                subject,
                render("alert.txt.j2", **context),
                render("alert.html.j2", **context),
            )
        except Exception:
            # One owner's failure must not block the others; the next start retries it.
            logger.exception("Alert delivery failed for one recipient")
            continue
        now = datetime.now(UTC)
        session.add_all(
            Notification(
                event_id=change.event_id,
                recipient_upn=owner,
                channel=CHANNEL,
                title=f"{change.name} moved to {change.to_label.lower()}",
                delivery_status=DeliveryStatus.SENT,
                sent_at=now,
            )
            for change in pending
        )
        await session.commit()
        emails_sent += 1
    return emails_sent
