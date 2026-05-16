# Donchian Breakout

## 策略ID

`donchian_breakout`

## 策略简介

经典通道突破策略，当价格突破N日高点时做多，跌破M日低点时平仓。属于趋势跟踪类策略，适用于有明显趋势的市场。

## 适用市场

- 市场: A股、商品期货、数字货币
- 资产类型: 股票、期货、ETF、数字货币
- 时间周期: 1d (股票/期货)、1h (数字货币)

## 策略逻辑

1. 计算N日 Entry Window 最高价 (前一日最高价的滚动最大值)
2. 计算M日 Exit Window 最低价 (前一日最低价的滚动最小值)
3. 当收盘价 > N日突破阈值时，全仓做多
4. 当收盘价 < M日退出阈值时，平仓
5. 使用前向填充保持仓位直到触发退出条件

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `entry_window` | 20 | 进场窗口天数，用于计算N日最高价 |
| `exit_window` | 10 | 退出窗口天数，用于计算M日最低价 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,TSLA,BNB
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: donchian_breakout
  params:
    entry_window: 20
    exit_window: 10
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/donchian_breakout_demo
```

## 回测结果

最佳标的: ETH (Crypto - Ethereum)

| 指标 | 值 |
|------|-----|
| 总收益率 | 196.29% |
| 年化收益率 | 16.80% |
| 夏普比率 | 0.608 |
| 最大回撤 | -27.88% |
| 交易次数 | 226 |

## 图表

> 回测图表:
> - `results/charts/donchian_breakout_eth.png` - ETH权益曲线
> - `results/charts/donchian_breakout_btc.png` - BTC权益曲线
> - `results/charts/donchian_breakout_hsi.png` - HSI权益曲线

## 风险提示

1. 突破策略在震荡行情中容易产生假信号
2. 交易频率可能较低，需要耐心等待机会
3. 数字货币市场波动剧烈，止损非常重要
4. 建议结合市场环境判断使用

## 改进方向

- [ ] 增加成交量确认，避免虚假突破
- [ ] 添加波动率过滤
- [ ] 设置固定止损或追踪止损
- [ ] 优化entry/exit窗口参数