# Dual Momentum

## 策略ID

`dual_momentum`

## 策略简介

双重动量策略，同时考虑相对动量(截面排名)和绝对动量(收益率是否为正)。只有绝对动量为正的标的才能入选，有效过滤弱趋势市场。

## 适用市场

- 市场: US equity、全球股票
- 资产类型: 股票、ETF
- 时间周期: 1d

## 策略逻辑

1. 计算每只标的过去N日收益率
2. 只保留收益率超过阈值(默认0，即正收益)的标的
3. 在剩余标的中选择相对动量排名前K的标的
4. 阈值过滤可以避免在下跌市场中逆势做多

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `lookback` | 252 | 动量计算窗口天数(约一年) |
| `top_k` | 1 | 选择相对动量排名前K的标的 |
| `absolute_threshold` | 0.0 | 绝对动量阈值，只有收益超过此值才入选 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: SPY,QQQ,EFA,EEM,TLT,GLD
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: dual_momentum
  params:
    lookback: 252
    top_k: 1
    absolute_threshold: 0.0
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/dual_momentum_demo
```

## 回测结果

最佳标的: BTC (Crypto - Bitcoin)

| 指标 | 值 |
|------|-----|
| 总收益率 | 1747.64% |
| 年化收益率 | 51.73% |
| 夏普比率 | 0.909 |
| 最大回撤 | -53.06% |
| 交易次数 | 31 |

## 图表

> 回测图表:
> - `results/charts/dual_momentum_btc.png` - BTC权益曲线
> - `results/charts/dual_momentum_eth.png` - ETH权益曲线
> - `results/charts/dual_momentum_qqq.png` - QQQ权益曲线

## 风险提示

1. 市场普跌时可能空仓错过反弹机会
2. 绝对动量阈值设置影响信号频率
3. 长周期回看可能滞后
4. K=1时集中度风险较高

## 改进方向

- [ ] 动态调整绝对动量阈值
- [ ] 增加空头配置选项
- [ ] 结合相对强弱指数RSI确认信号
- [ ] 考虑加入多空配对交易