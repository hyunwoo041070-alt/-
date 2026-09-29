# Forward Earnings Compression 스크리닝 — "성장이 밸류에이션을 따라잡는 기업" 발굴

- **검색 기준일**: 2026-09-29 (KST)
- **주가 기준**: 미국/ADR 2026-09-28 종가, 한국·일본 2026-09-29 종가 (Yahoo Finance)
- **컨센서스 기준**: Yahoo Finance EPS Trend/Revision (2026-09-29 조회, LSEG 기반), StockAnalysis(S&P Global) 재무·ROIC (2026-09-20~28 업데이트)
- **태그**: [A] Actual · [G] Guidance · [C] Consensus · [M] Model(본 분석 가정) · [I] Implied(현재가 역산)
- **FY 정의**: FY+1 = 아직 보고되지 않은 첫 회계연도(진행 중인 연도), FY+2 = 그 다음 연도. Current P/E = 최근 4개 분기 조정 EPS 합(LTM) 기준. 해외 ADR은 EPS 통화를 주가 통화로 환산했다.
- **원자료**: [`2026-09-29_screen_data.csv`](./2026-09-29_screen_data.csv) (382개 종목 전체 지표·점수)

> **한 줄 결론**: 현재 가격 대비 1~3년 이익 성장의 불균형이 가장 큰 곳은 여전히 **AI 인프라 핵심 공급망**이다. 7월 반도체 급락 이후 주가는 제자리이거나 하락했지만 FY+2 EPS는 계속 상향돼 멀티플이 오히려 압축됐다. 1순위는 **NVIDIA**(FY+2 P/E 14.6x, 2Y EPS CAGR 81%, PEG 0.21, FY+2 EPS 90일 +23%)다. 그 뒤로 **Celestica**, **Broadcom**, **TSMC**, **Credo**가 Top 5다. 메모리 5종(MU, SK하이닉스, 삼성전자, SanDisk, Kioxia)은 FY+2 P/E 4~7배로 표면상 가장 싸지만 **Cyclical Peak Trap 검증 전까지 순위에서 분리**했다.

---

## 0. 시장 맥락 (스크리닝 해석에 필요한 최소한)

| 항목 | 내용 | 태그 |
|---|---|---|
| 7월 말 AI 반도체 급락 | SOX 하루 -6%, 4거래일 연속 하락. Nasdaq-100은 고점 대비 -9.7%, KOSPI -11%. Alphabet이 2026 Capex를 $205B로 상향한 것이 "AI 과잉투자" 공포를 촉발했다 | [A] ([Fortune](https://fortune.com/2026/07/28/why-are-stocks-down-chips-panic-semiconductors/)) |
| 반도체 이익 vs 주가 | 당시 섹터 가격은 선행 이익성장 28%만 반영했지만 실제 성장률은 70% 수준이었다는 분석 | [I]/[C] (동일 출처) |
| 메모리 슈퍼사이클 | MU FQ4(8월 분기) 매출 컨센서스 $51B(+353% YoY), **9/30 장 마감 후 발표** 예정. 하이퍼스케일러가 2027년 상반기 메모리를 4Q26보다 비싸게 사기로 합의했다(BofA) | [C] ([Yahoo](https://finance.yahoo.com/markets/stocks/articles/micron-earnings-preview-analysts-see-022234081.html)) |
| 3개월 주가 괴리 | AI 2차 수혜주(CRDO -22%, AMAT -30%, COHR -28%, MKSI -38%, TTMI -34%)는 급락했지만 FY+2 EPS는 +9~28% 상향됐다 | [A]/[C] |
| 소프트웨어 디레이팅 | ADBE FY+2 8.3x, HUBS 12x, INTU 9.9x. AI 대체 우려와 성장 둔화가 겹쳐 Value Trap 후보가 다수 생겼다 | [C] |

**함의**: 이번 스크리닝에서 "EPS Revision > 주가 상승률"인 종목, 즉 주가가 가만히 있어도 Forward P/E가 저절로 내려간 종목이 대거 포착됐다. 반대로 상위권이 한 가지 요인(AI Capex)에 몰려 있다는 점은 포트폴리오 차원에서 반드시 관리해야 한다(§11).

---

## 1. 스크리닝 Funnel

| 단계 | 기준 | 통과 종목 수 |
|---|---|---|
| Universe | 미국 상장(ADR 포함) 260 + 한국 34 + 일본 39 + 유럽 49 | 382 |
| 컨센서스 확보 | FY0·FY+1·FY+2 EPS가 모두 존재하고 양수 | 356 |
| 1단계 Growth Screen | (FY+1, FY+2 평균 매출성장 > 15%) AND (2Y EPS CAGR > 18%) | 154 |
| 2단계 Compression/PEG | PEG 2Y < 1.5 OR FY+2 Compression > 35% | 144 |
| 5단계 Revision | FY+2 EPS 90일 변화 ≥ -2% | 131 |
| 정량 100점 채점 → 상위 53개 정성 조정 | Catalyst, 리스크, False Positive 반영 | 53 |
| False Positive 분리 | Cyclical Peak(메모리 7), Turnaround, M&A, 저품질 성장 | → **Top 20** |

**점수 산식(요약)**: A. Growth 20 = 매출성장 7 + EPS CAGR 7 + 가속 3 + EPS>매출 레버리지 3. B. Valuation 20 = FY+2 P/E 6 + PEG 2Y 7 + FY+2 Compression 7. C. Revision 15 = 상태(1~5)×3, EPS 상향폭이 3개월 주가 상승률을 넘으면 +1.5. D. Quality 15 = ROIC 6 + FCF Margin 5 + 주식수 ±2 + 이익률 확대 2. E. Expectation Gap 10 = 컨센서스 경로 5Y EPS CAGR − 현재가 요구 CAGR. F. Catalyst 10(정성). G. Balance Sheet/Risk 10 = 순부채/EBITDA와 리스크 플래그. 상세는 §13.

---

## 2. False Positive 제거 결과 (11단계)

### A. Cyclical Peak Trap: 점수는 높지만 순위에서 분리

| 기업 | 주가 | FY0 EPS [A] | FY+1 EPS [C] | FY+2 EPS [C] | FY+2 P/E | LTM 영업이익률 | 직전 사이클 고점(2018) OPM | 판정 |
|---|---|---|---|---|---|---|---|---|
| Micron (MU) | $1,053.98 | $8.29 (FY25) | $73.71 (FY26, 9/30 발표) | $161.09 (FY27) | 6.5x | ~80% | ~49% | Peak 검증 필요 |
| SK하이닉스 (000660) | ₩1,765,000 | ₩60,372 | ₩354,324 | ₩472,677 | 3.7x | ~76% | ~51.5% | Peak 검증 필요 |
| 삼성전자 (005930) | ₩272,500 | ₩6,605 | ₩48,312 | ₩71,422 | 3.8x | ~52% | ~24% | Peak 검증 필요 |
| SanDisk (SNDK) | $1,712.89 | $70.88 | $213.90 | $263.49 | 6.5x | ~78% | n/a | Peak 검증 필요 |
| Kioxia (285A) | ¥17,880 | ¥341 | ¥3,465 | ¥4,740 | 3.8x | ~72% | n/a | Peak 검증 필요 |
| Western Digital (WDC) | $453.23 | $10.22 | $20.09 | $31.75 | 14.3x | ~44% | n/a | HDD 가격 사이클 |
| Seagate (STX) | $921.51 | $15.58 | $35.78 | $55.37 | 16.6x | ~43% | n/a | HDD 가격 사이클 |

- 현재 이익률이 과거 사이클 고점의 1.5~2배다. P/E 4~7배는 **Peak EPS × 낮은 멀티플**이라는 전형적인 사이클 구조와 구분되지 않는다.
- Mid-cycle/Normalized EPS 컨센서스는 **확인 불가**다. 정밀분석 시 과거 10년 평균 ROIC/이익률을 FY+2 매출 컨센서스에 적용하는 정규화 작업이 필수다.
- 정량 점수(WDC 83, MU 82.5, SNDK 81, SK하이닉스 80, STX 79, 삼성전자 79, Kioxia 76.5)만 보면 Top 20에 들어간다. **9/30 MU 실적과 2027년 가격 협상이 구조적 성장(HBM·장기계약)의 증거가 되는지** 확인한 뒤 별도 트랙으로 편입을 검토한다.

### B. 기타 제거·감점 사례

| 유형 | 종목 | 이유 |
|---|---|---|
| Turnaround Illusion | STM, KLIC, INTC, LI, XPEV | 낮은 기저 때문에 EPS 성장률이 수백 %로 부풀었다(STM FY0 EPS $0.53 → FY+2 $2.53). 성장 점수 신뢰도를 하향 |
| One-off(투자이익) | GOOGL, AMZN, GEV | FY+1 EPS에 대규모 평가이익이 들어 있다(GOOGL FY26 $20.64 → FY27 $14.94, AMZN $12.88 → $10.50). Compression 계산이 왜곡된다 |
| M&A-driven | SANM(ZT Systems 제조), HPE(Juniper), STRL(CEC), TLN(발전소 인수) | Reported와 Organic 성장이 분리되지 않는다 |
| Buyback 기여 | EXPE(주식수 YoY -6%) | 매출성장 7~10%로 1단계 Growth Screen 미달 |
| Low-Quality Growth | ORCL(TTM FCF -$28.7B, Capex/매출 105%, 순부채 $132B, ROIC 16%→11%), COHR(FCF 적자, ROIC 7%), TTMI(FCF 적자) | "성장↑ + ROIC↓ + Capex↑ + FCF↓" 경계 패턴 |
| Cyclical Peak 의심 | DELL | FY+2 EPS -5%(FY+1 +151%)로 컨센서스 자체가 피크를 가정 |
| Value Trap 후보 | HUBS(가이던스 하향, 신규고객 미달, 52주 -57%), APP(Q2 가이던스 미달, EPS Revision 하향, 집단소송), ADBE/INTU/CRM | 낮은 P/E와 약한 Revision·성장 둔화가 겹침 |

---

## 3. Top 20 (15단계)

| 순위 | 기업 | 티커 | 유형 | Revenue Growth FY+1/FY+2 [C] | EPS CAGR 2Y [C] | FY+1 P/E | FY+2 P/E | PEG 2Y | ROIC [A] | Revision (FY+2 EPS 90일) | 점수 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NVIDIA | NVDA | High-Growth at Fair Price + Earnings Revision | 91% / 66% | 81% | 24.6x | 14.6x | 0.21 | 92% | 5 (+23.4%) | 94 (S+) |
| 2 | Celestica | CLS | Earnings Revision Play / Growth Inflection | 66% / 71% | 79% | 31.8x | 18.4x | 0.26 | 42% | 5 (+33.8%) | 85.5 (S) |
| 3 | Broadcom | AVGO | High-Growth at Fair Price | 66% / 64% | 69% | 30.0x | 18.0x | 0.27 | 31% | 3 (-0.4%) | 85 (S) |
| 4 | TSMC (ADR) | TSM | Quality Compounder / GARP | 43% / 35% | 43% | 26.7x | 20.7x | 0.50 | 54% | 5 (+11.5%) | 84 (A+) |
| 5 | Credo Technology | CRDO | High-Growth at Fair Price / Earnings Revision | 87% / 55% | 67% | 30.6x | 19.9x | 0.37 | 38% | 5 (+8.9%) | 84 (A+) |
| 6 | AMD | AMD | Growth Inflection | 47% / 73% | 93% | 80.2x | 39.0x | 0.48 | 10% | 5 (+18.2%) | 84 (A+) |
| 7 | 에이피알(APR) | 278470 KS | High-Growth at Fair Price | 102% / 35% | 67% | 23.2x | 16.8x | 0.27 | n/a (ROE 82%) | 5 (+13.7%) | 82.5 (A+) |
| 8 | Vertiv | VRT | Quality Compounder / Growth | 37% / 30% | 48% | 36.2x | 26.6x | 0.60 | 38% | 4 (+4.1%) | 80.5 (A+) |
| 9 | Applied Materials | AMAT | Earnings Revision Play (WFE 사이클) | 21% / 35% | 40% | 38.1x | 26.4x | 0.68 | 36% | 5 (+12.5%) | 80.0 (A+) |
| 10 | Reddit | RDDT | High-Growth at Fair Price | 54% / 32% | 64% | 26.6x | 20.2x | 0.34 | 164% | 5 (+9.2%) | 79.5 (A) |
| 11 | ASML (ADR) | ASML | Quality Compounder + Revision | 31% / 27% | 45% | 40.7x | 30.1x | 0.72 | 66% | 5 (+22.9%) | 79.5 (A) |
| 12 | Flex | FLEX | GARP + Spin-off | 24% / 30% | 46% | 24.0x | 16.0x | 0.42 | 15% | 4 (+1.5%) | 78.0 (A) |
| 13 | Onto Innovation | ONTO | Earnings Revision Play (장비 사이클) | 43% / 31% | 54% | 35.6x | 24.7x | 0.50 | 13% | 5 (+17.5%) | 78.0 (A) |
| 14 | Lumentum | LITE | Earnings Revision Play | 110% / 52% | 100% | 42.3x | 26.5x | 0.37 | 16% | 5 (+22.8%) | 76.5 (A) |
| 15 | Nu Holdings | NU | GARP | 45% / 24% | 37% | 14.3x | 11.1x | 0.32 | 106% | 4 (+1.9%) | 76.0 (A) |
| 16 | Comfort Systems USA | FIX | Quality Compounder | 43% / 19% | 44% | 33.8x | 27.6x | 0.65 | 77% | 5 (+13.1%) | 75.5 (A) |
| 17 | Toast | TOST | GARP | 21% / 18% | 31% | 21.9x | 17.5x | 0.60 | 146% | 4 (+2.2%) | 74.5 (B+) |
| 18 | Rorze(ローツェ) | 6323 JP | Earnings Revision Play | 143% / 18% | 51% | 19.4x | 15.5x | 0.33 | n/a (ROE 15%) | 5 (+29.4%) | 74.5 (B+) |
| 19 | Semtech | SMTC | Earnings Revision Play | 42% / 29% | 85% | 50.3x | 29.9x | 0.41 | 14% | 5 (+50.2%) | 74.0 (B+) |
| 20 | HD현대중공업 | 329180 KS | Cyclical Recovery (조선) | 42% / 7% | 51% | 13.8x | 12.0x | 0.24 | n/a (ROE 30%) | 4 (+5.8%) | 74.0 (B+) |

- 동점 처리: 프롬프트의 유형 우선순위(GARP > High-Growth at Fair Price > Earnings Revision > Growth Inflection > Quality Compounder)를 적용했다(TSM > CRDO > AMD, TOST > Rorze, SMTC > HD현대중공업).
- **Top 20 경계선 탈락(참고)**: ON(74.5, 매출성장 11%로 1단계 미달), STM(74.5, Turnaround), LRCX(73.5), STRL(73, M&A 혼재·FY+2 Revision -6%), ADI(72.5), LLY(71, 비AI Quality Compounder로 분산 대안), APP(71, Revision 하향).
- ROIC는 StockAnalysis(S&P Global) TTM 정의를 쓴다. 한국·일본 종목은 ROIC 확인 불가이므로 ROE를 표시했다.

### Growth-Adjusted Valuation 상세 (2·3·7·8단계)

| 기업 | 주가 | LTM P/E | NTM P/E | FY+1 P/E | FY+2 P/E | FY+2 Compression | 등급 | PEG 1Y | PEG 2Y | 현재가 요구 EPS CAGR [I] | 컨센서스 경로 5Y [M] | Gap | 12M Base [M] | Bear [M] | Stress [M] | 목표가 괴리 [C] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NVIDIA | 228.86 | 32.6x | 16.9x | 24.6x | 14.6x | 55% | SS | 0.18 | 0.21 | 8.7% | 36.6% | +27.9%p | +35% | -19% | -45% | +43% |
| Celestica | 356.53 | 43.6x | 20.6x | 31.8x | 18.4x | 58% | SS | 0.24 | 0.26 | 13.0% | 38.5% | +25.5%p | +42% | -15% | -48% | +32% |
| Broadcom | 349.57 | 35.8x | 18.7x | 30.0x | 18.0x | 50% | S | 0.26 | 0.27 | 10.8% | 35.6% | +24.7%p | +41% | -15% | -50% | +52% |
| TSMC (ADR) | 452.88 | 32.7x | 21.9x | 26.7x | 20.7x | 37% | A | 0.37 | 0.50 | 14.4% | 18.5% | +4.1%p | +18% | -29% | -34% | +22% |
| Credo | 192.67 | 47.0x | 25.0x | 30.6x | 19.9x | 58% | SS | 0.30 | 0.37 | 17.4% | 29.9% | +12.5%p | +40% | -16% | -35% | +45% |
| AMD | 607.87 | 105.5x | 44.9x | 80.2x | 39.0x | 63% | SS | 0.55 | 0.48 | 32.1% | 52.9% | +20.8%p | +60% | -4% | -55% | +2% |
| 에이피알 | ₩362,500 | 47.0x* | 18.0x | 23.2x | 16.8x | 64%* | SS | 0.18 | 0.27 | 10.1% | 22.9% | +12.8%p | +23% | -26% | -38% | +45%† |
| Vertiv | 244.04 | 46.1x | 28.6x | 36.2x | 26.6x | 42% | A | 0.47 | 0.60 | 20.6% | 21.6% | +1.0%p | +22% | -27% | -37% | +39% |
| Applied Materials | 486.76 | 44.6x | 27.1x | 38.1x | 26.4x | 41% | A | 0.76 | 0.68 | 19.4% | 25.5% | +6.1%p | +24% | -26% | -43% | +31% |
| Reddit | 143.08 | 33.3x | 21.6x | 26.6x | 20.2x | 39% | A | 0.20 | 0.34 | 14.0% | 19.4% | +5.4%p | +19% | -29% | -35% | +49% |
| ASML (ADR) | 1,771.41 | 56.6x | 32.3x | 40.7x | 30.1x | 47% | S | 0.59 | 0.72 | 23.6% | 21.1% | -2.5%p | +21% | -27% | -37% | +19% |
| Flex | 113.04 | 31.5x | 19.2x | 24.0x | 16.0x | 49% | S | 0.45 | 0.42 | 11.5% | 28.0% | +16.6%p | +35% | -19% | -36% | +42% |
| Onto Innovation | 288.74 | 52.2x | 26.8x | 35.6x | 24.7x | 53% | S | 0.42 | 0.50 | 19.1% | 25.4% | +6.3%p | +26% | -24% | -40% | +34% |
| Lumentum | 921.32 | 110.1x | 36.9x | 42.3x | 26.5x | 76% | SS | 0.24 | 0.37 | 27.0% | 32.5% | +5.6%p | +49% | -10% | -30% | +26% |
| Nu Holdings | 12.23 | 16.6x | 11.8x | 14.3x | 11.1x | 33% | - | 0.25 | 0.32 | 1.0% | 18.1% | +17.0%p | +17% | -30% | -34% | +53% |
| Comfort Systems | 1,658.30 | 40.8x | 28.9x | 33.8x | 27.6x | 32% | - | 0.42 | 0.65 | 20.9% | 15.3% | -5.7%p | +14% | -32% | -32% | +32% |
| Toast | 30.38 | 25.5x | 18.5x | 21.9x | 17.5x | 31% | - | 0.50 | 0.60 | 10.5% | 16.4% | +5.8%p | +15% | -31% | -33% | +28% |
| Rorze | ¥3,880 | 35.5x* | 16.9x | 19.4x | 15.5x | 56%* | SS | 0.20 | 0.33 | 8.7% | 16.4% | +7.8%p | +17% | -30% | -30% | +61%† |
| Semtech | 174.78 | 81.7x | 34.7x | 50.3x | 29.9x | 63% | SS | 0.34 | 0.41 | 25.4% | 36.3% | +10.8%p | +42% | -15% | -45% | +19% |
| HD현대중공업 | ₩429,000 | 16.9x | 12.4x | 13.8x | 12.0x | 29% | - | 0.13 | 0.24 | 2.1% | 11.5% | +9.4%p | +10% | -34% | -28% | (확인 필요)† |

\* LTM 분기 EPS를 확보할 수 없어 FY0 실적 P/E로 대체했다. † 한국·일본 목표주가 컨센서스는 Yahoo 집계로 갱신이 지연됐을 수 있어 신뢰도가 낮다.

**모델 정의 [M]/[I]**
- **현재가 요구 EPS CAGR [I]**: 요구수익률 10%, 5년 후 Exit P/E 18x(메모리는 12x)를 가정해 현재가를 정당화하는 NTM EPS의 5년 CAGR.
- **컨센서스 경로 5Y [M]**: FY+2 EPS 성장률에서 출발해 5년 차 8%까지 선형 감속한다고 가정.
- **12M Base [M]**: 12개월 후 NTM EPS × 현재 NTM P/E(멀티플 불변). FY+3 EPS는 컨센서스를 확인할 수 없어 FY+2 × (1 + 0.5×FY+2 성장률, 하한 8%)로 가정했다. NVDA는 +25%, AVGO는 +40%(FY28 AI 매출 $230B 가이던스 반영).
- **Bear [M]**: Base 경로 EPS -25%, 멀티플 -20%(= Base × 0.6).
- **Stress [M]**: EPS가 FY+1 수준에서 정체되고 멀티플 -20%. AI Capex 급감 시나리오.

---

## 4. Top 10 (Thesis · 시장이 놓치고 있는 것 · Catalyst · 주요 위험)

**1. NVIDIA (NVDA): 94점, S+, ★★ Exceptional**
- **Thesis**: Q2 FY27 매출 $96.2B(+106% YoY), 데이터센터 $89.0B(+117%), GM 75.0% [A]. Q3 가이던스는 $108B ±2%다 [G]. 경영진은 FY28 매출 성장 약 70%를 언급했다 [G]. 컨센서스는 FY28 매출 $683B(+66%), EPS $15.68이다 [C].
- **시장이 놓치고 있는 것**: FY28 EPS가 90일간 +23% 상향($12.71 → $15.68)되는 동안 주가는 +17%에 그쳐 FY+2 P/E가 14.6x로 내려왔다. 현재가는 FY28 이후 EPS 성장이 연 8.7%로 급감한다고 가정한다 [I].
- **Catalyst**: 11월 중순 Q3 실적과 Q4 가이던스, Rubin 램프, 9/30 MU 실적(HBM 공급 신호).
- **위험**: 하이퍼스케일러 Capex 소화, 고객 집중, AI 기업 지분투자와 공급계약이 얽힌 순환 구조, 수출규제, CoWoS/HBM/전력 제약.

**2. Celestica (CLS): 85.5점, S, ★ Alpha**
- **Thesis**: 2026 가이던스를 매출 $20.5B(+66%), 조정 EPS $11.30으로 상향했다 [G]. **2027 매출성장이 2026년의 65%보다 가속하고 EPS가 매출보다 빨리 성장한다**고 명시했다 [G]. OpenAI 랙, AMD Helios, 1.6T 스위치 10개 프로그램이 동력이다.
- **시장이 놓치고 있는 것**: 가이던스를 산술 적용하면 2027 EPS는 $18.6 이상이다. FY+2 컨센서스는 30일간 +30% 상향된 $19.36으로 이를 따라잡았지만, 주가는 3개월간 +4%에 그쳤다. ROIC는 13% → 22% → 37% → 42%로 상승 중이다 [A].
- **Catalyst**: **10/27 Q3 실적과 Investor Day**(2027~28 목표 제시 가능성).
- **위험**: 8월 $3B 유상증자(주당 $310, 약 9~10% 희석) [A], FCF Margin 3.3%, 2026E FCF $240M [C], 고객 집중, FY+2 추정 애널리스트가 9명뿐이다.

**3. Broadcom (AVGO): 85점, S, Alpha 근접(Revision 중립)**
- **Thesis**: Q3 FY26 매출 $29.6B(+86%), AI 반도체 $16.7B(+221%) [A]. Q4 가이던스는 매출 $34.8B, AI $21.7B다 [G]. **AI 매출 가이던스는 FY26 $58B → FY27 $115B → FY28 $230B**다 [G].
- **시장이 놓치고 있는 것**: FY28 AI 매출 $230B는 FY+2(FY27) 컨센서스에 들어 있지 않다. FY+3 EPS를 보수적으로 $27(+40%) [M]로 잡아도 FY+3 P/E는 12.9x다. 가이던스 발표 이후 주가는 오히려 -6%다.
- **Catalyst**: 12월 Q4 실적과 FY27 가이던스, 신규 XPU 고객 발표.
- **위험**: 고객 집중(Google TPU·Meta·OpenAI·Anthropic), 랙 단위 매출 확대에 따른 GM 희석, 순부채 $35B(순부채/EBITDA 0.7x), SBC/매출 9.5%. FY+2 Revision이 정체(-0.4%)되어 점수가 깎였다.

**4. TSMC (TSM): 84점, A+**
- **Thesis**: 2026 매출성장 가이던스를 "40%대 초반(USD)"으로 상향했다 [G]. Q2 GM 67.7%, 7월 매출 +44.7% [A]. ROIC는 32% → 38% → 51% → 54%로 우상향이다 [A].
- **시장이 놓치고 있는 것**: 현재가는 5년 EPS CAGR 14%만 요구한다 [I]. N2 가격 인상과 AI 비중 확대에 따른 이익 지속기간은 반영되지 않았다.
- **Catalyst**: 10월 중순 Q3 실적과 2027 가이던스, 월간 매출(10/10).
- **위험**: 지정학, 관세, Capex $60~64B, 해외 팹의 마진 희석.

**5. Credo (CRDO): 84점, A+, ★ Alpha**
- **Thesis**: Q1 FY27 매출 $479M(+115%), 조정 EPS $1.20 [A]. FY27 매출성장 가이던스 **85% 초과**, 광학 매출 $600M 초과 [G]. Q2 가이던스는 $525~535M다 [G].
- **시장이 놓치고 있는 것**: 실적 발표 다음 날 -20%, 3개월 -22%로 주가는 내렸지만 FY+2 EPS는 +8.9% 올라 FY+2 P/E가 19.9x로 압축됐다.
- **Catalyst**: 12월 초 Q2 실적, 신규 10% 고객 추가 [A], 광학(ZeroFlap) 램프.
- **위험**: 상위 4개 고객 매출 비중 84%(33/28/13/10%) [A], GAAP GM 64.5%(전분기 68.2%), SBC/매출 14.8%, Q1 FCF $83M으로 조정 순이익 $236M 대비 전환율이 약하다.

**6. AMD (AMD): 84점, A+**
- **Thesis**: 2027 데이터센터 매출이 2배 이상, 서버 CPU +70% 이상 [G]. OpenAI·Meta 다년 계약과 Anthropic 최대 2GW MI450(1H27 배치)이 있다 [A]. EPS는 FY26 $7.58 → FY27 $15.58 [C].
- **시장이 놓치고 있는 것**: LTM P/E 105x만 보면 탈락하지만 FY+2 P/E는 39x, PEG 0.48이다. "현재 P/E는 높지만 실제로는 싼" 전형적인 사례다.
- **Catalyst**: 11월 초 Q3 실적, MI450/Helios 첫 출하.
- **위험**: OpenAI 워런트 희석, MI450 실행 리스크, 절대 멀티플 부담, 컨센서스 목표가 괴리 +2%로 주가가 이미 목표가에 근접했다.

**7. 에이피알 (278470 KS): 82.5점, A+, ★ Alpha(ROIC 확인 불가, ROE 82%)**
- **Thesis**: 2Q26 매출 ₩7,675억(+134%), 영업이익 ₩1,906억(+134.5%), OPM 24.8% [A]. 상반기 매출 ₩1.36조로 2025년 연간(₩1.53조)에 육박했다. 북미·유럽 비중은 40%에서 68%로 늘었다 [A].
- **시장이 놓치고 있는 것**: FY+2 P/E 16.8x, PEG 0.27, 순현금, FCF 흑자로 소비재 중 가장 강한 Earnings Inflection이다. 3개월 주가는 0%다.
- **Catalyst**: 11월 3Q 실적, 유럽 채널 확장, 뷰티 디바이스 신제품.
- **위험**: K-뷰티 트렌드 지속성, 아마존·틱톡 등 채널 집중, 관세와 환율.

**8. Vertiv (VRT): 80.5점, A+**
- **Thesis**: Q2 매출 $3.27B(+24%), 조정 EPS $1.52(+60%), 조정 OPM 22.6%(+410bp) [A]. 2026 가이던스는 매출 $14.0B(유기적 +31%), EPS $6.70이다 [G]. ROIC는 18% → 38%, FCF는 $0.77B → $2.93B(TTM)로 동반 개선됐다 [A].
- **시장이 놓치고 있는 것**: 이익률 레버리지다. 하지만 FY+2 P/E 26.6x는 이를 상당 부분 반영했다(Gap +1%p).
- **Catalyst**: 10월 말 Q3 실적과 수주잔고, 액체냉각 신규 계약.
- **위험**: 멀티플 부담, 생산능력 증설 실행, 경쟁 심화.

**9. Applied Materials (AMAT): 80점, A+**
- **Thesis**: Q3 FY26 매출 $9.12B(+25%), EPS $3.50(+41%) [A]. 2026~27 WFE 성장의 약 80%가 선단 로직, DRAM, 첨단 패키징에서 나온다 [G].
- **시장이 놓치고 있는 것**: 3개월 주가 -30%, 같은 기간 FY+2 EPS +12.5%. 중국 둔화와 시스템 출하 가이던스 소폭 하향(44% → 42%)에 과잉 반응했다.
- **Catalyst**: 11월 중순 Q4 실적과 FY27 WFE 전망.
- **위험**: 중국 매출, WFE 사이클, 메모리 Capex 피크 논쟁.

**10. Reddit (RDDT): 79.5점, A**
- **Thesis**: Q2 매출 $805M(+61%), EPS $1.25(컨센서스 $0.96) [A]. Q3 가이던스 $860~870M은 컨센서스 $828M를 웃돈다 [G].
- **시장이 놓치고 있는 것**: 검색 유입 변동성 한 가지 우려로 3개월 -18%가 됐다. 그동안 FY+1 EPS는 +8.3%, FY+2 EPS는 +9.2% 상향됐다.
- **Catalyst**: 10월 말 Q3 실적, 해외 광고와 데이터 라이선스 갱신.
- **위험**: Google 트래픽 의존, AI 답변엔진의 클릭 잠식, SBC/매출 12%, 주식수 +8% YoY.

**11~20위 한 줄 요약**
- **ASML**: 2026 매출 가이던스를 €43~45B로 두 차례 상향했고 [G], EUV 생산능력을 2027년 +30% 늘린다 [G]. 다만 Gap -2.5%p로 이미 선반영.
- **Flex**: FY27 EPS 가이던스 $4.42~4.74(+39%) [G]. **CPI 사업(Axiom) 스핀오프가 1Q CY27 완료 예정**이라 SOTP 재평가 여지가 있다. FCF Margin 3%.
- **Onto**: 첨단 패키징 성장 전망을 50% → 80%로 올렸고, 수주잔고가 처음으로 $1B를 넘었다 [G/A]. ROIC 13%.
- **Lumentum**: FQ1 가이던스 매출 $1.225~1.275B, EPS $4.05~4.35 [G], CPO 수억 달러 추가 수주 [A]. 전환사채 희석과 +466%(52주) 급등 부담.
- **Nu**: Q2 순이익 $1.1B(+49%), ROE 33% [A]. FY+2 P/E 11.1x로 ★★ 조건을 충족하지만 **Monzo 인수 협상(£8~10B)**이 희석 리스크다.
- **Comfort Systems**: ROIC 26% → 77%, FCF 4배 증가로 Quality는 최상이다. Gap -5.7%p로 이미 선반영.
- **Toast**: 2026 조정 EBITDA 가이던스 $805~825M로 상향 [G], 순신규 매장 9,500개로 사상 최대 [A].
- **Rorze**: 1Q 반도체 수주 +188%, 수주잔고 +128% [A]. 주요 고객 AMAT 비중 21.9% [A].
- **Semtech**: Q3 가이던스 $405~415M로 컨센서스 $324.5M를 크게 웃돌았다 [G]. 데이터센터 +160% YoY 예상. 주식수 +15%, 순부채.
- **HD현대중공업**: FY+2 P/E 12.0x, 순현금이지만 FY+2 매출성장이 7%로 급감속하는 조선 사이클 종목이다.

---

## 5. Top 5 상세

### ① NVIDIA (NVDA)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | NVIDIA Corp. / NVDA (NASDAQ) |
| 2 | 현재가 | $228.86 (2026-09-28 종가) |
| 3 | 시가총액 | $5.53T |
| 4 | 사업 유형 | AI 가속기(GPU)·네트워킹·랙 시스템 플랫폼 |
| 5 | 현재 핵심 사업 변화 | Q2 FY27 매출 $96.2B(+106%), 데이터센터 $89.0B(+117%), GM 75.0% [A]. Q3 가이던스 $108B ±2% [G]. FY28 매출 약 70% 성장 언급 [G] |
| 6 | NTM Revenue Growth | +95% [C] (NTM $590B vs LTM $303B) |
| 7 | 2Y Revenue CAGR | +78% [C] (FY26 $215.9B → FY28 $682.7B) |
| 8 | FY+1 EPS Growth | +95% [C] (FY26 $4.77 [A] → FY27 $9.31) |
| 9 | 2Y EPS CAGR | +81% [C] (→ FY28 $15.68) |
| 10 | 3Y EPS CAGR | +60% [M] (FY29 = FY28 × 1.25 가정. FY+3 컨센서스는 확인 불가) |
| 11 | NTM P/E | 16.9x (LTM 32.6x, LTM 조정 EPS $7.01 [A]) |
| 12 | FY+1 P/E | 24.6x |
| 13 | FY+2 P/E | 14.6x (FY+3 11.7x [M]) |
| 14 | PEG 1Y | 0.18 |
| 15 | PEG 2Y | 0.21 (PEG 3Y 0.28 [M]) |
| 16 | FY+2 P/E Compression | 55% (**SS급**). EV/NTM Sales 9.3x ÷ 매출 CAGR 78 = 0.12 |
| 17 | ROIC | 92% (TTM) [A]. FY25 191% → FY26 145% → TTM 92%. 하락 원인은 순현금·재고·전략투자로 투하자본이 커진 것이며, WACC 대비 스프레드는 80%p 이상이다 |
| 18 | RONIC | 68% [M] (FY25 → TTM, ΔEBIT/Δ투하자본) |
| 19 | FCF Margin | 41.9% (TTM) [A]. FCF FY27E $194B [C] |
| 20 | Net Debt/EBITDA | -0.12x (순현금 $23.6B) [A] |
| 21 | 최근 1개월 Revision | FY27 EPS +0.2%, FY28 EPS +2.5% [C]. 매출·EBITDA·FCF Revision은 확인 불가 |
| 22 | 최근 3개월 Revision | FY27 +4.1%, **FY28 +23.4%** [C]. 30일간 상향 42건, 하향 0건 |
| 23 | 가장 중요한 Catalyst | 11월 중순 Q3 FY27 실적과 FY28 초기 가이던스. Rubin 램프 속도 |
| 24 | 가장 중요한 Risk | 하이퍼스케일러 Capex 소화(2027~28), 고객 집중, AI 고객사 지분투자를 통한 순환 수요 |
| 25 | 시장이 놓치고 있는 것 | FY28 EPS가 주가보다 빨리 올라 멀티플이 압축됐다. 시장은 FY28을 피크로 가정하지만 경영진 가이던스와 공급 병목(CoWoS·HBM)은 2028년 이후 성장 지속을 시사한다 |
| 26 | 현재 주가가 요구하는 성장 | 5년 EPS CAGR **8.7%** [I] |
| 27 | Consensus가 예상하는 성장 | FY27 +95%, FY28 +68.5% [C], 5Y 경로 36.6% [M] |
| 28 | Expectation Gap | **+27.9%p**, "지나치게 낮음" |
| 29 | 12개월 EPS × P/E 예상가격 | $309 = 12M 후 NTM EPS $18.27 [M] × 16.9x |
| 30 | Potential Upside | +35% (멀티플 불변). 컨센서스 목표가 $327.7(+43%) [C] |
| 31 | Bear Downside | -19% (Bear $185) / Stress -45% ($126) [M] |
| 32 | Risk/Reward | 1.8 : 1 (Base/Bear) |
| 33 | 총점 | **94 (S+)** |
| 34 | 투자 유형 | High-Growth at Fair Price + Earnings Revision Play. **★★ Exceptional Growth-Adjusted Candidate** |

### ② Celestica (CLS)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Celestica Inc. / CLS (NYSE·TSX) |
| 2 | 현재가 | $356.53 |
| 3 | 시가총액 | $45.0B (8월 증자 후) |
| 4 | 사업 유형 | AI/클라우드 인프라 ODM·EMS(스위치, 랙 통합, 커스텀 서버) |
| 5 | 현재 핵심 사업 변화 | 2026 매출 $20.5B, EPS $11.30으로 상향 [G]. **2027 매출성장이 65%보다 가속, EPS는 그보다 더 빠르게 성장** [G]. OpenAI 랙, AMD Helios, 1.6T 프로그램 10개 |
| 6 | NTM Revenue Growth | +102% [C] (NTM $31.5B vs LTM $15.6B) |
| 7 | 2Y Revenue CAGR | +69% [C] (2025 $12.39B → 2027 $35.19B) |
| 8 | FY+1 EPS Growth | +85% [C] (2025 $6.05 [A] → 2026 $11.20) |
| 9 | 2Y EPS CAGR | +79% [C] (→ 2027 $19.36) |
| 10 | 3Y EPS CAGR | +63% [M] (2028 = 2027 × 1.36) |
| 11 | NTM P/E | 20.6x (LTM 43.6x) |
| 12 | FY+1 P/E | 31.8x |
| 13 | FY+2 P/E | 18.4x (FY+3 13.5x [M]) |
| 14 | PEG 1Y | 0.24 |
| 15 | PEG 2Y | 0.26 |
| 16 | FY+2 P/E Compression | 58% (**SS급**). EV/NTM Sales 1.3x |
| 17 | ROIC | 42% (TTM) [A]. 2023 13% → 2024 22% → 2025 37% → TTM 42%로 상승 |
| 18 | RONIC | 179% [M] |
| 19 | FCF Margin | 3.3% (TTM) [A]. 2026E FCF $240M [C]로 Capex와 운전자본 부담이 크다 |
| 20 | Net Debt/EBITDA | 0.28x(6월 말) [A]. 8월 $3B 증자 후 순현금 전환 추정 [M] |
| 21 | 최근 1개월 Revision | FY26 -0.2%, **FY27 +30.2%** [C] |
| 22 | 최근 3개월 Revision | FY26 +8.8%, FY27 +33.8% [C] (FY27 추정 애널리스트 9명) |
| 23 | 가장 중요한 Catalyst | **10/27 Q3 실적과 Investor Day**(2027~2028 중기 목표) |
| 24 | 가장 중요한 Risk | 저마진(OPM 약 10%) 구조에서 Capex·운전자본 급증에 따른 FCF 희석, 반복 증자 가능성, 고객 집중 |
| 25 | 시장이 놓치고 있는 것 | 가이던스만으로 2027 EPS $18.6 이상이 확정적이지만 주가는 3개월 +4%로 반응이 미미하다. ROIC가 오르는 성장이다 |
| 26 | 현재 주가가 요구하는 성장 | 5년 EPS CAGR 13.0% [I] |
| 27 | Consensus가 예상하는 성장 | 2026 +85%, 2027 +73% [C], 5Y 경로 38.5% [M] |
| 28 | Expectation Gap | **+25.5%p**, "지나치게 낮음" |
| 29 | 12개월 EPS × P/E 예상가격 | $508 [M] |
| 30 | Potential Upside | +42%. 컨센서스 목표가 $471(+32%) [C] |
| 31 | Bear Downside | -15% ($305) / Stress -48% ($185) [M] |
| 32 | Risk/Reward | 2.8 : 1 |
| 33 | 총점 | **85.5 (S)** |
| 34 | 투자 유형 | Earnings Revision Play / Growth Inflection. **★ Alpha Candidate** |

### ③ Broadcom (AVGO)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Broadcom Inc. / AVGO (NASDAQ) |
| 2 | 현재가 | $349.57 |
| 3 | 시가총액 | $1.67T |
| 4 | 사업 유형 | 커스텀 AI 가속기(XPU)·AI 네트워킹 반도체 + 인프라 소프트웨어(VMware) |
| 5 | 현재 핵심 사업 변화 | Q3 FY26 AI 매출 $16.7B(+221%) [A]. Q4 AI $21.7B(+236%) [G]. **AI 매출 FY26 $58B → FY27 $115B → FY28 $230B** [G] |
| 6 | NTM Revenue Growth | +88% [C] (NTM $167B vs LTM $89B) |
| 7 | 2Y Revenue CAGR | +65% [C] (FY25 $63.9B → FY27 $173.5B) |
| 8 | FY+1 EPS Growth | +71% [C] (FY25 $6.82 [A] → FY26 $11.66) |
| 9 | 2Y EPS CAGR | +69% [C] (→ FY27 $19.38) |
| 10 | 3Y EPS CAGR | +58% [M] (FY28 = FY27 × 1.40. AI 매출 2배 가이던스에 랙 믹스로 인한 마진 희석을 반영한 보수적 가정) |
| 11 | NTM P/E | 18.7x (LTM 35.8x) |
| 12 | FY+1 P/E | 30.0x (FY26은 10/31 종료로 1개월 남음) |
| 13 | FY+2 P/E | 18.0x (FY+3 12.9x [M]) |
| 14 | PEG 1Y | 0.26 |
| 15 | PEG 2Y | 0.27 |
| 16 | FY+2 P/E Compression | 50% (**S급**) |
| 17 | ROIC | 31% (TTM) [A]. FY24 11% → FY25 20% → TTM 31%. VMware 인수 후 정상화 중 |
| 18 | RONIC | n.m. [M]. 2년간 투하자본은 거의 그대로인데 EBIT이 +$27.7B 늘어 사실상 매우 높다 |
| 19 | FCF Margin | 44.2% (TTM) [A]. FY26E FCF $49B [C] |
| 20 | Net Debt/EBITDA | 0.68x (순부채 $35.4B) [A] |
| 21 | 최근 1개월 Revision | FY26 +0.3%, FY27 -1.0% [C] |
| 22 | 최근 3개월 Revision | FY26 +0.3%, FY27 -0.4% [C]. Revision 상태 3(안정) |
| 23 | 가장 중요한 Catalyst | 12월 Q4 실적과 FY27 가이던스. FY28 $230B 경로가 컨센서스에 반영되는 과정 |
| 24 | 가장 중요한 Risk | 소수 하이퍼스케일러·AI 랩 집중, 랙/시스템 매출 확대에 따른 GM 하락, 고객 자체설계·파트너 교체 |
| 25 | 시장이 놓치고 있는 것 | FY+3(FY28) 이익이 컨센서스 창 밖에 있다. 가이던스대로라면 FY28 P/E 12~13배다 |
| 26 | 현재 주가가 요구하는 성장 | 5년 EPS CAGR 10.8% [I] |
| 27 | Consensus가 예상하는 성장 | FY26 +71%, FY27 +66% [C], 5Y 경로 35.6% [M] |
| 28 | Expectation Gap | **+24.7%p**, "지나치게 낮음" |
| 29 | 12개월 EPS × P/E 예상가격 | $494 [M] (FY28 가정에 크게 의존) |
| 30 | Potential Upside | +41%. 컨센서스 목표가 $531.9(+52%) [C] |
| 31 | Bear Downside | -15% ($296) / Stress -50% ($174) [M] |
| 32 | Risk/Reward | 2.7 : 1 |
| 33 | 총점 | **85 (S)** |
| 34 | 투자 유형 | High-Growth at Fair Price. Alpha 근접(Revision 양수 조건 미충족) |

### ④ TSMC (TSM)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Taiwan Semiconductor Manufacturing / TSM (NYSE ADR, 1 ADR = 5주) |
| 2 | 현재가 | $452.88 |
| 3 | 시가총액 | $2.35T |
| 4 | 사업 유형 | 파운드리(선단 로직·첨단 패키징 CoWoS) |
| 5 | 현재 핵심 사업 변화 | 2026 매출성장을 "40%대 초반(USD)"으로 상향 [G]. Q2 매출 $40.2B, GM 67.7%, HPC 비중 66% [A]. Capex $60~64B [G]. 7월 매출 +44.7% [A] |
| 6 | NTM Revenue Growth | +54% [C] (TWD 기준, NTM vs LTM) |
| 7 | 2Y Revenue CAGR | +39% [C] (2025 NT$3.81T → 2027 NT$7.32T) |
| 8 | FY+1 EPS Growth | +59% [C] (2025 $10.65/ADR → 2026 $16.93) |
| 9 | 2Y EPS CAGR | +43% [C] (→ 2027 $21.93) |
| 10 | 3Y EPS CAGR | +33% [M] (2028 = 2027 × 1.15) |
| 11 | NTM P/E | 21.9x (LTM 32.7x) |
| 12 | FY+1 P/E | 26.7x |
| 13 | FY+2 P/E | 20.7x (FY+3 18.0x [M]) |
| 14 | PEG 1Y | 0.37 |
| 15 | PEG 2Y | 0.50 |
| 16 | FY+2 P/E Compression | 37% (**A급**) |
| 17 | ROIC | 54% (TTM) [A]. 2023 32% → 2024 38% → 2025 51% → TTM 54% |
| 18 | RONIC | 99% [M] |
| 19 | FCF Margin | 25.8% (TTM) [A]. Capex/매출 34%에도 FCF는 증가 |
| 20 | Net Debt/EBITDA | -0.77x (순현금) [A] |
| 21 | 최근 1개월 Revision | 2026 +0.2%, 2027 +0.7% [C] |
| 22 | 최근 3개월 Revision | 2026 +7.4%, **2027 +11.5%** [C] |
| 23 | 가장 중요한 Catalyst | 10월 중순 Q3 실적과 2027 성장·가격 인상 가이던스 |
| 24 | 가장 중요한 Risk | 대만 지정학, 미국 관세/232조, 해외 팹 마진 희석 |
| 25 | 시장이 놓치고 있는 것 | ROIC가 오르면서 Capex가 늘어나는 드문 구조다. 독점적 선단 공정의 가격결정력이 2027~28 이익 지속기간을 늘린다 |
| 26 | 현재 주가가 요구하는 성장 | 5년 EPS CAGR 14.4% [I] |
| 27 | Consensus가 예상하는 성장 | 2026 +59%, 2027 +30% [C], 5Y 경로 18.5% [M] |
| 28 | Expectation Gap | +4.1%p, "적절 ~ 실적이 주가를 따라잡는 중" |
| 29 | 12개월 EPS × P/E 예상가격 | $534 [M] |
| 30 | Potential Upside | +18%. 컨센서스 목표가 $552(+22%) [C] |
| 31 | Bear Downside | -29% ($320) / Stress -34% ($297) [M] |
| 32 | Risk/Reward | 0.6 : 1. 기대수익은 가장 낮지만 품질과 재무 안정성이 가장 높은 **포트폴리오 앵커** |
| 33 | 총점 | **84 (A+)** |
| 34 | 투자 유형 | Quality Compounder / GARP |

### ⑤ Credo Technology (CRDO)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Credo Technology Group / CRDO (NASDAQ) |
| 2 | 현재가 | $192.67 |
| 3 | 시가총액 | $36.2B |
| 4 | 사업 유형 | AI 데이터센터 고속 연결(AEC, SerDes/DSP, 광학) 팹리스 |
| 5 | 현재 핵심 사업 변화 | Q1 FY27 매출 $479M(+115%) [A]. FY27 성장 85% 초과, 광학 $600M 초과 [G]. 신규 10% 고객 추가 [A] |
| 6 | NTM Revenue Growth | +93% [C] (NTM $3.08B vs LTM $1.59B) |
| 7 | 2Y Revenue CAGR | +70% [C] (FY26 $1.34B → FY28 $3.88B) |
| 8 | FY+1 EPS Growth | +82% [C] (FY26 $3.46 [A] → FY27 $6.31) |
| 9 | 2Y EPS CAGR | +67% [C] (→ FY28 $9.70) |
| 10 | 3Y EPS CAGR | +53% [M] (FY29 = FY28 × 1.27) |
| 11 | NTM P/E | 25.0x (LTM 47.0x) |
| 12 | FY+1 P/E | 30.6x |
| 13 | FY+2 P/E | 19.9x (FY+3 15.6x [M]) |
| 14 | PEG 1Y | 0.30 |
| 15 | PEG 2Y | 0.37 |
| 16 | FY+2 P/E Compression | 58% (**SS급**) |
| 17 | ROIC | 38% (TTM) [A]. FY26 97%에서 하락했는데, 재고와 생산능력 투자가 원인이다 |
| 18 | RONIC | 42% [M] |
| 19 | FCF Margin | 27.6% (TTM) [A]. 단 Q1 FCF $83M vs 조정 순이익 $236M |
| 20 | Net Debt/EBITDA | -1.36x (순현금 $0.74B) [A] |
| 21 | 최근 1개월 Revision | FY27 +2.2%, FY28 +6.2% [C] |
| 22 | 최근 3개월 Revision | FY27 +3.0%, **FY28 +8.9%** [C]. 같은 기간 주가 -22% |
| 23 | 가장 중요한 Catalyst | 12월 초 Q2 FY27 실적(가이던스 $525~535M)과 하반기 가속 확인 |
| 24 | 가장 중요한 Risk | 상위 4개 고객 84% 집중, GM 하락 추세(GAAP 64.5%), SBC/매출 14.8% |
| 25 | 시장이 놓치고 있는 것 | 이익은 올라가는데 주가만 내린 **Revision 괴리 최대** 종목이다. FY27 가이던스의 절반은 이미 수주로 확보됐다 |
| 26 | 현재 주가가 요구하는 성장 | 5년 EPS CAGR 17.4% [I] |
| 27 | Consensus가 예상하는 성장 | FY27 +82%, FY28 +54% [C], 5Y 경로 29.9% [M] |
| 28 | Expectation Gap | +12.5%p, "실적이 주가를 따라잡는 중" |
| 29 | 12개월 EPS × P/E 예상가격 | $269 [M] |
| 30 | Potential Upside | +40%. 컨센서스 목표가 $280(+45%) [C] |
| 31 | Bear Downside | -16% ($161) / Stress -35% ($126) [M] |
| 32 | Risk/Reward | 2.5 : 1 |
| 33 | 총점 | **84 (A+)** |
| 34 | 투자 유형 | High-Growth at Fair Price / Earnings Revision Play. **★ Alpha Candidate** |

---

## 6. 최종 Ranking (16단계)

| 순위 | 기업 | 총점 | Growth (20) | Valuation (20) | Revision (15) | Quality (15) | Expectation Gap (10) | Catalyst (10) | Risk/BS (10) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NVIDIA (NVDA) | **94** (S+) | 18 | 19 | 15 | 15 | 10 | 9 | 8 |
| 2 | Celestica (CLS) | **85.5** (S) | 20 | 18 | 15 | 7.5 | 10 | 9 | 6 |
| 3 | Broadcom (AVGO) | **85** (S) | 20 | 17 | 9 | 14 | 10 | 9 | 6 |
| 4 | TSMC (TSM) | **84** (A+) | 20 | 14 | 15 | 14 | 5 | 8 | 8 |
| 5 | Credo (CRDO) | **84** (A+) | 15 | 18 | 15 | 13 | 8 | 8 | 7 |
| 6 | AMD (AMD) | **84** (A+) | 20 | 15 | 15 | 8 | 10 | 9 | 7 |
| 7 | 에이피알 (278470 KS) | **82.5** (A+) | 15.5 | 18 | 15 | 11 | 8 | 7 | 8 |
| 8 | Vertiv (VRT) | **80.5** (A+) | 20 | 13 | 13.5 | 14 | 5 | 8 | 7 |
| 9 | Applied Materials (AMAT) | **80.0** (A+) | 18.5 | 13 | 15 | 14 | 6.5 | 6 | 7 |
| 10 | Reddit (RDDT) | **79.5** (A) | 18 | 15 | 15 | 11 | 6.5 | 7 | 7 |
| 11 | ASML (ASML) | **79.5** (A) | 18.5 | 11.5 | 15 | 15 | 3.5 | 7 | 9 |
| 12 | Flex (FLEX) | **78.0** (A) | 18.5 | 17 | 13.5 | 8.5 | 8 | 8 | 4.5 |
| 13 | Onto Innovation (ONTO) | **78.0** (A) | 18 | 16 | 15 | 9.5 | 6.5 | 6 | 7 |
| 14 | Lumentum (LITE) | **76.5** (A) | 17 | 16 | 15 | 7 | 6.5 | 8 | 7 |
| 15 | Nu Holdings (NU) | **76.0** (A) | 18 | 16.5 | 13.5 | 7 | 8 | 6 | 7 |
| 16 | Comfort Systems (FIX) | **75.5** (A) | 17 | 11.5 | 15 | 14 | 2 | 7 | 9 |
| 17 | Toast (TOST) | **74.5** (B+) | 14.5 | 13.5 | 12 | 13 | 6.5 | 6 | 9 |
| 18 | Rorze (6323 JP) | **74.5** (B+) | 14 | 18 | 15 | 7 | 6.5 | 6 | 8 |
| 19 | Semtech (SMTC) | **74.0** (B+) | 18 | 16 | 15 | 6.5 | 8 | 7 | 3.5 |
| 20 | HD현대중공업 (329180 KS) | **74.0** (B+) | 15.5 | 16.5 | 13.5 | 9 | 6.5 | 6 | 7 |

**"왜 지금 조사해야 하는가?"**
1. **NVDA**: FY28 EPS가 90일 새 23% 올랐는데 주가는 덜 올라, 세계 최대 이익성장 기업이 FY+2 14.6배에 거래된다.
2. **CLS**: 경영진이 "2027 성장 가속, EPS는 더 빠르게"를 명시했고, 10/27 Investor Day가 추정치 재상향의 방아쇠다.
3. **AVGO**: FY28 AI 매출 $230B 가이던스가 컨센서스 창(FY+2) 밖에 있어 FY+3 P/E가 약 13배다.
4. **TSM**: ROIC 54%, 순현금 상태에서 EPS CAGR 43%인데 요구성장률은 14%에 불과한 최고 품질의 앵커다.
5. **CRDO**: 주가 -22%와 FY+2 EPS +9%로 괴리가 가장 크고, FY+2 P/E 20배에 성장 85%다.
6. **AMD**: 2027년 EPS 2배(MI450) 전환점이다. LTM 105배가 FY+2 39배로 압축된다.
7. **에이피알**: 매출과 영업이익이 동시에 +134%인 인플렉션이 FY+2 17배, 순현금으로 거래되는 비AI 성장주다.
8. **VRT**: ROIC와 FCF가 함께 개선되는 AI 전력·냉각 Compounder다. 다만 밸류에이션이 성장 상당 부분을 이미 반영했다.
9. **AMAT**: 3개월 -30%인데 FY+2 EPS는 +12.5%로 WFE 사이클 속 Revision 역행 기회다.
10. **RDDT**: 가이던스 상회에도 트래픽 우려 하나로 -18%가 됐고, PEG 0.34다.
11. **ASML**: 가이던스를 두 차례 상향했고 FY+2 EPS +23%지만, 기대가 이미 선반영돼 가격 규율이 필요하다.
12. **FLEX**: CPI 스핀오프(1Q27)라는 구조적 이벤트와 FY+2 16배의 조합이다.
13. **ONTO**: 수주잔고가 처음 $1B를 넘었고 첨단 패키징 전망을 80%로 상향했는데 주가는 -18%다.
14. **LITE**: CPO 수주로 FY+2 EPS가 +23% 올랐다. 다만 급등과 전환사채 희석 점검이 필요하다.
15. **NU**: FY+2 11배, EPS CAGR 37%인 ★★ 수치다. Monzo 인수 조건이 확정되는 시점이 판단 포인트다.
16. **FIX**: ROIC 77%, FCF 4배의 최상급 품질이지만 Gap이 음수라 가격을 기다려야 한다.
17. **TOST**: 순현금, ROIC 고수익의 GARP로, 가이던스 상향과 신규 버티컬 확장이 이어지고 있다.
18. **Rorze**: 1Q 수주 +190%, 수주잔고 +128%로 장비 소형주의 강한 Earnings Revision(+29%)이 나왔다.
19. **SMTC**: Q3 가이던스가 컨센서스를 25% 웃돌았다. 다만 희석과 부채를 감안해야 한다.
20. **HD현대중공업**: FY+2 12배, 순현금이지만 FY+2 성장이 7%로 급감속하는 사이클 종목이다.

---

## 7. 최종 판정: Absolute vs Growth-Adjusted vs Market Expectations (17단계)

| 기업 | Absolute Valuation | Growth-Adjusted Valuation | Market Expectations |
|---|---|---|---|
| NVIDIA | 쌈 | 성장 대비 매우 저평가 | 지나치게 낮음 |
| Celestica | 적정 | 성장 대비 매우 저평가 | 지나치게 낮음 |
| Broadcom | 적정 | 성장 대비 매우 저평가 | 지나치게 낮음 |
| TSMC | 적정 | 성장 대비 매력적 | 적절 ~ 실적이 주가를 따라잡는 중 |
| Credo | 적정 | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 |
| AMD | 비쌈 | 성장 대비 매력적 | 지나치게 낮음 (단 실행 리스크 큼) |
| 에이피알 | 적정 | 성장 대비 매우 저평가 | 실적이 주가를 따라잡는 중 |
| Vertiv | 비쌈 | 성장 대비 적정 | 적절 |
| Applied Materials | 비쌈 | 성장 대비 적정 | 적절 |
| Reddit | 적정 | 성장 대비 매력적 | 적절 |
| ASML | 비쌈 | 성장 대비 적정 | 상당히 선반영 |
| Flex | 적정 | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 |
| Onto Innovation | 비쌈 | 성장 대비 매력적 | 적절 |
| Lumentum | 비쌈 | 성장 대비 매력적 | 적절 |
| Nu Holdings | 쌈 | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 |
| Comfort Systems | 비쌈 | 성장 대비 적정 | 상당히 선반영 |
| Toast | 적정 | 성장 대비 적정 | 적절 |
| Rorze | 적정 | 성장 대비 매력적 | 적절 |
| Semtech | 비쌈 | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 |
| HD현대중공업 | 쌈 | 성장 대비 매력적(사이클 할인 필요) | 적절 |

판정 기준: Absolute는 NTM/FY+2 P/E를 시장 평균(약 20~22배)과 비교했다. Growth-Adjusted는 PEG 2Y 기준으로 <0.3 매우 저평가, 0.3~0.55 매력적, 0.55~1.0 적정, 1.0~1.5 비쌈, >1.5 극단적으로 비쌈이다. Market Expectations는 Gap 기준으로 >20%p 지나치게 낮음, 10~20%p 따라잡는 중, 0~10%p 적절, <0 상당히 선반영이다.

---

## 8. Alpha 표시 (14단계)

| 표시 | 종목 | 비고 |
|---|---|---|
| **★★ Exceptional Growth-Adjusted Candidate** (EPS CAGR >30% + FY+2 P/E <15x + Revision 양수) | **NVIDIA**, Nu Holdings*, HD현대중공업** | *Monzo M&A 리스크 **조선 사이클 할인. 메모리 7종도 수치상 충족하지만 Cyclical Peak로 제외 |
| **★ Alpha Candidate** (Rev >20%, EPS CAGR >25%, FY+2 P/E <20x, PEG <0.8, ROIC >12%, Revision+, Compression >30%, BS 양호) | NVIDIA, Celestica, Credo, Flex, 에이피알(ROE 대용), Rorze(ROE 대용) | |
| Alpha 근접(1개 조건 미충족) | Broadcom(Revision 중립), TSMC(FY+2 20.7x), Reddit(FY+2 20.2x), Toast(매출성장 19.6%) | |

---

## 9. Deep Dive 후보 (18단계)

**★★★ 즉시 정밀분석 추천**
1. NVIDIA (NVDA)
2. Celestica (CLS)
3. Broadcom (AVGO)

**★★ 높은 관심**

4. TSMC (TSM)
5. Credo Technology (CRDO)
6. AMD (AMD)
7. 에이피알 (278470 KS)

**★ Watchlist**

8. Vertiv (VRT)
9. Applied Materials (AMAT)
10. Reddit (RDDT)

**"왜 이 기업을 지금 내가 사용하는 전체 기업가치평가 프롬프트에 넣어야 하는가?"**

- **NVIDIA**: 시가총액 $5.5T 기업이 FY+2 P/E 14.6배, PEG 0.21이라는 것 자체가 시장이 FY28 이후 성장 지속기간을 거의 0으로 보고 있다는 뜻이다. Forward DCF, Reverse DCF, ROIC/RONIC로 "FY28 이후 성장 곡선"과 "Capex 사이클 정상화 EPS"를 명시적으로 모델링해야만 진짜 저평가인지 Peak 이익인지 판별할 수 있다. 90일간 FY28 EPS +23%라는 Revision 강도는 정상화 선행실적의 기준점을 계속 올리고 있다. Earnings Growth에 따른 Valuation Compression 분석에 가장 이상적인 표본이다.
- **Celestica**: 경영진이 2027년 성장 가속과 EPS 레버리지를 명시해 가이던스 기반 선행실적 모델링이 가능하다. 다만 저마진 ODM, 증자, FCF 3%라는 약점이 있다. 그래서 ROIC/RONIC와 FCF 전환율, 희석 후 주당가치를 따지는 정밀 프레임워크의 변별력이 가장 크게 작동한다. 10/27 Investor Day 전에 Base/Bear 모델을 세워 두면 이벤트 후 Revision을 즉시 가치로 환산할 수 있다.
- **Broadcom**: FY28 AI 매출 $230B라는 명시적 가이던스가 컨센서스 창 밖에 있는 드문 사례다. FY+3까지 확장한 Forward DCF와 Reverse DCF가 가장 큰 Expectation Gap을 드러낼 수 있다. 커스텀 XPU의 고객 집중과 랙 믹스에 따른 마진 희석은 상대가치와 시나리오 분석으로 정량화해야 한다. VMware 이후 ROIC 정상화(11% → 31%) 경로까지 포함하면 Quality와 Growth를 동시에 검증할 수 있다.

---

## 10. 최종 질문 8가지에 대한 답

1. **지금 시장에서 가장 Growth-Adjusted Valuation이 좋은 기업은?**
   **NVIDIA**(PEG 2Y 0.21, FY+2 14.6x, EPS CAGR 81%)다. 다음은 Celestica(0.26), Broadcom(0.27), 에이피알(0.27) 순이다. 메모리(MU·SK하이닉스 PEG 0.02)는 수치상 더 낮지만 Peak EPS 왜곡 가능성 때문에 제외했다.

2. **현재 P/E는 높지만 향후 EPS 성장 때문에 실제로는 싼 기업은?**
   **AMD**(LTM 105x → FY+2 39x, PEG 0.48), **Lumentum**(110x → 26.5x, PEG 0.37), **Semtech**(82x → 30x), **Credo**(47x → 20x)다. 품질까지 감안하면 Credo, 순수 전환 폭으로 보면 AMD가 가장 극적이다.

3. **현재 주가가 유지되기만 해도 FY+2 P/E가 가장 빠르게 낮아지는 기업은?**
   비사이클 기준으로 **Lumentum 76%**, AMD 63%, Semtech 63%, 에이피알 64%(FY0 대비), Celestica·Credo 58%, Rorze 56%, NVIDIA 55% 순이다. 사이클 포함 시 SanDisk 73%, MU 72%, Seagate 72%지만 Peak 검증 대상이다.

4. **최근 Earnings Revision이 가장 강하면서 아직 주가가 충분히 반응하지 않은 기업은?**
   **Credo**(FY+2 EPS 90일 +8.9%, 주가 3개월 -22%)와 **Celestica**(FY+2 +33.8%, 주가 +4%)다. 장비주에서는 AMAT(+12.5% vs -30%), Onto(+17.5% vs -18%), Rorze(+29% vs -20%)가 뒤를 잇는다. NVIDIA도 +23.4% vs +17%로 "EPS Revision > 주가 상승" 조건을 충족한다.

5. **EPS뿐 아니라 FCF와 ROIC까지 함께 개선되는 기업은?**
   **TSMC**(ROIC 32% → 54%, FCF 증가), **Comfort Systems**(ROIC 26% → 77%, FCF $545M → $2.16B), **Vertiv**(ROIC 18% → 38%, FCF $0.77B → $2.93B), **NVIDIA**(FCF $96.7B → FY27E $194B, ROIC 90%대), **Toast**(FCF $93M → $576M TTM)다. Celestica는 ROIC가 오르지만 FCF가 얇아 제외했다.

6. **시장이 향후 3~5년 성장 지속기간을 가장 과소평가하는 기업은?**
   **Broadcom**(FY28 AI 매출 $230B 가이던스, 요구성장률 10.8%)과 **NVIDIA**(요구성장률 8.7%, 경영진은 FY28 +70% 언급)다. 구조적 독점 관점에서는 TSMC(요구 14.4% vs 2Y 컨센서스 43%)도 해당한다.

7. **멀티플 상승 없이 12~24개월 15% 이상 기대수익이 가능한 기업은?**
   12개월 Base [M] 기준으로 AMD +60%, Lumentum +49%, Celestica +42%, Semtech +42%, Broadcom +41%, Credo +40%, NVIDIA +35%, Flex +35%, Onto +26%, AMAT +24%, 에이피알 +23%, Vertiv +22%, ASML +21%, Reddit +19%, TSMC +18%, Nu +17%, Rorze +17%, Toast +15%다. FY+3는 [M] 가정이다. 24개월로 보면 대부분 +25% 이상이다.

8. **이 모든 조건을 종합했을 때 지금 정밀 기업가치평가를 수행할 가치가 가장 높은 Top 5는?**
   **① NVIDIA ② Celestica ③ Broadcom ④ TSMC ⑤ Credo**

---

## 11. 포트폴리오 관점 경고와 비AI 대안

- **팩터 집중**: Top 10 중 8개, Top 20 중 15개가 AI 인프라 Capex(반도체·광통신·전력/냉각·데이터센터 시공)에 연동된다. 7월 급락(SOX -6%/일)처럼 하이퍼스케일러 Capex 신호 하나에 동시에 흔들린다. 정밀분석 시 공통 Bear 시나리오(2027 Capex 증가율 둔화)를 일관되게 적용해야 한다.
- **즉시 이벤트**: **9/30 MU 실적**(메모리와 HBM 가격, 2027 Capex)이 AI 복합 전체의 단기 방향을 정한다. 이어 CLS 10/27, TSM 10월 중순, NVDA 11월 중순 실적이 추정치 경로를 확인할 이벤트다.
- **비AI 분산 대안(점수순)**: 에이피알(82.5), Reddit(79.5), Nu(76), Toast(74.5), HD현대중공업(74), Eli Lilly(71, FY+2 24.9x, EPS CAGR 40%, ROIC 42%), Expedia(72.5, Buyback 기여).

---

## 12. 데이터 한계 및 "확인 불가" 항목

- **FY+3 컨센서스**: 무료 소스에서 확인 불가. 3Y EPS CAGR, FY+3 P/E, 12M 예상가격은 모두 [M] 가정이다.
- **매출·EBITDA·FCF 컨센서스 Revision(1M/3M)**: 확인 불가. EPS Revision만 Yahoo EPS Trend(7/30/60/90일 전 대비)로 측정했다. 매출 방향성은 가이던스 변화 [G]로 보완했다.
- **EV/EBITDA ÷ EBITDA CAGR, EV/EBIT ÷ EBIT CAGR**: EBITDA/EBIT 컨센서스를 확보하지 못해 산출하지 않았다. EV/NTM Sales ÷ 매출 CAGR로 대체했다(NVDA 0.12, AVGO 0.16, CRDO 0.16, CLS 0.02).
- **RONIC**: 공시된 값이 아니다. StockAnalysis ROIC 정의에서 역산한 투하자본으로 계산한 [M]이며, 투하자본이 감소한 경우 n.m.으로 표시했다.
- **한국·일본 ROIC**: 확인 불가. ROE, 영업이익률, 순현금/EBITDA로 대체했다. 목표주가 컨센서스는 갱신 지연 가능성이 있다.
- **Normalized/Mid-cycle EPS**(메모리): 확인 불가. 정밀분석 단계에서 산출해야 한다.
- FX 환산(2026-09-29): USD/KRW 1,357.36, USD/JPY 157.28, USD/TWD 31.85, EUR/USD 1.136, USD/CNY 6.70, USD/DKK 6.58.

---

## 13. 점수 산식 상세

| 항목 | 배점 | 규칙 |
|---|---|---|
| A. Forward Growth | 20 | FY+1·FY+2 매출성장 평균: >30% 7 / >20% 5.5 / >15% 4 / >10% 2.5 / >5% 1. 2Y EPS CAGR: >35% 7 / >25% 5.5 / >18% 4 / >12% 2.5 / >5% 1. 가속: FY+1 > FY0×1.05이고 FY+2 ≥ FY+1×0.75이면 3, 유지 2, 완만한 감속 1, 급감속 0. EPS CAGR > 매출+3%p면 3, 비슷하면 1.5 |
| B. Growth-Adjusted Valuation | 20 | FY+2 P/E: <12 6 / <15 5 / <20 4 / <25 3 / <30 2 / <40 1. PEG 2Y: <0.5 7 / <0.7 6 / <1.0 4.5 / <1.5 3 / <2.0 1.5. FY+2 Compression: ≥55% 7 / ≥45% 6 / ≥35% 5 / ≥25% 3.5 / ≥15% 2 |
| C. Earnings Revision | 15 | 상태(5 강한 상향 ~ 1 강한 하향) × 3. 가중 Revision(FY+2 90일 60% + FY+1 90일 40%)이 ≥8%이거나 FY+2 30일이 ≥4%면 5, ≥2% 4, ±2% 3, -2~-8% 2, <-8% 1. 상태 4 이상이고 FY+2 EPS 상향 > 3개월 주가상승이면 +1.5 |
| D. Growth Quality | 15 | ROIC: >30% 6 / >20% 5 / >15% 4 / >10% 2.5 / >5% 1. FCF Margin: >25% 5 / >15% 4 / >8% 3 / >3% 1.5 / >0 0.5. 주식수 YoY: ≤0 +2 / <3% +1 / >5% -1. FY+1 영업이익률 확대 +2. 정성 조정(증자, FCF 전환 등) -1~-3 |
| E. Expectation Gap | 10 | 컨센서스 경로 5Y − 요구 CAGR: >20%p 10 / >10 8 / >5 6.5 / >0 5 / >-5 3.5 / >-10 2 / 그 외 1. 사이클 종목 상한 4 |
| F. Catalyst | 10 | 정성 평가. 12~18개월 내 숫자를 움직일 이벤트가 있는지와 가이던스 명시성 |
| G. Balance Sheet/Risk | 10 | 순현금 9 / 순부채/EBITDA <1 8, <2 7, <3 5.5, <4 4, 그 외 2. 고객 집중·희석·지정학 등 -1~-3, 사이클 -3 |

---

## 출처

- 시장 맥락: [Fortune – chip selloff (2026-07-28)](https://fortune.com/2026/07/28/why-are-stocks-down-chips-panic-semiconductors/), [Fortune (2026-07-17)](https://fortune.com/2026/07/17/tech-stocks-global-selloff-as-investors-ai-semiconductor-chips/), [CNBC 9/1 market](https://www.cnbc.com/2026/08/31/stock-market-today-live-updates.html), [Micron earnings preview (Yahoo)](https://finance.yahoo.com/markets/stocks/articles/micron-earnings-preview-analysts-see-022234081.html)
- NVIDIA: [Q2 FY27 8-K](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm), [CNBC – Huang forecasts 70% FY28 growth](https://www.cnbc.com/2026/08/26/nvidia-nvda-earnings-report-q2-2027-live-updates.html)
- Celestica: [Q2 2026 results](https://corporate.celestica.com/news-releases/news-release-details/celestica-announces-second-quarter-2026-financial-results), [Q2 call highlights (Yahoo)](https://finance.yahoo.com/markets/stocks/articles/celestica-inc-cls-q2-2026-190135107.html), [$3B equity offering priced (TipRanks)](https://www.tipranks.com/news/company-announcements/celestica-prices-3-billion-equity-offering-to-fund-growth-in-ai-and-cloud-infrastructure), [Investor Day 10/27](https://www.globenewswire.com/news-release/2026/09/08/3358122/0/en/celestica-to-host-2026-investor-and-analyst-day-on-october-27-2026.html)
- Broadcom: [Q3 FY26 results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial), [AI revenue $115B/$230B (Seeking Alpha)](https://seekingalpha.com/news/4639799-broadcom-forecasts-58b-fiscal-2026-ai-revenue-and-outlines-115b-in-2027-230b-in-2028)
- TSMC: [July revenue (Yahoo)](https://finance.yahoo.com/technology/ai/articles/tsmc-july-2026-revenue-jumps-110802277.html), [CNBC 8/10](https://www.cnbc.com/2026/08/10/tsmc-revenue-surge-ai-chip-big-tech.html)
- Credo: [Q1 FY27 selloff (Tickeron)](https://tickeron.com/blogs/credo-technology-crdo-falls-24-over-30-days-after-strong-earnings-16431/), [Q1 FY27 call (Motley Fool)](https://www.fool.com/earnings/call-transcripts/2026/09/08/credo-crdo-q1-2027-earnings-call-transcript/), [FY27 optical >$600M (Seeking Alpha)](https://seekingalpha.com/news/4639254-credo-targets-more-than-600m-in-fiscal-27-optical-revenue-as-q2-revenue-is-guided-to-525m), [FCF conversion (Yahoo)](https://finance.yahoo.com/markets/stocks/articles/credo-236-million-adjusted-profit-154239820.html)
- AMD: [Q2 2026 results](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results), [CNBC 8/4](https://www.cnbc.com/2026/08/04/amd-earnings-report-q2-2026.html)
- 에이피알: [파이낸셜뉴스 2Q26](https://www.fnnews.com/news/202608051015092608), [EBN](https://www.ebn.co.kr/news/articleView.html?idxno=1719246)
- Vertiv: [Q2 2026 release](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Second-Quarter-2026-with-Diluted-EPS-Growth-of-53-Adjusted-Diluted-EPS-Growth-of-60-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/default.aspx)
- Applied Materials: [Q3 FY26 (TIKR)](https://www.tikr.com/blog/applied-materials-beat-q2-estimates-and-raised-its-2026-outlook-the-stock-dipped-heres-what-investors-should-know), [Investing.com transcript](https://www.investing.com/news/transcripts/earnings-call-transcript-applied-materials-beats-q3-2026-estimates-shares-fall-93CH-4859444)
- Reddit: [Q2 2026 (Yahoo)](https://finance.yahoo.com/markets/stocks/articles/reddit-plunges-21-post-q2-174800672.html), [TIKR](https://www.tikr.com/blog/reddit-rddt-stock-sinks-search-referral-concerns-q2-2026)
- ASML: [Q2 2026 results](https://www.asml.com/en/news/press-releases/2026/q2-2026-financial-results), [Investing.com slides](https://www.investing.com/news/company-news/asml-q2-2026-slides-outlook-raised-on-ai-demand-high-na-milestone-93CH-4792166)
- Flex: [Q1 FY27 results](https://investors.flex.com/news/news-details/2026/FLEX-REPORTS-FIRST-QUARTER-FISCAL-2027-RESULTS/default.aspx), [Axiom spin-off](https://www.prnewswire.com/news-releases/flex-announces-new-company-name-for-the-planned-cloud-and-power-infrastructure-spin-off-and-files-form-10-registration-statement-302878102.html)
- Onto: [Q2 2026 results](https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Reports-2026-Second-Quarter-Results/default.aspx)
- Lumentum: [FQ4 2026 results](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Results/default.aspx)
- Nu: [Q2 2026 results](https://nu.com/en/newsroom/company/nu-holdings-ltd-reports-second-quarter-2026-financial-results), [Monzo talks (TNW)](https://thenextweb.com/news/monzo-nubank-sale-talks)
- Toast: [Q2 2026 call highlights (Yahoo)](https://finance.yahoo.com/markets/stocks/articles/toast-inc-tost-q2-2026-050038112.html)
- Semtech: [Q2 FY27 results](https://www.semtech.com/company/press/semtech-announces-second-quarter-of-fiscal-year-2027-results), [TrendSpider](https://trendspider.com/blog/semtech-stock-q2-earnings-q3-guidance/)
- Rorze: [ENVALITH segments](https://envalith.com/en/companies/6323/segments)
- HubSpot(Value Trap 판단): [Benzinga](https://www.benzinga.com/markets/earnings/26/08/60977923/why-hubspot-shares-are-trading-lower-wednesday-after-q2-results)
- AppLovin(Value Trap 판단): [Yahoo](https://finance.yahoo.com/markets/stocks/articles/applovin-stock-down-54-2026-114303125.html)
- Rheinmetall(탈락 사유): [CNBC 8/6](https://www.cnbc.com/2026/08/06/rheinmetall-stock-earnings-guidance-frigate.html)
- 정량 데이터: Yahoo Finance quoteSummary(earningsTrend, financialData, price), StockAnalysis.com(statistics, forecast, financials/ratios; S&P Global Market Intelligence)

*본 자료는 아이디어 발굴용 스크리닝이며 투자 권유가 아니다. [M]/[I] 수치는 명시된 가정에 따른 모델값이다.*
