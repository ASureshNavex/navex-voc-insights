"""Tables of the serving store. Column meanings are in docs/02-architecture/lld.md, section 3.2."""

from datetime import date, datetime
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from voc_data.enums import DeliveryStatus, DocumentStatus, RunStatus

# JSONB on PostgreSQL, plain JSON on SQLite so unit tests need no database server.
JsonColumn = JSON().with_variant(JSONB(), "postgresql")


class Base(DeclarativeBase):
    pass


def _uuid_pk() -> Mapped[UUID]:
    return mapped_column(primary_key=True, default=uuid4)


def _created_at() -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), server_default=func.now())


class Person(Base):
    """A user synced from Corp AD and the org chart. Drives TEAM and REGION scopes."""

    __tablename__ = "person"

    upn: Mapped[str] = mapped_column(String(320), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(200))
    manager_upn: Mapped[str | None] = mapped_column(String(320), index=True)
    team: Mapped[str | None] = mapped_column(String(120))
    segment: Mapped[str | None] = mapped_column(String(120))
    region: Mapped[str | None] = mapped_column(String(60))


class Account(Base):
    __tablename__ = "account"

    account_id: Mapped[UUID] = _uuid_pk()
    sfdc_account_id: Mapped[str] = mapped_column(String(18), unique=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    segment: Mapped[str] = mapped_column(String(60))
    team: Mapped[str | None] = mapped_column(String(120))
    region: Mapped[str] = mapped_column(String(60))
    arr: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    next_renewal_date: Mapped[date | None] = mapped_column(Date)
    cxm_owner_upn: Mapped[str | None] = mapped_column(String(320), index=True)
    ae_owner_upn: Mapped[str | None] = mapped_column(String(320), index=True)
    exec_sponsor: Mapped[str | None] = mapped_column(String(200))
    super_product_family: Mapped[str | None] = mapped_column(String(120))
    products: Mapped[list[str]] = mapped_column(JsonColumn, default=list)
    churn_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    churn_score_as_of: Mapped[date | None] = mapped_column(Date)
    nps_category: Mapped[str | None] = mapped_column(String(20))
    nps_date: Mapped[date | None] = mapped_column(Date)
    issue_status: Mapped[str | None] = mapped_column(String(40))


class RefreshRun(Base):
    __tablename__ = "refresh_run"

    run_id: Mapped[UUID] = _uuid_pk()
    started_at: Mapped[datetime] = _created_at()
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[RunStatus] = mapped_column(String(20), default=RunStatus.RUNNING)
    is_alert_evaluation: Mapped[bool] = mapped_column(Boolean, default=False)
    accounts_processed: Mapped[int] = mapped_column(Integer, default=0)
    unmatched_records: Mapped[int] = mapped_column(Integer, default=0)
    rule_set_version: Mapped[str | None] = mapped_column(String(40))
    note: Mapped[str | None] = mapped_column(Text)


class PublishedRun(Base):
    """Single row naming the run that readers see. Switched in one transaction."""

    __tablename__ = "published_run"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("refresh_run.run_id"))
    published_at: Mapped[datetime] = _created_at()
    next_refresh_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AccountFeedbackBatch(Base):
    """Evidence the ingestion task stages per account and run for the scoring agent."""

    __tablename__ = "account_feedback_batch"

    run_id: Mapped[UUID] = mapped_column(ForeignKey("refresh_run.run_id"), primary_key=True)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"), primary_key=True)
    feedback_count: Mapped[int] = mapped_column(Integer, default=0)
    churn_language: Mapped[bool] = mapped_column(Boolean, default=False)
    voc_sentiment: Mapped[str | None] = mapped_column(String(20))
    theme_counts: Mapped[list[dict[str, Any]]] = mapped_column(JsonColumn, default=list)
    verbatims: Mapped[list[dict[str, Any]]] = mapped_column(JsonColumn, default=list)


class AccountRating(Base):
    __tablename__ = "account_rating"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"), primary_key=True)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("refresh_run.run_id"), primary_key=True)
    status: Mapped[str] = mapped_column(String(1), index=True)
    previous_status: Mapped[str | None] = mapped_column(String(1))
    score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    rule_code: Mapped[str] = mapped_column(String(10))
    rule_text: Mapped[str] = mapped_column(String(200))
    confidence: Mapped[str | None] = mapped_column(String(20))
    churn_language: Mapped[bool] = mapped_column(Boolean, default=False)
    voc_sentiment: Mapped[str | None] = mapped_column(String(20))
    explanation: Mapped[str | None] = mapped_column(Text)
    # Hash of the evidence the explanation was written from; unchanged evidence reuses the text.
    explanation_hash: Mapped[str | None] = mapped_column(String(64))
    feedback_count: Mapped[int] = mapped_column(Integer, default=0)
    signals: Mapped[dict[str, Any]] = mapped_column(JsonColumn, default=dict)
    rule_set_version: Mapped[str] = mapped_column(String(40))


class Theme(Base):
    """Enterpret taxonomy entry, stored as delivered with no custom layer."""

    __tablename__ = "theme"

    theme_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    level1: Mapped[str] = mapped_column(String(200))
    level2: Mapped[str | None] = mapped_column(String(200))
    level3: Mapped[str | None] = mapped_column(String(200))
    name: Mapped[str] = mapped_column(String(200), index=True)


class AccountTheme(Base):
    __tablename__ = "account_theme"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"), primary_key=True)
    theme_id: Mapped[str] = mapped_column(ForeignKey("theme.theme_id"), primary_key=True)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("refresh_run.run_id"), primary_key=True)
    volume: Mapped[int] = mapped_column(Integer)
    negative_volume: Mapped[int] = mapped_column(Integer)
    rank: Mapped[int] = mapped_column(Integer)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)


class VerbatimRef(Base):
    """A masked excerpt that drives a theme. Raw records stay in Enterpret."""

    __tablename__ = "verbatim_ref"

    verbatim_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("refresh_run.run_id"), primary_key=True)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"), index=True)
    theme_id: Mapped[str | None] = mapped_column(ForeignKey("theme.theme_id"))
    source: Mapped[str] = mapped_column(String(60))
    feedback_date: Mapped[date] = mapped_column(Date)
    product: Mapped[str | None] = mapped_column(String(120))
    masked_excerpt: Mapped[str] = mapped_column(Text)
    citation_url: Mapped[str | None] = mapped_column(Text)


class AccountStatusState(Base):
    """Memory that keeps alerts from flapping. See LLD 5.2."""

    __tablename__ = "account_status_state"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"), primary_key=True)
    confirmed_status: Mapped[str] = mapped_column(String(1))
    confirmed_at: Mapped[datetime] = _created_at()
    pending_status: Mapped[str | None] = mapped_column(String(1))
    pending_runs: Mapped[int] = mapped_column(Integer, default=0)
    last_alert_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class StatusChangeEvent(Base):
    __tablename__ = "status_change_event"

    event_id: Mapped[UUID] = _uuid_pk()
    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"), index=True)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("refresh_run.run_id"), index=True)
    from_status: Mapped[str] = mapped_column(String(1))
    to_status: Mapped[str] = mapped_column(String(1))
    urgency: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = _created_at()


class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = (UniqueConstraint("event_id", "recipient_upn", "channel"),)

    notification_id: Mapped[UUID] = _uuid_pk()
    event_id: Mapped[UUID | None] = mapped_column(ForeignKey("status_change_event.event_id"))
    recipient_upn: Mapped[str] = mapped_column(String(320), index=True)
    channel: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(String(300))
    delivery_status: Mapped[DeliveryStatus] = mapped_column(
        String(20), default=DeliveryStatus.PENDING
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = _created_at()


class WeeklySnapshot(Base):
    __tablename__ = "weekly_snapshot"

    week_start: Mapped[date] = mapped_column(Date, primary_key=True)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("account.account_id"), primary_key=True)
    status: Mapped[str] = mapped_column(String(1))
    score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    arr: Mapped[Decimal] = mapped_column(Numeric(14, 2))


class SavedView(Base):
    __tablename__ = "saved_view"
    __table_args__ = (UniqueConstraint("owner_upn", "name"),)

    view_id: Mapped[UUID] = _uuid_pk()
    owner_upn: Mapped[str] = mapped_column(String(320), index=True)
    name: Mapped[str] = mapped_column(String(120))
    filters: Mapped[dict[str, Any]] = mapped_column(JsonColumn)
    created_at: Mapped[datetime] = _created_at()


class DigestTemplate(Base):
    __tablename__ = "digest_template"

    digest_id: Mapped[UUID] = _uuid_pk()
    name: Mapped[str] = mapped_column(String(120), unique=True)
    audience: Mapped[str] = mapped_column(String(60))
    schedule: Mapped[str] = mapped_column(String(60))
    content: Mapped[dict[str, bool]] = mapped_column(JsonColumn)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class DigestPreference(Base):
    __tablename__ = "digest_preference"

    upn: Mapped[str] = mapped_column(String(320), primary_key=True)
    digest_id: Mapped[UUID] = mapped_column(
        ForeignKey("digest_template.digest_id"), primary_key=True
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_document"

    document_id: Mapped[UUID] = _uuid_pk()
    title: Mapped[str] = mapped_column(String(200))
    source_type: Mapped[str | None] = mapped_column(String(60))
    account_id: Mapped[UUID | None] = mapped_column(ForeignKey("account.account_id"))
    product_domain: Mapped[str | None] = mapped_column(String(120))
    file_name: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(120))
    size_bytes: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str | None] = mapped_column(String(64), index=True)
    storage_key: Mapped[str] = mapped_column(Text)
    status: Mapped[DocumentStatus] = mapped_column(String(30), index=True)
    uploaded_by_upn: Mapped[str] = mapped_column(String(320), index=True)
    uploaded_at: Mapped[datetime] = _created_at()
    decided_by_upn: Mapped[str | None] = mapped_column(String(320))
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    decline_reason: Mapped[str | None] = mapped_column(Text)


class KnowledgeReviewEvent(Base):
    __tablename__ = "knowledge_review_event"

    event_id: Mapped[UUID] = _uuid_pk()
    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("knowledge_document.document_id"), index=True
    )
    from_status: Mapped[str] = mapped_column(String(30))
    to_status: Mapped[str] = mapped_column(String(30))
    actor_upn: Mapped[str] = mapped_column(String(320))
    note: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = _created_at()


class AuditEvent(Base):
    __tablename__ = "audit_event"

    audit_id: Mapped[UUID] = _uuid_pk()
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    actor_upn: Mapped[str] = mapped_column(String(320), index=True)
    action: Mapped[str] = mapped_column(String(60), index=True)
    detail: Mapped[dict[str, Any]] = mapped_column(JsonColumn, default=dict)
