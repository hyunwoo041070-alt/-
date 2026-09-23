import json, math
FX=json.load(open("fx.json"))
S=json.load(open("scored.json"))
EXCL={"CDNS":"FY1/FY2 추정 기준 불일치(GAAP vs Non-GAAP) → 성장률 왜곡","GALD.SW":"FY1/FY2 추정 기준·통화 불일치 의심 → 성장률 신뢰 불가"}
FMAN={"CLS":4,"NVDA":4,"CRDO":3,"FLEX":3,"278470.KS":3,"SMTC":3,"AEIS":3,"TSEM":4,"AMD":4,"TSM":2,"JBL":3,"MKSI":3,"TTMI":3,"298040.KS":3,"MRVL":3,"AVGO":3,"RDDT":1,"HALO":2,"FTAI":2,"APP":0,"MTZ":0.5}
out=[]
for r in S:
    if r["sym"] in EXCL: r["excluded"]=EXCL[r["sym"]]
    q=r["q"]; Sc=r["S"]
    fman=FMAN.get(r["sym"],1.5)
    F=min(10,r["F_base"]+fman); Sc["F"]=round(F,1)
    tot=sum(Sc[k] for k in "ABCDEFG")
    if r["cyc"]: tot-=0.4*(Sc["A"]+Sc["B"])
    r["score"]=round(tot,1)
    g=r["score"]
    r["grade"]="S+" if g>=90 else "S" if g>=85 else "A+" if g>=80 else "A" if g>=75 else "B+" if g>=70 else "B" if g>=65 else "C" if g>=60 else "제외"
    # EV/NTM sales / rev growth
    try:
        ev=r["ev"]; fc=r.get("fin_cur") or r["cur"]
        ev_f=ev*FX.get(r["cur"],1)/FX.get(fc,1) if ev else None
        w=r["w"]; ntm_rev=w*r["rev1"]+(1-w)*r["rev2"]
        r["ev_sales_ntm"]=ev_f/ntm_rev if ev_f and ntm_rev else None
        rg=r.get("rev_cagr2") or r.get("ntm_revg")
        r["evs_g"]=r["ev_sales_ntm"]/(rg*100) if r.get("ev_sales_ntm") and rg and rg>0 else None
        r["ev_ebitda_g"]=r["ev_ebitda"]/(r["eps_cagr2"]*100) if r.get("ev_ebitda") and r.get("eps_cagr2") and r["eps_cagr2"]>0 else None
    except Exception as e: pass
    # 12m earnings-only price & bear
    pe=r["pe_ntm"]
    if pe:
        r["px12"]=r["ntm_eps_12m"]*pe
        r["up12"]=r["px12"]/r["price"]-1
        lo=r.get("eps2_lo") or r["eps2"]
        w=r["w"]
        bear_eps=w*(r.get("eps1_lo") or r["eps1"])+(1-w)*lo
        mult=0.75 if not r["cyc"] else 0.6
        r["bear_px"]=bear_eps*pe*mult
        r["down"]=r["bear_px"]/r["price"]-1
        r["rr"]=r["up12"]/abs(r["down"]) if r["down"]<0 else None
    # alpha flags
    nd=q.get("nd_ebitda")
    bs_ok= r["fin"] or nd is None or nd<3
    roic=q.get("roic") if not r["fin"] else r.get("roe")
    if q.get("roic_capped") and (q.get("roic_gross") or 0)>0.15: roic=1.0
    revpos=(r.get("rev3m_bl") or 0)>0
    revg=max([x for x in [r.get("ntm_revg"),r.get("rev_cagr2")] if x is not None] or [0])
    a1 = revg>0.20 and (r["eps_cagr2"] or 0)>0.25 and (r["pe2"] or 99)<20 and (r["peg2"] or 9)<0.8 and (roic or 0)>0.12 and revpos and (r["comp2"] or 0)>0.30 and bs_ok
    a2 = (r["eps_cagr2"] or 0)>0.30 and (r["pe2"] or 99)<15 and revpos
    r["alpha"]="★★" if a2 else "★" if a1 else ""
    out.append(r)
json.dump(out,open("final.json","w"),default=str)
live=[r for r in out if not r.get("excluded")]
live.sort(key=lambda r:-r["score"])
f=lambda x,p=1,pct=False: "-" if x is None else (f"{x*100:.0f}%" if pct else f"{x:.{p}f}")
for i,r in enumerate(live[:45]):
    Sc=r["S"]
    print(i+1,r["sym"],r["grade"],r["score"],"cyc" if r["cyc"] else "", "T" if r["turnaround"] else "", r["alpha"], "| up12",f(r.get("up12"),pct=True),"down",f(r.get("down"),pct=True),"rr",f(r.get("rr"),2),"| evs/g",f(r.get("evs_g"),2), "|",Sc)
