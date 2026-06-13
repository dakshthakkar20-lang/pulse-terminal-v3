import yfinance as yf
import pandas as pd

def emd_signal(close, length=28, mult=1.0):
    avg = close.rolling(length).mean()
    abs_dev = (close - avg).abs()
    emd = abs_dev.ewm(span=length).mean()
    upper = avg + (emd * mult)
    lower = avg - (emd * mult)
    if close.iloc[-1] > upper.iloc[-1]:
        return 1
    elif close.iloc[-1] < lower.iloc[-1]:
        return -1
    return 0

def rsi_signal(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])

def calculate_score(emd, rsi):
    score = 0
    if emd == 1:
        score += 50
    if rsi > 60:
        score += 50
    return score

symbols = [
    "SBIN.NS",
    "RELIANCE.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "ZYDUSLIFE.NS",
    "INFY.NS",
    "TCS.NS"
]

results = []

for symbol in symbols:
    try:
        df = yf.download(symbol, period="30d", interval="5m", progress=False)
        close = df["Close"].squeeze()
        emd = emd_signal(close)
        rsi = rsi_signal(close)
        score = calculate_score(emd, rsi)
        signal = "BUY" if score >= 70 else "SELL"
        results.append({
            "symbol": symbol,
            "signal": signal,
            "score": score,
            "rsi": round(rsi, 2)
        })
    except Exception as e:
        print(f"Error on {symbol}: {e}")

results.sort(key=lambda x: x["score"], reverse=True)

print("\n=== PULSE TERMINAL SIGNALS ===")
for r in results:
    print(r)
print("==============================\n")
