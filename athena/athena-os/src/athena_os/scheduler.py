"""Task scheduler — APS-007."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

TaskFn = Callable[[], Any]


@dataclass
class ScheduledTask:
    task_id: str
    name: str
    run_at: datetime
    callback: TaskFn
    cancelled: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


class Scheduler:
    """In-process scheduler stub — due tasks polled by caller."""

    def __init__(self) -> None:
        self._tasks: dict[str, ScheduledTask] = {}

    def schedule(self, name: str, run_at: datetime, callback: TaskFn, **metadata: Any) -> str:
        task_id = uuid4().hex
        self._tasks[task_id] = ScheduledTask(
            task_id=task_id,
            name=name,
            run_at=run_at,
            callback=callback,
            metadata=metadata,
        )
        return task_id

    def cancel(self, task_id: str) -> bool:
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.cancelled = True
        return True

    def due_tasks(self, now: datetime | None = None) -> list[ScheduledTask]:
        current = now or datetime.now(tz=timezone.utc)
        return [
            task
            for task in self._tasks.values()
            if not task.cancelled and task.run_at <= current
        ]

    def run_due(self, now: datetime | None = None) -> list[Any]:
        results: list[Any] = []
        for task in self.due_tasks(now):
            results.append(task.callback())
            self._tasks.pop(task.task_id, None)
        return results
