from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openaitrade.backtest.engine import BacktestEngine
from openaitrade.data.base import DataRequest, CsvAdapter
from openaitrade.strategies.factory import create_strategy


PATH_PATTERN = re.compile(r"`((?:\.\./)+[^`]+)`")


def _assert_skill_paths_exist(skill_path: Path):
    text = skill_path.read_text(encoding="utf-8")
    matches = PATH_PATTERN.findall(text)
    assert matches, f"No relative paths found in {skill_path}"
    for raw in matches:
        if "<strategy>" in raw or "<category>" in raw or "*.py" in raw:
            continue
        resolved = (skill_path.parent / raw).resolve()
        assert resolved.exists(), f"{skill_path.name} references missing path: {raw}"


def test_public_skill_paths_resolve():
    _assert_skill_paths_exist(ROOT / "skills" / "openaitrade" / "SKILL.md")


def test_zh_skill_paths_resolve():
    _assert_skill_paths_exist(ROOT / "zh" / "skills" / "openaitrade" / "SKILL.md")


def test_en_skill_paths_resolve():
    _assert_skill_paths_exist(ROOT / "en" / "skills" / "openaitrade" / "SKILL.md")


def test_skill_advertised_workflow_runs_from_current_directory():
    data_path = ROOT / "data" / "market_data" / "spy.csv"
    data = CsvAdapter(data_path).fetch_ohlcv(
        DataRequest(symbol="SPY", start="2018-01-01", end="2024-12-31")
    )
    strategy = create_strategy("sma_crossover", short_window=20, long_window=60)
    result = BacktestEngine().run(data, strategy)

    assert not result.equity.empty
    assert result.metrics["final_equity"] > 0
    assert "sharpe" in result.metrics
