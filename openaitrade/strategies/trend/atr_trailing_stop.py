from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class ATRTrailingStopStrategy(Strategy):
    strategy_id = "atr_trailing_stop"
    name = "ATR Trend Following Trailing Stop"
    category = "trend_following"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        ma=int(self.params.get('ma_window',50)); atr_n=int(self.params.get('atr_window',14)); mult=float(self.params.get('atr_multiplier',3.0))
        out=data.copy().sort_values(['symbol','timestamp'])
        parts=[]
        for _, d in out.groupby('symbol'):
            d=d.copy()
            prev=d['close'].shift(1)
            tr=pd.concat([(d.high-d.low).abs(),(d.high-prev).abs(),(d.low-prev).abs()],axis=1).max(axis=1)
            atr=tr.rolling(atr_n).mean()
            trend=d.close>d.close.rolling(ma).mean()
            trail=(d.close- mult*atr).cummax()
            d['atr']=atr; d['trail_stop']=trail
            d['signal']=(trend & (d.close>trail)).astype(float)
            d['target_weight']=d['signal']
            parts.append(d)
        return pd.concat(parts, ignore_index=True)
