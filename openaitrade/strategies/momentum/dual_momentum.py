from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class DualMomentumStrategy(Strategy):
    strategy_id = "dual_momentum"
    name = "Dual Momentum Rotation"
    category = "momentum"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        lookback=int(self.params.get('lookback',252)); top_k=int(self.params.get('top_k',1)); threshold=float(self.params.get('absolute_threshold',0.0))
        out=data.copy().sort_values(['timestamp','symbol'])
        close=out.pivot(index='timestamp', columns='symbol', values='close').sort_index().ffill()
        mom=close.pct_change(lookback)
        weights=pd.DataFrame(0.0,index=close.index,columns=close.columns)
        for ts,row in mom.iterrows():
            winners=row[row>threshold].sort_values(ascending=False).head(top_k)
            if len(winners): weights.loc[ts,winners.index]=1/len(winners)
        merged=out.merge(weights.stack().rename('target_weight').reset_index(), on=['timestamp','symbol'], how='left')
        merged['target_weight']=merged['target_weight'].fillna(0.0); merged['signal']=merged['target_weight']
        return merged
