from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = ROOT / "artifacts"


def main():
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OpenAITrade Social Preview</title>
  <style>
    :root {
      --bg: #07111d;
      --panel: rgba(16, 27, 44, 0.92);
      --line: rgba(255,255,255,0.08);
      --ink: #eef5ff;
      --muted: #9cb3d1;
      --accent: #6eb6ff;
      --warm: #ffd166;
      --good: #4fd18b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      width: 1280px;
      height: 640px;
      overflow: hidden;
      font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(110,182,255,0.18), transparent 32%),
        radial-gradient(circle at bottom right, rgba(255,209,102,0.12), transparent 26%),
        linear-gradient(160deg, #07111d 0%, #0b1524 100%);
    }
    .wrap {
      width: 100%;
      height: 100%;
      padding: 42px 48px;
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 28px;
      align-items: stretch;
    }
    .left {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .brand {
      display: inline-flex;
      align-self: flex-start;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(110,182,255,0.35);
      color: var(--accent);
      font-size: 14px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 22px;
    }
    h1 {
      margin: 0;
      font-size: 76px;
      line-height: 0.96;
      letter-spacing: -0.045em;
      max-width: 680px;
    }
    .sub {
      margin-top: 22px;
      max-width: 640px;
      color: var(--muted);
      font-size: 26px;
      line-height: 1.35;
    }
    .tags {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-top: 28px;
      max-width: 760px;
    }
    .tag {
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 16px 18px;
      font-size: 18px;
      color: var(--ink);
    }
    .footer {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    .pill {
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--line);
      color: var(--muted);
      font-size: 16px;
    }
    .panel {
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
      border: 1px solid var(--line);
      border-radius: 28px;
      padding: 24px;
      box-shadow: 0 24px 70px rgba(0,0,0,0.3);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .panel h2 {
      margin: 0 0 14px;
      font-size: 22px;
      letter-spacing: -0.02em;
    }
    .cmd {
      border-radius: 18px;
      border: 1px solid var(--line);
      background: #0a1220;
      padding: 16px 18px;
      color: #dcecff;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 15px;
      line-height: 1.45;
      white-space: pre-wrap;
    }
    .metric-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
      margin-top: 18px;
    }
    .metric {
      border-radius: 18px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.03);
      padding: 16px;
    }
    .metric .label {
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 8px;
    }
    .metric .value {
      font-size: 26px;
      font-weight: 700;
    }
    .good { color: var(--good); }
    .accent { color: var(--accent); }
    .warm { color: var(--warm); }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="left">
      <div>
        <div class="brand">OpenAITrade Public</div>
        <h1>Start with<br>skill.md</h1>
        <div class="sub">Get free data, pick a strategy, run backtests, and see results fast.</div>
        <div class="tags">
          <div class="tag">Get data</div>
          <div class="tag">Pick strategy</div>
          <div class="tag">See results</div>
          <div class="tag">Start with the skill</div>
        </div>
      </div>
      <div class="footer">
        <div class="pill">Free data</div>
        <div class="pill">Free strategies</div>
        <div class="pill">Free workflow</div>
      </div>
    </div>
    <div class="panel">
      <div>
        <h2>Copy and start</h2>
        <div class="cmd">python -m venv .venv && source .venv/bin/activate && pip install -e .

python examples/quickstart.py

python examples/optimize.py</div>
      </div>
      <div>
        <div class="metric-grid">
          <div class="metric">
            <div class="label">Data</div>
            <div class="value accent">Bundled CSV</div>
          </div>
          <div class="metric">
            <div class="label">Strategy</div>
            <div class="value">Built-in</div>
          </div>
          <div class="metric">
            <div class="label">Backtest</div>
            <div class="value good">Ready</div>
          </div>
          <div class="metric">
            <div class="label">Workflow</div>
            <div class="value warm">Skill-first</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""
    out = ARTIFACTS_DIR / "social_preview.html"
    out.write_text(html, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
