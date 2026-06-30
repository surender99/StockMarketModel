# athena-common

Pure domain types shared across Athena packages — no infrastructure dependencies.

## Contents

- `types.py` — Money, Percentage, OHLC, Candle, Pair, Currency, Precision
- `timeframe.py` — TimeFrame enum
- `enums.py` — Side, OrderType, OrderStatus, SignalDirection
- `events_generated.py` — generated event classes (see `athena/scripts/generate_events.py`)

## Usage

```python
from athena_common import Candle, Money, TimeFrame
```
