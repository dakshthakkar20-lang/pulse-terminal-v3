import pandas as pd

def supertrend_signal(df):

    period = 10
    multiplier = 3

    hl2 = (df["High"] + df["Low"]) / 2

    tr1 = df["High"] - df["Low"]
    tr2 = abs(df["High"] - df["Close"].shift())
    tr3 = abs(df["Low"] - df["Close"].shift())

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    upper = hl2 + multiplier * atr
    lower = hl2 - multiplier * atr

    close = df["Close"]

    if close.iloc[-1] > upper.iloc[-1]:
        return 1

    elif close.iloc[-1] < lower.iloc[-1]:
        return -1

    return 0
