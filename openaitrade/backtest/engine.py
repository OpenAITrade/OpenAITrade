from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from .metrics import compute_metrics


@dataclass
class BacktestConfig:
    initial_cash: float = 100000.0
    commission_rate: float = 0.0005
    slippage_rate: float = 0.0002


@dataclass
class BacktestResult:
    equity: pd.DataFrame
    trades: pd.DataFrame
    positions: pd.DataFrame
    metrics: dict


class BacktestEngine:
    """Simple daily close-to-close vectorized portfolio backtester.

    Signals are generated at close[t], positions are applied from close[t+1].
    This avoids obvious look-ahead bias for daily-bar research.
    """

    def __init__(self, config: BacktestConfig | None = None):
        self.config = config or BacktestConfig()

    def run(self, data: pd.DataFrame, strategy) -> BacktestResult:
        required = {"timestamp", "symbol", "close"}
        missing = required - set(data.columns)
        if missing:
            raise ValueError(f"Backtest data missing columns: {missing}")

        data = data.copy().sort_values(["timestamp", "symbol"])
        sig = strategy.generate_signals(data)
        if "target_weight" not in sig.columns:
            sig["target_weight"] = sig.get("signal", 0.0)

        close = sig.pivot(index="timestamp", columns="symbol", values="close").sort_index().ffill()
        weights = sig.pivot(index="timestamp", columns="symbol", values="target_weight").reindex(close.index).fillna(0)
        weights = weights.div(weights.abs().sum(axis=1).clip(lower=1), axis=0)
        shifted = weights.shift(1).fillna(0)
        asset_returns = close.pct_change().fillna(0)
        turnover = weights.diff().abs().sum(axis=1).fillna(weights.abs().sum(axis=1))
        costs = turnover * (self.config.commission_rate + self.config.slippage_rate)
        portfolio_returns = (shifted * asset_returns).sum(axis=1) - costs
        equity = self.config.initial_cash * (1 + portfolio_returns).cumprod()
        equity_df = pd.DataFrame({"timestamp": equity.index, "equity": equity.values, "returns": portfolio_returns.values})

        trades = []
        prev_w = pd.Series(0.0, index=weights.columns)
        for ts, row in weights.iterrows():
            diff = row - prev_w
            for sym, delta in diff[diff.abs() > 1e-9].items():
                trades.append({
                    "timestamp": ts,
                    "symbol": sym,
                    "side": "buy" if delta > 0 else "sell",
                    "target_weight": row[sym],
                    "delta_weight": delta,
                    "price": close.loc[ts, sym],
                    "reason": strategy.strategy_id,
                })
            prev_w = row
        trades_df = pd.DataFrame(trades)
        positions_df = weights.stack().rename("target_weight").reset_index()
        metrics = compute_metrics(equity_df, trades_df)
        metrics.update({"strategy_id": strategy.strategy_id, "strategy_name": strategy.name})
        return BacktestResult(equity_df, trades_df, positions_df, metrics)

    @staticmethod
    def save(result: BacktestResult, output_dir: str | Path) -> None:
        import json

        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        result.equity.to_csv(path / "equity_curve.csv", index=False)
        result.trades.to_csv(path / "trades.csv", index=False)
        result.positions.to_csv(path / "positions.csv", index=False)
        with open(path / "metrics.json", "w", encoding="utf-8") as f:
            json.dump(result.metrics, f, ensure_ascii=False, indent=2)
