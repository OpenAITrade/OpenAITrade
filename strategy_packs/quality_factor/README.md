# Quality Factor

## 策略ID

`quality_factor`

## 策略简介

质量因子策略，选择盈利质量高的标的。质量分数由收益风险比(R/M)衡量，即收益均值除以收益标准差，数值越高表示质量越好。

## 适用市场

- 市场: A股、US equity
- 资产类型: 股票、ETF
- 时间周期: 1d

## 策略逻辑

1. 计算每只标的日收益率序列
2. 计算N日收益均值和标准差
3. 质量分数 = 收益均值 / 收益标准差 (收益风险比)
4. 在每个时间点对所有标的质量分数排名
5. 选择排名前K的标的等权配置

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `top_k` | 10 | 选择质量分数排名前K的标的 |
| `window` | 120 | 质量和波动率计算窗口天数 |

## 回测设置

```yaml
data:
  source: synthetic
  symbols: AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,AMD,INTC
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: quality_factor
  params:
    top_k: 10
    window: 120
backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/quality_factor_demo
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

1. 质量因子在牛市中可能表现落后
2. 基于历史波动率的质量衡量可能不反映真实风险
3. 需要结合市场环境判断
4. 建议与动量或价值因子配合使用

## 改进方向

- [ ] 使用真实财务数据(ROE、毛利率等)
- [ ] 结合分析师预期数据
- [ ] 增加基本面筛选条件
- [ ] 考虑盈利可持续性评分