from __future__ import annotations

import numpy as np
import pandas as pd

from openaitrade.strategies.base import Strategy


class SectorRotationStrategy(Strategy):
    strategy_id = "sector_rotation"
    name = "Sector Rotation"
    category = "momentum"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        lookback = int(self.params.get("lookback", 126))
        top_k = int(self.params.get("top_k", 2))
        absolute_threshold = float(self.params.get("absolute_threshold", 0.03))
        trend_window = int(self.params.get("trend_window", 200))
        out = data.copy().sort_values(["timestamp", "symbol"])

        close = out.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()
        momentum = close.pct_change(lookback)
        trend_ok = close > close.rolling(trend_window).mean()
        month_key = close.index.to_period("M")
        rebalance_dates = close.index.to_series().groupby(month_key).last()

        weights = pd.DataFrame(0.0, index=close.index, columns=close.columns)
        current = pd.Series(0.0, index=close.columns, dtype=float)

        for ts in close.index:
            if ts in rebalance_dates.values:
                row = momentum.loc[ts]
                eligible = row[(row > absolute_threshold) & trend_ok.loc[ts]].dropna()
                picks = eligible.sort_values(ascending=False).head(top_k)
                current = pd.Series(0.0, index=close.columns, dtype=float)
                if len(picks) > 0:
                    current.loc[picks.index] = 1.0 / len(picks)
            weights.loc[ts] = current

        merged = out.merge(
            weights.stack().rename("target_weight").reset_index(),
            on=["timestamp", "symbol"],
            how="left",
        )
        merged["target_weight"] = merged["target_weight"].fillna(0.0).astype(float)
        merged["signal"] = merged["target_weight"]
        return merged
