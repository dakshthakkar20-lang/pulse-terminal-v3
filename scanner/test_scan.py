import yfinance as yf

from emd import emd_signal
from supertrend import supertrend_signal
from indicators import rsi_signal
from scoring import calculate_score

symbol = "SBIN.NS"

df = yf.download(
    symbol,
    period="30d",
    interval="5m",
    progress=False
)

emd = emd_signal(df["Close"])

st = supertrend_signal(df)

rsi = rsi_signal(df["Close"])

score = calculate_score(
    emd,
    st,
    rsi
)

signal = "BUY" if score >= 70 else "SELL"

print({
    "symbol": symbol,
    "signal": signal,
    "score": score,
    "rsi": round(rsi, 2)
})
