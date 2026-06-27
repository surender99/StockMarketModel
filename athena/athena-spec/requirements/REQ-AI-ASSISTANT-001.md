# REQ-AI-ASSISTANT-001

**Requirement ID:** REQ-AI-ASSISTANT-001

**Title:** AI Research Assistant

**Purpose:** Enable natural-language experiment orchestration on top of `AthenaClient`, proposing and executing scan, backtest, walk-forward, optimize, and compare workflows with experiment-backed recommendations.

**Description:** The `athena-ai` package provides a rule-based intent parser (with optional OpenAI when `OPENAI_API_KEY` is set), a research orchestrator that delegates to `AthenaClient`, and CLI entrypoints (`athena-ai`, `athena research`). All recommendations must cite persisted experiment IDs and require backtest + walk-forward validation for full-research flows.

**Inputs:**
- Natural-language research query
- Optional Athena config path and profile
- Optional research assistant YAML (`config/research_assistant.yaml`)
- `--dry-run` to propose plans without execution

**Outputs:**
- Structured `ResearchPlan` and `ResearchResult` with step outputs
- Recommendations citing `experiment_id` values
- AI session logs under `experiments/ai_sessions/`

**Configuration:**
```yaml
research_assistant:
  default_strategy_path: ../athena-examples/config/ema_crossover.yaml
  strategy_paths:
    ema: ../athena-examples/config/ema_crossover.yaml
  default_start: "2022-01-01"
  default_end: "2024-06-01"
  ai_session_log_path: ./experiments/ai_sessions
  use_openai_when_available: true
```

**Algorithm:**
1. Parse user query → `ResearchIntent` (rule-based or OpenAI).
2. Build multi-step `ResearchPlan` mapped to `AthenaClient` methods.
3. Execute steps (unless dry-run); backtests use `track_experiment=True`.
4. Walk-forward validation gates recommendations.
5. Log session metadata with linked experiment IDs.

**Dependencies:**
- REQ-SDK-001 (`AthenaClient`)
- REQ-EXP-TRACK-001 (experiment tracking)
- REQ-CLI-001 (`athena research` subcommand)

**Acceptance Criteria:**
- [ ] Rule-based parser handles scan/backtest/walk-forward/optimize/compare/full-research intents
- [ ] `athena research "..."` and `athena-ai` entrypoints work
- [ ] Full-research flow runs scan → backtest (tracked) → walk-forward → compare
- [ ] Recommendations cite experiment IDs; no recommendation without validation path
- [ ] AI sessions logged to configurable path
- [ ] Optional OpenAI parser when `OPENAI_API_KEY` set

**Unit Tests:**
- Intent parser keyword coverage
- Orchestrator plan building and dry-run execution
- Experiment ID requirement for recommendations
- CLI smoke tests

**Future Enhancements:**
- Conversation memory across sessions
- Multi-strategy tournament mode
- Dashboard integration for agent proposals
