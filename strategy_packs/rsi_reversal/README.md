# RSI Reversal

## 策略ID

`rsi_reversal`

## 策略简介

RSI超卖超买反转策略，当RSI低于下阈值时做多(超卖)，当RSI高于上阈值时平仓(超买)。经典的均值回归类策略，适用于震荡市场。

## 适用市场

- 市场: A股、US equity、数字货币
- 资产类型: 股票、ETF、数字货币
- 时间周期: 1d (股票/ETF)、1h (数字货币)

## 策略逻辑

1. 计算N日RSI (默认14日)
2. 当RSI < 下阈值(默认30)时，判定为超卖，信号=1做多
3. 当RSI > 上阈值(默认70)时，判定为超买，平仓
4. 使用前向填充保持仓位直到触发超买阈值

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `rsi_window` | 14 | RSI计算窗口天数 |
| `lower` | 30 | 超卖阈值，RSI低于此值时做多 |
| `upper` | 70 | 超买阈值，RSI高于此值时平仓 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: rsi_reversal
  params:
    rsi_window: 14
    lower: 30
    upper: 70
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/rsi_reversal_demo
```

## 回测结果

最佳标的: QQQ (US Equity - NASDAQ 100 ETF)

| 指标 | 值 |
|------|-----|
| 总收益率 | 82.85% |
| 年化收益率 | 9.01% |
| 夏普比率 | 1.103 |
| 最大回撤 | -10.30% |
| 交易次数 | 86 |

## 图表

> 回测图表:
> - `results/charts/rsi_reversal_qqq.png` - QQQ权益曲线
> - `results/charts/rsi_reversal_spy.png` - SPY权益曲线
> - `results/charts/rsi_reversal_tencent.png` - Tencent权益曲线

## 风险提示

1. 强势趋势行情中RSI可能长期维持超买状态，导致过早止损
2. 参数(30/70)需要根据不同标的和市场环境优化
3. 单边趋势市场中可能产生连续亏损
4. 建议结合趋势判断指标使用

## 改进方向

- [ ] 增加趋势过滤，只在趋势不明确时使用RSI信号
- [ ] 动态调整RSI阈值
- [ ] 结合成交量确认信号
- [ ] 添加止损机制保护