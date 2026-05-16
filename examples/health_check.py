from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

CASES = {
    "yfinance": {
        "kwargs": {},
        "request": {
            "symbol": "AAPL",
            "start": "2024-01-02",
            "end": "2024-02-01",
        },
    },
    "akshare": {
        "kwargs": {"timeout_seconds": 15.0},
        "request": {
            "symbol": "000001",
            "start": "2024-01-02",
            "end": "2024-02-01",
        },
    },
    "baostock": {
        "kwargs": {"timeout_seconds": 15.0},
        "request": {
            "symbol": "sh.600000",
            "start": "2024-01-02",
            "end": "2024-02-01",
        },
    },
    "ccxt": {
        "kwargs": {"exchange": "binance", "timeout_seconds": 15.0},
        "request": {
            "symbol": "BTC/USDT",
            "start": "2024-01-02",
            "end": "2024-02-01",
        },
    },
    "openbb": {
        "kwargs": {},
        "request": {
            "symbol": "AAPL",
            "start": "2024-01-02",
            "end": "2024-02-01",
        },
    },
}


def run_single_source(source_name: str) -> int:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from openaitrade.data.base import DataRequest
    from openaitrade.data.factory import create_data_adapter

    config = CASES[source_name]
    payload = config["request"]

    try:
        adapter = create_data_adapter(source_name, **config["kwargs"])
        df = adapter.fetch_ohlcv(
            DataRequest(
                payload["symbol"],
                payload["start"],
                payload["end"],
            )
        )
        result = {
            "source": source_name,
            "status": "OK",
            "detail": f"rows={len(df)} range={df['timestamp'].min().date()}..{df['timestamp'].max().date()}",
        }
    except ImportError as exc:
        result = {"source": source_name, "status": "MISSING", "detail": str(exc)}
    except TimeoutError as exc:
        result = {"source": source_name, "status": "TIMEOUT", "detail": str(exc)}
    except Exception as exc:
        result = {
            "source": source_name,
            "status": "FAIL",
            "detail": f"{type(exc).__name__}: {exc}",
        }

    print(json.dumps(result, ensure_ascii=False))
    return 0


def run_full_health_check() -> int:
    print("OpenAITrade Public Data Source Health Check")
    print("=" * 48)
    for source_name in CASES:
        cmd = [sys.executable, __file__, "--source", source_name]
        try:
            proc = subprocess.run(
                cmd,
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            stdout = proc.stdout.strip().splitlines()
            payload = json.loads(stdout[-1]) if stdout else {
                "source": source_name,
                "status": "FAIL",
                "detail": "No output from child health check",
            }
        except subprocess.TimeoutExpired:
            payload = {
                "source": source_name,
                "status": "TIMEOUT",
                "detail": "Child process exceeded 20s timeout",
            }

        print(f"{payload['source']:10s} {payload['status']:8s} {payload['detail']}")
    return 0


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--source":
        return run_single_source(sys.argv[2])
    return run_full_health_check()


if __name__ == "__main__":
    raise SystemExit(main())
