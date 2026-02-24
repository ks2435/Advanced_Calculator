# app/calculator_repl.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Protocol

from .calculation import Calculation
from .calculator_config import CalculatorConfig
from .calculator_memento import CalculatorMemento
from .exceptions import InvalidInputError
from .history import History
from .input_validators import is_command, normalize_command, parse_two_floats
from .operations import OperationFactory


class Observer(Protocol):
    """Observer Pattern: observers react to new calculations."""
    def on_calculation(self, calc: Calculation) -> None: ...


class AutoSaveObserver:
    def __init__(self, save_fn: Callable[[], None]) -> None:
        self._save_fn = save_fn

    def on_calculation(self, calc: Calculation) -> None:  # pragma: no cover
        # This is intentionally light; we test via integration on Calculator.save()
        self._save_fn()


class LoggingObserver:
    def __init__(self, log_fn: Callable[[str], None]) -> None:
        self._log_fn = log_fn

    def on_calculation(self, calc: Calculation) -> None:
        self._log_fn(f"[LOG] {calc.operation}({calc.a}, {calc.b}) = {calc.result}")


@dataclass
class Calculator:
    """
    Facade Pattern: exposes a simplified interface for:
      - operation execution (Factory + Strategy)
      - history persistence (pandas)
      - observers (Observer)
      - undo/redo (Memento)
    """
    config: CalculatorConfig
    history: History

    def __post_init__(self) -> None:
        self._observers: List[Observer] = []
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []

    def add_observer(self, obs: Observer) -> None:
        self._observers.append(obs)

    def _notify(self, calc: Calculation) -> None:
        for obs in self._observers:
            obs.on_calculation(calc)

    def _snapshot(self) -> CalculatorMemento:
        return CalculatorMemento(history_df=self.history.df)

    def calculate(self, op_token: str, a: float, b: float) -> Calculation:
        # take snapshot before change for undo
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()

        strategy = OperationFactory.create(op_token)
        calc = Calculation.from_strategy(a, b, strategy)
        self.history.add(calc)

        if self.config.autosave:
            self.save()

        self._notify(calc)
        return calc

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        self._redo_stack.append(self._snapshot())
        m = self._undo_stack.pop()
        self.history._df = m.copy_df()  # internal restore
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        self._undo_stack.append(self._snapshot())
        m = self._redo_stack.pop()
        self.history._df = m.copy_df()  # internal restore
        return True

    def clear(self) -> None:
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self.history.clear()
        if self.config.autosave:
            self.save()

    def save(self) -> None:
        self.history.to_csv(self.config.history_file)

    def load(self) -> None:
        self._undo_stack.append(self._snapshot())
        self._redo_stack.clear()
        self.history.from_csv(self.config.history_file)

    def format_history(self) -> str:
        df = self.history.df
        if df.empty:
            return "(history is empty)"
        # keep it simple and deterministic for tests
        lines = []
        for _, r in df.iterrows():
            lines.append(f"{r['operation']} {r['a']} {r['b']} = {r['result']}")
        return "\n".join(lines)


HELP_TEXT = """Commands:
  help       Show this help
  history    Show calculation history
  clear      Clear history
  undo       Undo last change
  redo       Redo last undone change
  save       Save history to CSV
  load       Load history from CSV
  exit       Exit the program

Operations:
  add/+   sub/-   mul/*   div/    pow/^   root
Usage:
  <op> <a> <b>
Example:
  add 2 3
"""


def process_line(calc: Calculator, line: str) -> str:
    """
    Process one line of input; returns output string.
    Designed for testability (no direct I/O here).
    """
    s = normalize_command(line)
    if not s:
        raise InvalidInputError("Empty input.")

    low = s.lower()
    if is_command(low):
        if low == "help":
            return HELP_TEXT.strip()
        if low == "history":
            return calc.format_history()
        if low == "clear":
            calc.clear()
            return "Cleared."
        if low == "undo":
            return "Undone." if calc.undo() else "Nothing to undo."
        if low == "redo":
            return "Redone." if calc.redo() else "Nothing to redo."
        if low == "save":
            calc.save()
            return "Saved."
        if low == "load":
            calc.load()
            return "Loaded."
        if low == "exit": # pragma: no cover
            return "EXIT"
    # operation line
    parts = s.split()
    if len(parts) < 3:
        raise InvalidInputError("Expected: <op> <a> <b>")

    op = parts[0]
    a, b = parse_two_floats(parts[1:3])
    c = calc.calculate(op, a, b)
    return f"{c.result}"


def run_repl(
    calc: Calculator,
    input_fn: Callable[[], str],
    output_fn: Callable[[str], None],
) -> None:
    while True:
        try:
            line = input_fn()
            out = process_line(calc, line)
            if out == "EXIT":
                output_fn("Bye.")
                return
            output_fn(out)
        except Exception as e:  # noqa: BLE001
            output_fn(f"Error: {e}")