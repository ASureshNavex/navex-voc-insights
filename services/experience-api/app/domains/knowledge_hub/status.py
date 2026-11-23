"""Document status rules. Pure functions, so every transition is unit tested without I/O."""

from voc_data.enums import DocumentStatus as S

from app.core.exceptions import Conflict

ALLOWED_CONTENT_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "text/csv": "csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
}

_TRANSITIONS: dict[S, set[S]] = {
    S.DRAFT: {S.UPLOADING, S.WITHDRAWN},
    S.UPLOADING: {S.CHECKING},
    S.CHECKING: {S.REJECTED_BY_CHECK, S.AWAITING_APPROVAL, S.PUBLISHED},
    S.AWAITING_APPROVAL: {S.PUBLISHED, S.DECLINED},
    S.PUBLISHED: {S.WITHDRAWN},
}


def after_clean_check(require_approval: bool) -> S:
    """A clean file is published straight away unless the approval step is switched on."""
    return S.AWAITING_APPROVAL if require_approval else S.PUBLISHED


def transition(current: S, target: S) -> S:
    if target not in _TRANSITIONS.get(current, set()):
        raise Conflict(f"A file that is {current.value} cannot become {target.value}.")
    return target
