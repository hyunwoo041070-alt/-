import json, os, math, datetime as dt
U={x[0].replace('.','-'):x for x in json.load(open("universe_us.json"))}
px=json.load(open("px.json"))
TODAY=dt.date(2026,9,23)
def g(d,*ks):
    for k in ks:
        if d is None: return None
        d=d.get(k) if isinstance(d,dict) else None
    if isinstance(d,dict):
        d=d.get("raw")
    return d
rows=[]
for f in os.listdir("raw"):
    s=f[:-5]
    r=json.load(open("raw/"+f))
    p=r.get("price",{}); sd=r.get("summaryDetail",{}); ks=r.get("defaultKeyStatistics",{}); fd=r.get("financialData",{})
    tr={t["period"]:t for t in g(r,"earningsTrend","trend") or []}
    y0=tr.get("0y"); y1=tr.get("+1y"); q0=tr.get("0q")
    if not y0 or not y1: continue
    row=dict(sym=s, name=p.get("shortName") or p.get("longName"), cur=p.get("currency"), price=g(p,"regularMarketPrice"),
        mcap=g(p,"marketCap") or g(sd,"marketCap"), avgvol=g(sd,"averageVolume"),
        teps=g(ks,"trailingEps"), feps=g(ks,"forwardEps"), ev=g(ks,"enterpriseValue"), ev_ebitda=g(ks,"enterpriseToEbitda"),
        shares=g(ks,"sharesOutstanding"), fin_cur=fd.get("financialCurrency"),
        rev_ttm=g(fd,"totalRevenue"), gm=g(fd,"grossMargins"), om=g(fd,"operatingMargins"), ebitdam=g(fd,"ebitdaMargins"),
        fcf=g(fd,"freeCashflow"), ocf=g(fd,"operatingCashflow"), debt=g(fd,"totalDebt"), cash=g(fd,"totalCash"), ebitda=g(fd,"ebitda"),
        roe=g(fd,"returnOnEquity"), revg_q=g(fd,"revenueGrowth"), epsg_q=g(fd,"earningsGrowth"),
        fy1_end=y0.get("endDate"), fy2_end=y1.get("endDate"), eps_cur2=g(y1,"earningsEstimate","earningsCurrency"),
        eps_cur=g(y0,"earningsEstimate","earningsCurrency"),
        eps0=g(y0,"earningsEstimate","yearAgoEps"), eps1=g(y0,"earningsEstimate","avg"), eps2=g(y1,"earningsEstimate","avg"),
        eps1_lo=g(y0,"earningsEstimate","low"), eps2_lo=g(y1,"earningsEstimate","low"), eps2_hi=g(y1,"earningsEstimate","high"),
        n1=g(y0,"earningsEstimate","numberOfAnalysts"), n2=g(y1,"earningsEstimate","numberOfAnalysts"),
        rev0=g(y0,"revenueEstimate","yearAgoRevenue"), rev1=g(y0,"revenueEstimate","avg"), rev2=g(y1,"revenueEstimate","avg"),
        nrev=g(y1,"revenueEstimate","numberOfAnalysts"),
        e1_7=g(y0,"epsTrend","7daysAgo"), e1_30=g(y0,"epsTrend","30daysAgo"), e1_60=g(y0,"epsTrend","60daysAgo"), e1_90=g(y0,"epsTrend","90daysAgo"),
        e2_7=g(y1,"epsTrend","7daysAgo"), e2_30=g(y1,"epsTrend","30daysAgo"), e2_60=g(y1,"epsTrend","60daysAgo"), e2_90=g(y1,"epsTrend","90daysAgo"),
        up30_1=g(y0,"epsRevisions","upLast30days"), dn30_1=g(y0,"epsRevisions","downLast30days"),
        up30_2=g(y1,"epsRevisions","upLast30days"), dn30_2=g(y1,"epsRevisions","downLast30days"),
        q0_end=q0.get("endDate") if q0 else None,
    )
    u=U.get(s)
    row["sector"]=u[4] if u else "INTL"; row["industry"]=u[5] if u else ""; row["country"]=u[6] if u else s.split(".")[-1]
    row["dollar_vol"]=u[2] if u else None
    row.update({k:v for k,v in (px.get(s) or {}).items()})
    rows.append(row)
json.dump(rows,open("rows.json","w"))
print(len(rows))
