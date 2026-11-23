"""Values the scoring steps pass to each other. No I/O and no framework types."""

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from voc_data.enums import Rating, Urgency


class Confidence(StrEnum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass(frozen=True, slots=True)
class ThemeCount:
    theme_id: str
    name: str
    volume: int
    negative_volume: int


@dataclass(frozen=True, slots=True)
class DriverVerbatim:
    verbatim_id: str
    theme_id: str | None
    source: str
    feedback_date: date
    product: str | None
    text: str
    citation_url: str | None = None


@dataclass(frozen=True, slots=True)
class StatusState:
    confirmed_status: Rating
    pending_status: Rating | None = None
    pending_runs: int = 0


@dataclass(frozen=True, slots=True)
class AccountInput:
    account_id: str
    name: str
    products: tuple[str, ...]
    feedback_count: int
    churn_language: bool
    voc_sentiment: str | None
    previous_week_status: Rating | None
    state: StatusState | None
    theme_counts: tuple[ThemeCount, ...] = ()
    verbatims: tuple[DriverVerbatim, ...] = ()


@dataclass(frozen=True, slots=True)
class RatingDecision:
    rating: Rating
    score: float
    confidence: Confidence
    rule_set_version: str


@dataclass(frozen=True, slots=True)
class Trigger:
    code: str
    text: str


@dataclass(frozen=True, slots=True)
class RankedTheme:
    theme_id: str
    name: str
    volume: int
    negative_volume: int
    rank: int
    is_primary: bool


@dataclass(frozen=True, slots=True)
class StatusChange:
    account_id: str
    from_status: Rating
    to_status: Rating
    urgency: Urgency


@dataclass(frozen=True, slots=True)
class ScoredAccount:
    account: AccountInput
    decision: RatingDecision
    trigger: Trigger
    themes: tuple[RankedTheme, ...]
    drivers: tuple[DriverVerbatim, ...]
    state: StatusState
    explanation: str | None = None
    explanation_hash: str | None = None
    change: StatusChange | None = field(default=None)
