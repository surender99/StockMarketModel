Example

entry:
  ema3 > ema5 > ema9
filters:
  market_regime == bull
exit:
  ema3 < ema5
risk:
  max_positions: 10
