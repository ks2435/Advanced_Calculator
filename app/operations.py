# app/operations.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol, Type

from .exceptions import DivisionByZeroError, OperationNotFoundError


class OperationStrategy(Protocol):
    """Strategy Pattern: each operation is a strategy with an execute method."""
    symbol: str
    name: str

    def execute(self, a: float, b: float) -> float: ...


@dataclass(frozen=True)
class Add:
    symbol: str = "+"
    name: str = "add"

    def execute(self, a: float, b: float) -> float:
        return a + b


@dataclass(frozen=True)
class Subtract:
    symbol: str = "-"
    name: str = "sub"

    def execute(self, a: float, b: float) -> float:
        return a - b


@dataclass(frozen=True)
class Multiply:
    symbol: str = "*"
    name: str = "mul"

    def execute(self, a: float, b: float) -> float:
        return a * b


@dataclass(frozen=True)
class Divide:
    symbol: str = "/"
    name: str = "div"

    def execute(self, a: float, b: float) -> float:
        # LBYL example (look before you leap)
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return a / b


@dataclass(frozen=True)
class Power:
    symbol: str = "^"
    name: str = "pow"

    def execute(self, a: float, b: float) -> float:
        return a ** b


@dataclass(frozen=True)
class Root:
    symbol: str = "root"
    name: str = "root"

    def execute(self, a: float, b: float) -> float:
        # EAFP example: attempt, then handle invalid cases
        try:
            if b == 0:
                raise ValueError("Zeroth root undefined.")
            # nth root: a ** (1/b)
            return a ** (1.0 / b)
        except Exception as e:  # noqa: BLE001
            # wrap as ValueError for the caller to interpret if needed
            raise ValueError(f"Invalid root operation: {e}") from e


class OperationFactory:
    """Factory Pattern: build operations based on user token."""
    _registry: Dict[str, Type[OperationStrategy]] = {
        "+": Add,
        "add": Add,
        "-": Subtract,
        "sub": Subtract,
        "*": Multiply,
        "mul": Multiply,
        "/": Divide,
        "div": Divide,
        "^": Power,
        "pow": Power,
        "root": Root,
    }

    @classmethod
    def create(cls, token: str) -> OperationStrategy:
        key = token.strip().lower()
        op_cls = cls._registry.get(key)
        if not op_cls:
            raise OperationNotFoundError(f"Unknown operation: {token}")
        return op_cls()