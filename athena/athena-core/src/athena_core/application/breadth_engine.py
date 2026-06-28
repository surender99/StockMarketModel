"""Market breadth engine — AES-0401, REQ-MI-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd

from athena_core.domain.indicators.ema import compute_ema
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort


@dataclass(frozen=True)
class BreadthMetrics:
    """Universe breadth snapshot — REQ-MI-001."""

    as_of: date
    advances: int
    declines: int
    unchanged: int
    advance_decline_ratio: float
    pct_above_ema20: float
    pct_above_ema50: float
    new_highs: int
    new_lows: int
    breadth_score: float


class BreadthEngine:
    """Compute advance/decline and % above SMA-style breadth for a universe."""

    def __init__(
        self,
        ohlcv_repo: OHLCVRepositoryPort,
        *,
        lookback_highs_lows: int = 252,
        ema_fast: int = 20,
        ema_slow: int = 50,
    ) -> None:
        self._ohlcv = ohlcv_repo
        self._lookback = lookback_highs_lows
        self._ema_fast = ema_fast
        self._ema_slow = ema_slow

    def compute(self, symbols: list[str], as_of: date) -> BreadthMetrics:
        """Deterministic breadth metrics for *symbols* on *as_of* — REQ-MI-001."""
        start = as_of - timedelta(days=self._lookback + self._ema_slow + 30)
        advances = declines = unchanged = 0
        above_ema20 = above_ema50 = 0
        valid_count = 0
        new_highs = new_lows = 0

        for symbol in sorted(symbols):
            frame = self._ohlcv.read(symbol, start=start, end=as_of)
            if frame.empty:
                continue
            frame = frame.sort_values("date").reset_index(drop=True)
            idx = self._index_for_date(frame, as_of)
            if idx is None or idx < 1:
                continue

            close = float(frame["close"].iloc[idx])
            prev_close = float(frame["close"].iloc[idx - 1])
            if close > prev_close:
                advances += 1
            elif close < prev_close:
                declines += 1
            else:
                unchanged += 1

            closes = frame["close"].astype(float)
            ema20 = compute_ema(closes, self._ema_fast)
            ema50 = compute_ema(closes, self._ema_slow)
            if pd.notna(ema20.iloc[idx]) and close > float(ema20.iloc[idx]):
                above_ema20 += 1
            if pd.notna(ema50.iloc[idx]) and close > float(ema50.iloc[idx]):
                above_ema50 += 1
            valid_count += 1

            window_start = max(0, idx - self._lookback + 1)
            window = frame.iloc[window_start : idx + 1]
            if len(window) >= 2:
                high = float(window["high"].max())
                low = float(window["low"].min())
                if close >= high:
                    new_highs += 1
                if close <= low:
                    new_lows += 1

        if declines > 0:
            ad_ratio = advances / declines
        elif advances > 0:
            ad_ratio = float(advances)
        else:
            ad_ratio = 1.0

        pct_ema20 = (above_ema20 / valid_count) if valid_count else 0.0
        pct_ema50 = (above_ema50 / valid_count) if valid_count else 0.0
        breadth_score = self._breadth_score(ad_ratio, pct_ema20, pct_ema50, new_highs, new_lows)

        return BreadthMetrics(
            as_of=as_of,
            advances=advances,
            declines=declines,
            unchanged=unchanged,
            advance_decline_ratio=round(ad_ratio, 4),
            pct_above_ema20=round(pct_ema20, 4),
            pct_above_ema50=round(pct_ema50, 4),
            new_highs=new_highs,
            new_lows=new_lows,
            breadth_score=round(breadth_score, 2),
        )

    @staticmethod
    def _index_for_date(frame: pd.DataFrame, session: date) -> int | None:
        matches = frame.index[frame["date"] == session].tolist()
        if not matches:
            return None
        return int(matches[0])

    @staticmethod
    def _breadth_score(
        ad_ratio: float,
        pct_ema20: float,
        pct_ema50: float,
        new_highs: int,
        new_lows: int,
    ) -> float:
        """Map breadth inputs to 0–100 score — AES-0401."""
        ad_component = min(max(ad_ratio / 2.0, 0.0), 1.0) * 30.0
        ema_component = (pct_ema20 * 0.6 + pct_ema50 * 0.4) * 50.0
        hl_net = new_highs - new_lows
        hl_component = min(max(0.5 + hl_net / 20.0, 0.0), 1.0) * 20.0
        return min(max(ad_component + ema_component + hl_component, 0.0), 100.0)
