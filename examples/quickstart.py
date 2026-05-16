from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openaitrade.data.base import DataRequest, SyntheticAdapter
from openaitrade.strategies.factory import create_strategy


def main():
    adapter = SyntheticAdapter()
    data = adapter.fetch_ohlcv(DataRequest("SPY", "2020-01-01", "2021-01-01"))
    strategy = create_strategy("sma_crossover", short_window=20, long_window=60)
    signals = strategy.generate_signals(data)
    print(signals[["timestamp", "signal"]].tail().to_string(index=False))


if __name__ == "__main__":
    main()
