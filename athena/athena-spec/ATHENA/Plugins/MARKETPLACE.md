# Plugin Marketplace Architecture

> **Status:** Specification (Priority 3)  
> **Runtime:** `athena_os.plugins.PluginRegistry`, `PluginManifest`

## Overview

The Athena plugin marketplace enables third-party and internal extensions for indicators, patterns, strategies, risk models, and ML models without modifying core packages.

## Plugin Types

| Type | Package | Discovery |
|------|---------|-----------|
| Indicator | `athena-indicators` | `PluginType.INDICATOR` |
| Pattern | `athena-patterns` | `PluginType.PATTERN` |
| Strategy | `athena-strategies` | `PluginType.STRATEGY` |
| Risk | `athena-risk` | `PluginType.RISK` |
| ML Model | `athena-ai` | `PluginType.ML_MODEL` |

## Manifest Contract

`PluginManifest` (in `athena_os.plugins`) carries:

- `id`, `version`, `plugin_type`
- `metadata` (name, description, author)
- `entry_point` — import path to factory function
- `dependencies` — other plugin IDs required
- `marketplace_url` — optional catalog link

## Lifecycle

```
discover → validate manifest → register → activate → execute
```

## Security

- Plugins run in-process (ADR-0003); marketplace entries must be signed and reviewed before production activation.
- RBAC gates plugin registration via `athena_os.security`.

## Future Work

- Remote catalog API
- Version compatibility matrix
- Sandboxed execution for untrusted plugins
