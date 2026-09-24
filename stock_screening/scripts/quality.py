import json, os, pandas as pd, numpy as np
def ser(D,st,item):
    x=(D.get(st) or {}).get(item)
    if not x: return pd.Series(dtype=float)
    s=pd.Series({pd.Timestamp(k.split(' ')[0]):v for k,v in x.items()}).dropna().sort_index()
    return s
def first(D,st,items):
    for it in items:
        s=ser(D,st,it)
        if len(s): return s
    return pd.Series(dtype=float)
out={}
for fn in os.listdir('d2'):
    s=fn[:-5]; D=json.load(open('d2/'+fn)); r={}
    rev=first(D,'is',['Total Revenue','Operating Revenue']); ebit=first(D,'is',['Operating Income','EBIT'])
    tax=ser(D,'is','Tax Rate For Calcs'); ic=first(D,'bs',['Invested Capital']); cash=first(D,'bs',['Cash Cash Equivalents And Short Term Investments','Cash And Cash Equivalents'])
    qrev=first(D,'qis',['Total Revenue','Operating Revenue']); qebit=first(D,'qis',['Operating Income','EBIT'])
    qfcf=ser(D,'qcf','Free Cash Flow'); qsbc=ser(D,'qcf','Stock Based Compensation'); qni=first(D,'qis',['Net Income Common Stockholders','Net Income'])
    qcap=ser(D,'qcf','Capital Expenditure'); qacq=ser(D,'qcf','Purchase Of Business')
    qic=first(D,'qbs',['Invested Capital']); qcash=first(D,'qbs',['Cash Cash Equivalents And Short Term Investments','Cash And Cash Equivalents'])
    qsh=first(D,'qis',['Diluted Average Shares','Basic Average Shares']); ash=first(D,'is',['Diluted Average Shares','Basic Average Shares'])
    qar=first(D,'qbs',['Accounts Receivable','Receivables']); qinv=ser(D,'qbs','Inventory')
    fcf=ser(D,'cf','Free Cash Flow'); sbc=ser(D,'cf','Stock Based Compensation')
    def t4(x): return x.iloc[-4:].sum() if len(x)>=4 else None
    def tr(t):
        return float(min(0.30,max(0.10,t))) if t==t and t is not None else 0.21
    trate=tr(tax.iloc[-1]) if len(tax) else 0.21
    # annual NOPAT and IC ex cash
    icx=(ic-cash.reindex(ic.index).fillna(0)) if len(ic) else pd.Series(dtype=float)
    nop=ebit*(1-trate)
    # TTM
    ttm_rev=t4(qrev); ttm_ebit=t4(qebit); ttm_fcf=t4(qfcf); ttm_sbc=t4(qsbc); ttm_ni=t4(qni); ttm_cap=t4(qcap); ttm_acq=t4(qacq)
    qicx=(qic-qcash.reindex(qic.index).fillna(0)).dropna() if len(qic) else pd.Series(dtype=float)
    if ttm_ebit is not None and len(qicx):
        icb=qicx.iloc[-5] if len(qicx)>=5 else (icx.iloc[-1] if len(icx) else qicx.iloc[0])
        avgic=(qicx.iloc[-1]+icb)/2
        r['roic']=ttm_ebit*(1-trate)/avgic if avgic>0 else None
        r['ic_neg']=avgic<=0
    # annual ROIC history
    ar=[]
    for k in range(1,len(icx)):
        d=icx.index[k]
        if d in nop.index:
            a=(icx.iloc[k]+icx.iloc[k-1])/2
            ar.append(nop[d]/a if a>0 else None)
    r['roic_hist']=[round(x,3) if x is not None else None for x in ar]
    # RONIC: delta NOPAT (latest FY vs 2y prior) / delta IC (lagged)
    try:
        common=[d for d in nop.index if d in icx.index]
        if len(common)>=3:
            d0,d2=common[-3],common[-1]
            dn=nop[d2]-nop[d0]; di=icx[common[-2]]-icx[common[-4]] if len(common)>=4 else icx[d2]-icx[d0]
            r['ronic']=dn/di if di>0 else (np.inf if dn>0 else None)
    except Exception: pass
    # incremental op margin FY
    if len(rev)>=2 and len(ebit)>=2:
        dr=rev.iloc[-1]-rev.iloc[-2]; de=ebit.iloc[-1]-ebit.iloc[-2]
        r['inc_om']=de/dr if dr>0 else None
        r['om_fy']=ebit.iloc[-1]/rev.iloc[-1]; r['om_fy_1']=ebit.iloc[-2]/rev.iloc[-2]
    if ttm_rev:
        r['om_ttm']=ttm_ebit/ttm_rev if ttm_ebit is not None else None
        r['fcfm_ttm']=ttm_fcf/ttm_rev if ttm_fcf is not None else None
        r['sbc_rev']=ttm_sbc/ttm_rev if ttm_sbc is not None else None
        r['capex_rev']=-ttm_cap/ttm_rev if ttm_cap is not None else None
        r['acq_ttm']=-ttm_acq if ttm_acq is not None else 0
    if len(fcf)>=2 and len(rev)>=2:
        r['fcfm_fy']=fcf.iloc[-1]/rev.iloc[-1]; r['fcfm_fy_1']=fcf.iloc[-2]/rev.iloc[-2]
    if ttm_ni and ttm_fcf is not None: r['fcf_conv']=ttm_fcf/ttm_ni if ttm_ni>0 else None
    if len(qsh)>=5: r['sh_g']=qsh.iloc[-1]/qsh.iloc[-5]-1
    elif len(ash)>=2: r['sh_g']=ash.iloc[-1]/ash.iloc[-2]-1
    if len(qrev)>=5:
        r['rev_yoy_q']=qrev.iloc[-1]/qrev.iloc[-5]-1
        if len(qar)>=5 and qar.iloc[-5]>0: r['ar_g']=qar.iloc[-1]/qar.iloc[-5]-1
        if len(qinv)>=5 and qinv.iloc[-5]>0: r['inv_g']=qinv.iloc[-1]/qinv.iloc[-5]-1
    if len(rev)>=3: r['rev_g_hist']=[round(rev.iloc[k]/rev.iloc[k-1]-1,3) for k in range(1,len(rev))]
    eps=first(D,'is',['Diluted EPS','Basic EPS'])
    r['eps_hist']=[round(x,2) for x in eps.values[-4:]]
    r['om_hist']=[round(ebit[d]/rev[d],3) for d in rev.index if d in ebit.index and rev[d]][-4:]
    out[s]=r
q=pd.DataFrame(out).T
q.to_pickle('q.pkl'); print(q.shape); print(q.head(3).T)
