# REQ-DASH-001

**Requirement ID:** REQ-DASH-001

**Title:** Streamlit Dashboard MVP

**Purpose:** Visualize scan candidates, compare experiments, and inspect feature/SHAP importance without manual JSON inspection.

**Description:** The `athena-dashboard` package ships a Streamlit app (`athena-dashboard` script) with Scan, Experiments, and Import pages. Scan page runs `AthenaClient.scan_dict` or loads uploaded JSON. Experiments page loads latest N comparisons. Candidate drill-down shows component score bar charts and SHAP attribution charts when available.

**Inputs:**
- Sidebar config path and profile
- Strategy path, as-of date, optional symbols file
- Uploaded scan or comparison JSON (Import page)

**Outputs:**
- Interactive tables and bar/line charts in browser

**Configuration:** Uses same Athena YAML as CLI/SDK via sidebar inputs.

**Algorithm:**
1. Build `AthenaClient` from sidebar config.
2. On Scan: call SDK or parse upload → render candidate table and selected symbol detail.
3. On Experiments: `compare_experiments(latest=N)` → table + metric line chart.
4. Render component scores; if `ml_attributions` present, render SHAP bar chart.

**Dependencies:**
- REQ-SDK-001
- REQ-EXPLAIN-001 (optional attributions in scan JSON)

**Acceptance Criteria:**
- [ ] Streamlit app launches via `athena-dashboard`
- [ ] Scan page displays ranked candidates and component scores
- [ ] Experiments page compares latest N runs
- [ ] SHAP attributions chart when scan JSON includes `ml_attributions`
- [ ] Import page accepts uploaded scan JSON

**Unit Tests:**
- Package import smoke test

**Future Enhancements:**
- Live refresh and alerting
- Equity curve visualization from experiment artifacts
