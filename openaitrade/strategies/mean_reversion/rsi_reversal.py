import pandas as pd
from openaitrade.strategies.base import Strategy


def rsi(series: pd.Series, window: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = (-delta.clip(upper=0)).rolling(window).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


class RSIReversalStrategy(Strategy):
    strategy_id = "rsi_reversal"
    name = "RSI Reversal"
    category = "mean_reversion"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        window = int(self.params.get("rsi_window", 14))
        lower = float(self.params.get("lower", 30))
        upper = float(self.params.get("upper", 70))
        out = data.copy()
        out["rsi"] = out.groupby("symbol")["close"].transform(lambda s: rsi(s, window))
        out["signal"] = 0.0
        out.loc[out["rsi"] < lower, "signal"] = 1.0
        out.loc[out["rsi"] > upper, "signal"] = 0.0
        out["signal"] = out.groupby("symbol")["signal"].ffill().fillna(0)
        out["target_weight"] = out["signal"]
        return out
