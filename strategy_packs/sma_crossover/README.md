# SMA Crossover

## 策略ID

`sma_crossover`

## 策略简介

经典趋势跟踪策略，通过短期SMA与长期SMA的金叉/死叉判断市场趋势方向。当短期均线上穿长期均线时做多，下穿时平仓。

## 适用市场

- 市场: A股、US equity、数字货币
- 资产类型: 股票、ETF、数字货币
- 时间周期: 1d (股票/ETF)、1h (数字货币)

## 策略逻辑

1. 计算短期SMA (默认20日) 和长期SMA (默认60日)
2. 当短期SMA > 长期SMA 时，生成做多信号
3. 当短期SMA < 长期SMA 时，平仓
4. 信号执行时使用target_weight=1全仓配置

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `short_window` | 20 | 短期SMA窗口天数 |
| `long_window` | 60 | 长期SMA窗口天数 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: sma_crossover
  params:
    short_window: 20
    long_window: 60
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/sma_crossover_demo
```

## 回测结果

最佳标的: BTC (Crypto - Bitcoin)

| 指标 | 值 |
|------|-----|
| 总收益率 | 1234.68% |
| 年化收益率 | 44.84% |
| 夏普比率 | 0.871 |
| 最大回撤 | -53.06% |
| 交易次数 | 47 |

## 图表

> 回测图表:
> - `results/charts/sma_crossover_btc.png` - BTC权益曲线
> - `results/charts/sma_crossover_eth.png` - ETH权益曲线
> - `results/charts/sma_crossover_qqq.png` - QQQ权益曲线

## 风险提示

1. SMA具有滞后性，可能在趋势反转时产生较大回撤
2. 震荡行情中可能出现频繁假信号
3. 参数敏感度较高，不同市场需要重新优化
4. 适用于趋势明显的市场，A 股市场需要结合其他过滤条件

## 改进方向

- [ ] 添加波动率过滤，避免震荡市场入场
- [ ] 结合RSI或MACD确认信号
- [ ] 增加止损机制
- [ ] 优化短期/长期窗口参数组合