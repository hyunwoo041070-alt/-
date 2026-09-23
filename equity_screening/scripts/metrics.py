import json, datetime as dt, math
TODAY=dt.date(2026,9,23)
rows=json.load(open("rows.json"))
FX=json.load(open("fx.json"))
def sd(a,b):
    try:
        if a is None or b is None or b==0: return None
        return a/b
    except: return None
out=[]
for r in rows:
    try:
        pc=r["cur"]; ec=r["eps_cur"] or pc
        f=FX.get(ec,None)/FX.get(pc,None) if ec!=pc else 1.0
        r["fxf"]=f
        for k in ["eps0","eps1","eps2","e1_30","e1_60","e1_90","e2_30","e2_60","e2_90","eps2_lo","eps2_hi","eps1_lo"]:
            if r.get(k) is not None: r[k]=r[k]*f
        r["mcap_usd"]=(r["mcap"] or 0)*FX.get(pc,1)
        r["adv_usd"]=(r["avgvol"] or 0)*(r["price"] or 0)*FX.get(pc,1)
        e0,e1,e2=r["eps0"],r["eps1"],r["eps2"]
        if None in (e1,e2,r["price"]): continue
        fe=dt.date.fromisoformat(r["fy1_end"])
        w=min(max((fe-TODAY).days/365.0,0),1)
        r["w"]=w
        r["ntm_eps"]=w*e1+(1-w)*e2
        r["pe1"]=sd(r["price"],e1) if e1>0 else None
        r["pe2"]=sd(r["price"],e2) if e2>0 else None
        r["pe_ntm"]=sd(r["price"],r["ntm_eps"]) if r["ntm_eps"]>0 else None
        r["pe_ttm_gaap"]=sd(r["price"],r["teps"]) if r["teps"] and r["teps"]>0 else None
        r["pe0"]=sd(r["price"],e0) if e0 and e0>0 else None
        r["ttm_eps_est"]=(1-w)*e1+w*e0 if e0 is not None else None
        r["pe_ttm_est"]=sd(r["price"],r["ttm_eps_est"]) if r["ttm_eps_est"] and r["ttm_eps_est"]>0 else None
        r["epsg1"]=sd(e1,e0)-1 if e0 and e0>0 else None
        r["epsg2"]=sd(e2,e1)-1 if e1>0 else None
        r["eps_cagr2"]=math.sqrt(e2/e0)-1 if e0 and e0>0 and e2>0 else None
        r0,r1,r2=r["rev0"],r["rev1"],r["rev2"]
        r["revg1"]=sd(r1,r0)-1 if r0 and r1 else None
        r["revg2"]=sd(r2,r1)-1 if r1 and r2 else None
        r["rev_cagr2"]=math.sqrt(r2/r0)-1 if r0 and r2 and r0>0 else None
        if r0 and r1 and r2:
            ttm=(1-w)*r1+w*r0; ntm=w*r1+(1-w)*r2
            r["ntm_revg"]=ntm/ttm-1
        else: r["ntm_revg"]=None
        # revisions
        r["rev1m_fy1"]=sd(e1,r["e1_30"])-1 if r["e1_30"] and r["e1_30"]>0 else None
        r["rev3m_fy1"]=sd(e1,r["e1_90"])-1 if r["e1_90"] and r["e1_90"]>0 else None
        r["rev1m_fy2"]=sd(e2,r["e2_30"])-1 if r["e2_30"] and r["e2_30"]>0 else None
        r["rev3m_fy2"]=sd(e2,r["e2_90"])-1 if r["e2_90"] and r["e2_90"]>0 else None
        r["peg1"]=r["pe_ntm"]/(r["epsg2"]*100) if r["pe_ntm"] and r["epsg2"] and r["epsg2"]>0 else None
        r["peg2"]=r["pe_ntm"]/(r["eps_cagr2"]*100) if r["pe_ntm"] and r["eps_cagr2"] and r["eps_cagr2"]>0 else None
        # dollar volume
        if r.get("avgvol") and r["price"]:
            r["adv"]=r["avgvol"]*r["price"]
        out.append(r)
    except Exception as ex:
        print(r["sym"],ex)
json.dump(out,open("m.json","w"))
print(len(out))
mis=[(r["sym"],r["cur"],r["eps_cur"]) for r in out if r["eps_cur"] and r["cur"] and r["eps_cur"]!=r["cur"]]
print(len(mis), mis[:40])
