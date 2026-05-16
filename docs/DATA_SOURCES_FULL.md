# Data Sources

First-class adapters:

| Adapter | Package | Market | Notes |
|---|---|---|---|
| synthetic | built-in | demo | offline deterministic sample data |
| csv | built-in | any | normalized CSV input |
| yfinance | yfinance | US/global | research-oriented historical data |
| akshare | akshare | CN/HK/US/macro | broad Chinese data aggregator |
| baostock | baostock | CN A-share | free A-share history/fundamentals |
| ccxt | ccxt | crypto | exchange public OHLCV |
| openbb | openbb | global | optional aggregated finance platform |

Canonical OHLCV schema:

```text
timestamp, open, high, low, close, volume, symbol, source
```
