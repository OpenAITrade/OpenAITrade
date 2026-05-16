# Live Trading

Live trading is deliberately disabled by default.

Supported adapter skeletons:

- PaperBroker: local paper trading.
- CCXTBroker: crypto exchanges through CCXT.
- IBKRBroker: Interactive Brokers via ib_insync.
- FutuBroker: Futu OpenAPI.
- AlpacaBroker: Alpaca paper/live API.

Before enabling live orders, add:

1. Symbol mapping.
2. Exchange trading rules.
3. Order precision and min-notional checks.
4. RiskEngine validation.
5. Manual confirmation or signed deployment approval.
6. Full audit logging.
