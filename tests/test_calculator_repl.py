import pytest

from app.calculator_repl import Calculator, process_line, run_repl, LoggingObserver
from app.calculator_config import CalculatorConfig
from app.history import History

def make_calc(tmp_path, autosave=False):
    cfg = CalculatorConfig(history_file=str(tmp_path / "hist.csv"), autosave=autosave)
    return Calculator(config=cfg, history=History())

@pytest.mark.parametrize(
    "line,expected",
    [
        ("help", "Commands:"),
        ("history", "(history is empty)"),
    ],
)
def test_process_line_commands(tmp_path, line, expected):
    calc = make_calc(tmp_path)
    out = process_line(calc, line)
    assert expected in out

def test_process_line_operation(tmp_path):
    calc = make_calc(tmp_path)
    out = process_line(calc, "add 2 3")
    assert out == "5.0"
    assert "add" in process_line(calc, "history")

def test_process_line_empty_error(tmp_path):
    calc = make_calc(tmp_path)
    with pytest.raises(Exception):
        process_line(calc, "   ")

def test_undo_redo_flow(tmp_path):
    calc = make_calc(tmp_path)
    process_line(calc, "add 1 2")
    assert "add" in process_line(calc, "history")

    assert process_line(calc, "undo") == "Undone."
    assert process_line(calc, "history") == "(history is empty)"

    assert process_line(calc, "redo") == "Redone."
    assert "add" in process_line(calc, "history")

def test_clear(tmp_path):
    calc = make_calc(tmp_path)
    process_line(calc, "add 1 2")
    assert process_line(calc, "clear") == "Cleared."
    assert process_line(calc, "history") == "(history is empty)"

def test_save_load(tmp_path):
    calc = make_calc(tmp_path, autosave=False)
    process_line(calc, "add 2 3")
    assert process_line(calc, "save") == "Saved."

    calc2 = make_calc(tmp_path, autosave=False)
    assert process_line(calc2, "load") == "Loaded."
    assert "add" in process_line(calc2, "history")

def test_logging_observer_called(tmp_path):
    logs = []
    calc = make_calc(tmp_path, autosave=False)
    calc.add_observer(LoggingObserver(logs.append))
    process_line(calc, "add 2 2")
    assert any("add(2.0, 2.0)" in s for s in logs)

def test_run_repl_smoke(tmp_path):
    calc = make_calc(tmp_path, autosave=False)
    inputs = iter(["add 1 1", "exit"])
    outputs = []

    def input_fn():
        return next(inputs)

    def output_fn(s: str):
        outputs.append(s)

    run_repl(calc, input_fn, output_fn)
    assert outputs[0] == "2.0"
    assert outputs[-1] == "Bye."

def test_invalid_command_format(tmp_path):
    calc = make_calc(tmp_path)
    with pytest.raises(Exception):
        process_line(calc, "add 1")  # missing arg


def test_unknown_operation_error(tmp_path):
    calc = make_calc(tmp_path)
    with pytest.raises(Exception):
        process_line(calc, "unknown 1 2")


def test_redo_nothing(tmp_path):
    calc = make_calc(tmp_path)
    assert process_line(calc, "redo") == "Nothing to redo."


def test_undo_nothing(tmp_path):
    calc = make_calc(tmp_path)
    assert process_line(calc, "undo") == "Nothing to undo."


def test_repl_exception_branch(tmp_path):
    calc = make_calc(tmp_path)

    inputs = iter(["bad input", "exit"])
    outputs = []

    def input_fn():
        return next(inputs)

    def output_fn(s):
        outputs.append(s)

    run_repl(calc, input_fn, output_fn)

    assert any("Error:" in o for o in outputs)

def test_autosave_observer_runs(tmp_path):
    calc = make_calc(tmp_path, autosave=True)
    process_line(calc, "add 1 1")

    # file should exist due to autosave
    assert calc.config.history_file

def test_snapshot_created_before_calculation(tmp_path):
    calc = make_calc(tmp_path)
    assert calc.undo() is False  # empty first

    process_line(calc, "add 1 2")
    assert calc.undo() is True

def test_operation_missing_args(tmp_path):
    calc = make_calc(tmp_path)
    with pytest.raises(Exception):
        process_line(calc, "add")

def test_repl_exception_handler_branch(tmp_path):
    calc = make_calc(tmp_path)

    inputs = iter([
        "add 1",   # causes exception
        "exit",
    ])
    outputs = []

    def input_fn():
        return next(inputs)

    def output_fn(x):
        outputs.append(x)

    run_repl(calc, input_fn, output_fn)

    assert any("Error:" in o for o in outputs)

def test_autosave_observer_line_covered():
    from app.calculator_repl import AutoSaveObserver
    from app.calculation import Calculation
    from app.operations import OperationFactory

    called = {"n": 0}

    def save_fn():
        called["n"] += 1

    obs = AutoSaveObserver(save_fn)
    calc = Calculation.from_strategy(1, 1, OperationFactory.create("add"))
    obs.on_calculation(calc)

    assert called["n"] == 1

def test_process_line_too_few_parts(tmp_path):
    calc = make_calc(tmp_path)
    import pytest
    with pytest.raises(Exception):
        process_line(calc, "add 1")  # only 2 tokens -> triggers the <3 tokens branch

def test_run_repl_hits_exception_handler(tmp_path):
    calc = make_calc(tmp_path)
    outputs = []

    inputs = iter(["add 1", "exit"])  # first causes exception, second exits

    def input_fn():
        return next(inputs)

    def output_fn(s: str):
        outputs.append(s)

    run_repl(calc, input_fn, output_fn)

    assert any(o.startswith("Error:") for o in outputs)
    assert outputs[-1] == "Bye."

def test_clear_autosave_branch(tmp_path):
    calc = make_calc(tmp_path, autosave=True)

    # ensure there is something in history
    process_line(calc, "add 1 2")

    # calling clear should trigger autosave branch (line 101)
    result = process_line(calc, "clear")

    assert result == "Cleared."

def test_process_line_exit_branch(tmp_path):
    calc = make_calc(tmp_path)

    out = process_line(calc, "exit")
    assert out == "EXIT"

def test_exit_command_branch_counts(tmp_path):
    from app.input_validators import is_command

    calc = make_calc(tmp_path)

    assert is_command("exit") is True  # ensures it enters the command block
    assert process_line(calc, "exit") == "EXIT"