# REQ-DATA-CALENDAR-001

**Requirement ID:** REQ-DATA-CALENDAR-001

**Title:** NSE Trading Calendar

**Purpose:** Provide accurate NSE trading session dates and holidays so indicators, backtests, and data validation never assume calendar-day continuity.

**Description:** The calendar module exposes whether a given date is a trading day on NSE, lists holidays for a year, and generates business-day offsets aligned to NSE sessions. MVP uses a static holiday table (YAML/JSON) maintained manually or sourced from exchange published lists; future versions may fetch from an API.

**Inputs:**
- Date or date range
- Optional year for full holiday list

**Outputs:**
- `is_trading_day(date) -> bool`
- `trading_days_between(start, end) -> list[date]`
- `next_trading_day(date) -> date`
- `previous_trading_day(date) -> date`

**Configuration:**
```yaml
calendar:
  exchange: NSE
  timezone: Asia/Kolkata
  holidays_file: ./config/nse_holidays.yaml
  weekend_days: [Saturday, Sunday]
```

**Algorithm:**
1. Load holiday dates from configured file into a set.
2. `is_trading_day(d)`: return False if weekend or in holiday set; else True.
3. `trading_days_between`: iterate dates, filter with `is_trading_day`.
4. `next/previous_trading_day`: step one calendar day at a time until trading day found (max 10 steps guard).

**Dependencies:**
- Python `datetime`, optional `zoneinfo`
- Static NSE holiday data file

**Acceptance Criteria:**
- [ ] Correctly identifies weekends as non-trading
- [ ] Recognizes known NSE holidays for 2024–2025 (≥10 spot checks)
- [ ] `trading_days_between` excludes holidays and weekends
- [ ] Calendar is injectable (domain port) for testability with mock holidays

**Performance Target:**
- `is_trading_day` lookup: O(1) after load, < 1 ms
- Full year trading day list: < 10 ms

**Unit Tests:**
- Weekend rejection
- Known holiday rejection (Republic Day, Diwali sample dates)
- Consecutive trading day navigation
- Empty holiday file (weekends only)

**Integration Tests:**
- Cross-check 2024 trading day count against published NSE schedule (±1 tolerance for ad-hoc closures)

**Future Enhancements:**
- Muhurat trading sessions
- Ad-hoc market closures (e.g. national mourning)
- BSE/MCX calendar variants
- Auto-update holiday file from exchange feed
