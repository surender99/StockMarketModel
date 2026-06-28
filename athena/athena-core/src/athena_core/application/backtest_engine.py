"""Event-driven backtest engine — REQ-BT-ENGINE-001."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, cast

import pandas as pd
import structlog

from athena_core.application.backtest_config import BacktestConfig
from athena_core.application.backtest_metrics import compute_benchmark_metrics, compute_metrics
from athena_core.application.costs import apply_slippage, compute_trade_costs
from athena_core.application.portfolio_engine import PortfolioEngine
from athena_core.application.regime_engine import RegimeEngine
from athena_core.application.statistics_engine import StatisticsEngine
from athena_core.domain.backtest import TradeRecord
from athena_core.domain.portfolio import PortfolioEvaluation, PortfolioState
from athena_core.domain.portfolio.positions import OpenPosition
from athena_core.domain.ports.ohlcv_repository import OHLCVRepositoryPort
from athena_core.domain.ports.trading_calendar import TradingCalendarPort
from athena_core.domain.strategy.config import StrategyConfig
from athena_core.domain.strategy.expression import evaluate_condition_at_index
from athena_core.domain.strategy.indicators import indicator_column_name, indicator_feature_id

log = structlog.get_logger(__name__)


@dataclass(frozen=True)
class BacktestResult:
    """Backtest outputs."""

    trades: list[TradeRecord]
    equity_curve: pd.DataFrame
    metrics: dict[str, Any]
    benchmark_metrics: dict[str, Any]
    portfolio_evaluation: PortfolioEvaluation | None = None
    statistics_report: dict[str, Any] | None = None


class FeatureProviderPort:
    """Minimal port for indicator/feature access during backtest."""

    def get_indicator_frame(
        self,
        symbol: str,
        indicator_type: str,
        params: dict[str, Any],
        start: date | None,
        end: date | None,
    ) -> pd.DataFrame:
        raise NotImplementedError


class BacktestEngine:
    """Walk-forward backtest engine — REQ-BT-ENGINE-001."""

    def __init__(
        self,
        calendar: TradingCalendarPort,
        ohlcv_repo: OHLCVRepositoryPort,
        feature_provider: FeatureProviderPort,
        regime_engine: RegimeEngine | None = None,
    ) -> None:
        self._calendar = calendar
        self._ohlcv = ohlcv_repo
        self._features = feature_provider
        self._regime = regime_engine

    def run(
        self,
        strategy: StrategyConfig,
        config: BacktestConfig,
        *,
        symbols: list[str] | None = None,
        dataset_version: str = "v1",
    ) -> BacktestResult:
        universe = symbols if symbols is not None else strategy.universe.symbols
        if not universe:
            msg = "backtest requires at least one symbol"
            raise ValueError(msg)

        symbol_frames = self._build_symbol_frames(strategy, universe, config)
        trading_days = self._calendar.trading_days_between(config.start, config.end)

        portfolio = PortfolioState(cash=config.initial_capital)
        trades: list[TradeRecord] = []
        equity_rows: list[dict[str, Any]] = []

        max_positions = int(strategy.position_sizing.params.get("max_positions", 10))

        for session in trading_days:
            marks: dict[str, float] = {}
            for symbol, frame in symbol_frames.items():
                row = self._row_for_date(frame, session)
                if row is not None:
                    marks[symbol] = float(row[config.fill_price])

            self._process_exits(
                strategy,
                config,
                portfolio,
                symbol_frames,
                session,
                trades,
                marks,
            )

            self._process_entries(
                strategy,
                config,
                portfolio,
                symbol_frames,
                session,
                max_positions,
            )

            equity = portfolio.equity(marks)
            equity_rows.append({"date": session, "equity": equity, "cash": portfolio.cash})

        if portfolio.positions and trading_days:
            last_day = trading_days[-1]
            marks = {
                sym: float(
                    symbol_frames[sym]
                    .loc[symbol_frames[sym]["date"] == last_day, config.fill_price]
                    .iloc[0]
                )
                for sym in list(portfolio.positions)
                if sym in symbol_frames
                and not symbol_frames[sym].loc[symbol_frames[sym]["date"] == last_day].empty
            }
            self._process_exits(
                strategy,
                config,
                portfolio,
                symbol_frames,
                last_day,
                trades,
                marks,
                force_reason="end_of_backtest",
            )
            if equity_rows and equity_rows[-1]["date"] == last_day:
                equity_rows[-1]["equity"] = portfolio.equity(marks)
                equity_rows[-1]["cash"] = portfolio.cash

        equity_curve = pd.DataFrame(equity_rows)
        metrics: dict[str, Any] = compute_metrics(
            equity_curve,
            trades,
            initial_capital=config.initial_capital,
        )
        benchmark_metrics = self._benchmark_metrics(config)
        metrics.update(benchmark_metrics)
        metrics["dataset_version"] = dataset_version

        final_marks = self._final_marks(symbol_frames, portfolio, trading_days, config)
        portfolio_eval = PortfolioEngine().evaluate(portfolio, final_marks)
        stats_engine = StatisticsEngine()
        perf = stats_engine.compute_performance(
            equity_curve, trades, initial_capital=config.initial_capital
        )
        bootstrap = stats_engine.bootstrap_sharpe(equity_curve)
        statistics_report = stats_engine.to_report_dict(perf, bootstrap)
        metrics.update(
            {
                "expectancy": statistics_report.get("expectancy"),
                "portfolio_heat": portfolio_eval.metrics.portfolio_heat,
                "gross_exposure": portfolio_eval.metrics.gross_exposure,
            }
        )

        return BacktestResult(
            trades=trades,
            equity_curve=equity_curve,
            metrics=metrics,
            benchmark_metrics=benchmark_metrics,
            portfolio_evaluation=portfolio_eval,
            statistics_report=statistics_report,
        )

    def _build_symbol_frames(
        self,
        strategy: StrategyConfig,
        symbols: list[str],
        config: BacktestConfig,
    ) -> dict[str, pd.DataFrame]:
        frames: dict[str, pd.DataFrame] = {}
        for symbol in symbols:
            ohlcv = self._ohlcv.read(symbol, start=config.start, end=config.end)
            if ohlcv.empty:
                log.warning("backtest.no_ohlcv", symbol=symbol)
                continue
            frame = ohlcv.sort_values("date").reset_index(drop=True)
            for spec in strategy.indicators:
                feature_id = indicator_feature_id(spec.type)
                indicator_df = self._features.get_indicator_frame(
                    symbol,
                    feature_id,
                    spec.params,
                    config.start,
                    config.end,
                )
                col = indicator_column_name(spec)
                merged = indicator_df.sort_values("date").reset_index(drop=True)
                value_col = next(c for c in merged.columns if c != "date")
                indicator_values = merged.rename(columns={value_col: col})[["date", col]]
                frame = frame.merge(indicator_values, on="date", how="left")
                frame[spec.id] = frame[col]
            frames[symbol] = frame
        return frames

    @staticmethod
    def _row_for_date(frame: pd.DataFrame, session: date) -> pd.Series | None:
        matches = frame.index[frame["date"] == session]
        if len(matches) == 0:
            return None
        return cast(pd.Series, frame.loc[matches[0]])

    def _process_exits(
        self,
        strategy: StrategyConfig,
        config: BacktestConfig,
        portfolio: PortfolioState,
        symbol_frames: dict[str, pd.DataFrame],
        session: date,
        trades: list[TradeRecord],
        marks: dict[str, float],
        *,
        force_reason: str | None = None,
    ) -> None:
        to_close: list[tuple[str, str]] = []
        for symbol, position in list(portfolio.positions.items()):
            frame = symbol_frames.get(symbol)
            if frame is None:
                continue
            idx = self._index_for_date(frame, session)
            if idx is None:
                continue

            exit_reason: str | None = force_reason
            bar = frame.iloc[idx]
            float(bar[config.fill_price])

            if (
                exit_reason is None
                and position.stop_price is not None
                and bar["low"] <= position.stop_price
            ):
                exit_reason = "stop_loss"
            elif (
                exit_reason is None
                and position.target_price is not None
                and bar["high"] >= position.target_price
            ):
                exit_reason = "take_profit"
            elif exit_reason is None and strategy.risk.max_holding_days is not None:
                held = (session - position.entry_date).days
                if held >= strategy.risk.max_holding_days:
                    exit_reason = "max_holding_days"

            if exit_reason is None:
                indicator_map = {
                    spec.id: indicator_column_name(spec) for spec in strategy.indicators
                }
                for rule in strategy.exit.rules:
                    if evaluate_condition_at_index(rule.condition, frame, indicator_map, idx):
                        exit_reason = rule.reason
                        break

            if exit_reason is not None:
                to_close.append((symbol, exit_reason))

        for symbol, reason in to_close:
            position = portfolio.positions.pop(symbol)
            fill = apply_slippage(marks[symbol], config.costs, is_buy=False)
            notional = fill * position.quantity
            exit_fees = compute_trade_costs(notional, config.costs, is_sell=True)
            portfolio.cash += notional - exit_fees
            gross_pnl = (fill - position.entry_price) * position.quantity
            net_pnl = gross_pnl - position.entry_fees - exit_fees
            trades.append(
                TradeRecord(
                    symbol=symbol,
                    side="long",
                    entry_date=position.entry_date,
                    exit_date=session,
                    entry_price=position.entry_price,
                    exit_price=fill,
                    quantity=position.quantity,
                    entry_fees=position.entry_fees,
                    exit_fees=exit_fees,
                    gross_pnl=gross_pnl,
                    net_pnl=net_pnl,
                    exit_reason=reason,
                )
            )

    def _process_entries(
        self,
        strategy: StrategyConfig,
        config: BacktestConfig,
        portfolio: PortfolioState,
        symbol_frames: dict[str, pd.DataFrame],
        session: date,
        max_positions: int,
    ) -> None:
        if portfolio.position_count() >= max_positions:
            return

        indicator_map = {spec.id: indicator_column_name(spec) for spec in strategy.indicators}
        candidates: list[str] = []

        for symbol, frame in symbol_frames.items():
            if symbol in portfolio.positions:
                continue
            if not self._passes_filters(strategy, frame, session):
                continue
            idx = self._index_for_date(frame, session)
            if idx is None:
                continue
            for rule in strategy.entry.rules:
                if rule.side != "long":
                    continue
                if evaluate_condition_at_index(rule.condition, frame, indicator_map, idx):
                    candidates.append(symbol)
                    break

        for symbol in candidates:
            if portfolio.position_count() >= max_positions:
                break
            frame = symbol_frames[symbol]
            idx = self._index_for_date(frame, session)
            assert idx is not None
            raw_price = float(frame.iloc[idx][config.fill_price])
            fill = apply_slippage(raw_price, config.costs, is_buy=True)
            qty = self._size_quantity(strategy, config, portfolio, fill)
            if qty <= 0:
                continue
            notional = fill * qty
            entry_fees = compute_trade_costs(notional, config.costs, is_sell=False)
            total_cost = notional + entry_fees
            if total_cost > portfolio.cash:
                affordable = int((portfolio.cash - entry_fees) / fill)
                if affordable <= 0:
                    continue
                qty = affordable
                notional = fill * qty
                entry_fees = compute_trade_costs(notional, config.costs, is_sell=False)
                total_cost = notional + entry_fees

            stop_price = None
            target_price = None
            if strategy.risk.stop_loss_pct is not None:
                stop_price = fill * (1.0 - strategy.risk.stop_loss_pct)
            if strategy.risk.take_profit_pct is not None:
                target_price = fill * (1.0 + strategy.risk.take_profit_pct)

            portfolio.cash -= total_cost
            portfolio.positions[symbol] = OpenPosition(
                symbol=symbol,
                side="long",
                entry_date=session,
                entry_price=fill,
                quantity=qty,
                entry_fees=entry_fees,
                stop_price=stop_price,
                target_price=target_price,
            )

    @staticmethod
    def _index_for_date(frame: pd.DataFrame, session: date) -> int | None:
        matches = frame.index[frame["date"] == session].tolist()
        if not matches:
            return None
        return int(matches[0])

    def _passes_filters(self, strategy: StrategyConfig, frame: pd.DataFrame, session: date) -> bool:
        idx_matches = frame.index[frame["date"] == session].tolist()
        if not idx_matches:
            return False
        idx = int(idx_matches[0])
        for filt in strategy.filters:
            if filt.type == "min_volume":
                min_avg = float(filt.params.get("min_avg_volume_20d", 0))
                if "volume" not in frame.columns:
                    return False
                window = frame["volume"].iloc[max(0, idx - 19) : idx + 1]
                if window.mean() < min_avg:
                    return False
            elif filt.type == "regime":
                if self._regime is None:
                    continue
                state = self._regime.classify_as_of(
                    self._regime._config.benchmark_symbol,
                    session,
                )
                if state is None:
                    return False
                allowed_trends = filt.params.get("allowed_trends", [])
                allowed_vols = filt.params.get("allowed_volatility", [])
                if allowed_trends and state.trend.value not in allowed_trends:
                    return False
                if allowed_vols and state.volatility.value not in allowed_vols:
                    return False
        return True

    @staticmethod
    def _size_quantity(
        strategy: StrategyConfig,
        config: BacktestConfig,
        portfolio: PortfolioState,
        price: float,
    ) -> int:
        if config.allow_fractional:
            msg = "fractional shares not implemented in MVP"
            raise NotImplementedError(msg)

        method = strategy.position_sizing.method
        params = strategy.position_sizing.params
        if method == "fixed_fraction":
            fraction = float(params.get("fraction", 0.05))
            max_positions = int(params.get("max_positions", 10))
            allocation = portfolio.cash * fraction
            per_slot = portfolio.cash / max(max_positions - portfolio.position_count(), 1)
            budget = min(allocation, per_slot)
            return int(budget / price)
        if method == "fixed_amount":
            amount = float(params.get("amount", 0))
            return int(amount / price)
        return 0

    @staticmethod
    def _final_marks(
        symbol_frames: dict[str, pd.DataFrame],
        portfolio: PortfolioState,
        trading_days: list[date],
        config: BacktestConfig,
    ) -> dict[str, float]:
        if not trading_days:
            return {}
        last_day = trading_days[-1]
        marks: dict[str, float] = {}
        symbols = set(portfolio.positions) | set(symbol_frames)
        for sym in symbols:
            frame = symbol_frames.get(sym)
            if frame is None:
                continue
            rows = frame.loc[frame["date"] == last_day]
            if not rows.empty:
                marks[sym] = float(rows.iloc[0][config.fill_price])
        return marks

    def _benchmark_metrics(self, config: BacktestConfig) -> dict[str, Any]:
        benchmark = self._ohlcv.read(config.benchmark, start=config.start, end=config.end)
        if benchmark.empty:
            return compute_benchmark_metrics(
                pd.DataFrame(columns=["date", "close"]),
                initial_capital=config.initial_capital,
            )
        return compute_benchmark_metrics(
            benchmark.sort_values("date"),
            initial_capital=config.initial_capital,
        )
