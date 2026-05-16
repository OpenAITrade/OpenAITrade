# Multi Factor Ranking

## 策略ID

`multi_factor_ranking`

## 策略简介

多因子排名策略，综合动量和低波动两个维度进行选股。通过因子排名组合，可以在捕捉趋势的同时控制下行风险。

## 适用市场

- 市场: A股、US equity、全球股票
- 资产类型: 股票、ETF
- 时间周期: 1d

## 策略逻辑

1. 计算动量因子 (M日收益率)
2. 计算波动率因子 (M日收益标准差)
3. 对每个因子进行截面排名(百分位)
4. 综合得分 = 0.6 * 动量排名 + 0.4 * 低波动排名
5. 选择综合排名前K的标的等权配置

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `momentum_window` | 120 | 动量计算窗口天数 |
| `vol_window` | 60 | 波动率计算窗口天数 |
| `top_k` | 5 | 选择综合排名前K的标的 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: multi_factor_ranking
  params:
    momentum_window: 120
    vol_window: 60
    top_k: 5
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/multi_factor_ranking_demo
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

1. 因子有效性会随市场状态变化
2. 多因子组合可能增加复杂度
3. 需要定期重新校准因子权重
4. 交易成本可能因频繁换仓而增加

## 改进方向

- [ ] 加入更多因子(价值、质量、规模)
- [ ] 使用机器学习方法优化因子权重
- [ ] 增加因子有效性监控机制
- [ ] 考虑加入风险模型控制组合风险