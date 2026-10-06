from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

Source = Literal["bundesagentur", "arbeitnow", "adzuna", "email_alert", "company_page"]


class JobPosting(BaseModel):
    """Canonical posting. Every source is converted into this before anything else sees it."""

    source: Source
    source_id: str
    title: str
    company: str
    location: str | None = None
    url: HttpUrl
    description: str = ""
    language: Literal["de", "en", "unknown"] = "unknown"
    posted_at: datetime | None = None
    match_score: float | None = Field(default=None, ge=0, le=1)
