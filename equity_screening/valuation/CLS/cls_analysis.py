"""Scenario, sensitivity, and reverse-DCF analysis on top of cls_dcf.py. Prints markdown-ready tables and saves results.json."""
import json, copy
from cls_dcf import *

WACC = 0.11
G_T = 0.03
res = {}

def ps(s, **kw): return run(s, wacc=kw.pop("wacc", WACC), g_T=kw.pop("g_T", G_T), **kw)["per_share"]

# 1) scenarios
sc = {}
for k, s in SCEN.items():
    r = run(s, wacc=WACC, g_T=G_T)
    ep = eps_path(s)
    sc[k] = dict(per_share=r["per_share"], ev=r["ev"], equity=r["equity"], pv_fcf=r["pv_fcf"], pv_tv=r["pv_tv"], tv_share=r["tv_share"],
                 rows=[{kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in row.items()} for row in r["rows"]],
                 eps={y: round(v["eps"], 2) for y, v in ep.items()}, prob=s["prob"])
pw = sum(sc[k]["prob"] * sc[k]["per_share"] for k in sc)
res["scenarios"] = sc; res["prob_weighted"] = pw
print(f"## Scenarios @ WACC {WACC:.1%}, g {G_T:.1%}")
for k in sc: print(f"{k}: ${sc[k]['per_share']:.0f} (EV {sc[k]['ev']:,.0f}, TV {sc[k]['tv_share']:.0%}) EPS27 {sc[k]['eps'][2027]} EPS28 {sc[k]['eps'][2028]} EPS30 {sc[k]['eps'][2030]}")
print(f"Prob-weighted ${pw:.0f} ({pw/PRICE-1:+.0%})")

# 2) sensitivity: WACC x g (Base)
waccs = [0.095, 0.10, 0.105, 0.11, 0.115, 0.12, 0.125]; gs = [0.02, 0.025, 0.03, 0.035, 0.04]
tab = {w: {g: ps(SCEN["Base"], wacc=w, g_T=g) for g in gs} for w in waccs}
res["sens_wacc_g"] = {str(w): {str(g): v for g, v in d.items()} for w, d in tab.items()}
print("\n## Base: WACC x terminal g")
print("| WACC \\ g | " + " | ".join(f"{g:.1%}" for g in gs) + " |")
for w in waccs: print(f"| {w:.1%} | " + " | ".join(f"${tab[w][g]:.0f}" for g in gs) + " |")

# 3) sensitivity: margin shift x 2028-2031 growth multiplier (Base, WACC 11%)
madds = [-0.015, -0.01, -0.005, 0.0, 0.005, 0.01, 0.015]
gms = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
def base_gm(gm):
    s = copy.deepcopy(SCEN["Base"]); s["g"] = [s["g"][0]] + [x * gm for x in s["g"][1:5]] + s["g"][5:]; return s
tab2 = {m: {gm: ps(base_gm(gm), margin_add=m) for gm in gms} for m in madds}
res["sens_margin_growth"] = {str(m): {str(g): v for g, v in d.items()} for m, d in tab2.items()}
print("\n## Base: margin shift (all yrs) x 2028-31 growth multiplier")
print("| margin Δ \\ growth × | " + " | ".join(f"{gm:.1f}x" for gm in gms) + " |")
for m in madds: print(f"| {m*100:+.1f}%p | " + " | ".join(f"${tab2[m][gm]:.0f}" for gm in gms) + " |")

# 4) reverse DCF
def solve(f, lo, hi, target=PRICE, it=60):
    flo = f(lo) - target
    for _ in range(it):
        mid = (lo + hi) / 2; fm = f(mid) - target
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return (lo + hi) / 2
rev = {}
rev["implied_wacc_base"] = solve(lambda w: ps(SCEN["Base"], wacc=w), 0.06, 0.20)
rev["implied_wacc_bull"] = solve(lambda w: ps(SCEN["Bull"], wacc=w), 0.06, 0.20)
rev["implied_wacc_bear"] = solve(lambda w: ps(SCEN["Bear"], wacc=w), 0.0305, 0.20)
rev["implied_margin_add"] = solve(lambda m: ps(SCEN["Base"], margin_add=m), -0.05, 0.08)
# uniform growth 2028-2031 (2027 fixed at +70% guidance-consistent), fade to 3% by 2035
def uni(g):
    s = copy.deepcopy(SCEN["Base"]); fade = [g - (g - 0.03) * k / 4 for k in range(1, 5)]
    s["g"] = [0.70, g, g, g, g] + fade; return s
rev["implied_g_2028_31"] = solve(lambda g: ps(uni(g)), -0.05, 0.60)
# duration: years of 20% growth after 2027 before fading 1 yr to 3%
def dur(n):
    import math
    s = copy.deepcopy(SCEN["Base"]); n_i = int(math.floor(n)); frac = n - n_i
    g = [0.70] + [0.20] * n_i + ([0.20 * frac + 0.05 * (1 - frac)] if frac > 0 else []) 
    g = (g + [0.05, 0.04, 0.035, 0.03] * 3)[:9]
    s["g"] = g; return s
durs = {n: ps(dur(n)) for n in range(0, 7)}
rev["duration_table"] = durs
rev["implied_rev_2031"] = None
for k in ["implied_wacc_base", "implied_wacc_bull", "implied_wacc_bear", "implied_margin_add", "implied_g_2028_31"]:
    print(f"{k}: {rev[k]:.4f}")
s_u = uni(rev["implied_g_2028_31"]); r_u = run(s_u, wacc=WACC); rev["implied_rev_2031"] = r_u["rows"][4]["rev"]
print("implied 2031 revenue", round(rev["implied_rev_2031"]), "base 2031", round(sc["Base"]["rows"][4]["rev"]))
print("duration (years of +20% after 2027) -> value:", {n: round(v) for n, v in durs.items()})
res["reverse"] = rev

# 5) valuation compression path at current price (Base EPS)
comp = {y: PRICE / sc["Base"]["eps"][y] for y in [2027, 2028, 2029, 2030]}
res["pe_path_base"] = comp
print("P/E at current price on Base EPS:", {y: round(v, 1) for y, v in comp.items()})
# 6) implied P/E of DCF value
for k in sc:
    print(k, "DCF value / EPS27 =", round(sc[k]["per_share"] / sc[k]["eps"][2027], 1), " / EPS28 =", round(sc[k]["per_share"] / sc[k]["eps"][2028], 1))
json.dump(res, open("results.json", "w"), indent=1, default=float)
