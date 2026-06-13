from ta.momentum import RSIIndicator

def rsi_signal(close):

    rsi = RSIIndicator(close, 14).rsi()

    return float(rsi.iloc[-1])
