import pandas as pd

def emd_signal(close, length=28, mult=1.0):

    avg = close.rolling(length).mean()

    abs_dev = (close - avg).abs()

    emd = abs_dev.ewm(span=length).mean()

    upper = avg + (emd * mult)
    lower = avg - (emd * mult)

    latest_close = close.iloc[-1]

    latest_upper = upper.iloc[-1]
    latest_lower = lower.iloc[-1]

    if latest_close > latest_upper:
        return 1

    elif latest_close < latest_lower:
        return -1

    return 0
