import json, os, math, datetime as dt
s1=json.load(open("s1.json")); Q=json.load(open("q.json"))
MON={m:i for i,m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],1)}
MEM={"MU","SNDK","WDC","STX","005930.KS","000660.KS","285A.T","SIMO","009150.KS"}
CYC_IND=["Gold","Silver","Copper","Aluminum","Steel","Oil & Gas","Marine Shipping","Coal","Uranium","Other Industrial Metals","Other Precious Metals","Specialty Chemicals","Agricultural Inputs","Chemicals","Lumber","Airlines","Auto Parts","Auto Manufacturers","Recreational Vehicles","Residential Construction","Mortgage Finance","Independent Power","Building Materials","Paper","Farm","Trucking","Semiconductor Equipment","Utilities - Renewable","Solar"]
EM={"GGAL","BMA","SUPV","BBAR","YPF","PAM","TGS","CEPU","VIST","LOMA","IRS","TEO","CRESY","EDN"}
def band(x,tbl):
    if x is None: return 0
    for th,p in tbl:
        if x>=th: return p
    return 0
def band_lo(x,tbl):
    if x is None: return 0
    for th,p in tbl:
        if x<th: return p
    return 0
def fy3(r):
    fn=f"nq/{r['sym']}.json"
    if not os.path.exists(fn): return None,None
    try:
        rows=json.load(open(fn))["data"]["yearlyForecast"]["rows"]
    except: return None,None
    fe=dt.date.fromisoformat(r["fy2_end"])
    for i,x in enumerate(rows):
        mo,yr=x["fiscalEnd"].split()
        if int(yr)==fe.year and abs(MON[mo]-fe.month)<=1 and i+1<len(rows):
            z2=x["consensusEPSForecast"]; z3=rows[i+1]["consensusEPSForecast"]; n3=rows[i+1]["noOfEstimates"]
            if z2 and z2>0 and z3 and n3>=2:
                return r["eps2"]*z3/z2, n3
    return None,None
out=[]
seen=set()
for r in s1:
    if r["sym"]=="STMPA.PA": continue
    q=Q.get(r["sym"],{}); r.update({"q":q})
    # --- revenue base sanity fix (broken yearAgoRevenue, esp. Japan)
    ra=q.get("rev_a") or [None]
    try:
        fya=dt.date.fromisoformat(q.get("fy_a")) if q.get("fy_a") else None
        fe1=dt.date.fromisoformat(r["fy1_end"])
        if r["sym"].endswith(".T") and ra[0] and r["rev0"] and fya and abs((fe1-fya).days-365)<60 and abs(r["rev0"]/ra[0]-1)>0.25:
            r["rev0_fix"]=(r["rev0"],ra[0]); r["rev0"]=ra[0]
            r0,r1,r2=r["rev0"],r["rev1"],r["rev2"]; w=r["w"]
            r["revg1"]=r1/r0-1; r["rev_cagr2"]=(r2/r0)**0.5-1
            r["ntm_revg"]=(w*r1+(1-w)*r2)/((1-w)*r1+w*r0)-1
    except Exception as e: print("fix err",r["sym"],e)
    ind=(q.get("yindustry") or r.get("industry") or "")
    r["ind"]=ind
    cyc=None
    if r["sym"] in MEM: cyc="Memory/Storage cycle"
    elif r["sym"] in EM or r.get("country")=="Argentina": cyc="EM macro (Argentina)"
    elif any(k.lower() in ind.lower() for k in CYC_IND): cyc="Commodity/Cyclical: "+ind
    r["cyc"]=cyc
    fin = (q.get("ysector")=="Financial Services") or r.get("sector")=="Finance" and "Real Estate" not in (q.get("ysector") or "")
    r["fin"]=fin
    # FY3
    e3,n3=fy3(r); r["eps3"]=e3; r["n3"]=n3
    P=r["price"]
    r["pe3"]=P/e3 if e3 and e3>0 else None
    r["cagr3"]=(e3/r["eps0"])**(1/3)-1 if e3 and r["eps0"] and r["eps0"]>0 and e3>0 else None
    r["g_fwd"]=(e3/r["eps1"])**0.5-1 if e3 and e3>0 else r["epsg2"]
    # current PE on adjusted TTM
    te=q.get("ttm_eps_adj")
    if te and te>0 and r["eps1"] and 0.2<te/r["eps1"]<5: r["pe_cur"]=P/te; r["pe_cur_src"]="adjTTM"
    elif r.get("pe_ttm_est"): r["pe_cur"]=r["pe_ttm_est"]; r["pe_cur_src"]="estTTM"
    elif r.get("pe_ttm_gaap"): r["pe_cur"]=r["pe_ttm_gaap"]; r["pe_cur_src"]="GAAP"
    else: r["pe_cur"]=None; r["pe_cur_src"]=None
    pc=r["pe_cur"]
    r["comp1"]=1-r["pe1"]/pc if pc and r["pe1"] else None
    r["comp2"]=1-r["pe2"]/pc if pc and r["pe2"] else None
    r["comp3"]=1-r["pe3"]/pc if pc and r["pe3"] else None
    pe=r["pe_ntm"]
    r["peg3"]=pe/(r["cagr3"]*100) if pe and r["cagr3"] and r["cagr3"]>0 else None
    gf=r["g_fwd"]
    r["peg_fwd"]=pe/(min(gf,0.5)*100) if pe and gf and gf>0.01 else None
    # EV-based
    q2=q
    # ---------- A Growth (20)
    revg=max([x for x in [r.get("ntm_revg"),r.get("rev_cagr2")] if x is not None] or [0])
    A=band(revg,[(.30,7),(.20,5.5),(.15,4),(.10,2)])
    epsc=r["eps_cagr2"]
    turnaround = (r["eps0"] is None or r["eps0"]<=0 or (r["epsg1"] or 0)>1.5)
    r["turnaround"]=turnaround
    epsA=band(epsc,[(.35,7),(.25,5.5),(.18,4),(.12,2)])
    if turnaround: epsA=min(epsA,4)
    A+=epsA
    A+=band(r["epsg2"],[(.30,3),(.20,2),(.15,1)])
    g1,g2=r.get("revg1"),r.get("revg2")
    acc=0
    if g1 is not None and g2 is not None:
        if g2>=g1+0.03: acc=3
        elif g2>=g1-0.03 and g2>=0.15: acc=1.5
        elif g1>0.3 and g2<g1/2: acc=-2
    r["accel"]=g2-g1 if g1 is not None and g2 is not None else None
    A=max(0,min(20,A+acc))
    # ---------- B Valuation (20)
    B=band_lo(r["peg_fwd"],[(0.5,8),(0.7,6.5),(1.0,5),(1.5,3),(2.0,1.5)])
    B+=band_lo(r["pe2"],[(12,4),(15,3.5),(20,3),(25,2),(30,1),(40,.5)])
    B+=band(r["comp2"],[(.55,5),(.45,4),(.35,3),(.25,2),(.15,1)])
    B+=band_lo(r["peg2"],[(0.7,3),(1.0,2),(1.5,1)])
    B=min(20,B)
    # ---------- C Revision (15)
    def bl(a,b):
        if a is None: return b
        if b is None: return a
        return 0.35*a+0.65*b
    r["rev3m_bl"]=bl(r["rev3m_fy1"],r["rev3m_fy2"]); r["rev1m_bl"]=bl(r["rev1m_fy1"],r["rev1m_fy2"])
    C=band(r["rev3m_bl"],[(.15,6),(.08,5),(.04,4),(.01,3),(-.01,2),(-.04,1)])
    C+=band(r["rev1m_bl"],[(.05,4),(.02,3),(.005,2.5),(-.005,2),(-.02,1)])
    n2=r["n2"] or 1
    br=((r["up30_2"] or 0)-(r["dn30_2"] or 0))/n2
    r["breadth"]=br
    C+=3 if br>0.3 else 2 if br>0.1 else 1 if br>=0 else 0
    if r["rev3m_bl"] is not None and r.get("r3m") is not None:
        gap=r["rev3m_bl"]-r["r3m"]; r["rev_minus_px"]=gap
        C+=2 if gap>0.10 else 1 if gap>0 else 0
    C=min(15,C)
    rv=r["rev3m_bl"]
    r["rev_state"]=5 if rv is not None and rv>=.08 else 4 if rv is not None and rv>=.02 else 3 if rv is not None and rv>-.02 else 2 if rv is not None and rv>-.08 else 1 if rv is not None else None
    # ---------- D Quality (15)
    D=0
    if fin:
        D+=band(r.get("roe"),[(.20,4),(.15,3),(.12,2),(.08,1)])
        D+=2
    else:
        roic=q.get("roic")
        if q.get("roic_capped") and (q.get("roic_gross") or 0)>0.15: roic=1.0
        r["roic_use"]=roic
        D+=band(roic,[(.30,5),(.20,4),(.15,3),(.10,2),(.06,1)])
        ron=q.get("ronic")
        if q.get("ronic_nm") and (q.get("dnopat") or 0)>0: D+=3
        else: D+=band(ron,[(.20,3),(.10,2),(.08,1)])
        D+=band(q.get("fcf_m"),[(.25,3),(.15,2.5),(.08,2),(.03,1)])
        D+=band(q.get("fcf_conv"),[(.8,1.5),(.5,.75)])
        om=q.get("om_a") or [None,None]; gm=q.get("gm_a") or [None,None]
        if om[0] is not None and om[1] is not None and om[0]>om[1]: D+=1.5
        if gm[0] is not None and gm[1] is not None and gm[0]>gm[1]: D+=1
    sbc=q.get("sbc_rev")
    if sbc and sbc>0.10: D-=2
    elif sbc and sbc>0.05: D-=1
    if (q.get("sh_g") or 0)>0.03: D-=1
    D=max(0,min(15,D))
    # ---------- E Expectation gap (10)
    ntm=r["ntm_eps"]
    gi=None
    if ntm and ntm>0:
        gi=(P*1.10**5/(17*ntm))**0.25-1
    r["g_impl"]=gi
    gc=min(gf,0.5) if gf is not None else None
    if r["cyc"] and gc is not None: gc=min(gc,0.10)  # cyclicals: do not credit peak growth
    r["g_cons_use"]=gc
    E=0
    if gi is not None and gc is not None:
        gap=gc-gi; r["exp_gap"]=gap
        E=band(gap,[(.15,10),(.10,8),(.05,6),(0,4),(-.05,2)])
    else: r["exp_gap"]=None
    # ---------- F Catalyst (10) base (manual overlay later)
    su=q.get("surprises") or []
    beats=sum(1 for x in su if x is not None and x>0)
    F=beats*0.75  # up to 3
    avg_su=sum(x for x in su if x is not None)/max(1,len([x for x in su if x is not None])) if su else 0
    F+=1 if avg_su>0.05 else 0.5 if avg_su>0.02 else 0
    if (r["up30_2"] or 0)>(r["dn30_2"] or 0) and (r["rev1m_fy2"] or 0)>0: F+=1
    ne=q.get("next_earn")
    try:
        if ne and 0<= (dt.date.fromisoformat(ne)-dt.date(2026,9,23)).days<=60: F+=1
    except: pass
    F=min(6,F)  # base max 6; up to 4 from manual catalyst review
    r["F_base"]=F
    # ---------- G Risk (10)
    G=10
    nd=q.get("nd_ebitda")
    if not fin:
        if nd is not None and nd>4: G-=4
        elif nd is not None and nd>3: G-=2.5
        elif nd is not None and nd>2: G-=1
    if sbc and sbc>0.15: G-=2
    elif sbc and sbc>0.08: G-=1
    shg=q.get("sh_g") or 0
    if shg>0.05: G-=2
    elif shg>0.02: G-=1
    rg=q.get("rev_g_a")
    if rg is not None and q.get("ar_g") is not None and q["ar_g"]-rg>0.20: G-=1
    if rg is not None and q.get("inv_g") is not None and q["inv_g"]-rg>0.25: G-=1
    if not fin and (q.get("fcf_ttm") or 0)<0: G-=2
    if r["cyc"]: G-=2
    if (r["n2"] or 0)<5: G-=1
    if (q.get("acq_rev") or 0)>0.2: G-=1; r["mna"]=True
    G=max(0,G)
    r["S"]=dict(A=round(A,1),B=round(B,1),C=round(C,1),D=round(D,1),E=round(E,1),F=round(F,1),G=round(G,1))
    tot=A+B+C+D+E+F+G
    # cyclical haircut on growth & valuation credit (Peak trap), turnaround cap
    if r["cyc"]:
        tot-= 0.4*(A+B)
    r["score_base"]=round(tot,1)
    # earnings-only return: 12m forward NTM EPS growth at constant NTM P/E
    w=r["w"]
    r["eps3_model"]= e3 is None
    e3u=e3 if e3 else r["eps2"]*(1+min(max(r["epsg2"] or 0,0)*0.5,0.25))
    r["eps3_use"]=e3u
    ntm12=w*r["eps2"]+(1-w)*e3u
    r["ntm_eps_12m"]=ntm12
    r["eo_ret12"]=ntm12/ntm-1 if ntm and ntm>0 else None
    r["tgt12"]=ntm12*pe if pe else None
    out.append(r)
json.dump(out,open("scored.json","w"),default=str)
out.sort(key=lambda r:-r["score_base"])
def f(x,p=1,pct=False):
    if x is None: return "-"
    return f"{x*100:.0f}%" if pct else f"{x:.{p}f}"
print("rk sym name mcapB cyc | revg ntmRevG epsCAGR2 epsg2 | peCur peNTM pe2 comp2 pegF | rev1m rev3m r3m | roic fcfm | gi gc | A B C D E F G = tot")
for i,r in enumerate(out[:120]):
    q=r["q"];S=r["S"]
    print(i+1, r["sym"], (r["name"] or "")[:16].replace(" ","_"), f(r["mcap_usd"]/1e9,0), "C" if r["cyc"] else ("T" if r["turnaround"] else "."), "|", f(r["rev_cagr2"],pct=True), f(r["ntm_revg"],pct=True), f(r["eps_cagr2"],pct=True), f(r["epsg2"],pct=True),"|", f(r["pe_cur"]), f(r["pe_ntm"]), f(r["pe2"]), f(r["comp2"],pct=True), f(r["peg_fwd"],2),"|", f(r["rev1m_fy2"],pct=True), f(r["rev3m_fy2"],pct=True), f(r.get("r3m"),pct=True),"|", f(q.get("roic"),pct=True), f(q.get("fcf_m"),pct=True),"|", f(r["g_impl"],pct=True), f(r["g_cons_use"],pct=True),"|", S["A"],S["B"],S["C"],S["D"],S["E"],S["F"],S["G"],"=",r["score_base"])
