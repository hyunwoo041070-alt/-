#!/usr/bin/env python3
"""
sec_normalize.py — Normalized EPS / Peak Ratio calculator from SEC XBRL.

Solves the Normalized-EPS bottleneck in the Deep Value x Growth Discriminator
screen: everything below is derived from SEC filings (free, no API key).
SEC does NOT publish prices or analyst estimates, so --price is required and
--fwd-eps is optional; every other input is fetched or derived.

Zero third-party dependencies (stdlib urllib only).

Usage
-----
  # online (needs data.sec.gov reachable)
  ./sec_normalize.py MU --price 1043.96 --fwd-eps 95.97

  # cache the raw filing facts, then run fully offline
  ./sec_normalize.py MU --save-cache cache/
  ./sec_normalize.py MU --price 1043.96 --fwd-eps 95.97 --cache cache/MU.json

  # batch
  ./sec_normalize.py --batch portfolio.csv        # ticker,price,fwd_eps

  # verify the maths with no network at all
  ./sec_normalize.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field

SEC_TICKERS = "https://www.sec.gov/files/company_tickers.json"
SEC_FACTS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
UA = os.environ.get("SEC_USER_AGENT", "normalized-eps-research research@example.com")
ANNUAL_FORMS = ("10-K", "20-F", "40-F", "10-K/A", "20-F/A")

# ---------------------------------------------------------------- tag fallbacks
# SEC filers tag the same economics differently; first hit with data wins.
TAGS: dict[str, list[str]] = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
        "SalesRevenueGoodsNet",
    ],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": [
        "NetIncomeLoss",
        "ProfitLoss",
        "NetIncomeLossAvailableToCommonStockholdersBasic",
    ],
    "diluted_eps": ["EarningsPerShareDiluted", "IncomeLossFromContinuingOperationsPerDilutedShare"],
    "diluted_shares": [
        "WeightedAverageNumberOfDilutedSharesOutstanding",
        "WeightedAverageNumberOfDilutedSharesOutstandingBasicAndDiluted",
    ],
    "equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    ],
    "debt_lt": [
        "LongTermDebtNoncurrent",
        "LongTermDebt",
        "LongTermDebtAndCapitalLeaseObligations",
    ],
    "debt_cur": ["LongTermDebtCurrent", "DebtCurrent", "ShortTermBorrowings"],
    "cash": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],
    "capex": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],
    "dep_amort": [
        "DepreciationDepletionAndAmortization",
        "DepreciationAmortizationAndAccretionNet",
        "DepreciationAndAmortization",
        "Depreciation",
    ],
    "tax_expense": ["IncomeTaxExpenseBenefit"],
    "pretax_income": [
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
    ],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities"],
    "receivables": ["AccountsReceivableNetCurrent"],
    "inventory": ["InventoryNet"],
}
FLOW = {"revenue", "operating_income", "net_income", "diluted_eps", "diluted_shares",
        "capex", "dep_amort", "tax_expense", "pretax_income", "ocf"}


# ------------------------------------------------------------------- fetching
def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        import gzip
        raw = gzip.decompress(raw)
    return raw


def resolve_cik(ticker: str) -> int:
    data = json.loads(_get(SEC_TICKERS))
    for row in data.values():
        if row["ticker"].upper() == ticker.upper():
            return int(row["cik_str"])
    raise SystemExit(f"ticker not found in SEC registry: {ticker}")


def load_facts(ticker: str, cache: str | None, save_cache: str | None) -> dict:
    """Return companyfacts JSON, from cache when given, else from SEC."""
    if cache:
        path = cache if cache.endswith(".json") else os.path.join(cache, f"{ticker.upper()}.json")
        with open(path) as fh:
            return json.load(fh)
    try:
        facts = json.loads(_get(SEC_FACTS.format(cik=resolve_cik(ticker))))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
        raise SystemExit(
            f"\nSEC unreachable ({exc}).\n"
            "  -> allow 'data.sec.gov' and 'www.sec.gov' in the environment's Network access,\n"
            "     or run with --cache pointing at a previously saved companyfacts JSON."
        ) from exc
    if save_cache:
        os.makedirs(save_cache, exist_ok=True)
        with open(os.path.join(save_cache, f"{ticker.upper()}.json"), "w") as fh:
            json.dump(facts, fh)
    return facts


# ----------------------------------------------------------------- extraction
def annual_series(facts: dict, field_name: str) -> dict[int, float]:
    """{fiscal_year: value} for the first tag that yields annual data.

    Flow items are restricted to ~12-month periods so a stray quarter can never
    be mistaken for a full year. Instant (balance-sheet) items have no start
    date and are taken as filed. Later filings win on duplicate years, so
    restatements supersede originals.
    """
    gaap = facts.get("facts", {}).get("us-gaap", {})
    is_flow = field_name in FLOW
    for tag in TAGS[field_name]:
        node = gaap.get(tag)
        if not node:
            continue
        out: dict[int, tuple[str, float]] = {}
        for unit_vals in node.get("units", {}).values():
            for v in unit_vals:
                if v.get("fp") != "FY" or v.get("form") not in ANNUAL_FORMS:
                    continue
                if v.get("val") is None or v.get("fy") is None:
                    continue
                if is_flow:
                    start, end = v.get("start"), v.get("end")
                    if not start or not end or not _is_annual(start, end):
                        continue
                fy = int(v["fy"])
                filed = v.get("filed", "")
                if fy not in out or filed >= out[fy][0]:
                    out[fy] = (filed, float(v["val"]))
        if out:
            return {fy: val for fy, (_, val) in sorted(out.items())}
    return {}


def _is_annual(start: str, end: str) -> bool:
    from datetime import date
    try:
        s = date(*map(int, start.split("-")))
        e = date(*map(int, end.split("-")))
    except (ValueError, TypeError):
        return False
    return 330 <= (e - s).days <= 400


def last_n(series: dict[int, float], n: int) -> list[float]:
    return [series[fy] for fy in sorted(series)[-n:]]


# ---------------------------------------------------------------- calculations
WACC_DEFAULT = {"large": 0.085, "mid": 0.100, "small": 0.120}
TERMINAL_G = 0.04


@dataclass
class Result:
    ticker: str
    price: float
    years: int = 0
    fwd_eps: float | None = None
    eff_tax: float | None = None
    median_op_margin: float | None = None
    median_roic: float | None = None
    latest_revenue: float | None = None
    latest_shares: float | None = None
    invested_capital: float | None = None
    net_debt: float | None = None
    peak_eps: float | None = None
    trough_eps: float | None = None
    norm_eps_margin: float | None = None      # method (a)
    norm_eps_roic: float | None = None        # method (b)
    norm_eps_cycle: float | None = None       # method (c)
    norm_eps_band: tuple[float, float] | None = None   # method (e) bounds
    norm_eps: float | None = None             # chosen
    method_used: str = "none"
    peak_ratio: float | None = None
    peak_bucket: str = "확인 불가"
    cyclicality_flags: list[str] = field(default_factory=list)
    norm_pe: float | None = None
    norm_fcf_yield: float | None = None
    ev: float | None = None
    ev_over_ic: float | None = None
    fair_ev_over_ic: float | None = None
    ev_ic_discount: float | None = None
    ev_ic_ratio: float | None = None
    wacc: float = 0.10
    warnings: list[str] = field(default_factory=list)


def _median(vals: list[float]) -> float | None:
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None


def compute(ticker: str, facts: dict, price: float, fwd_eps: float | None,
            wacc: float | None, years: int = 10) -> Result:
    S = {k: annual_series(facts, k) for k in TAGS}
    r = Result(ticker=ticker.upper(), price=price, fwd_eps=fwd_eps)

    rev, opinc = S["revenue"], S["operating_income"]
    common = sorted(set(rev) & set(opinc))[-years:]
    r.years = len(common)
    if r.years < 4:
        r.warnings.append(f"annual history only {r.years}y — normalization unreliable")

    # effective tax rate, 3y, clamped to a sane band
    tax, pre = S["tax_expense"], S["pretax_income"]
    tax_years = [fy for fy in sorted(set(tax) & set(pre))[-3:] if pre[fy] > 0]
    if tax_years:
        rate = sum(tax[fy] for fy in tax_years) / sum(pre[fy] for fy in tax_years)
        r.eff_tax = min(max(rate, 0.05), 0.35)
    else:
        r.eff_tax = 0.21
        r.warnings.append("effective tax rate unavailable — 21% assumed")

    # market-cap-driven WACC default
    r.latest_shares = S["diluted_shares"][max(S["diluted_shares"])] if S["diluted_shares"] else None
    mcap = price * r.latest_shares if r.latest_shares else None
    if wacc is not None:
        r.wacc = wacc
    elif mcap:
        r.wacc = WACC_DEFAULT["large"] if mcap > 2e10 else (
            WACC_DEFAULT["mid"] if mcap > 2e9 else WACC_DEFAULT["small"])

    # --- cyclicality pre-screen (STEP 0-A, mechanical part) -------------------
    margins = [opinc[fy] / rev[fy] for fy in common if rev[fy]]
    if margins:
        r.median_op_margin = _median(margins)
        if (max(margins) - min(margins)) >= 0.15:
            r.cyclicality_flags.append("margin swing >=15pp")
        if min(margins) < 0:
            r.cyclicality_flags.append("operating loss year in history")
    eps_hist = last_n(S["diluted_eps"], years)
    if eps_hist:
        r.peak_eps, r.trough_eps = max(eps_hist), min(eps_hist)
        if r.trough_eps < 0:
            r.cyclicality_flags.append("EPS loss year in history")

    # --- invested capital & ROIC ---------------------------------------------
    eq, dlt, dcur, cash = S["equity"], S["debt_lt"], S["debt_cur"], S["cash"]
    def ic_at(fy: int) -> float | None:
        if fy not in eq:
            return None
        debt = dlt.get(fy, 0.0) + dcur.get(fy, 0.0)
        return eq[fy] + debt - cash.get(fy, 0.0)
    roics = []
    for fy in common:
        ic = ic_at(fy)
        if ic and ic > 0:
            roics.append(opinc[fy] * (1 - r.eff_tax) / ic)
    r.median_roic = _median(roics)
    latest_fy = max(common) if common else None
    if latest_fy is not None:
        r.invested_capital = ic_at(latest_fy)
        r.net_debt = (dlt.get(latest_fy, 0.0) + dcur.get(latest_fy, 0.0)
                      - cash.get(latest_fy, 0.0))
        r.latest_revenue = rev.get(latest_fy)

    # --- normalized EPS: methods (a) (b) (c) (e) -----------------------------
    sh = r.latest_shares
    if sh and r.latest_revenue and r.median_op_margin is not None:
        r.norm_eps_margin = r.latest_revenue * r.median_op_margin * (1 - r.eff_tax) / sh
    if sh and r.invested_capital and r.median_roic is not None and r.invested_capital > 0:
        r.norm_eps_roic = r.invested_capital * r.median_roic / sh
    if len(eps_hist) >= 5:
        r.norm_eps_cycle = statistics.mean(eps_hist)
    if r.peak_eps is not None and r.trough_eps is not None:
        lo = r.trough_eps * 1.5 if r.trough_eps > 0 else 0.0
        r.norm_eps_band = (lo, r.peak_eps * 0.6)

    # preference: margin method, then ROIC method, then cycle mean
    for name, val in (("margin-normalized (a)", r.norm_eps_margin),
                      ("ROIC-normalized (b)", r.norm_eps_roic),
                      ("cycle-mean (c)", r.norm_eps_cycle)):
        if val and val > 0:
            r.norm_eps, r.method_used = val, name
            break
    if r.norm_eps is None and r.norm_eps_band and r.norm_eps_band[1] > 0:
        r.norm_eps = statistics.mean(r.norm_eps_band)
        r.method_used = "trough-anchored band (e)"
        r.warnings.append("band midpoint used — treat Peak Ratio as a bucket only")

    # --- Peak Ratio ----------------------------------------------------------
    if r.norm_eps and r.norm_eps > 0 and fwd_eps:
        r.peak_ratio = fwd_eps / r.norm_eps
        pr = r.peak_ratio
        r.peak_bucket = ("TROUGH (<=0.8) — 가장 유망" if pr <= 0.8 else
                         "NORMAL (0.8-1.4)" if pr <= 1.4 else
                         "PEAK 의심 (1.4-2.0) — 감점" if pr <= 2.0 else
                         "PEAK 강력의심 (>=2.0) — 이익방어계약 입증 없으면 배제")
    elif not fwd_eps:
        r.warnings.append("no --fwd-eps supplied — Peak Ratio not computed")

    # --- absolute valuation gate inputs --------------------------------------
    if r.norm_eps and r.norm_eps > 0:
        r.norm_pe = price / r.norm_eps
        # Normalized earnings yield, used as the FCF-yield proxy: maintenance
        # capex ~= D&A, which NOPAT already deducts. An approximation, not a
        # measurement - real FCF needs the cash-flow statement.
        r.norm_fcf_yield = r.norm_eps / price
    if mcap is not None and r.net_debt is not None:
        r.ev = mcap + r.net_debt
    if r.ev and r.invested_capital and r.invested_capital > 0:
        r.ev_over_ic = r.ev / r.invested_capital
    if r.median_roic is not None and r.wacc > TERMINAL_G:
        r.fair_ev_over_ic = (r.median_roic - TERMINAL_G) / (r.wacc - TERMINAL_G)
    if r.ev_over_ic and r.fair_ev_over_ic and r.fair_ev_over_ic > 0:
        r.ev_ic_ratio = r.ev_over_ic / r.fair_ev_over_ic
        r.ev_ic_discount = 1 - r.ev_ic_ratio
    if r.median_roic is not None and r.median_roic < r.wacc:
        r.warnings.append(
            f"median ROIC {r.median_roic*100:.1f}% < WACC {r.wacc*100:.1f}% — growth destroys "
            "value; GATE 2 (G2-4) fails and PEG is meaningless here")
    return r


# -------------------------------------------------------------------- reporting
def _f(v, pct=False, n=2):
    if v is None:
        return "확인 불가"
    return f"{v*100:,.1f}%" if pct else f"{v:,.{n}f}"


def report(r: Result) -> str:
    L = [
        f"\n{'='*70}",
        f" {r.ticker}   price {_f(r.price)}   annual history {r.years}y   WACC {_f(r.wacc, pct=True)}",
        f"{'='*70}",
        "\n[STEP 0-A] 사이클 노출 사전판정",
        f"  기계적 플래그: {', '.join(r.cyclicality_flags) if r.cyclicality_flags else '없음'}",
        f"  -> {'CYCLICAL TRACK (완전 정상화 필수)' if len(r.cyclicality_flags) >= 2 else 'STRUCTURAL/준시클리컬 TRACK'}",
        "  ※ 상품가격 연동·고객 capex 연동 여부는 정성 판정이므로 수동 확인 필요",
        "\n[STEP 0-B] Normalized EPS",
        f"  10y 중위 영업이익률        {_f(r.median_op_margin, pct=True)}",
        f"  10y 중위 ROIC             {_f(r.median_roic, pct=True)}",
        f"  실효세율(3y)              {_f(r.eff_tax, pct=True)}",
        f"  (a) 마진 정상화 EPS        {_f(r.norm_eps_margin)}",
        f"  (b) ROIC 정상화 EPS        {_f(r.norm_eps_roic)}",
        f"  (c) 사이클 평균 EPS        {_f(r.norm_eps_cycle)}",
        f"  (e) Trough 앵커 구간       "
        + (f"{_f(r.norm_eps_band[0])} ~ {_f(r.norm_eps_band[1])}" if r.norm_eps_band else "확인 불가"),
        f"  Peak EPS / Trough EPS     {_f(r.peak_eps)} / {_f(r.trough_eps)}",
        f"  >> 채택 Normalized EPS     {_f(r.norm_eps)}   [{r.method_used}]",
        "\n[PEAK RATIO]",
        f"  Forward EPS               {_f(r.fwd_eps)}",
        f"  Peak Ratio                {_f(r.peak_ratio)}",
        f"  판정                      {r.peak_bucket}",
        "\n[GATE 1 — Absolute Valuation 입력값]",
        f"  Normalized P/E            {_f(r.norm_pe)}x     (기준 <= 자기중위x0.6)",
        f"  Normalized 이익수익률     {_f(r.norm_fcf_yield, pct=True)}     (FCF Yield 프록시, 기준 >= 8%)",
        f"  EV                        {_f(r.ev, n=0)}",
        f"  EV/IC                     {_f(r.ev_over_ic)}x",
        f"  이론 적정 EV/IC           {_f(r.fair_ev_over_ic)}x   [(ROIC-g)/(WACC-g), g=4%]",
        f"  적정 대비                 "
        + ("확인 불가" if r.ev_ic_ratio is None else
           (f"{_f(r.ev_ic_discount, pct=True)} 할인  (기준 >= 40% 할인)" if r.ev_ic_ratio < 1
            else f"적정의 {_f(r.ev_ic_ratio)}배 — 프리미엄, GATE 1 탈락")),
    ]
    if r.fwd_eps and r.norm_eps:
        L.append(f"  Forward 기준 P/E(참고)    {_f(r.price / r.fwd_eps)}x  <-- 주 판정에 쓰지 말 것")
    if r.warnings:
        L.append("\n[경고]")
        L += [f"  ! {w}" for w in r.warnings]
    L.append("\n※ FCF Yield는 유지보수capex≈감가상각 가정의 근사치. EV/IC 할인율이 "
             "\n  절대 저평가의 이론적 주지표이며, 나머지는 보조지표.")
    return "\n".join(L)


def csv_row(r: Result) -> dict:
    return {
        "ticker": r.ticker, "price": r.price, "history_y": r.years,
        "median_op_margin": r.median_op_margin, "median_roic": r.median_roic,
        "norm_eps": r.norm_eps, "method": r.method_used,
        "fwd_eps": r.fwd_eps, "peak_ratio": r.peak_ratio, "peak_bucket": r.peak_bucket,
        "norm_pe": r.norm_pe, "norm_fcf_yield": r.norm_fcf_yield,
        "ev_over_ic": r.ev_over_ic, "fair_ev_over_ic": r.fair_ev_over_ic,
        "ev_ic_discount": r.ev_ic_discount, "ev_ic_ratio": r.ev_ic_ratio,
        "cyclicality_flags": "; ".join(r.cyclicality_flags),
        "warnings": "; ".join(r.warnings),
    }


# --------------------------------------------------------------------- selftest
def _synth_facts() -> dict:
    """A deliberately cyclical filer with a hand-checkable answer.

    margins  [.10 .05 -.05 .02 .15 .30 .08 -.02 .35 .50] -> median .09
    revenue latest 10,000 ; shares 1,000 ; effective tax 20%
    => margin-normalized EPS = 10000 * .09 * .8 / 1000 = 0.72
    """
    margins = [.10, .05, -.05, .02, .15, .30, .08, -.02, .35, .50]
    revs = [4000, 4500, 4200, 5000, 6000, 7000, 6500, 6200, 8500, 10000]
    facts: dict = {"facts": {"us-gaap": {}}}

    def put(tag, unit, rows):
        facts["facts"]["us-gaap"].setdefault(tag, {"units": {}})["units"][unit] = rows

    rev_rows, op_rows, ni_rows, eps_rows, sh_rows = [], [], [], [], []
    tax_rows, pre_rows, eq_rows, cash_rows, debt_rows = [], [], [], [], []
    for i, fy in enumerate(range(2017, 2027)):
        rev, op = revs[i], revs[i] * margins[i]
        pre = op
        tax = pre * 0.20 if pre > 0 else 0.0
        ni = pre - tax
        per = {"fy": fy, "fp": "FY", "form": "10-K", "filed": f"{fy+1}-02-15",
               "start": f"{fy}-01-01", "end": f"{fy}-12-31"}
        inst = {"fy": fy, "fp": "FY", "form": "10-K", "filed": f"{fy+1}-02-15", "end": f"{fy}-12-31"}
        rev_rows.append({**per, "val": rev})
        op_rows.append({**per, "val": op})
        ni_rows.append({**per, "val": ni})
        eps_rows.append({**per, "val": ni / 1000})
        sh_rows.append({**per, "val": 1000})
        tax_rows.append({**per, "val": tax})
        pre_rows.append({**per, "val": pre})
        eq_rows.append({**inst, "val": 5000})
        cash_rows.append({**inst, "val": 1000})
        debt_rows.append({**inst, "val": 2000})

    # a stray quarter that must be ignored by the annual filter
    rev_rows.append({"fy": 2026, "fp": "FY", "form": "10-K", "filed": "2027-02-15",
                     "start": "2026-10-01", "end": "2026-12-31", "val": 99999})
    # a restatement filed later that must win for FY2018
    rev_rows.append({"fy": 2018, "fp": "FY", "form": "10-K/A", "filed": "2020-06-01",
                     "start": "2018-01-01", "end": "2018-12-31", "val": 4500})

    put("Revenues", "USD", rev_rows)
    put("OperatingIncomeLoss", "USD", op_rows)
    put("NetIncomeLoss", "USD", ni_rows)
    put("EarningsPerShareDiluted", "USD/shares", eps_rows)
    put("WeightedAverageNumberOfDilutedSharesOutstanding", "shares", sh_rows)
    put("IncomeTaxExpenseBenefit", "USD", tax_rows)
    put("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "USD", pre_rows)
    put("StockholdersEquity", "USD", eq_rows)
    put("CashAndCashEquivalentsAtCarryingValue", "USD", cash_rows)
    put("LongTermDebtNoncurrent", "USD", debt_rows)
    return facts


def selftest() -> int:
    facts = _synth_facts()
    fails: list[str] = []

    def check(label, got, want, tol=1e-6):
        ok = got is not None and abs(got - want) <= tol
        print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
        if not ok:
            fails.append(label)

    print("\n--- extraction ---")
    rev = annual_series(facts, "revenue")
    check("10 annual revenue years (quarter filtered out)", float(len(rev)), 10.0)
    check("FY2026 revenue is the annual figure, not the stray quarter", rev[2026], 10000.0)
    check("FY2018 restated value wins", rev[2018], 4500.0)
    print(f"  INFO  _is_annual rejects a 92-day period: {not _is_annual('2026-10-01','2026-12-31')}")
    if _is_annual("2026-10-01", "2026-12-31"):
        fails.append("_is_annual quarter rejection")

    print("\n--- normalization (fwd EPS 3.00, price 60.00) ---")
    r = compute("SYNTH", facts, price=60.0, fwd_eps=3.00, wacc=0.10)
    check("effective tax rate", r.eff_tax, 0.20, 1e-9)
    check("10y median operating margin", r.median_op_margin, 0.09, 1e-9)
    check("margin-normalized EPS", r.norm_eps_margin, 0.72, 1e-9)
    check("chosen normalized EPS", r.norm_eps, 0.72, 1e-9)
    check("Peak Ratio = 3.00 / 0.72", r.peak_ratio, 3.00 / 0.72, 1e-9)
    check("invested capital = 5000 + 2000 - 1000", r.invested_capital, 6000.0, 1e-9)
    check("normalized P/E = 60 / 0.72", r.norm_pe, 60.0 / 0.72, 1e-9)

    print("\n--- gating behaviour ---")
    bucket_ok = "강력의심" in r.peak_bucket
    print(f"  {'PASS' if bucket_ok else 'FAIL'}  Peak Ratio 4.17 -> PEAK 강력의심 bucket: {r.peak_bucket}")
    if not bucket_ok:
        fails.append("peak bucket")
    flags_ok = len(r.cyclicality_flags) >= 2
    print(f"  {'PASS' if flags_ok else 'FAIL'}  cyclicality flags >= 2: {r.cyclicality_flags}")
    if not flags_ok:
        fails.append("cyclicality flags")
    fwd_pe = 60.0 / 3.00
    trap_ok = fwd_pe < 21 and r.norm_pe > 60
    print(f"  {'PASS' if trap_ok else 'FAIL'}  trap exposed: Forward P/E {fwd_pe:.1f}x looks cheap "
          f"but Normalized P/E is {r.norm_pe:.1f}x")
    if not trap_ok:
        fails.append("trap exposure")

    print("\n--- degradation: no forward EPS ---")
    r2 = compute("SYNTH", facts, price=60.0, fwd_eps=None, wacc=0.10)
    deg_ok = r2.peak_ratio is None and r2.peak_bucket == "확인 불가" and r2.norm_eps is not None
    print(f"  {'PASS' if deg_ok else 'FAIL'}  Peak Ratio '확인 불가', normalized EPS still computed "
          f"({_f(r2.norm_eps)})")
    if not deg_ok:
        fails.append("graceful degradation")

    print(report(r))
    print(f"\n{'='*70}\n{'SELFTEST FAILED: ' + ', '.join(fails) if fails else 'SELFTEST: all checks passed'}\n{'='*70}")
    return 1 if fails else 0


# -------------------------------------------------------------------------- cli
def main() -> int:
    p = argparse.ArgumentParser(description="Normalized EPS / Peak Ratio from SEC XBRL")
    p.add_argument("ticker", nargs="?", help="US ticker, e.g. MU")
    p.add_argument("--price", type=float, help="current share price (SEC has no prices)")
    p.add_argument("--fwd-eps", type=float, help="forward consensus EPS (SEC has no estimates)")
    p.add_argument("--wacc", type=float, help="override WACC, e.g. 0.095")
    p.add_argument("--years", type=int, default=10)
    p.add_argument("--cache", help="read companyfacts JSON from this dir or file")
    p.add_argument("--save-cache", help="save fetched companyfacts JSON into this dir")
    p.add_argument("--batch", help="CSV with columns ticker,price,fwd_eps")
    p.add_argument("--csv-out", help="write results to this CSV")
    p.add_argument("--selftest", action="store_true", help="verify the maths, no network")
    a = p.parse_args()

    if a.selftest:
        return selftest()

    jobs: list[tuple[str, float, float | None]] = []
    if a.batch:
        with open(a.batch, newline="") as fh:
            for row in csv.DictReader(fh):
                fe = row.get("fwd_eps") or ""
                jobs.append((row["ticker"], float(row["price"]), float(fe) if fe.strip() else None))
    elif a.ticker and a.price is not None:
        jobs.append((a.ticker, a.price, a.fwd_eps))
    elif a.ticker and a.save_cache:
        load_facts(a.ticker, None, a.save_cache)
        print(f"cached companyfacts for {a.ticker.upper()} -> {a.save_cache}")
        return 0
    else:
        p.error("need TICKER --price, or --batch FILE, or --selftest, or TICKER --save-cache DIR")

    results = []
    for tk, px, fe in jobs:
        try:
            facts = load_facts(tk, a.cache, a.save_cache)
        except SystemExit as exc:
            print(f"{tk}: {exc}", file=sys.stderr)
            continue
        r = compute(tk, facts, px, fe, a.wacc, a.years)
        results.append(r)
        print(report(r))

    if a.csv_out and results:
        with open(a.csv_out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(csv_row(results[0])))
            w.writeheader()
            for r in results:
                w.writerow(csv_row(r))
        print(f"\nwrote {len(results)} rows -> {a.csv_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
