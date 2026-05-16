from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class StrategyContext:
    cash: float = 100000.0
    params: dict[str, Any] = field(default_factory=dict)


class Strategy:
    strategy_id = "base"
    name = "Base Strategy"
    category = "base"

    def __init__(self, **params):
        self.params = params

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def with_signal_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        out = data.copy()
        if "signal" not in out.columns:
            out["signal"] = 0.0
        if "target_weight" not in out.columns:
            out["target_weight"] = out["signal"].clip(-1, 1)
        return out
