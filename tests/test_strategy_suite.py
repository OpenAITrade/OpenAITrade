import pandas as pd

from openaitrade.backtest.engine import BacktestEngine
from openaitrade.data.base import DataRequest, SyntheticAdapter
from openaitrade.strategies.factory import STRATEGIES, create_strategy


def _build_data(strategy_id: str, category: str) -> pd.DataFrame:
    adapter = SyntheticAdapter()
    symbols = ["SPY"]

    if category in {"momentum", "factor"} or strategy_id in {"pairs_trading", "basket_statarb"}:
        symbols = ["SPY", "QQQ", "IWM", "TLT", "GLD", "BTC"]

    return pd.concat(
        [
            adapter.fetch_ohlcv(DataRequest(symbol, "2020-01-01", "2021-01-01"))
            for symbol in symbols
        ],
        ignore_index=True,
    )


def test_all_public_strategies_generate_signals_and_backtest():
    for strategy_id, strategy_cls in STRATEGIES.items():
        data = _build_data(strategy_id, strategy_cls.category)
        strategy = create_strategy(strategy_id)

        signals = strategy.generate_signals(data.copy())
        result = BacktestEngine().run(data.copy(), strategy)

        assert not signals.empty, f"{strategy_id} returned empty signals"
        assert "signal" in signals.columns, f"{strategy_id} missing signal column"
        assert "target_weight" in signals.columns, f"{strategy_id} missing target_weight column"
        assert not result.equity.empty, f"{strategy_id} returned empty equity"
        assert "sharpe" in result.metrics, f"{strategy_id} missing sharpe metric"


def test_special_field_arbitrage_strategies_trade_when_research_fields_exist():
    idx = pd.date_range("2024-01-01", periods=120, freq="B")
    base = pd.DataFrame(
        {
            "timestamp": idx,
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": [100 + (i % 7) for i in range(len(idx))],
            "volume": 1_000_000,
        }
    )

    etf = base.copy()
    etf["symbol"] = "ETF"
    etf["source"] = "synthetic"
    etf["nav"] = etf["close"] * 0.97

    basis = pd.concat(
        [
            base.assign(
                symbol="SPOT",
                source="synthetic",
                basis=[0.03 if i % 10 < 5 else -0.03 for i in range(len(base))],
            ),
            base.assign(
                symbol="PERP",
                source="synthetic",
                basis=[0.03 if i % 10 < 5 else -0.03 for i in range(len(base))],
            ),
        ],
        ignore_index=True,
    )

    funding = base.copy()
    funding["symbol"] = "BTC/USDT"
    funding["source"] = "synthetic"
    funding["funding_rate"] = [0.0005 if i % 8 < 4 else 0.0 for i in range(len(base))]

    cases = {
        "etf_premium": etf,
        "basis_arbitrage": basis,
        "funding_rate_arbitrage": funding,
    }

    for strategy_id, data in cases.items():
        strategy = create_strategy(strategy_id)
        signals = strategy.generate_signals(data.copy())
        assert (signals["target_weight"] != 0).any(), f"{strategy_id} should react to research fields"
