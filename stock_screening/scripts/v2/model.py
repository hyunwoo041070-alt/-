"""Prompt v2 screen: intrinsic value + growth-adjusted, normalized earnings, cycle check."""
import json, os, math, sys
import numpy as np, pandas as pd, datetime as dt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
FX = json.load(open('fx.json'))
RF = 0.0511          # US 10Y (^TNX) 2026-09-23
ERP = 0.045
GT = 0.025           # terminal growth
TODAY = dt.datetime(2026, 9, 23).timestamp()
PX5 = pd.read_pickle('v2/px5y.pkl')
UNI = {x['symbol']: x for x in json.load(open('v2/universe_all.json'))}

COMMODITY = {'Oil & Gas E&P', 'Oil & Gas Integrated', 'Oil & Gas Drilling', 'Oil & Gas Equipment & Services',
             'Oil & Gas Refining & Marketing', 'Steel', 'Aluminum', 'Copper', 'Gold', 'Silver',
             'Other Precious Metals & Mining', 'Other Industrial Metals & Mining', 'Chemicals', 'Agricultural Inputs',
             'Marine Shipping', 'Trucking', 'Residential Construction', 'Lumber & Wood Production',
             'Paper & Paper Products', 'Coal', 'Uranium', 'Farm Products', 'Airlines', 'Building Materials',
             'Auto Manufacturers', 'Farm & Heavy Construction Machinery', 'Specialty Chemicals'}
CAPEX_CYCLE = {'Semiconductors', 'Semiconductor Equipment & Materials', 'Electronic Components',
               'Communication Equipment', 'Computer Hardware', 'Electrical Equipment & Parts'}
CRP = {'Brazil': 0.03, 'China': 0.015, 'Hong Kong': 0.01, 'Kazakhstan': 0.03, 'Ukraine': 0.08, 'Argentina': 0.08,
       'Turkey': 0.05, 'Mexico': 0.02, 'Colombia': 0.03, 'India': 0.02, 'Indonesia': 0.02, 'Greece': 0.015,
       'Chile': 0.01, 'Peru': 0.02, 'South Africa': 0.03, 'Philippines': 0.02, 'Vietnam': 0.03, 'Malaysia': 0.01,
       'Uruguay': 0.02, 'Nigeria': 0.06, 'Egypt': 0.06, 'Israel': 0.01, 'Cayman Islands': 0.0, 'Taiwan': 0.005,
       'South Korea': 0.005, 'Singapore': 0.0}
MEMORY = {'MU', 'SNDK', 'WDC', 'STX', '000660.KS', '005930.KS'}


def g(d, *k):
    for kk in k:
        if not isinstance(d, dict):
            return None
        d = d.get(kk)
    return d


def ser(D, st, items):
    for it in items:
        x = (D.get(st) or {}).get(it)
        if x:
            s = pd.Series({pd.Timestamp(k.split(' ')[0]): v for k, v in x.items()}).dropna().sort_index()
            if len(s):
                return s
    return pd.Series(dtype=float)


def nz(x):
    return x is not None and not (isinstance(x, float) and (math.isnan(x) or math.isinf(x)))


def dcf(rev0, m0, m_target, growth, wacc, stc, ronic_t, tax, years=10, fade_margin=5):
    """FCFF DCF. growth: list of 10 revenue growth rates. Margin moves linearly m0->m_target over fade_margin yrs."""
    rev, pv, prev = rev0, 0.0, rev0
    for t in range(1, years + 1):
        rev = prev * (1 + growth[t - 1])
        m = m0 + (m_target - m0) * min(1, t / fade_margin)
        nopat = rev * m * (1 - tax)
        reinv = max(0.0, (rev - prev) / stc)
        pv += (nopat - reinv) / (1 + wacc) ** t
        prev = rev
    nopat_next = prev * (1 + GT) * m_target * (1 - tax)
    rn = max(ronic_t, wacc)
    tv = nopat_next * (1 - GT / rn) / (wacc - GT)
    return pv + tv / (1 + wacc) ** years


def growth_path(g1, g2, years=10, hold=0, decay=0.70):
    """years 1,2 = g1,g2; hold extra years at g2; then excess growth over GT decays geometrically."""
    path = [g1, g2] + [g2] * hold
    ex = g2 - GT
    while len(path) < years:
        ex *= decay
        path.append(GT + ex)
    return path[:max(years, len(path))]


def evaluate(sym):
    try:
        D1 = json.load(open(f'd1/{sym}.json'))
        D2 = json.load(open(f'd2/{sym}.json'))
    except Exception:
        return None
    i = D1.get('info') or {}
    P = i.get('currentPrice') or i.get('regularMarketPrice')
    if not P:
        return None
    pc = i.get('currency') or 'USD'
    fc = i.get('financialCurrency') or pc
    if fc not in FX or pc not in FX:
        return None
    k = FX[fc] / FX[pc]            # statements -> price currency
    kusd = FX.get(pc, 1.0)
    sector, ind = i.get('sector'), i.get('industry')
    name = i.get('shortName') or sym
    qt = i.get('quoteType')
    if ind and ind.startswith('REIT') or qt not in (None, 'EQUITY'):
        return None
    shares_cands = [x for x in (i.get('sharesOutstanding'), i.get('impliedSharesOutstanding')) if x]
    if not shares_cands:
        return None
    shares = max(shares_cands)
    mcap = P * shares
    fin = sector == 'Financial Services' and ind != 'Financial Data & Stock Exchanges'

    # ---------- statements ----------
    rev = ser(D2, 'is', ['Total Revenue', 'Operating Revenue']) * k
    ebit = ser(D2, 'is', ['Operating Income', 'EBIT']) * k
    ni = ser(D2, 'is', ['Net Income Common Stockholders', 'Net Income']) * k
    eps_h = ser(D2, 'is', ['Diluted EPS', 'Basic EPS']) * k
    fcf_a = ser(D2, 'cf', ['Free Cash Flow']) * k
    sbc_a = ser(D2, 'cf', ['Stock Based Compensation']) * k
    eq_a = ser(D2, 'bs', ['Stockholders Equity', 'Common Stock Equity']) * k
    tbv_a = ser(D2, 'bs', ['Tangible Book Value']) * k
    debt_a = ser(D2, 'bs', ['Total Debt']) * k
    cash_a = ser(D2, 'bs', ['Cash Cash Equivalents And Short Term Investments', 'Cash And Cash Equivalents']) * k
    qrev = ser(D2, 'qis', ['Total Revenue', 'Operating Revenue']) * k
    qebit = ser(D2, 'qis', ['Operating Income', 'EBIT']) * k
    qni = ser(D2, 'qis', ['Net Income Common Stockholders', 'Net Income']) * k
    qfcf = ser(D2, 'qcf', ['Free Cash Flow']) * k
    qsbc = ser(D2, 'qcf', ['Stock Based Compensation']) * k
    qint = ser(D2, 'qis', ['Interest Expense']) * k
    qdebt = ser(D2, 'qbs', ['Total Debt']) * k
    qcash = ser(D2, 'qbs', ['Cash Cash Equivalents And Short Term Investments', 'Cash And Cash Equivalents']) * k
    qeq = ser(D2, 'qbs', ['Stockholders Equity', 'Common Stock Equity']) * k
    qtbv = ser(D2, 'qbs', ['Tangible Book Value']) * k
    qsh = ser(D2, 'qis', ['Diluted Average Shares', 'Basic Average Shares'])
    qar = ser(D2, 'qbs', ['Accounts Receivable', 'Receivables']) * k
    qinv = ser(D2, 'qbs', ['Inventory']) * k
    tax_s = ser(D2, 'is', ['Tax Rate For Calcs'])
    if len(qsh) and qsh.iloc[-1] > shares * 1.05 and qsh.iloc[-1] < shares * 4:
        shares = float(qsh.iloc[-1])
    mcap = P * shares
    if len(rev) < 2:
        return None
    PAYMENTS = {'PYPL', 'V', 'MA', 'FI', 'FIS', 'GPN', 'FOUR', 'CPAY', 'WEX', 'WU', 'PAYO', 'RELY', 'IMXI', 'EEFT', 'FLYW',
                'DLO', 'STNE', 'PAGS', 'MQ', 'PAY', 'CASS', 'QTWO', 'NRDS', 'CCSI', 'PMTS', 'XYZ', 'ADYEN.AS'}
    LENDERS = {'PGY', 'UPST', 'AFRM', 'SEZL', 'DAVE', 'SOFI', 'LC', 'OPRT', 'ENVA', 'OMF', 'CACC', 'WRLD', 'RM', 'OPFI', 'LPRO', 'KSPI'}
    if ind == 'Credit Services':
        fin = sym not in PAYMENTS
    if sym in LENDERS:
        fin = True

    def t4(x):
        return float(x.iloc[-4:].sum()) if len(x) >= 4 else None

    rev_ttm = t4(qrev) or float(rev.iloc[-1])
    ebit_ttm = t4(qebit) if t4(qebit) is not None else (float(ebit.iloc[-1]) if len(ebit) else None)
    ni_ttm = t4(qni) if t4(qni) is not None else (float(ni.iloc[-1]) if len(ni) else None)
    fcf_ttm = t4(qfcf) if t4(qfcf) is not None else (float(fcf_a.iloc[-1]) if len(fcf_a) else None)
    sbc_ttm = t4(qsbc) if t4(qsbc) is not None else (float(sbc_a.iloc[-1]) if len(sbc_a) else 0.0)
    int_ttm = abs(t4(qint) or 0.0)
    debt = float(qdebt.iloc[-1]) if len(qdebt) else (float(debt_a.iloc[-1]) if len(debt_a) else 0.0)
    cash = float(qcash.iloc[-1]) if len(qcash) else (float(cash_a.iloc[-1]) if len(cash_a) else 0.0)
    equity = float(qeq.iloc[-1]) if len(qeq) else (float(eq_a.iloc[-1]) if len(eq_a) else None)
    tbv = float(qtbv.iloc[-1]) if len(qtbv) else (float(tbv_a.iloc[-1]) if len(tbv_a) else None)
    if not rev_ttm or rev_ttm <= 0 or ebit_ttm is None:
        return None
    tax = float(min(0.25, max(0.15, tax_s.iloc[-1]))) if len(tax_s) and nz(tax_s.iloc[-1]) else 0.21

    # margin history
    om_hist = [float(ebit[d] / rev[d]) for d in rev.index if d in ebit.index and rev[d] > 0]
    om_ttm = ebit_ttm / rev_ttm
    om_prior = om_hist[:-1] if len(om_hist) > 1 else om_hist
    om_avg = float(np.mean(om_prior)) if om_prior else om_ttm
    om_med_all = float(np.median(om_hist + [om_ttm]))
    rg_hist = [float(rev.iloc[j] / rev.iloc[j - 1] - 1) for j in range(1, len(rev)) if rev.iloc[j - 1] > 0]
    structural = (len(om_hist) >= 3 and all(om_hist[j] > om_hist[j - 1] for j in range(len(om_hist) - 2, len(om_hist)))
                  and om_ttm >= om_hist[-1] - 0.01 and all(x > 0 for x in rg_hist[-2:]))

    # ---------- consensus ----------
    ck = 1.0
    cur = g(D1, 'ee', '0y', 'currency')
    if cur and cur != pc:
        ck = FX.get(cur, 1.0) / FX.get(pc, 1.0)
    f0 = g(D1, 'ee', '0y', 'yearAgoEps'); f1 = g(D1, 'ee', '0y', 'avg'); f2 = g(D1, 'ee', '+1y', 'avg')
    f0 = f0 * ck if nz(f0) else None; f1 = f1 * ck if nz(f1) else None; f2 = f2 * ck if nz(f2) else None
    f2lo, f2hi = g(D1, 'ee', '+1y', 'low'), g(D1, 'ee', '+1y', 'high')
    n2 = g(D1, 'ee', '+1y', 'numberOfAnalysts') or 0
    r0 = g(D1, 're', '0y', 'yearAgoRevenue'); r1 = g(D1, 're', '0y', 'avg'); r2 = g(D1, 're', '+1y', 'avg')
    rq0 = g(D1, 're', '0q', 'growth')
    if r0 and r1 and r1 / r0 - 1 > 2 and (rq0 is None or rq0 < 1):
        r0 = float(rev.iloc[-1]) / k if r1 / (float(rev.iloc[-1]) / k) - 1 < 2 else None
    rg1 = (r1 / r0 - 1) if (r0 and r1 and r0 > 0) else None
    rg2 = (r2 / r1 - 1) if (r1 and r2) else None
    has_cons = bool(f1 and f2 and f1 > 0 and f2 > 0 and n2 >= 1)
    eh = D1.get('eh') or {}
    acts = [v.get('epsActual') for _, v in sorted(eh.items())][-4:]
    ttm_adj = sum(a * ck for a in acts) if len(acts) == 4 and all(a is not None for a in acts) else None
    surpr = [v.get('surprisePercent') for _, v in sorted(eh.items())][-4:]
    beats = sum(1 for x in surpr if x is not None and x > 0)
    negq = bool(f0 and f0 > 0 and any(a is not None and a < 0 for a in acts))
    et = D1.get('et') or {}

    def rv(per, ago):
        c, o = g(et, per, 'current'), g(et, per, ago)
        return (c / o - 1) if (c and o and o > 0) else None
    rv3m_f2, rv1m_f2, rv3m_f1 = rv('+1y', '90daysAgo'), rv('+1y', '30daysAgo'), rv('0y', '90daysAgo')
    nfy = i.get('nextFiscalYearEnd') or 0
    w = min(1, max(0, (nfy - TODAY) / (365 * 86400)))
    ntm = (w * f1 + (1 - w) * f2) if has_cons else None
    eg1 = (f1 / f0 - 1) if (has_cons and f0 and f0 > 0) else None
    eg2 = (f2 / f1 - 1) if has_cons else None
    ecagr = (math.sqrt(f2 / f0) - 1) if (has_cons and f0 and f0 > 0) else None
    oneoff = bool(negq and eg1 and eg1 > 0.6 and eg1 > 2 * max(eg2 or 0, 0.05))
    lowbase = bool(eg1 is not None and eg2 is not None and eg1 > 2 * max(eg2, 0.01) and eg1 > 0.3)
    e_norm = eg2 if (oneoff or lowbase or ecagr is None) else ecagr

    # prices
    col = PX5[sym].dropna() if sym in PX5 else pd.Series(dtype=float)
    def ret(nw):
        return float(col.iloc[-1] / col.iloc[-1 - nw] - 1) if len(col) > nw else None
    r3m, r12m = ret(13), ret(52)

    # ---------- cost of capital ----------
    beta = i.get('beta')
    beta = min(1.8, max(0.7, 0.67 * beta + 0.33)) if nz(beta) else 1.1   # Blume-adjusted
    mcap_usd = mcap * kusd
    size = 0.02 if mcap_usd < 3e8 else (0.01 if mcap_usd < 2e9 else 0.0)
    crp = CRP.get(i.get('country'), 0.0)
    ke = RF + beta * ERP + size + crp
    ebitda = ebit_ttm + (float(ser(D2, 'cf', ['Depreciation And Amortization', 'Depreciation Amortization Depletion']).iloc[-1]) * k
                         if len(ser(D2, 'cf', ['Depreciation And Amortization', 'Depreciation Amortization Depletion'])) else 0)
    nd = debt - cash
    nd_ebitda = nd / ebitda if ebitda > 0 else None
    kd = (RF + (0.03 if (nd_ebitda or 0) > 3 else 0.015)) * (1 - tax)
    wd = debt / (debt + mcap) if debt + mcap > 0 else 0
    wacc = max(0.075, (1 - wd) * ke + wd * kd)

    out = dict(country=i.get('country'), crp=crp, sym=sym, name=name, sector=sector, ind=ind, P=P, cur=pc, mcap_usd=mcap_usd / 1e9, fin=fin,
               beta=beta, ke=ke, wacc=wacc, rev_ttm=rev_ttm, om_ttm=om_ttm, om_avg=om_avg, om_hist=om_hist,
               structural=structural, f0=f0, f1=f1, f2=f2, n2=n2, ttm_adj=ttm_adj, rg1=rg1, rg2=rg2,
               eg1=eg1, eg2=eg2, ecagr=ecagr, e_norm=e_norm, oneoff=oneoff, lowbase=lowbase,
               rv3m_f2=rv3m_f2, rv1m_f2=rv1m_f2, rv3m_f1=rv3m_f1, r3m=r3m, r12m=r12m, beats=beats,
               nd_ebitda=nd_ebitda, debt=debt, cash=cash, has_cons=has_cons,
               disp=((f2hi - f2lo) / abs(f2 / ck)) if (has_cons and nz(f2hi) and nz(f2lo) and f2) else None,
               tgt=i.get('targetMeanPrice'), tlow=i.get('targetLowPrice'))
    out['pe_ttm'] = P / ttm_adj if ttm_adj and ttm_adj > 0 else None
    out['pe_ntm'] = P / ntm if ntm else None
    out['pe1'] = P / f1 if has_cons else None
    out['pe2'] = P / f2 if has_cons else None
    out['comp2'] = 1 - out['pe2'] / out['pe_ttm'] if (out['pe2'] and out['pe_ttm']) else None
    out['fpeg'] = out['pe_ntm'] / (eg2 * 100) if (out['pe_ntm'] and eg2 and eg2 > 0) else None
    out['peg2y'] = out['pe_ntm'] / (ecagr * 100) if (out['pe_ntm'] and ecagr and ecagr > 0) else None

    # quality
    sh_g = float(qsh.iloc[-1] / qsh.iloc[-5] - 1) if len(qsh) >= 5 else None
    out['sh_g'] = sh_g
    out['sbc_rev'] = sbc_ttm / rev_ttm if sbc_ttm is not None else None
    fcf_sbc = (fcf_ttm - (sbc_ttm or 0)) if fcf_ttm is not None else None
    out['fcf_m_sbc'] = fcf_sbc / rev_ttm if fcf_sbc is not None else None
    ic = (equity or 0) + debt - cash
    out['ic'] = ic
    stc_raw = rev_ttm / ic if ic > 0 else None
    stc = min(6.0, max(0.8, stc_raw)) if stc_raw else 3.0
    out['roic'] = ebit_ttm * (1 - tax) / ic if ic > 0 else None
    roic_hist = []
    if len(eq_a) and len(debt_a):
        for d in rev.index:
            if d in ebit.index and d in eq_a.index:
                icd = eq_a[d] + debt_a.get(d, 0) - cash_a.get(d, 0)
                if icd > 0:
                    roic_hist.append(float(ebit[d] * (1 - tax) / icd))
    out['roic_hist'] = roic_hist
    if len(qrev) >= 5:
        ry = float(qrev.iloc[-1] / qrev.iloc[-5] - 1)
        out['ar_flag'] = bool(len(qar) >= 5 and qar.iloc[-5] > 0 and qar.iloc[-1] / qar.iloc[-5] - 1 > ry + 0.2)
        out['inv_flag'] = bool(len(qinv) >= 5 and qinv.iloc[-5] > 0 and qinv.iloc[-1] / qinv.iloc[-5] - 1 > ry + 0.2)
    else:
        out['ar_flag'] = out['inv_flag'] = False

    # ---------- cycle position (prompt v2 stage 2) ----------
    eps_pos = [float(x) for x in eps_h.values[-5:] if nz(x)]
    eps5 = float(np.mean(eps_pos)) if eps_pos else None
    c1 = om_ttm > om_avg + 0.10
    c2 = bool(has_cons and eps5 is not None and ((eps5 > 0 and f2 >= 3 * eps5) or eps5 <= 0))
    c3 = ind in COMMODITY or ind in CAPEX_CYCLE or sym in MEMORY
    crit = int(c1) + int(c2) + int(c3)
    peak_literal = crit >= 2 or sym in MEMORY
    # documented exception: margin rise from scaling in non-cyclical industry
    scaling_exc = bool(peak_literal and not c3 and om_hist and om_ttm >= max(om_hist) - 0.005
                       and len(rg_hist) >= 2 and all(x > 0 for x in rg_hist[-3:]))
    peak = peak_literal and not scaling_exc
    if peak:
        cyc = '정점 근접'
    elif om_ttm < om_avg - 0.05 and has_cons and f2 and ttm_adj and f2 > 1.2 * ttm_adj:
        cyc = '회복'
    elif om_ttm < om_avg - 0.05:
        cyc = '저점'
    elif len(om_hist) < 3:
        cyc = '판단 불가'
    else:
        cyc = '중반'
    out.update(c1=c1, c2=c2, c3=c3, crit=crit, peak=peak, peak_literal=peak_literal, scaling_exc=scaling_exc, cyc=cyc, eps5=eps5)

    # ---------- normalized earnings ----------
    if peak:
        m_norm = om_avg if om_avg > 0 else om_med_all                                  # mid-cycle
    elif structural or scaling_exc:
        m_norm = om_ttm
    elif cyc in ('회복', '저점'):
        m_norm = om_med_all
    else:
        m_norm = (om_ttm + om_med_all) / 2
    m_norm = max(m_norm, -0.5)
    ebit_norm = m_norm * rev_ttm
    nopat_norm = ebit_norm * (1 - tax)
    eps_norm = (ebit_norm - int_ttm) * (1 - tax) / shares
    out.update(m_norm=m_norm, ebit_norm=ebit_norm, eps_norm=eps_norm,
               pe_norm=P / eps_norm if eps_norm > 0 else None,
               ev=mcap + debt - cash)
    out['ev_ebit_norm'] = out['ev'] / ebit_norm if ebit_norm > 0 else None
    out['ev_ebit_ttm'] = out['ev'] / ebit_ttm if ebit_ttm > 0 else None
    # normalized FCF (steady-state at hist growth): NOPAT - reinvestment for ~3% growth
    fcf_norm = nopat_norm - rev_ttm * 0.03 / stc
    out['fcfy_norm'] = fcf_norm / mcap if mcap > 0 else None
    out['fcfy_ttm_sbc'] = fcf_sbc / mcap if fcf_sbc is not None else None
    # historical EV/EBIT at FY ends (market cap scaled by split-adjusted price)
    hist_mult = []
    if len(col) > 20:
        pnow = float(col.iloc[-1])
        for d in ebit.index:
            if ebit[d] > 0 and d in rev.index:
                pd_ = col[col.index <= d]
                if len(pd_):
                    mc_d = mcap * float(pd_.iloc[-1]) / pnow
                    ev_d = mc_d + debt_a.get(d, 0) - cash_a.get(d, 0)
                    hist_mult.append(ev_d / ebit[d])
    out['ev_ebit_hist_med'] = float(np.median(hist_mult)) if len(hist_mult) >= 2 else None

    # ---------- intrinsic value ----------
    if fin:
        roe_hist = [float(ni[d] / eq_a[d]) for d in ni.index if d in eq_a.index and eq_a[d] > 0]
        roe_ttm = ni_ttm / equity if (equity and equity > 0 and ni_ttm is not None) else None
        rote = ni_ttm / tbv if (tbv and tbv > 0 and ni_ttm is not None) else None
        roe_n = float(np.median(roe_hist + ([roe_ttm] if roe_ttm else []))) if roe_hist else roe_ttm
        bv = tbv if (tbv and tbv > 0) else equity
        if not (bv and bv > 0 and roe_n):
            return None
        rote_n = roe_n * (equity / bv) if equity else roe_n
        rote_n = min(rote_n, 0.20)   # long-run cap for normalized ROTE (cycle-peak underwriting/credit)
        ke = max(ke, 0.10)
        out['ke'] = ke
        gF = min(0.025, max(0.0, (e_norm or 0.03) * 0.5))
        def ri(roe_, g_):
            return bv * (roe_ - g_) / (ke - g_) / shares
        base = ri(rote_n, gF)
        bear = ri(rote_n * 0.8, 0.0)
        bull = ri(max(rote_n, (rote or rote_n)) * 1.1, min(0.03, gF + 0.005))
        epv = bv * rote_n / ke / shares
        out.update(rote=rote, rote_n=rote_n, ptbv=mcap / bv, roe_n=roe_n)
        out['roic'] = rote_n
        out['m_norm'] = None
    else:
        g1 = rg1 if nz(rg1) else (rg_hist[-1] if rg_hist else 0.03)
        g2 = rg2 if nz(rg2) else (np.mean(rg_hist[-3:]) if rg_hist else 0.03)
        g1, g2 = float(min(0.6, max(-0.2, g1))), float(min(0.5, max(-0.1, g2)))
        if ind in COMMODITY or sym in MEMORY:   # commodity: strip price-driven growth, use mid-cycle margin
            g1, g2 = min(g1, 0.05), min(g2, 0.05)
        if not has_cons:  # no consensus: be conservative on growth
            g1 = g2 = float(min(0.15, max(-0.05, np.mean(rg_hist[-3:]) if rg_hist else 0.03)))
        # consensus-implied GAAP margin in FY+2
        m_c2 = None
        if has_cons and r2:
            m_c2 = (f2 / ck * shares / (1 - tax) + int_ttm / k) / r2 - (out['sbc_rev'] or 0)
            m_c2 = float(min(m_c2, max(om_ttm, om_avg) + 0.15))
        roic_n = nopat_norm / ic if ic > 0 else 0.25
        if peak or ind in COMMODITY:
            mt_base = min(m_norm, om_avg) if om_avg > 0 else m_norm
        elif m_c2 is not None:
            mt_base = max(m_norm, 0.9 * m_c2) if not structural else max(m_norm, m_c2 * 0.95)
        else:
            mt_base = m_norm
        mt_bear = min(m_norm, om_ttm) * 0.85 if min(m_norm, om_ttm) > 0 else min(m_norm, om_ttm) * 1.15
        mt_bull = max(mt_base, om_ttm, m_c2 or -1)
        ron_base = max(wacc, min(roic_n, 0.30)) if roic_n > 0 else wacc
        ron_bull = max(wacc, min(roic_n, 0.40)) if roic_n > 0 else wacc
        m0 = om_ttm
        base_ev = dcf(rev_ttm, m0, mt_base, growth_path(g1, g2), wacc, stc, ron_base, tax)
        bear_ev = dcf(rev_ttm, m0, mt_bear, growth_path(g1 * 0.5, g2 * 0.4, decay=0.55), wacc, stc, wacc, tax, fade_margin=3)
        bull_ev = dcf(rev_ttm, m0, mt_bull, growth_path(min(0.7, g1 * 1.2), min(0.6, g2 * 1.25), hold=1, decay=0.80), wacc, stc, ron_bull, tax)
        adj = cash - debt
        base, bear, bull = [(x + adj) / shares for x in (base_ev, bear_ev, bull_ev)]
        epv = (nopat_norm / wacc + adj) / shares
        out.update(mt_base=mt_base, mt_bear=mt_bear, mt_bull=mt_bull, m_c2=m_c2, g1=g1, g2=g2, stc=stc, roic_n=roic_n)
        # reverse DCF: years N that growth g_h is held before fading (base margin)
        g_h = max(g2, 0.0)
        def val(N):
            return (dcf(rev_ttm, m0, mt_base, growth_path(g_h, g_h, years=max(10, int(N) + 6), hold=max(0, int(N) - 2)),
                        wacc, stc, ron_base, tax, years=max(10, int(N) + 6)) + adj) / shares
        v0 = (dcf(rev_ttm, m0, mt_base, [GT] * 10, wacc, stc, ron_base, tax) + adj) / shares
        if v0 >= P:
            nimp = 0.0
        else:
            nimp = None
            for N in range(2, 26):
                if val(N) >= P:
                    nimp = float(N)
                    break
            if nimp is None:
                nimp = 26.0
        out.update(n_implied=nimp, g_h=g_h, v_nogrowth=v0)
        out['rote'] = None
    bear, base, bull = max(bear, 0.0), max(base, 0.0), max(bull, 0.0)
    pw = 0.25 * bear + 0.5 * base + 0.25 * bull
    dflag = []
    te = i.get('trailingEps')
    if nz(te) and te > 0 and ni_ttm and ni_ttm > 0:
        ratio = (ni_ttm / shares) / te
        if ratio > 3 or ratio < 1 / 3:
            dflag.append('ADR·주식수 불일치')
    ps = i.get('priceToSalesTrailing12Months')
    if nz(ps) and ps > 0:
        ratio = (mcap / rev_ttm) / ps
        if ratio > 3 or ratio < 1 / 3:
            dflag.append('매출·시총 단위 불일치')
    if len(rev) < 3:
        dflag.append('재무 이력 3년 미만')
    mi = ser(D2, 'qbs', ['Minority Interest'])
    teq = ser(D2, 'qbs', ['Total Equity Gross Minority Interest'])
    if len(mi) and len(teq) and teq.iloc[-1] > 0 and mi.iloc[-1] / teq.iloc[-1] > 0.3:
        dflag.append('비지배지분 과다(Up-C 구조 등)')
    if (equity or 0) <= 0 and not fin:
        dflag.append('자본잠식')
    if out.get('pe2') is not None and out['pe2'] < 2:
        dflag.append('컨센서스 단위 이상(P/E<2)')
    if pw / P - 1 > 2.0 and n2 < 1:
        dflag.append('커버리지 없는 극단적 저평가(검증 불가)')
    out['dflag'] = ';'.join(dflag)
    out.update(v_bear=bear, v_base=base, v_bull=bull, v_pw=pw, epv=epv,
               mos=pw / P - 1, bear_dd=bear / P - 1, epv_ratio=epv / P,
               growth_share=(pw - epv) / pw if pw > 0 else None)
    # evidence-based duration proxy (years) [M]
    if not fin:
        consist = sum(1 for x in rg_hist[-4:] if x >= max(0.03, 0.5 * (out.get('g_h') or 0)))
        sustain = 2 if (nz(rg2) and nz(rg1) and rg2 >= 0.7 * max(rg1, 0.01)) else 0
        revup = 1 if (rv3m_f2 or 0) > 0.03 else 0
        out['dur_ev'] = 1 + consist + sustain + revup
    return out


if __name__ == '__main__':
    syms = json.load(open(sys.argv[1]))
    rows = []
    for s in syms:
        try:
            r = evaluate(s)
        except Exception as e:
            r = None
        if r:
            rows.append(r)
    df = pd.DataFrame(rows).set_index('sym')
    df.to_pickle('v2/model.pkl')
    print(df.shape)
