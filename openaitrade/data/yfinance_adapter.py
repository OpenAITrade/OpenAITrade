from __future__ import annotations

import pandas as pd

from .base import DataAdapter, DataRequest, normalize_ohlcv


class YFinanceAdapter(DataAdapter):
    name = "yfinance"

    def fetch_ohlcv(self, req: DataRequest):
        try:
            import yfinance as yf
        except ImportError as exc:
            raise ImportError("Install optional dependencies: pip install openaitrade[data]") from exc
        df = yf.download(
            req.symbol,
            start=req.start,
            end=req.end,
            interval=req.timeframe,
            progress=False,
            auto_adjust=False,
        )
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [str(level0).lower() for level0, *_ in df.columns.to_flat_index()]
        return normalize_ohlcv(df, req.symbol, self.name)
