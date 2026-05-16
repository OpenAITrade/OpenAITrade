import pandas as pd
from openaitrade.strategies.base import Strategy


class PairsTradingStrategy(Strategy):
    strategy_id = "pairs_trading"
    name = "Pairs Trading"
    category = "arbitrage"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        lookback = int(self.params.get("lookback", 120))
        entry_z = float(self.params.get("entry_z", 2.0))
        exit_z = float(self.params.get("exit_z", 0.5))
        symbols = list(data["symbol"].drop_duplicates())
        if len(symbols) < 2:
            raise ValueError("PairsTradingStrategy requires at least two symbols")
        a, b = symbols[:2]
        wide = data.pivot(index="timestamp", columns="symbol", values="close")[[a, b]].dropna()
        spread = wide[a] / wide[b]
        z = (spread - spread.rolling(lookback).mean()) / spread.rolling(lookback).std()
        weights = pd.DataFrame(0.0, index=wide.index, columns=[a, b])
        weights.loc[z > entry_z, [a, b]] = [-0.5, 0.5]
        weights.loc[z < -entry_z, [a, b]] = [0.5, -0.5]
        weights.loc[z.abs() < exit_z, [a, b]] = [0.0, 0.0]
        weights = weights.ffill().fillna(0)
        long = weights.stack().rename("target_weight").reset_index().rename(columns={"level_1": "symbol"})
        out = data.merge(long, on=["timestamp", "symbol"], how="left")
        out["target_weight"] = out["target_weight"].fillna(0)
        out["signal"] = out["target_weight"]
        return out
