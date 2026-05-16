# Top-N Momentum

## 策略ID

`topn_momentum`

## 策略简介

截面动量策略，每个调仓周期选择过去N日收益率最高的前K个标的等权配置。动量效应的核心实现方式之一。

## 适用市场

- 市场: A股、US equity、全球股票
- 资产类型: 股票、ETF
- 时间周期: 1d

## 策略逻辑

1. 计算每只标的过去N日收益率作为动量指标
2. 在每个时间点对所有标的动量排名
3. 选择排名前K的标的等权配置
4. 权重 = 1/K，每期按排名重新平衡

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `lookback` | 120 | 动量计算窗口天数 |
| `top_k` | 3 | 选择动量排名前K的标的 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: topn_momentum
  params:
    lookback: 120
    top_k: 3
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/topn_momentum_demo
```

## 回测结果

最佳标的: QQQ (US Equity - NASDAQ 100 ETF)

| 指标 | 值 |
|------|-----|
| 总收益率 | 200.66% |
| 年化收益率 | 17.05% |
| 夏普比率 | 0.789 |
| 最大回撤 | -35.62% |
| 交易次数 | 1 |

## 图表

> 回测图表:
> - `results/charts/topn_momentum_qqq.png` - QQQ权益曲线
> - `results/charts/topn_momentum_spy.png` - SPY权益曲线
> - `results/charts/topn_momentum_gld.png` - GLD权益曲线

## 风险提示

1. 动量反转风险：极端行情后动量可能迅速反转
2. 集中风险：选择K个标的可能导致集中度过高
3. 趋势跟踪类策略在市场转换期可能产生较大回撤
4. A股市场需要考虑交易成本和冲击成本

## 改进方向

- [ ] 增加动量反转过滤器
- [ ] 结合波动率调整权重
- [ ] 加入风险中性化处理
- [ ] 考虑加入质量或价值因子