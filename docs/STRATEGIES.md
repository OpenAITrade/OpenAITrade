# Built-in Strategy Library

This edition includes 20 strategy templates across 5 categories.

## Trend Following

- `sma_crossover`: short/long moving average crossover.
- `donchian_breakout`: channel breakout.
- `triple_ma_filter`: three moving-average regime filter.
- `atr_trailing_stop`: trend following with ATR trailing stop.

## Mean Reversion

- `bollinger_reversion`: Bollinger lower-band entry.
- `rsi_reversal`: RSI oversold/overbought reversal.
- `zscore_reversion`: rolling Z-score mean reversion.

## Momentum / Rotation

- `topn_momentum`: top-N cross-sectional momentum.
- `sector_rotation`: sector/asset rotation wrapper.
- `dual_momentum`: absolute + relative momentum.
- `low_vol_momentum`: momentum adjusted by volatility.

## Factor Investing

- `multi_factor_ranking`: generic multi-factor ranking template.
- `value_factor`: value-factor research template.
- `quality_factor`: quality-factor research template.
- `size_factor`: size-factor research template.

## Arbitrage / Market Neutral

- `pairs_trading`: pair spread Z-score.
- `basket_statarb`: basket statistical arbitrage.
- `etf_premium`: ETF premium/discount research strategy.
- `basis_arbitrage`: spot-futures basis research strategy.
- `funding_rate_arbitrage`: crypto funding-rate research strategy.

Each strategy is intentionally conservative and educational. Production usage requires data validation, survivorship-bias handling, corporate-action handling, slippage modeling and broker-specific order mapping.
