# Bollinger Reversion

## 策略ID

`bollinger_reversion`

## 策略简介

布林带均值回归策略，当价格触及布林下轨时做多，认为价格会向均值回归。经典的反转类策略，适用于区间震荡市场。

## 适用市场

- 市场: A股、US equity、数字货币
- 资产类型: 股票、ETF、数字货币
- 时间周期: 1d (股票/ETF)、1h (数字货币)

## 策略逻辑

1. 计算N日移动平均线(Mid)
2. 计算N日标准差(Std)
3. 计算布林上下轨: Mid ± K*Std (K默认2)
4. 当价格 < 下轨时，做多入场
5. 当价格 > 中轨时，平仓出场
6. 使用前向填充保持仓位直到触发中轨出场

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `window` | 20 | 移动平均和标准差的窗口天数 |
| `num_std` | 2 | 布林带倍数(K) |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: bollinger_reversion
  params:
    window: 20
    num_std: 2
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/bollinger_reversion_demo
```

## 回测结果

最佳标的: QQQ (US Equity - NASDAQ 100 ETF)

| 指标 | 值 |
|------|-----|
| 总收益率 | 43.41% |
| 年化收益率 | 5.29% |
| 夏普比率 | 0.737 |
| 最大回撤 | -7.82% |
| 交易次数 | 96 |

## 图表

> 回测图表:
> - `results/charts/bollinger_reversion_qqq.png` - QQQ权益曲线
> - `results/charts/bollinger_reversion_spy.png` - SPY权益曲线
> - `results/charts/bollinger_reversion_tencent.png` - Tencent权益曲线

## 风险提示

1. 趋势行情中价格可能沿布林轨道持续运行，均值回归假设失效
2. 参数对市场状态敏感，不同标的需要重新优化
3. 建议在波动率较高但均值回复特征明显时使用
4. A股市场需要结合市场环境判断

## 改进方向

- [ ] 增加趋势过滤器，避免在趋势行情中使用
- [ ] 结合RSI或MACD确认超卖状态
- [ ] 优化出场机制(可设置分批止盈)
- [ ] 动态调整布林倍数适应市场波动