# app/input_validators.py
from __future__ import annotations

from typing import Tuple

from .exceptions import InvalidInputError


def parse_two_floats(tokens: list[str]) -> Tuple[float, float]:
    """
    Parse exactly two numeric tokens into floats.
    EAFP style: attempt float conversion, then raise on failure.
    """
    if len(tokens) != 2:
        raise InvalidInputError("Expected exactly two numeric arguments.")
    try:
        return float(tokens[0]), float(tokens[1])
    except Exception as e:  # noqa: BLE001
        raise InvalidInputError(f"Invalid number(s): {tokens}") from e


def normalize_command(line: str) -> str:
    if line is None:
        raise InvalidInputError("Input cannot be None.")
    return line.strip()


def is_command(line: str) -> bool:
    return line.lower() in {
        "help",
        "history",
        "exit",
        "clear",
        "undo",
        "redo",
        "save",
        "load",
    }