from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Any, Callable
import signal
import threading

import pandas as pd


@dataclass(frozen=True)
class DataRequest:
    symbol: str
    start: str
    end: str
    timeframe: str = "1d"
    market: str = "US"
    asset_type: str = "equity"


class DataAdapter(ABC):
    name: str

    @abstractmethod
    def fetch_ohlcv(self, req: DataRequest) -> pd.DataFrame:
        """Return normalized columns: timestamp, open, high, low, close, volume, symbol, source."""


class DataSourceError(RuntimeError):
    """Raised when an external data source cannot return usable data."""


def run_with_timeout(
    fn: Callable[..., Any],
    *,
    timeout_seconds: float,
    source_name: str,
    operation: str,
    **kwargs: Any,
) -> Any:
    if threading.current_thread() is threading.main_thread():
        previous = signal.getsignal(signal.SIGALRM)

        def _handle_timeout(signum, frame):
            raise TimeoutError(
                f"{source_name} timed out after {timeout_seconds:.1f}s during {operation}"
            )

        try:
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
            return fn(**kwargs)
        except TimeoutError:
            raise
        except Exception as exc:
            raise DataSourceError(f"{source_name} failed during {operation}: {exc}") from exc
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(fn, **kwargs)
    try:
        return future.result(timeout=timeout_seconds)
    except FutureTimeoutError as exc:
        future.cancel()
        raise TimeoutError(
            f"{source_name} timed out after {timeout_seconds:.1f}s during {operation}"
        ) from exc
    except Exception as exc:
        raise DataSourceError(f"{source_name} failed during {operation}: {exc}") from exc
    finally:
        executor.shutdown(wait=False, cancel_futures=True)


def normalize_ohlcv(df: pd.DataFrame, symbol: str, source: str) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError(f"No data returned for {symbol} from {source}")
    df = df.copy()
    lower = {c: str(c).lower() for c in df.columns}
    df = df.rename(columns=lower)
    if "date" in df.columns and "timestamp" not in df.columns:
        df = df.rename(columns={"date": "timestamp"})
    if df.index.name and "timestamp" not in df.columns:
        df = df.reset_index().rename(columns={df.index.name: "timestamp"})
    if "timestamp" not in df.columns:
        df = df.reset_index().rename(columns={"index": "timestamp"})
    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns {missing} in {source} data for {symbol}")
    out = df[required].copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"])
    for c in ["open", "high", "low", "close", "volume"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    out = out.dropna(subset=["timestamp", "open", "high", "low", "close"])
    out["symbol"] = symbol
    out["source"] = source
    return out.sort_values("timestamp").reset_index(drop=True)


class CsvAdapter(DataAdapter):
    name = "csv"

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def fetch_ohlcv(self, req: DataRequest) -> pd.DataFrame:
        df = pd.read_csv(self.path)
        df = normalize_ohlcv(df, req.symbol, self.name)
        mask = (df["timestamp"] >= pd.to_datetime(req.start)) & (df["timestamp"] <= pd.to_datetime(req.end))
        return df.loc[mask].reset_index(drop=True)


class SyntheticAdapter(DataAdapter):
    name = "synthetic"

    def fetch_ohlcv(self, req: DataRequest) -> pd.DataFrame:
        import numpy as np
        import hashlib

        dates = pd.date_range(req.start, req.end, freq="B")
        seed = int(hashlib.md5(req.symbol.encode()).hexdigest(), 16) % (2**32)
        rng = np.random.default_rng(seed)
        rets = rng.normal(0.00035, 0.015, len(dates))
        close = 100 * (1 + pd.Series(rets, index=dates)).cumprod()
        open_ = close.shift(1).fillna(close.iloc[0]) * (1 + rng.normal(0, 0.002, len(dates)))
        high = pd.concat([open_, close], axis=1).max(axis=1) * (1 + rng.random(len(dates)) * 0.01)
        low = pd.concat([open_, close], axis=1).min(axis=1) * (1 - rng.random(len(dates)) * 0.01)
        volume = rng.integers(1_000_000, 5_000_000, len(dates))
        df = pd.DataFrame({"timestamp": dates, "open": open_.values, "high": high.values, "low": low.values, "close": close.values, "volume": volume})
        return normalize_ohlcv(df, req.symbol, self.name)
