"""Second-pass calculations: growth-adjusted valuation, time-based values,
reverse-DCF matrices, 12M scenarios. Imports the base model."""
from mu_model import (SCEN, build, eps_path, solve, PRICE, DILUTED_SH, KE, WACC, G,
                      NET_FIN, CASH_EST, OP_CASH, DEBT, OP_LEASE, CUST_DEPOSITS, FY26_REV, DPS)

res = {k: build(v) for k, v in SCEN.items()}
eps = {k: eps_path(SCEN[k], res[k]) for k in SCEN}
P = {k: SCEN[k]["prob"] for k in SCEN}

FY26_EPS = 73.09          # 4.78 + 12.20 + 25.11 + 31.00 [A+G]
TTM_EPS = 45.12           # 3.03 + 4.78 + 12.20 + 25.11 [A]
CONS_FY27 = 156.53        # [C]
CONS_NTM = 158.0          # [I] FY27 cons rolled 3 weeks
EV_MKT = PRICE * DILUTED_SH - NET_FIN

print("=== Multiples ladder (price fixed) ===")
b = res["Base"]; be = eps["Base"]
print(f"TTM P/E {PRICE/TTM_EPS:.1f}  FY26E P/E {PRICE/FY26_EPS:.1f}  NTM(cons) {PRICE/CONS_NTM:.2f}  FY27 cons {PRICE/CONS_FY27:.2f}")
ntm_base = be[0]['eps'] * 49/52 + be[1]['eps'] * 3/52
print(f"NTM base EPS {ntm_base:.1f} P/E {PRICE/ntm_base:.2f}")
for i, fy in enumerate([27, 28, 29]):
    for k in SCEN:
        print(f"  FY{fy} {k}: EPS {eps[k][i]['eps']:.1f}  P/E {PRICE/eps[k][i]['eps']:.1f}  FCF/sh {eps[k][i]['fcf_ps']:.1f} FCFy {eps[k][i]['fcf_ps']/PRICE*100:.1f}%")
for i, fy in enumerate([27, 28, 29]):
    r = b["rows"][i]
    ebitda = r["ebit"] + r["da"]
    print(f"FY{fy} Base EV/EBIT {EV_MKT/r['ebit']:.2f} EV/EBITDA {EV_MKT/ebitda:.2f} EV/Rev {EV_MKT/r['rev']:.2f}  EBITDA {ebitda:.1f}")
fy26_ebit, fy26_da = 97.1, 10.5
print(f"FY26E EV/EBIT {EV_MKT/fy26_ebit:.1f} EV/EBITDA {EV_MKT/(fy26_ebit+fy26_da):.1f}  EV/Rev {EV_MKT/FY26_REV:.2f}")
ttm_ebit, ttm_da = 59.6, 9.8
print(f"TTM EV/EBIT {EV_MKT/ttm_ebit:.1f} EV/EBITDA {EV_MKT/(ttm_ebit+ttm_da):.1f}")

print("\n=== Growth rates (Base) ===")
e27, e28, e29 = be[0]['eps'], be[1]['eps'], be[2]['eps']
g1 = e27 / FY26_EPS - 1; g2 = (e28 / FY26_EPS) ** 0.5 - 1; g3 = (e29 / FY26_EPS) ** (1/3) - 1
print(f"FY27 EPS g {g1*100:.1f}%  2Y CAGR {g2*100:.1f}%  3Y CAGR {g3*100:.1f}%  (cons FY27 g {(CONS_FY27/73.46-1)*100:.1f}%)")
pe27 = PRICE / e27
print(f"PEG1Y(cons) {PRICE/CONS_FY27/((CONS_FY27/73.46-1)*100):.3f} PEG1Y(base) {pe27/(g1*100):.3f} PEG2Y {pe27/(g2*100):.3f} PEG3Y {pe27/(g3*100):.2f}")
rv = [FY26_REV] + [r['rev'] for r in b['rows'][:3]]
eb = [fy26_ebit] + [r['ebit'] for r in b['rows'][:3]]
ed = [fy26_ebit + fy26_da] + [r['ebit'] + r['da'] for r in b['rows'][:3]]
for name, arr in [("Rev", rv), ("EBIT", eb), ("EBITDA", ed)]:
    c1 = arr[1]/arr[0]-1; c2 = (arr[2]/arr[0])**0.5-1; c3 = (arr[3]/arr[0])**(1/3)-1
    print(f"{name}: 1Y {c1*100:.1f}% 2Y {c2*100:.1f}% 3Y {c3*100:.1f}%")
fcf26 = 59.1   # 3.9 + 6.9 + 18.3 + ~30 (FQ4 guide) [A+G]
fc = [fcf26] + [e['fcf_ps'] * e['avg_sh'] for e in be[:3]]
fps = [fcf26/1.145] + [e['fcf_ps'] for e in be[:3]]
print(f"FCF 2Y CAGR {((fc[2]/fc[0])**0.5-1)*100:.1f}% 3Y {((fc[3]/fc[0])**(1/3)-1)*100:.1f}%  FCF/sh 2Y {((fps[2]/fps[0])**0.5-1)*100:.1f}% 3Y {((fps[3]/fps[0])**(1/3)-1)*100:.1f}%")
evebitda27 = EV_MKT/(b['rows'][0]['ebit']+b['rows'][0]['da'])
print(f"EV/EBITDA27 / EBITDA 2Y CAGR {evebitda27/(((ed[2]/ed[0])**0.5-1)*100):.3f}; /3Y {evebitda27/(((ed[3]/ed[0])**(1/3)-1)*100):.2f}")
evrev27 = EV_MKT/b['rows'][0]['rev']
print(f"EV/Rev27 / Rev 2Y CAGR {evrev27/(((rv[2]/rv[0])**0.5-1)*100):.3f}; /3Y {evrev27/(((rv[3]/rv[0])**(1/3)-1)*100):.3f}")
evebit27 = EV_MKT/b['rows'][0]['ebit']
print(f"EV/EBIT27 / EBIT 2Y CAGR {evebit27/(((eb[2]/eb[0])**0.5-1)*100):.3f}")

print("\n=== Mid-cycle / Normalized EPS (per CURRENT diluted share, no buyback, no windfall interest) ===")
norm = {}
for k in SCEN:
    rows = res[k]['rows']
    mid_rev = sum(r['rev'] for r in rows[2:7]) / 5          # FY29-FY33
    mid_m = sum(r['margin'] for r in rows[2:7]) / 5
    mid_eps = mid_rev * (mid_m + 0.01) * (1 - 0.16) / DILUTED_SH
    lr_m = SCEN[k]['lr_margin']
    trend_rev = rows[5]['rev']                                  # FY32
    norm_eps = trend_rev * (lr_m + 0.01) * (1 - 0.16) / DILUTED_SH
    peak = max(e['eps'] for e in eps[k])
    norm[k] = dict(mid_rev=mid_rev, mid_m=mid_m, mid_eps=mid_eps, norm_eps=norm_eps, peak=peak)
    print(f"{k}: mid-cycle rev {mid_rev:.0f} margin {mid_m*100:.1f}% EPS {mid_eps:.1f} | normalized (FY32 rev {trend_rev:.0f} x LR {lr_m*100:.0f}%) EPS {norm_eps:.1f} | peak EPS {peak:.1f}")
    print(f"   P/E on mid-cycle {PRICE/mid_eps:.1f}x, on normalized {PRICE/norm_eps:.1f}x, on peak {PRICE/peak:.1f}x")

print("\n=== Excess (above-normal) FCF during peak FY27-FY29, PV per share ===")
excess = {}
for k in SCEN:
    rows = res[k]['rows']
    normal_fcff = norm[k]['norm_eps'] * DILUTED_SH * 0.85   # ~85% conversion of normalized NOPAT
    pv = sum(max(0, rows[i]['fcff'] - normal_fcff) * (1 + WACC) ** (-((i + 1) - 0.55)) for i in range(3))
    excess[k] = pv / DILUTED_SH
    print(f"{k}: normal FCFF {normal_fcff:.1f}  PV excess {pv:.1f} -> ${excess[k]:.0f}/sh")
netfin_ps = NET_FIN / DILUTED_SH
print(f"net financial assets/sh {netfin_ps:.1f}")

print("\n=== Growth-Adjusted fair price ===")
fwdpe = {"Bear": 4.5, "Base": 6.0, "Bull": 8.5}
normpe = {"Bear": 12.0, "Base": 14.0, "Bull": 16.0}
W = (0.25, 0.20, 0.55)
ga = {}
for k in SCEN:
    a = eps[k][0]['eps'] * fwdpe[k]
    bb = eps[k][1]['eps'] * fwdpe[k] / (1 + KE) + DPS
    c = norm[k]['norm_eps'] * normpe[k] + excess[k] + netfin_ps
    ga[k] = W[0]*a + W[1]*bb + W[2]*c
    print(f"{k}: FY+1 {a:.0f} | FY+2 (disc.) {bb:.0f} | normalized {c:.0f} -> GA {ga[k]:.0f}")
ga_pw = sum(P[k]*ga[k] for k in SCEN)
print(f"GA prob-weighted {ga_pw:.0f}")

print("\n=== Relative value (peer fwd P/E on consensus NTM EPS) ===")
rel = {"Bear": 4.5*CONS_NTM, "Base": 6.2*CONS_NTM, "Bull": 8.8*CONS_NTM}
rel_pw = sum(P[k]*rel[k] for k in SCEN)
print({k: round(v) for k, v in rel.items()}, round(rel_pw))

print("\n=== Integrated (DCF 50 / GA 40 / Rel 10) ===")
wd, wg, wr = 0.50, 0.40, 0.10
integ = {k: wd*res[k]['ps'] + wg*ga[k] + wr*rel[k] for k in SCEN}
dcf_pw = sum(P[k]*res[k]['ps'] for k in SCEN)
integ_pw = wd*dcf_pw + wg*ga_pw + wr*rel_pw
print({k: round(v) for k, v in integ.items()}, "PW", round(integ_pw), "DCF PW", round(dcf_pw))
print(f"upside vs price: DCF {dcf_pw/PRICE-1:+.1%} GA {ga_pw/PRICE-1:+.1%} integ {integ_pw/PRICE-1:+.1%}")

print("\n=== 12M roll-forward IV (Base-case payout, buyback at $1,090) ===")
E0 = integ_pw * DILUTED_SH
ret = be[0]['buyback'] + be[0]['div']
E1 = E0 * (1 + KE) - ret
sh1 = be[0]['end_sh']
iv1 = E1 / sh1
iv1_nobb = (E0 * (1 + KE) - be[0]['div']) / DILUTED_SH - (be[0]['buyback'] / DILUTED_SH)
print(f"E0 {E0:.1f} E1 {E1:.1f} shares {sh1:.3f} IV_12M {iv1:.0f} ; value-neutral (buyback at IV) would be {integ_pw*(1+KE)-DPS:.0f}")

print("\n=== 3Y (end FY29 ~ Sep-2029) intrinsic value per share, DCF-based ===")
iv3 = {}
for k in SCEN:
    r = res[k]
    rows = r['rows']
    w = WACC
    ev3 = sum(rows[i]['fcff'] * (1 + w) ** (-((i - 2) - 0.5)) for i in range(3, len(rows)))
    ev3 += r['tv'] * (1 + w) ** (-(len(rows) - 3))
    cash3 = eps[k][2]['cash']
    eq3 = ev3 + cash3 - OP_CASH - DEBT - OP_LEASE
    sh3 = eps[k][2]['end_sh']
    iv3[k] = eq3 / sh3
    print(f"{k}: EV3 {ev3:.0f} cash3 {cash3:.0f} eq3 {eq3:.0f} sh3 {sh3:.3f} IV3 {iv3[k]:.0f}")
iv3_pw = sum(P[k]*iv3[k] for k in SCEN)
print(f"IV3 PW {iv3_pw:.0f}")
pfv = 1.10  # [M] trough-anticipation premium
mkt3 = {k: iv3[k] * pfv for k in SCEN}
mkt3_pw = sum(P[k]*mkt3[k] for k in SCEN)
divs3 = DPS * 3 * 1.05
cagr3 = ((mkt3_pw + divs3) / PRICE) ** (1/3) - 1
print(f"3Y market price PW {mkt3_pw:.0f} (P/FV {pfv}) -> 3Y CAGR {cagr3*100:.1f}%")
for k in SCEN:
    print(f"   {k} 3Y CAGR {(((mkt3[k]+divs3)/PRICE)**(1/3)-1)*100:.1f}%")
# integrated-scaled alternative
scale = integ_pw / dcf_pw
print(f"IV3 scaled by integrated/DCF ratio ({scale:.2f}) = {iv3_pw*scale:.0f}")

print("\n=== Required-return buy price & safety margin ===")
req = 0.15
for rq in [0.12, 0.15]:
    print(f"req {rq:.0%}: buy price {(mkt3_pw + divs3)/(1+rq)**3:.0f} ; using scaled IV3 {(iv3_pw*scale + divs3)/(1+rq)**3:.0f}")
for d in [0.30, 0.35, 0.40]:
    print(f"safety discount {d:.0%}: {integ_pw*(1-d):.0f}")

print("\n=== 12M price scenarios (Sep-2027: price = FY28 EPS x forward P/E) ===")
now_eps, now_pe = CONS_NTM, PRICE / CONS_NTM
sc = [
    ("A EPS 성장(Base) + P/E 유지", eps['Base'][1]['eps'], now_pe, 0.25),
    ("B EPS 성장(Bull) + P/E 상승", eps['Bull'][1]['eps'], 8.5, 0.20),
    ("C EPS 성장(Base) + P/E 하락", eps['Base'][1]['eps'], 5.0, 0.25),
    ("D EPS 미달(Bear) + P/E 압축", eps['Bear'][1]['eps'], 6.0, 0.30),
]
exp = 0
for name, e, pe, p in sc:
    px = e * pe
    tot = (px + DPS) / PRICE - 1
    exp += p * (px + DPS)
    print(f"{name}: FY27 EPS(trailing then) n/a | FY28 EPS {e:.1f} | exit P/E {pe:.1f} | price {px:.0f} | TSR {tot:+.1%} "
          f"| EPS contrib {e/now_eps-1:+.1%} | multiple contrib {pe/now_pe-1:+.1%} | p={p}")
print(f"Expected 12M value {exp:.0f} -> {exp/PRICE-1:+.1%}")

print("\n=== Reverse DCF 2-variable matrices (Base otherwise) ===")
s = SCEN['Base']
print("mid-cycle revenue scale x LR margin")
for scl in [1.0, 1.5, 2.0, 2.5, 3.0]:
    print(f"{scl:.1f}x " + " ".join(f"{build(s, rev_scale=scl, lr_margin=m)['ps']:6.0f}" for m in [0.30, 0.35, 0.40, 0.45, 0.50]))
print("plateau x LR margin")
for p_ in [0, 2, 4, 6, 8]:
    print(f"p{p_} " + " ".join(f"{build(s, plateau=p_, lr_margin=m)['ps']:6.0f}" for m in [0.30, 0.40, 0.50, 0.60]))
print("plateau x mid-cycle scale")
for p_ in [0, 1, 2, 3, 4]:
    print(f"p{p_} " + " ".join(f"{build(s, plateau=p_, rev_scale=scl)['ps']:6.0f}" for scl in [1.0, 1.25, 1.5, 1.75, 2.0, 2.5]))
pl = solve(lambda x: build(s, plateau=int(round(x)))['ps'], PRICE, 0, 30)
for p_ in range(8, 22, 2):
    print(f"  plateau {p_} -> {build(s, plateau=p_)['ps']:.0f}")
# required RONIC with LR margin 45%
print("RONIC x mid-cycle scale (LR margin 30%)")
for rn in [0.11, 0.13, 0.18, 0.25]:
    print(f"{rn:.2f} " + " ".join(f"{build(s, ronic=rn, rev_scale=scl)['ps']:6.0f}" for scl in [1.0, 1.5, 2.0, 2.5]))
# implied scale with LR margin 40%
sc40 = solve(lambda x: build(s, rev_scale=x, lr_margin=0.40)['ps'], PRICE, 0.5, 5)
print(f"scale needed if LR margin 40%: {sc40:.2f}x -> FY31 rev {158*sc40:.0f}, FY36 rev {build(s, rev_scale=sc40, lr_margin=0.40)['rows'][9]['rev']:.0f}")
sc_p2 = solve(lambda x: build(s, rev_scale=x, plateau=2)['ps'], PRICE, 0.5, 5)
print(f"scale needed with 2-yr plateau: {sc_p2:.2f}x")
