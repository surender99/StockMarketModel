"""Experiment metadata tracking — REQ-EXP-TRACK-001."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import structlog
from pydantic import BaseModel, Field, model_validator

from athena_core import __version__
from athena_core.application.backtest_config import BacktestConfig, ExperimentTrackingConfig
from athena_core.application.backtest_engine import BacktestResult
from athena_core.domain.strategy.config import StrategyConfig

log = structlog.get_logger(__name__)


class ExperimentRecord(BaseModel):
    """Persisted experiment metadata — REQ-EXP-TRACK-001."""

    experiment_id: str
    strategy_id: str
    strategy_version: str
    dataset_version: str
    train_start: str
    train_end: str
    metrics: dict[str, Any]
    git_commit: str | None
    created_at: str
    params: dict[str, Any] = Field(default_factory=dict)
    artifacts: dict[str, str] = Field(default_factory=dict)
    python_version: str = Field(default_factory=lambda: platform.python_version())
    athena_core_version: str = Field(default_factory=lambda: __version__)

    @model_validator(mode="after")
    def required_fields_present(self) -> ExperimentRecord:
        required = {
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "dataset_version": self.dataset_version,
            "train_start": self.train_start,
            "train_end": self.train_end,
            "metrics": self.metrics,
            "git_commit": self.git_commit,
            "created_at": self.created_at,
        }
        missing = [key for key, value in required.items() if value is None and key != "git_commit"]
        if missing:
            msg = f"missing required experiment fields: {missing}"
            raise ValueError(msg)
        if not self.metrics:
            msg = "metrics must not be empty"
            raise ValueError(msg)
        return self


class ExperimentTracker:
    """Write and list experiment records — REQ-EXP-TRACK-001."""

    def __init__(self, config: ExperimentTrackingConfig) -> None:
        self._config = config
        self._base = Path(config.base_path)

    def create_record(
        self,
        strategy: StrategyConfig,
        backtest: BacktestConfig,
        result: BacktestResult,
        *,
        dataset_version: str,
        artifacts: dict[str, str] | None = None,
        git_commit: str | None | object = ...,
    ) -> ExperimentRecord:
        created_at = datetime.now(UTC).replace(microsecond=0).isoformat()
        commit = self._resolve_git_commit(git_commit)
        short_hash = hashlib.sha256(
            json.dumps(
                {
                    "strategy_id": strategy.strategy.id,
                    "start": backtest.start.isoformat(),
                    "end": backtest.end.isoformat(),
                    "metrics": result.metrics,
                    "nonce": datetime.now(UTC).isoformat(),
                },
                sort_keys=True,
            ).encode()
        ).hexdigest()[:8]
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
        experiment_id = f"{stamp}_{strategy.strategy.id}_{short_hash}"

        record = ExperimentRecord(
            experiment_id=experiment_id,
            strategy_id=strategy.strategy.id,
            strategy_version=strategy.strategy.version,
            dataset_version=dataset_version,
            train_start=backtest.start.isoformat(),
            train_end=backtest.end.isoformat(),
            metrics=result.metrics,
            git_commit=commit,
            created_at=created_at,
            params={
                "strategy": strategy.model_dump(mode="json"),
                "backtest": backtest.model_dump(mode="json"),
            },
            artifacts=artifacts or {},
        )
        self._validate_required(record)
        return record

    def save(self, record: ExperimentRecord) -> Path:
        self._base.mkdir(parents=True, exist_ok=True)
        target = self._base / f"{record.experiment_id}.json"
        tmp = target.with_suffix(".json.tmp")
        payload = record.model_dump(mode="json")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp.replace(target)
        self._append_index(record)
        return target

    def list_records(self, limit: int = 50) -> list[ExperimentRecord]:
        if not self._base.exists():
            return []
        files = sorted(self._base.glob("*.json"), reverse=True)
        records: list[ExperimentRecord] = []
        for path in files[:limit]:
            if path.name == "index.json":
                continue
            raw = json.loads(path.read_text(encoding="utf-8"))
            records.append(ExperimentRecord.model_validate(raw))
        return records

    def _append_index(self, record: ExperimentRecord) -> None:
        index_path = self._base / "index.json"
        entries: list[dict[str, Any]] = []
        if index_path.is_file():
            entries = json.loads(index_path.read_text(encoding="utf-8"))
        entries.insert(
            0,
            {
                "experiment_id": record.experiment_id,
                "strategy_id": record.strategy_id,
                "created_at": record.created_at,
                "metrics": record.metrics,
            },
        )
        index_path.write_text(json.dumps(entries[:200], indent=2), encoding="utf-8")

    def _validate_required(self, record: ExperimentRecord) -> None:
        for field_name in self._config.required_fields:
            if field_name == "git_commit":
                continue
            if getattr(record, field_name, None) in (None, "", {}):
                msg = f"required experiment field missing: {field_name}"
                raise ValueError(msg)

    def _resolve_git_commit(self, git_commit: str | None | object) -> str | None:
        if git_commit is not ...:
            return git_commit  # type: ignore[return-value]
        if not self._config.auto_capture_git:
            return None
        try:
            proc = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            return proc.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError) as exc:
            log.warning("experiment.git_unavailable", error=str(exc))
            return None
