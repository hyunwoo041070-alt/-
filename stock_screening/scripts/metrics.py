import json, os, math, pandas as pd, numpy as np, datetime as dt
px=pd.read_pickle('px.pkl')
TODAY=dt.datetime(2026,9,23).timestamp()
R=0.095; PET=17.0
rows=[]
FX=json.load(open('fx.json'))
def g(d,*k):
    for kk in k:
        if d is None: return None
        d=d.get(kk) if isinstance(d,dict) else None
    return d
for fn in os.listdir('d1'):
    s=fn[:-5]; D=json.load(open('d1/'+fn)); i=D['info'] or {}
    P=i.get('currentPrice') or i.get('regularMarketPrice')
    cur=g(D,'ee','0y','currency'); pc=i.get('currency') or 'USD'; k=FX.get(cur,1.0)/FX.get(pc,1.0) if (cur and cur!=pc) else 1.0
    f0=g(D,'ee','0y','yearAgoEps'); f1=g(D,'ee','0y','avg'); f2=g(D,'ee','+1y','avg')
    f0=f0*k if f0 is not None else None; f1=f1*k if f1 else f1; f2=f2*k if f2 else f2
    r0=g(D,'re','0y','yearAgoRevenue'); r1=g(D,'re','0y','avg'); r2=g(D,'re','+1y','avg')
    if not (P and f1 and f2) or f1<=0 or f2<=0: continue
    rq0=g(D,'re','0q','growth')
    if r0 and r1 and r1/r0-1>2 and (rq0 is None or rq0<1) and os.path.exists('d2/'+fn):
        try:
            tr=json.load(open('d2/'+fn))['is'].get('Total Revenue') or {}
            vals=[v for k,v in sorted(tr.items()) if v]
            r0=vals[-1] if vals and r1/vals[-1]-1<2 else None
        except Exception: r0=None
    elif r0 and r1 and r1/r0-1>2 and (rq0 is None or rq0<1): r0=None
    eh=D.get('eh') or {}
    acts=[v.get('epsActual') for k,v in sorted(eh.items())][-4:]
    acts=[a*k if a is not None else None for a in acts]
    ttm=sum(acts) if len(acts)==4 and all(a is not None for a in acts) else None
    negq=bool(f0 and f0>0 and any(a is not None and a<0 for a in acts))
    surpr=[v.get('surprisePercent') for k,v in sorted(eh.items())][-4:]
    surpr=[x for x in surpr if x is not None]
    nfy=i.get('nextFiscalYearEnd') or 0
    w=min(1,max(0,(nfy-TODAY)/(365*86400)))
    ntm=w*f1+(1-w)*f2
    et=D.get('et') or {}
    def rv(per,ago):
        c=g(et,per,'current'); o=g(et,per,ago)
        return (c/o-1) if (c and o and o>0) else None
    col=px[s].dropna() if s in px else pd.Series(dtype=float)
    def ret(n): return (col.iloc[-1]/col.iloc[-1-n]-1) if len(col)>n else None
    ltg=g(D,'ge','LTG','stockTrend')
    rq=g(D,'re','0q','growth'); rq1=g(D,'re','+1q','growth')
    mc=i.get('marketCap'); ev=i.get('enterpriseValue'); ebitda=i.get('ebitda')
    debt=i.get('totalDebt') or 0; cash=i.get('totalCash') or 0
    row=dict(sym=s,name=i.get('shortName'),sector=i.get('sector'),ind=i.get('industry'),P=P,mcap=mc*FX.get(i.get('currency') or 'USD',1.0)/1e9 if mc else None,
      adv=(i.get('averageVolume') or 0)*P*FX.get(i.get('currency') or 'USD',1.0)/1e6,
      f0=f0,f1=f1,f2=f2,ttm=ttm,w=w,ntm=ntm,
      pe_ttm=P/ttm if ttm and ttm>0 else None, pe_gaap=i.get('trailingPE'),
      pe1=P/f1, pe2=P/f2, pe_ntm=P/ntm,
      eg1=(f1/f0-1) if f0 and f0>0 else None, eg2=f2/f1-1,
      ecagr2=(math.sqrt(f2/f0)-1) if f0 and f0>0 else None,
      rg_q=i.get('revenueGrowth'), rg_0q=rq, rg_1q=rq1,
      rg1=(r1/r0-1) if r0 and r1 and r0>0 else None, rg2=(r2/r1-1) if r1 and r2 else None,
      rcagr2=(math.sqrt(r2/r0)-1) if r0 and r2 and r0>0 else None,
      rev1=r1, rev2=r2, ltg=ltg,
      rv1m_f1=rv('0y','30daysAgo'), rv3m_f1=rv('0y','90daysAgo'), rv1m_f2=rv('+1y','30daysAgo'), rv3m_f2=rv('+1y','90daysAgo'),
      up30=g(D,'er','+1y','upLast30days'), dn30=g(D,'er','+1y','downLast30days'),
      r1m=ret(21), r3m=ret(63), r12m=ret(len(col)-1) if len(col)>1 else None,
      surp_avg=np.mean(surpr) if surpr else None, beats=sum(1 for x in surpr if x>0),
      gm=i.get('grossMargins'), om=i.get('operatingMargins'), fcf=i.get('freeCashflow'), rev_ttm=i.get('totalRevenue'),
      nd_ebitda=((debt-cash)/ebitda) if ebitda and ebitda>0 else None, ev_ebitda=i.get('enterpriseToEbitda'), ev_rev=i.get('enterpriseToRevenue'),
      roe=i.get('returnOnEquity'), beta=i.get('beta'), dy=(i.get('dividendYield') or 0)/100,
      tgt=i.get('targetMeanPrice'), tlow=i.get('targetLowPrice'), thigh=i.get('targetHighPrice'), nan=i.get('numberOfAnalystOpinions'),
      n_eps=g(D,'ee','+1y','numberOfAnalysts'),negq=negq,fxk=k, country=i.get('country'),fcur=i.get('financialCurrency') or i.get('currency'), fye=dt.datetime.utcfromtimestamp(nfy).strftime('%Y-%m') if nfy else None,
      ins=i.get('heldPercentInsiders'), sbc=None)
    row['fcf_m']=row['fcf']/row['rev_ttm'] if row['fcf'] and row['rev_ttm'] else None
    row['comp1']=1-row['pe1']/row['pe_ttm'] if row['pe_ttm'] else None
    row['comp2']=1-row['pe2']/row['pe_ttm'] if row['pe_ttm'] else None
    row['peg1']=row['pe_ntm']/(row['eg1']*100) if row['eg1'] and row['eg1']>0 else None
    row['peg2']=row['pe_ntm']/(row['ecagr2']*100) if row['ecagr2'] and row['ecagr2']>0 else None
    row['pegf']=row['pe_ntm']/(row['eg2']*100) if row['eg2']>0 else None
    # implied 4y EPS CAGR from NTM such that P = EPS_ntm*(1+g)^4*PET/(1+R)^5
    row['impl_g']=(P*(1+R)**5/(ntm*PET))**(1/4)-1
    cons=row['ecagr2'] if row['ecagr2'] is not None else row['eg2']
    row['gap']=cons-row['impl_g']
    # FY3 extrapolation (M) and 12M price at constant NTM PE
    g3=min(0.30,max(0.05,0.7*row['eg2']))
    f3=f2*(1+g3); ntm12=w*f2+(1-w)*f3
    row['f3m']=f3; row['p12']=row['pe_ntm']*ntm12; row['up12']=row['p12']/P-1+row['dy']
    row['up_roll']=f2/f1-1+row['dy']
    row['bear']=row['tlow']/P-1 if row['tlow'] else None
    rows.append(row)
df=pd.DataFrame(rows).set_index('sym')
df.to_pickle('m1.pkl'); print(df.shape)
print(df[['pe_ttm','pe1','pe2','eg1','eg2','ecagr2','rg1','rg2','rv3m_f2','impl_g','gap','up12']].describe().T.round(2))
