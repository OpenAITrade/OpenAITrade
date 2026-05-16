from openaitrade.data.base import DataRequest, SyntheticAdapter
from openaitrade.data.factory import ADAPTERS, create_data_adapter
from openaitrade.strategies.factory import STRATEGIES, create_strategy


def test_public_bundle_contains_expected_data_adapters():
    assert "synthetic" in ADAPTERS
    assert "csv" in ADAPTERS
    assert "yfinance" in ADAPTERS
    assert create_data_adapter("synthetic").name == "synthetic"


def test_public_bundle_contains_strategy_catalog():
    assert len(STRATEGIES) >= 20
    assert "sma_crossover" in STRATEGIES
    assert "pairs_trading" in STRATEGIES


def test_strategy_generates_signals_on_synthetic_data():
    adapter = SyntheticAdapter()
    data = adapter.fetch_ohlcv(DataRequest("SPY", "2020-01-01", "2021-01-01"))
    strategy = create_strategy("sma_crossover", short_window=5, long_window=20)
    signals = strategy.generate_signals(data)

    assert not signals.empty
    assert "signal" in signals.columns

