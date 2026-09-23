"""Extra cross-checks: probability sensitivity, 12M P/E scenarios, peers-implied values, normalized EPS, dilution bridge, forward ROIC/RONIC."""
import json
from cls_dcf import *
from cls_analysis import ps, WACC, G_T, sc

print("\n## Prob-weighted by WACC")
for w in [0.095, 0.10, 0.11, 0.12]:
    v = {k: ps(SCEN[k], wacc=w) for k in SCEN}
    pw = sum(SCEN[k]["prob"] * v[k] for k in SCEN)
    print(f"WACC {w:.1%}: Bear ${v['Bear']:.0f} Base ${v['Base']:.0f} Bull ${v['Bull']:.0f} -> PW ${pw:.0f} ({pw/PRICE-1:+.0%})")
print("\n## Probability sensitivity @11%")
for pb, pbase, pbull in [(0.15,0.50,0.35),(0.20,0.50,0.30),(0.25,0.50,0.25),(0.35,0.45,0.20)]:
    pw = pb*sc["Bear"]["per_share"] + pbase*sc["Base"]["per_share"] + pbull*sc["Bull"]["per_share"]
    print(f"Bear {pb:.0%}/Base {pbase:.0%}/Bull {pbull:.0%}: ${pw:.0f} ({pw/PRICE-1:+.0%})")

print("\n## 12M (Sep-2027) P/E-based scenario prices")
mult = {"Bear": 10.0, "Base": 17.0, "Bull": 20.0}
tp = {}
for k in SCEN:
    e = sc[k]["eps"]; ntm = 0.25*e[2027] + 0.75*e[2028]
    tp[k] = ntm*mult[k]
    print(f"{k}: NTM EPS(Sep-27) {ntm:.2f} x {mult[k]}x = ${tp[k]:.0f} ({tp[k]/PRICE-1:+.0%})")
pw12 = sum(SCEN[k]["prob"]*tp[k] for k in SCEN); print(f"PW 12M ${pw12:.0f} ({pw12/PRICE-1:+.0%})")

print("\n## Peers-implied (on CLS consensus FY27 EPS $19.36 / NTM EPS $17.15)")
P = json.load(open("/tmp/claude-0/-home-user--/f5651176-3b71-5722-a31d-b18082282959/scratchpad/peers.json"))
import statistics as st
groups = {"US EMS (JBL,FLEX,SANM,PLXS,BHE,FN)": ["JBL","FLEX","SANM","PLXS","BHE","FN"],
          "Taiwan AI ODM (Hon Hai,Quanta,Wiwynn,Wistron)": ["2317.TW","2382.TW","6669.TW","3231.TW"],
          "Accton (switch ODM)": ["2345.TW"], "AI systems (DELL,HPE,SMCI)": ["DELL","HPE","SMCI"]}
for gname, tick in groups.items():
    n = st.median([P[t]["pe_ntm"] for t in tick]); f2 = st.median([P[t]["pe2"] for t in tick]); gr = st.median([P[t]["epsg2"] for t in tick if P[t]["epsg2"] is not None])
    print(f"{gname}: NTM {n:.1f}x FY2 {f2:.1f}x EPSg2 {gr:.0%} -> ${17.15*n:.0f} (NTM) / ${19.36*f2:.0f} (FY27)")

print("\n## Normalized forward EPS")
for label, rev, m in [("Base 2028 (no haircut)", sc["Base"]["rows"][1]["rev"], 0.090), ("Mid-cycle: avg(Base,Bear) 2028 rev, 8.5% margin", (sc["Base"]["rows"][1]["rev"]+sc["Bear"]["rows"][1]["rev"])/2, 0.085), ("Trough: Bear 2029", sc["Bear"]["rows"][2]["rev"], 0.065)]:
    eps = (rev*m + 40)*0.8/(SHARES_DIL+0.6)
    print(f"{label}: rev {rev:,.0f} margin {m:.1%} -> EPS ${eps:.2f}, P/E at price {PRICE/eps:.1f}x")

print("\n## Dilution bridge")
q3_sh = 116.2 + 11.129*(55/92); q4_sh = 116.2 + 11.129 + 0.0
print(f"Q3 weighted diluted shares ~{q3_sh:.1f}M, Q4 ~{q4_sh:.1f}M, 2027 ~{SHARES_DIL:.1f}M")
mid = 2.98; adj = mid*116.2/q3_sh + (3390*0.04/4*(55/92)*0.8)/q3_sh
print(f"Q3 guide midpoint $2.98 on 116.2M -> dilution-adjusted ~${adj:.2f} (vs consensus $2.99)")
fy26 = (1314.0*116.3/116.3)
ni26 = 11.30*116.3 + 3390*0.04*(4.5/12)*0.8
sh26 = (116.0*2 + q3_sh + q4_sh)/4
print(f"FY26: guide $11.30 x 116.3M = NI {11.30*116.3:,.0f}; + interest ~{3390*0.04*(4.5/12)*0.8:.0f} -> ${ni26/sh26:.2f} on {sh26:.1f}M avg shares")

print("\n## Forward ROIC / RONIC (Base, model)")
rows = sc["Base"]["rows"]
nopat26 = REV_2026*(MARGIN_2026-SBC_PCT)*0.8; ic26 = NWC_2026 + PPE_2026 + GW_INTANG + OTHER_OP
print(f"2026E NOPAT {nopat26:,.0f} IC {ic26:,.0f} ROIC {nopat26/ic26:.0%}")
for r in rows[:5]: print(f"{r['year']}: NOPAT {r['nopat']:,.0f} IC {r['ic']:,.0f} ROIC {r['roic']:.0%} EP {r['nopat']-WACC*r['ic']:,.0f}")
print(f"RONIC 2026->2028: {(rows[1]['nopat']-nopat26)/(rows[1]['ic']-ic26):.0%}; 2026->2030: {(rows[3]['nopat']-nopat26)/(rows[3]['ic']-ic26):.0%}")
e = sc["Base"]["eps"]; print("Base EPS path", e, "5y CAGR 26->31", round((e[2031]/11.22)**(1/5)-1,3))
