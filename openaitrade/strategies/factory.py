from openaitrade.strategies.trend.sma_crossover import SMACrossoverStrategy
from openaitrade.strategies.trend.donchian_breakout import DonchianBreakoutStrategy
from openaitrade.strategies.trend.triple_ma_filter import TripleMAFilterStrategy
from openaitrade.strategies.trend.atr_trailing_stop import ATRTrailingStopStrategy
from openaitrade.strategies.mean_reversion.bollinger_reversion import BollingerReversionStrategy
from openaitrade.strategies.mean_reversion.rsi_reversal import RSIReversalStrategy
from openaitrade.strategies.mean_reversion.zscore_reversion import ZScoreReversionStrategy
from openaitrade.strategies.momentum.topn_momentum import TopNMomentumStrategy
from openaitrade.strategies.momentum.sector_rotation import SectorRotationStrategy
from openaitrade.strategies.momentum.dual_momentum import DualMomentumStrategy
from openaitrade.strategies.momentum.low_vol_momentum import LowVolMomentumStrategy
from openaitrade.strategies.factor.multi_factor import MultiFactorRankingStrategy
from openaitrade.strategies.factor.value_factor import ValueFactorStrategy
from openaitrade.strategies.factor.quality_factor import QualityFactorStrategy
from openaitrade.strategies.factor.size_factor import SizeFactorStrategy
from openaitrade.strategies.arbitrage.pairs_trading import PairsTradingStrategy
from openaitrade.strategies.arbitrage.basket_statarb import BasketStatArbStrategy
from openaitrade.strategies.arbitrage.etf_premium import ETFPremiumStrategy
from openaitrade.strategies.arbitrage.basis_arbitrage import BasisArbitrageStrategy
from openaitrade.strategies.arbitrage.funding_rate_arbitrage import FundingRateArbitrageStrategy

_STRATEGY_CLASSES = [
    SMACrossoverStrategy, DonchianBreakoutStrategy, TripleMAFilterStrategy, ATRTrailingStopStrategy,
    BollingerReversionStrategy, RSIReversalStrategy, ZScoreReversionStrategy,
    TopNMomentumStrategy, SectorRotationStrategy, DualMomentumStrategy, LowVolMomentumStrategy,
    MultiFactorRankingStrategy, ValueFactorStrategy, QualityFactorStrategy, SizeFactorStrategy,
    PairsTradingStrategy, BasketStatArbStrategy, ETFPremiumStrategy, BasisArbitrageStrategy, FundingRateArbitrageStrategy,
]
STRATEGIES = {cls.strategy_id: cls for cls in _STRATEGY_CLASSES}

def create_strategy(strategy_id: str, **params):
    if strategy_id not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {strategy_id}. Available: {list(STRATEGIES)}")
    return STRATEGIES[strategy_id](**params)
