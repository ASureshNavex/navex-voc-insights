from datetime import date

import pytest
from voc_data.enums import Rating, Urgency

from account_scoring_agent.domain.models import (
    AccountInput,
    DriverVerbatim,
    StatusState,
    ThemeCount,
)
from account_scoring_agent.domain.scoring import ThresholdRuleSet
from account_scoring_agent.domain.status_confirmation import confirm_status
from account_scoring_agent.domain.theme_ranking import driver_verbatims, rank_themes
from account_scoring_agent.domain.triggers import trigger_for

RULES = ThresholdRuleSet(version="test", red_above=65, yellow_from=35)


def account(negative: int, volume: int = 10) -> AccountInput:
    return AccountInput(
        account_id="a1", name="Crestview Pharma", products=("Compliance Training",),
        feedback_count=volume, churn_language=False, voc_sentiment="Negative",
        previous_week_status=None, state=None,
        theme_counts=(ThemeCount("t1", "Report accuracy", volume, negative),),
    )  # fmt: skip


@pytest.mark.parametrize(("negative", "expected"), [(7, "R"), (5, "Y"), (3, "G")])
def test_rating_follows_the_rule_set_bands(negative: int, expected: str) -> None:
    decision = RULES.rate(account(negative))
    assert decision.rating == expected
    assert decision.rule_set_version == "test"


def test_no_feedback_scores_zero_and_green() -> None:
    assert RULES.rate(account(0, volume=0)).rating is Rating.GREEN


@pytest.mark.parametrize(
    ("rating", "previous", "churn", "code"),
    [
        (Rating.RED, Rating.YELLOW, False, "AR1"),
        (Rating.RED, Rating.RED, False, "AR2"),
        (Rating.RED, Rating.RED, True, "AR4"),
        (Rating.YELLOW, Rating.GREEN, False, "AY1"),
        (Rating.YELLOW, Rating.YELLOW, False, "AY2"),
        (Rating.YELLOW, Rating.RED, False, "AY3"),
        (Rating.GREEN, Rating.YELLOW, False, "AG0"),
    ],
)
def test_trigger_codes(rating: Rating, previous: Rating, churn: bool, code: str) -> None:
    assert trigger_for(rating, previous, churn).code == code


def test_themes_rank_by_negative_volume_then_volume() -> None:
    ranked = rank_themes(
        (ThemeCount("a", "A", 10, 2), ThemeCount("b", "B", 4, 3), ThemeCount("c", "C", 9, 3))
    )
    assert [t.theme_id for t in ranked] == ["c", "b", "a"]
    assert [t.is_primary for t in ranked] == [True, False, False]


def test_driver_verbatims_keep_the_newest_per_top_theme() -> None:
    def verbatim(vid: str, theme: str, day: int) -> DriverVerbatim:
        return DriverVerbatim(vid, theme, "Support case", date(2026, 11, day), None, "text")

    themes = rank_themes((ThemeCount("a", "A", 5, 4), ThemeCount("b", "B", 5, 1)))
    verbatims = (verbatim("v1", "a", 1), verbatim("v2", "a", 5), verbatim("v3", "b", 2))
    assert [v.verbatim_id for v in driver_verbatims(themes, verbatims, per_theme=1)] == [
        "v2",
        "v3",
    ]


def test_status_change_needs_the_configured_number_of_runs() -> None:
    state = StatusState(confirmed_status=Rating.GREEN)

    state, change = confirm_status("a1", state, Rating.YELLOW, confirm_runs=2)
    assert (state.confirmed_status, state.pending_runs, change) == (Rating.GREEN, 1, None)

    state, change = confirm_status("a1", state, Rating.YELLOW, confirm_runs=2)
    assert state.confirmed_status is Rating.YELLOW
    assert change is not None and change.urgency is Urgency.ACTION_NEEDED


def test_returning_to_the_confirmed_status_clears_the_pending_change() -> None:
    state = StatusState(Rating.GREEN, pending_status=Rating.YELLOW, pending_runs=1)
    state, change = confirm_status("a1", state, Rating.GREEN, confirm_runs=2)
    assert (state.pending_status, state.pending_runs, change) == (None, 0, None)


def test_improvement_is_fyi() -> None:
    state = StatusState(Rating.RED, pending_status=Rating.YELLOW, pending_runs=1)
    _, change = confirm_status("a1", state, Rating.YELLOW, confirm_runs=2)
    assert change is not None and change.urgency is Urgency.FYI
