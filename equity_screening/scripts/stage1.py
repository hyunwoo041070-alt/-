# Stage-1 growth screen: keep names with double-digit forward revenue AND EPS growth
import json
m=json.load(open("m.json"))
def ok(r):
    if r["mcap_usd"]<2e9 or r["adv_usd"]<1e7: return False
    if (r["n2"] or 0)<3: return False
    if not(r["eps1"]>0 and r["eps2"]>0): return False
    revok=any((r.get(k) or 0)>=t for k,t in [("rev_cagr2",.12),("ntm_revg",.15),("revg2",.15)])
    epsok=(r["eps_cagr2"] or 0)>=.15 or ((r["epsg2"] or 0)>=.15 and (r["epsg1"] or 0)>=.10)
    return revok and epsok
s1=[r for r in m if ok(r)]
json.dump(s1,open("s1.json","w"))
print(len(m), len(s1))
