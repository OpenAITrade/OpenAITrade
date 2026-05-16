from __future__ import annotations
from openaitrade.data.base import DataAdapter, DataRequest, normalize_ohlcv

class OpenBBAdapter(DataAdapter):
    name='openbb'
    def fetch_ohlcv(self, req: DataRequest):
        try:
            from openbb import obb
        except Exception as e:
            raise ImportError('Install openbb to use OpenBBAdapter') from e
        df=obb.equity.price.historical(req.symbol, start_date=req.start, end_date=req.end).to_df()
        return normalize_ohlcv(df, req.symbol, self.name)
