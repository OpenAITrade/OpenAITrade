import pandas as pd
from openaitrade.strategies.base import Strategy


class DonchianBreakoutStrategy(Strategy):
    strategy_id = "donchian_breakout"
    name = "Donchian Breakout"
    category = "trend_following"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        entry = int(self.params.get("entry_window", 20))
        exit_ = int(self.params.get("exit_window", 10))
        out = data.copy()
        g = out.groupby("symbol")
        out["entry_high"] = g["high"].transform(lambda s: s.shift(1).rolling(entry).max())
        out["exit_low"] = g["low"].transform(lambda s: s.shift(1).rolling(exit_).min())
        out["raw"] = 0
        out.loc[out["close"] > out["entry_high"], "raw"] = 1
        out.loc[out["close"] < out["exit_low"], "raw"] = 0
        out["signal"] = out.groupby("symbol")["raw"].ffill().fillna(0).astype(float)
        out["target_weight"] = out["signal"]
        return out
