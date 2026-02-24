# app/exceptions.py

class CalculatorError(Exception):
    """Base exception for calculator-related errors."""


class InvalidInputError(CalculatorError):
    """Raised when user input is invalid."""


class OperationNotFoundError(CalculatorError):
    """Raised when an operation token is not recognized."""


class DivisionByZeroError(CalculatorError):
    """Raised on attempted division by zero."""


class ConfigError(CalculatorError):
    """Raised when configuration is missing/invalid."""


class HistoryError(CalculatorError):
    """Raised when history save/load fails."""