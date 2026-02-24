import os
import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigError

def test_config_defaults(monkeypatch):
    monkeypatch.delenv("CALC_HISTORY_FILE", raising=False)
    monkeypatch.delenv("CALC_AUTOSAVE", raising=False)
    cfg = CalculatorConfig.load()
    assert cfg.history_file == "calc_history.csv"
    assert cfg.autosave is True

@pytest.mark.parametrize("val,expected", [("true", True), ("false", False), ("1", True), ("0", False), ("yes", True), ("no", False)])
def test_config_autosave_variants(monkeypatch, val, expected):
    monkeypatch.setenv("CALC_HISTORY_FILE", "x.csv")
    monkeypatch.setenv("CALC_AUTOSAVE", val)
    cfg = CalculatorConfig.load()
    assert cfg.autosave is expected

def test_config_empty_history_file(monkeypatch):
    monkeypatch.setenv("CALC_HISTORY_FILE", "   ")
    monkeypatch.setenv("CALC_AUTOSAVE", "true")
    with pytest.raises(ConfigError):
        CalculatorConfig.load()

def test_config_bad_autosave(monkeypatch):
    monkeypatch.setenv("CALC_HISTORY_FILE", "x.csv")
    monkeypatch.setenv("CALC_AUTOSAVE", "maybe")
    with pytest.raises(ConfigError):
        CalculatorConfig.load()