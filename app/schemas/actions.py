from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

ActionKind = Literal["draft_cover_letter", "save_application", "send_email"]
Status = Literal["pending", "approved", "rejected", "executed", "failed"]


class ProposedAction(BaseModel):
    """What the model is allowed to produce for anything consequential."""

    id: str = Field(default_factory=lambda: uuid4().hex[:8])
    kind: ActionKind
    summary: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: Status = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    result: str | None = None
