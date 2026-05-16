from pathlib import Path

import pandas as pd

from openaitrade.backtest.engine import BacktestEngine
from openaitrade.data.base import CsvAdapter, DataRequest
from openaitrade.strategies.factory import STRATEGIES, create_strategy


MARKET_DATA_DIR = Path("data/market_data")


def _load_symbol(symbol: str) -> pd.DataFrame:
    path = MARKET_DATA_DIR / f"{symbol.lower()}.csv"
    return CsvAdapter(path).fetch_ohlcv(
        DataRequest(symbol=symbol.upper(), start="2018-01-01", end="2024-12-31")
    )


def _build_real_dataset(strategy_id: str, category: str) -> pd.DataFrame:
    if strategy_id == "pairs_trading":
        symbols = ["spy", "qqq"]
    elif strategy_id in {"basket_statarb", "topn_momentum", "sector_rotation", "dual_momentum", "low_vol_momentum",
                         "multi_factor_ranking", "value_factor", "quality_factor", "size_factor"} or category in {"momentum", "factor"}:
        symbols = ["spy", "qqq", "iwm", "tlt", "gld", "btc", "eth"]
    elif strategy_id in {"basis_arbitrage", "funding_rate_arbitrage"}:
        symbols = ["btc", "eth"]
    else:
        symbols = ["spy"]

    return pd.concat([_load_symbol(symbol) for symbol in symbols], ignore_index=True)


def test_all_strategies_run_on_real_market_data_bundle():
    for strategy_id, strategy_cls in STRATEGIES.items():
        if strategy_id == "etf_premium":
            continue

        data = _build_real_dataset(strategy_id, strategy_cls.category)
        strategy = create_strategy(strategy_id)
        signals = strategy.generate_signals(data.copy())
        result = BacktestEngine().run(data.copy(), strategy)

        assert not signals.empty, f"{strategy_id} returned empty signals on real bundled data"
        assert "signal" in signals.columns, f"{strategy_id} missing signal column"
        assert "target_weight" in signals.columns, f"{strategy_id} missing target_weight column"
        assert not result.equity.empty, f"{strategy_id} returned empty equity"
        assert result.metrics["final_equity"] > 0, f"{strategy_id} produced non-positive equity"
        assert -1.0 <= result.metrics["max_drawdown"] <= 0.0, f"{strategy_id} drawdown out of range"

