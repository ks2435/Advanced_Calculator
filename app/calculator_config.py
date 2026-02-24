# app/calculator_config.py
from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

from .exceptions import ConfigError


@dataclass(frozen=True)
class CalculatorConfig:
    history_file: str
    autosave: bool

    @staticmethod
    def load() -> "CalculatorConfig":
        """
        Load configuration from environment variables (dotenv supported).
        Expected:
          - CALC_HISTORY_FILE (default: calc_history.csv)
          - CALC_AUTOSAVE (default: true)
        """
        load_dotenv()

        history_file = os.getenv("CALC_HISTORY_FILE", "calc_history.csv").strip()
        if not history_file:
            raise ConfigError("CALC_HISTORY_FILE cannot be empty.")

        autosave_raw = os.getenv("CALC_AUTOSAVE", "true").strip().lower()
        if autosave_raw not in {"true", "false", "1", "0", "yes", "no"}:
            raise ConfigError("CALC_AUTOSAVE must be a boolean-like value.")

        autosave = autosave_raw in {"true", "1", "yes"}
        return CalculatorConfig(history_file=history_file, autosave=autosave)