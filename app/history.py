# app/history.py
from __future__ import annotations

import pandas as pd

from .exceptions import HistoryError
from .calculation import Calculation


class History:
    """
    pandas-based history store.
    Columns: timestamp_utc, a, b, operation, result
    """
    COLUMNS = ["timestamp_utc", "a", "b", "operation", "result"]

    def __init__(self) -> None:
        self._df = pd.DataFrame(columns=self.COLUMNS)

    @property
    def df(self) -> pd.DataFrame:
        return self._df.copy()

    def clear(self) -> None:
        self._df = pd.DataFrame(columns=self.COLUMNS)

    def add(self, calc: Calculation) -> None:
        row = {
            "timestamp_utc": calc.timestamp_utc,
            "a": calc.a,
            "b": calc.b,
            "operation": calc.operation,
            "result": calc.result,
        }
        self._df = pd.concat([self._df, pd.DataFrame([row])], ignore_index=True)

    def to_csv(self, path: str) -> None:
        try:
            self._df.to_csv(path, index=False)
        except Exception as e:  # noqa: BLE001
            raise HistoryError(f"Failed to save history to {path}: {e}") from e

    def from_csv(self, path: str) -> None:
        try:
            df = pd.read_csv(path)
            # validate columns
            missing = [c for c in self.COLUMNS if c not in df.columns]
            if missing:
                raise HistoryError(f"History file missing columns: {missing}")
            self._df = df[self.COLUMNS].copy()
        except HistoryError:
            raise
        except Exception as e:  # noqa: BLE001
            raise HistoryError(f"Failed to load history from {path}: {e}") from e