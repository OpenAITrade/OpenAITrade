from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import math
import subprocess
import sys

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openaitrade.backtest.engine import BacktestEngine
from openaitrade.data.base import CsvAdapter, DataRequest
from openaitrade.strategies.factory import STRATEGIES, create_strategy


MARKET_DATA_DIR = ROOT / "data" / "market_data"
REPORT_DIR = ROOT / "reports"


def load_local_symbol(symbol: str) -> pd.DataFrame:
    path = MARKET_DATA_DIR / f"{symbol.lower()}.csv"
    return CsvAdapter(path).fetch_ohlcv(
        DataRequest(symbol=symbol.upper(), start="2018-01-01", end="2024-12-31")
    )


def build_local_dataset(strategy_id: str, category: str) -> pd.DataFrame:
    if strategy_id == "pairs_trading":
        symbols = ["spy", "qqq"]
    elif strategy_id in {
        "basket_statarb",
        "topn_momentum",
        "sector_rotation",
        "dual_momentum",
        "low_vol_momentum",
        "multi_factor_ranking",
        "value_factor",
        "quality_factor",
        "size_factor",
    } or category in {"momentum", "factor"}:
        symbols = ["spy", "qqq", "iwm", "tlt", "gld", "btc", "eth"]
    elif strategy_id in {"basis_arbitrage", "funding_rate_arbitrage"}:
        symbols = ["btc", "eth"]
    else:
        symbols = ["spy"]
    return pd.concat([load_local_symbol(symbol) for symbol in symbols], ignore_index=True)


def build_etf_premium_proxy_dataset() -> pd.DataFrame:
    spy = load_local_symbol("spy").copy()
    voo = spy.copy()
    qqq = load_local_symbol("qqq").copy()
    proxy = (voo["close"] / voo["close"].iloc[0] + qqq["close"] / qqq["close"].iloc[0]) / 2.0
    spy["nav"] = proxy * spy["close"].iloc[0]
    return spy


def run_external_source(source_name: str) -> dict:
    cmd = [sys.executable, str(ROOT / "examples" / "health_check.py"), "--source", source_name]
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        lines = [line for line in proc.stdout.splitlines() if line.strip()]
        if not lines:
            return {"source": source_name, "status": "FAIL", "detail": "No output"}
        return json.loads(lines[-1])
    except subprocess.TimeoutExpired:
        return {"source": source_name, "status": "TIMEOUT", "detail": "Child process exceeded 30s timeout"}


def fetch_binance_klines(base_url: str, path: str, params: dict) -> pd.DataFrame:
    response = requests.get(f"{base_url}{path}", params=params, timeout=20)
    response.raise_for_status()
    rows = response.json()
    df = pd.DataFrame(
        rows,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "num_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )
    out = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(df["open_time"], unit="ms", utc=True).dt.tz_convert(None),
            "open": pd.to_numeric(df["open"]),
            "high": pd.to_numeric(df["high"]),
            "low": pd.to_numeric(df["low"]),
            "close": pd.to_numeric(df["close"]),
            "volume": pd.to_numeric(df["volume"]),
        }
    )
    return out.sort_values("timestamp").reset_index(drop=True)


def fetch_binance_funding(symbol: str = "BTCUSDT", limit: int = 1000) -> pd.DataFrame:
    response = requests.get(
        "https://fapi.binance.com/fapi/v1/fundingRate",
        params={"symbol": symbol, "limit": limit},
        timeout=20,
    )
    response.raise_for_status()
    rows = response.json()
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True).dt.tz_convert(None).dt.floor("D")
    df["funding_rate"] = pd.to_numeric(df["fundingRate"])
    return df.groupby("timestamp", as_index=False)["funding_rate"].mean()


def build_basis_dataset() -> tuple[pd.DataFrame | None, dict]:
    try:
        spot = fetch_binance_klines(
            "https://api.binance.com",
            "/api/v3/klines",
            {"symbol": "BTCUSDT", "interval": "1d", "limit": 1000},
        )
        perp = fetch_binance_klines(
            "https://fapi.binance.com",
            "/fapi/v1/klines",
            {"symbol": "BTCUSDT", "interval": "1d", "limit": 1000},
        )
        merged = spot.merge(
            perp[["timestamp", "close"]].rename(columns={"close": "perp_close"}),
            on="timestamp",
            how="inner",
        )
        merged["basis"] = (merged["perp_close"] / merged["close"]) - 1.0
        spot_leg = merged[["timestamp", "open", "high", "low", "close", "volume", "basis"]].copy()
        perp_leg = merged[["timestamp", "open", "high", "low", "perp_close", "volume", "basis"]].copy()
        spot_leg["symbol"] = "SPOT"
        perp_leg["symbol"] = "PERP"
        spot_leg["source"] = "binance_spot"
        perp_leg["source"] = "binance_perp"
        perp_leg = perp_leg.rename(columns={"perp_close": "close"})
        columns = ["timestamp", "open", "high", "low", "close", "volume", "symbol", "source", "basis"]
        data = pd.concat([spot_leg[columns], perp_leg[columns]], ignore_index=True)
        return data, {"source": "binance_basis", "status": "OK", "detail": f"rows={len(data)}"}
    except Exception as exc:
        return None, {"source": "binance_basis", "status": "FAIL", "detail": f"{type(exc).__name__}: {exc}"}


def build_funding_dataset() -> tuple[pd.DataFrame | None, dict]:
    try:
        price = fetch_binance_klines(
            "https://fapi.binance.com",
            "/fapi/v1/klines",
            {"symbol": "BTCUSDT", "interval": "1d", "limit": 1000},
        )
        funding = fetch_binance_funding(symbol="BTCUSDT", limit=1000)
        merged = price.merge(funding, on="timestamp", how="left").fillna({"funding_rate": 0.0})
        merged["symbol"] = "BTC/USDT"
        merged["source"] = "binance_futures"
        return merged, {"source": "binance_funding", "status": "OK", "detail": f"rows={len(merged)}"}
    except Exception as exc:
        return None, {"source": "binance_funding", "status": "FAIL", "detail": f"{type(exc).__name__}: {exc}"}


def classify_metrics(metrics: dict, strategy_id: str, has_nonzero_signal: bool) -> tuple[str, list[str]]:
    notes: list[str] = []
    status = "PASS"

    for key in ["total_return", "annual_return", "annual_volatility", "sharpe", "sortino", "calmar", "max_drawdown", "final_equity"]:
        value = metrics.get(key)
        if value is None or not math.isfinite(value):
            status = "FAIL"
            notes.append(f"{key} is not finite")

    if not (-1.0 <= metrics["max_drawdown"] <= 0.0):
        status = "FAIL"
        notes.append("max_drawdown out of expected range")

    if metrics["annual_volatility"] < 0:
        status = "FAIL"
        notes.append("annual_volatility is negative")

    if metrics["final_equity"] <= 0:
        status = "FAIL"
        notes.append("final_equity is not positive")

    if metrics["max_drawdown"] < -0.60:
        status = "WARN" if status == "PASS" else status
        notes.append("max_drawdown is unusually deep")

    if metrics["annual_return"] < -0.20 and metrics["sharpe"] < 0:
        status = "WARN" if status == "PASS" else status
        notes.append("annual_return and sharpe are both materially weak")

    if abs(metrics["sharpe"]) > 10:
        status = "WARN" if status == "PASS" else status
        notes.append("sharpe magnitude is unusually high")

    if metrics["annual_volatility"] > 2.0:
        status = "WARN" if status == "PASS" else status
        notes.append("annual_volatility is unusually high")

    if metrics["num_trades"] == 0 and has_nonzero_signal:
        status = "WARN" if status == "PASS" else status
        notes.append("signals exist but no trades were recorded")

    if metrics["num_trades"] == 0 and strategy_id not in {"etf_premium", "basis_arbitrage", "funding_rate_arbitrage"}:
        status = "WARN" if status == "PASS" else status
        notes.append("strategy produced zero trades on this dataset")

    return status, notes


def run_strategy_validation() -> tuple[list[dict], dict]:
    rows: list[dict] = []
    external_status: dict[str, dict] = {}

    for strategy_id, strategy_cls in STRATEGIES.items():
        data_origin = "local_real_csv"
        dataset_note = ""

        if strategy_id == "etf_premium":
            data = build_etf_premium_proxy_dataset()
            data_origin = "real_etf_price_with_real_proxy_nav"
            dataset_note = "Used real ETF price with benchmark-style NAV proxy because free historical official NAV was unavailable locally."
        elif strategy_id == "basis_arbitrage":
            data, external_status["binance_basis_gate"] = build_basis_dataset()
            if data is None:
                rows.append({
                    "strategy_id": strategy_id,
                    "strategy_name": strategy_cls.name,
                    "status": "SKIP",
                    "data_origin": "external_gate_failed",
                    "notes": [external_status["binance_basis_gate"]["detail"]],
                })
                continue
            data_origin = "real_binance_spot_and_perp_basis"
            dataset_note = "Used real Binance spot and perpetual futures daily data to compute basis."
        elif strategy_id == "funding_rate_arbitrage":
            data, external_status["binance_funding_gate"] = build_funding_dataset()
            if data is None:
                rows.append({
                    "strategy_id": strategy_id,
                    "strategy_name": strategy_cls.name,
                    "status": "SKIP",
                    "data_origin": "external_gate_failed",
                    "notes": [external_status["binance_funding_gate"]["detail"]],
                })
                continue
            data_origin = "real_binance_funding_and_futures_price"
            dataset_note = "Used real Binance funding rates merged with real Binance futures daily OHLCV."
        else:
            data = build_local_dataset(strategy_id, strategy_cls.category)

        strategy = create_strategy(strategy_id)
        signals = strategy.generate_signals(data.copy())
        result = BacktestEngine().run(data.copy(), strategy)
        has_nonzero_signal = bool((signals["target_weight"].fillna(0) != 0).any())
        status, notes = classify_metrics(result.metrics, strategy_id, has_nonzero_signal)
        if dataset_note:
            notes.append(dataset_note)

        rows.append(
            {
                "strategy_id": strategy_id,
                "strategy_name": strategy_cls.name,
                "category": strategy_cls.category,
                "status": status,
                "data_origin": data_origin,
                "num_rows": int(len(data)),
                "num_symbols": int(data["symbol"].nunique()),
                "nonzero_signal_rows": int((signals["target_weight"].fillna(0) != 0).sum()),
                "metrics": result.metrics,
                "notes": notes,
            }
        )
    return rows, external_status


def write_report(rows: list[dict], external_status: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = REPORT_DIR / f"real_data_strategy_validation_{stamp}.json"
    md_path = REPORT_DIR / f"real_data_strategy_validation_{stamp}.md"

    json_payload = {"generated_at_utc": stamp, "external_status": external_status, "strategies": rows}
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Real Data Strategy Validation",
        "",
        f"Generated at UTC: `{stamp}`",
        "",
        "## Summary",
        "",
        f"- Total strategies: `{len(rows)}`",
        f"- PASS: `{sum(1 for row in rows if row['status'] == 'PASS')}`",
        f"- WARN: `{sum(1 for row in rows if row['status'] == 'WARN')}`",
        f"- FAIL: `{sum(1 for row in rows if row['status'] == 'FAIL')}`",
        f"- SKIP: `{sum(1 for row in rows if row['status'] == 'SKIP')}`",
        "",
        "## External Gates",
        "",
    ]

    if external_status:
        for key, value in external_status.items():
            lines.append(f"- `{key}`: `{value.get('status', 'UNKNOWN')}` - {value.get('detail', '')}")
    else:
        lines.append("- No external gate checks recorded.")

    lines.extend(
        [
            "",
            "## Strategy Results",
            "",
            "| Strategy | Status | Data | Symbols | Trades | Sharpe | Max DD | Notes |",
            "|---|---|---|---:|---:|---:|---:|---|",
        ]
    )

    for row in rows:
        metrics = row.get("metrics", {})
        notes = "; ".join(row.get("notes", [])) or "-"
        lines.append(
            f"| `{row['strategy_id']}` | `{row['status']}` | `{row['data_origin']}` | "
            f"{row.get('num_symbols', 0)} | {metrics.get('num_trades', 0)} | "
            f"{metrics.get('sharpe', 0):.2f} | {metrics.get('max_drawdown', 0):.2%} | {notes} |"
        )

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def main():
    rows, external_status = run_strategy_validation()
    report_path = write_report(rows, external_status)
    print(f"Report written to {report_path}")
    for row in rows:
        metrics = row.get("metrics", {})
        print(
            f"{row['strategy_id']:24s} {row['status']:4s} "
            f"trades={metrics.get('num_trades', 0):4d} "
            f"sharpe={metrics.get('sharpe', 0):7.3f} "
            f"max_dd={metrics.get('max_drawdown', 0):7.3%}"
        )


if __name__ == "__main__":
    main()
