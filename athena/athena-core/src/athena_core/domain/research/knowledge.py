"""Research knowledge base — ATH-REL-010 §5.6."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class KnowledgeEntry:
    """Research journal entry — FR-011."""

    entry_id: str
    project_id: str
    title: str
    body: str
    tags: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        project_id: str,
        title: str,
        body: str,
        *,
        tags: list[str] | None = None,
        references: list[str] | None = None,
    ) -> KnowledgeEntry:
        return cls(
            entry_id=str(uuid.uuid4()),
            project_id=project_id,
            title=title,
            body=body,
            tags=list(tags or []),
            references=list(references or []),
        )
