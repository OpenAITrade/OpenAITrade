# 数据源说明

## synthetic

内置合成数据，用于测试和演示，无需联网。

## csv

读取本地 CSV。要求至少包含：

```text
timestamp,open,high,low,close,volume
```

## yfinance

适合美股、ETF、指数等研究数据。需要安装：

```bash
pip install yfinance
```

## AKShare

适合 A 股、港股、美股、期货、基金、宏观等中文金融数据聚合。需要安装：

```bash
pip install akshare
```

## BaoStock

适合 A 股历史行情、复权和财务数据。需要安装：

```bash
pip install baostock
```

## CCXT

适合加密货币交易所行情。需要安装：

```bash
pip install ccxt
```
