from pathlib import Path

import pandas as pd

from openaitrade.data.base import CsvAdapter, DataRequest, SyntheticAdapter
from openaitrade.data.factory import ADAPTERS, create_data_adapter


def test_all_public_csv_samples_normalize_correctly():
    base = Path("data/market_data")
    files = sorted(base.glob("*.csv"))

    assert files, "Expected bundled sample CSV files"

    for path in files:
        df = CsvAdapter(path).fetch_ohlcv(
            DataRequest(symbol=path.stem.upper(), start="2000-01-01", end="2030-01-01")
        )
        assert not df.empty, f"{path.name} should not be empty"
        assert list(df.columns) == [
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "symbol",
            "source",
        ]
        assert df["timestamp"].is_monotonic_increasing


def test_synthetic_adapter_returns_expected_columns():
    df = SyntheticAdapter().fetch_ohlcv(DataRequest("SPY", "2020-01-01", "2020-12-31"))
    assert not df.empty
    assert {"timestamp", "open", "high", "low", "close", "volume", "symbol", "source"} <= set(
        df.columns
    )


def test_yfinance_adapter_flattens_multiindex_columns(monkeypatch):
    sample = pd.DataFrame(
        {
            ("Adj Close", "AAPL"): [10.0, 11.0],
            ("Close", "AAPL"): [10.0, 11.0],
            ("High", "AAPL"): [10.5, 11.5],
            ("Low", "AAPL"): [9.5, 10.5],
            ("Open", "AAPL"): [9.8, 10.8],
            ("Volume", "AAPL"): [1000, 1200],
        },
        index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
    )
    sample.index.name = "Date"

    class FakeYF:
        @staticmethod
        def download(*args, **kwargs):
            return sample

    import sys

    sys.modules["yfinance"] = FakeYF()
    try:
        df = create_data_adapter("yfinance").fetch_ohlcv(
            DataRequest("AAPL", "2024-01-02", "2024-01-04")
        )
    finally:
        sys.modules.pop("yfinance", None)

    assert not df.empty
    assert list(df.columns) == [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "symbol",
        "source",
    ]


def test_public_adapter_registry_contains_free_data_sources():
    for name in ["synthetic", "csv", "yfinance", "akshare", "baostock", "ccxt", "openbb"]:
        assert name in ADAPTERS
