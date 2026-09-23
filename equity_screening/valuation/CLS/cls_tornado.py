"""One-at-a-time sensitivity (tornado) around the Base case @ WACC 11%, g 3%."""
import copy, json
import cls_dcf as M
from cls_dcf import run, SCEN, PRICE

def val(s=None, **kw):
    s = s or SCEN["Base"]
    return run(s, wacc=kw.pop("wacc", 0.11), g_T=kw.pop("g_T", 0.03), **kw)["per_share"]

base = val()
def mod(**ch):
    s = copy.deepcopy(SCEN["Base"]); s.update(ch); return s
def g_at(i, v):
    s = copy.deepcopy(SCEN["Base"]); s["g"][i] = v; return s
def with_sbc(x):
    old = M.SBC_PCT; M.SBC_PCT = x; v = val(); M.SBC_PCT = old; return v
items = [
 ("WACC 10% / 12%", val(wacc=0.10), val(wacc=0.12)),
 ("영구성장률 4% / 2%", val(g_T=0.04), val(g_T=0.02)),
 ("장기 영업이익률 ±1%p", val(margin_add=0.01), val(margin_add=-0.01)),
 ("2028 성장 +40% / +10%", val(g_at(1, 0.40)), val(g_at(1, 0.10))),
 ("2027 성장 +85% / +55%", val(g_at(0, 0.85)), val(g_at(0, 0.55))),
 ("순운전자본 5% / 11% of 매출", val(mod(nwc=0.05)), val(mod(nwc=0.11))),
 ("장기 capex 1.6% / 2.8% of 매출", val(mod(capex_pct=0.016)), val(mod(capex_pct=0.028))),
 ("터미널 RONIC 35% / 12%", val(mod(ronic_T=0.35)), val(mod(ronic_T=0.12))),
 ("SBC 0.3% / 0.8% of 매출", with_sbc(0.003), with_sbc(0.008)),
 ("세율 17% / 24%", val(tax=(0.17,)*9), val(tax=(0.24,)*9)),
]
print(f"Base ${base:.0f}")
out = []
for name, hi, lo in sorted(items, key=lambda x: -abs(x[1]-x[2])):
    print(f"| {name} | ${lo:.0f} | ${hi:.0f} | {hi-lo:.0f} |")
    out.append(dict(name=name, low=lo, high=hi))
json.dump(dict(base=base, items=out), open("tornado.json", "w"), indent=1)
