# 스크리닝 파이프라인 재현 방법

필요 패키지: `pip install yfinance pandas numpy`

모든 스크립트는 같은 작업 디렉터리에서 실행한다. 중간 산출물(`d1/`, `d2/`, `*.pkl`, `*.json`)이 그 디렉터리에 생긴다.

| 순서 | 스크립트 | 역할 |
|---|---|---|
| 1 | `universe.py` | Yahoo 스크리너로 미국 상장 시총 $2B 이상 전 종목을 받아 `universe.json`에 저장 |
| 2 | (수동) | `universe.json`으로 사전 필터(FY+2 EPS 성장 ≥ 12%, FY+2 P/E < 45x, 거래대금 > $15M)를 걸어 `stage1.json` 생성. 해외 종목 목록은 `intl.json` |
| 3 | `fetch1.py stage1.json` / `fetch1.py intl.json` | 종목별 info, EPS·매출 컨센서스, EPS 트렌드·리비전, 서프라이즈 수집 → `d1/` |
| 4 | (수동) | `yf.download`로 1년 주가(`px.pkl`), FX 환율(`fx.json`) 저장 |
| 5 | `metrics.py` | P/E·압축률·PEG·리비전·역산 성장률·12M 가격 계산 → `m1.pkl` |
| 6 | `fetch2.py <list>` | 성장 필터 통과 종목의 연간·분기 재무제표 수집 → `d2/` |
| 7 | `quality.py` | ROIC·RONIC·FCF 마진·SBC·희석·매출채권/재고 계산 → `q.pkl` |
| 8 | `score.py` | 100점 스코어링과 Peak/Turnaround/일회성 플래그 → `scored.pkl` |
| 9 | `final.py` | Catalyst·Risk 수동 오버레이, 유형 분류, Alpha 플래그 → `final.pkl` |
| 10 | `tables.py` | Top 20·Ranking·Peak-trap 표와 전체 CSV 출력 |

동시 요청이 많으면 Yahoo가 요청 수를 제한한다. `W=2` 환경변수로 동시 작업 수를 줄이고 다시 실행하면 된다. 이미 받은 파일은 건너뛴다.

## v2 (내재가치 + 성장 대비, 시총 제한 없음)

`scripts/v2/`의 스크립트는 v1 스크립트와 같은 작업 디렉터리에서, v1 산출물(`d1/`, `d2/`, `fx.json`, `intl.json`)이 있는 상태에서 실행한다. 스크립트는 `v2/` 하위 폴더에 두고 실행한다.

| 순서 | 스크립트 | 역할 |
|---|---|---|
| 1 | `v2/universe_all.py` | 시총 제한 없는 미국 상장 전 종목 수집 → 거래대금 $1M·주가 $1 필터는 수동 단계에서 `v2/liquid.json`으로 저장 |
| 2 | `fetch1.py v2/liquid.json` | 컨센서스 수집 |
| 3 | `v2/d2list.py` → `fetch2.py v2/d2todo.json` | 흑자·금융사만 재무제표 수집(빈 응답은 재시도) |
| 4 | (수동) | 5년 주간 주가 `v2/px5y.pkl` 저장 |
| 5 | `v2/model.py v2/all.json` | 정상화 이익·사이클 판정·DCF 3시나리오·EPV·역산 지속기간 → `v2/model.pkl` |
| 6 | `v2/score2.py` | 트랙 A/B/C, 제외 규칙, 100점 채점, `v2/overlay.json` 수동 판단 반영 → `v2/scored2.pkl` |
