from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class FundingRateArbitrageStrategy(Strategy):
    strategy_id = "funding_rate_arbitrage"
    name = "Crypto Funding Rate Arbitrage Research Strategy"
    category = "arbitrage"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        min_rate=float(self.params.get('min_funding_rate',0.00002))
        out=data.copy().sort_values(['timestamp','symbol'])
        if 'funding_rate' in out.columns:
            out['target_weight']=(out['funding_rate']>min_rate).astype(float)
        else:
            out['target_weight']=0.0
        out['signal']=out['target_weight']
        return out
