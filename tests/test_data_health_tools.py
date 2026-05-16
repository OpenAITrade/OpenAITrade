import time

import pandas as pd
import pytest

from openaitrade.data.base import DataSourceError, run_with_timeout


def test_run_with_timeout_returns_result():
    result = run_with_timeout(
        lambda value: value + 1,
        timeout_seconds=1.0,
        source_name="test",
        operation="unit",
        value=2,
    )
    assert result == 3


def test_run_with_timeout_raises_timeout():
    with pytest.raises(TimeoutError, match="timed out"):
        run_with_timeout(
            lambda: time.sleep(0.2),
            timeout_seconds=0.01,
            source_name="test",
            operation="unit",
        )


def test_run_with_timeout_wraps_exception():
    with pytest.raises(DataSourceError, match="failed during unit"):
        run_with_timeout(
            lambda: (_ for _ in ()).throw(ValueError("boom")),
            timeout_seconds=1.0,
            source_name="test",
            operation="unit",
        )
