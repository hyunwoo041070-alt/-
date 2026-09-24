# 성장주 스크리닝: Growth-Adjusted Valuation Screen

- **검색 기준일: 2026-09-23 미국 종가** (한국·일본·대만·유럽 종목은 2026-09-24 현지 시세), 작성일 2026-09-24
- 컨센서스 출처: Yahoo Finance 애널리스트 컨센서스 집계, 2026-09-23 스냅샷 [C]
- 실적·가이던스 출처: 회사 8-K/6-K, IR 보도자료, 실적 콜 [A]/[G]
- 라벨: **[A]** Actual · **[G]** Guidance · **[C]** Consensus · **[M]** Model(본 분석 산식) · **[I]** Implied(주가 역산)
- 확인하지 못한 숫자는 추정하지 않고 "확인 불가"로 적었다.

---

## 0. 결론 요약

1. **성장 대비 가장 싼 영역은 여전히 AI 인프라 밸류체인이다.** 8~9월 'AI capex 페이싱' 우려로 주가는 조정받았다. 반대로 FY+2 EPS 컨센서스는 오히려 올라갔다. 그래서 주가가 그대로여도 P/E가 빠르게 낮아지는 종목이 많다. 예: NVDA FY+2 P/E 14.4x, CLS 18.7x.
2. **정밀 가치평가 투입 순서(Top 5): NVDA → CLS → CIEN → TSM → AVC(3017.TW).** 다섯 종목 모두 멀티플이 오르지 않아도 이익성장만으로 12개월 +24~39%[M]가 가능하다.
3. **공통 리스크는 단 하나, '하이퍼스케일러 capex가 얼마나 오래 가느냐'다.** Top 20 중 17개가 이 변수에 묶여 있다.
   - 메모리(MU·SK하이닉스·삼성전자·SNDK)와 HDD(WDC·STX)는 FY+2 P/E 4~17x로 싸 보인다.
   - 하지만 **Cyclical Peak Trap**으로 판단해 순위에서 빼고 따로 표시했다.

---

## 1. 스크리닝 과정과 방법론

### Funnel

| 단계 | 조건 | 종목 수 |
|---|---|---|
| Universe | 미국 상장(NYSE/Nasdaq/NYSE American, ADR 포함) 시총 $2B 이상 2,150개 + 한국·일본·대만·유럽 주요 44개 | 2,194 |
| Pre-screen | FY+1·FY+2 EPS > 0, FY+2 EPS 성장 ≥ 12%, FY+2 P/E < 45x, 일평균 거래대금 > $15M(미국) | 826 (지표 산출 823) |
| 1단계 Growth Screen | 2Y EPS CAGR ≥ 15%, FY+2 EPS 성장 ≥ 10%, (2Y 매출 CAGR ≥ 12% 또는 FY+2 매출 성장 ≥ 15%), FY+2 P/E ≤ 40x | 338 |
| 2~14단계 | 100점 스코어 + False Positive 플래그 + 애널리스트 오버레이 | 338 채점 |
| 최종 | Peak-trap 제외 → Top 20 → Top 10 → Top 5 | 20 / 10 / 5 |

### 지표 정의

- **Current P/E**: 주가 ÷ 최근 4개 분기 조정 EPS 실적 합계 [A]. 컨센서스와 같은 non-GAAP 기준이라 GAAP TTM P/E와 다를 수 있다.
- **FY+1**: 진행 중인 회계연도(미발표). **FY+2**: 그다음 회계연도 [C]. **NTM EPS**: FY+1과 FY+2를 남은 기간으로 가중평균 [M].
- **P/E 압축률(Compression)**: FYn = 1 − FYn P/E ÷ Current P/E.
- **2Y EPS CAGR**: (FY+2 ÷ FY0 실적)^½ − 1. FY0에 일회성 손실이 있으면 FY+2 성장률로 대체해 정상화했다.
- **PEG**
  - PEG 1Y = NTM P/E ÷ FY+1 EPS 성장률(%).
  - PEG 2Y = NTM P/E ÷ 2Y EPS CAGR(%).
  - 보조 지표 Forward PEG = NTM P/E ÷ FY+2 성장률.
- **ROIC**: TTM EBIT × (1 − 세율) ÷ 평균 투하자본(자기자본 + 차입금 − 현금).
- **RONIC**: 2년 ΔNOPAT ÷ 2년 ΔIC(1년 시차).
  - 둘 다 재무제표 실적 [A]으로 계산했다.
  - GAAP 기준이라 인수 영업권이 큰 기업(AMD, AVGO, ONTO, MKSI)은 과소 측정된다.
- **현재 주가가 요구하는 성장 [I]**: 아래 식을 만족하는 4년 EPS CAGR g.
  - 주가 = NTM EPS × (1+g)^4 × 17 ÷ 1.095^5
  - 즉 5년 뒤 종료 P/E 17x, 요구수익률 9.5%로 역산했다.
- **12개월 가격 [M]**: 현재 NTM P/E를 고정하고, 12개월 뒤 NTM EPS를 곱한다.
  - FY+3는 FY+2 × (1 + min(30%, 0.7 × FY+2 성장률))로 외삽했다.
  - **멀티플 상승은 가정하지 않는다.**
- **Revision**: FY+1·FY+2 EPS 컨센서스를 30일·90일 전과 비교 [C].

### 확인 불가 항목

- Revenue·EBITDA·FCF 컨센서스 리비전: 데이터 소스 한계로 확인 불가. 회사 가이던스 상향 이력 [G]으로 보완했다.
- FY+3 컨센서스를 확보하지 못해 **3Y EPS CAGR과 PEG 3Y도 확인 불가**다.

### 점수 산정

- 13단계 배점(20/20/15/15/10/10/10)을 그대로 썼다.
- **Catalyst(10점)**
  - 7점은 정량: 최근 4분기 서프라이즈, 30일 상향·하향 애널리스트 수.
  - 3점은 뉴스·가이던스를 확인한 뒤 수동으로 줬다.
- **Risk(10점)**
  - 정량 감점: 순부채/EBITDA, SBC, 희석, FCF<0, 매출채권·재고 급증, Peak, Turnaround.
  - 여기에 수동 조정(−2~0)을 더했다. 대상은 고객 집중, 지정학, 소송, 단일 제품 LOE다.

---

## 2. False Positive 제거 (11단계)

### A. Cyclical Peak Trap: 순위에서 제외하고 별도 표시

| 기업 | 티커 | TTM P/E | FY+1 P/E | FY+2 P/E | EPS 2Y CAGR | FY+2 EPS ÷ 과거 4년 평균 EPS | 영업이익률 TTM vs 과거 평균 | 3M 주가 | 기계적 점수 |
|---|---|---|---|---|---|---|---|---|---|
| Western Digital | WDC | 46.5x | 23.6x | 14.9x | 76% | 5.3x | 36% vs 6% | −26% | 81.8 |
| Seagate | STX | 59.5x | 25.8x | 16.7x | 89% | 11.2x | 35% vs 9% | −11% | 79.8 |
| Sandisk | SNDK | 25.9x | 8.5x | 6.9x | 93% | 확인 불가 | 62% vs −7% | −5% | 79.3 |
| SK하이닉스 | 000660.KS | 8.2x | 5.3x | 3.9x | 180% | 24.0x | 68% vs 9% | −29% | 78.3 |
| 삼성전자 | 005930.KS | 12.6x | 5.9x | 4.0x | 228% | 13.1x | 37% vs 9% | −16% | 75.3 |
| Micron | MU | 23.8x | 14.6x | 6.7x | 338% | 59.5x | 66% vs 1% | +2% | 75.3 |

- 사이클 증거
  - 2026년 1분기 일반 DRAM 계약가격이 QoQ +93~98% 올랐다. 기록상 가장 빠른 상승이다.
  - 인텔 CEO는 메모리 가격이 5~7배 올랐다고 말했다.
- 전형적인 함정 조건
  - FY+2 EPS가 과거 4년 평균의 5~60배다.
  - 영업이익률이 과거 평균보다 30~60%p 높다.
  - 프롬프트가 경고한 "P/E 한 자릿수 + EPS 성장 100%+" 조합 그대로다.
- SK하이닉스는 "공급이 2030년까지 수요를 못 따라간다"고 주장한다. 그렇다 해도 Mid-cycle EPS를 추정할 수 없다는 사실은 달라지지 않는다. 정밀평가 전에 Normalized EPS를 따로 만들어야 한다.
- 같은 논리로 원자재 가격·업황이 EPS를 끌어올린 종목 29개도 제외했다: 금·은·구리 등 금속 광산주 25개, Century Aluminum(CENX), 기타 SEI·ALGT·RXO. 전체 목록은 CSV의 `peak` 열에 있다.

### B. 그 밖의 필터

- **Turnaround Illusion**: FY0 EPS ≤ 0 또는 FY+2/FY0 > 4배인 경우. EPS 점수 상한을 5/8로 두고 PEG·Expectation 점수는 60%만 인정했다. 예: KLIC, ARQT, TVTX.
- **일회성 저기저**
  - Halozyme(HALO)은 4Q25 조정 EPS가 −$0.24였다(IPR&D 비용). 그 때문에 2Y EPS CAGR이 58%로 부풀려져 보였다.
  - FY+2 성장률 21%로 정상화하자 75.5점으로 Top 20 밖으로 밀렸다.
  - 참고로 최근 +62%(3M) 급등은 Merck 피하주사 Keytruda 특허 분쟁과 관련된 이벤트성 움직임이다.
- **Buyback 효과**: 희석주식수가 연 4% 넘게 줄어든 기업은 따로 표시했다(DAVE, CXW, SEZL, RSI).
  - ENVA는 시총의 약 8%인 $349M ASR을 발표했다 [G].
  - 따라서 향후 EPS 성장 중 자사주 기여분은 분리해서 봐야 한다.
- **저품질 성장 감점**: FCF<0, 희석>5%, SBC>10%.
  - 예: COHR 희석 30%, LITE 전환사채로 희석 17.5%, CRDO SBC>10%에 내부자 매도.
- **AppLovin(APP)**: FY+2 P/E 15.8x·PEG 0.39로 숫자상은 싸다.
  - 그러나 Q2 매출이 컨센서스에 못 미쳤고, 'AI 모델 개선 속도 둔화'를 공시했다.
  - 증권 집단소송이 걸렸고 컨센서스도 하향 중이다(3M −5%).
  - 그래서 **Value Trap Candidate**로 분류했다.

---

## 3. Top 20

| 순위 | 기업 | 티커 | 유형 | Revenue Growth (2Y CAGR) [C] | EPS CAGR (2Y) [C] | FY+1 P/E | FY+2 P/E | PEG 2Y | ROIC [A] | Revision (상태, FY+2 EPS 3M) | 점수 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NVIDIA | NVDA | Earnings Revision Play / High-Growth at Fair Price | 78% | 81% | 24.2x | 14.4x | 0.21 | >100% | 5 (+23.7%) | 92.0 (S+) ★★ |
| 2 | Celestica | CLS | Earnings Revision Play / Growth Inflection | 69% | 79% | 32.2x | 18.7x | 0.27 | 46% | 5 (+33.8%) | 92.0 (S+) ★ |
| 3 | Asia Vital Components (AVC) | 3017.TW | Growth Inflection / Capex-to-FCF | 50% | 82% | 34.1x | 22.1x | 0.30 | >100% | 5 (+17.4%) | 90.5 (S+) |
| 4 | Ciena | CIEN | Earnings Revision Play / Growth Inflection | 33% | 97% | 49.7x | 34.8x | 0.37 | 20% | 5 (+28.4%) | 86.0 (S) |
| 5 | TSMC (ADR) | TSM | Quality Compounder / GARP | 39% | 43% | 26.4x | 20.4x | 0.50 | 61% | 5 (+11.5%) | 85.5 (S) |
| 6 | AMD | AMD | Earnings Revision Play / Momentum-supported Fundamental | 59% | 93% | 81.1x | 39.5x | 0.49 | 9%† | 5 (+18.3%) | 85.5 (S) |
| 7 | Fujikura | 5803.T | Growth Inflection | 27% | 55% | 25.3x | 21.8x | 0.43 | 36% | 5 (+46.7%) | 84.0 (A+) |
| 8 | Teradyne | TER | Earnings Revision Play | 40% | 72% | 42.8x | 33.4x | 0.50 | 44% | 5 (+23.0%) | 84.0 (A+) |
| 9 | Reddit | RDDT | High-Growth at Fair Price | 42% | 64% | 28.3x | 21.5x | 0.36 | >100% | 5 (+9.2%) | 83.5 (A+) |
| 10 | Onto Innovation | ONTO | Growth Inflection / Earnings Revision | 37% | 54% | 34.8x | 24.0x | 0.48 | 10%† | 5 (+21.7%) | 83.0 (A+) |
| 11 | Tower Semiconductor | TSEM | Growth Inflection / Capex-to-FCF | 32% | 70% | 59.4x | 34.7x | 0.56 | 10% | 5 (+15.8%) | 83.0 (A+) |
| 12 | Lumentum | LITE | Earnings Revision Play / Growth Inflection | 79% | 100% | 43.2x | 27.1x | 0.38 | 15% | 5 (+22.1%) | 82.5 (A+) |
| 13 | Advantest | 6857.T | Quality Compounder / Earnings Revision | 50% | 51% | 35.7x | 28.2x | 0.62 | 94% | 5 (+36.1%) | 82.5 (A+) |
| 14 | Flex | FLEX | GARP / Margin Expansion | 27% | 47% | 23.8x | 15.8x | 0.41 | 17% | 4 (+2.3%) | 82.5 (A+) ★ |
| 15 | Comfort Systems USA | FIX | Quality Compounder | 30% | 44% | 33.2x | 27.0x | 0.64 | 93% | 5 (+13.1%) | 82.5 (A+) |
| 16 | Enova International | ENVA | GARP / Earnings Revision | 20% | 27% | 9.7x | 8.0x | 0.31 | ROE 26% | 5 (+7.3%) | 82.0 (A+) |
| 17 | Applied Materials | AMAT | Cyclical Recovery / GARP | 28% | 40% | 37.1x | 25.7x | 0.66 | 35% | 5 (+13.2%) | 82.0 (A+) |
| 18 | Eli Lilly | LLY | Quality Compounder | 25% | 40% | 31.2x | 24.2x | 0.64 | 47% | 4 (+6.9%) | 81.5 (A+) |
| 19 | MKS Instruments | MKSI | GARP / Deleveraging | 25% | 50% | 20.0x | 14.9x | 0.32 | 10%† | 5 (+18.1%) | 81.0 (A+) ★★(조건부) |
| 20 | Tokyo Electron | 8035.T | Cyclical Recovery / Earnings Revision | 38% | 38% | 31.8x | 22.7x | 0.70 | 33% | 5 (+20.2%) | 81.0 (A+) |

표 읽는 법:

- † 인수 영업권이 포함된 GAAP 기준이라 과소 측정됨.
- 동점은 Valuation 점수 + Revision 점수로 순서를 정했다.
- TSM은 ADR 기준 FY+2 P/E가 20.4x라 ★ 조건(20x 미만)에 조금 못 미친다. 대만 본주(2330.TW) 기준으로는 17.3x라 충족한다.

---

## 4. Top 10: 투자 Thesis / 시장이 놓치고 있는 것 / Catalyst / 주요 위험

**1. NVIDIA (NVDA)**

- **Thesis**
  - Q2 FY27 실적 [A]: 매출 $96.2B(+106%), DC $89.0B(+117%), GM 75%.
  - Q3 가이던스 [G]: $108B.
  - **FY28 매출 +70%** 가이던스 [G]. 애널리스트 예상은 +44~45%였다.
  - 이후 FY+2 EPS 컨센서스가 1개월 만에 +21.7% 올랐다 [C]. 같은 기간 주가는 +8.3%였다.
- **시장이 놓치고 있는 것**
  - 주가가 요구하는 4년 EPS CAGR은 11.5% [I]에 불과하다. 사실상 FY28 이후 AI capex가 급감한다고 가정하는 셈이다.
  - 하이퍼스케일 밖 수요도 커지고 있다. AI Clouds·Industrial·Enterprise 매출이 $40.3B로 DC의 45%다 [A].
  - Rubin 램프도 남아 있다.
- **Catalyst**: 11월 중순 Q3 FY27 실적과 Q4 가이던스, Vera Rubin 양산 출하.
- **위험**
  - 하이퍼스케일러 capex 조정.
  - 커스텀 ASIC(TPU·Trainium·AVGO)과 AMD MI450에 점유율을 잠식당할 가능성.
  - 중국 DC 매출은 0으로 가정돼 있다.
  - 매출채권 증가 속도.

**2. Celestica (CLS)**

- **Thesis**
  - Q2 실적 [A]: 매출 $4.70B(+62%), 조정 EPS $2.54.
  - 2026 가이던스를 매출 $20.5B(+65%), EPS $11.30(+87%)로 상향 [G].
  - **2027 매출 성장은 2026보다 가속하고, EPS는 매출보다 빠르게 성장** [G].
  - FY+2 EPS는 3개월 +33.8%인데 주가는 +3% [C].
- **시장이 놓치고 있는 것**
  - 시장은 여전히 EMS 멀티플로 본다. 실제 ROIC는 46%, RONIC는 178%로 설계형 AI 랙·1.6T 스위치(HPS) 쪽으로 믹스가 바뀌었다.
  - OpenAI, AMD Helios, 1.6T 네트워킹 신규 프로그램이 있다 [G].
- **Catalyst**: **10/27 Investor Day**(2027 목표 첫 제시), 10월 말 Q3 실적.
- **위험**
  - 소수 하이퍼스케일러에 고객이 집중돼 있다.
  - FCF 마진이 3%대다(2026 FCF 가이던스 $600M) [G].
  - FY+2 추정치를 낸 애널리스트가 9명뿐이라 신뢰도가 낮다.

**3. Asia Vital Components (3017.TW)**

- **Thesis**
  - Q2 실적 [A]: 매출 NT$49.1B(+66%), GM 32.6%(+8.2%p), EPS NT$24.37(+137%).
  - 액냉 모듈 캐파를 월 20만 → 100만 유닛으로 증설한다 [G].
- **시장이 놓치고 있는 것**
  - 부품사에서 콜드플레이트·매니폴드·CDU를 묶은 토털 열관리 솔루션 업체로 바뀌면서 GM이 구조적으로 오르고 있다.
  - FCF 마진이 6.8% → 24.1%로 좋아졌다 [A]. 순현금 상태다.
- **Catalyst**: 매월 10일 전후 월매출 발표, Rubin 세대에서 액냉 전면 채택, 11월 Q3 실적.
- **위험**
  - 3개월 주가 +54%가 FY+2 리비전 +17%보다 앞서갔다. 진입가가 부담이다.
  - 경쟁자: Auras, Cooler Master, Vertiv/CoolIT.
  - NVIDIA 생태계 의존도가 높다.

**4. Ciena (CIEN)**

- **Thesis**
  - FQ3 실적 [A]: 매출 $1.67B(+37%), 조정 EPS $2.11(+215%).
  - FY26 매출 가이던스를 $6.42B로 상향 [G].
  - **FY27 매출 ≥ +30%($8.3~8.4B), OPM 25~27%** [G].
  - 백로그 $8.5B [A], FY말 > $10B 예상 [G].
- **시장이 놓치고 있는 것**
  - 가이던스 중간값을 산식에 넣으면 FY27 EPS가 약 **$12** [M]다. 세율 18%, 희석주식 1.45억주를 가정했다.
  - FY+2 컨센서스 $10.24 [C]는 추정 애널리스트가 7명뿐이고, 가이던스 산식 EPS보다 약 17% 낮다.
  - 그런데도 FY+2 EPS가 3개월 +28% 오르는 동안 주가는 **−23%** 빠졌다.
- **Catalyst**: 12월 초 FQ4 실적과 FY27 공식 가이던스, CPO(Vesta) 2027년 매출 기여 시작.
- **위험**
  - 부품 부족에 따른 마진 압박.
  - 광 관련 트레이드 쏠림이 풀리며 나오는 매물.
  - TTM P/E 59x로 절대가치가 비싸다.

**5. TSMC (TSM)**

- **Thesis**
  - 2026 매출 성장 가이던스를 >30% → **40%+**로 올렸다 [G].
  - 8월 매출 NT$514.9B(+53% YoY)로 4개월 연속 사상 최대 [A].
  - 3Q 가이던스 [G]: $44.6~45.8B.
- **시장이 놓치고 있는 것**
  - ROIC 61%, 순현금, FCF 마진 25%인데 주가 내재 성장률은 19% [I]다.
  - N2/A16과 CoWoS를 사실상 독점하고 가격 인상력도 있다. 그러니 2027~28년에도 20%대 성장을 이어갈 가능성이 크다.
- **Catalyst**: 10월 중순 3Q 실적과 4Q 가이던스, 10일경 월매출 발표, 2027 가격 인상.
- **위험**
  - 대만 지정학 리스크.
  - capex가 $60~64B로 늘어나 FCF 마진이 29.8%에서 25.3%로 낮아졌다 [A].
  - 해외 팹의 마진 희석, 환율.

**6. AMD (AMD)**

- **Thesis**
  - GW급 MI450 계약이 잇따랐다: OpenAI 6GW, Meta 6GW, Anthropic 2GW, Oracle 5만 개.
  - 2027년 DC 매출이 2배 넘게 늘 것이라고 가이드 [G].
  - FY+2 EPS +105% [C].
- **시장이 놓치고 있는 것**
  - 경영진은 "EPS $20 목표를 전략 기간 내 크게 상회"한다고 말한다. FY27 컨센서스 $15.6과 차이가 있다.
- **Catalyst**: 11월 초 Q3 실적, MI450 램프(2H26~2027).
- **위험**
  - 올해 주가가 +183%다. 주가가 요구하는 성장이 이미 43% [I]로 기대가 상당히 선반영돼 있다.
  - FY+2 P/E 39.5x.
  - 고객 쪽 자금조달 구조(워런트, 오프테이크).

**7. Fujikura (5803.T)**

- **Thesis**
  - FY3/27 가이던스를 두 번(6월, 8월) 올렸다 [G]: 매출 ¥1.755T(+48%), 영업이익 ¥432B(+129%), 순이익 ¥326B(+107%).
  - 광섬유 캐파를 3배로 늘린다(최대 ¥300B 투자) [G].
- **시장이 놓치고 있는 것**
  - 데이터센터 케이블 가격 인상.
  - 미국 외 지역의 대형 광부품 수주.
- **Catalyst**: 11월 상반기 실적과 추가 상향 여부.
- **위험**
  - **FY+2 성장률이 16%** [C]로 꺾인다. Forward PEG 1.45로, 2Y CAGR이 FY+1에 쏠려 있다.
  - 5월 고점 대비 −40%.
  - 캐파 병목.

**8. Teradyne (TER)**

- **Thesis**
  - Q2 실적 [A]: 매출 $1.33B(+104%), 반도체 테스트 +128%, 메모리 테스트 3분기 연속 $200M 이상.
  - FY+2 EPS 3개월 +23% [C].
- **시장이 놓치고 있는 것**: AI 컴퓨트와 HBM 테스트는 테스트 강도가 구조적으로 올라가는 추세다.
- **Catalyst**: 10월 말 Q3 실적과 2027 전망.
- **위험**: Q3 가이던스가 전분기보다 낮다(중간값 $1.25B) [G]. FY+2 P/E 33x로, 기대가 상당히 선반영됐다.

**9. Reddit (RDDT)**

- **Thesis**
  - Q2 실적 [A]: 매출 $805M(+61%), 순이익률 31%, FCF $261M.
  - Q3 가이던스 [G]: 매출 +47~49%, EBITDA 마진 45%.
- **시장이 놓치고 있는 것**
  - 구글 유입 트래픽 우려로 FY+2 P/E가 21.5x까지 내려왔다.
  - 그러나 AI 시대 '인간 생성 데이터' 라이선스 가치, 해외 확장, 광고 ARPU 상승 여지가 크다. ROIC는 100%를 넘고 순현금이다.
- **Catalyst**: 10월 말 Q3 실적, 데이터 라이선스 갱신·확대.
- **위험**: 구글 검색 유입 변동성, SBC/매출 12%, 사용자 성장 둔화.

**10. Onto Innovation (ONTO)**

- **Thesis**
  - Q2 매출 $343M로 사상 최대, 가이던스 상단 초과 [A].
  - 어드밴스드 패키징 성장 전망을 50% → **80%**로 상향 [G].
  - 하반기 매출이 상반기보다 +25% 이상 늘 것으로 가이드 [G]. 백로그 > $1.1B [A].
- **시장이 놓치고 있는 것**
  - HBM·2.5D·실리콘 포토닉스 계측 수요는 구조적이다.
  - 그런데도 장비주 동반 매도에 휩쓸려 주가 −11%(3M). 같은 기간 FY+2 EPS는 +22%였다.
- **Catalyst**: 11월 초 Q3 실적(가이던스 $380~400M), 연말 OPM 33% 이상.
- **위험**: 장비 capex 속도 조절 우려, 고객 집중.

---

## 5. Top 5 상세 (34개 항목)

| # | 항목 | NVDA | CLS | AVC (3017.TW) | CIEN | TSM (ADR) |
|---|---|---|---|---|---|---|
| 1 | 기업명 / 티커 | NVIDIA / NVDA | Celestica / CLS | Asia Vital Components / 3017.TW | Ciena / CIEN | TSMC / TSM |
| 2 | 현재가 (9/23) | $225.51 | $361.84 | NT$3,530 | $355.91 | $446.57 |
| 3 | 시가총액 | $5.45T | $45.6B | $43.6B | $50.5B | $2.32T |
| 4 | 사업 유형 | AI 가속 컴퓨팅 플랫폼(GPU·네트워킹·시스템), fabless | EMS/ODM: AI 랙·스위치(HPS) 중심 CCS + ATS | 열관리 부품·액냉 솔루션(콜드플레이트·매니폴드·CDU) | 광전송(WaveLogic)·광모듈·라우팅 | 선단 파운드리 + CoWoS 패키징 |
| 5 | 핵심 사업 변화 | Blackwell Ultra에서 Rubin으로 전환, 비하이퍼스케일 비중 45%, FY28 매출 +70% [G] | 2026 +65% 성장 뒤 2027 가속 [G], OpenAI·AMD Helios·1.6T 신규 프로그램 | 공랭에서 액냉으로 전환, GM +8.2%p, 캐파 5배 | DCI·데이터센터 내부 광 확장, 백로그 $8.5B, CPO 2027 | 2026 성장 가이던스 40%+로 상향, capex $60~64B |
| 6 | NTM Revenue Growth [C/A] | +95% | +100% | +56% | +36% | +53% |
| 7 | 2Y Revenue CAGR [C] | 78% | 69% | 50% | 33% | 39% |
| 8 | FY+1 EPS Growth [C] | +95% | +86% | +114% | +171% (저기저) | +59% |
| 9 | 2Y EPS CAGR [C] | 81% | 79% | 82% | 97% | 43% |
| 10 | 3Y EPS CAGR | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 | 확인 불가 |
| 11 | NTM P/E | 16.7x | 21.1x | 24.4x | 35.9x | 21.7x |
| 12 | FY+1 P/E | 24.2x | 32.2x | 34.1x | 49.7x | 26.4x |
| 13 | FY+2 P/E | 14.4x | 18.7x | 22.1x | 34.8x (가이던스 산식 기준 약 30x [M]) | 20.4x (본주 17.3x) |
| 14 | PEG 1Y | 0.18 | 0.25 | 0.21 | 0.21 (저기저로 왜곡) | 0.37 |
| 15 | PEG 2Y | 0.21 | 0.27 | 0.30 | 0.37 (Forward PEG 0.84) | 0.50 |
| 16 | FY+2 P/E Compression | −55% | −58% | −53% | −41% | −37% |
| 17 | ROIC [A] | 132% | 46% | >100% (순현금으로 IC가 작음, ROE 67%) | 20% | 61% |
| 18 | RONIC [A] | 333% | 178% | 204% | n/m (FY24 NOPAT 감소) | 140% |
| 19 | FCF Margin (TTM) [A] | 41.9% | 3.3% | 24.1% | 13.5% | 25.3% |
| 20 | Net Debt / EBITDA [A] | −0.1x (순현금) | 0.3x | −1.0x (순현금) | 0.6x | −0.8x (순현금) |
| 21 | 1M Revision (FY+1 / FY+2 EPS) [C] | +3.6% / **+21.7%** | −0.1% / **+30.2%** | +4.6% / +5.9% | +9.5% / **+26.6%** | +0.2% / +0.7% |
| 22 | 3M Revision (FY+1 / FY+2 EPS) [C] | +4.3% / +23.7% | +9.1% / +33.8% | +9.4% / +17.4% | +9.6% / +28.4% | +7.4% / +11.5% |
| 21·22 | 매출 컨센서스 리비전 | 확인 불가 (FY28 +70% 가이던스 [G]) | 확인 불가 (2026 매출 가이던스 상향 [G]) | 확인 불가 | 확인 불가 (FY26 매출 가이던스 상향 [G]) | 확인 불가 (2026 성장 가이던스 상향 [G]) |
| — | 주가 1M / 3M | +8% / +13% | +22% / +3% | +12% / +54% | −10% / −23% | +9% / +2% |
| 23 | 가장 중요한 Catalyst | 11월 Q3 FY27 실적·Rubin 출하 | **10/27 Investor Day** (2027 목표) | 월매출·Rubin 액냉 채택 | 12월 FQ4 실적·FY27 공식 가이던스 | 10월 중순 3Q 실적·월매출 |
| 24 | 가장 중요한 Risk | AI capex 지속기간, ASIC 점유율 | 고객 집중·저FCF | 주가가 리비전을 앞서감, 경쟁 | 부품 부족·마진, 절대 밸류 | 지정학·capex 증가 |
| 25 | 시장이 놓치고 있는 것 | FY29 이후 성장 지속(비하이퍼스케일 수요) | 설계형 믹스로 ROIC 46% 체질 전환 | 액냉 토털 솔루션화로 GM 구조적 상승 | 가이던스 산식 EPS가 컨센서스보다 약 17% 높음 | 2027~28 가격 인상·N2 독점 지속 |
| 26 | 현재 주가가 요구하는 성장 [I] | 4Y EPS CAGR 11.5% | 18.2% | 22.6% | 35.1% | 19.1% |
| 27 | Consensus 예상 성장 [C] | 2Y 81% (FY+2 +69%) | 79% (+73%) | 82% (+55%) | 97% (+43%) | 43% (+30%) |
| 28 | Expectation Gap (2Y 기준 / FY+2 기준) | +70%p / +57%p | +61%p / +55%p | +59%p / +32%p | +62%p / +8%p | +24%p / +10%p |
| 29 | 12개월 EPS × P/E 예상가 [M] (NTM P/E 고정) | $313.5 | $497.7 | NT$4,758 | $466.1 | $547.5 |
| 30 | Potential Upside [M] / 컨센서스 평균 목표가 [C] | +39% / +45% ($327.7) | +38% / +30% ($471.2) | +35% / +16% (NT$4,099) | +31% / +45% ($516.8) | +24% / +24% ($552.3) |
| 31 | Bear Downside [M] / 최저 목표가 [C] | −28% ($163: FY+2 EPS −20%, 13x) / −20% ($180) | −36% ($232: −20%, 15x) / +4% ($375) | −35% (NT$2,302: −20%, 18x) / −6% | −32% ($244: −15%, 28x) / −3% ($347) | −25% ($336: −10%, 17x) / −1.5% ($440) |
| 32 | Risk / Reward (Upside ÷ Bear [M]) | **1.43** | 1.05 | 1.01 | 0.98 | 0.94 |
| 33 | 총점 | 92.0 (S+) | 92.0 (S+) | 90.5 (S+) | 86.0 (S) | 85.5 (S) |
| 34 | 투자 유형 | Earnings Revision Play / High-Growth at Fair Price | Earnings Revision Play / Growth Inflection | Growth Inflection / Capex-to-FCF | Earnings Revision Play / Growth Inflection | Quality Compounder / GARP |

**Risk/Reward 해석**

- Bear 시나리오는 이익 하향과 디레이팅이 **동시에** 온다고 가정했다. 그래서 R/R이 1 안팎으로 나온다.
- 비대칭성은 R/R 숫자보다 다른 곳에서 나온다.
  - 리비전이 상향 중이다(→ Base 시나리오 확률이 더 높다).
  - 컨센서스가 주가 내재 기대보다 한참 높다.
- 멀티플이 가장 낮은 NVDA만 R/R 1.4로 뚜렷하게 비대칭이다.
- CLS·AVC·CIEN·TSM은 **진입가 관리**가 수익률을 좌우한다.

---

## 6. 최종 Ranking (16단계)

| 순위 | 기업 | 총점 | Growth (20) | Valuation (20) | Revision (15) | Quality (15) | Expectation Gap (10) | Catalyst (10) | Risk (10) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | NVIDIA (NVDA) | **92.0** | 16.0 | 19.5 | 14.5 | 14.0 | 10.0 | 10.0 | 8.0 |
| 2 | Celestica (CLS) | **92.0** | 18.0 | 18.5 | 15.0 | 12.5 | 10.0 | 10.0 | 8.0 |
| 3 | AVC (3017.TW) | **90.5** | 17.0 | 17.0 | 14.0 | 15.0 | 10.0 | 8.5 | 9.0 |
| 4 | Ciena (CIEN) | **86.0** | 18.0 | 13.5 | 15.0 | 9.5 | 10.0 | 10.0 | 10.0 |
| 5 | TSMC (TSM) | **85.5** | 17.0 | 16.5 | 13.0 | 14.0 | 8.5 | 9.5 | 7.0 |
| 6 | AMD (AMD) | **85.5** | 20.0 | 13.5 | 13.5 | 9.5 | 10.0 | 10.0 | 9.0 |
| 7 | Fujikura (5803.T) | **84.0** | 15.5 | 16.0 | 15.0 | 11.0 | 10.0 | 7.5 | 9.0 |
| 8 | Teradyne (TER) | **84.0** | 17.0 | 12.5 | 14.0 | 14.0 | 10.0 | 8.5 | 8.0 |
| 9 | Reddit (RDDT) | **83.5** | 16.0 | 15.5 | 13.0 | 12.5 | 10.0 | 9.0 | 7.5 |
| 10 | Onto Innovation (ONTO) | **83.0** | 17.0 | 15.0 | 14.0 | 11.0 | 8.5 | 8.5 | 9.0 |
| 11 | Tower Semiconductor (TSEM) | **83.0** | 20.0 | 13.5 | 14.5 | 6.0 | 10.0 | 10.0 | 9.0 |
| 12 | Lumentum (LITE) | **82.5** | 17.0 | 14.5 | 14.5 | 9.5 | 10.0 | 10.0 | 7.0 |
| 13 | Advantest (6857.T) | **82.5** | 16.0 | 14.0 | 15.0 | 11.0 | 8.5 | 9.0 | 9.0 |
| 14 | Flex (FLEX) | **82.5** | 18.5 | 18.0 | 9.5 | 8.5 | 10.0 | 9.0 | 9.0 |
| 15 | Comfort Systems (FIX) | **82.5** | 17.0 | 12.5 | 12.0 | 14.5 | 7.0 | 9.5 | 10.0 |
| 16 | Enova (ENVA) | **82.0** | 14.0 | 16.5 | 13.0 | 10.5 | 10.0 | 9.0 | 9.0 |
| 17 | Applied Materials (AMAT) | **82.0** | 18.5 | 12.5 | 12.5 | 13.5 | 7.0 | 9.0 | 9.0 |
| 18 | Eli Lilly (LLY) | **81.5** | 15.5 | 13.5 | 11.5 | 14.5 | 7.0 | 9.5 | 10.0 |
| 19 | MKS Instruments (MKSI) | **81.0** | 15.5 | 18.5 | 14.0 | 8.5 | 10.0 | 8.5 | 6.0 |
| 20 | Tokyo Electron (8035.T) | **81.0** | 18.0 | 14.5 | 15.0 | 11.0 | 7.0 | 6.5 | 9.0 |

### "왜 지금 조사해야 하는가?" 한 줄 답

1. **NVDA**: FY28 +70% 가이던스로 FY+2 EPS는 1개월 +22% 올랐는데 주가는 +8%. 시총 1위가 FY+2 14x에 거래된다.
2. **CLS**: FY+2 EPS +34% vs 주가 +3%. 10/27 Investor Day에서 2027 목표가 처음 나온다.
3. **AVC**: 액냉 전환의 최대 수혜주이고 캐파를 5배로 늘린다. 다만 주가(+54%)가 리비전(+17%)을 앞서 진입가 판단이 핵심이다.
4. **CIEN**: 가이던스 산식 EPS(~$12)가 컨센서스($10.24)보다 높은데 주가는 −23%. 리비전과 주가 사이 괴리가 가장 크다.
5. **TSM**: 2026 성장 가이던스를 40%+로 올렸고, ROIC 61%·순현금에 FY+2 20x다. 품질 대비 가장 싼 초대형주다.
6. **AMD**: GW급 MI450 계약으로 FY+2 EPS +105%. 다만 YTD +183%라 기대가 상당히 선반영돼 있다.
7. **Fujikura**: 두 차례 가이던스를 올렸는데도 고점 대비 −40%. 다만 FY+2 성장은 16%로 꺾인다.
8. **TER**: AI·HBM 테스트로 매출 +104%. Q3 순차 감소 가이던스로 '감속인가, 구조적 강도인가' 논쟁이 붙은 구간이다.
9. **RDDT**: 매출 +61%·FCF 마진 37%인데 FY+2 21.5x. AI 하드웨어 밖에서 고른 분산 후보다.
10. **ONTO**: 패키징 성장 전망을 80%로 올렸고 백로그 $1.1B+인데 장비주 동반 매도로 −11%.
11. **TSEM**: SiPho 매출 +270% YoY, 연말 $1B 런레이트, 2028 모델 매출 $3.6B·영업이익 $1.38B [G].
12. **LITE**: TTM P/E 112x가 FY+2 27x로 압축된다. CPO 대형 수주와 OCS 백로그 > $400M. 전환사채 희석(+17.5%)은 점검이 필요하다.
13. **Advantest**: FY+2 EPS +36%(3M), ROIC 94%의 테스트 과점 기업. FY+2 성장 27% 대비 28x는 부담이다.
14. **FLEX**: FY+2 15.8x에 EPS 2Y CAGR 47%, 최저 목표가도 현재가보다 +26% 높다. Cloud & Power 분사가 재평가 트리거다.
15. **FIX**: 백로그 $14.1B(+73%), ROIC 93%, 순현금 $1.8B. 품질은 최상위지만 FY+2 성장 23% 대비 27x다.
16. **ENVA**: 은행 인수 철회로 1개월 −31%. 가이던스는 유지했고 시총 8% 규모 ASR까지 발표했다. FY+2 8x에 주가 내재 성장률은 마이너스다.
17. **AMAT**: 2027 WFE $190B+ 전망 속에 FY+2 EPS +13%, 주가 −19%. 장비 사이클 재가속에 거는 베팅이다.
18. **LLY**: ROIC 47%, FCF 마진 1%에서 17%로 전환. 비AI 품질 컴파운더다.
19. **MKSI**: FY+2 14.9x·PEG 0.32로 장비주 중 가장 싸다. 다만 순부채/EBITDA 3.4x라 디레버리징 확인이 먼저다.
20. **Tokyo Electron**: FY+2 EPS +20% vs 주가 −30%(3M). 리비전과 주가 사이 괴리가 큰 장비 대형주다.

---

## 7. 최종 판정 (17단계)

| 순위 | 기업 | Absolute Valuation | Growth-Adjusted Valuation | Market Expectations |
|---|---|---|---|---|
| 1 | NVDA | 쌈 (FY+2 14.4x) | 성장 대비 매우 저평가 | **지나치게 낮음** (내재 11.5% vs 컨센서스 FY+2 +69%) |
| 2 | CLS | 적정 (18.7x) | 성장 대비 매우 저평가 | **지나치게 낮음** (18% vs +73%) |
| 3 | AVC | 적정 (22.1x) | 성장 대비 매우 저평가 | 실적이 주가를 따라잡는 중 (3M +54%) |
| 4 | CIEN | 비쌈 (34.8x, TTM 59x) | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 (TTM 59x → FY+2 35x) |
| 5 | TSM | 적정 (20.4x) | 성장 대비 매력적 | 적절 (다소 낮음, 19% vs +30%) |
| 6 | AMD | 매우 비쌈 (39.5x) | 성장 대비 매력적 | 상당히 선반영 (내재 43%) |
| 7 | Fujikura | 적정 (21.8x) | 성장 대비 적정 (Forward PEG 1.45) | 상당히 선반영 (21% vs FY+2 +16%) |
| 8 | TER | 비쌈 (33.4x) | 성장 대비 적정 | 상당히 선반영 (35% vs +28%) |
| 9 | RDDT | 적정 (21.5x) | 성장 대비 매력적 | 적절 (21% vs +31%) |
| 10 | ONTO | 비쌈 (24.0x) | 성장 대비 매력적 | 적절 |
| 11 | TSEM | 비쌈 (34.7x) | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 |
| 12 | LITE | 비쌈 (27.1x) | 성장 대비 매력적 | 실적이 주가를 따라잡는 중 (12M +513%) |
| 13 | Advantest | 비쌈 (28.2x) | 성장 대비 적정 | 상당히 선반영 |
| 14 | FLEX | 적정 (15.8x) | 성장 대비 매우 저평가 | 지나치게 낮음 |
| 15 | FIX | 비쌈 (27.0x) | 성장 대비 적정 | 상당히 선반영 (27% vs +23%) |
| 16 | ENVA | 매우 쌈 (8.0x) | 성장 대비 매우 저평가 | **지나치게 낮음** (내재 성장 −6%) |
| 17 | AMAT | 비쌈 (25.7x) | 성장 대비 매력적 | 적절 |
| 18 | LLY | 비쌈 (24.2x) | 성장 대비 매력적 | 적절 |
| 19 | MKSI | 쌈 (14.9x) | 성장 대비 매우 저평가 | 지나치게 낮음 (레버리지 할인) |
| 20 | Tokyo Electron | 적정 (22.7x) | 성장 대비 매력적 | 적절 |

판정 기준:

- **Absolute**: FY+2 P/E 기준. 10x 미만 매우 쌈, 10~15x 쌈, 15~23x 적정, 23~35x 비쌈, 35x 초과 매우 비쌈.
- **Growth-Adjusted**: (PEG 2Y + Forward PEG) ÷ 2 기준. 0.4 미만 매우 저평가, 0.4~0.8 매력적, 0.8~1.2 적정, 1.2~2.0 비쌈.
- **Market Expectations**: 주가 내재 4년 성장률 [I]을 FY+2 컨센서스 성장률과 비교하고, 주가 경로를 보고 판단했다.

---

## 8. Alpha Candidate (14단계)

- **★★ Exceptional Growth-Adjusted Candidate**: EPS CAGR > 30%, FY+2 P/E < 15x, Revision이 상향이고 ★ 조건도 모두 충족.
  - **NVDA**
  - **NU (Nu Holdings)**: FY+2 12.4x, EPS CAGR 37%, ROE 32%, 77.5점. AI 하드웨어가 아닌 ★★다.
  - AAMI, TIGO: TIGO는 순부채/EBITDA > 2.5x 주의.
- **★ Alpha Candidate**: CLS, FLEX, AEIS, TTMI, MTZ, SEZL.
- **★★ 조건부**: ★★ 3조건은 맞췄지만 품질·재무 조건이 미달한 경우.

| 종목 | 미달 사유 |
|---|---|
| MKSI | ROIC 10%, 레버리지 3.4x |
| HRMY | 단일 제품 LOE 위험 |
| NESR | 사이클·턴어라운드 |
| Wiwynn | FCF<0, 재고 급증 |
| HD현대중공업 | 조선 사이클, 합병 희석 |
| Quanta Computer | FCF<0 |

- **Peak-trap이라 ★★에서 제외**: MU, SK하이닉스, 삼성전자, SNDK, WDC, STX.
- **Top 20 밖이지만 주목할 종목: AVGO (73.0점)**
  - FY+2 P/E 18.3x, PEG 0.28, EPS 2Y CAGR 69% [C].
  - FY27 AI 매출 $115B, **FY28 $230B 윤곽**을 제시했다 [G].
  - 그런데도 FY+2 컨센서스는 정체다(3M −0.4%). 그래서 Revision 점수가 낮았다.
  - 컨센서스가 가이던스를 반영하기 시작하면 바로 상위권에 들어올 후보다.

---

## 9. Deep Dive 후보 (18단계)

**★★★ 즉시 정밀분석 추천**
1. **NVIDIA (NVDA)**
2. **Celestica (CLS)**
3. **Ciena (CIEN)**

**★★ 높은 관심**
4. TSMC (TSM)
5. Asia Vital Components (3017.TW)
6. Reddit (RDDT)
7. AMD (AMD)

**★ Watchlist**
8. Tower Semiconductor (TSEM)
9. Onto Innovation (ONTO)
10. Enova International (ENVA)

Deep Dive 순서는 총점에 Risk/Reward·진입가 판단을 더해 정했다.

- AVC는 총점 3위지만 최근 3개월 +54%로 주가가 리비전을 앞섰다. 그래서 ★★로 조정했다.
- Fujikura·TER은 FY+2 성장이 둔화되고 기대가 선반영돼 있어 Deep Dive에서 뺐다.
- RDDT·ENVA는 AI 하드웨어 집중을 분산하려고 넣었다.

### 왜 이 기업을 지금 전체 기업가치평가 프롬프트에 넣어야 하는가?

**NVDA**

1. FY+2 EPS 컨센서스가 1개월 만에 +22% 올라 FY+2 P/E 14.4x, PEG 0.21이 됐다. 대형주 중 성장 대비 가장 싸다.
2. 주가 내재 4년 EPS CAGR은 11.5% [I]다. FY28 매출 +70% 가이던스 [G]와의 격차가 전체 유니버스에서 가장 크다.
3. 결국 가치는 'FY29 이후 AI capex 지속기간' 한 변수에 달렸다. 이 변수는 Forward DCF와 Reverse DCF의 terminal 가정으로 바로 연결된다.
4. ROIC 100% 이상, FCF 마진 42%, 순현금이라 정상화 이익과 RONIC 가정을 검증하기 쉽다.
5. 그래서 FY29 capex −30%/0%/+30% 시나리오별 가치 민감도를 정량화할 가치가 가장 크다.

**CLS**

1. FY+2 EPS가 3개월 +34% 올랐지만 주가는 +3%라, 현재가 기준 P/E가 58% 압축된다.
2. 회사는 이미 2027 성장 가속과 매출보다 빠른 EPS 성장을 가이드했다 [G]. 10/27 Investor Day가 컨센서스를 다시 맞추는 이벤트다.
3. 반면 FCF 마진이 3%이고 고객이 몰려 있어, 정상화 선행 실적과 운전자본 가정이 가치를 좌우한다.
4. ROIC 46%, RONIC 178%의 믹스 개선이 이어질지는 정밀 모델로만 판별할 수 있다.
5. Reverse DCF로 시장 내재 기대(18%)와 가이던스 경로의 차이를 숫자로 확인해야 한다.

**CIEN**

1. FY27 가이던스(매출 $8.3~8.4B, OPM 25~27%)로 산출한 EPS는 약 $12 [M]다. 7명이 낸 FY+2 컨센서스 $10.24 [C]보다 약 17% 높다.
2. FY+2 EPS가 3개월 +28% 오르는 동안 주가는 −23%였다. 리비전과 주가의 괴리가 대형 성장주 중 가장 크다.
3. 백로그 $8.5B는 FY말 $10B+ [G]로 늘어날 전망이고, FY27 매출의 120% 이상을 덮는다. 이익 가시성이 높다.
4. 다만 TTM P/E 59x로 절대가치가 비싸다. CPO(Vesta) 램프와 부품 부족에 따른 마진 경로를 DCF로 검증해야 한다.
5. 이익 추정치는 오르는데 가격은 반대로 가는, 전형적인 'Earnings Growth에 따른 Valuation Compression' 케이스다.

---

## 10. 최종 질문 8개에 대한 답

**1. 지금 시장에서 Growth-Adjusted Valuation이 가장 좋은 기업은?**

- **NVIDIA**: PEG 2Y 0.21, FY+2 P/E 14.4x, EPS 2Y CAGR 81%, ROIC 100% 이상.
- 차순위
  - Celestica (0.27)
  - AVC (0.30)
  - Enova (0.31, FY+2 8x, 비AI)
  - MKS (0.32, 레버리지 주의)
- 순위 밖 참고: AVGO (0.28, 리비전 정체).

**2. 현재 P/E는 높지만 향후 EPS 성장 때문에 실제로는 싼 기업은?**

| 종목 | TTM P/E | FY+2 P/E | PEG 2Y | 비고 |
|---|---|---|---|---|
| Lumentum | 112x | 27x | 0.38 | |
| AMD | 107x | 39x | 0.49 | |
| Tower | 81x | 35x | 0.56 | |
| **Ciena** | 59x | 35x | 0.37 | 가이던스 산식 기준 약 30x |
| **Celestica** | 44x | 18.7x | 0.27 | |

- 가치 스크리너라면 모두 탈락했을 종목이다.

**3. 주가가 유지되기만 해도 FY+2 P/E가 가장 빠르게 낮아지는 기업은?**

- Peak-trap 제외 기준: **Lumentum −76%**, AMD −63%, Semtech −63%, BESI −60%, Coherent −60%, **Celestica −58%**, Tower −57%, **NVIDIA −55%**.
- 메모리 SNDK −73%, MU −72%, WDC −68%은 Peak-trap이라 제외했다.

**4. 최근 Earnings Revision이 가장 강하면서 아직 주가가 충분히 반응하지 않은 기업은?**

| 종목 | FY+2 EPS 3M | 주가 3M | 비고 |
|---|---|---|---|
| **Ciena** | +28.4% | −22.6% | 1M 기준 +26.6% vs −10.1% |
| **Celestica** | +33.8% | +3.0% | |
| Fujikura | +46.7% | −19.4% | |
| Tokyo Electron | +20.2% | −30.1% | |
| MKS | +18.1% | −32.4% | |
| Advanced Energy | +30.2% | −23.4% | |
| TTM Technologies | +27.6% | −41.0% | |

- 점수와 품질까지 감안하면 **CIEN과 CLS가 1순위**다.

**5. EPS뿐 아니라 FCF와 ROIC까지 함께 개선되는 기업은?**

| 종목 | ROIC 추이 | FCF 마진 | EPS 2Y CAGR |
|---|---|---|---|
| **Comfort Systems** | 28→51→73→93% | 10.5→19.2% | 44% |
| **AVC** | 52→56→113%+ | 6.8→24.1% | 82% |
| **Eli Lilly** | 29→35→45→47% | 0.9→17.0% | 40% |
| Vertiv | 16→25→32→38% | 14.2→25.5% | 47% |
| Celestica | 15→24→39→46% | 3%대로 낮지만 소폭 개선 | |

- NVDA와 TSM은 수준은 최상위다. 다만 NVDA는 ROIC와 FCF 마진이, TSM은 FCF 마진(capex 증가)이 고점보다 소폭 낮아져 '개선' 조건에서 빠졌다.

**6. 시장이 향후 3~5년 성장 지속기간을 가장 과소평가하고 있는 기업은?**

- **NVIDIA**
  - 주가는 4년 EPS CAGR 11.5% [I]만 요구한다.
  - 이미 FY+2까지 +69%가 확인됐다. 결국 FY29 이후 성장을 거의 0으로 가정하는 셈이다.
- 차순위
  - **Broadcom**: 내재 15%. 반면 FY28 AI 매출 $230B 윤곽 [G].
  - **TSMC**: 내재 19%. 2026 +40%, capex 상향.
  - **Celestica**: 내재 18%. 2027 가속 가이던스.

**7. 멀티플 상승 없이 향후 12~24개월 15% 이상 기대수익이 가능한 기업은?**

- NTM P/E를 고정한 12개월 [M] 기대수익

| 종목 | 12M [M] | 비고 |
|---|---|---|
| NVDA | +39% | |
| FLEX | +39% | |
| CLS | +38% | |
| AVC | +35% | |
| CIEN | +31% | |
| RDDT | +24% | |
| TSM | +24% | |
| LLY | +23% | |
| FIX | +18% | |
| ENVA | +16% | ASR 효과 별도 |

- 24개월 roll-forward(FY+2 EPS × 현재 FY+1 P/E)로 보면 NVDA +69%, CLS +73%.

**8. 이 모든 조건을 종합했을 때 정밀 기업가치평가 가치가 가장 높은 Top 5는?**

1. **NVIDIA**
2. **Celestica**
3. **Ciena**
4. **TSMC**
5. **Asia Vital Components**

- 차순위 교체 후보: Reddit(비AI 분산), AMD(리비전 최강이나 기대 선반영).

---

## 부록 A. 데이터 파일과 재현 방법

- `2026-09-24_screen_full.csv`: 채점된 338개 전체(Peak-trap 포함)의 지표, 세부 점수, 플래그.
- `scripts/`: 데이터 수집·산출 파이프라인(Python, yfinance). 실행 순서는 `scripts/README.md`를 참고.

### 한계

1. Yahoo Finance 컨센서스는 제공처(LSEG 등)와 표본 수가 다를 수 있다. CIEN FY+2 7명, CLS FY+2 9명, TSEM 9명처럼 표본이 작으면 신뢰도가 낮다.
2. 매출·EBITDA·FCF 컨센서스 리비전과 FY+3 컨센서스는 확인 불가.
3. ROIC/RONIC은 GAAP 재무제표로 산출했다. 영업권과 순현금 규모에 따라 왜곡될 수 있다(†표시).
4. Catalyst 3점과 Risk −2~0점은 뉴스 확인에 기반한 주관적 오버레이다.
5. 본 자료는 투자 권유가 아닌 리서치 아이디어 발굴용 스크리닝이다.

## 부록 B. 주요 출처

- NVIDIA Q2 FY27 실적: [SEC 8-K](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm), [CNBC: FY28 +70% 전망](https://www.cnbc.com/2026/08/26/nvidia-nvda-earnings-report-q2-2027-live-updates.html)
- Celestica: [Q2 2026 실적](https://corporate.celestica.com/news-releases/news-release-details/celestica-announces-second-quarter-2026-financial-results), [Events (Investor Day)](https://corporate.celestica.com/events-and-presentations)
- Ciena: [FQ3 2026 실적](https://investor.ciena.com/news/news-details/2026/Ciena-Reports-Fiscal-Third-Quarter-2026-Financial-Results/default.aspx), [Q3 콜 하이라이트](https://finance.yahoo.com/markets/stocks/articles/ciena-q3-earnings-call-highlights-150431612.html), [주가 하락 배경](https://www.investing.com/news/transcripts/earnings-call-transcript-ciena-tops-q3-2026-forecasts-but-shares-fall-93CH-4888077)
- TSMC: [2026 가이던스 상향](https://finance.yahoo.com/technology/ai/articles/tsmc-raised-2026-revenue-guidance-143624251.html), [8월 매출](https://www.tradingkey.com/analysis/stocks/us-stocks/262160382-tsmc-august-revenue-hit-new-high-tradingkey)
- AVC: [Q2 2026 콜](https://finance.yahoo.com/quote/3017.TW/earnings/3017.TW-Q2-2026-earnings_call-665770.html), [Digitimes 액냉 확장](https://www.digitimes.com/news/a20260422PD205/avc-liquid-cooling-growth-revenue-data-center.html)
- AMD: [Benzinga MI450/OpenAI/Oracle](https://www.benzinga.com/markets/tech/26/09/61900130/amd-stock-record-high-openai-oracle-mi450-raymond-james)
- Broadcom: [Q3 FY26 실적](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial), [AI 매출 FY27 $115B / FY28 $230B](https://seekingalpha.com/news/4639799-broadcom-forecasts-58b-fiscal-2026-ai-revenue-and-outlines-115b-in-2027-230b-in-2028)
- Teradyne: [Q2 2026](https://www.investing.com/news/company-news/teradyne-q2-2026-slides-ai-drives-record-revenue-104-growth-93CH-4820714)
- Reddit: [Q2 2026 (CNBC)](https://www.cnbc.com/2026/07/30/reddit-rddt-q2-2026-earnings-report.html)
- Lumentum: [FQ4 2026](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Results/default.aspx)
- Onto Innovation: [Q2 2026](https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Reports-2026-Second-Quarter-Results/default.aspx)
- Tower Semiconductor: [Q2 2026 콜 하이라이트](https://finance.yahoo.com/markets/stocks/articles/tower-semiconductor-q2-earnings-call-180441124.html)
- Fujikura: [가이던스 상향](https://www.investing.com/news/company-news/fujikura-raises-fullyear-operating-profit-guidance-to-310bn-93CH-4749383), [광섬유 캐파 3배](https://w.media/fujikura-to-triple-fiber-capacity-with-%C2%A5300bn-ai-push/)
- Comfort Systems: [Q2 2026](https://investors.comfortsystemsusa.com/news-releases/news-release-details/comfort-systems-usa-reports-second-quarter-2026-results)
- Enova: [Grasshopper 인수 철회 및 ASR](https://www.fool.com/investing/2026/09/17/why-enova-international-stock-was-plummeting-this/)
- Flex: [실적 후 하락·분사](https://seekingalpha.com/news/4620412-flex-declines-9-on-earnings-extends-losing-streak-to-four-sessions)
- MKS: [9월 하락](https://www.gurufocus.com/news/9080377/mks-inc-mksi-shares-fall-105-gf-value-says-still-overvalued)
- 반도체 장비 매도: [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/chip-equipment-stocks-slide-ai-145229848.html)
- Credo: [FQ1 2027 후 하락](https://www.tikr.com/blog/credo-technology-crdo-stock-drops-q1-fiscal-2027-earnings-beat)
- AppLovin: [Q2 미스·소송](https://www.fool.com/investing/2026/08/09/applovin-revenue-jump-why-stock-plunge/)
- Halozyme: [주가 급등 배경](https://stockstory.org/us/stocks/nasdaq/halo/news/why-up-down/halozyme-therapeutics-halo-shares-skyrocket-what-you-need-to-know)
- Harmony: [2026 가이던스](https://ir.harmonybiosciences.com/news-releases/news-release-details/harmony-biosciences-reports-q1-financial-results-and-confirms)
- 메모리 사이클: [Motley Fool: Peak 논쟁](https://www.fool.com/investing/2026/09/02/is-the-memory-supercycle-peak-near-for-micron-and/), [Invezz: 인텔 경고](https://invezz.com/news/2026/09/18/sk-hynix-jumps-5-samsung-rises-3-as-intel-warning-challenges-peak-memory-fears/)
- Wiwynn: [Digitimes](https://www.digitimes.com/news/a20260910PD224/wiwynn-ai-server-shipments-asic-revenue.html)
- 컨센서스·주가·재무제표: Yahoo Finance(yfinance 경유), 2026-09-23 스냅샷
