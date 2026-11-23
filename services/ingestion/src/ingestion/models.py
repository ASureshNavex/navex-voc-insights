"""Shapes that cross the ingestion ports. Adapters translate vendor payloads into these."""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SourceAccount(BaseModel):
    sfdc_account_id: str
    name: str
    segment: str
    team: str | None = None
    region: str
    arr: Decimal
    next_renewal_date: date | None = None
    cxm_owner_upn: str | None = None
    ae_owner_upn: str | None = None
    exec_sponsor: str | None = None
    super_product_family: str | None = None
    products: list[str] = []
    churn_score: Decimal | None = None
    churn_score_as_of: date | None = None
    nps_category: str | None = None
    nps_date: date | None = None
    issue_status: str | None = None


class TaxonomyTheme(BaseModel):
    theme_id: str
    level1: str
    level2: str | None = None
    level3: str | None = None
    name: str


class ThemeCount(BaseModel):
    theme_id: str
    volume: int
    negative_volume: int


class SourceVerbatim(BaseModel):
    verbatim_id: str
    theme_id: str | None = None
    source: str
    feedback_date: date
    product: str | None = None
    text: str
    citation_url: str | None = None


class AccountFeedback(BaseModel):
    sfdc_account_id: str
    feedback_count: int
    churn_language: bool = False
    voc_sentiment: str | None = None
    theme_counts: list[ThemeCount] = []
    verbatims: list[SourceVerbatim] = []


class IngestionResult(BaseModel):
    run_id: str
    accounts: int
    matched: int
    unmatched_records: int
