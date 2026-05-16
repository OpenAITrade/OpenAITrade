from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openaitrade.backtest.engine import BacktestConfig
from openaitrade.data.base import DataRequest, SyntheticAdapter
from openaitrade.strategies.factory import STRATEGIES
from openaitrade.tools import OptimizationConfig, ParameterOptimizer


def main():
    adapter = SyntheticAdapter()
    data = adapter.fetch_ohlcv(DataRequest("SPY", "2020-01-01", "2021-01-01"))
    optimizer = ParameterOptimizer(OptimizationConfig(metric="sharpe"))
    result = optimizer.grid_search(
        strategy_class=STRATEGIES["sma_crossover"],
        param_grid={"short_window": [5, 10, 20], "long_window": [30, 60]},
        data=data,
        initial_cash=BacktestConfig().initial_cash,
    )
    print("best_params =", result.best_params)
    print("best_score =", result.best_score)


if __name__ == "__main__":
    main()

