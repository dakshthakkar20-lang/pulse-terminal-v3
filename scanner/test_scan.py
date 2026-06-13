import yfinance as yf

symbol = "SBIN.NS"

df = yf.download(
    symbol,
    period="5d",
    interval="5m",
    progress=False
)

print(df.tail())
print("Data fetch successful")
