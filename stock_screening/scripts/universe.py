import yfinance as yf, json, time
from yfinance import EquityQuery as EQ
q=EQ('and',[EQ('eq',['region','us']),EQ('gt',['intradaymarketcap',2e9]),EQ('is-in',['exchange','NMS','NYQ','ASE','NGM','NCM'])])
allq=[]
off=0
while True:
    r=yf.screen(q,size=250,offset=off,sortField='intradaymarketcap',sortAsc=False)
    allq+=r['quotes']; off+=250
    if off>=r['total']: break
    time.sleep(0.5)
json.dump(allq,open('universe.json','w'))
print(len(allq))
from collections import Counter
print(Counter(x.get('quoteType') for x in allq))
print(sum(1 for x in allq if x.get('epsForward') and x.get('epsCurrentYear')))
