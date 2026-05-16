# OpenAITrade Public

免费数据，免费策略，免费工作流。

一个围绕 `skill.md` 构建的 agent-first 量化研究项目。

这个项目的设计重点不是“先读完整个代码仓库”，而是“先把结果跑出来”。你应该先从 `skill.md` 开始，再决定要不要深入读代码。

![Cheat Sheet Card](../assets/cheatsheet-card.png)

## 用户能直接看到什么

### 先拿数据

![Data Demo](../assets/data-targeted.png)
几秒内拿到仓库内置的真实样例数据。

```bash
python -c "from pathlib import Path; import pandas as pd; p=Path('data/market_data/spy.csv'); df=pd.read_csv(p); print(df.head(5).to_string(index=False))"
```

### 先选策略

![Strategy Demo](../assets/strategy-targeted.png)
先选一个现成策略，再决定要不要深入读完整代码。

```bash
python -c "from openaitrade.strategies.factory import STRATEGIES; [print(f'{sid:24s} {cls.category:18s} {cls.name}') for sid, cls in STRATEGIES.items()]"
```

### 先看结果

![Backtest Demo](../assets/backtest-targeted.png)
先看到真实回测结果，而不是先理解整套框架。

```bash
python examples/quickstart.py
```

### 先用 Skill

![Skill Demo](../assets/skill-targeted.png)
把 `skill.md` 当成从想法到结果的最短路径。

```bash
python -m pytest -q tests/test_skill_installation.py
```

## Cheat Sheet

一句话安装：

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

## 你可以很快做到什么

通过这个公开版 skill，agent 可以帮你：

- 快速读取免费样例数据或免费数据源
- 快速选择并运行内置免费策略
- 快速完成回测
- 快速尝试参数优化

这就是这个公开项目最想强调的特色：先用 skill，后看代码。

## 不写代码也能先开始

推荐使用路径：

1. 加载 `skill.md`
2. 使用免费数据
3. 选择免费策略
4. 运行回测
5. 运行优化
6. 如果需要，再继续深入代码实现

## 3 分钟快速开始

一句话安装：

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e .
```

安装完成后，一句话验证整个公开版：

```bash
python -m pytest -q
```

安装完成后，一句话完成下面功能：

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

详细可直接复制的安装指令：

```bash
git clone <your-public-repo-url>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -e .
python examples/quickstart.py
python examples/optimize.py
```

如果你想验证整个公开版工作流：

```bash
python -m pytest -q
```

## Skill 安装与验证

当前目录下的 `skill.md` 已经完成可用性测试，目的是确保用户通过 skill 就能进入这套免费数据、免费策略、免费回测工作流。

已验证通过：

- skill 中引用的相对路径可以正确解析
- 可以直接读取当前目录中的真实样例数据
- 可以通过策略工厂创建策略
- 可以通过回测引擎完成回测

对应测试文件：

- [tests/test_skill_installation.py](/Users/f/GitHub/OpenAITrade/public_release/tests/test_skill_installation.py)

如果你只想验证 skill 所承诺的最小工作流，也可以直接运行：

```bash
python examples/quickstart.py
python examples/optimize.py
```

## 这个项目最适合谁

- 想让 agent 快速帮自己做策略研究的人
- 想先用免费数据、免费策略试起来的人
- 不想先搭完整回测框架的人
- 想把量化研究流程沉淀成 skill 的人

## 推荐阅读顺序

1. 先看 [skills/openaitrade/SKILL.md](/Users/f/GitHub/OpenAITrade/public_release/zh/skills/openaitrade/SKILL.md)
2. 再看 [docs/STRATEGIES.md](/Users/f/GitHub/OpenAITrade/public_release/zh/docs/STRATEGIES.md)
3. 然后跑 `examples/quickstart.py`
4. 再跑 `examples/optimize.py`
5. 最后如果你想深入，再看共享代码层

## 共享核心

中英文入口共用同一套代码和研究资源：

- [../openaitrade/data](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/data)：免费数据接入
- [../openaitrade/strategies](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/strategies)：免费策略代码
- [../openaitrade/backtest](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/backtest)：回测引擎
- [../openaitrade/tools](/Users/f/GitHub/OpenAITrade/public_release/openaitrade/tools)：优化工具
- [../data/market_data](/Users/f/GitHub/OpenAITrade/public_release/data/market_data)：免费样例数据
- [../strategy_packs](/Users/f/GitHub/OpenAITrade/public_release/strategy_packs)：结构化策略工作流资产

## 目录说明

```text
zh/
├── README.md
├── docs/
└── skills/
```

这个中文目录主要负责：

- 给中文用户提供 agent-first 入口
- 给 skill 使用者提供最短路径
- 把“免费数据、免费策略、免费工作流”讲清楚

## 项目定位

这不是完整商业产品的公开镜像，而是一个更适合被复用的公共子集：

- 免费数据
- 免费策略
- 以 `skill.md` 为核心的 agent-friendly 工作流
