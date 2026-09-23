# 성장조정 밸류에이션 스크리닝 — Forward Earnings Compression 후보 발굴

- **검색 기준일:** 2026-09-23 (주가는 별도 표기 없으면 2026-09-21~22 종가/호가 기준)
- **작성 관점:** 글로벌 롱온리 / 헤지펀드 / 성장주 펀드 아이디어 발굴 (정밀 가치평가 투입 전 1차 선별)
- **표기 규칙:** [A] Actual · [G] Guidance · [C] Consensus · [M] Model(본 분석 산출) · [I] Implied(주가 역산)

> **데이터 한계 (반드시 읽을 것)**
> 이번 세션 환경에서는 Bloomberg/FactSet/Yahoo/StockAnalysis 등 데이터 사이트 직접 접속이 네트워크 정책으로 차단됐다.
> 모든 수치는 웹 검색으로 확인한 공개 자료(회사 IR·보도자료·10-Q, 언론, 컨센서스 집계 페이지 요약)에서 가져왔고,
> 컨센서스는 제공처·일자마다 다를 수 있다. 확인하지 못한 값은 "확인 불가"로 적었고, 직접 계산한 값은 [M]으로 구분했다.
> 정밀 가치평가 단계에서는 반드시 원자료(터미널 컨센서스, 10-Q/10-K)로 재검증해야 한다.

---

## 0. 요약 (Executive Summary)

1. **2026년 9월 시장 환경:** S&P 500 Q3'26 예상 EPS 성장률 +28.7~28.9%, Forward P/E 19.1x(5년 평균 19.8x 하회)[C, FactSet 9월 초].
   이익이 주가보다 빨리 늘면서 **지수 전체가 "Valuation Compression" 국면**에 있다. 상향의 진원지는 AI 인프라(GPU·ASIC·메모리·장비)다.
2. **가장 강한 성장조정 밸류에이션은 여전히 AI 반도체 대형주에 있다.** 주가가 멈춰 있어도 FY+2 P/E가 절반 이하로 떨어지는 종목이 NVDA·AVGO다.
3. **메모리(MU·SK하이닉스·삼성전자)는 P/E 압축이 가장 크지만(4~7x), 시장이 이익 급감을 이미 가격에 넣은 경기민감주다.**
   Cyclical Peak Trap 검증(정상화 EPS)을 거치기 전에는 PEG 신뢰도를 낮게 보고 점수에 상한을 뒀다.
4. **AI 외 분산 후보:** NU(2027 P/E 12x, EPS 2Y CAGR ~41%, ROE 33%)와 APP(2027 P/E 16x, ROIC 130%+)가 성장조정 기준으로 가장 매력적이다.
   단 APP는 최근 추정치가 하향 중이다.
5. **최종 Top 5 (정밀분석 우선순위):** ① NVDA ② AVGO ③ NU ④ TSM ⑤ MU

---

## 1. 스크리닝 과정 요약

| 단계 | 내용 | 결과 |
|---|---|---|
| Universe | 미국 + 한국·일본·유럽 대형 성장주, AI 인프라·플랫폼·핀테크·헬스케어·산업재 약 45개 | 데이터 확보 30여 개 |
| 1단계 Growth | Rev > 15%, EPS > 15%, 가속 여부 | 26개 통과 |
| 2~3단계 Compression / PEG | FY+2 P/E 압축률, PEG 1Y/2Y | 20개 선별 (Top 20) |
| 4~11단계 Quality·Revision·Risk·False Positive | ROIC/FCF, 추정치 변화, 경기 Peak·일회성 이익 필터 | 10개 (Top 10) |
| 13~17단계 점수·최종판정 | 100점 척도 + 3축 판정 | 5개 (Top 5) |

### 1-1. False Positive로 제거·강등한 종목

| 종목 | 사유 (필터 유형) |
|---|---|
| Alphabet (GOOGL) | Q2'26 순이익 $112.1B(+298%), EPS $9.11[A]가 대규모 투자평가이익으로 부풀려짐 → **One-off**. 2026 capex $195~205B로 상향, 2027 "대폭 증가" → FCF 악화 (**Low-Quality Growth** 경계). Cloud +82%·수주잔고 $514B는 매력적이나 정상화 EPS 재산정 필요 |
| Amazon (AMZN) | 2026 EPS 컨센서스 $8.66→$12.57(90일)[C] 상향 대부분이 투자평가이익 → **One-off**. 정상화 EPS 기준 P/E 약 28x, capex $220B |
| Astera Labs (ALAB) | Forward P/E 64~120x → **Overvalued Growth** |
| Lumentum (LITE) | $858, FQ1 EPS 가이던스 연율 약 $17 → 약 50x |
| Arista (ANET) | 2026 매출 +40%[G]이나 EPS 성장 약 20%[C] → PEG > 2 |
| GE Vernova (GEV) | 수주잔고 $176B는 강력하나 P/E가 성장 대비 높음, 고점 대비 −22% |
| MercadoLibre (MELI) | 매출 +50%이나 순이익률 4.6%, EPS 역성장($9.19 vs $10.31)[A] → 마진 변곡 확인 전까지 보류 |
| Sea Ltd (SE) | 매출 +48%이나 순이익 +10.6%, EPS 미스[A] → 이익 레버리지 미확인 |
| Robinhood (HOOD) | 2026 EPS 성장 둔화(가상자산 매출 감소)[C] |
| SanDisk (SNDK) | FQ1 EPS 가이던스 $44~46(연율 약 10x)[G]이나 연간 컨센서스 확인 불가, 9월 NAND 가격 모멘텀 둔화 → Top 20 경계선 탈락 |
| HD현대일렉트릭·효성중공업·LS ELECTRIC | 2026 영업이익 +25~47%[C]이나 P/E 부담, 컨센서스 PER 확인 불가 |
| Credo·Advantest·Kioxia | 성장·추정치 상향은 매우 강하나 현재 주가·연간 컨센서스 확인 불가 → Watchlist 외부 보관 |

---

## 2. Top 20

(FY+1 = 진행 중인 회계연도, FY+2 = 다음 회계연도. NVDA FY+1 = FY27(2027년 1월 종료), AVGO FY+1 = FY26(2026년 11월 종료), MU/LRCX/WDC/STX FY+1 = FY27)

| 순위 | 기업 | 티커 | 유형 | Revenue Growth | EPS CAGR | FY+1 P/E | FY+2 P/E | PEG | ROIC | Revision | 점수 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NVIDIA | NVDA | High-Growth at Fair Price ★★ | FY27 ~+87%[M], FY28 +70%[G] | 81% (FY26→28)[C] | 24.4x | 14.5x | 0.21 | 확인 불가 (WACC의 수배[M]) | 5 | **88** |
| 2 | Broadcom | AVGO | High-Growth at Fair Price ★ | FY26 ~+65%[M], FY27 ~+50%[M] | 69% (FY25→27)[C] | 30.7x | 18.5x (FY28 13.8x) | 0.28 | ~25~40%[M] | 4 | **86** |
| 3 | Nu Holdings | NU | GARP ★★ | 총수익 +39% (Q2)[A] | 41% (25→27)[C] | 16.0x | 12.2x | 0.32 | ROE 33%[A] | 4 | **79** |
| 4 | TSMC | TSM | GARP / Quality | 2026 >40%[G] | +33% (26→27)[C] | 26.9x | 20.3x | 0.67 | ~30%+[M] | 4 | **79** |
| 5 | Micron | MU | Earnings Revision (⚠Cyclical) | FQ4 +~340% y/y[G] | FY27 +113%[C] | 6.9x | 확인 불가 | n/m (경기민감) | 확인 불가 | 5 | **78** |
| 6 | AppLovin | APP | GARP | +53% (Q2)[A] | 2027 +34%[C] | 21.3x | 15.9x | 0.50 | ~133%[A/aggregator] | 2 | **76** |
| 7 | Lam Research | LRCX | Earnings Revision | 9월분기 가이던스 +52%[G] | FY27 +60%[C] | 32.0x | 확인 불가 | 0.53 | 확인 불가 (고수익[M]) | 5 | **76** |
| 8 | 삼성전자 | 005930 | Earnings Revision (⚠Cyclical) | Q2 OP 약 ₩89.4조, 사상 최대[A/G] | 확인 불가 | 4.4x (fwd) | 확인 불가 | n/m | 확인 불가 | 4 | **76** |
| 9 | SK하이닉스 | 000660 | Earnings Revision (⚠Cyclical) | Q2 +257% y/y[A] | 2027 NI +33%[C] | 5.4x | 4.1x | n/m | ROE ~44% (2026)[C] | 3 | **75** |
| 10 | Celestica | CLS | High-Growth at Fair Price | 2026 +65%[G], 2027 가속[G] | 75% (25→27)[G 기반 M] | 42.8x | ≤26.0x[G 기반 M] | 0.39 | 확인 불가 | 4 | **74** |
| 11 | Dell | DELL | Earnings Revision | FY27 +69%[G] | FY27 +150%[G] | 22.9x | 확인 불가 | 0.15 (신뢰도 낮음) | 확인 불가 | 5 | 74 |
| 12 | AMD | AMD | Growth Inflection | +50% (Q2)[A] | 2027 +105%[C] | 82.2x | 40.0x | 0.44 | 낮음(영업권)[M] | 5 | 74 |
| 13 | Uber | UBER | GARP | GB +24%, EBITDA +33%[A] | 비GAAP EPS +35% (Q2)[A] | Fwd 17.3x[C] | 확인 불가 | ~0.55[M] | 확인 불가 | 3 | 73 |
| 14 | Western Digital | WDC | Earnings Revision (⚠Cyclical) | GM 50% 돌파[A] | 확인 불가 (FY27 $20.03[C]) | 22.4x | 확인 불가 | n/m | 확인 불가 | 4 | 73 |
| 15 | Seagate | STX | Earnings Revision (⚠Cyclical) | FQ1 $4.1B[G] | 확인 불가 (FY27 $35.78[C]) | ~31x | 확인 불가 | n/m | 확인 불가 | 5 | 73 |
| 16 | Eli Lilly | LLY | Quality Compounder | 확인 불가 | 약 20~25%[M] | ~30x (NTM) | 확인 불가 | ~1.2~1.3[M] | 높음 | 3 | 70 |
| 17 | Marvell | MRVL | Growth Inflection | FY28 +50% ($18B)[G] | 확인 불가 | 확인 불가 | ~39x (단일 추정) | ~0.65~0.8[M] | 낮음(영업권) | 4 | 69 |
| 18 | Vertiv | VRT | Growth Inflection | 유기적 +30~32%[G] | Q2 조정 EPS +60%[A] | ~43x | 확인 불가 | ~1.1~1.4[M] | 높음 | 4 | 69 |
| 19 | Microsoft | MSFT | Quality Compounder | Azure +43~45%[A/G] | 약 15~20%[M] | ~25~26x | 확인 불가 | ~1.4[M] | 높음 | 3 | 69 |
| 20 | Meta | META | Momentum-supported Fundamental | +28% (Q2)[A] | 약 20~25%[M] | 확인 불가 | 21.8x | ~0.9~1.0[M] | 하락 중(capex) | 3 | 68 |

**경계선 탈락:** SanDisk(68), Alphabet·Amazon(일회성 이익으로 EPS 정상화 필요), Kioxia·Advantest·Credo(주가 데이터 확인 불가).

**동점 처리 원칙:** 유형 우선순위(GARP > High-Growth at Fair Price > Earnings Revision > Growth Inflection > Quality Compounder) → 경기민감(⚠) 플래그가 없는 종목 우선 → Valuation 점수 순.

---

## 3. Top 10 — Thesis / 시장이 놓치는 것 / Catalyst / Risk

### ① NVIDIA (NVDA) — 88점 · S
- **Thesis:** FY28 EPS 컨센서스가 30일 만에 $12.82→$15.68(+22%, 상향 42건·하향 0건)[C]. 같은 기간 주가는 실적 발표 전 $214.77 → $227.38(+5.9%)에 그쳤다. **이익이 주가를 추월하면서 FY28 P/E가 14.5x까지 압축**됐다.
- **시장이 놓치는 것:** 주가에서 역산하면 FY28 이후 5년간 EPS 연 **+3.9%**만 반영돼 있다[I]. 시장은 FY28을 사이클 고점으로 가격에 넣었다. 경영진은 FY28 매출 +70%를 제시했다(종전 모델 ~44%)[G]. 또한 FY27부터 비GAAP EPS에 SBC를 포함하므로, 과거 정의 대비 이익 성장률이 보수적으로 표시된다[A].
- **Catalyst:** 11월 FQ3 실적(가이던스 $108B ±2%)[G], Vera Rubin 양산 램프, FY28 가이던스 구체화.
- **Risk:** 이익의 질. Q2 순이익 $59.7B 대비 영업현금흐름 $24.1B, FCF $21.3B(전분기 대비 −$27.2B)[A]. 매출채권 +$22B, 재고 $32B, DSO 60일로 고객 결제조건이 연장됐다. $279B 공급 약정과 AI 클라우드 파트너 보증(상한 $108.5B)도 있다[A]. 그 밖에 하이퍼스케일러 capex 소화 국면, 커스텀 ASIC 잠식, 수출규제.

### ② Broadcom (AVGO) — 86점 · S
- **Thesis:** AI 반도체 매출 FY26 $58B → FY27 가시성 $115B → FY28 $230B[G]. FY27 EPS $19.38[C] 기준 18.5x, FY28 $25.86[C] 기준 13.8x다. 호실적에도 주가는 횡보·하락했다[언론 9/17].
- **시장이 놓치는 것:** 주가가 FY28 이후 연 **+3.5%** 성장만 반영한다[I]. 반면 FY28 AI 매출 가시성은 FY27의 2배다. FY28 컨센서스 $25.86은 이 가이던스를 다 반영하지 못했을 가능성이 크다(확인 필요).
- **Catalyst:** 12월 FQ4 실적(매출 가이던스 $34.8B, +93%)[G]과 FY27 가이던스, 신규 XPU 고객.
- **Risk:** 고객 집중(Google·Meta·OpenAI·Anthropic), 랙스케일 시스템 비중 확대에 따른 GM 희석, VMware 정상화, 부채(ND/EBITDA 약 1x[M]). FY27 추정치는 상향 6건·하향 1건(Truist $22.35→$21.12)[C].

### ③ Nu Holdings (NU) — 79점 · A (★★ Exceptional)
- **Thesis:** 2026 EPS $0.88 → 2027 $1.15(+31%)[C]. 2027 P/E 12.2x, ROE 33%[A], Q2 순이익 $1.06B(+67%)[A], 고객 1.39억 명. 추정치는 상향되는데 주가는 최근 $15 중반 → $14.06으로 밀렸다.
- **시장이 놓치는 것:** 13% 자기자본비용 가정 시 주가는 2027 이후 연 **+8.9%** 성장만 반영한다[I]. 컨센서스 3년 순이익 CAGR은 35%다[C]. 멕시코 은행업 전환과 미국 진출 옵션은 가격에 거의 들어가 있지 않다.
- **Catalyst:** 11월 Q3 실적(EPS 컨센 $0.23, +35%)[C], 멕시코 라이선스 가동, 미국 서비스 개시.
- **Risk:** 브라질 신용주기·고금리·BRL 환율, 핀테크 과세·규제, 신규 시장 확장 비용. 베어 시나리오 하방이 커서 R/R이 Top 5 중 가장 약하다.

### ④ TSMC (TSM) — 79점 · A
- **Thesis:** 2026 USD 매출 +40% 이상[G], 8월 매출 NT$514.8B(+53% y/y)[A]. 2027 EPS $21.93(+33%)[C] 기준 20.3x다. AI 체인에서 ROIC·FCF 질이 가장 높은 해자다.
- **시장이 놓치는 것:** 주가는 2027 이후 연 +12.4% 성장을 반영한다[I]. N2 램프와 CoWoS 가격 인상이 구조적 성장률(~20%)을 받쳐 준다.
- **Catalyst:** 월별 매출(10월 초), 10월 중순 Q3 실적과 2027 capex·가격 전망.
- **Risk:** 지정학, 미국 공장 마진 희석, 고객 집중.

### ⑤ Micron (MU) — 78점 · A (⚠ Cyclical Peak Trap 검증 필요)
- **Thesis:** FY27 EPS 컨센서스가 약 3개월 만에 $98.52 → $156.07(+58%)[C]로 가장 강하게 상향됐다. FY27 P/E 6.9x. FQ4 가이던스는 매출 $50B·EPS $31[G], 보고일은 9/30이다.
- **시장이 놓치는 것:** 주가는 FY27 이후 **연 −12%의 이익 감소**를 반영한다[I]. 그런데 16개 전략고객계약(SCA)이 최소가격 기준 약 $100B 매출과 $22B 선수금을 확보했다[A/G]. 경영진은 수급 타이트가 2027년 이후까지 지속된다고 본다.
- **Catalyst:** **9/30 FQ4 실적 + FY27 가이던스**(1주 내), HBM4 Rubin 공급.
- **Risk:** 메모리 사이클(스트리트는 2028 피크 예상), 신규 capa(삼성 P5·용인 2028), capex 급증. EPS가 사상 최고라 PEG는 의미가 없다.

### ⑥ AppLovin (APP) — 76점 · A
- **Thesis:** 2027 EPS $20.79[C] 기준 15.9x. ROIC 약 133%, 조정 EBITDA 마진 80%대 중반, FCF는 EBITDA의 약 75%[A/aggregator]. Q2 매출 미스(−1%) 이후 −16~21% 급락해 52주 저점권이다.
- **시장이 놓치는 것:** 주가는 2027 이후 연 +9.6% 성장만 반영한다[I]. 경영진은 모델 개선의 계단식 상승이 분기 말 직후에 나타났다고 밝혔다.
- **Catalyst:** 11월 초 Q3 실적과 Q4 가이던스, 이커머스 셀프서브 확장, 자사주 매입(Q2 $551M)[A].
- **Risk:** 2026 EPS 컨센서스가 30일간 −$0.50(−3%)[C]로 **Revision 음수**. 집단소송, 플랫폼 정책, 게임 광고 의존.

### ⑦ Lam Research (LRCX) — 76점 · A
- **Thesis:** FY27 EPS 컨센서스가 30일간 +17.8% 상향돼 $9.32(+60%)[C]. 9월분기 가이던스는 매출 $8.1B·EPS $2.15[G]. JPM은 2027 WFE +38%($225B)를 전망한다[C].
- **시장이 놓치는 것:** 메모리 capex(HBM·NAND 전환)의 강도.
- **Catalyst:** 10월 실적과 12월분기 가이던스.
- **Risk:** 주가가 FY27 이후 연 +23.5% 성장을 이미 요구한다[I]. **상당히 선반영**돼 있고, 베어 −48%로 R/R이 약하다. WFE 사이클과 중국 비중도 부담.

### ⑧ 삼성전자 (005930) — 76점 · A (⚠ Cyclical)
- **Thesis:** 주가 ₩276,500, Forward P/E 4.43x[C], TTM 13.6x → FY+1 압축률 67%. Q2'26 영업이익 사상 최대[A]. HBM4가 Nvidia Rubin 인증을 받았다[언론].
- **시장이 놓치는 것:** 경영진은 2027년 공급 부족이 더 심해진다고 본다. 신규 capa(P5·용인)는 2028년에나 가동된다.
- **Catalyst:** 10월 초 Q3 잠정실적, HBM4 물량, 주주환원.
- **Risk:** 메모리 사이클, 파운드리 적자, 연간 EPS 컨센서스 확인 불가.

### ⑨ SK하이닉스 (000660) — 75점 · A (⚠ Cyclical)
- **Thesis:** 2027 영업이익 컨센서스 ₩391.8조, 순이익 ₩334조[C] → 2027 P/E 4.1x. Q2 영업이익률 76%[A], LTA 체결 고객 10곳[A].
- **시장이 놓치는 것:** 11% 할인율 가정 시 주가는 **2027 이후 연 −26%의 이익 감소**를 반영한다[I]. LTA가 이익 지속기간을 늘릴 수 있다.
- **Catalyst:** 10월 말 Q3 실적, HBM4 점유율, ADR(SKHY) 수급.
- **Risk:** Q2가 컨센서스(매출 ₩84조, 영업이익 ₩64조)를 하회했다[A]. 사이클과 capex.

### ⑩ Celestica (CLS) — 74점 · B+
- **Thesis:** 2026 매출 $20.5B(+65%)·EPS $11.30(+87%)로 연중 두 차례 상향[G]. 2027 매출 성장은 65%를 넘어 가속하고 EPS 성장은 그보다 빠르다고 가이던스했다[G] → 2027 EPS ≥ 약 $18.6[M].
- **시장이 놓치는 것:** 일부 2027 컨센서스(약 $15)[C]가 가이던스를 따라가지 못하고 있다.
- **Catalyst:** 10월 말 Q3 실적, 1월 2027 공식 가이던스.
- **Risk:** 고객 집중, EMS 저마진 구조. 가이던스 기준으로도 주가가 2027 이후 연 +19% 성장을 요구한다[I]. 주가 $483은 평균 목표가 $473을 이미 넘었다.

---

## 4. Top 5 상세

### [1] NVIDIA (NVDA)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | NVIDIA Corp. / NVDA |
| 2 | 현재가 | $227.38 (2026-09-22 종가)[A] |
| 3 | 시가총액 | 약 $5.43T[A] |
| 4 | 사업 유형 | AI 가속 컴퓨팅 플랫폼 (GPU·네트워킹·시스템·소프트웨어) |
| 5 | 핵심 사업 변화 | Blackwell Ultra에서 Vera Rubin으로 전환. 데이터센터 매출 $89.0B(+117% y/y)[A]. 배당 25배 인상(분기 $0.25), FCF의 50% 이상 환원 방침[A] |
| 6 | NTM Revenue Growth | 약 +75~80%[M] (FQ3 가이던스 $108B[G], FY28 +70%[G] 가정) |
| 7 | 2Y Revenue CAGR | 약 +78% (FY26→FY28)[M] |
| 8 | FY+1 EPS Growth | +95% (FY26 $4.77[A] → FY27 $9.31[C, 9/8]) |
| 9 | 2Y EPS CAGR | +81% (→ FY28 $15.68[C]) |
| 10 | 3Y EPS CAGR | 확인 불가 (FY29 컨센서스 없음) |
| 11 | NTM P/E | 16.7x[M] (FY27/FY28 기간 가중 NTM EPS $13.56) |
| 12 | FY+1 P/E | 24.4x |
| 13 | FY+2 P/E | 14.5x |
| 14 | PEG 1Y | 0.18[M] |
| 15 | PEG 2Y | 0.21[M] |
| 16 | FY+2 P/E Compression | **55%** (TTM 32.4x → 14.5x; TTM EPS $7.01[A]) → **SS급** |
| 17 | ROIC | 확인 불가 (GM 75%[A], 순이익률 약 62% → WACC의 수배[M]) |
| 18 | RONIC | 확인 불가 (Q2에 운전자본 +$20B대 증가로 단기 RONIC 하락 추정[M]) |
| 19 | FCF Margin | Q2 22% (FCF $21.3B / 매출 $96.2B)[A] ⚠ (순이익률 대비 크게 낮음) |
| 20 | Net Debt/EBITDA | 순현금 (정확치 확인 불가) |
| 21 | 최근 1개월 Revision | FY28 EPS +22.3% ($12.82→$15.68, 상향 42 / 하향 0)[C] → **5** |
| 22 | 최근 3개월 Revision | FY28 EPS +22.4% (90일)[C] → 5 |
| 23 | 가장 중요한 Catalyst | 11월 FQ3 실적과 Vera Rubin 램프 확인, FY28 +70% 가이던스의 수치화 |
| 24 | 가장 중요한 Risk | **이익의 질**: 매출채권·재고 급증, 공급 약정 $279B, 파트너 보증 상한 $108.5B |
| 25 | 시장이 놓치는 것 | FY28을 고점으로 가정한 가격. 비GAAP 정의 변경(SBC 포함)으로 성장률이 과소 표시됨 |
| 26 | 현재 주가가 요구하는 성장 | FY28 이후 5년 EPS 연 **+3.9%**, 이후 영구 3% (자기자본비용 10%, EPS≈FCF 가정)[I] |
| 27 | Consensus가 예상하는 성장 | FY27 +95%, FY28 +68%[C] |
| 28 | Expectation Gap | 매우 큼. 다만 FCF 전환율이 회복되지 않으면 EPS≈FCF 가정이 과대평가될 수 있음 |
| 29 | 12개월 단순 EPS×P/E 가격 | $323[M] (NTM P/E 16.7x 고정, FY29 = FY28×(1+34%) 외삽) / 컨센서스만 쓰면 $263 |
| 30 | Potential Upside | +42%[M] (컨센서스만 쓰면 +15%) |
| 31 | Bear Downside | $165 (−28%) (FY28 EPS −30% × 15x)[M] |
| 32 | Risk/Reward | 1.5 : 1 (컨센서스만 쓰면 0.5 : 1) |
| 33 | 총점 | **88 / 100 (S)** |
| 34 | 투자 유형 | High-Growth at Fair Price + Earnings Revision Play, **★★ Exceptional Growth-Adjusted Candidate** |

### [2] Broadcom (AVGO)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Broadcom Inc. / AVGO |
| 2 | 현재가 | 약 $357.61 (2026-09-22)[A, 언론] |
| 3 | 시가총액 | 약 $1.77T[M] (희석주식 약 49.5억 주 가정) |
| 4 | 사업 유형 | 커스텀 AI 가속기(XPU)·AI 네트워킹 + 인프라 소프트웨어(VMware) |
| 5 | 핵심 사업 변화 | AI 반도체 매출 FQ3 $16.7B(+221%) → FQ4 가이던스 $21.7B(+236%)[A/G]. FY27 $115B, FY28 $230B 가시성[G] |
| 6 | NTM Revenue Growth | 약 +55%[M] |
| 7 | 2Y Revenue CAGR | 약 +58% (FY25 $63.9B → FY27 약 $160B)[M] |
| 8 | FY+1 EPS Growth | +71% (FY25 $6.82[A] → FY26 약 $11.66[M]: Q1 $2.05 + Q2 $2.44 + Q3 $3.32[A] + Q4 약 $3.85[M, 가이던스 기반]) |
| 9 | 2Y EPS CAGR | +69% (→ FY27 $19.38[C, 47명]) |
| 10 | 3Y EPS CAGR | +56% (→ FY28 $25.86[C, LSEG]) |
| 11 | NTM P/E | 19.3x[M] |
| 12 | FY+1 P/E | 30.7x (FY26) |
| 13 | FY+2 P/E | 18.5x (FY27) · FY+3 13.8x |
| 14 | PEG 1Y | 0.27[M] |
| 15 | PEG 2Y | 0.28[M] (3Y 0.34) |
| 16 | FY+2 P/E Compression | **50%** (TTM 36.6x → 18.5x) · FY+3 기준 **62%** → S~SS급 |
| 17 | ROIC | 약 25~40% (비GAAP NOPAT, 영업권 포함)[M] (확인 필요) |
| 18 | RONIC | 매우 높음 (팹리스 구조로 증분 투하자본이 작음)[M] |
| 19 | FCF Margin | FY25 약 42%[A 근사]. FY26 정확치 확인 불가 |
| 20 | Net Debt/EBITDA | 약 1x, 하락 추세[M] |
| 21 | 최근 1개월 Revision | FY27 EPS 상향 6 / 하향 1[C] → **4** |
| 22 | 최근 3개월 Revision | 확인 불가 |
| 23 | 가장 중요한 Catalyst | 12월 FQ4 실적과 FY27 매출·EPS 가이던스 ($115B AI 가시성의 수치화) |
| 24 | 가장 중요한 Risk | 상위 3~4개 고객 집중, 시스템 매출 비중 증가에 따른 GM 하락 |
| 25 | 시장이 놓치는 것 | FY28 AI 매출 2배 가시성 대비 FY28 컨센서스 EPS +33%는 보수적. 주가 횡보로 멀티플만 계속 압축 중 |
| 26 | 현재 주가가 요구하는 성장 | FY28 이후 5년 EPS 연 **+3.5%**[I] |
| 27 | Consensus가 예상하는 성장 | FY27 +66%, FY28 +33%[C] |
| 28 | Expectation Gap | 매우 큼 |
| 29 | 12개월 단순 EPS×P/E 가격 | $485[M] (NTM P/E 19.3x × 12개월 뒤 NTM EPS $25.15) |
| 30 | Potential Upside | +36% |
| 31 | Bear Downside | $248 (−31%) (FY27 EPS −20% × 16x)[M] |
| 32 | Risk/Reward | 1.2 : 1 |
| 33 | 총점 | **86 / 100 (S)** |
| 34 | 투자 유형 | High-Growth at Fair Price, ★ Alpha (FY+3 기준 ★★) |

### [3] Nu Holdings (NU)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Nu Holdings Ltd. / NU |
| 2 | 현재가 | $14.06 (2026-09-21)[A] |
| 3 | 시가총액 | 약 $68B[M] |
| 4 | 사업 유형 | 중남미 디지털 은행 (브라질·멕시코·콜롬비아, 미국 진출 추진) |
| 5 | 핵심 사업 변화 | 분기 순이익 $1B대 정착, 멕시코 은행업, 미국 진출 |
| 6 | NTM Revenue Growth | 약 +35%[M] (Q2 총수익 약 $5.9B, +39%[A]) |
| 7 | 2Y Revenue CAGR | 확인 불가 |
| 8 | FY+1 EPS Growth | +52% (2025 약 $0.58[A 근사] → 2026 $0.88[C]) |
| 9 | 2Y EPS CAGR | +41% (→ 2027 $1.15[C]) |
| 10 | 3Y EPS CAGR | 순이익 3년 CAGR 35%[C] |
| 11 | NTM P/E | 13.1x[M] |
| 12 | FY+1 P/E | 16.0x |
| 13 | FY+2 P/E | 12.2x |
| 14 | PEG 1Y | 0.25[M] |
| 15 | PEG 2Y | 0.32[M] |
| 16 | FY+2 P/E Compression | 34% (TTM 약 18.5x[M] → 12.2x) → A급 경계 |
| 17 | ROIC | 해당 없음 (은행) → ROE 33%[A] |
| 18 | RONIC | 증분 ROE 30%대 추정[M] |
| 19 | FCF Margin | 해당 없음 (은행). 순이익률 약 43%(Q2)[aggregator] |
| 20 | Net Debt/EBITDA | 해당 없음 (자본비율로 평가해야 함, 확인 불가) |
| 21 | 최근 1개월 Revision | 상향 중[C, 정량치 확인 불가] → **4** |
| 22 | 최근 3개월 Revision | 확인 불가 |
| 23 | 가장 중요한 Catalyst | 11월 Q3 실적(신용비용·NIM), 멕시코 은행 전환 |
| 24 | 가장 중요한 Risk | 브라질 신용 사이클(NPL)과 규제·과세 |
| 25 | 시장이 놓치는 것 | 30%대 ROE로 30%대 성장이 가능한데 P/E 12x. 미국·멕시코 옵션가치 |
| 26 | 현재 주가가 요구하는 성장 | 2027 이후 5년 EPS 연 **+8.9%** (자기자본비용 13%)[I] |
| 27 | Consensus가 예상하는 성장 | 2026 +52%, 2027 +31%, 3년 CAGR 35%[C] |
| 28 | Expectation Gap | 큼 |
| 29 | 12개월 단순 EPS×P/E 가격 | $16.8[M] (컨센서스만 쓰면 $15.1) |
| 30 | Potential Upside | +19% (컨센서스만 쓰면 +7%) |
| 31 | Bear Downside | $8.6 (−39%) (EPS −25% × 10x)[M] |
| 32 | Risk/Reward | 0.5 : 1 ⚠ (정밀분석에서 신용비용 시나리오가 핵심) |
| 33 | 총점 | **79 / 100 (A)** |
| 34 | 투자 유형 | GARP, **★★ Exceptional Growth-Adjusted Candidate** |

### [4] TSMC (TSM)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Taiwan Semiconductor Manufacturing / TSM (ADR) |
| 2 | 현재가 | $445.33 (2026-09-22 시가)[A] |
| 3 | 시가총액 | 약 $2.3T[M] |
| 4 | 사업 유형 | 파운드리 (선단 공정·첨단 패키징) |
| 5 | 핵심 사업 변화 | 2026 USD 매출 가이던스 +40% 초과로 상향[G], 8월 매출 +53% y/y[A] |
| 6 | NTM Revenue Growth | 약 +30~35%[M] |
| 7 | 2Y Revenue CAGR | 확인 불가 |
| 8 | FY+1 EPS Growth | 확인 불가 (2025 확정치 미확인). 2026 EPS $16.55~16.93[C] |
| 9 | 2Y EPS CAGR | 확인 불가 |
| 10 | 3Y EPS CAGR | 확인 불가 |
| 11 | NTM P/E | 21.7x[M] |
| 12 | FY+1 P/E | 26.9x |
| 13 | FY+2 P/E | 20.3x (2027 EPS $21.93[C]) |
| 14 | PEG 1Y | 확인 불가 |
| 15 | PEG 2Y | 0.67[M] (2027 성장률 +33% 사용) |
| 16 | FY+2 P/E Compression | 25% (FY+1 대비. TTM 기준은 확인 불가) |
| 17 | ROIC | 약 30%+[M] |
| 18 | RONIC | 높음 (가격 인상과 선단 공정 믹스)[M] |
| 19 | FCF Margin | 확인 불가 (대규모 capex에도 흑자) |
| 20 | Net Debt/EBITDA | 순현금 |
| 21 | 최근 1개월 Revision | 2026 EPS 소폭 상향(Erste $16.72→$16.78), 목표가 상향(BofA $490→$590)[C] → **4** |
| 22 | 최근 3개월 Revision | 확인 불가 |
| 23 | 가장 중요한 Catalyst | 10월 Q3 실적과 2027 가격·capex 전망 |
| 24 | 가장 중요한 Risk | 대만 지정학, 해외 공장 마진 희석 |
| 25 | 시장이 놓치는 것 | AI 체인에서 가장 경쟁이 적은 병목인데 P/E는 NVDA와 비슷한 수준 |
| 26 | 현재 주가가 요구하는 성장 | 2027 이후 5년 연 +12.4%[I] |
| 27 | Consensus가 예상하는 성장 | 2027 +33%[C] |
| 28 | Expectation Gap | 중간 (실적이 주가를 따라잡는 중) |
| 29 | 12개월 단순 EPS×P/E 가격 | $534[M] (컨센서스만 쓰면 $470) |
| 30 | Potential Upside | +20% (컨센서스만 쓰면 +7%) |
| 31 | Bear Downside | $298 (−33%)[M] |
| 32 | Risk/Reward | 0.6 : 1 |
| 33 | 총점 | **79 / 100 (A)** |
| 34 | 투자 유형 | GARP / Quality Compounder (Near-Alpha: FY+2 P/E 20.3x) |

### [5] Micron (MU)

| # | 항목 | 값 |
|---|---|---|
| 1 | 기업명/티커 | Micron Technology / MU |
| 2 | 현재가 | $1,080.67 (2026-09-22)[A] (YTD +247%) |
| 3 | 시가총액 | 약 $1.22T[M] |
| 4 | 사업 유형 | DRAM·HBM·NAND 메모리 |
| 5 | 핵심 사업 변화 | HBM4 Rubin 공급, 16개 SCA(최소가격 약 $100B, 선수금 $22B), Cloud Memory GM 83%[A] |
| 6 | NTM Revenue Growth | 확인 불가 (FQ4 가이던스 $50B, 전년 동기 대비 약 +340%[G]) |
| 7 | 2Y Revenue CAGR | 확인 불가 |
| 8 | FY+1 EPS Growth | +113% (FY26 약 $73.44[A+G] → FY27 $156.07[C, 9/21]) |
| 9 | 2Y EPS CAGR | 확인 불가 (FY28 컨센서스 없음) |
| 10 | 3Y EPS CAGR | 확인 불가 |
| 11 | NTM P/E | 약 6.9x[M] |
| 12 | FY+1 P/E | 6.9x (FY27) · FY26 기준 14.7x |
| 13 | FY+2 P/E | 확인 불가 |
| 14 | PEG 1Y | 0.06 (산술값. 경기민감주라 **신뢰도 낮음**) |
| 15 | PEG 2Y | 확인 불가 |
| 16 | P/E Compression | TTM(FQ3 기준 약 23.9x[M]) → FY27 6.9x = **71%**. FY26 대비 53% |
| 17 | ROIC | 확인 불가 (현재 사상 최고, 사이클 평균은 10~15%대로 추정[M]) |
| 18 | RONIC | 확인 불가 |
| 19 | FCF Margin | 확인 불가 |
| 20 | Net Debt/EBITDA | 순현금 전환 추정 (확인 불가) |
| 21 | 최근 1개월 Revision | 강한 상향 (정량치 확인 불가) → **5** |
| 22 | 최근 3개월 Revision | FY27 EPS $98.52(6월) → $156.07(9월) **+58%**[C] |
| 23 | 가장 중요한 Catalyst | **9/30 FQ4 실적과 FY27 가이던스** |
| 24 | 가장 중요한 Risk | 메모리 사이클 피크(스트리트 2028 예상), 2028년 경쟁사 신규 capa |
| 25 | 시장이 놓치는 것 | SCA 최소가격 계약 → 과거 사이클보다 이익 바닥이 높을 가능성 |
| 26 | 현재 주가가 요구하는 성장 | FY27 이후 5년 **연 −12%**(이익 감소), 할인율 11%[I] |
| 27 | Consensus가 예상하는 성장 | FY27 +113%. FY28은 스트리트가 사이클 피크로 봄 |
| 28 | Expectation Gap | 큼 (단, 시장이 가정한 하락 폭 자체가 핵심 논쟁) |
| 29 | 12개월 단순 EPS×P/E 가격 | 멀티플 고정 시: FY28 EPS 횡보면 $1,080(0%), FY28 +15%면 $1,229(+14%)[M]. FY27 10x 재평가 시 $1,561(+44%) |
| 30 | Potential Upside | 멀티플 고정 기준 0~+14% (멀티플 정상화가 필요) |
| 31 | Bear Downside | $720 (−33%) (정상화 EPS $60 × 12x)[M]. 심화 시 −50% 이상 |
| 32 | Risk/Reward | 재평가 가정 시 1.3 : 1, 멀티플 고정 시 0.4 : 1 |
| 33 | 총점 | **78 / 100 (A)** — Valuation 13·Risk 5로 상한 적용 |
| 34 | 투자 유형 | Earnings Revision Play (⚠ Cyclical, ★★ 조건을 산술적으로는 충족하나 보류) |

---

## 5. 최종 Ranking (점수 분해)

배점: Growth 20 · Valuation 20 · Revision 15 (상태 × 3) · Quality 15 · Expectation Gap 10 · Catalyst 10 · Risk 10

| 순위 | 기업 | 총점 | Growth | Valuation | Revision | Quality | Expectation Gap | Catalyst | Risk |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NVDA | 88 | 19 | 18 | 15 | 11 | 9 | 9 | 7 |
| 2 | AVGO | 86 | 18 | 18 | 12 | 13 | 9 | 9 | 7 |
| 3 | NU | 79 | 15 | 18 | 12 | 13 | 8 | 7 | 6 |
| 4 | TSM | 79 | 15 | 14 | 12 | 15 | 7 | 8 | 8 |
| 5 | MU | 78 | 18 | 13 | 15 | 11 | 7 | 9 | 5 |
| 6 | APP | 76 | 15 | 18 | 6 | 15 | 8 | 8 | 6 |
| 7 | LRCX | 76 | 17 | 12 | 15 | 14 | 4 | 8 | 6 |
| 8 | 삼성전자 | 76 | 18 | 13 | 12 | 10 | 8 | 8 | 7 |
| 9 | SK하이닉스 | 75 | 19 | 13 | 9 | 12 | 8 | 8 | 6 |
| 10 | CLS | 74 | 19 | 13 | 12 | 11 | 5 | 8 | 6 |
| 11 | DELL | 74 | 18 | 14 | 15 | 9 | 5 | 8 | 5 |
| 12 | AMD | 74 | 19 | 11 | 15 | 11 | 3 | 9 | 6 |
| 13 | UBER | 73 | 13 | 16 | 9 | 13 | 8 | 7 | 7 |
| 14 | WDC | 73 | 17 | 14 | 12 | 12 | 6 | 7 | 5 |
| 15 | STX | 73 | 18 | 11 | 15 | 12 | 5 | 7 | 5 |
| 16 | LLY | 70 | 14 | 11 | 9 | 14 | 6 | 8 | 8 |
| 17 | MRVL | 69 | 17 | 11 | 12 | 9 | 5 | 8 | 7 |
| 18 | VRT | 69 | 15 | 10 | 12 | 13 | 5 | 7 | 7 |
| 19 | MSFT | 69 | 12 | 12 | 9 | 13 | 7 | 7 | 9 |
| 20 | META | 68 | 14 | 13 | 9 | 11 | 5 | 8 | 8 |

**"왜 지금 조사해야 하는가?" (한 줄)**

1. **NVDA:** FY28 추정치가 한 달 새 22% 올랐는데 주가는 6% 올랐다. 이익의 질(FCF 전환) 논란만 풀리면 14.5x는 너무 싸다.
2. **AVGO:** AI 매출 2배 가시성($115B→$230B)에도 주가가 횡보해 FY28 P/E가 13.8x까지 눌렸다.
3. **NU:** 추정치는 오르고 주가는 내린다. ROE 33%·EPS +31% 종목이 2027 P/E 12x다.
4. **TSM:** AI 병목 1위 자산이 성장률(+33%) 대비 20x이고 목표가가 오르고 있다.
5. **MU:** 9/30 실적 직전. 시장은 FY27 이후 연 −12% 감익을 가정하는데 SCA 최소가격 계약이 이를 반박할 수 있다.
6. **APP:** 매출 1% 미스로 −20% 급락했다. ROIC 130%대 기업이 2027 P/E 16x이지만 추정치 하향이 멈추는지 확인해야 한다.
7. **LRCX:** 30일 +17.8% 상향으로 추정치 모멘텀은 1위급이나, 주가가 이미 많이 반영해 진입가 규율이 필요하다.
8. **삼성전자:** Forward P/E 4.4x. 공급 부족이 2027년 더 심해진다는 회사 전망이 맞다면 이익 지속기간이 과소평가돼 있다.
9. **SK하이닉스:** 2027 P/E 4.1x로 연 −26% 감익이 가격에 반영돼 있다. LTA 10곳이 이 가정을 시험한다.
10. **CLS:** 회사 가이던스(2027 EPS 성장 > 매출 성장 65%+)가 컨센서스보다 앞서 있다.
11. **DELL:** FY27 EPS 가이던스가 $17.90→$25.50으로 올라 추정치 모멘텀은 최강이나, CFO 매도($585)와 저마진 구조를 점검해야 한다.
12. **AMD:** 2027 EPS 2배는 확실해 보이나 FY+2 P/E 40x로 이미 Bull 수준까지 반영됐다.
13. **UBER:** P/FCF 15.6x에 자율주행 공포가 반영돼 있다. EPS +35%와 FCF $10B+가 성장조정 기준으로 싸다.
14. **WDC:** FY27 P/E 22x로 HDD 공급 규율의 지속 여부가 핵심이다.
15. **STX:** 추정치가 90일간 35% 올랐으나 FY27 30x로 반영 속도가 빠르다.
16. **LLY:** 경구 GLP-1 출시 후 NTM 30x. 퀄리티는 최고지만 PEG 1 이상이다.
17. **MRVL:** FY28 매출 목표를 $16.5B→$18B로 올렸으나 멀티플이 여전히 높다.
18. **VRT:** 수주잔고 $15B+, 가이던스 상향에도 주가는 고점 대비 −24%. 2027 추정치 확인이 필요하다.
19. **MSFT:** Azure +45%에도 주가가 연초 대비 제자리다. PEG 약 1.4로 Quality 대안이다.
20. **META:** 9월 +35% 랠리로 기대가 빠르게 반영됐다. Muse 수익화 전까지는 적정 가격이다.

---

## 6. 최종 판정 (3축)

| 기업 | Absolute Valuation | Growth-Adjusted Valuation | Market Expectations |
|---|---|---|---|
| NVDA | 적정 | 성장 대비 매우 저평가 | 지나치게 낮음 |
| AVGO | 적정 | 성장 대비 매우 저평가 | 지나치게 낮음 |
| NU | 쌈 | 성장 대비 매우 저평가 | 지나치게 낮음 |
| TSM | 적정 | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 |
| MU | 매우 쌈 (정상화 EPS 기준 적정) | 성장 대비 매력적 (사이클 조정) | 지나치게 낮음 (감익을 이미 가정) |
| APP | 적정 | 성장 대비 매력적 | 지나치게 낮음 |
| LRCX | 비쌈 | 성장 대비 매력적 | 상당히 선반영 |
| 삼성전자 | 매우 쌈 | 성장 대비 매력적 (사이클 조정) | 지나치게 낮음 |
| SK하이닉스 | 매우 쌈 | 성장 대비 매력적 (사이클 조정) | 지나치게 낮음 |
| CLS | 비쌈 | 성장 대비 매력적 | 상당히 선반영 |
| DELL | 비쌈 (역사 10~15x 대비) | 성장 대비 매력적 (신뢰도 낮음) | 상당히 선반영 |
| AMD | 매우 비쌈 | 성장 대비 적정 | Bull 이상 선반영 |
| UBER | 적정 | 성장 대비 매력적 | 지나치게 낮음 |
| WDC | 적정 | 성장 대비 매력적 | 적절 |
| STX | 비쌈 | 성장 대비 적정 | 상당히 선반영 |
| LLY | 비쌈 | 성장 대비 적정 | 적절 |
| MRVL | 비쌈 | 성장 대비 적정 | 상당히 선반영 |
| VRT | 비쌈 | 성장 대비 비쌈 | 적절 |
| MSFT | 비쌈 | 성장 대비 비쌈 | 적절 |
| META | 적정 | 성장 대비 적정 | 상당히 선반영 |

---

## 7. Deep Dive 후보

**★★★ 즉시 정밀분석 추천**
1. NVIDIA (NVDA)
2. Broadcom (AVGO)
3. Nu Holdings (NU)

**★★ 높은 관심**
4. TSMC (TSM)
5. Micron (MU)
6. AppLovin (APP)
7. Lam Research (LRCX)

**★ Watchlist**
8. 삼성전자 (005930)
9. SK하이닉스 (000660)
10. Celestica (CLS)

### 상위 3개를 지금 전체 기업가치평가 프롬프트에 넣어야 하는 이유

**NVDA:** 주가는 FY28 이후 연 3.9% 성장만 반영하는데, 경영진은 FY28 매출 +70%를 제시했고 추정치는 한 달에 22% 올랐다. 결국 쟁점은 멀티플이 아니라 이익의 지속기간과 질이다. 그래서 Reverse DCF와 정상화 선행 실적, RONIC 분석이 가장 큰 차이를 만든다. 특히 운전자본 급증(매출채권 +$22B)과 보증·공급 약정을 반영한 FCF 기반 DCF로 "EPS 14.5x"가 "FCF 기준 몇 배"인지 검증해야 한다.

**AVGO:** 회사가 제시한 FY27~28 AI 매출 경로($115B→$230B)가 컨센서스 EPS에 얼마나 반영됐는지가 이 종목의 핵심 Expectation Gap이다. Forward DCF로 세그먼트별 매출·마진을 직접 모델링하면 컨센서스 대비 상향 여지를 정량화할 수 있다. 주가가 횡보한 상태라 멀티플 확장 없이 이익성장만으로 수익이 나는지 검증하기에 가장 깨끗한 사례다.

**NU:** 성장률 대비 P/E가 가장 낮은 비(非)AI 종목이라 포트폴리오 팩터 분산 효과가 있다. 은행이므로 일반 DCF 대신 잔여이익모형(ROE−COE)과 신용비용 스트레스 테스트가 필요하다. 이 프레임워크가 R/R 0.5의 약점(베어 −39%)을 걸러낼 수 있는지가 투자 여부를 가른다.

---

## 8. 핵심 질문에 대한 답

1. **Growth-Adjusted Valuation이 가장 좋은 기업:** **NVDA.** PEG 2Y 0.21, FY+2 P/E 14.5x, EPS 2Y CAGR 81%. 비AI 중에서는 **NU**(PEG 2Y 0.32, 2027 P/E 12.2x). 메모리주는 산술 PEG가 더 낮지만 경기민감주라 제외했다.
2. **현재 P/E는 높지만 EPS 성장 때문에 실제로 싼 기업:** **AVGO.** TTM 36.6x → FY27 18.5x → FY28 13.8x. 차순위는 CLS(2025 기준 약 80x → 2027 약 26x, 가이던스 기반)와 LRCX(51x → 32x).
3. **주가가 유지돼도 FY+2 P/E가 가장 빨리 내려가는 기업:** 비경기민감 중에서는 **NVDA**(−55%, 32.4x → 14.5x)와 AVGO(FY+3 기준 −62%). 경기민감주까지 포함하면 MU(TTM 대비 −71%)와 삼성전자(−67%)가 더 빠르지만, Peak EPS 함정 검증이 먼저다.
4. **Revision이 가장 강한데 주가 반응이 부족한 기업:** **NVDA.** FY28 EPS +22.3%(30일) vs 주가 +5.9%. 차순위는 NU(추정치 상향, 주가 −10%)와 AVGO(추정치 상향, 주가 횡보).
5. **EPS·FCF·ROIC가 함께 개선되는 기업:** **AVGO.** 팹리스라 증분 투하자본이 작고, 이익 증가에 따라 VMware 영업권이 희석되면서 ROIC가 오른다. 차순위는 **TSM**, **APP**(ROIC 130%대, FCF/EBITDA 약 75%). NVDA는 Q2 FCF 전환율(약 36%)이 급락해 이 질문에서는 제외했다.
6. **시장이 3~5년 성장 지속기간을 가장 과소평가하는 기업:** **AVGO.** FY28 이후 연 3.5%만 반영된 반면 AI 매출 가시성이 FY28까지 제시돼 있다. 차순위는 NVDA. 고위험 버전으로는 SK하이닉스(연 −26% 감익 반영 vs 5년 LTA).
7. **멀티플 상승 없이 12~24개월 15%+ 기대수익이 가능한 기업:** **AVGO**(+36%, FY28 컨센서스 기준)와 **NVDA**(컨센서스만 써도 +15%, 외삽 시 +42%). 그다음 CLS·TSM·APP·NU(외삽 시 +19~38%, 컨센서스만 쓰면 +7~12%)와 LRCX(+19%[M]).
8. **지금 정밀 기업가치평가 가치가 가장 높은 Top 5:** **① NVDA ② AVGO ③ NU ④ TSM ⑤ MU**

---

## 9. 포트폴리오 관점 경고

- **팩터 집중:** Top 10 중 8개(NVDA·AVGO·TSM·MU·LRCX·삼성·SK하이닉스·CLS)가 같은 변수, 즉 **하이퍼스케일러 AI capex**에 묶여 있다. 2027~28년 capex 소화가 오면 동시에 추정치가 하향될 수 있다. NU·APP·UBER는 이 리스크의 분산 수단이다.
- **이익의 질 신호:** NVDA의 운전자본 급증과 벤더 파이낸싱·보증, GOOGL·AMZN의 투자평가이익은 2026년 AI 사이클 후반부의 전형적인 경고 신호다. 정밀분석에서 EPS보다 FCF를 우선해야 한다.
- **메모리:** P/E 4~7x는 싸서가 아니라, 시장이 이익 급감을 가정해서 나온 숫자다. 정상화 EPS(사이클 평균)로 다시 계산한 P/E가 핵심 판단 기준이다.

---

## 10. 방법론 메모

- **NTM EPS** = FY+1 × (FY+1 잔여 비율) + FY+2 × (1 − 잔여 비율) [M]
- **Compression** = 1 − (FY+n P/E ÷ Current P/E). Current는 TTM, TTM이 불명이면 직전 회계연도 확정치.
- **PEG 1Y** = NTM P/E ÷ FY+1 EPS 성장률(%), **PEG 2Y** = NTM P/E ÷ 2Y EPS CAGR(%)
- **12개월 가격** = NTM P/E(고정) × 12개월 뒤 NTM EPS. FY+3 컨센서스가 없으면 FY+2 성장률의 절반으로 외삽[M]하고, 외삽 없는 값도 함께 표기.
- **Implied 성장률[I]:** 컨센서스 EPS 경로 → 이후 5년 일정 성장률 g → 영구성장 3%. 자기자본비용 10%(NU 13%, MU·WDC·STX·SK하이닉스 11%, APP 11%). EPS ≈ FCF로 가정했으며 NVDA처럼 FCF 전환율이 낮은 기업은 과소추정될 수 있음.
- **점수 상한:** 경기민감(메모리·스토리지)은 Valuation ≤ 14, Risk ≤ 6. 컨센서스 확인 불가 항목은 중립 이하로 처리.

---

## Sources (웹 검색 확인, 2026-09-22~23)

- 시장: [FactSet Earnings Insight](https://www.factset.com/earningsinsight), [FactSet S&P 500 Earnings Season Update](https://insight.factset.com/sp-500-earnings-season-update-august-7-2026)
- NVDA: [NVIDIA Q2 FY27 보도자료](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027), [NVIDIA Q4 FY26 보도자료](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026), [CNBC 8/26](https://www.cnbc.com/2026/08/26/nvidia-nvda-earnings-report-q2-2027-live-updates.html), [24/7 Wall St. 9/22](https://247wallst.com/investing/2026/09/22/nvidia-price-prediction-wall-street-and-our-model-finally-agree/), [24/7 Wall St. FCF 8/28](https://247wallst.com/investing/2026/08/28/nvidias-blockbuster-quarter-has-one-ugly-loose-end-27-billion-of-free-cash-flow-vanished/), [ad-hoc-news 9/22 종가](https://www.ad-hoc-news.de/boerse/news/nebenwerte/nvidia-stock-ends-the-day-2-30-percent-higher-at-usd-227-38/70159592), [Motley Fool 8/25](https://www.fool.com/investing/2026/08/25/nvda-stock-earnings-q2-date-aug-26/)
- AVGO: [Broadcom Q3 FY26 보도자료](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial), [Broadcom Q1 FY26](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial), [CNBC 9/2](https://www.cnbc.com/2026/09/02/broadcom-avgo-q3-earnings-report-2026.html), [Seeking Alpha AI 가이던스](https://seekingalpha.com/news/4639799-broadcom-forecasts-58b-fiscal-2026-ai-revenue-and-outlines-115b-in-2027-230b-in-2028), [FX Leaders 9/22](https://www.fxleaders.com/news/2026/09/22/broadcom-stock-forecast-avgo-ai-demand-recovery/), [24/7 Wall St. 9/17](https://247wallst.com/investing/2026/09/17/despite-hype-broadcom-keeps-edging-sideways-and-down-this-wall-street-analyst-says-it-will-provide-75-returns-soon/)
- NU: [Nu Q2 2026 보도자료](https://www.businesswire.com/news/home/20260813187996/en/Nu-Holdings-Ltd.-Reports-Second-Quarter-2026-Financial-Results), [StockTitan 6-K](https://www.stocktitan.net/sec-filings/NU/6-k-nu-holdings-ltd-current-report-foreign-issuer-b2dec17c9f33.html), [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/nu-holdings-ltd-nu-stock-214504003.html), [Simply Wall St](https://simplywall.st/stocks/us/banks/nyse-nu/nu-holdings)
- TSM: [TradingKey 8월 매출](https://www.tradingkey.com/analysis/stocks/us-stocks/262160382-tsmc-august-revenue-hit-new-high-tradingkey), [TipRanks](https://www.tipranks.com/news/tsmcs-revenue-acceleration-could-drive-more-upside), [ad-hoc-news 9/22](https://www.ad-hoc-news.de/boerse/news/corporate-news/tsm-stock-gains-as-earnings-estimates-rise/70155585)
- MU: [24/7 Wall St. 9/21](https://247wallst.com/investing/2026/09/21/micron-walks-into-the-biggest-earnings-setup-of-the-ai-memory-cycle/), [Micron FQ3 Prepared Remarks](https://investors.micron.com/static-files/631b1a32-5537-46ae-8f40-82e42fc79dfe), [Motley Fool 6/16](https://www.fool.com/investing/2026/06/16/this-will-be-microns-stock-price-late-2027/), [Vantage 실적일](https://www.vantagemarkets.com/market-news/micron-fiscal-q4-earnings-30-september-2026-september-23-2026/)
- APP: [CNBC 8/6](https://www.cnbc.com/2026/08/06/applovin-stock-q2-earnings-revenue.html), [AppLovin Q2 2026 보도자료](https://investors.applovin.com/news/news-details/2026/AppLovin-Announces-Second-Quarter-2026-Financial-Results/default.aspx), [Yahoo Finance 목표가 하향](https://finance.yahoo.com/markets/stocks/articles/analysts-slashing-price-targets-applovin-162723805.html), [GuruFocus Fwd P/E](https://www.gurufocus.com/term/forward-pe-ratio/APP)
- LRCX: [ad-hoc-news 9/21](https://www.ad-hoc-news.de/boerse/news/corporate-news/lam-research-stock-gains-3-58-percent-as-estimates-rise/70155739), [TIKR](https://www.tikr.com/blog/what-lam-research-q4-earnings-call-reveals-about-the-2027-setup), [Simply Wall St](https://simplywall.st/stocks/us/semiconductors/nasdaq-lrcx/lam-research)
- 삼성전자·SK하이닉스: [SK hynix 2Q26](https://news.skhynix.com/en/q2-2026-business-results/), [Investing.com SK hynix Q2](https://www.investing.com/news/company-news/sk-hynix-q2-2026-slides-record-revenue-76-operating-margin-93CH-4818489), [파이낸셜뉴스 8/13](https://www.fnnews.com/news/202608131045450610), [디일렉 1Q26](https://www.thelec.kr/news/articleView.html?idxno=55559), [CNBC Samsung Q2](https://www.cnbc.com/2026/07/30/samsung-q2-earnings-ai-chip-.html), [companiesmarketcap SK hynix](https://companiesmarketcap.com/sk-hynix/marketcap/)
- CLS: [Celestica Q2 2026](https://corporate.celestica.com/news-releases/news-release-details/celestica-announces-second-quarter-2026-financial-results), [Seeking Alpha 가이던스](https://seekingalpha.com/news/4619751-celestica-projects-20_5b-2026-revenue-and-11_30-adjusted-eps-as-it-outlines-2027-growth), [Stockchase](https://stockchase.com/CLS-T)
- DELL: [CNBC 9/1](https://www.cnbc.com/2026/09/01/dell-q2-earnings-report-2027.html), [TIKR](https://www.tikr.com/blog/dell-raised-guidance-by-27-billion-the-street-is-catching-up), [Vantage 9/3](https://www.vantagemarkets.com/en/market-analysis/dell-stock-price-today-september-3-2026/), [S&P Global Preview](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/08/dell-earnings-preview-fiscal-q2-2027)
- AMD: [24/7 Wall St. 9/21](https://247wallst.com/investing/2026/09/21/amd-is-about-to-become-a-trillion-dollar-stock-as-it-hikes-chip-prices-10/), [FX Leaders 9/22](https://www.fxleaders.com/news/2026/09/22/amds-1250-bullish-forecast-hyperscaler-lock-in-and-50-cpu-growth/)
- UBER: [Uber Q2 2026](https://investor.uber.com/news-events/news/press-release-details/2026/Uber-Announces-Results-for-Second-Quarter-2026/default.aspx), [GuruFocus P/FCF](https://www.gurufocus.com/term/price-to-free-cash-flow/UBER)
- WDC·STX: [ad-hoc-news WDC](https://www.ad-hoc-news.de/boerse/news/corporate-news/western-digital-stock-gains-as-ai-demand-lifts-earnings-estimates/70153577), [Seagate FQ4 2026](https://investors.seagate.com/news/news-details/2026/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2026-Financial-Results/default.aspx), [24/7 Wall St. STX 9/22](https://247wallst.com/investing/2026/09/22/seagate-went-from-207-to-1144-where-does-it-go-next/)
- 기타: [Meta 9월 랠리](https://finance.yahoo.com/markets/stocks/articles/meta-stock-jumped-11-monday-075049227.html), [Meta Q2](https://www.webull.com/blog/244-META-Q2-2026-Earnings-Revenue-EPS-Guidance-and-Key-Metrics), [Alphabet Q2 순이익](https://finance.yahoo.com/markets/stocks/articles/alphabet-q2-2026-net-income-065128000.html), [Amazon capex](https://www.cnbc.com/2026/07/30/amazon-amzn-q2-earnings-report-2026.html), [Microsoft 24/7](https://247wallst.com/investing/2026/09/21/azure-ai-capex-and-what-to-expect-out-of-microsoft-through-the-end-of-2026/), [Vertiv Q2](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Second-Quarter-2026-with-Diluted-EPS-Growth-of-53-Adjusted-Diluted-EPS-Growth-of-60-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/default.aspx), [Marvell FY28](https://www.tradingkey.com/news/transcripts/262137259-tradingkey), [MercadoLibre Q2](https://www.businesswire.com/news/home/20260805925866/en/MercadoLibre-Inc.-Reports-Second-Quarter-2026-Financial-Results), [Sea Q2](https://www.stocktitan.net/news/SE/sea-limited-reports-second-quarter-2026-hnyva894m8wm.html), [Eli Lilly](https://www.gurufocus.com/term/forward-pe-ratio/LLY), [SanDisk](https://www.forbes.com/sites/investor-hub/article/sandisk-stock-over-574-where-its-heading-2026/), [Kioxia](https://www.investing.com/news/transcripts/earnings-call-transcript-kioxia-q1-2026-profit-surges-stock-jumps-18-93CH-4826967), [Advantest](https://www.investing.com/news/company-news/advantest-q1-fy26-slides-record-profit-raised-forecast-on-ai-demand-93CH-4821153), [한국 전력기기](https://en.sedaily.com/news/2026/05/23/korean-power-equipment-trio-eyes-3-trillion-won-profit-on)

*본 자료는 정밀 가치평가 대상 선별을 위한 1차 스크리닝이며 투자 권유가 아니다.*
