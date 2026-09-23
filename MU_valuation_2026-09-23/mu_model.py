"""
Micron Technology (MU) valuation model — analysis date 2026-09-23, price $1,090.

Pure-python (no numpy). Every forward input below is a model assumption [M]
unless noted. Historical / guidance / consensus anchors are listed in the report.

Timeline
  t = 0            : 2026-09-23 (valuation date; FY27 began 2026-09-04)
  FY27 (FY+1)      : 2026-09-04 ~ 2027-09-02   -> year index 1
  FY28 (FY+2)      : 2027-09-03 ~ 2028-08-31   -> year index 2
  ...
  Stage I          : FY27-FY31 (explicit cycle)
  Stage II (fade)  : FY32-FY36
  Stage III        : FY37+ (terminal, value-driver formula)
Mid-year discounting: FY_n cash flow at t = n - 0.55, TV at t = 10 - 0.05.
"""

import json
import math

PRICE = 1090.0
DILUTED_SH = 1.15            # bn, FQ4'26 guidance basis [G]
BASIC_SH = 1.13              # bn [A, 2차 자료]
FY26_REV = 128.96            # FQ1-3 actual + FQ4 guide midpoint [A+G]
IC_FY26 = 95.0               # invested capital at FY26 end, $bn [I/M]
NWC_PCT = 0.14               # NWC as % of revenue [M]
# EV -> equity bridge at valuation date ($bn) [M/I]
CASH_EST = 55.0              # FQ3 30.2 + FQ4 FCF >30 - est. FQ4 buyback/div ~5
OP_CASH = 6.0                # operating cash, stays in IC
DEBT = 5.7                   # FQ3 actual
OP_LEASE = 0.7
CUST_DEPOSITS = 5.0          # SCA cash deposits assumed received by FY26 end (debt-like)
NET_FIN = CASH_EST - OP_CASH - DEBT - OP_LEASE - CUST_DEPOSITS   # 37.6

RF, ERP, BETA = 0.050, 0.045, 1.35
KE = RF + BETA * ERP                    # 11.08%
KD_PRE, TAX_MARG, WD = 0.058, 0.15, 0.03
WACC_CALC = (1 - WD) * KE + WD * KD_PRE * (1 - TAX_MARG)
WACC = 0.110                            # rounded base
G = 0.030

SBC = [1.5, 1.6, 1.6, 1.6, 1.7]         # $bn FY27-31, already inside EBIT margin (GAAP-like)
INT_YIELD = 0.040                       # interest on retained cash
PAYOUT = 0.70                           # share of FCF returned (buyback+div) [M]
DPS = 0.60                              # $/yr ($0.15/q) [A]

SCEN = {
    "Bear": dict(
        prob=0.30,
        rev=[210, 150, 95, 85, 100],
        margin=[0.80, 0.60, 0.22, 0.05, 0.15],
        capex=[45, 38, 25, 20, 24],
        da=[15, 19, 22, 23, 24],
        s2g=[0.08, 0.07, 0.06, 0.05, 0.04],   # stage II revenue growth
        lr_margin=0.20, s2c=0.80, ronic=0.11, tax1=0.15, tax2=0.16, taxT=0.17,
    ),
    "Base": dict(
        prob=0.50,
        rev=[232, 228, 170, 140, 158],
        margin=[0.83, 0.77, 0.52, 0.30, 0.35],
        capex=[47, 50, 38, 30, 34],
        da=[15, 20, 25, 28, 30],
        s2g=[0.09, 0.08, 0.07, 0.055, 0.04],
        lr_margin=0.30, s2c=0.90, ronic=0.13, tax1=0.15, tax2=0.16, taxT=0.17,
    ),
    "Bull": dict(
        prob=0.20,
        rev=[255, 285, 270, 240, 262],
        margin=[0.85, 0.83, 0.72, 0.58, 0.58],
        capex=[50, 60, 55, 45, 48],
        da=[15, 21, 27, 32, 35],
        s2g=[0.10, 0.09, 0.08, 0.06, 0.045],
        lr_margin=0.42, s2c=1.00, ronic=0.18, tax1=0.15, tax2=0.16, taxT=0.17,
    ),
}


def build(s, wacc=WACC, g=G, lr_margin=None, ronic=None, rev_scale=1.0,
          stage1_rev_scale=1.0, plateau=0, fade_years=5, full_fade=False,
          margin_scale=1.0):
    """Return dict with annual rows and valuation outputs.

    plateau   : extra years of FY27-level economics inserted before the downturn
    rev_scale : multiplies FY29+ revenue (mid-cycle level) — reverse-DCF lever
    full_fade : terminal value with ROIC on ALL capital -> WACC (TV = NOPAT/WACC)
    """
    lr_margin = s["lr_margin"] if lr_margin is None else lr_margin
    ronic = s["ronic"] if ronic is None else ronic
    rev1 = list(s["rev"])
    mar1 = list(s["margin"])
    capex1 = list(s["capex"])
    da1 = list(s["da"])
    # plateau: repeat year-1 economics (grow revenue 0%, keep margin) before cycle turns
    for _ in range(plateau):
        rev1.insert(1, rev1[0]); mar1.insert(1, mar1[0])
        capex1.insert(1, capex1[0]); da1.insert(1, da1[0])
    n1 = len(rev1)
    rev1 = [r * stage1_rev_scale if i == 0 else r * stage1_rev_scale for i, r in enumerate(rev1)]
    # mid-cycle scale applies from the first downturn year (index >= 2 + plateau)
    rev1 = [r * (rev_scale if i >= 2 + plateau else 1.0) for i, r in enumerate(rev1)]
    mar1 = [min(0.9, m * margin_scale) if i >= 2 + plateau else m for i, m in enumerate(mar1)]

    rows = []
    ic = IC_FY26
    prev_rev = FY26_REV
    for i in range(n1):
        rev = rev1[i]
        m = mar1[i]
        ebit = rev * m
        nopat = ebit * (1 - s["tax1"])
        dnwc = NWC_PCT * (rev - prev_rev)
        capex = capex1[i] * (rev_scale if i >= 2 + plateau else 1.0) ** 0.5
        da = da1[i]
        net_inv = capex - da + dnwc
        fcff = nopat - net_inv
        ic_open = ic
        ic = ic + net_inv
        rows.append(dict(stage="I", rev=rev, g=rev / prev_rev - 1, margin=m, ebit=ebit,
                         nopat=nopat, da=da, capex=capex, dnwc=dnwc, net_inv=net_inv,
                         fcff=fcff, ic_open=ic_open, ic_close=ic))
        prev_rev = rev
    # Stage II fade
    last_m = mar1[-1]
    for k in range(fade_years):
        gk = s["s2g"][min(k, len(s["s2g"]) - 1)] if fade_years == 5 else \
            s["s2g"][0] + (s["s2g"][-1] - s["s2g"][0]) * k / max(1, fade_years - 1)
        rev = prev_rev * (1 + gk)
        m = last_m + (lr_margin - last_m) * (k + 1) / fade_years
        ebit = rev * m
        nopat = ebit * (1 - s["tax2"])
        # growth capital via incremental sales-to-capital on NEXT year's growth
        g_next = s["s2g"][min(k + 1, len(s["s2g"]) - 1)] if k + 1 < fade_years else g
        net_inv = rev * g_next / s["s2c"]
        fcff = nopat - net_inv
        ic_open = ic
        ic = ic + net_inv
        rows.append(dict(stage="II", rev=rev, g=gk, margin=m, ebit=ebit, nopat=nopat,
                         da=None, capex=None, dnwc=None, net_inv=net_inv, fcff=fcff,
                         ic_open=ic_open, ic_close=ic))
        prev_rev = rev
    # Stage III
    nT = len(rows)
    nopat_T1 = rows[-1]["rev"] * (1 + g) * lr_margin * (1 - s["taxT"])
    if full_fade:
        tv = nopat_T1 / wacc
        reinv_rate = None
    else:
        reinv_rate = g / ronic
        tv = nopat_T1 * (1 - reinv_rate) / (wacc - g)
    pv1 = pv2 = 0.0
    for i, r in enumerate(rows):
        t = (i + 1) - 0.55
        df = (1 + wacc) ** (-t)
        r["df"] = df
        r["pv"] = r["fcff"] * df
        if r["stage"] == "I":
            pv1 += r["pv"]
        else:
            pv2 += r["pv"]
    t_tv = nT - 0.05
    pv3 = tv * (1 + wacc) ** (-t_tv)
    ev = pv1 + pv2 + pv3
    eq = ev + NET_FIN
    ps = eq / DILUTED_SH
    # Economic-profit cross-check (end-of-year convention, then same mid-year factor)
    ep_pv = 0.0
    for i, r in enumerate(rows):
        r["roic"] = r["nopat"] / ((r["ic_open"] + r["ic_close"]) / 2)
        r["ep"] = r["nopat"] - wacc * r["ic_open"]
        ep_pv += r["ep"] / (1 + wacc) ** (i + 1)
    ic_T = rows[-1]["ic_close"]
    ep_T1 = nopat_T1 - wacc * ic_T
    if full_fade:
        cv_ep = (nopat_T1 - wacc * ic_T) / wacc  # approximation (no growth)
    else:
        cv_ep = ep_T1 / wacc + (nopat_T1 * (g / ronic) * (ronic - wacc)) / (wacc * (wacc - g))
    ev_ep_eoy = IC_FY26 + ep_pv + cv_ep / (1 + wacc) ** nT
    fcff_pv_eoy = sum(r["fcff"] / (1 + wacc) ** (i + 1) for i, r in enumerate(rows)) + tv / (1 + wacc) ** nT
    return dict(rows=rows, pv1=pv1, pv2=pv2, pv3=pv3, tv=tv, ev=ev, eq=eq, ps=ps,
                tv_share=pv3 / ev, nopat_T1=nopat_T1, reinv_rate=reinv_rate,
                ev_ep_eoy=ev_ep_eoy, ev_fcff_eoy=fcff_pv_eoy, ic_T=ic_T,
                roic_T1=nopat_T1 / ic_T)


def eps_path(s, res, price_for_buyback=PRICE):
    """Adjusted (non-GAAP-like) EPS FY27-FY31: add back SBC, add interest on retained cash."""
    shares = DILUTED_SH
    cash = CASH_EST
    out = []
    for i, r in enumerate(res["rows"][:5]):
        sbc = SBC[i]
        interest = INT_YIELD * cash
        pretax_adj = r["ebit"] + sbc + interest
        ni_adj = pretax_adj * (1 - s["tax1"])
        fcf_eq = r["fcff"] + interest * (1 - s["tax1"])
        returned = max(0.0, PAYOUT * fcf_eq)
        div = DPS * shares
        buyback = max(0.0, returned - div)
        sh_open = shares
        shares = shares - buyback / price_for_buyback + 0.005  # +SBC issuance
        avg_sh = (sh_open + shares) / 2
        cash = cash + fcf_eq - returned
        out.append(dict(ni_adj=ni_adj, eps=ni_adj / avg_sh, avg_sh=avg_sh, end_sh=shares,
                        cash=cash, buyback=buyback, div=div, fcf_eq=fcf_eq,
                        fcf_ps=fcf_eq / avg_sh))
    return out


def solve(fn, target, lo, hi, it=80):
    flo = fn(lo) - target
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = fn(mid) - target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    out = {}
    res = {k: build(v) for k, v in SCEN.items()}
    eps = {k: eps_path(SCEN[k], res[k]) for k in SCEN}
    pw = sum(SCEN[k]["prob"] * res[k]["ps"] for k in SCEN)
    print(f"KE={KE:.4f} WACC_calc={WACC_CALC:.4f} WACC_used={WACC} g={G} NET_FIN={NET_FIN:.1f}")
    mcap_d = PRICE * DILUTED_SH
    mkt_ev = mcap_d - NET_FIN
    print(f"Mcap diluted={mcap_d:.1f} basic={PRICE*BASIC_SH:.1f} market EV(op)={mkt_ev:.1f}")
    for k in SCEN:
        r = res[k]
        print(f"\n=== {k} (p={SCEN[k]['prob']}) ===")
        print("FY   rev    g%    mgn%  EBIT   NOPAT  capex  D&A  dNWC  netInv  FCFF   IC_close ROIC%  EP")
        for i, row in enumerate(r["rows"]):
            fy = 27 + i
            cap = f"{row['capex']:6.1f}" if row['capex'] is not None else "   -  "
            da = f"{row['da']:5.1f}" if row['da'] is not None else "  -  "
            dn = f"{row['dnwc']:5.1f}" if row['dnwc'] is not None else "  -  "
            print(f"FY{fy} {row['rev']:6.1f} {row['g']*100:6.1f} {row['margin']*100:5.1f} {row['ebit']:6.1f} "
                  f"{row['nopat']:6.1f} {cap} {da} {dn} {row['net_inv']:6.1f} {row['fcff']:6.1f} "
                  f"{row['ic_close']:7.1f} {row['roic']*100:6.1f} {row['ep']:6.1f}")
        print(f"PV StageI={r['pv1']:.1f} StageII={r['pv2']:.1f} StageIII={r['pv3']:.1f} TV={r['tv']:.1f} "
              f"TVshare={r['tv_share']*100:.1f}% EV={r['ev']:.1f} Equity={r['eq']:.1f} /sh={r['ps']:.0f}")
        print(f"NOPAT_T+1={r['nopat_T1']:.1f} reinv={r['reinv_rate']} IC_T={r['ic_T']:.1f} ROIC_T+1={r['roic_T1']*100:.1f}%")
        print(f"EP check (EOY): EV_EP={r['ev_ep_eoy']:.1f} vs EV_FCFF={r['ev_fcff_eoy']:.1f}")
        for i, e in enumerate(eps[k]):
            print(f"  FY{27+i} adjNI={e['ni_adj']:.1f} EPS={e['eps']:.1f} avgSh={e['avg_sh']:.3f} endSh={e['end_sh']:.3f} "
                  f"cash={e['cash']:.1f} buyback={e['buyback']:.1f} FCF/sh={e['fcf_ps']:.1f}")
        out[k] = dict(ps=r["ps"], ev=r["ev"], eq=r["eq"], pv1=r["pv1"], pv2=r["pv2"], pv3=r["pv3"],
                      tv_share=r["tv_share"], eps=[e["eps"] for e in eps[k]],
                      fcfps=[e["fcf_ps"] for e in eps[k]], end_sh=[e["end_sh"] for e in eps[k]])
    print(f"\nProb-weighted DCF/share = {pw:.0f}")

    # FCFE cross-check (Base): FCFE ~ FCFF - after-tax interest on debt; discount at KE
    b = res["Base"]
    kd_at = KD_PRE * (1 - 0.15)
    fcfe_pv = sum((r["fcff"] - DEBT * kd_at) * (1 + KE) ** (-((i + 1) - 0.55)) for i, r in enumerate(b["rows"]))
    tv_e = (b["nopat_T1"] * (1 - G / SCEN["Base"]["ronic"]) - DEBT * kd_at) / (KE - G)
    fcfe_pv += tv_e * (1 + KE) ** (-(len(b["rows"]) - 0.05))
    eq_fcfe = fcfe_pv + (CASH_EST - OP_CASH - OP_LEASE - CUST_DEPOSITS)
    print(f"FCFE cross-check Base equity={eq_fcfe:.1f} /sh={eq_fcfe/DILUTED_SH:.0f} (KE={KE:.4f})")

    # Sensitivities (Base)
    s = SCEN["Base"]
    print("\nWACC x g (Base $/sh)")
    for w in [0.10, 0.105, 0.11, 0.115, 0.12]:
        print(f"{w*100:5.1f}% " + " ".join(f"{build(s, wacc=w, g=gg)['ps']:6.0f}" for gg in [0.02, 0.025, 0.03, 0.035, 0.04]))
    print("\nMid-cycle revenue scale x long-run margin (Base $/sh)")
    for sc in [0.8, 0.9, 1.0, 1.15, 1.3, 1.5]:
        print(f"{sc:4.2f} " + " ".join(f"{build(s, rev_scale=sc, lr_margin=m)['ps']:6.0f}" for m in [0.20, 0.25, 0.30, 0.35, 0.40, 0.45]))
    print("\nTerminal RONIC x fade years (Base $/sh); last col = full fade (ROIC->WACC on all capital)")
    for rn in [0.11, 0.13, 0.15, 0.18, 0.22]:
        cells = [build(s, ronic=rn, fade_years=fy)['ps'] for fy in [3, 5, 8]]
        print(f"{rn*100:4.0f}% " + " ".join(f"{c:6.0f}" for c in cells) + f"  full-fade={build(s, full_fade=True)['ps']:.0f}")
    print("\nLong-run margin x WACC (Base $/sh)")
    for m in [0.20, 0.25, 0.30, 0.35, 0.40, 0.45]:
        print(f"{m*100:4.0f}% " + " ".join(f"{build(s, lr_margin=m, wacc=w)['ps']:6.0f}" for w in [0.10, 0.11, 0.12]))
    print("\nPlateau years (FY27-level economics repeated) x long-run margin (Base $/sh)")
    for p in [0, 1, 2, 3]:
        print(f"plateau {p} " + " ".join(f"{build(s, plateau=p, lr_margin=m)['ps']:6.0f}" for m in [0.25, 0.30, 0.35, 0.40, 0.45]))

    # Reverse DCF — solve one variable at a time, Base otherwise fixed
    target_ps = PRICE
    print("\nReverse DCF (one variable at a time, Base otherwise):")
    lr = solve(lambda x: build(s, lr_margin=x)['ps'], target_ps, 0.05, 0.95)
    print(f"  required long-run op margin = {lr*100:.1f}%")
    sc = solve(lambda x: build(s, rev_scale=x)['ps'], target_ps, 0.5, 5.0)
    print(f"  required mid-cycle revenue scale = {sc:.2f}x (FY31 rev = {158*sc:.0f})")
    rn = None
    try:
        rn = solve(lambda x: build(s, ronic=x)['ps'], target_ps, 0.111, 50.0)
        print(f"  required terminal RONIC = {rn*100:.0f}% (ps at RONIC=inf: {build(s, ronic=1e9)['ps']:.0f})")
    except Exception as e:
        print("  RONIC solve failed", e)
    print(f"  ps at RONIC=1e9 (no reinvestment) = {build(s, ronic=1e9)['ps']:.0f}")
    for p in range(0, 6):
        print(f"  plateau {p}y -> {build(s, plateau=p)['ps']:.0f}")
    # two-variable: plateau x margin already above; margin_scale on downturn years
    ms = solve(lambda x: build(s, margin_scale=x, lr_margin=min(0.9, s['lr_margin']*x))['ps'], target_ps, 0.5, 3.0)
    print(f"  required uniform margin uplift (FY29+ & LR) = {ms:.2f}x -> LR margin {s['lr_margin']*ms*100:.1f}%, FY30 {0.30*ms*100:.0f}%")
    # Implied 5Y / 10Y revenue CAGR: scale all revenue FY29+ with margins fixed
    r_sc = build(s, rev_scale=sc)
    rev31 = r_sc['rows'][4]['rev']; rev36 = r_sc['rows'][9]['rev']
    print(f"  implied FY31 rev={rev31:.0f} (5Y CAGR {((rev31/FY26_REV)**(1/5)-1)*100:.1f}%), FY36 rev={rev36:.0f} (10Y CAGR {((rev36/FY26_REV)**(1/10)-1)*100:.1f}%)")

    # Market-implied at price with Bull structure?
    print(f"\nBull per-share={res['Bull']['ps']:.0f}; Bull with WACC 10% = {build(SCEN['Bull'], wacc=0.10)['ps']:.0f}")

    json.dump(out, open(__file__.replace('mu_model.py', 'model_output.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
