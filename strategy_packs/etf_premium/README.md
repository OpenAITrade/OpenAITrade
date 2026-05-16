# ETF Premium

## 策略ID

`etf_premium`

## 策略简介

ETF折溢价研究策略，捕捉ETF市场价格与净值(NAV)之间的偏离。当ETF溢价时卖出，折价时买入，期望回归平价。

## 适用市场

- 市场: US equity、A股
- 资产类型: ETF
- 时间周期: 1d

## 策略逻辑

1. 计算ETF溢价率: close / nav - 1
2. 当溢价率绝对值 > threshold 时进行交易
3. target_weight = -premium (溢价时卖，贴水时买)
4. 权重裁剪至[-1, 1]范围
5. 无NAV数据时保持空仓(安全fallback)

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `premium_threshold` | 0.01 | 溢价率阈值，超过此值触发交易(1%) |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: SPY,QQQ,IWM,EFA,EEM
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: etf_premium
  params:
    premium_threshold: 0.01
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/etf_premium_demo
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

1. ETF折溢价可能长期存在，回归时间不确定
2. 需要实时NAV数据才能准确计算溢价率
3. 流动性差的ETF冲击成本较高
4. A股ETF可能存在涨跌停限制

## 改进方向

- [ ] 结合成交量确认信号强度
- [ ] 加入历史溢价率分布分析
- [ ] 考虑流动性对折溢价的影响
- [ ] 优化入场时机选择