# Pairs Trading

## 策略ID

`pairs_trading`

## 策略简介

配对交易策略，基于两只标的之间价差的均值回归特性。当价差偏离历史均值达到Z分数阈值时，做多低估一方、做空高估一方，期望价差回归。

## 适用市场

- 市场: US equity、ETF、数字货币
- 资产类型: 股票对、ETF、数字货币对
- 时间周期: 1d (数字货币可用1h)

## 策略逻辑

1. 选择两只标的A和B
2. 计算价差 = A / B (价格比率)
3. 计算N日滚动Z分数: (spread - mean) / std
4. Z > entry_z 时，做空A、做多B
5. Z < -entry_z 时，做多A、做空B
6. Z绝对值 < exit_z 时，平仓

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `lookback` | 120 | 计算价差均值和标准差的窗口天数 |
| `entry_z` | 2.0 | 入场Z分数阈值 |
| `exit_z` | 0.5 | 出场Z分数阈值 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: SPY,QQQ
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: pairs_trading
  params:
    lookback: 120
    entry_z: 2.0
    exit_z: 0.5
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/pairs_trading_demo
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

1. 价差可能长期不回归，导致持仓亏损
2. 需要关注两只标的的基本面关系是否稳定
3. 交易成本和滑点会影响策略表现
4. 建议选择相关性高、质地稳定的两只标的

## 改进方向

- [ ] 增加协整性检验
- [ ] 动态调整仓位适应波动率变化
- [ ] 加入止损机制
- [ ] 优化配对选择逻辑