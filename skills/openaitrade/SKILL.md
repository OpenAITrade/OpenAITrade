---
name: openaitrade-public
description: Use when the user wants OpenAITrade public materials loaded into context, especially its free data, free strategies, or its free workflow for backtesting and strategy optimization.
---

# OpenAITrade Public Skill

This skill is the public-facing subset of the OpenAITrade project. It is designed for research, documentation, and strategy understanding rather than private deployment workflows.

Its core framing is:

- free data
- free strategies
- free workflow

Here, free workflow specifically means that the skill can help an agent reach:

- free data access
- free strategy loading
- backtesting
- strategy optimization

## Scope

Load this skill when the user asks for any of the following:

- strategy code
- strategy explanation
- strategy pack authoring
- market data adapter usage
- public strategy documentation
- backtesting workflow
- strategy optimization workflow
- live trading integration notes

## Available content

```text
public_release/
├── openaitrade/data/          # Data adapters and data request helpers
├── openaitrade/backtest/      # Backtest engine
├── openaitrade/strategies/    # Strategy implementations and factory
├── openaitrade/tools/         # Optimization tools
├── strategy_packs/            # YAML + README bundles for each strategy
├── docs/STRATEGIES.md         # Strategy catalog
├── docs/data_sources.md       # Data adapter summary
├── docs/BACKTESTING.md        # Backtest assumptions and outputs
├── docs/LIVE_TRADING.md       # Live trading notes and cautions
└── data/market_data/          # Example CSV market data
```

## Suggested loading order

1. `../../docs/STRATEGIES.md` for the catalog view.
2. `../../strategy_packs/<strategy>/README.md` for human-readable strategy details.
3. `../../openaitrade/strategies/<category>/<file>.py` for implementation details.
4. `../../openaitrade/data/*.py` when the user asks about data ingestion.
5. `../../openaitrade/backtest/*.py` and `../../openaitrade/tools/*.py` for backtesting or optimization.
6. `../../docs/LIVE_TRADING.md` and `../../docs/broker_adapters.md` for live deployment discussions.

## Notes

- This public skill does not assume access to the private web frontend.
- Treat live trading content as integration guidance, not production readiness.
- If the user asks for sensitive deployment details, stay within the published subset unless they explicitly provide the private context.
