from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class BasisArbitrageStrategy(Strategy):
    strategy_id = "basis_arbitrage"
    name = "Spot-Futures Basis Arbitrage Research Strategy"
    category = "arbitrage"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        threshold=float(self.params.get('basis_threshold',0.0005))
        out=data.copy().sort_values(['timestamp','symbol'])
        # Expected symbols contain SPOT and FUT/PERP. Demo creates pairwise long/short if basis is available.
        if 'basis' in out.columns:
            out['target_weight']=(-out['basis']).where(out['basis'].abs()>threshold,0).clip(-1,1)
        else:
            out['target_weight']=0.0
        out['signal']=out['target_weight']
        return out
