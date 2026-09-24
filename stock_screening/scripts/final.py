import pandas as pd, numpy as np, json, math
d=pd.read_pickle('scored.pkl')
FX=json.load(open('fx.json'))
# analyst overlays: F manual (0-3, replaces default 1.5), G manual (-2..0), type
OV={
'NVDA':(3,0,'Earnings Revision Play / High-Growth at Fair Price'),
'CLS':(3,-1,'Earnings Revision Play / Growth Inflection'),
'TSM':(2.5,-1,'Quality Compounder / GARP'),
'CIEN':(3,0,'Earnings Revision Play / Growth Inflection'),
'3017.TW':(2.5,0,'Growth Inflection / Capex-to-FCF'),
'5803.T':(1.5,-1,'Growth Inflection (가이던스 신뢰도 낮음)'),
'AMD':(3,0,'Earnings Revision Play / Momentum-supported Fundamental'),
'TER':(1.5,0,'Earnings Revision Play (분기 감속)'),
'RDDT':(2,-0.5,'High-Growth at Fair Price'),
'ENVA':(2,-1,'GARP / Earnings Revision'),
'HRMY':(1.5,-2,'Deep Value (단일제품 LOE 위험)'),
'FLEX':(2,0,'GARP / Margin Expansion'),
'6857.T':(2,0,'Quality Compounder / Earnings Revision'),
'ONTO':(2.5,0,'Growth Inflection / Earnings Revision'),
'LITE':(3,-1,'Earnings Revision Play / Growth Inflection'),
'WDC':(1.5,0,'Cyclical Recovery (Peak 의심)'),
'FIX':(2.5,0,'Quality Compounder / Growth'),
'AMAT':(2,0,'Cyclical Recovery / GARP'),
'TSEM':(3,0,'Growth Inflection / Capex-to-FCF'),
'CRDO':(1,-1,'High-Growth at Fair Price (모멘텀 훼손)'),
'NESR':(1,-1,'Cyclical Recovery / Turnaround'),
'MKSI':(1.5,0,'GARP / Deleveraging'),
'VRT':(2,0,'Quality Growth'),
'329180.KS':(2,-1,'Cyclical Recovery / Earnings Revision'),
'8035.T':(2,0,'Cyclical Recovery / Earnings Revision'),
'6669.TW':(2,-1,'Growth Inflection (운전자본 부담)'),
'BESI.AS':(2,0,'Growth Inflection'),
'LLY':(2.5,0,'Quality Compounder'),
'ENR.DE':(2,0,'Margin Expansion / Turnaround'),
'AEIS':(2,0,'Earnings Revision Play'),
'DAVE':(1.5,0,'GARP'),
'LRCX':(2,0,'Cyclical Recovery / Quality'),
'STX':(1.5,0,'Cyclical Recovery (Peak 의심)'),
'APH':(2,0,'Quality Compounder'),
'AVGO':(3,-1,'High-Growth at Fair Price'),
'APP':(0.5,-1,'Value Trap Candidate (소송/모델 둔화)'),
'HALO':(2,-1,'GARP (특허 만료 위험)'),
'NU':(2,0,'GARP'),
'SNDK':(1.5,0,'Cyclical Peak Trap'),
'MU':(1.5,0,'Cyclical Peak Trap'),
'000660.KS':(1.5,0,'Cyclical Peak Trap'),
'005930.KS':(1.5,0,'Cyclical Peak Trap'),
'SMTC':(2,-1,'Growth Inflection'),
'TTMI':(2,0,'Growth Inflection'),
'STRL':(1.5,0,'Quality Growth (리비전 하향)'),
'MYRG':(2,0,'GARP'),
'ASM.AS':(2,0,'Quality Compounder'),
'2308.TW':(2,0,'Quality Growth'),
'SANM':(2,0,'GARP'),
'ONON':(1.5,0,'GARP'),
'RHM.DE':(2,-1,'GARP (정책 리스크)'),
'COHR':(2,-1,'Growth Inflection (희석)'),
'ASX':(2,0,'Growth Inflection'),
'KEYS':(2,0,'Earnings Revision Play'),
'JBL':(2,0,'GARP'),
}
d['Fm']=[OV.get(s,(1.5,0,''))[0] for s in d.index]; d['Gm']=[OV.get(s,(1.5,0,''))[1] for s in d.index]
d['type']=[OV.get(s,(1.5,0,''))[2] for s in d.index]
d['F2']=d.F-1.5+d.Fm; d['G2']=(d.G+d.Gm).clip(lower=0)
d['final']=d.A+d.B+d.C+d.D+d.E+d.F2+d.G2
def grade(x): return 'S+' if x>=90 else 'S' if x>=85 else 'A+' if x>=80 else 'A' if x>=75 else 'B+' if x>=70 else 'B' if x>=65 else 'C' if x>=60 else '제외'
d['grade']=d.final.map(grade)
# NTM revenue growth
fxr=[FX.get(f,1.0)/FX.get(c,1.0) if isinstance(f,str) and isinstance(c,str) else 1.0 for f,c in zip(d.fcur,[None]*len(d))]
d['ntm_rev']=d.w*d.rev1+(1-d.w)*d.rev2
# rev_ttm from info is in financial currency; estimates also -> same currency typically
d['ntm_rg']=d.ntm_rev/d.rev_ttm-1
# alpha flags
def alpha(r):
    roic=r.roic_u if r.sector!='Financial Services' else r.roe
    a=(r.rc or 0)>0.20 and r.e2>0.25 and r.pe2<20 and (r.peg or 9)<0.8 and (roic or 0)>0.12 and (r.rv3m_f2 or 0)>0 and (r.comp2 if r.comp2==r.comp2 else 0)>0.30 and r.G>=6
    aa=r.e2>0.30 and r.pe2<15 and (r.rv3m_f2 or 0)>0
    if r.peak: return 'Peak-trap(제외)' if (a or aa) else ''
    return '★★' if (aa and a) else ('★★(조건부)' if aa else ('★' if a else ''))
d['alpha']=d.apply(alpha,axis=1)
d['rev_state']=d.C.map(lambda c: 5 if c>=12 else 4 if c>=9 else 3 if c>=6.5 else 2 if c>=4 else 1)
d.to_pickle('final.pkl')
x=d.sort_values('final',ascending=False)
x['rank']=range(1,len(x)+1)
pd.set_option('display.width',260); pd.set_option('display.max_colwidth',30)
print(x[['name','type','final','grade','A','B','C','D','E','F2','G2','alpha','peak']].head(45).round(1).to_string())
