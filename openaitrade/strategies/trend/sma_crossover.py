import pandas as pd
from openaitrade.strategies.base import Strategy


class SMACrossoverStrategy(Strategy):
    strategy_id = "sma_crossover"
    name = "SMA Crossover"
    category = "trend_following"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        short = int(self.params.get("short_window", 20))
        long = int(self.params.get("long_window", 60))
        out = data.copy()
        out["sma_short"] = out.groupby("symbol")["close"].transform(lambda s: s.rolling(short).mean())
        out["sma_long"] = out.groupby("symbol")["close"].transform(lambda s: s.rolling(long).mean())
        out["signal"] = (out["sma_short"] > out["sma_long"]).astype(float)
        out["target_weight"] = out["signal"]
        return out
