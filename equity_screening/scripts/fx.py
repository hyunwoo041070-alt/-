# FX rates to USD (used to convert EPS estimates reported in a different currency than the quote)
import yfinance as yf, json
curs=['CNY','ARS','CAD','GBP','EUR','KZT','JPY','BRL','UAH','CLP','KRW','INR','PEN','ZAR','AUD','MXN','DKK','CHF','TRY','HKD','SEK','TWD']
df=yf.download([c+"USD=X" for c in curs], period="5d", progress=False)["Close"]
fx={"USD":1.0}
for c in curs:
    v=df[c+"USD=X"].dropna()
    if len(v): fx[c]=float(v.iloc[-1])
fx["GBp"]=fx["GBP"]/100
json.dump(fx,open("fx.json","w"))
