from app.exceptions import (
    CalculatorError,
    InvalidInputError,
    OperationNotFoundError,
    DivisionByZeroError,
    ConfigError,
    HistoryError,
)

def test_exceptions_inherit():
    assert issubclass(InvalidInputError, CalculatorError)
    assert issubclass(OperationNotFoundError, CalculatorError)
    assert issubclass(DivisionByZeroError, CalculatorError)
    assert issubclass(ConfigError, CalculatorError)
    assert issubclass(HistoryError, CalculatorError)