import pytest
from app.operations import OperationFactory
from app.exceptions import OperationNotFoundError, DivisionByZeroError

@pytest.mark.parametrize(
    "token,a,b,expected",
    [
        ("add", 2, 3, 5),
        ("+", 2, 3, 5),
        ("sub", 5, 2, 3),
        ("-", 5, 2, 3),
        ("mul", 2, 4, 8),
        ("*", 2, 4, 8),
        ("div", 8, 2, 4),
        ("/", 8, 2, 4),
        ("pow", 2, 3, 8),
        ("^", 2, 3, 8),
    ],
)
def test_factory_and_execute(token, a, b, expected):
    op = OperationFactory.create(token)
    assert op.execute(a, b) == expected

def test_unknown_operation():
    with pytest.raises(OperationNotFoundError):
        OperationFactory.create("nope")

def test_division_by_zero():
    op = OperationFactory.create("div")
    with pytest.raises(DivisionByZeroError):
        op.execute(1, 0)

@pytest.mark.parametrize(
    "a,b",
    [
        (9, 2),   # sqrt(9)
        (27, 3),  # cbrt(27)
    ],
)
def test_root_ok(a, b):
    op = OperationFactory.create("root")
    res = op.execute(a, b)
    # allow float rounding
    assert round(res, 6) in {3.0}

@pytest.mark.parametrize("a,b", [(9, 0)])
def test_root_invalid(a, b):
    op = OperationFactory.create("root")
    with pytest.raises(ValueError):
        op.execute(a, b)