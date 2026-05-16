from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class ZScoreReversionStrategy(Strategy):
    strategy_id = "zscore_reversion"
    name = "Rolling Z-Score Mean Reversion"
    category = "mean_reversion"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        window=int(self.params.get('window',60)); entry=float(self.params.get('entry_z',-2)); exit_z=float(self.params.get('exit_z',0))
        out=data.copy().sort_values(['symbol','timestamp'])
        g=out.groupby('symbol')['close']
        mean=g.transform(lambda x:x.rolling(window).mean()); std=g.transform(lambda x:x.rolling(window).std())
        out['zscore']=(out.close-mean)/std
        out['signal']=(out['zscore']<entry).astype(float)
        # simple long-only version exits when zscore >= exit_z
        out.loc[out['zscore']>=exit_z, 'signal']=0.0
        out['target_weight']=out['signal']
        return out
