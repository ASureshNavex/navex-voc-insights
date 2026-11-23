"""One context model per prompt template. Rendering fails fast on a missing or misspelled field."""

from pydantic import BaseModel


class EvidenceItem(BaseModel):
    id: str
    source: str
    date: str
    text: str


class ThemeLine(BaseModel):
    name: str
    volume: int
    negative_volume: int


class AccountSummaryContext(BaseModel):
    account_name: str
    rating: str
    previous_rating: str | None
    rule_text: str
    products: list[str]
    themes: list[ThemeLine]
    evidence: list[EvidenceItem]
