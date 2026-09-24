import yfinance as yf, json, os, sys, time, pandas as pd
from concurrent.futures import ThreadPoolExecutor
tick=json.load(open(sys.argv[1]))
def df2(d):
    if d is None or (hasattr(d,'empty') and d.empty): return None
    d=d.copy(); d.index=d.index.map(str); d.columns=d.columns.map(str)
    return json.loads(d.to_json(orient='index',date_format='iso'))
def one(s):
    fn=f'd1/{s}.json'
    if os.path.exists(fn): return
    for a in range(3):
        try:
            t=yf.Ticker(s)
            out={'info':t.info,'ee':df2(t.earnings_estimate),'re':df2(t.revenue_estimate),'et':df2(t.eps_trend),
                 'er':df2(t.eps_revisions),'eh':df2(t.earnings_history),'ge':df2(t.growth_estimates)}
            json.dump(out,open(fn,'w'),default=str); return
        except Exception as e:
            err=str(e); time.sleep(3*(a+1))
    print('FAIL',s,err[:100])
with ThreadPoolExecutor(int(os.environ.get("W","2"))) as ex: list(ex.map(one,tick))
print('done',len(os.listdir('d1')))
