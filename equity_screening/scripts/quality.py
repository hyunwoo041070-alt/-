import json, pickle, os, math
import pandas as pd
FX=json.load(open("fx.json"))
m={r["sym"]:r for r in json.load(open("m.json"))}
s1=json.load(open("s1.json"))
def v(df,row,col=0):
    try:
        if row not in df.index or df.shape[1]<=col: return None
        x=df.loc[row].iloc[col]
        return None if pd.isna(x) else float(x)
    except: return None
def first(df,rows,col=0):
    for r in rows:
        x=v(df,r,col)
        if x is not None: return x
    return None
def qsum(df,rows,n=4):
    for r in rows:
        if r in df.index:
            s=df.loc[r].iloc[:n]
            if s.notna().sum()==n: return float(s.sum())
    return None
def sdiv(a,b):
    if a is None or b is None or b==0: return None
    return a/b
Q={}
for r in s1:
    s=r["sym"]; fn=f"fin/{s}.pkl"
    if not os.path.exists(fn): continue
    d=pickle.load(open(fn,"rb"))
    IS,BS,CF,QCF,QIS=d["is"],d["bs"],d["cf"],d["qcf"],d["qis"]
    q={}
    try:
        rev=[first(IS,["Total Revenue","Operating Revenue"],i) for i in range(3)]
        oi=[first(IS,["Operating Income","Total Operating Income As Reported","EBIT"],i) for i in range(3)]
        gp=[first(IS,["Gross Profit"],i) for i in range(2)]
        pti=first(IS,["Pretax Income"]); tax=first(IS,["Tax Provision"])
        t=first(IS,["Tax Rate For Calcs"])
        if t is None or not (0.02<=t<=0.4):
            t=sdiv(tax,pti) if pti and pti>0 else None
            if t is None or not (0.02<=t<=0.4): t=0.21
        q["tax"]=t
        def ic(i):
            debt=first(BS,["Total Debt"],i) or 0
            eq=first(BS,["Total Equity Gross Minority Interest","Stockholders Equity","Common Stock Equity"],i)
            cash=first(BS,["Cash Cash Equivalents And Short Term Investments","Cash And Cash Equivalents"],i) or 0
            if eq is None: return None,None
            return debt+eq-cash, debt+eq
        ics=[ic(i) for i in range(3)]
        nopat=[x*(1-t) if x is not None else None for x in oi]
        # ROIC latest FY on avg IC ex-cash
        ic0,icg0=ics[0]; ic1,icg1=ics[1]
        if nopat[0] is not None and ic0 is not None:
            avg=(ic0+(ic1 if ic1 is not None else ic0))/2
            q["roic"]=nopat[0]/avg if avg>0 else None
            q["roic_gross"]=nopat[0]/((icg0+(icg1 if icg1 is not None else icg0))/2) if icg0 else None
            if q["roic"] is None or q["roic"]>3: q["roic_capped"]=True
        # RONIC 2y
        ic2=ics[2][0] if ics[2] else None
        if nopat[0] is not None and nopat[2] is not None and ic0 is not None and ic2 is not None:
            dn=nopat[0]-nopat[2]; dic=ic0-ic2
            q["dnopat"]=dn; q["dic"]=dic
            q["ronic"]=dn/dic if dic>0 else None
            q["ronic_nm"]= dic<=0
        elif nopat[0] is not None and nopat[1] is not None and ic0 is not None and ic1 is not None:
            dn=nopat[0]-nopat[1]; dic=ic0-ic1
            q["dnopat"]=dn; q["dic"]=dic
            q["ronic"]=dn/dic if dic>0 else None; q["ronic_nm"]= dic<=0
        # TTM
        rev_ttm=qsum(QIS,["Total Revenue","Operating Revenue"])
        oi_ttm=qsum(QIS,["Operating Income","Total Operating Income As Reported"])
        ni_ttm=qsum(QIS,["Net Income Common Stockholders","Net Income"])
        ebitda_ttm=qsum(QIS,["EBITDA","Normalized EBITDA"])
        fcf_ttm=qsum(QCF,["Free Cash Flow"])
        ocf_ttm=qsum(QCF,["Operating Cash Flow"])
        capex_ttm=qsum(QCF,["Capital Expenditure"])
        sbc_ttm=qsum(QCF,["Stock Based Compensation"])
        if fcf_ttm is None and ocf_ttm is not None and capex_ttm is not None: fcf_ttm=ocf_ttm+capex_ttm
        # annual fallbacks
        if rev_ttm is None: rev_ttm=rev[0]
        if fcf_ttm is None: fcf_ttm=first(CF,["Free Cash Flow"])
        if ni_ttm is None: ni_ttm=first(IS,["Net Income Common Stockholders","Net Income"])
        if ebitda_ttm is None: ebitda_ttm=first(IS,["EBITDA","Normalized EBITDA"])
        if capex_ttm is None: capex_ttm=first(CF,["Capital Expenditure"])
        if sbc_ttm is None: sbc_ttm=first(CF,["Stock Based Compensation"])
        if oi_ttm is None: oi_ttm=oi[0]
        q.update(rev_ttm=rev_ttm, oi_ttm=oi_ttm, ni_ttm=ni_ttm, ebitda_ttm=ebitda_ttm, fcf_ttm=fcf_ttm, capex_ttm=capex_ttm, sbc_ttm=sbc_ttm)
        q["fcf_m"]=sdiv(fcf_ttm,rev_ttm)
        q["fcf_conv"]=sdiv(fcf_ttm,ni_ttm) if ni_ttm and ni_ttm>0 else None
        q["om_ttm"]=sdiv(oi_ttm,rev_ttm)
        q["capex_int"]=sdiv(-capex_ttm if capex_ttm else None,rev_ttm)
        q["sbc_rev"]=sdiv(sbc_ttm,rev_ttm)
        if nopat[0] is not None and oi_ttm is not None and ic0 and ic0>0:
            q["roic_ttm"]=oi_ttm*(1-t)/ic0
        fcfa=[first(CF,["Free Cash Flow"],i) for i in range(3)]
        q["fcf_m_a"]=[sdiv(fcfa[i],rev[i]) for i in range(3)]
        q["om_a"]=[sdiv(oi[i],rev[i]) for i in range(3)]
        q["gm_a"]=[sdiv(gp[i],rev[i]) for i in range(2)]
        q["incr_m"]=sdiv((oi[0]-oi[1]) if None not in (oi[0],oi[1]) else None,(rev[0]-rev[1]) if None not in (rev[0],rev[1]) else None)
        q["s2c"]=sdiv(rev[0],ic0) if ic0 and ic0>0 else None
        sh=[first(IS,["Diluted Average Shares"],i) for i in range(2)]
        q["sh_g"]=sdiv(sh[0],sh[1])-1 if sh[0] and sh[1] else None
        ni=[first(IS,["Net Income Common Stockholders","Net Income"],i) for i in range(2)]
        debt=first(BS,["Total Debt"]) or 0; cash=first(BS,["Cash Cash Equivalents And Short Term Investments","Cash And Cash Equivalents"]) or 0
        q["netdebt"]=debt-cash
        q["nd_ebitda"]=sdiv(debt-cash,ebitda_ttm) if ebitda_ttm and ebitda_ttm>0 else None
        ar=[first(BS,["Accounts Receivable","Receivables"],i) for i in range(2)]
        inv=[first(BS,["Inventory"],i) for i in range(2)]
        rg=sdiv(rev[0],rev[1])-1 if rev[0] and rev[1] else None
        q["rev_g_a"]=rg
        q["ar_g"]=sdiv(ar[0],ar[1])-1 if ar[0] and ar[1] else None
        q["inv_g"]=sdiv(inv[0],inv[1])-1 if inv[0] and inv[1] else None
        acq=first(CF,["Purchase Of Business","Net Business Purchase And Sale"])
        q["acq_rev"]=sdiv(-acq if acq else 0, rev[0]) if rev[0] else None
        q["fy_a"]=str(IS.columns[0].date()) if IS.shape[1] else None
        q["rev_a"]=rev
        # adjusted TTM EPS from earningsHistory
        eh=(d.get("qs") or {}).get("earningsHistory",{}).get("history",[])
        acts=[h.get("epsActual",{}).get("raw") if isinstance(h.get("epsActual"),dict) else None for h in eh]
        cur=[h.get("currency") for h in eh]
        if len(acts)>=4 and all(a is not None for a in acts[-4:]):
            c=cur[-1] or r["eps_cur"] or r["cur"]
            f=FX.get(c,1)/FX.get(r["cur"],1) if c!=r["cur"] and c in FX and r["cur"] in FX else 1.0
            q["ttm_eps_adj"]=sum(acts[-4:])*f
            q["surprises"]=[h.get("surprisePercent",{}).get("raw") if isinstance(h.get("surprisePercent"),dict) else None for h in eh[-4:]]
        ce=(d.get("qs") or {}).get("calendarEvents",{}).get("earnings",{})
        ed=ce.get("earningsDate") or []
        q["next_earn"]=ed[0].get("fmt") if ed and isinstance(ed[0],dict) else None
        ap=(d.get("qs") or {}).get("assetProfile",{})
        q["yindustry"]=ap.get("industry"); q["ysector"]=ap.get("sector"); q["summary"]=(ap.get("longBusinessSummary") or "")[:600]
        ins=(d.get("qs") or {}).get("netSharePurchaseActivity",{})
        q["ins_net_pct"]=ins.get("netPercentInsiderShares",{}).get("raw") if isinstance(ins.get("netPercentInsiderShares"),dict) else None
        q["ins_sell_n"]=ins.get("sellInfoCount",{}).get("raw") if isinstance(ins.get("sellInfoCount"),dict) else None
    except Exception as e:
        import traceback; traceback.print_exc(); print(s)
    Q[s]=q
json.dump(Q,open("q.json","w"),default=str)
print(len(Q))
