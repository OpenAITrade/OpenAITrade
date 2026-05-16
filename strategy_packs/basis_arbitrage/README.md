# Basis Arbitrage

## 策略ID

`basis_arbitrage`

## 策略简介

期现套利策略，捕捉现货与期货之间的基差偏离。当基差超过阈值时，做多现货、做空期货(基差缩小收益)，或反向操作。

## 适用市场

- 市场: 商品期货、数字货币
- 资产类型: 期货、现货、数字货币
- 时间周期: 1d (数字货币可用1h)

## 策略逻辑

1. 计算现货-期货基差 (basis = spot - futures)
2. 当基差绝对值 > threshold 时进行套利
3. target_weight = -basis (基差为正时卖基差，基差为负时买基差)
4. 权重裁剪至[-1, 1]范围
5. 无基差数据时保持空仓(安全fallback)

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `basis_threshold` | 0.02 | 基差阈值，超过此值触发套利(2%) |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: BTC_USDT_SPOT,BTC_USDT_FUTURES
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: basis_arbitrage
  params:
    basis_threshold: 0.02
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/basis_arbitrage_demo
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

1. 期货移仓成本可能侵蚀套利利润
2. 数字货币基差波动剧烈，风险较高
3. 需要准确的基差数据
4. 资金费率变化可能影响策略表现

## 改进方向

- [ ] 考虑移仓时机优化
- [ ] 加入资金费率预测
- [ ] 动态调整仓位适应基差波动
- [ ] 多品种分散配置