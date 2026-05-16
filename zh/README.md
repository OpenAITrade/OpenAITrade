# OpenAITrade Public

从 `skill.md` 开始，快速拿到数据、选策略、跑回测、看结果。

免费数据，免费策略，免费工作流。

![Cheat Sheet Card](../assets/cheatsheet-card.png)

## 现在开始

安装：

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e .
```

先拿数据：

```bash
python -c "from pathlib import Path; import pandas as pd; p=Path('data/market_data/spy.csv'); df=pd.read_csv(p); print(df.head(5).to_string(index=False))"
```

先选策略：

```bash
python -c "from openaitrade.strategies.factory import STRATEGIES; [print(f'{sid:24s} {cls.category:18s} {cls.name}') for sid, cls in STRATEGIES.items()]"
```

先看结果：

```bash
python examples/quickstart.py
```

先用 Skill：

```bash
python -m pytest -q tests/test_skill_installation.py
```

## 你会得到

- 仓库里自带的免费样例市场数据
- 可以直接使用的免费内置策略
- 可以马上运行的回测引擎
- 可以直接尝试的参数优化流程
- 把整套流程串起来的 `skill.md`

## 你一眼能看到什么

### 先拿数据

![Data Demo](../assets/data-targeted.png)
几秒内拿到仓库内置的真实样例数据。

### 先选策略

![Strategy Demo](../assets/strategy-targeted.png)
先选一个现成策略，再决定要不要深入读代码实现。

### 先看结果

![Backtest Demo](../assets/backtest-targeted.png)
先跑出真实回测结果，再决定要不要研究整套框架。

### 先用 Skill

![Skill Demo](../assets/skill-targeted.png)
把 `skill.md` 当成从想法到结果的最快路径。

## 如果你只想先跑起来

1. 加载 `skill.md`
2. 使用免费数据
3. 选择免费策略
4. 运行回测
5. 运行优化
6. 只有在你需要更强控制时，再继续读代码

## 快速验证

验证整个公开版：

```bash
python -m pytest -q
```

验证当前目录下的 skill 工作流：

```bash
python -m pytest -q tests/test_skill_installation.py
```

已经验证通过的范围：

- skill 中引用的相对路径可以正确解析
- 可以直接读取真实样例数据
- 可以通过策略工厂创建策略
- 可以通过回测引擎完成回测

## 适合这样用

- 让 agent 快速帮你验证一个策略想法
- 先用免费数据和免费策略试起来
- 不先搭基础设施就开始做回测
- 把量化研究流程沉淀成可复用的 skill

## 去哪里找

- [../openaitrade/data](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/data)：免费数据接入
- [../openaitrade/strategies](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/strategies)：免费策略代码
- [../openaitrade/backtest](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/backtest)：回测引擎
- [../openaitrade/tools](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/tools)：优化工具
- [../data/market_data](/Users/f/GitHub/OpenAITrade/public_release/data/market_data)：免费样例数据
- [../strategy_packs](/Users/f/GitHub/OpenAITrade/public_release/strategy_packs)：结构化策略工作流资产

## 继续深入

- [skills/openaitrade/SKILL.md](/Users/f/GitHub/OpenAITrade/public_release/zh/skills/openaitrade/SKILL.md)
- [docs/STRATEGIES.md](/Users/f/GitHub/OpenAITrade/public_release/zh/docs/STRATEGIES.md)
- [docs/BACKTESTING.md](/Users/f/GitHub/OpenAITrade/public_release/zh/docs/BACKTESTING.md)
- [docs/LIVE_TRADING.md](/Users/f/GitHub/OpenAITrade/public_release/zh/docs/LIVE_TRADING.md)
