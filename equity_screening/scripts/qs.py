import json, sys, time
from yfinance.data import YfData
data = YfData()
MODS="price,summaryDetail,defaultKeyStatistics,financialData,earningsTrend"
def qs(sym):
    url=f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{sym}"
    r=data.get_raw_json(url, params={"modules":MODS,"corsDomain":"finance.yahoo.com","formatted":"false","symbol":sym})
    return r["quoteSummary"]["result"][0]
if __name__=="__main__":
    t=time.time()
    r=qs(sys.argv[1])
    print(time.time()-t)
    print(json.dumps(r)[:3000])
