"""Masks personal details before a verbatim is stored. Rules are confirmed with NAVEX security."""

import re

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
_PHONE = re.compile(r"(?<!\w)\+?\d[\d\s().-]{7,}\d(?!\w)")


def mask_personal_details(text: str) -> str:
    return _PHONE.sub("[phone]", _EMAIL.sub("[email]", text))
