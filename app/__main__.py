from __future__ import annotations

from .calculator_config import CalculatorConfig
from .calculator_repl import Calculator, LoggingObserver, run_repl
from .history import History


def main() -> None:  # pragma: no cover
    cfg = CalculatorConfig.load()
    calc = Calculator(config=cfg, history=History())
    calc.add_observer(LoggingObserver(print))

    # Try loading existing history (EAFP)
    try:
        calc.load()
    except Exception:
        pass

    def input_fn() -> str:
        return input("> ")

    def output_fn(s: str) -> None:
        print(s)

    run_repl(calc, input_fn, output_fn)


if __name__ == "__main__":  # pragma: no cover
    main()
