from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class LowVolMomentumStrategy(Strategy):
    strategy_id = "low_vol_momentum"
    name = "Low Volatility Momentum"
    category = "momentum"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        m=int(self.params.get('momentum_window',120)); v=int(self.params.get('vol_window',60)); top_k=int(self.params.get('top_k',5))
        out=data.copy().sort_values(['timestamp','symbol'])
        close=out.pivot(index='timestamp', columns='symbol', values='close').sort_index().ffill()
        score=close.pct_change(m) - close.pct_change().rolling(v).std()*10
        weights=pd.DataFrame(0.0,index=close.index,columns=close.columns)
        for ts,row in score.iterrows():
            winners=row.dropna().sort_values(ascending=False).head(top_k)
            if len(winners): weights.loc[ts,winners.index]=1/len(winners)
        merged=out.merge(weights.stack().rename('target_weight').reset_index(), on=['timestamp','symbol'], how='left')
        merged['target_weight']=merged['target_weight'].fillna(0.0); merged['signal']=merged['target_weight']
        return merged
