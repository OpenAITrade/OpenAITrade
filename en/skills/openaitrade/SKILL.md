---
name: openaitrade-public-en
description: Use when the user wants the OpenAITrade public package loaded into context, especially its free data, free strategies, and free workflow for backtesting and strategy optimization.
---

# OpenAITrade Public Skill

This is the English public skill entrypoint.

Its three key ideas are:

- free data
- free strategies
- free workflow

Here, free workflow specifically means:

- the skill can help an agent access free data
- the skill can help an agent load free strategies
- the skill can help an agent run backtests
- the skill can help an agent perform strategy optimization

## Suggested loading order

1. `../../docs/STRATEGIES.md`
2. `../../../openaitrade/strategies/`
3. `../../../openaitrade/data/`
4. `../../../openaitrade/backtest/`
5. `../../../openaitrade/tools/`
6. `../../docs/LIVE_TRADING.md`
