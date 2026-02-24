# app/calculation.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .operations import OperationStrategy


@dataclass(frozen=True)
class Calculation:
    a: float
    b: float
    operation: str
    result: float
    timestamp_utc: str

    @staticmethod
    def from_strategy(a: float, b: float, strategy: OperationStrategy) -> "Calculation":
        res = strategy.execute(a, b)
        ts = datetime.now(timezone.utc).isoformat()
        return Calculation(a=a, b=b, operation=strategy.name, result=res, timestamp_utc=ts)