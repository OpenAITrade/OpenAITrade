# Broker Adapters

OpenAITrade provides a unified broker interface for paper and live trading.

## Available Adapters

| Adapter | Package | Description | Live Trading |
|---------|---------|-------------|--------------|
| `PaperBroker` | built-in | Local paper trading simulator | N/A |
| `CCXTBroker` | ccxt | Crypto exchanges (Binance, OKX, etc.) | Optional |
| `IBKRBroker` | ib_insync | Interactive Brokers | Optional |
| `FutuBroker` | futu-api | Futu OpenAPI | Optional |
| `AlpacaBroker` | alpaca-py | Alpaca US equities | Optional |

## Interface

All broker adapters implement the `BrokerAdapter` protocol:

```python
class BrokerAdapter(Protocol):
    name: str

    def get_account(self) -> dict:
        """Return account cash, positions, and PnL."""

    def get_positions(self) -> list[Position]:
        """Return current open positions."""

    def get_orders(self) -> list[dict]:
        """Return open orders."""

    def place_order(self, order: Order) -> dict:
        """Place an order. Returns order status."""

    def cancel_order(self, order_id: str) -> dict:
        """Cancel an open order."""
```

## Usage

```python
from openaitrade.broker.paper import PaperBroker, Order

broker = PaperBroker(cash=100000.0)
order = Order(symbol="AAPL", side="buy", quantity=100, price=150.0)
result = broker.place_order(order)
print(result)  # {'status': 'filled', 'order': ...}
```

## Live Trading Setup

For live trading, install optional dependencies:

```bash
pip install openaitrade[brokers]
```

Before enabling live orders:

1. Add symbol mapping for your broker's conventions
2. Configure exchange trading rules (lot size, min notional)
3. Set order precision and price limits
4. Enable RiskEngine validation
5. Add audit logging

**Note:** Live trading is disabled by default. All brokers run in dry-run mode unless explicitly configured.