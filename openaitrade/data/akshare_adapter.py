from __future__ import annotations

from .base import DataAdapter, DataRequest, normalize_ohlcv, run_with_timeout


class AKShareAdapter(DataAdapter):
    name = "akshare"

    def __init__(self, timeout_seconds: float = 20.0):
        self.timeout_seconds = timeout_seconds

    def fetch_ohlcv(self, req: DataRequest):
        try:
            import akshare as ak
        except ImportError as exc:
            raise ImportError("Install optional dependencies: pip install openaitrade[data]") from exc
        period = "daily" if req.timeframe == "1d" else req.timeframe
        df = run_with_timeout(
            ak.stock_zh_a_hist,
            timeout_seconds=self.timeout_seconds,
            source_name=self.name,
            operation="fetch_ohlcv",
            symbol=req.symbol,
            period=period,
            start_date=req.start.replace("-", ""),
            end_date=req.end.replace("-", ""),
            adjust="qfq",
        )
        mapping = {"日期": "timestamp", "开盘": "open", "最高": "high", "最低": "low", "收盘": "close", "成交量": "volume"}
        df = df.rename(columns=mapping)
        return normalize_ohlcv(df, req.symbol, self.name)
