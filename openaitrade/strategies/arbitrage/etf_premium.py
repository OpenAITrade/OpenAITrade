from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class ETFPremiumStrategy(Strategy):
    strategy_id = "etf_premium"
    name = "ETF Premium/Discount Research Strategy"
    category = "arbitrage"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        threshold=float(self.params.get('premium_threshold',0.01))
        out=data.copy().sort_values(['symbol','timestamp'])
        # Requires optional nav column. Without NAV, stays flat and remains safe.
        if 'nav' in out.columns:
            out['premium']=(out['close']/out['nav'])-1
            out['target_weight']=(-out['premium']).where(out['premium'].abs()>threshold,0).clip(-1,1)
        else:
            out['premium']=0.0; out['target_weight']=0.0
        out['signal']=out['target_weight']
        return out
