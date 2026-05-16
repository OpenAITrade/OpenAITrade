# Strategy Pack 标准

每个策略应包含：

```text
strategy_id/
├─ README.md
├─ logic.md
├─ risk.md
├─ params.yaml
├─ backtest.yaml
└─ results/
```

## README 必备章节

1. 策略简介
2. 适用市场
3. 策略逻辑
4. 参数说明
5. 回测设置
6. 回测结果
7. 图表
8. 风险提示
9. 改进方向

## 回测结果必须包含

- `metrics.json`
- `equity_curve.csv`
- `trades.csv`
- `positions.csv`
- `report.html`
- `charts/equity_curve.png`
- `charts/drawdown.png`
- `charts/monthly_returns.png`
