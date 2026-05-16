# Low Vol Momentum

## 策略ID

`low_vol_momentum`

## 策略简介

低波动动量策略，在动量因子基础上叠加波动率调整。选择高动量但低波动的标的，兼顾趋势性和稳定性。学术研究表明低波动因子与动量因子具有负相关性，组合使用可以分散风险。

## 适用市场

- 市场: A股、US equity、全球股票
- 资产类型: 股票、ETF
- 时间周期: 1d

## 策略逻辑

1. 计算每只标的动量分数 (N日收益率)
2. 计算每只标的波动率分数 (M日收益标准差)
3. 综合得分 = 0.6 * 动量排名分 + 0.4 * 低波动排名分
4. 选择综合排名前K的标的等权配置

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
  id: low_vol_momentum
  params:
    momentum_window: 120
    vol_window: 60
    top_k: 5
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/low_vol_momentum_demo
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

1. 低波动因子可能在牛市中表现落后
2. 权重调整可能增加交易成本
3. 波动率计算窗口影响因子有效性
4. 建议定期再平衡

## 改进方向

- [ ] 优化动量与波动率权重比例
- [ ] 使用波动率倒数加权替代等权
- [ ] 加入止损机制
- [ ] 结合其他因子(质量、价值)进一步筛选