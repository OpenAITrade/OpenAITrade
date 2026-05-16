# ATR Trailing Stop

## 策略ID

`atr_trailing_stop`

## 策略简介

基于ATR(平均真实波幅)的趋势跟踪策略，使用价格与ATR计算的追踪止损线判断趋势方向。当价格高于均线且站上ATR追踪止损时做多。

## 适用市场

- 市场: A股、数字货币、商品期货
- 资产类型: 股票、期货、数字货币
- 时间周期: 1d (股票/期货)、1h (数字货币)

## 策略逻辑

1. 计算MA窗口(默认50日)判断趋势方向
2. 计算ATR(默认14日)衡量市场波动
3. 追踪止损线 = 最高价 - ATR_multiplier * ATR
4. 当价格 > MA均线 且 价格 > 追踪止损时做多
5. ATR倍数(默认3.0)决定止损距离

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ma_window` | 50 | 趋势判断均线窗口 |
| `atr_window` | 14 | ATR计算窗口 |
| `atr_multiplier` | 3.0 | ATR倍数，决定止损距离 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: BTC,ETH,BNB
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: atr_trailing_stop
  params:
    ma_window: 50
    atr_window: 14
    atr_multiplier: 3.0
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/atr_trailing_stop_demo
```

## 回测结果

最佳标的: BTC (Crypto - Bitcoin)

| 指标 | 值 |
|------|-----|
| 总收益率 | 100.37% |
| 年化收益率 | 10.45% |
| 夏普比率 | 0.402 |
| 最大回撤 | -50.67% |
| 交易次数 | 58 |

## 图表

> 回测图表:
> - `results/charts/atr_trailing_stop_btc.png` - BTC权益曲线
> - `results/charts/atr_trailing_stop_eth.png` - ETH权益曲线
> - `results/charts/atr_trailing_stop_spy.png` - SPY权益曲线

## 风险提示

1. ATR追踪止损在趋势初期可能止损过于频繁
2. 波动率剧烈变化时止损线可能过于宽松或紧凑
3. 震荡行情中容易反复开平仓
4. 数字货币市场建议增大ATR倍数

## 改进方向

- [ ] 动态调整ATR倍数适应市场状态
- [ ] 增加趋势确认过滤器
- [ ] 结合成交量确认信号
- [ ] 设置固定止损作为最后防线