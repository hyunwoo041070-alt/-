import yfinance as yf, json, time
from yfinance import EquityQuery as EQ
allq=[]
# split by market cap buckets to stay under paging limits
buckets=[(0,1e8),(1e8,3e8),(3e8,1e9),(1e9,2e9),(2e9,1e15)]
for lo,hi in buckets:
    q=EQ('and',[EQ('eq',['region','us']),EQ('btwn',['intradaymarketcap',lo,hi]),EQ('is-in',['exchange','NMS','NYQ','ASE','NGM','NCM','PCX','BTS'])])
    off=0
    while True:
        for a in range(4):
            try:
                r=yf.screen(q,size=250,offset=off,sortField='intradaymarketcap',sortAsc=False); break
            except Exception as e: time.sleep(5)
        allq+=r['quotes']; off+=250
        if off>=r['total'] or not r['quotes']: break
        time.sleep(0.4)
    print(lo,hi,r['total'])
d={x['symbol']:x for x in allq}
json.dump(list(d.values()),open('v2/universe_all.json','w'))
print(len(d))
