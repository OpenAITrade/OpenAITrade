from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class TripleMAFilterStrategy(Strategy):
    strategy_id = "triple_ma_filter"
    name = "Triple Moving Average Trend Filter"
    category = "trend_following"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        short=int(self.params.get('short_window',10)); mid=int(self.params.get('mid_window',30)); long=int(self.params.get('long_window',120))
        out=data.copy().sort_values(['symbol','timestamp'])
        g=out.groupby('symbol')['close']
        out['ma_s']=g.transform(lambda x:x.rolling(short).mean())
        out['ma_m']=g.transform(lambda x:x.rolling(mid).mean())
        out['ma_l']=g.transform(lambda x:x.rolling(long).mean())
        out['signal']=((out.ma_s>out.ma_m)&(out.ma_m>out.ma_l)).astype(float)
        out['target_weight']=out['signal']
        return out
