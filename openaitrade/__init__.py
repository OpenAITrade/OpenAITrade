"""
Public OpenAITrade subset.

This package intentionally exposes the public-safe research modules that are
useful to publish as open-source assets: free data access, free strategies,
backtesting, and optimization workflow components.
"""

__version__ = "1.0.0"

from openaitrade.data.factory import ADAPTERS, create_data_adapter
from openaitrade.backtest.engine import BacktestConfig, BacktestEngine, BacktestResult
from openaitrade.strategies.factory import STRATEGIES, create_strategy
from openaitrade.tools import OptimizationConfig, OptimizationResult, ParameterOptimizer

__all__ = [
    "ADAPTERS",
    "STRATEGIES",
    "BacktestConfig",
    "BacktestEngine",
    "BacktestResult",
    "OptimizationConfig",
    "OptimizationResult",
    "ParameterOptimizer",
    "create_data_adapter",
    "create_strategy",
]
