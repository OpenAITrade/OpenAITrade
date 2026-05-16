# Backtesting

The default engine is a simple vectorized daily-bar research engine.

Important assumptions:

- Signals are generated from close[t].
- Positions are applied from close[t+1] by shifting target weights one bar.
- Transaction cost = turnover × (commission_rate + slippage_rate).
- Target weights are normalized so gross exposure does not exceed 1 by default.

Output files:

- `equity_curve.csv`
- `trades.csv`
- `positions.csv`
- `metrics.json`
- `report.html`
- PNG charts when matplotlib is available
