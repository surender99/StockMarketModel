# Indicator Framework

Pipeline:
OHLCV -> Validation -> Indicator -> Feature Store

Every indicator exposes:
name()
version()
parameters()
calculate(data)
