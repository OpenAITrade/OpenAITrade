import pandas as pd

from openaitrade.backtest.metrics import compute_metrics


def test_compute_metrics_handles_flat_equity_without_nan():
    equity = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "equity": [100000.0, 100000.0, 100000.0],
        }
    )
    metrics = compute_metrics(equity, trades=pd.DataFrame())

    assert metrics["total_return"] == 0.0
    assert metrics["annual_volatility"] == 0.0
    assert metrics["sharpe"] == 0.0
    assert metrics["sortino"] == 0.0
    assert metrics["max_drawdown"] == 0.0
