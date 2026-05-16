from __future__ import annotations

import pandas as pd

from openaitrade.strategies.base import Strategy


class SizeFactorStrategy(Strategy):
    strategy_id = "size_factor"
    name = "Size Factor Ranking"
    category = "factor"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        requested_top_k = int(self.params.get("top_k", 3))
        min_liquidity = float(self.params.get("min_liquidity", 5_000_000))
        liquidity_window = int(self.params.get("liquidity_window", 20))
        trend_window = int(self.params.get("trend_window", 126))
        out = data.copy().sort_values(["timestamp", "symbol"])

        out["dollar_volume"] = out["close"] * out["volume"]
        out["liquidity_proxy"] = out.groupby("symbol")["dollar_volume"].transform(
            lambda s: s.rolling(liquidity_window).median()
        )
        out["trend_filter"] = out.groupby("symbol")["close"].pct_change(trend_window)

        weights: list[dict] = []
        for ts, frame in out.groupby("timestamp"):
            eligible = frame[(frame["liquidity_proxy"] >= min_liquidity) & (frame["trend_filter"] > 0)].copy()
            if eligible.empty:
                eligible = frame[frame["liquidity_proxy"] >= min_liquidity].copy()

            effective_top_k = min(requested_top_k, max(1, len(eligible) // 2 or len(eligible)))
            picks = eligible.sort_values("liquidity_proxy").head(effective_top_k)["symbol"].tolist()

            for sym in frame["symbol"].unique():
                weights.append(
                    {
                        "timestamp": ts,
                        "symbol": sym,
                        "target_weight": (1.0 / len(picks) if sym in picks and picks else 0.0),
                    }
                )

        merged = out.merge(pd.DataFrame(weights), on=["timestamp", "symbol"], how="left")
        merged["target_weight"] = merged["target_weight"].fillna(0.0).astype(float)
        merged["signal"] = merged["target_weight"]
        return merged
