# OpenAITrade Public

Free data. Free strategies. Free workflow.

An agent-first quant research project built around `skill.md`.

This repository is designed so that you can start with the skill, not the codebase. The goal is simple:

- use free data quickly
- run free strategies quickly
- backtest and optimize quickly
- get results before reading the whole repository

![Cheat Sheet Card](assets/cheatsheet-card.png)

## What Users Actually See

### Get Data

![Data Demo](assets/data-targeted.png)
Load real sample market data from the repository in seconds.

```bash
python -c "from pathlib import Path; import pandas as pd; p=Path('data/market_data/spy.csv'); df=pd.read_csv(p); print(df.head(5).to_string(index=False))"
```

### Pick Strategy

![Strategy Demo](assets/strategy-targeted.png)
Choose a built-in strategy before you ever read the full codebase.

```bash
python -c "from openaitrade.strategies.factory import STRATEGIES; [print(f'{sid:24s} {cls.category:18s} {cls.name}') for sid, cls in STRATEGIES.items()]"
```

### See Results

![Backtest Demo](assets/backtest-targeted.png)
See a concrete backtest result fast, not just a framework description.

```bash
python examples/quickstart.py
```

### Start With The Skill

![Skill Demo](assets/skill-targeted.png)
Use `skill.md` as the shortest path from idea to result.

```bash
python -m pytest -q tests/test_skill_installation.py
```

## Start Here

- 中文入口: [zh/README.md](/Users/f/GitHub/OpenAITrade/public_release/zh/README.md)
- English entry: [en/README.md](/Users/f/GitHub/OpenAITrade/public_release/en/README.md)

## Cheat Sheet

Install in one line:

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e .
```

Get data fast:

```bash
python -c "from pathlib import Path; import pandas as pd; p=Path('data/market_data/spy.csv'); df=pd.read_csv(p); print(df.head(5).to_string(index=False))"
```

Pick strategy fast:

```bash
python -c "from openaitrade.strategies.factory import STRATEGIES; [print(f'{sid:24s} {cls.category:18s} {cls.name}') for sid, cls in STRATEGIES.items()]"
```

See results fast:

```bash
python examples/quickstart.py
```

Start with the skill:

```bash
python -m pytest -q tests/test_skill_installation.py
```

## What You Can Do Fast

With the public `skill.md`, an agent can help you:

- load free sample or external market data
- inspect and choose from free built-in strategies
- run a backtest without building your own framework first
- try parameter optimization on the same workflow

This is the core product idea of the public release: `skill.md` is the entrypoint, and code is the deeper layer.

## No-Code First

You do not need to understand the whole repository before using it.

The intended path is:

1. Load the skill
2. Use the bundled data or a free data adapter
3. Pick a strategy
4. Run a backtest
5. Try optimization
6. Read the code only if you want to go deeper

## 3-Minute Quickstart

One-line install:

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e .
```

One line to validate the public package:

```bash
python -m pytest -q
```

One line each to do the main workflow:

Get data fast:

```bash
python -c "from pathlib import Path; import pandas as pd; p=Path('data/market_data/spy.csv'); df=pd.read_csv(p); print(df.head(5).to_string(index=False))"
```

Pick a strategy fast:

```bash
python -c "from openaitrade.strategies.factory import STRATEGIES; [print(f'{sid:24s} {cls.category:18s} {cls.name}') for sid, cls in STRATEGIES.items()]"
```

See backtest results fast:

```bash
python examples/quickstart.py
```

Start with the skill:

```bash
python -m pytest -q tests/test_skill_installation.py
```

Detailed copy-paste setup:

```bash
git clone <your-public-repo-url>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -e .
python examples/quickstart.py
python examples/optimize.py
```

If you want to verify the full public package:

```bash
python -m pytest -q
```

## Skill Installation And Verification

The skill flow has already been tested directly in the current directory.

Verified:

- skill-relative paths resolve correctly
- bundled real sample data can be loaded
- strategies can be created through the strategy factory
- backtests can be executed through the backtest engine

Related validation:

- [tests/test_skill_installation.py](/Users/f/GitHub/OpenAITrade/public_release/tests/test_skill_installation.py)

## Shared Core

Both language versions use the same shared assets:

- [openaitrade/data](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/data) for free data access
- [openaitrade/strategies](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/strategies) for free strategies
- [openaitrade/backtest](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/backtest) for backtesting
- [openaitrade/tools](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/tools) for optimization
- [data/market_data](/Users/f/GitHub/OpenAITrade/public_release/data/market_data) for sample data
- [strategy_packs](/Users/f/GitHub/OpenAITrade/public_release/strategy_packs) for structured strategy workflow assets

## Common Use Cases

- “I want an agent to help me test a strategy idea quickly.”
- “I want free data and free strategies before I invest in paid tooling.”
- “I want a reusable quant skill instead of a large platform dependency.”
- “I want backtesting and optimization without building infrastructure first.”

## Repository Layout

```text
public_release/
├── zh/                     # Chinese agent-first docs and skill
├── en/                     # English agent-first docs and skill
├── configs/                # Shared workflow configs
├── data/                   # Shared sample data
├── docs/                   # Shared reference docs
├── examples/               # Runnable examples
├── openaitrade/            # Shared code
├── strategy_packs/         # Structured workflow assets
└── tests/                  # Validation
```

## Why This Repo Exists

This is not a full mirror of the private product. It is the public subset with the strongest reuse value:

- free data access
- free strategy code
- an agent-friendly workflow centered on `skill.md`
