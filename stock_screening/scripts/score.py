import pandas as pd, numpy as np, json, math
df=pd.read_pickle('m1.pkl'); q=pd.read_pickle('q.pkl')
e=df.ecagr2.fillna(df.eg2)
m=(e>=0.15)&(df.eg2>=0.10)&((df.rcagr2.fillna(0)>=0.12)|(df.rg2.fillna(0)>=0.15))&(df.pe2<=40)
df=df[m & df.index.isin(q.index) & (df.index!='2330.TW')].join(q)
def nz(x): return x is not None and not (isinstance(x,float) and math.isnan(x))
def band(x,edges,pts,default):
    if not nz(x): return default
    for e,p in zip(edges,pts):
        if x<e: return p
    return pts[-1] if len(pts)>len(edges) else pts[-1]
COMM_IND={'Oil & Gas E&P','Oil & Gas Integrated','Oil & Gas Drilling','Oil & Gas Equipment & Services','Oil & Gas Refining & Marketing','Steel','Aluminum','Copper','Gold','Silver','Other Precious Metals & Mining','Other Industrial Metals & Mining','Chemicals','Agricultural Inputs','Marine Shipping','Trucking','Residential Construction','Lumber & Wood Production','Paper & Paper Products','Coal','Uranium','Farm Products','Airlines','Building Materials'}
CYC_IND={'Semiconductors','Semiconductor Equipment & Materials','Computer Hardware','Oil & Gas E&P','Oil & Gas Integrated','Oil & Gas Drilling','Oil & Gas Equipment & Services','Oil & Gas Refining & Marketing','Oil & Gas Midstream','Steel','Aluminum','Copper','Gold','Silver','Other Precious Metals & Mining','Other Industrial Metals & Mining','Chemicals','Specialty Chemicals','Agricultural Inputs','Marine Shipping','Trucking','Residential Construction','Lumber & Wood Production','Paper & Paper Products','Coal','Uranium','Auto Manufacturers','Farm & Heavy Construction Machinery','Building Products & Equipment','Farm Products','Airlines','Metal Fabrication','Auto Parts','Packaging & Containers','Building Materials','Real Estate - Development','Recreational Vehicles','Electronic Components'}
res=[]
FXR=json.load(open('fx.json'))
for s,r in df.iterrows():
    fin = r.sector=='Financial Services'
    roic=r.roic if nz(r.roic) else (r.roic_hist[-1] if isinstance(r.roic_hist,list) and r.roic_hist and r.roic_hist[-1] is not None else None)
    eh=[x for x in (r.eps_hist if isinstance(r.eps_hist,list) else []) if nz(x)]
    midc=np.mean(eh) if eh else None
    peak_ratio=r.f2/midc if (midc and midc>0) else None
    cyc_ind = r.ind in CYC_IND
    # peak trap: cyclical industry and FY2 EPS > 2.5x mid-cycle average, or EPS history volatile with margin spike
    omh=[x for x in (r.om_hist if isinstance(r.om_hist,list) else []) if nz(x)]
    om_now=r.om_ttm if nz(r.om_ttm) else (omh[-1] if omh else None)
    om_spike=bool(omh and nz(om_now) and om_now>np.mean(omh[:-1] if len(omh)>1 else omh)+0.08)
    MEM={'MU','SNDK','WDC','STX','000660.KS','005930.KS'}
    comm = r.ind in COMM_IND
    peak = bool(s in MEM or (comm and ((om_spike and peak_ratio is not None and peak_ratio>2.0) or (midc is not None and midc<=0))))
    oneoff = bool(r.negq and nz(r.eg1) and r.eg1>0.6 and r.eg1>2*max(r.eg2,0.05))
    turn = bool((not nz(r.f0)) or r.f0<=0 or (r.f2/r.f0>4))
    bb = bool(nz(r.sh_g) and r.sh_g<-0.04)
    mna = bool(nz(r.acq_ttm) and r.mcap and r.acq_ttm*FXR.get(r.fcur,1.0)/1e9 > 0.10*r.mcap)
    e2=r.ecagr2 if nz(r.ecagr2) else r.eg2
    if oneoff: e2=r.eg2
    rc=r.rcagr2 if nz(r.rcagr2) else r.rg2
    # A growth 20
    A_rev=band(rc,[0.10,0.15,0.20,0.30],[1,3,5,6.5,8],1)
    A_eps=band(e2,[0.15,0.20,0.25,0.35],[2,4,5,6.5,8],2)
    if turn: A_eps=min(A_eps,5)
    acc=0
    if nz(r.rg1) and nz(r.rg2):
        if r.rg2>=r.rg1: acc+=2
        elif r.rg2>=0.8*r.rg1: acc+=1
        if r.rg1>0.4 and r.rg2<0.5*r.rg1: acc=0
    if nz(r.eg1) and r.eg2>=r.eg1 and not turn: acc+=1
    if nz(r.rg2) and r.eg2>r.rg2+0.03: acc+=1
    A=A_rev+A_eps+min(acc,4)
    # B valuation 20
    peg=r.peg2 if (nz(r.peg2) and not oneoff) else r.pegf
    B_pe=band(r.pe2,[10,15,20,25,30],[5,4.5,3.5,2.5,1.5,0.5],1)
    B_peg=band(peg,[0.5,0.7,1.0,1.5,2.0],[8,7,5.5,3.5,1.5,0.5],1)
    if peak or turn: B_peg*=0.6
    B_c=band(r.comp2,[0.15,0.25,0.35,0.45,0.55],[0.5,1,2,3,3.5,4],2) if nz(r.comp2) else 2
    evg=(r.ev_ebitda/(e2*100)) if nz(r.ev_ebitda) and nz(e2) and e2>0 and r.ev_ebitda>0 else None
    B_ev=band(evg,[0.5,0.8,1.2],[3,2,1,0],1)
    if fin: B_ev=1.5
    B=B_pe+B_peg+B_c+B_ev
    # C revisions 15
    C1=band(r.rv3m_f2,[-0.07,-0.03,0,0.03,0.07,0.15],[0,1,2,3,4,5,6],2)
    C2=band(r.rv1m_f2,[-0.02,-0.005,0.005,0.02,0.05],[0,1,2,3,3.5,4],2)
    C3=band(r.rv3m_f1,[-0.05,-0.01,0.01,0.05],[0,0.5,1.5,2.5,3],1.5)
    C4=2 if (nz(r.rv3m_f2) and nz(r.r3m) and r.rv3m_f2>r.r3m) else (1 if nz(r.rv3m_f2) and r.rv3m_f2>0.02 else 0)
    C=C1+C2+C3+C4
    rev_state=5 if C>=12 else 4 if C>=9 else 3 if C>=6.5 else 2 if C>=4 else 1
    # D quality 15
    if fin:
        D1=band(r.roe,[0.08,0.12,0.15,0.20],[0.5,1.5,3,4,5],2); D2=1.5; D3=2
    else:
        D1=5 if (r.ic_neg is True) else band(roic,[0.07,0.10,0.15,0.20,0.30],[0.5,1.5,3,4,5,6],2)
        ron=r.ronic
        D2=1 if not nz(ron) else (3 if ron==np.inf else band(ron,[0.05,0.10,0.15,0.25],[0,0.5,1.5,2.5,3],1))
        D3=band(r.fcfm_ttm,[0,0.05,0.10,0.20],[0,0.5,1.5,2.5,3],1)+(1 if nz(r.fcfm_ttm) and nz(r.fcfm_fy_1) and r.fcfm_ttm>=r.fcfm_fy_1 else 0)
    sbc=r.sbc_rev if nz(r.sbc_rev) else 0.03; shg=r.sh_g if nz(r.sh_g) else 0
    D4=2 if (sbc<0.03 and shg<0.01) else (1 if sbc<0.07 and shg<0.03 else 0)
    D=D1+D2+min(D3,4)+D4
    # E expectation gap 10
    gapx=(e2-r.impl_g) if oneoff else r.gap
    E=band(gapx,[-0.06,0,0.06,0.12,0.20,0.30],[1,2.5,4,5.5,7,8.5,10],3)
    if peak or turn: E*=0.6
    # F catalyst quant 7 (+3 manual later, default 1.5)
    F1=4 if (r.beats>=4 and nz(r.surp_avg) and r.surp_avg>0.05) else 3 if r.beats>=3 else 1.5 if r.beats==2 else 0.5
    up,dn=(r.up30 or 0),(r.dn30 or 0)
    F2=3 if up>2*dn and up>=2 else 2 if up>dn else 1 if up==dn else 0
    F=F1+F2+1.5
    # G risk 10
    G=10; notes=[]
    if nz(r.nd_ebitda):
        if r.nd_ebitda>4: G-=4; notes.append('ND/EBITDA>4x')
        elif r.nd_ebitda>2.5: G-=2; notes.append('ND/EBITDA>2.5x')
        elif r.nd_ebitda>1.5: G-=1
    if sbc>0.10: G-=2; notes.append('SBC>10%')
    elif sbc>0.06: G-=1
    if shg>0.05: G-=2; notes.append('희석>5%')
    elif shg>0.02: G-=1
    if nz(r.fcfm_ttm) and r.fcfm_ttm<0 and not fin: G-=2; notes.append('FCF<0')
    if nz(r.ar_g) and nz(r.rev_yoy_q) and r.ar_g>r.rev_yoy_q+0.20: G-=1; notes.append('매출채권 급증')
    if nz(r.inv_g) and nz(r.rev_yoy_q) and r.inv_g>r.rev_yoy_q+0.25: G-=1; notes.append('재고 급증')
    if peak: G-=2; notes.append('Cyclical Peak 의심')
    elif cyc_ind: G-=1
    if turn: G-=1; notes.append('Turnaround 기저효과')
    if oneoff: notes.append('FY0 일회성 저기저(정상화 성장률 적용)')
    if (not fin) and nz(roic) and roic<0.08: G-=1; notes.append('ROIC<8%')
    if nz(r.rv3m_f2) and r.rv3m_f2<-0.05: G-=1; notes.append('컨센 하향')
    if mna: G-=1; notes.append('M&A 비중 큼')
    if bb: notes.append('자사주 효과 큼')
    G=max(G,0)
    tot=A+B+C+D+E+F+G
    res.append(dict(oneoff=oneoff,sym=s,A=A,B=B,C=C,D=D,E=E,F=F,G=G,total=tot,rev_state=rev_state,roic_u=roic,peak=peak,turn=turn,cyc=cyc_ind,bb=bb,mna=mna,peak_ratio=peak_ratio,midc=midc,risk=';'.join(notes),e2=e2,rc=rc,peg=peg))
sc=pd.DataFrame(res).set_index('sym')
out=df.join(sc)
out.to_pickle('scored.pkl')
cols=['name','ind','mcap','pe_ttm','pe1','pe2','comp2','e2','rc','peg','roic_u','fcfm_ttm','rv3m_f2','r3m','gap','A','B','C','D','E','F','G','total','risk']
pd.set_option('display.width',300); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',22)
print(out.sort_values('total',ascending=False)[cols].head(70).round(2).to_string())
