import pandas as pd
import numpy as np
from openaitrade.strategies.base import Strategy


class TopNMomentumStrategy(Strategy):
    strategy_id = "topn_momentum"
    name = "Top-N Cross Sectional Momentum"
    category = "momentum"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        lookback = int(self.params.get("lookback", 120))
        top_k = int(self.params.get("top_k", 3))
        out = data.copy()
        out["momentum"] = out.groupby("symbol")["close"].pct_change(lookback)
        out["rank"] = out.groupby("timestamp")["momentum"].rank(ascending=False, method="first")
        out["signal"] = (out["rank"] <= top_k).astype(float)
        counts = out.groupby("timestamp")["signal"].transform("sum").replace(0, np.nan)
        out["target_weight"] = out["signal"].div(counts).fillna(0.0).astype(float)
        return out
