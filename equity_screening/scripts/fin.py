import json, os, time, random, pickle
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
from yfinance.data import YfData
data=YfData()
os.makedirs("fin", exist_ok=True)
s1=json.load(open("s1.json"))
syms=[r["sym"] for r in s1]
extra=[x for x in open("extra.txt").read().split()] if os.path.exists("extra.txt") else []
syms=list(dict.fromkeys(syms+extra))
def work(s):
    fn=f"fin/{s}.pkl"
    if os.path.exists(fn): return s,"cached"
    for a in range(3):
        try:
            t=yf.Ticker(s)
            d={}
            d["is"]=t.income_stmt
            d["bs"]=t.balance_sheet
            d["cf"]=t.cashflow
            d["qcf"]=t.quarterly_cashflow
            d["qis"]=t.quarterly_income_stmt
            try:
                r=data.get_raw_json(f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{s}", params={"modules":"earningsHistory,calendarEvents,netSharePurchaseActivity,assetProfile","formatted":"false","symbol":s})
                d["qs"]=r["quoteSummary"]["result"][0]
            except Exception as e:
                d["qs"]={}
            pickle.dump(d,open(fn,"wb"))
            return s,"ok"
        except Exception as e:
            time.sleep(2**a+random.random()); err=str(e)
    return s,"fail "+err[:80]
with ThreadPoolExecutor(6) as ex:
    fs=[ex.submit(work,s) for s in syms]
    for i,f in enumerate(as_completed(fs)):
        s,st=f.result()
        if not st in("ok","cached"): print(s,st,flush=True)
        if i%50==0: print(i,flush=True)
print("done")
