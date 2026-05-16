# Funding Rate Arbitrage

## 策略ID

`funding_rate_arbitrage`

## 策略简介

Crypto资金费率套利策略。当资金费率高于阈值时，做多合约收取资金费率；当资金费率为负时反向操作。

## 适用市场

- 市场: 数字货币期货/永续
- 资产类型: 数字货币合约
- 时间周期: 1h (数字货币)

## 策略逻辑

1. 当 funding_rate > min_rate 时，target_weight = 1 (做多收取费率)
2. 当 funding_rate < -min_rate 时，可做空收取负费率
3. 无 funding_rate 数据时保持空仓(安全fallback)
4. 期望资金费率回归零时平仓获利

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `min_funding_rate` | 0.0003 | 最小资金费率阈值(0.03%) |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: BTC_USDT,ETH_USDT
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: funding_rate_arbitrage
  params:
    min_funding_rate: 0.0003
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/funding_rate_arbitrage_demo
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

1. 资金费率可能急剧变化导致亏损
2. 数字货币波动剧烈，需要动态调整仓位
3. 对冲操作可能产生额外成本
4. 高资金费率往往发生在市场极端时期

## 改进方向

- [ ] 加入趋势判断避免逆势操作
- [ ] 动态调整仓位大小
- [ ] 结合波动率控制风险
- [ ] 多币种分散配置