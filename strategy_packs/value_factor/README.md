# Value Factor

## 策略ID

`value_factor`

## 策略简介

价值因子策略，选择相对便宜的标的进行配置。使用价格与滚动高点的比率作为价值代理指标，数值越低表示相对价格越便宜。

## 适用市场

- 市场: A股、US equity
- 资产类型: 股票、ETF
- 时间周期: 1d

## 策略逻辑

1. 计算每只标的滚动窗口内的最高价
2. 计算价值分数: -(price / rolling_high)，取负使分数越高越有价值
3. 在每个时间点对所有标的价值分数排名
4. 选择排名前K的标的等权配置

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `top_k` | 10 | 选择价值分数排名前K的标的 |
| `lookback` | 252 | 滚动窗口天数，用于计算最高价 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,AMD,INTC
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: value_factor
  params:
    top_k: 10
    lookback: 252
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/value_factor_demo
```

## 回测结果

最佳标的: QQQ (US Equity - NASDAQ 100 ETF)

| 指标 | 值 |
|------|-----|
| 总收益率 | 232.68% |
| 年化收益率 | 18.76% |
| 夏普比率 | 0.877 |
| 最大回撤 | -35.62% |
| 交易次数 | 1 |

## 图表

> 回测图表:
> - `results/charts/value_factor_qqq.png` - QQQ权益曲线
> - `results/charts/value_factor_spy.png` - SPY权益曲线
> - `results/charts/value_factor_gld.png` - GLD权益曲线

## 风险提示

1. 价值陷阱风险：便宜可能有便宜的原因
2. 长时间周期可能滞后于市场
3. 需要结合其他因子使用
4. A股市场需要考虑基本面数据质量

## 改进方向

- [ ] 使用真实PB、PE等基本面指标
- [ ] 结合动量因子筛选
- [ ] 增加质量过滤条件
- [ ] 加入分红率等辅助指标