from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
import threading
import time
import yfinance as yf
from datetime import datetime

app = Flask(__name__)
CORS(app)

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
    "SBIN.NS", "RELIANCE.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "ZYDUSLIFE.NS", "INFY.NS", "TCS.NS"
]

def run_scanner():
    while True:
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
        output = {
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
            "signals": results
        }
        with open("signals.json", "w") as f:
            json.dump(output, f, indent=2)
        print(f"Scanner updated at {output['last_updated']}")
        time.sleep(300)

@app.route("/signals")
def get_signals():
    try:
        with open("signals.json") as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "signals not ready yet"}), 503

@app.route("/")
def index():
    return "Pulse Terminal API is running."

if __name__ == "__main__":
    t = threading.Thread(target=run_scanner, daemon=True)
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
