# Sector Rotation

## 策略ID

`sector_rotation`

## 策略简介

行业轮动策略，基于动量效应的行业层面实现。选择过去N日收益率最高的行业进行配置，属于截面动量策略的行业版本。

## 适用市场

- 市场: A股(行业ETF)、US equity(Sector ETF)
- 资产类型: 行业ETF
- 时间周期: 1d

## 策略逻辑

1. 计算各行业ETF过去N日收益率作为动量指标
2. 在每个时间点对行业动量排名
3. 选择排名前K的行业等权配置
4. 继承自TopNMomentumStrategy，逻辑一致

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `lookback` | 120 | 动量计算窗口天数 |
| `top_k` | 3 | 选择动量排名前K的行业 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: XLK,XLF,XLV,XLE,XLY,XLRE
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: sector_rotation
  params:
    lookback: 120
    top_k: 3
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/sector_rotation_demo
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

1. 行业轮动频率较低，换手率相对股票组合更低
2. 行业动量可能受市场风格影响较大
3. 极端行情下行业轮动可能失效
4. 需要注意行业间的相关性

## 改进方向

- [ ] 增加行业相关性过滤
- [ ] 结合宏观周期信号
- [ ] 动态调整动量窗口
- [ ] 加入行业趋势持续性判断