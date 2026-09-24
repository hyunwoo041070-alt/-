"""Prompt v2 tracks, false-positive flags and 100-point scoring with the bands written in the prompt."""
import json, os, math
import numpy as np, pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
d = pd.read_pickle('v2/model.pkl')
OV = json.load(open('v2/overlay.json')) if os.path.exists('v2/overlay.json') else {}


def nz(x):
    return x is not None and not (isinstance(x, float) and (math.isnan(x) or math.isinf(x)))


def band(x, edges, pts, default):
    if not nz(x):
        return default
    for e, p in zip(edges, pts):
        if x < e:
            return p
    return pts[-1]


# industry medians for relative value
d['pe_norm_c'] = d.pe_norm.where(d.pe_norm > 0)
ind_pe = d.groupby('ind').pe_norm_c.median()
ind_roic = d.groupby('ind').roic.median()
ind_n = d.groupby('ind').size()

rows = []
for s, r in d.iterrows():
    o = OV.get(s, {})
    fin = bool(r.fin)
    # ---------------- tracks ----------------
    ta = []
    if nz(r.fcfy_norm) and r.fcfy_norm >= 0.06 and not fin: ta.append('FCFy')
    if nz(r.ev_ebit_norm) and 0 < r.ev_ebit_norm <= 12 and not fin: ta.append('EV/EBIT')
    if nz(r.ev_ebit_norm) and nz(r.ev_ebit_hist_med) and r.ev_ebit_norm > 0 and r.ev_ebit_hist_med > 0 \
            and r.ev_ebit_norm <= 0.7 * r.ev_ebit_hist_med and not fin: ta.append('vsHist')
    ipe, iro = ind_pe.get(r.ind), ind_roic.get(r.ind)
    if ind_n.get(r.ind, 0) >= 5 and nz(r.pe_norm) and r.pe_norm > 0 and nz(ipe) and r.pe_norm <= 0.7 * ipe \
            and nz(r.roic) and nz(iro) and r.roic >= iro: ta.append('vsPeer')
    if fin and nz(r.ptbv) and nz(r.rote_n) and r.ptbv <= r.rote_n / r.ke: ta.append('P/TBV')
    # net cash >= 30% of market cap (local currency; mcap = EV - debt + cash)
    mcl = r.ev - r.debt + r.cash
    if mcl and (r.cash - r.debt) >= 0.3 * mcl: ta.append('NetCash')
    trackA = len(ta) >= 2 or (fin and 'P/TBV' in ta and len(ta) >= 1 and nz(r.rote_n) and r.rote_n > r.ke)
    tb = []
    if nz(r.fpeg) and r.fpeg <= 1.0: tb.append('fPEG')
    en = r.e_norm
    if nz(en) and en >= 0.15 and nz(r.pe2) and r.pe2 <= 25: tb.append('CAGR+PE')
    if nz(r.comp2) and r.comp2 >= 0.35: tb.append('Compress')
    if nz(r.rv3m_f2) and nz(r.r3m) and r.rv3m_f2 - r.r3m >= 0.10: tb.append('Rev>Px')
    trackB = len(tb) >= 2
    trackC = bool(not fin and nz(r.ebit_norm) and r.ebit_norm > 0 and r.om_ttm * r.rev_ttm <= 0.7 * r.ebit_norm
                  and nz(r.pe_norm) and 0 < r.pe_norm <= 15
                  and (r.cyc in ('회복', '저점')) and r.has_cons and nz(r.f2) and nz(r.ttm_adj) and r.f2 > 1.2 * max(r.ttm_adj, 1e-9))
    tracks = ''.join(t for t, ok in (('A', trackA), ('B', trackB), ('C', trackC)) if ok)

    # ---------------- false positives ----------------
    trap = []
    # value trap: 3 consecutive revenue declines, or estimates falling + revenue shrinking
    if nz(r.rg1) and r.rg1 < 0 and nz(r.rg2) and r.rg2 < 0: trap.append('매출 역성장 지속(컨센)')
    if nz(r.rv3m_f2) and r.rv3m_f2 < -0.10 and nz(r.rv3m_f1) and r.rv3m_f1 < -0.10: trap.append('컨센서스 급락')
    if nz(r.ev_ebit_hist_med) and r.ev_ebit_hist_med < 9 and nz(r.rg2) and r.rg2 <= 0: trap.append('만성 저멀티플+무성장')
    gov = []
    if nz(r.sh_g) and r.sh_g > 0.10: gov.append('희석>10%')
    if o.get('gov'): gov.append(o['gov'])
    if o.get('trap'): trap.append(o['trap'])

    # ---------------- scores ----------------
    # A margin of safety (20)
    A = band(r.mos, [0, 0.15, 0.30, 0.50], [0, 5, 11, 16, 20], 8)
    if nz(r.bear_dd) and r.bear_dd < -0.40: A = min(A, 12)
    # B growth-adjusted (15)
    growth_route = nz(en) and en >= 0.08 and r.has_cons and not r.peak
    if growth_route:
        B = band(r.fpeg, [0.5, 0.8, 1.2, 2.0], [15, 12, 8, 4, 0], 6)
        B_cons = B
    else:
        fy = r.fcfy_norm if not fin else (r.rote_n / r.ptbv if nz(r.ptbv) and r.ptbv > 0 else None)
        gg = r.rg2 if nz(r.rg2) else 0.0
        B = band((fy or 0) + max(min(gg, 0.10), -0.05), [0.06, 0.09, 0.12, 0.15], [0, 4, 8, 12, 15], 6)
        B_cons = 0
    # C evidence (15): 10 independent + 5 revision
    ev_pts = 0
    if r.n2 >= 5: ev_pts += 2
    if nz(r.disp) and r.disp < 0.4: ev_pts += 2
    if r.beats >= 3: ev_pts += 2
    if nz(r.rg1) and nz(r.rg2) and r.rg2 >= 0.7 * max(r.rg1, 0.01) and r.rg2 > 0: ev_pts += 2
    if r.has_cons and nz(r.f2) and nz(r.f1) and nz(r.ttm_adj) and r.f1 >= r.ttm_adj: ev_pts += 2
    if 'evidence' in o: ev_pts = o['evidence']          # manual: 10 strong / 6 partial / 2 none / 0 against
    ev_pts = min(ev_pts, 10)
    if not r.has_cons:
        C_rev = 2
    else:
        C_rev = band(r.rv3m_f2, [0, 0.05], [0, 3, 5], 2)
        if r.n2 < 5: C_rev /= 2
    C = ev_pts + C_rev
    # D quality (15)
    spread = (r.roic - r.wacc) if not fin else ((r.rote_n or 0) - r.ke)
    D1 = band(spread, [0, 0.05, 0.15], [0, 2, 4, 6], 2)
    rh = r.roic_hist if isinstance(r.roic_hist, list) else []
    D2 = 2 if len(rh) < 2 else (3 if rh[-1] > rh[0] + 0.02 else (2 if rh[-1] >= rh[0] - 0.02 else 0))
    D3 = 3 if fin else band(r.fcf_m_sbc, [0, 0.10, 0.20], [0, 1, 3, 4], 1)
    sbcr = r.sbc_rev if nz(r.sbc_rev) else 0.03
    shg = r.sh_g if nz(r.sh_g) else 0.0
    D4 = 2 if (shg < 0.01 and sbcr < 0.03) else (1 if shg < 0.03 else 0)
    D = D1 + D2 + D3 + D4
    # E expectation gap (10): duration
    if fin:
        E = band((r.rote_n or 0) / (r.ptbv or 9) - r.ke, [-0.02, 0.0, 0.02, 0.05], [0, 4, 7, 9, 10], 4)
        E_cons = 0
    else:
        gap = (o.get('dur_ev', r.dur_ev)) - r.n_implied
        E = 10 if r.n_implied == 0 else band(gap, [-0.5, 1, 3], [0, 4, 7, 10], 4)
        E_cons = E if r.has_cons else 0
    # F cycle (10)
    cyc = o.get('cyc', r.cyc)
    F = {'저점': 10, '회복': 10, '중반': 7, '판단 불가': 4, '정점 근접': 0}[cyc]
    # G risk (10)
    G = 10; notes = []
    if nz(r.nd_ebitda) and not fin:
        if r.nd_ebitda > 3: G -= 4; notes.append('순부채/EBITDA>3x')
        elif r.nd_ebitda > 2: G -= 2
    if o.get('cust25'): G -= 2; notes.append('고객집중>25%')
    if shg > 0.05 or sbcr > 0.10: G -= 2; notes.append('희석/SBC 과다')
    if r.ar_flag or r.inv_flag: G -= 1; notes.append('매출채권·재고 급증')
    G += o.get('g_adj', 0)
    if o.get('g_note'): notes.append(o['g_note'])
    G = max(G, 0)
    # H catalyst (5)
    H = o.get('cat', 3 if ((r.beats >= 3) or (nz(r.rv3m_f2) and r.rv3m_f2 > 0.03)) else 0)
    # consensus-dependence cap 30
    cons_pts = B_cons + C_rev + E_cons
    if cons_pts > 30:
        ex = cons_pts - 30
        cutE = min(ex, E_cons); E -= cutE; ex -= cutE
        B -= min(ex, B_cons)
    total = A + B + C + D + E + F + G + H
    grade = 'S' if total >= 85 else 'A+' if total >= 78 else 'A' if total >= 72 else 'B' if total >= 65 else 'C' if total >= 60 else '제외'
    excl = []
    if r.peak or cyc == '정점 근접': excl.append('정점 근접' + (' (' + o['cyc_note'] + ')' if o.get('cyc_note') else ''))
    if trap: excl.append('가치함정: ' + ','.join(trap))
    if o.get('gov_excl'): excl.append('회계·지배구조: ' + o['gov_excl'])
    if r.dflag and not o.get('data_ok'): excl.append('데이터 이상: ' + r.dflag)
    if o.get('data_excl'): excl.append('데이터·모델 부적합: ' + o['data_excl'])
    # lens classification
    lens1 = nz(r.mos) and r.mos >= 0.15 or (nz(r.epv_ratio) and r.epv_ratio >= 0.9)
    lens2 = growth_route and nz(r.fpeg) and r.fpeg <= 0.8
    rows.append(dict(cyc2=cyc, factor=o.get('factor', ''), why=o.get('why', ''), sym=s, tracks=tracks, trackA_hits=','.join(ta), trackB_hits=','.join(tb), A=A, B=B, C=C, D=D, E=E, F=F,
                     G=G, H=H, total=total, grade=grade, excl=';'.join(excl), risk=';'.join(notes),
                     lens1=bool(lens1), lens2=bool(lens2), both=bool(lens1 and lens2), cons_pts=cons_pts,
                     gap_years=(None if fin else (o.get('dur_ev', r.dur_ev) - r.n_implied))))
sc = pd.DataFrame(rows).set_index('sym')
out = d.join(sc)
out.to_pickle('v2/scored2.pkl')
elig = out[(out.tracks != '') & (out.excl == '')].sort_values('total', ascending=False)
print('universe', len(out), 'any track', (out.tracks != '').sum(), 'eligible', len(elig),
      'excluded(track but flagged)', ((out.tracks != '') & (out.excl != '')).sum())
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 24)
print(elig[['name', 'ind', 'mcap_usd', 'tracks', 'pe_norm', 'pe2', 'fpeg', 'mos', 'bear_dd', 'epv_ratio', 'n_implied',
            'cyc', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'total']].head(60).round(2).to_string())
