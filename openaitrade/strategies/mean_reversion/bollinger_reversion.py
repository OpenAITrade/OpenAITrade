import pandas as pd
from openaitrade.strategies.base import Strategy


class BollingerReversionStrategy(Strategy):
    strategy_id = "bollinger_reversion"
    name = "Bollinger Mean Reversion"
    category = "mean_reversion"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        window = int(self.params.get("window", 20))
        num_std = float(self.params.get("num_std", 2))
        out = data.copy()
        g = out.groupby("symbol")["close"]
        out["mid"] = g.transform(lambda s: s.rolling(window).mean())
        out["std"] = g.transform(lambda s: s.rolling(window).std())
        out["lower"] = out["mid"] - num_std * out["std"]
        out["upper"] = out["mid"] + num_std * out["std"]
        out["signal"] = 0.0
        out.loc[out["close"] < out["lower"], "signal"] = 1.0
        out.loc[out["close"] > out["mid"], "signal"] = 0.0
        out["signal"] = out.groupby("symbol")["signal"].ffill().fillna(0)
        out["target_weight"] = out["signal"]
        return out
