from openaitrade.backtest.engine import BacktestEngine
from openaitrade.data.base import DataRequest, SyntheticAdapter
from openaitrade.strategies.factory import STRATEGIES, create_strategy
from openaitrade.tools import OptimizationConfig, ParameterOptimizer


def test_public_workflow_runs_backtest():
    data = SyntheticAdapter().fetch_ohlcv(DataRequest("SPY", "2020-01-01", "2021-01-01"))
    strategy = create_strategy("sma_crossover", short_window=5, long_window=20)
    result = BacktestEngine().run(data, strategy)

    assert not result.equity.empty
    assert "sharpe" in result.metrics


def test_public_workflow_runs_parameter_optimization():
    data = SyntheticAdapter().fetch_ohlcv(DataRequest("SPY", "2020-01-01", "2021-01-01"))
    optimizer = ParameterOptimizer(OptimizationConfig(metric="sharpe"))
    result = optimizer.grid_search(
        strategy_class=STRATEGIES["sma_crossover"],
        param_grid={"short_window": [5, 10], "long_window": [20, 30]},
        data=data,
    )

    assert result.total_combinations == 4
    assert result.evaluated_count >= 1
    assert isinstance(result.best_params, dict)
