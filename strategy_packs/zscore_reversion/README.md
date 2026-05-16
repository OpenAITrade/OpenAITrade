# Z-Score Reversion

## 策略ID

`zscore_reversion`

## 策略简介

滚动Z分数均值回归策略，当价格相对历史均值偏离达到Z分数阈值时做多，认为价格会向均值回归。量化领域经典的反转策略之一。

## 适用市场

- 市场: A股、US equity、数字货币、商品期货
- 资产类型: 股票、ETF、期货、数字货币
- 时间周期: 1d (股票/期货)、1h (数字货币)

## 策略逻辑

1. 计算N日滚动均值和标准差
2. 计算当前价格Z分数: (price - mean) / std
3. 当Z分数 < 入场阈值(默认-2)时做多
4. 当Z分数 >= 出场阈值(默认0)时平仓
5. 只做多不做空，属于long-only均值回归

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `window` | 60 | 滚动均值和标准差的窗口天数 |
| `entry_z` | -2 | 入场Z分数阈值，价格低于此值时做多 |
| `exit_z` | 0 | 出场Z分数阈值，Z分数回升至此值时平仓 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,TSLA,BNB
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: zscore_reversion
  params:
    window: 60
    entry_z: -2
    exit_z: 0
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/zscore_reversion_demo
```

## 回测结果

最佳标的: QQQ (US Equity - NASDAQ 100 ETF)

| 指标 | 值 |
|------|-----|
| 总收益率 | 18.61% |
| 年化收益率 | 2.47% |
| 夏普比率 | 0.293 |
| 最大回撤 | -13.34% |
| 交易次数 | 44 |

## 图表

> 回测图表:
> - `results/charts/zscore_reversion_qqq.png` - QQQ权益曲线
> - `results/charts/zscore_reversion_tlt.png` - TLT权益曲线
> - `results/charts/zscore_reversion_btc.png` - BTC权益曲线

## 风险提示

1. 极端行情中Z分数可能长时间维持极端值，导致仓位过重
2. 均值回归假设在趋势行情中可能失效
3. 窗口参数选择对结果影响较大
4. 建议配合市场环境判断使用

## 改进方向

- [ ] 增加趋势过滤，避免逆势交易
- [ ] 设置最大持仓时间限制
- [ ] 动态调整入场阈值
- [ ] 增加止损机制