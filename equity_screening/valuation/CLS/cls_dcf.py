"""Celestica (CLS) forward DCF, reverse DCF, and sensitivity model.
Valuation date 2026-09-23. All figures in US$ millions except per-share values.
Sources: 2Q26 8-K/10-Q (actuals, balance sheet), 2026 outlook [G], Q2 call (capex), 8-K 2026-08-07 (equity offering)."""
import json, itertools

PRICE = 364.66            # 2026-09-23 close
# --- share count: 115.0M basic (6/30) + 11.129M offering (8/6) + ~1.2M dilutive awards
SHARES_BASIC = 115.0 + 9.677419 + 1.451612
SHARES_DIL = SHARES_BASIC + 1.2
# --- pro-forma net cash (6/30/2026 balance sheet + offering net proceeds)
CASH_0630, DEBT_0630, PENSION = 535.7, 26.4 + 784.0, 90.2
OFFERING_NET = 3390.0
NET_CASH_PF = CASH_0630 + OFFERING_NET - DEBT_0630 - PENSION   # ~= 3,025
H2_2026_FCF = 600.0 - 285.0   # 2026 FCF outlook $600M [G] less 1H26 actual $285M [A]

# --- 2026 base year (guidance-anchored)
REV_2026 = 20500.0           # [G]
MARGIN_2026 = 0.084          # adj. operating margin [G]
PPE_2026 = 1026.3 + 1000 - 493.3 - 110   # 6/30 net PP&E + 2H capex - 2H D&A (approx)
GW_INTANG = 332.9 + 244.9
OTHER_OP = 250.0
SBC_PCT = 0.005              # SBC ~0.5% of revenue, treated as a real cost

SCEN = {
 "Bear": dict(g=[0.50,-0.15,-0.05,0.05,0.05,0.04,0.03,0.03,0.03],
              m=[0.082,0.068,0.065,0.068,0.068,0.068,0.068,0.068,0.068],
              capex=[1500,600], capex_pct=0.018, nwc=0.10, ronic_T=0.12, prob=0.25),
 "Base": dict(g=[0.70,0.25,0.12,0.08,0.06,0.05,0.04,0.035,0.03],
              m=[0.088,0.090,0.090,0.088,0.086,0.085,0.085,0.085,0.085],
              capex=[1500,1300], capex_pct=0.022, nwc=0.08, ronic_T=0.18, prob=0.50),
 "Bull": dict(g=[0.85,0.35,0.18,0.12,0.08,0.06,0.05,0.04,0.03],
              m=[0.092,0.096,0.098,0.098,0.097,0.096,0.095,0.095,0.095],
              capex=[1500,1800], capex_pct=0.025, nwc=0.07, ronic_T=0.25, prob=0.25),
}
YEARS = list(range(2027, 2036))
NWC_2026 = 0.07 * REV_2026

def run(s, wacc=0.115, g_T=0.03, tax=(0.20,0.20,0.20,0.21,0.21,0.21,0.21,0.21,0.21), growth_mult=1.0, margin_add=0.0, detail=False):
    rev, ppe, nwc = REV_2026, PPE_2026, NWC_2026
    rows=[]; pv=0.0
    da_prev = 330.0
    for i,y in enumerate(YEARS):
        g = s["g"][i]*growth_mult if s["g"][i]>0 else s["g"][i]
        rev_new = rev*(1+g)
        m = s["m"][i] + margin_add
        ebit = rev_new*(m - SBC_PCT)                     # after SBC
        nopat = ebit*(1-tax[i])
        capex = s["capex"][i] if i < len(s["capex"]) else rev_new*s["capex_pct"]
        # D&A: ramps with the 2026-27 capex wave, then converges to 85% of capex (growing company)
        if i == 0: da = 360.0
        elif i == 1: da = 550.0 if s["capex"][1] >= 1000 else 480.0
        elif i == 2: da = min(700.0, 0.95*capex + 50)
        else: da = min(0.85*capex, da_prev*1.25)   # smooth the step-up
        da_prev = da
        nwc_new = s["nwc"]*rev_new
        dnwc = nwc_new - nwc
        fcf = nopat + da - capex - dnwc
        ppe = ppe + capex - da
        ic = nwc_new + ppe + GW_INTANG + OTHER_OP
        t = (i + 0.5) + 0.27            # mid-year from 2026-09-23
        df = 1/(1+wacc)**t
        pv += fcf*df
        rows.append(dict(year=y, rev=rev_new, g=g, margin=m, ebit=ebit, nopat=nopat, da=da, capex=capex, dnwc=dnwc, fcf=fcf, ic=ic, roic=nopat/ic, df=df))
        rev, nwc = rev_new, nwc_new
    last = rows[-1]
    nopat_T = last["nopat"]*(1+g_T)
    tv = nopat_T*(1 - g_T/s["ronic_T"])/(wacc - g_T)
    pv_tv = tv*last["df"]*(1/(1+wacc))**0.5
    ev = pv + pv_tv + H2_2026_FCF*0.99
    eq = ev + NET_CASH_PF
    ps = eq/SHARES_DIL
    out = dict(ev=ev, pv_fcf=pv, pv_tv=pv_tv, tv_share=pv_tv/(pv+pv_tv), equity=eq, per_share=ps, rows=rows)
    return out

def eps_path(s):
    """Adjusted EPS (SBC excluded, company definition) for the scenario."""
    rev=REV_2026; res={}
    shares=[SHARES_DIL+0.3*i for i in range(9)]
    for i,y in enumerate(YEARS):
        rev=rev*(1+s["g"][i]); m=s["m"][i]
        net_fin = 20 if i==0 else 40
        ni=(rev*m + net_fin)*(1-0.20)
        res[y]=dict(rev=rev, eps=ni/shares[i], margin=m)
    return res

if __name__=="__main__":
    out={}
    for k,s in SCEN.items():
        r=run(s); out[k]=r
        print(f"{k}: EV {r['ev']:,.0f}  equity {r['equity']:,.0f}  per share ${r['per_share']:.0f}  TV share {r['tv_share']:.0%}")
        for row in r["rows"][:5]:
            print(f"   {row['year']} rev {row['rev']:,.0f} g {row['g']:+.0%} m {row['margin']:.1%} nopat {row['nopat']:,.0f} capex {row['capex']:,.0f} D&A {row['da']:,.0f} dNWC {row['dnwc']:,.0f} FCF {row['fcf']:,.0f} IC {row['ic']:,.0f} ROIC {row['roic']:.0%}")
        ep=eps_path(s); print("   EPS", {y:round(v['eps'],2) for y,v in ep.items() if y<=2030})
    pw=sum(SCEN[k]["prob"]*out[k]["per_share"] for k in SCEN)
    print(f"Probability-weighted ${pw:.0f}  vs price ${PRICE}  upside {pw/PRICE-1:+.0%}")
    print("net cash pf", round(NET_CASH_PF), "shares dil", round(SHARES_DIL,1), "PPE2026", round(PPE_2026))
