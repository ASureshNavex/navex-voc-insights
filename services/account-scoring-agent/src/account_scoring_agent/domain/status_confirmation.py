"""Keeps alerts from flapping: a new status must hold for several runs before it is confirmed."""

from voc_data.enums import Rating, Urgency

from account_scoring_agent.domain.models import StatusChange, StatusState

_SEVERITY = {Rating.GREEN: 0, Rating.YELLOW: 1, Rating.RED: 2}


def confirm_status(
    account_id: str, state: StatusState | None, new: Rating, confirm_runs: int
) -> tuple[StatusState, StatusChange | None]:
    # First sighting: record the status without raising a change.
    if state is None:
        return StatusState(confirmed_status=new), None
    if new is state.confirmed_status:
        return StatusState(confirmed_status=new), None

    pending_runs = state.pending_runs + 1 if new is state.pending_status else 1
    if pending_runs < confirm_runs:
        return StatusState(state.confirmed_status, new, pending_runs), None

    worse = _SEVERITY[new] > _SEVERITY[state.confirmed_status]
    change = StatusChange(
        account_id=account_id,
        from_status=state.confirmed_status,
        to_status=new,
        urgency=Urgency.ACTION_NEEDED if worse else Urgency.FYI,
    )
    return StatusState(confirmed_status=new), change
