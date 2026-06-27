"""Walk-forward validation configuration — REQ-WALK-FORWARD-001."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class WalkForwardConfig(BaseModel):
    """Train/test window parameters — REQ-WALK-FORWARD-001."""

    train_days: int = Field(default=252, ge=1)
    test_days: int = Field(default=63, ge=1)
    step_days: int = Field(default=63, ge=1)
    mode: Literal["rolling", "expanding"] = "rolling"
    min_train_days: int = Field(default=126, ge=1)
