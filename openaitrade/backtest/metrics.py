from __future__ import annotations

import numpy as np
import pandas as pd


def compute_metrics(equity: pd.DataFrame, trades: pd.DataFrame | None = None) -> dict:
    eq = equity.copy().dropna(subset=["equity"])
    returns = eq["equity"].pct_change().dropna()
    total_return = eq["equity"].iloc[-1] / eq["equity"].iloc[0] - 1 if len(eq) > 1 else 0
    years = max((eq["timestamp"].iloc[-1] - eq["timestamp"].iloc[0]).days / 365.25, 1e-9)
    cagr = (1 + total_return) ** (1 / years) - 1 if total_return > -1 else -1
    vol = returns.std() * np.sqrt(252) if not returns.empty else 0
    vol = 0 if pd.isna(vol) else float(vol)
    sharpe = float((returns.mean() * 252) / vol) if vol else 0.0
    downside = returns[returns < 0].std() * np.sqrt(252) if not returns.empty else 0
    downside = 0 if pd.isna(downside) else float(downside)
    sortino = float((returns.mean() * 252) / downside) if downside else 0.0
    roll_max = eq["equity"].cummax()
    drawdown = eq["equity"] / roll_max - 1
    max_dd = float(drawdown.min()) if not drawdown.empty else 0
    calmar = cagr / abs(max_dd) if max_dd else 0
    num_trades = 0 if trades is None or trades.empty else len(trades)
    return {
        "total_return": float(total_return),
        "annual_return": float(cagr),
        "annual_volatility": float(vol),
        "sharpe": float(sharpe),
        "sortino": float(sortino),
        "calmar": float(calmar),
        "max_drawdown": max_dd,
        "num_trades": int(num_trades),
        "final_equity": float(eq["equity"].iloc[-1]),
    }
