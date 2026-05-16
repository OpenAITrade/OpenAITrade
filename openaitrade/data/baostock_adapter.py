from __future__ import annotations

import pandas as pd

from .base import DataAdapter, DataRequest, normalize_ohlcv, DataSourceError, run_with_timeout


class BaoStockAdapter(DataAdapter):
    name = "baostock"

    def __init__(self, timeout_seconds: float = 20.0):
        self.timeout_seconds = timeout_seconds

    def fetch_ohlcv(self, req: DataRequest):
        try:
            import baostock as bs
        except ImportError as exc:
            raise ImportError("Install optional dependencies: pip install openaitrade[data]") from exc

        def _query_history():
            login_result = bs.login()
            if getattr(login_result, "error_code", "0") != "0":
                raise DataSourceError(
                    f"baostock login failed: {login_result.error_code} {login_result.error_msg}"
                )
            try:
                rs = bs.query_history_k_data_plus(
                    req.symbol,
                    "date,open,high,low,close,volume",
                    start_date=req.start,
                    end_date=req.end,
                    frequency="d",
                    adjustflag="2",
                )
                rows = []
                while rs.next():
                    rows.append(rs.get_row_data())
                return pd.DataFrame(rows, columns=rs.fields)
            finally:
                try:
                    bs.logout()
                except Exception:
                    pass

        df = run_with_timeout(
            _query_history,
            timeout_seconds=self.timeout_seconds,
            source_name=self.name,
            operation="fetch_ohlcv",
        )
        df = df.rename(columns={"date": "timestamp"})
        return normalize_ohlcv(df, req.symbol, self.name)
