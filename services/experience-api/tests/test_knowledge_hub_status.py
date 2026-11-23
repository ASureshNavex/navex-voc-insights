import pytest
from voc_data.enums import DocumentStatus as S

from app.core.exceptions import Conflict
from app.domains.knowledge_hub.status import after_clean_check, transition


def test_clean_file_publishes_straight_away_by_default() -> None:
    assert after_clean_check(require_approval=False) is S.PUBLISHED
    assert transition(S.CHECKING, S.PUBLISHED) is S.PUBLISHED


def test_clean_file_waits_for_approval_when_switched_on() -> None:
    assert after_clean_check(require_approval=True) is S.AWAITING_APPROVAL
    assert transition(S.AWAITING_APPROVAL, S.DECLINED) is S.DECLINED


@pytest.mark.parametrize(
    ("current", "target"),
    [(S.DECLINED, S.PUBLISHED), (S.UPLOADING, S.PUBLISHED), (S.WITHDRAWN, S.DRAFT)],
)
def test_other_transitions_conflict(current: S, target: S) -> None:
    with pytest.raises(Conflict):
        transition(current, target)
