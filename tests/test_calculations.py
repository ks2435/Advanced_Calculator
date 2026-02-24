from app.calculation import Calculation
from app.operations import OperationFactory

def test_calculation_from_strategy_has_timestamp():
    op = OperationFactory.create("add")
    c = Calculation.from_strategy(1, 2, op)
    assert c.a == 1
    assert c.b == 2
    assert c.operation == "add"
    assert c.result == 3
    assert "T" in c.timestamp_utc  # ISO-ish