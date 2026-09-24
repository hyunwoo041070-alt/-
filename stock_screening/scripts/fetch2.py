import yfinance as yf, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
tick=json.load(open(sys.argv[1]))
def df2(d):
    if d is None or d.empty: return None
    d=d.copy(); d.index=d.index.map(str); d.columns=d.columns.map(str)
    return json.loads(d.to_json(orient='index'))
def one(s):
    fn=f'd2/{s}.json'
    if os.path.exists(fn): return
    for a in range(3):
        try:
            t=yf.Ticker(s)
            out={'is':df2(t.income_stmt),'bs':df2(t.balance_sheet),'cf':df2(t.cashflow),
                 'qis':df2(t.quarterly_income_stmt),'qbs':df2(t.quarterly_balance_sheet),'qcf':df2(t.quarterly_cashflow)}
            json.dump(out,open(fn,'w')); return
        except Exception as e:
            err=str(e); time.sleep(5*(a+1))
    print('FAIL',s,err[:100])
with ThreadPoolExecutor(int(os.environ.get('W','3'))) as ex: list(ex.map(one,tick))
print('done',len(os.listdir('d2')))
