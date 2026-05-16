# Triple MA Filter

## 策略ID

`triple_ma_filter`

## 策略简介

三重移动平均线趋势过滤策略，同时使用短中长期SMA进行趋势判断。只有当短期 > 中期 > 长期时才确认上升趋势，可有效过滤假信号。

## 适用市场

- 市场: A股、US equity、数字货币
- 资产类型: 股票、ETF、数字货币
- 时间周期: 1d (股票/ETF)、1h (数字货币)

## 策略逻辑

1. 计算短期SMA (默认10日)、中期SMA (默认30日)、长期SMA (默认120日)
2. 多头条件: MA_short > MA_mid > MA_long
3. 当满足条件时全仓做多，不满足时平仓
4. 三重确认机制可有效过滤短期噪音

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `short_window` | 10 | 短期SMA窗口天数 |
| `mid_window` | 30 | 中期SMA窗口天数 |
| `long_window` | 120 | 长期SMA窗口天数 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: triple_ma_filter
  params:
    short_window: 10
    mid_window: 30
    long_window: 120
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/triple_ma_filter_demo
```

## 回测结果

最佳标的: BTC (Crypto - Bitcoin)

| 指标 | 值 |
|------|-----|
| 总收益率 | 1290.45% |
| 年化收益率 | 45.69% |
| 夏普比率 | 0.981 |
| 最大回撤 | -45.18% |
| 交易次数 | 54 |

## 图表

> 回测图表:
> - `results/charts/triple_ma_filter_btc.png` - BTC权益曲线
> - `results/charts/triple_ma_filter_eth.png` - ETH权益曲线
> - `results/charts/triple_ma_filter_qqq.png` - QQQ权益曲线

## 风险提示

1. 长期参数(120日)会导致信号严重滞后
2. 趋势转换时可能产生较大回撤
3. 适合长周期趋势明确的标的
4. A股市场建议结合市场情绪指标

## 改进方向

- [ ] 缩短长期窗口或改用指数移动平均(EMA)
- [ ] 添加动量确认指标
- [ ] 结合波动率自适应参数
- [ ] 增加出场机制(如跌破中期均线)