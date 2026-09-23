import json
F=json.load(open("final.json"))
live=[r for r in F if not r.get("excluded")]
live.sort(key=lambda r:(-r["score"], -(r["S"]["C"]+r["S"]["D"])))
S={r["sym"]:r for r in F}
TYPE={"CLS":"HGFP + Revision","NVDA":"HGFP + Quality Compounder","CRDO":"HGFP + Revision","FLEX":"GARP (+스핀오프)","AEIS":"Revision + Margin Exp.","SMTC":"Growth Inflection","278470.KS":"HGFP (Quality)","TSEM":"Capex→FCF Inflection","AMD":"Growth Inflection","MKSI":"GARP + Revision","TSM":"Quality Compounder","TTMI":"Earnings Revision","298040.KS":"GARP (수주잔고)","JBL":"GARP","HALO":"GARP (로열티)","DLO":"GARP","AVGO":"HGFP (Revision 정체)","IFX.DE":"Cyclical Recovery","MRVL":"Growth Inflection","PENG":"Earnings Revision"}
NAME={"CLS":"Celestica","NVDA":"NVIDIA","CRDO":"Credo Technology","FLEX":"Flex","AEIS":"Advanced Energy","SMTC":"Semtech","278470.KS":"에이피알(APR)","TSEM":"Tower Semiconductor","AMD":"AMD","MKSI":"MKS","TSM":"TSMC (ADR)","TTMI":"TTM Technologies","298040.KS":"효성중공업","JBL":"Jabil","HALO":"Halozyme","DLO":"dLocal","AVGO":"Broadcom","IFX.DE":"Infineon","MRVL":"Marvell","PENG":"Penguin Solutions"}
p=lambda x: "n/a" if x is None else f"{x*100:.0f}%"
p1=lambda x: "n/a" if x is None else f"{x*100:+.1f}%"
x1=lambda x: "n/a" if x is None else f"{x:.1f}x"
d2=lambda x: "n/a" if x is None else f"{x:.2f}"
def roic(r):
    q=r["q"]; v=q.get("roic")
    if v is None: return "n/a"
    return f"{v*100:.0f}%"
top=live[:20]
out={}
L=["| 순위 | 기업 | 티커 | 유형 | Revenue Growth (NTM) [C] | EPS CAGR 2Y (FY0→FY2) [C] | FY+1 P/E | FY+2 P/E | PEG 2Y | ROIC [A] | Revision (FY+2 EPS 3M) [C] | 점수 |","|---|---|---|---|---|---|---|---|---|---|---|---|"]
for i,r in enumerate(top):
    L.append(f"| {i+1} | {NAME[r['sym']]} | {r['sym']} | {TYPE[r['sym']]} | {p(r['ntm_revg'])} | {p(r['eps_cagr2'])} | {x1(r['pe1'])} | {x1(r['pe2'])} | {d2(r['peg2'])} | {roic(r)} | {p1(r['rev3m_fy2'])} (상태 {r['rev_state']}) | **{r['score']}** ({r['grade']}) |")
out["TOP20"]="\n".join(L)
# ranking 16
L=["| 순위 | 기업 | 총점 | Growth (20) | Valuation (20) | Revision (15) | Quality (15) | Expectation Gap (10) | Catalyst (10) | Risk (10) |","|---|---|---|---|---|---|---|---|---|---|"]
for i,r in enumerate(top):
    s=r["S"]
    L.append(f"| {i+1} | {NAME[r['sym']]} ({r['sym']}) | **{r['score']}** | {s['A']} | {s['B']} | {s['C']} | {s['D']} | {s['E']} | {s['F']} | {s['G']} |")
out["RANK16"]="\n".join(L)
# verdict 17
def absv(pe):
    if pe is None: return "확인 불가"
    return "매우 쌈" if pe<12 else "쌈" if pe<18 else "적정" if pe<25 else "비쌈" if pe<40 else "매우 비쌈"
def gav(peg):
    if peg is None: return "확인 불가"
    return "성장 대비 매우 저평가" if peg<0.5 else "성장 대비 매력적" if peg<0.8 else "성장 대비 적정" if peg<1.2 else "성장 대비 비쌈" if peg<2 else "성장 대비 극단적으로 비쌈"
def mexp(r):
    gi=r["g_impl"]; gc=r["g_fwd"]
    if gi is None or gc is None: return "확인 불가"
    if gi>=gc+0.10: return "Bull 이상 선반영"
    if gi>=gc: return "상당히 선반영"
    if ((r["pe_cur"] or 0)>45 and (r["comp2"] or 0)>0.5) or gi>=0.30: return "실적이 주가를 따라잡는 중"
    if gc-gi>=0.20: return "지나치게 낮음"
    return "적절"
L=["| 기업 | NTM P/E | Absolute Valuation | PEG (fwd) | Growth-Adjusted Valuation | 내재 EPS CAGR [I] vs 컨센서스 [C] | Market Expectations |","|---|---|---|---|---|---|---|"]
for r in top:
    L.append(f"| {NAME[r['sym']]} ({r['sym']}) | {x1(r['pe_ntm'])} | {absv(r['pe_ntm'])} | {d2(r['peg_fwd'])} | {gav(r['peg_fwd'])} | {p(r['g_impl'])} vs {p(r['g_fwd'])} | {mexp(r)} |")
out["VERDICT17"]="\n".join(L)
# 12m returns table top20
L=["| 기업 | 현재가 | NTM EPS | 12M 후 NTM EPS | FY+3 출처 | 12M 예상가 (EPS×현재 NTM P/E) [M] | Upside | Bear 가격 [M] | Bear Downside | R/R |","|---|---|---|---|---|---|---|---|---|---|"]
for r in top:
    L.append(f"| {NAME[r['sym']]} | {r['price']:,.2f} {r['cur']} | {r['ntm_eps']:,.2f} | {r['ntm_eps_12m']:,.2f} | {'[M] FY+2×(1+min(½·g,25%))' if r['eps3_model'] else '[C] Zacks 비율'} | {r['px12']:,.2f} | {p1(r['up12'])} | {r['bear_px']:,.2f} | {p1(r['down'])} | {d2(r['rr'])} |")
out["RET12"]="\n".join(L)
# alpha
L=["| 기업 | 판정 | Rev Growth | EPS CAGR 2Y | FY+2 P/E | PEG 2Y | ROIC | 3M Revision | FY+2 Compression | 비고 |","|---|---|---|---|---|---|---|---|---|---|"]
al=[r for r in F if r["alpha"] and not r.get("excluded") and not r["cyc"] and r["score"]>=65]
al.sort(key=lambda r:(r["cyc"] is not None, r["alpha"]!="★★", -r["score"]))
for r in al:
    note = "사이클 Peak 위험 → 별도(제외)" if r["cyc"] else ("적자/저기저 반등 → 신뢰도 제한" if r["turnaround"] else "")
    if r["sym"]=="HALO": note="FY+1 마일스톤 일회성 포함 → CAGR 과대, M&A(ELEKTROFI 등)"
    if r["sym"]=="YOU": note="주식수 −32% (자사주·구조 변경) → Buyback 효과 분리 필요, 커버리지 4명"
    if r["sym"]=="329180.KS": note="조선 업사이클(수주잔고 기반) — 성장률 FY+2 15%로 둔화"
    if r["sym"]=="MKSI": note="ND/EBITDA 3.7x — ★★ 조건은 충족하나 레버리지 감점"
    if not note and not r["fin"] and (r["q"].get("roic") is None or r["q"].get("roic")<0.08): note="ROIC<8%(≈WACC 이하) → 성장의 질 확인 필요"
    if r["sym"]=="TVTX": note="신약 매출 초기 흑자전환 구간, ROIC 음수 → PEG 신뢰도 낮음"
    nm=NAME.get(r["sym"], r["name"])
    L.append(f"| {nm} ({r['sym']}) | {r['alpha']} | {p(max([x for x in [r.get('ntm_revg'),r.get('rev_cagr2')] if x is not None]))} | {p(r['eps_cagr2'])} | {x1(r['pe2'])} | {d2(r['peg2'])} | {roic(r) if not r['fin'] else 'ROE '+p(r.get('roe'))} | {p1(r['rev3m_bl'])} | {p(r['comp2'])} | {note} |")
out["ALPHA"]="\n".join(L)
cy=[r for r in F if r["alpha"] and r["cyc"]]
out["ALPHA_CYC"]=", ".join(f"{r['sym']}({r['alpha']})" for r in sorted(cy,key=lambda r:-r["score"]))
json.dump(out,open("tables.json","w"),ensure_ascii=False)
for k,v in out.items(): print("=====",k); print(v)
