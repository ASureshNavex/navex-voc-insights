"""Structured outputs the model must return. Anything else fails validation and is not stored."""

from pydantic import BaseModel, Field


class AccountSummary(BaseModel):
    explanation: str = Field(
        min_length=20,
        max_length=600,
        description="One to two sentences on what is causing friction for this account.",
    )
    cited_verbatim_ids: list[str] = Field(
        min_length=1, description="IDs of the verbatims the explanation rests on."
    )
