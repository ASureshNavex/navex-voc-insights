"""Rating rules. The same inputs always give the same rating, recorded with the rule set version."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import yaml
from voc_data.enums import Rating

from account_scoring_agent.domain.models import AccountInput, Confidence, RatingDecision

LOW_VOLUME = 5
HIGH_VOLUME = 20


class RuleSet(Protocol):
    @property
    def version(self) -> str: ...

    def rate(self, account: AccountInput) -> RatingDecision: ...


def friction_score(account: AccountInput) -> float:
    """Share of negative theme mentions, 0 to 100. Placeholder until NAVEX's formula is imported."""
    volume = sum(theme.volume for theme in account.theme_counts)
    if volume == 0:
        return 0.0
    negative = sum(theme.negative_volume for theme in account.theme_counts)
    return round(100 * negative / volume, 2)


def _confidence(feedback_count: int) -> Confidence:
    if feedback_count >= HIGH_VOLUME:
        return Confidence.HIGH
    return Confidence.MEDIUM if feedback_count >= LOW_VOLUME else Confidence.LOW


@dataclass(frozen=True, slots=True)
class ThresholdRuleSet:
    version: str
    red_above: float
    yellow_from: float

    @classmethod
    def load(cls, path: Path) -> "ThresholdRuleSet":
        return cls(**yaml.safe_load(path.read_text(encoding="utf-8")))

    def rate(self, account: AccountInput) -> RatingDecision:
        score = friction_score(account)
        if score > self.red_above:
            rating = Rating.RED
        elif score >= self.yellow_from:
            rating = Rating.YELLOW
        else:
            rating = Rating.GREEN
        return RatingDecision(rating, score, _confidence(account.feedback_count), self.version)
