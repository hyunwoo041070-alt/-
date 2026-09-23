# Deep Value × Growth Discriminator

밸류에이션 대비 저평가된 성장주를 발굴하는 스크리닝 프레임워크와, 그 병목이었던
**Normalized EPS 산출을 자동화**하는 도구.

## 문제

3중 조건 — Absolute Valuation "매우 쌈" + Growth-Adjusted "성장 대비 매우 저평가" +
Market Expectations "지나치게 낮음" — 을 동시에 만족하는 종목은 **밸류 트랩의 지문**이다.
효율적 시장에서 이 조합이 성립하려면 시장이 P/E의 분모(E)를 믿지 않아야 하고,
대체로 시장이 맞다.

2026-09 실제 스크린에서 3중 조건을 모두 만족한 종목은 Micron, SK하이닉스, 삼성전자,
SanDisk 넷뿐이었다. 전부 메모리, 전부 사이클 피크.

따라서 필요한 것은 스크리너가 아니라 **판별기**다. 판별의 핵심은 Normalized EPS이고,
그것이 병목이었다.

## 구성

| 경로 | 내용 |
|---|---|
| `prompts/deep-value-growth-discriminator-v2.1.md` | 전체 스크리닝 프롬프트 (v2.1) |
| `normalizer/sec_normalize.py` | SEC XBRL → Normalized EPS / Peak Ratio 자동 산출 |
| `normalizer/portfolio.example.csv` | 배치 실행 입력 템플릿 |

## 병목 해소 구조

Normalized EPS와 Forward Consensus는 **성격이 다른 두 문제**다.

| | 필요 데이터 | 해결 | 비용 |
|---|---|---|---|
| Normalized EPS | **과거** 10년 재무제표 | SEC XBRL API | **$0** |
| Forward Consensus | **미래** 애널리스트 추정치 | 유료 벤더 | 유료 |

SEC가 과거 데이터를 무료·표준화·15년치로 API 제공하므로 Normalized EPS 병목은
완전히 해소된다. 스크립트는 SEC에서 얻을 수 없는 **주가와 컨센서스만** 인자로 받는다.

추가로, 방법론 개선으로 데이터 요구량 자체를 약 80% 줄인다:
- **STEP 0-A/0-B 분리** — Peak Ratio의 역할은 Type 1(사이클 피크) 배제뿐이므로,
  사이클 노출이 없는 종목은 정상화 계산을 생략한다. 실제 투자 후보인
  Type 4/5/6/7(고아 종목·수급왜곡·회계왜곡·Mix은폐)은 사이클 정상화를 요구하지 않는다.
- **방법 사다리 1~5** — 회사가 직접 공시한 through-cycle 수치(IR 덱 1개)를 1순위로,
  10년 시계열이 필요한 방법은 후순위로 배치.
- **Peak Ratio는 4구간 분류로만 소비된다** — 점 추정치가 아니라 구간만 필요하므로
  훨씬 거친 데이터로도 판정이 가능하다.

## 사전 준비

이 리포지토리가 도는 환경에서 `data.sec.gov` / `www.sec.gov` 가 차단되어 있으면
스크립트가 네트워크 오류와 함께 조치 방법을 안내한다. Claude Code 웹 세션에서는
제목줄의 클라우드 환경 메뉴 → Edit → **Network access** 에서 두 도메인을 허용하거나
접근 수준을 넓히면 된다.

차단 환경에서는 `--cache` 로 미리 저장한 companyfacts JSON을 쓰면 오프라인 동작한다.

```sh
export SEC_USER_AGENT="your-name your@email.com"   # SEC 요청 시 권장
```

## 사용법

```sh
# 단건
./normalizer/sec_normalize.py MU --price 1043.96 --fwd-eps 95.97

# 캐시 저장 후 오프라인 실행
./normalizer/sec_normalize.py MU --save-cache cache/
./normalizer/sec_normalize.py MU --price 1043.96 --fwd-eps 95.97 --cache cache/MU.json

# 배치 + CSV 출력
./normalizer/sec_normalize.py --batch normalizer/portfolio.example.csv --csv-out out.csv

# 네트워크 없이 계산 로직 검증 (12개 체크)
./normalizer/sec_normalize.py --selftest
```

의존성 없음 (Python 3.9+ 표준 라이브러리만).

## 스크립트가 산출하는 것

- **STEP 0-A 기계적 플래그** — 마진 변동폭 ≥15%p, 영업적자 연도, EPS 적자 연도
  (상품가격 연동·고객 capex 연동은 정성 판정이므로 수동)
- **Normalized EPS 4가지** — 마진 정상화(a) / ROIC 정상화(b) / 사이클 평균(c) /
  Trough 앵커 구간(e). 채택값과 사용 방법을 함께 표기
- **Peak Ratio + 4구간 판정**
- **GATE 1 입력값** — Normalized P/E, 이익수익률, EV/IC, 이론 적정 EV/IC
  `(ROIC−g)/(WACC−g)`, 적정 대비 할인/프리미엄
- **자동 경고** — 중위 ROIC < WACC 시 GATE 2(G2-4) 탈락 및 PEG 무의미 경고

## 검증

`--selftest` 는 손으로 검산 가능한 합성 시클리컬 기업으로 12개 항목을 확인한다.
분기 데이터 오인 방지, 재작성 우선 적용, 실효세율·중위마진·정상화 EPS·Peak Ratio·
투하자본 계산, 구간 판정, 컨센서스 없을 때의 graceful degradation을 포함한다.

핵심 검증 항목: **Forward P/E 20배로 싸 보이는 종목의 Normalized P/E가 83배로
드러나는지** — 트랩 노출이 실제로 작동하는지 확인한다.

## 한계

- **Normalized FCF Yield는 근사치**다. 유지보수 capex ≈ 감가상각 가정이며,
  실제 FCF는 현금흐름표가 필요하다. 표기도 "이익수익률"로 정직하게 바꿔 두었다.
- **주가·컨센서스는 SEC에 없다.** 인자로 넣어야 한다.
- **미국 상장사 전용.** 한국은 DART OpenAPI(`opendart.fss.or.kr`),
  일본은 EDINET API가 같은 역할을 하며 둘 다 무료다.
- XBRL 태그는 제출인마다 다르다. 폴백 목록으로 대응하지만 커버되지 않는 태그를
  쓰는 기업은 해당 항목이 "확인 불가"로 나온다 — 추정하지 않는다.
