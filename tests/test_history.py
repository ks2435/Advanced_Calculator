import os
import pandas as pd
import pytest

from app.history import History
from app.calculation import Calculation
from app.exceptions import HistoryError
from app.operations import OperationFactory

def test_history_add_and_clear():
    h = History()
    assert h.df.empty
    c = Calculation.from_strategy(2, 3, OperationFactory.create("add"))
    h.add(c)
    assert len(h.df) == 1
    h.clear()
    assert h.df.empty

def test_history_save_and_load_roundtrip(tmp_path):
    h = History()
    c = Calculation.from_strategy(2, 3, OperationFactory.create("add"))
    h.add(c)

    p = tmp_path / "hist.csv"
    h.to_csv(str(p))

    h2 = History()
    h2.from_csv(str(p))
    assert len(h2.df) == 1
    assert h2.df.iloc[0]["operation"] == "add"

def test_history_load_missing_columns(tmp_path):
    p = tmp_path / "bad.csv"
    pd.DataFrame([{"x": 1}]).to_csv(p, index=False)
    h = History()
    with pytest.raises(HistoryError):
        h.from_csv(str(p))

def test_history_save_failure_raises(monkeypatch):
    h = History()
    def boom(*args, **kwargs):
        raise OSError("nope")
    monkeypatch.setattr(h._df, "to_csv", boom)
    with pytest.raises(HistoryError):
        h.to_csv("any.csv")

def test_history_load_failure(monkeypatch):
    from app.history import History

    h = History()

    def boom(*args, **kwargs):
        raise OSError("fail")

    import pandas as pd
    monkeypatch.setattr(pd, "read_csv", boom)

    with pytest.raises(Exception):
        h.from_csv("x.csv")