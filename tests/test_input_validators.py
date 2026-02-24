import pytest
from app.input_validators import parse_two_floats, normalize_command, is_command
from app.exceptions import InvalidInputError

@pytest.mark.parametrize(
    "tokens,expected",
    [
        (["1", "2"], (1.0, 2.0)),
        (["-1.5", "3.25"], (-1.5, 3.25)),
    ],
)
def test_parse_two_floats_ok(tokens, expected):
    assert parse_two_floats(tokens) == expected

@pytest.mark.parametrize("tokens", [[], ["1"], ["1", "2", "3"]])
def test_parse_two_floats_wrong_count(tokens):
    with pytest.raises(InvalidInputError):
        parse_two_floats(tokens)

def test_parse_two_floats_bad_number():
    with pytest.raises(InvalidInputError):
        parse_two_floats(["a", "2"])

def test_normalize_command_ok():
    assert normalize_command("  hi  ") == "hi"

def test_normalize_command_none():
    with pytest.raises(InvalidInputError):
        normalize_command(None)  # type: ignore[arg-type]

@pytest.mark.parametrize("cmd", ["help", "history", "exit", "clear", "undo", "redo", "save", "load"])
def test_is_command(cmd):
    assert is_command(cmd) is True

def test_is_command_false():
    assert is_command("add 1 2") is False