import pandas as pd, numpy as np, json
d=pd.read_pickle('final.pkl')
d['tb']=d.B+d.C
x=d[~d.peak].sort_values(['final','tb'],ascending=False).copy(); x['rank']=range(1,len(x)+1)
NM={'3017.TW':'Asia Vital Components (AVC)','5803.T':'Fujikura','6857.T':'Advantest','8035.T':'Tokyo Electron','329180.KS':'HD현대중공업','6669.TW':'Wiwynn','ENR.DE':'Siemens Energy','BESI.AS':'BE Semiconductor'}
def nm(s,r): return NM.get(s,(r['name'] or s).replace(', Inc.','').replace(' Inc.','').replace(' Corporation','').replace(' Holdings','').replace(' Ltd.','').replace(' Corp.','').strip())
def pct(v,dig=0): return '확인 불가' if v is None or v!=v else f"{v*100:.{dig}f}%"
def f1(v): return '확인 불가' if v is None or v!=v else f"{v:.1f}x"
def roic(r):
    if r.sector=='Financial Services': return f"ROE {pct(r.roe)}"
    v=r.roic_u
    if v is None or v!=v: return '확인 불가'
    return '>100%' if v>1 else pct(v)
top=x.head(20)
lines=['| 순위 | 기업 | 티커 | 유형 | Rev 2Y CAGR [C] | EPS 2Y CAGR [C] | FY+1 P/E | FY+2 P/E | PEG 2Y | ROIC [A] | Revision (FY+2 EPS 3M) | 점수 |','|---|---|---|---|---|---|---|---|---|---|---|---|']
for s,r in top.iterrows():
    e2=r.e2; note='*' if r.oneoff else ''
    lines.append(f"| {r['rank']} | {nm(s,r)} | {s} | {r['type']} | {pct(r.rc)} | {pct(e2)}{note} | {f1(r.pe1)} | {f1(r.pe2)} | {r.peg:.2f} | {roic(r)} | {int(r.rev_state)} ({pct(r.rv3m_f2,1)}) | {r.final:.1f} ({r.grade}){' '+r.alpha if r.alpha else ''} |")
open('t_top20.md','w').write('\n'.join(lines))
lines=['| 순위 | 기업 | 총점 | Growth (20) | Valuation (20) | Revision (15) | Quality (15) | Expectation Gap (10) | Catalyst (10) | Risk (10) |','|---|---|---|---|---|---|---|---|---|---|']
for s,r in top.iterrows():
    lines.append(f"| {r['rank']} | {nm(s,r)} ({s}) | **{r.final:.1f}** | {r.A:.1f} | {r.B:.1f} | {r.C:.1f} | {r.D:.1f} | {r.E:.1f} | {r.F2:.1f} | {r.G2:.1f} |")
open('t_rank.md','w').write('\n'.join(lines))
# peak trap table
p=d[d.peak].sort_values('final',ascending=False)
lines=['| 기업 | 티커 | TTM P/E | FY+1 P/E | FY+2 P/E | EPS 2Y CAGR | FY+2 EPS ÷ 과거 4년 평균 EPS | 영업이익률 TTM vs 과거 평균 | 3M 주가 | 기계적 점수 |','|---|---|---|---|---|---|---|---|---|---|']
for s,r in p.iterrows():
    omh=[v for v in (r.om_hist if isinstance(r.om_hist,list) else []) if v==v and v is not None]
    lines.append(f"| {nm(s,r)} | {s} | {f1(r.pe_ttm)} | {f1(r.pe1)} | {f1(r.pe2)} | {pct(r.ecagr2)} | {('%.1fx'%r.peak_ratio) if r.peak_ratio==r.peak_ratio and r.peak_ratio else '확인 불가'} | {pct(r.om_ttm)} vs {pct(np.mean(omh[:-1]) if len(omh)>1 else np.nan)} | {pct(r.r3m)} | {r.final:.1f} |")
open('t_peak.md','w').write('\n'.join(lines))
top.to_pickle('top20.pkl')
cols=['rank','name','sector','ind','type','P','mcap','pe_ttm','pe_ntm','pe1','pe2','comp1','comp2','rg1','rg2','rc','eg1','eg2','ecagr2','e2','peg1','peg','roic_u','ronic','fcfm_ttm','nd_ebitda','sbc_rev','sh_g','rv1m_f1','rv3m_f1','rv1m_f2','rv3m_f2','r1m','r3m','impl_g','gap','up12','up_roll','tgt','tlow','A','B','C','D','E','F2','G2','final','grade','alpha','peak','turn','oneoff','risk']
out=x[cols].copy(); out.index.name='ticker'
pk=d[d.peak].copy(); pk['rank']=None; pk=pk[cols]; pk.index.name='ticker'
pd.concat([out,pk]).round(4).to_csv('screen_full.csv')
print(open('t_top20.md').read()); print(); print(open('t_rank.md').read()); print(); print(open('t_peak.md').read())
