# Master Event Catalog

| Event | Publisher | Subscribers |
|-------|-----------|-------------|
| Data.BarCreated.v1 | Data | Indicators |
| Indicator.Calculated.v1 | Indicators | Patterns, Strategy |
| Pattern.Detected.v1 | Patterns | Strategy |
| Strategy.SignalGenerated.v1 | Strategy | Portfolio, OMS |
| Order.Submitted.v1 | OMS | Broker |
| Trade.Executed.v1 | Broker | Portfolio, Risk |
| Portfolio.Updated.v1 | Portfolio | Analytics, Dashboard |
