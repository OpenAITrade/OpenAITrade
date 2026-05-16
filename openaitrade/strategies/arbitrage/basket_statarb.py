from __future__ import annotations
import pandas as pd
from openaitrade.strategies.base import Strategy

class BasketStatArbStrategy(Strategy):
    strategy_id = "basket_statarb"
    name = "Basket Statistical Arbitrage"
    category = "arbitrage"
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        lookback=int(self.params.get('lookback',120)); entry=float(self.params.get('entry_z',1.5))
        out=data.copy().sort_values(['timestamp','symbol'])
        close=out.pivot(index='timestamp', columns='symbol', values='close').sort_index().ffill()
        norm=close/close.rolling(lookback).mean()-1
        z=(norm.sub(norm.mean(axis=1), axis=0)).div(norm.std(axis=1).replace(0,pd.NA),axis=0)
        weights=pd.DataFrame(0.0,index=close.index,columns=close.columns)
        weights[z<-entry]=1; weights[z>entry]=-1
        denom=weights.abs().sum(axis=1).replace(0,1); weights=weights.div(denom,axis=0)
        return out.merge(weights.stack().rename('target_weight').reset_index(), on=['timestamp','symbol'], how='left').assign(signal=lambda x:x.target_weight.fillna(0), target_weight=lambda x:x.target_weight.fillna(0))
