from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openaitrade.backtest.engine import BacktestConfig, BacktestEngine
from openaitrade.data.base import CsvAdapter, DataRequest
from openaitrade.strategies.factory import STRATEGIES, create_strategy
from openaitrade.tools import OptimizationConfig, ParameterOptimizer


ARTIFACTS_DIR = ROOT / "artifacts"


def svg_line(values: list[float], width: int = 1000, height: int = 300) -> str:
    if not values:
        return ""
    min_v = min(values)
    max_v = max(values)
    span = max(max_v - min_v, 1e-9)
    points = []
    for i, value in enumerate(values):
        x = i * (width - 28) / max(len(values) - 1, 1) + 14
        y = height - (((value - min_v) / span) * (height - 28) + 14)
        points.append(f"{x:.2f},{y:.2f}")
    polyline = " ".join(points)
    return f"""
    <svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Equity curve">
      <defs>
        <linearGradient id="fillGrad" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#37b4ff" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#37b4ff" stop-opacity="0.04"/>
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="{width}" height="{height}" rx="24" fill="#09111f"/>
      <polyline points="{polyline}" fill="none" stroke="#7cc7ff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """


def page_template(title: str, eyebrow: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #06111d;
      --panel: rgba(14, 28, 45, 0.92);
      --panel-2: rgba(18, 38, 62, 0.96);
      --ink: #f2f7ff;
      --muted: #9ab2ce;
      --line: rgba(255,255,255,0.09);
      --good: #57d58f;
      --accent: #7cc7ff;
      --warm: #ffd166;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(124,199,255,0.16), transparent 28%),
        radial-gradient(circle at bottom right, rgba(255,209,102,0.12), transparent 24%),
        var(--bg);
    }}
    .wrap {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 42px;
    }}
    .eyebrow {{
      display: inline-flex;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(124,199,255,0.35);
      color: var(--accent);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 16px;
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 44px;
      line-height: 1.03;
      letter-spacing: -0.03em;
    }}
    p {{
      color: var(--muted);
      line-height: 1.6;
      font-size: 17px;
      margin: 0 0 20px;
    }}
    .panel {{
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid var(--line);
      border-radius: 24px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.28);
      backdrop-filter: blur(10px);
      overflow: hidden;
    }}
    .panel-inner {{ padding: 24px; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 18px;
    }}
    .metric {{
      background: var(--panel-2);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
    }}
    .metric .label {{ color: var(--muted); font-size: 13px; }}
    .metric .value {{ margin-top: 8px; font-size: 28px; font-weight: 700; }}
    .accent {{ color: var(--accent); }}
    .good {{ color: var(--good); }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      text-align: left;
      padding: 11px 10px;
      border-bottom: 1px solid var(--line);
    }}
    th {{ color: var(--muted); font-weight: 600; }}
    code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 13px;
      color: #d8ebff;
      background: rgba(255,255,255,0.04);
      padding: 3px 7px;
      border-radius: 8px;
    }}
    ul {{
      margin: 10px 0 0;
      padding-left: 20px;
      color: var(--muted);
      line-height: 1.6;
    }}
    li {{ margin-bottom: 8px; }}
    .steps {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-top: 14px;
    }}
    .step {{
      background: var(--panel-2);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
    }}
    .step .num {{
      color: var(--warm);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 10px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    {body}
  </div>
</body>
</html>"""


def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    spy = CsvAdapter(ROOT / "data" / "market_data" / "spy.csv").fetch_ohlcv(
        DataRequest("SPY", "2020-01-01", "2024-12-31")
    )
    strategy = create_strategy("sma_crossover", short_window=20, long_window=60)
    backtest = BacktestEngine(BacktestConfig(initial_cash=100000)).run(spy.copy(), strategy)
    optimizer = ParameterOptimizer(OptimizationConfig(metric="sharpe"))
    optimization = optimizer.grid_search(
        strategy_class=STRATEGIES["sma_crossover"],
        param_grid={"short_window": [10, 20, 30], "long_window": [40, 60, 90]},
        data=spy.copy(),
        initial_cash=100000,
    )

    rows = spy.head(6).copy()
    rows["timestamp"] = rows["timestamp"].dt.strftime("%Y-%m-%d")
    strategy_rows = [
        ("Strategy ID", "sma_crossover"),
        ("Short Window", "20"),
        ("Long Window", "60"),
        ("Factory Call", 'create_strategy("sma_crossover", short_window=20, long_window=60)'),
        ("Best Grid Params", json.dumps(optimization.best_params, ensure_ascii=False)),
    ]
    chart = svg_line(backtest.equity["equity"].tail(220).tolist())

    data_html = page_template(
        "Get real sample market data from the repo immediately.",
        "Data",
        f"""
        <p>Users do not need to wire up a data platform first. The repository already contains free sample market data that the skill can load directly from the current directory.</p>
        <div class="panel">
          <div class="panel-inner">
            <div class="grid">
              <div class="metric"><div class="label">Data Path</div><div class="value accent">spy.csv</div></div>
              <div class="metric"><div class="label">Rows</div><div class="value">{len(spy)}</div></div>
              <div class="metric"><div class="label">Start</div><div class="value">2020-01-02</div></div>
              <div class="metric"><div class="label">End</div><div class="value">2024-12-30</div></div>
            </div>
            <div style="margin-top:20px;">{rows.to_html(index=False, border=0)}</div>
          </div>
        </div>
        """,
    )

    strategy_table = "".join(
        f"<tr><th>{label}</th><td><code>{value}</code></td></tr>" for label, value in strategy_rows
    )
    strategy_html = page_template(
        "Pick a strategy without reading the whole codebase first.",
        "Strategy",
        f"""
        <p>The public skill can point the agent to built-in strategies immediately. Users can start from the strategy name and parameters, and only inspect implementation details later if needed.</p>
        <div class="panel">
          <div class="panel-inner">
            <table>
              <tbody>
                {strategy_table}
              </tbody>
            </table>
          </div>
        </div>
        """,
    )

    backtest_html = page_template(
        "Backtest first. Read framework details later.",
        "Backtest",
        f"""
        <p>The current repository can already run a real backtest path from bundled data to final metrics. This is the part that creates immediate user confidence.</p>
        <div class="panel">
          <div class="panel-inner">
            <div class="grid">
              <div class="metric"><div class="label">Final Equity</div><div class="value good">{backtest.metrics['final_equity']:.0f}</div></div>
              <div class="metric"><div class="label">Sharpe</div><div class="value">{backtest.metrics['sharpe']:.2f}</div></div>
              <div class="metric"><div class="label">Annual Return</div><div class="value">{backtest.metrics['annual_return']:.1%}</div></div>
              <div class="metric"><div class="label">Trades</div><div class="value">{backtest.metrics['num_trades']}</div></div>
            </div>
            <div style="margin-top:20px;">{chart}</div>
          </div>
        </div>
        """,
    )

    skill_html = page_template(
        "Use the skill as the entrypoint for the whole workflow.",
        "Skill",
        """
        <p>The README should make the skill feel like the shortest path to value. Instead of asking users to study architecture first, it should show the workflow the skill unlocks.</p>
        <div class="panel">
          <div class="panel-inner">
            <div class="steps">
              <div class="step"><div class="num">Step 1</div><strong>Load skill.md</strong><p>Start from the skill, not the framework.</p></div>
              <div class="step"><div class="num">Step 2</div><strong>Get free data</strong><p>Use bundled CSVs or free adapters.</p></div>
              <div class="step"><div class="num">Step 3</div><strong>Run a strategy</strong><p>Select a built-in strategy and backtest it.</p></div>
              <div class="step"><div class="num">Step 4</div><strong>Optimize fast</strong><p>Compare parameter choices in the same workflow.</p></div>
            </div>
            <ul>
              <li>Validated in the current directory</li>
              <li>Skill-relative paths resolve correctly</li>
              <li>Data, strategy, and backtest flow all tested locally</li>
            </ul>
          </div>
        </div>
        """,
    )

    cheat_html = page_template(
        "Copy four commands and start immediately.",
        "Cheat Sheet",
        """
        <p>This is the shortest agent-friendly entrypoint for the project. Install once, then copy one command for data, one for strategy, one for results, and one for skill verification.</p>
        <div class="panel">
          <div class="panel-inner">
            <div class="steps" style="grid-template-columns: 1fr; gap: 16px;">
              <div class="step">
                <div class="num">Install</div>
                <code>python -m venv .venv && source .venv/bin/activate && pip install -e .</code>
              </div>
              <div class="step">
                <div class="num">Get Data</div>
                <code>python -c "from pathlib import Path; import pandas as pd; p=Path('data/market_data/spy.csv'); df=pd.read_csv(p); print(df.head(5).to_string(index=False))"</code>
              </div>
              <div class="step">
                <div class="num">Pick Strategy</div>
                <code>python -c "from openaitrade.strategies.factory import STRATEGIES; [print(f'{sid:24s} {cls.category:18s} {cls.name}') for sid, cls in STRATEGIES.items()]"</code>
              </div>
              <div class="step">
                <div class="num">See Results</div>
                <code>python examples/quickstart.py</code>
              </div>
              <div class="step">
                <div class="num">Start With The Skill</div>
                <code>python -m pytest -q tests/test_skill_installation.py</code>
              </div>
            </div>
          </div>
        </div>
        """,
    )

    pages = {
        "cheatsheet_snapshot.html": cheat_html,
        "data_snapshot.html": data_html,
        "strategy_snapshot.html": strategy_html,
        "backtest_snapshot.html": backtest_html,
        "skill_snapshot.html": skill_html,
    }
    for name, html in pages.items():
        path = ARTIFACTS_DIR / name
        path.write_text(html, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
