# Basket Stat Arb

## 策略ID

`basket_statarb`

## 策略简介

篮子统计套利策略，对一篮子标的进行均值回归交易。计算每只标的的标准化价格偏离，当整体篮子偏离时做反向交易。

## 适用市场

- 市场: US equity、ETF
- 资产类型: 股票篮子、ETF
- 时间周期: 1d

## 策略逻辑

1. 计算每只标的的标准化价格: price / rolling_mean - 1
2. 计算截面Z分数: (偏离 - 均值) / 标准差
3. Z < -entry 时，做多(价格被低估)
4. Z > entry 时，做空(价格被高估)
5. 权重按Z分数分配，实现market-neutral

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `lookback` | 120 | 计算滚动均值的窗口天数 |
| `entry_z` | 1.5 | 入场Z分数阈值 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: SPY,QQQ,EFA,EEM,IWM,TLT,GLD,VNQ
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: basket_statarb
  params:
    lookback: 120
    entry_z: 1.5
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/basket_statarb_demo
```

## 回测结果

> 待运行回测后填充

| 指标 | 值 |
|------|-----|
| 总收益率 | - |
| 年化收益率 | - |
| 夏普比率 | - |
| 最大回撤 | - |
| 交易次数 | - |

## 图表

> 回测后生成:
> - `charts/equity_curve.png` - 权益曲线
> - `charts/drawdown.png` - 回撤图
> - `charts/monthly_returns.png` - 月度收益

## 风险提示

1. 市场整体趋势可能强于均值回归逻辑
2.篮子中标的之间的相关性变化会影响策略
3. 需要足够的样本量才能形成有效套利
4. 交易成本和滑点对高频交易影响更大

## 改进方向

- [ ] 增加行业中性化处理
- [ ] 优化篮子构成筛选
- [ ] 加入风险模型控制敞口
- [ ] 考虑加入PCA分析提取因子