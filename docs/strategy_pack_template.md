# {strategy_name}

## 策略ID

`{strategy_id}`

## 策略简介

{short_description}

## 适用市场

- 市场: {markets}
- 资产类型: {asset_types}
- 时间周期: {timeframes}

## 策略逻辑

{strategy_logic_description}

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
{% for param, desc in params.items() %}| `{param}` | {default} | {description} |
{% endfor %}

## 回测设置

```yaml
data:
  source: synthetic
  symbols: {symbols}
  start: '2020-01-01'
  end: '2023-12-31'
strategy:
  id: {strategy_id}
  params:
{param_block}backtest:
  initial_cash: 100000
  commission_rate: 0.0005
  slippage_rate: 0.0002
output_dir: results/{strategy_id}_demo
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

本策略模板仅供研究使用。实盘部署前请验证：
1. 数据质量和流动性
2. 交易成本和滑点建模
3. 券商订单映射规则
4. 风险管理机制

## 改进方向

- [ ] 添加基本面过滤条件
- [ ] 优化参数选择逻辑
- [ ] 增加风控规则（如止损、仓位限制）
- [ ] 支持多时间周期信号聚合