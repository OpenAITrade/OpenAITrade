# Size Factor

## 策略ID

`size_factor`

## 策略简介

规模因子策略，选择市值较小的标的。小市值股票长期来看可能具有超额收益，但同时伴随更高风险。本策略使用日均成交额作为流动性的代理，结合市值筛选。

## 适用市场

- 市场: A股、US equity
- 资产类型: 股票
- 时间周期: 1d

## 策略逻辑

1. 计算每只标的日均成交额 (close * volume)
2. 过滤成交额低于min_liquidity阈值的标的
3. 在满足流动性条件的标的中，选择成交额最低的K个
4. 等权配置，认为成交额越低表示市值越小

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `top_k` | 10 | 选择成交额最低的K个标的(代表小市值) |
| `min_liquidity` | 0 | 最小日均成交额阈值，低于此值则排除 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,AMD,INTC,META,JPM
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: size_factor
  params:
    top_k: 10
    min_liquidity: 0
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/size_factor_demo
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

1. 小市值股票流动性风险较高
2. 冲击成本可能显著
3. A股市场小市值效应明显但波动也更大
4. 建议设置合理的流动性阈值

## 改进方向

- [ ] 使用市值而非成交额作为规模代理
- [ ] 增加基本面筛选(避免壳价值股票)
- [ ] 结合质量因子过滤
- [ ] 设置单票最大权重限制