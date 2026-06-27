# athena-ai

**AI research assistant** for natural-language experiment orchestration — REQ-AI-ASSISTANT-001.

Parses queries like *"Find the best EMA strategy for sideways markets"* into multi-step research plans (scan → backtest → walk-forward → compare) executed via `AthenaClient`. Recommendations always cite persisted experiment IDs.

## Install

```bash
cd athena/athena-core
pip install -e ".[dev]"
pip install -e "../athena-sdk[dev]" -e "../athena-ai[dev]" -e "../athena-cli[dev]"
```

## Usage

```bash
# Standalone entrypoint (dry-run proposes plan only)
athena-ai "Find the best EMA strategy for sideways markets" --dry-run

# Via unified Athena CLI
athena research "walk-forward validate ema crossover" --config ../athena-examples/config/backtest.yaml --dry-run

# Execute (requires local OHLCV data)
athena research "backtest ema strategy" --config ../athena-examples/config/backtest.yaml
```

Optional OpenAI intent parsing when `OPENAI_API_KEY` is set (`pip install -e ".[openai]"`). Use `--no-openai` to force rule-based parsing.

## Architecture

| Layer | Module | Responsibility |
|-------|--------|----------------|
| `domain/` | intent, research_plan | Entities — no I/O |
| `application/` | intent_parser, orchestrator, research_assistant | Use cases |
| `infrastructure/` | config, experiment_logger, openai_parser | Config and adapters |
| `interfaces/` | cli | `athena-ai` entrypoint |

## Configuration

See `config/research_assistant.yaml` or set `ATHENA_AI_CONFIG`.
