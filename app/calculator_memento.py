# app/calculator_memento.py
from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class CalculatorMemento:
    """Memento Pattern: snapshot of calculator state (history dataframe)."""
    history_df: pd.DataFrame

    def copy_df(self) -> pd.DataFrame:
        return self.history_df.copy()