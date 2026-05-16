from __future__ import annotations

import pandas as pd

from .base import DataAdapter, DataRequest, normalize_ohlcv, run_with_timeout


class CCXTAdapter(DataAdapter):
    name = "ccxt"

    def __init__(self, exchange: str = "binance", timeout_seconds: float = 20.0):
        self.exchange_name = exchange
        self.timeout_seconds = timeout_seconds

    def fetch_ohlcv(self, req: DataRequest):
        try:
            import ccxt
        except ImportError as exc:
            raise ImportError("Install optional dependencies: pip install openaitrade[data]") from exc
        ex = getattr(ccxt, self.exchange_name)(
            {"enableRateLimit": True, "timeout": int(self.timeout_seconds * 1000)}
        )
        since = int(pd.Timestamp(req.start).timestamp() * 1000)
        rows = run_with_timeout(
            ex.fetch_ohlcv,
            timeout_seconds=self.timeout_seconds,
            source_name=f"{self.name}:{self.exchange_name}",
            operation="fetch_ohlcv",
            symbol=req.symbol,
            timeframe=req.timeframe,
            since=since,
            limit=1000,
        )
        df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        end = pd.Timestamp(req.end)
        df = df[df["timestamp"] <= end]
        return normalize_ohlcv(df, req.symbol, f"ccxt:{self.exchange_name}")
