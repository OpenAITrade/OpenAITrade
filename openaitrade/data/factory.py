from openaitrade.data.base import CsvAdapter, SyntheticAdapter
from openaitrade.data.yfinance_adapter import YFinanceAdapter
from openaitrade.data.akshare_adapter import AKShareAdapter
from openaitrade.data.baostock_adapter import BaoStockAdapter
from openaitrade.data.ccxt_adapter import CCXTAdapter
from openaitrade.data.openbb_adapter import OpenBBAdapter

ADAPTERS = {
    'synthetic': SyntheticAdapter,
    'csv': CsvAdapter,
    'yfinance': YFinanceAdapter,
    'akshare': AKShareAdapter,
    'baostock': BaoStockAdapter,
    'ccxt': CCXTAdapter,
    'openbb': OpenBBAdapter,
}

def create_data_adapter(name: str, **kwargs):
    name=name.lower()
    if name not in ADAPTERS:
        raise ValueError(f'Unknown data adapter: {name}. Available: {list(ADAPTERS)}')
    return ADAPTERS[name](**kwargs)
