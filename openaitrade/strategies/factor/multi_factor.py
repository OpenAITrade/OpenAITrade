import pandas as pd
import numpy as np
from openaitrade.strategies.base import Strategy


class MultiFactorRankingStrategy(Strategy):
    strategy_id = "multi_factor_ranking"
    name = "Multi-Factor Ranking"
    category = "factor"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        momentum_window = int(self.params.get("momentum_window", 120))
        vol_window = int(self.params.get("vol_window", 60))
        top_k = int(self.params.get("top_k", 5))
        out = data.copy()
        out["momentum"] = out.groupby("symbol")["close"].pct_change(momentum_window)
        out["vol"] = out.groupby("symbol")["close"].pct_change().transform(lambda s: s.rolling(vol_window).std())
        out["mom_rank"] = out.groupby("timestamp")["momentum"].rank(pct=True)
        out["lowvol_rank"] = out.groupby("timestamp")["vol"].rank(ascending=False, pct=True)
        out["score"] = 0.6 * out["mom_rank"] + 0.4 * out["lowvol_rank"]
        out["rank"] = out.groupby("timestamp")["score"].rank(ascending=False, method="first")
        out["signal"] = (out["rank"] <= top_k).astype(float)
        counts = out.groupby("timestamp")["signal"].transform("sum").replace(0, np.nan)
        out["target_weight"] = out["signal"].div(counts).fillna(0.0).astype(float)
        return out
