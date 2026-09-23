import yfinance as yf, json, os, pandas as pd
syms=[f[:-5] for f in os.listdir("raw")]
out={}
for i in range(0,len(syms),200):
    b=syms[i:i+200]
    df=yf.download(b, period="1y", interval="1d", auto_adjust=True, progress=False, threads=True)["Close"]
    for s in b:
        if s in df:
            c=df[s].dropna()
            if len(c)>70:
                last=c.iloc[-1]
                def ch(n): 
                    return float(last/c.iloc[-1-n]-1) if len(c)>n else None
                out[s]={"last":float(last),"d":str(c.index[-1].date()),"r1m":ch(21),"r3m":ch(63),"r6m":ch(126),"r12m":float(last/c.iloc[0]-1),"hi":float(c.max())}
    print(i,len(out),flush=True)
json.dump(out,open("px.json","w"))
