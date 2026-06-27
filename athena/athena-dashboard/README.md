# athena-dashboard

Streamlit MVP dashboard — **REQ-DASH-001**.

## Install

```bash
cd athena/athena-core && pip install -e ".[dev]"
cd ../athena-sdk && pip install -e ".[dev]"
cd ../athena-dashboard && pip install -e ".[dev]"
```

## Run

```bash
athena-dashboard
```

Pages:

- **Scan** — run or upload scan JSON; component score and SHAP charts
- **Experiments** — compare latest N persisted experiments
- **Import** — upload scan JSON for offline viewing

Configure data paths via sidebar config YAML and optional profile.
