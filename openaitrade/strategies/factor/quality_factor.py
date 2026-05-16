from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class QualityFactorStrategy(Strategy):
    strategy_id = "quality_factor"
    name = "Quality Factor Ranking"
    category = "factor"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        top_k=int(self.params.get('top_k',10)); window=int(self.params.get('window',120))
        out=data.copy().sort_values(['timestamp','symbol'])
        close=out.pivot(index='timestamp', columns='symbol', values='close').sort_index().ffill()
        ret=close.pct_change(); quality=ret.rolling(window).mean()/ret.rolling(window).std()
        weights=pd.DataFrame(0.0,index=close.index,columns=close.columns)
        for ts,row in quality.iterrows():
            picks=row.dropna().sort_values(ascending=False).head(top_k)
            if len(picks): weights.loc[ts,picks.index]=1/len(picks)
        return out.merge(weights.stack().rename('target_weight').reset_index(), on=['timestamp','symbol'], how='left').assign(signal=lambda x:x.target_weight.fillna(0), target_weight=lambda x:x.target_weight.fillna(0))
