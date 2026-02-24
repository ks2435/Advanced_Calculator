import pandas as pd
from app.calculator_memento import CalculatorMemento

def test_memento_copies_df():
    df = pd.DataFrame([{"a": 1}])
    m = CalculatorMemento(history_df=df)
    df2 = m.copy_df()
    assert df2.equals(df)
    assert df2 is not df