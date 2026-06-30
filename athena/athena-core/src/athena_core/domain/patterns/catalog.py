"""Pattern intelligence APS catalog — PHASE-4 MSP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from athena_core.domain.patterns.base import builtin_pattern_registry

PatternStatus = Literal["MVP", "Partial", "Deferred"]


@dataclass(frozen=True, slots=True)
class PatternApsCatalogEntry:
    """APS spec entry for pattern intelligence platform."""

    aps_id: str
    name: str
    domain: str
    status: PatternStatus


def _p(aps_id: str, name: str, domain: str, status: PatternStatus = "Deferred") -> PatternApsCatalogEntry:
    return PatternApsCatalogEntry(aps_id, name, domain, status)


PATTERN_APS_CATALOG: tuple[PatternApsCatalogEntry, ...] = (
    _p("APS-PAT-ARCH-001", "Pattern Detection Framework", "Pattern-Architecture", "Partial"),
    _p("APS-PAT-PIPELINE-001", "Pattern Detection Pipeline", "Pattern-Architecture", "Partial"),
    _p("APS-SWING-CORE-001", "Swing High Low", "Swing-Engine", "Partial"),
    _p("APS-SWING-PIVOT-001", "Pivot Detection", "Swing-Engine", "Deferred"),
    _p("APS-SWING-ZIGZAG-001", "ZigZag", "Swing-Engine", "Deferred"),
    _p("APS-SWING-STRENGTH-001", "Swing Strength", "Swing-Engine", "Deferred"),
    _p("APS-SWING-HIERARCHY-001", "Swing Hierarchy", "Swing-Engine", "Deferred"),
    _p("APS-SWING-FRACTAL-001", "Fractal Swings", "Swing-Engine", "Deferred"),
    _p("APS-SWING-NOISE-001", "Swing Noise Filter", "Swing-Engine", "Deferred"),
    _p("APS-SWING-CONFIRM-001", "Swing Confirmation", "Swing-Engine", "Deferred"),
    _p("APS-MS-HHHL-001", "Higher High Higher Low", "Market-Structure", "Deferred"),
    _p("APS-MS-BOS-001", "Break of Structure", "Market-Structure", "Deferred"),
    _p("APS-MS-CHOCH-001", "Change of Character", "Market-Structure", "Deferred"),
    _p("APS-MS-TREND-001", "Trend Classification", "Market-Structure", "Deferred"),
    _p("APS-MS-RANGE-001", "Range Detection", "Market-Structure", "Deferred"),
    _p("APS-MS-TRANSITION-001", "Structure Transition", "Market-Structure", "Deferred"),
    _p("APS-MS-LIQUIDITY-001", "Liquidity Sweeps", "Market-Structure", "Deferred"),
    _p("APS-MS-INTERNAL-001", "Internal Structure", "Market-Structure", "Deferred"),
    _p("APS-SR-HORIZONTAL-001", "Horizontal Levels", "Support-Resistance", "Deferred"),
    _p("APS-SR-DYNAMIC-001", "Dynamic Levels", "Support-Resistance", "Deferred"),
    _p("APS-SR-PIVOT-001", "Pivot Levels", "Support-Resistance", "Deferred"),
    _p("APS-SR-FIBONACCI-001", "Fibonacci Levels", "Support-Resistance", "Deferred"),
    _p("APS-SR-CLUSTER-001", "Support Clustering", "Support-Resistance", "Deferred"),
    _p("APS-SR-ZONE-001", "Zone Classification", "Support-Resistance", "Deferred"),
    _p("APS-TL-GENERATOR-001", "Automatic Trendlines", "Trendline-Engine", "Deferred"),
    _p("APS-TL-VALIDATION-001", "Trendline Validation", "Trendline-Engine", "Deferred"),
    _p("APS-TL-CHANNEL-001", "Price Channels", "Trendline-Engine", "Deferred"),
    _p("APS-TL-PARALLEL-001", "Parallel Channels", "Trendline-Engine", "Deferred"),
    _p("APS-TL-SLOPE-001", "Slope Analysis", "Trendline-Engine", "Deferred"),
    _p("APS-TL-BREAK-001", "Trendline Break", "Trendline-Engine", "Deferred"),
    _p("APS-CS-HAMMER-001", "Hammer", "Candlestick-Engine", "MVP"),
    _p("APS-CS-INVERTEDHAMMER-001", "Inverted Hammer", "Candlestick-Engine", "MVP"),
    _p("APS-CS-DOJI-001", "Doji", "Candlestick-Engine", "MVP"),
    _p("APS-CS-LONGLEGGEDDOJI-001", "Long Legged Doji", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-GRAVESTONEDOJI-001", "Gravestone Doji", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-DRAGONFLYDOJI-001", "Dragonfly Doji", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-SPINNINGTOP-001", "Spinning Top", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-MARUBOZU-001", "Marubozu", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-SHOOTINGSTAR-001", "Shooting Star", "Candlestick-Engine", "MVP"),
    _p("APS-CS-HANGINGMAN-001", "Hanging Man", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-BELTHOLD-001", "Belt Hold", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-BULLISHENGULFING-001", "Bullish Engulfing", "Candlestick-Engine", "MVP"),
    _p("APS-CS-BEARISHENGULFING-001", "Bearish Engulfing", "Candlestick-Engine", "MVP"),
    _p("APS-CS-HARAMI-001", "Harami", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-PIERCING-001", "Piercing Line", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-DARKCLOUD-001", "Dark Cloud Cover", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-TWEEZER-001", "Tweezer", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-MORNINGSTAR-001", "Morning Star", "Candlestick-Engine", "MVP"),
    _p("APS-CS-EVENINGSTAR-001", "Evening Star", "Candlestick-Engine", "MVP"),
    _p("APS-CS-THREEWHITESOLDIERS-001", "Three White Soldiers", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-THREEBLACKCROWS-001", "Three Black Crows", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-ABANDONEDBABY-001", "Abandoned Baby", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-THRUSTING-001", "Thrusting Pattern", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-MATCHINGLOW-001", "Matching Low", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-ONNECK-001", "On Neck", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-INNECK-001", "In Neck", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-COUNTERATTACK-001", "Counterattack", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-SEPARATINGLINES-001", "Separating Lines", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-KICKING-001", "Kicking", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-LADDERBOTTOM-001", "Ladder Bottom", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-RISEFALLTHREEMETHODS-001", "Rise Fall Three Methods", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-SIDEBYSIDE-001", "Side By Side", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-STALLEDPATTERN-001", "Stalled Pattern", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-TRISTAR-001", "Tristar", "Candlestick-Engine", "Deferred"),
    _p("APS-CS-UNIQUE3RIVER-001", "Unique Three River", "Candlestick-Engine", "Deferred"),
    _p("APS-CP-DOUBLETOP-001", "Double Top", "Chart-Patterns", "MVP"),
    _p("APS-CP-DOUBLEBOTTOM-001", "Double Bottom", "Chart-Patterns", "MVP"),
    _p("APS-CP-HEADSHOULDERS-001", "Head and Shoulders", "Chart-Patterns", "Deferred"),
    _p("APS-CP-INVERSEHEADSHOULDERS-001", "Inverse Head and Shoulders", "Chart-Patterns", "Deferred"),
    _p("APS-CP-TRIANGLE-001", "Triangle", "Chart-Patterns", "Deferred"),
    _p("APS-CP-WEDGE-001", "Wedge", "Chart-Patterns", "Deferred"),
    _p("APS-CP-FLAG-001", "Flag", "Chart-Patterns", "MVP"),
    _p("APS-CP-PENNANT-001", "Pennant", "Chart-Patterns", "Deferred"),
    _p("APS-CP-CUPHANDLE-001", "Cup and Handle", "Chart-Patterns", "Deferred"),
    _p("APS-CP-RECTANGLE-001", "Rectangle", "Chart-Patterns", "Deferred"),
    _p("APS-CP-DIAMOND-001", "Diamond", "Chart-Patterns", "Deferred"),
    _p("APS-CP-TRIPLETOP-001", "Triple Top", "Chart-Patterns", "Deferred"),
    _p("APS-CP-TRIPLEBOTTOM-001", "Triple Bottom", "Chart-Patterns", "Deferred"),
    _p("APS-CP-ROUNDTOP-001", "Round Top", "Chart-Patterns", "Deferred"),
    _p("APS-CP-ROUNDBOTTOM-001", "Round Bottom", "Chart-Patterns", "Deferred"),
    _p("APS-CP-ASCENDINGTRIANGLE-001", "Ascending Triangle", "Chart-Patterns", "Deferred"),
    _p("APS-CP-DESCENDINGTRIANGLE-001", "Descending Triangle", "Chart-Patterns", "Deferred"),
    _p("APS-CP-SYMMETRICALTRIANGLE-001", "Symmetrical Triangle", "Chart-Patterns", "Deferred"),
    _p("APS-CP-RISINGWEDGE-001", "Rising Wedge", "Chart-Patterns", "Deferred"),
    _p("APS-CP-FALLINGWEDGE-001", "Falling Wedge", "Chart-Patterns", "Deferred"),
    _p("APS-CP-BULLFLAG-001", "Bull Flag", "Chart-Patterns", "MVP"),
    _p("APS-CP-BEARFLAG-001", "Bear Flag", "Chart-Patterns", "MVP"),
    _p("APS-CP-BULLPENNANT-001", "Bull Pennant", "Chart-Patterns", "Deferred"),
    _p("APS-CP-BEARPENNANT-001", "Bear Pennant", "Chart-Patterns", "Deferred"),
    _p("APS-CP-BROADENING-001", "Broadening Formation", "Chart-Patterns", "Deferred"),
    _p("APS-BO-BREAKOUT-001", "Breakout Detection", "Breakout-Engine", "Deferred"),
    _p("APS-BO-FAKEBREAKOUT-001", "Fake Breakout", "Breakout-Engine", "Deferred"),
    _p("APS-BO-VOLUME-001", "Breakout Volume Confirmation", "Breakout-Engine", "Deferred"),
    _p("APS-BO-RETEST-001", "Retest Detection", "Breakout-Engine", "Deferred"),
    _p("APS-BO-RANGE-001", "Range Breakout", "Breakout-Engine", "Deferred"),
    _p("APS-BO-TRENDLINE-001", "Trendline Breakout", "Breakout-Engine", "Deferred"),
    _p("APS-BO-SR-001", "Support Resistance Breakout", "Breakout-Engine", "Deferred"),
    _p("APS-BO-MOMENTUM-001", "Momentum Breakout", "Breakout-Engine", "Deferred"),
    _p("APS-VOLUME-CONFIRM-001", "Volume Spike", "Volume-Confirmation", "Deferred"),
    _p("APS-VOLUME-DIVERGENCE-001", "Volume Divergence", "Volume-Confirmation", "Deferred"),
    _p("APS-VOLUME-PROFILE-001", "Volume Profile", "Volume-Confirmation", "Deferred"),
    _p("APS-VOLUME-CLIMAX-001", "Volume Climax", "Volume-Confirmation", "Deferred"),
    _p("APS-VOLUME-DRYUP-001", "Volume Dry Up", "Volume-Confirmation", "Deferred"),
    _p("APS-VOLUME-TREND-001", "Volume Trend", "Volume-Confirmation", "Deferred"),
    _p("APS-VOLUME-OBV-001", "OBV Confirmation", "Volume-Confirmation", "Deferred"),
    _p("APS-VOLUME-VWAP-001", "VWAP Confirmation", "Volume-Confirmation", "Deferred"),
    _p("APS-SMC-ORDERBLOCK-001", "Order Block", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-FVG-001", "Fair Value Gap", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-LIQUIDITY-001", "Liquidity Pool", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-EQUALHIGHS-001", "Equal Highs", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-EQUALLOWS-001", "Equal Lows", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-MITIGATION-001", "Mitigation Block", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-PREMIUMDISCOUNT-001", "Premium Discount", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-BREAKERBLOCK-001", "Breaker Block", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-INDUCEMENT-001", "Inducement", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-DISPLACEMENT-001", "Displacement", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-LIQUIDITYVOID-001", "Liquidity Void", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-SWEEPS-001", "Liquidity Sweeps", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-INTERNALBOS-001", "Internal BOS", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-EXTERNALBOS-001", "External BOS", "Smart-Money-Concepts", "Deferred"),
    _p("APS-SMC-STRUCTURE-001", "SMC Structure Map", "Smart-Money-Concepts", "Deferred"),
    _p("APS-WYCKOFF-PHASE-001", "Wyckoff Phase", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-SPRING-001", "Wyckoff Spring", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-UPTHRUST-001", "Wyckoff Upthrust", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-ACCUMULATION-001", "Wyckoff Accumulation", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-DISTRIBUTION-001", "Wyckoff Distribution", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-MARKUP-001", "Wyckoff Markup", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-MARKDOWN-001", "Wyckoff Markdown", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-REACCUMULATION-001", "Wyckoff Reaccumulation", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-REDISTRIBUTION-001", "Wyckoff Redistribution", "Wyckoff-Engine", "Deferred"),
    _p("APS-WYCKOFF-COMPOSITEOPERATOR-001", "Composite Operator", "Wyckoff-Engine", "Deferred"),
    _p("APS-EW-WAVECOUNT-001", "Elliott Wave Count", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-IMPULSE-001", "Elliott Impulse Wave", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-CORRECTION-001", "Elliott Correction", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-FIBONACCI-001", "Elliott Fibonacci", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-WAVE1-001", "Wave 1 Detection", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-WAVE3-001", "Wave 3 Detection", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-WAVE5-001", "Wave 5 Detection", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-ABC-001", "ABC Correction", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-FLAT-001", "Flat Correction", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-EW-TRIANGLEWAVE-001", "Triangle Wave", "Elliott-Wave-Engine", "Deferred"),
    _p("APS-SCORE-CONFIDENCE-001", "Pattern Confidence Score", "Pattern-Scoring", "Partial"),
    _p("APS-SCORE-RANKING-001", "Pattern Signal Ranking", "Pattern-Scoring", "Deferred"),
    _p("APS-SCORE-QUALITY-001", "Pattern Quality Score", "Pattern-Scoring", "Deferred"),
    _p("APS-SCORE-TRENDALIGN-001", "Trend Alignment Score", "Pattern-Scoring", "Deferred"),
    _p("APS-SCORE-VOLUMESCORE-001", "Volume Confirmation Score", "Pattern-Scoring", "Deferred"),
    _p("APS-SCORE-CONTEXTSCORE-001", "Context Score", "Pattern-Scoring", "Deferred"),
    _p("APS-PAT-REGISTRY-CORE-001", "Pattern Registry Core", "Pattern-Registry", "MVP"),
    _p("APS-PAT-REGISTRY-META-001", "Pattern Metadata Store", "Pattern-Registry", "MVP"),
    _p("APS-PAT-REGISTRY-DISCOVERY-001", "Pattern Plugin Discovery", "Pattern-Registry", "MVP"),
    _p("APS-PAT-VAL-PRECISION-001", "Pattern Precision Metrics", "Pattern-Validation", "Deferred"),
    _p("APS-PAT-VAL-RECALL-001", "Pattern Recall Metrics", "Pattern-Validation", "Deferred"),
    _p("APS-PAT-VAL-FP-001", "False Positive Detection", "Pattern-Validation", "Deferred"),
    _p("APS-PAT-VAL-FN-001", "False Negative Detection", "Pattern-Validation", "Deferred"),
    _p("APS-PAT-VAL-TV-001", "TradingView Validation", "Pattern-Validation", "Deferred"),
    _p("APS-PAT-VAL-GOLDEN-001", "Golden Dataset Validation", "Pattern-Validation", "Partial"),
    _p("APS-PAT-VAL-LOOKAHEAD-001", "Lookahead Checks", "Pattern-Validation", "Deferred"),
    _p("APS-PAT-VAL-MINBARS-001", "Minimum Bars Validation", "Pattern-Validation", "Deferred"),
    _p("APS-PAT-GOLD-CANDLE-001", "Candlestick Golden Dataset", "Golden-Datasets", "Deferred"),
    _p("APS-PAT-GOLD-CHART-001", "Chart Pattern Golden Dataset", "Golden-Datasets", "Deferred"),
    _p("APS-PAT-GOLD-BREAKOUT-001", "Breakout Golden Dataset", "Golden-Datasets", "Deferred"),
    _p("APS-PAT-GOLD-SWING-001", "Swing Structure Golden Dataset", "Golden-Datasets", "Deferred"),
    _p("APS-PAT-GOLD-BOS-001", "BOS CHOCH Golden Dataset", "Golden-Datasets", "Deferred"),
    _p("APS-PAT-GOLD-SMC-001", "SMC Golden Dataset", "Golden-Datasets", "Deferred"),
)


@dataclass(frozen=True, slots=True)
class PatternCatalogEntry:
    """Metadata for a built-in pattern detector."""

    pattern_id: str
    aps_id: str
    category: str
    status: PatternStatus


_BUILTIN_APS: dict[str, str] = {
    "hammer": "APS-CS-HAMMER-001",
    "inverted_hammer": "APS-CS-INVERTEDHAMMER-001",
    "doji": "APS-CS-DOJI-001",
    "shooting_star": "APS-CS-SHOOTINGSTAR-001",
    "bullish_engulfing": "APS-CS-BULLISHENGULFING-001",
    "bearish_engulfing": "APS-CS-BEARISHENGULFING-001",
    "morning_star": "APS-CS-MORNINGSTAR-001",
    "evening_star": "APS-CS-EVENINGSTAR-001",
    "bull_flag": "APS-CP-BULLFLAG-001",
    "bear_flag": "APS-CP-BEARFLAG-001",
    "double_top": "APS-CP-DOUBLETOP-001",
    "double_bottom": "APS-CP-DOUBLEBOTTOM-001",
}


def build_pattern_catalog() -> tuple[PatternCatalogEntry, ...]:
    """Build catalog from registered builtin patterns."""
    entries: list[PatternCatalogEntry] = []
    for pattern_id in builtin_pattern_registry():
        category = "Candlestick-Engine" if pattern_id in {
            "hammer", "inverted_hammer", "doji", "shooting_star",
            "bullish_engulfing", "bearish_engulfing", "morning_star", "evening_star",
        } else "Chart-Patterns"
        entries.append(
            PatternCatalogEntry(
                pattern_id=pattern_id,
                aps_id=_BUILTIN_APS.get(pattern_id, "APS-PAT-REGISTRY-CORE-001"),
                category=category,
                status="MVP",
            )
        )
    return tuple(entries)


PATTERN_CATALOG: tuple[PatternCatalogEntry, ...] = build_pattern_catalog()


def list_mvp_patterns() -> list[PatternApsCatalogEntry]:
    return [e for e in PATTERN_APS_CATALOG if e.status == "MVP"]


def lookup_pattern_aps(pattern_id: str) -> PatternCatalogEntry | None:
    """Resolve APS metadata for a pattern id."""
    for entry in PATTERN_CATALOG:
        if entry.pattern_id == pattern_id:
            return entry
    return None


def lookup_by_aps_id(aps_id: str) -> PatternApsCatalogEntry | None:
    """Resolve APS catalog entry by id."""
    for entry in PATTERN_APS_CATALOG:
        if entry.aps_id == aps_id:
            return entry
    return None

