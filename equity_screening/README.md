# Equity Screening — Growth-Adjusted Valuation

향후 1~3년 이익성장이 현재 밸류에이션 부담을 주가가 암시하는 것보다 빠르게 낮출 기업을 찾는 스크린이다. 결과는 정밀 가치평가 프레임워크(Forward DCF, ROIC/RONIC, PEG, Reverse DCF 등)에 넣을 순서로 정리했다.

| 파일 | 내용 |
|---|---|
| `2026-09-23_growth_adjusted_screen.md` | 본 보고서: Top 20 → Top 10 → Top 5, 최종 Ranking, 3대 판정, False Positive 제거, Deep Dive 후보, 최종 질문 8개 답변 |
| `data/scored_universe_2026-09-23.csv` | 1단계 성장 스크린 통과 486개 종목 전체 점수와 78개 필드 |
| `data/fx_2026-09-23.json` | 통화 환산에 쓴 환율 |
| `scripts/` | 재현 가능한 파이프라인 (Python 3, `yfinance`, `pandas`, `requests`) |

## 실행 순서

스크립트는 별도 작업 디렉터리에서 실행한다. 중간 산출물(raw/, fin/, nq/, *.json)은 현재 디렉터리에 저장된다.

1. `universe.py` — 미국 상장 시총 $2B 이상 (Nasdaq Screener) → `universe_us.json`
2. `bulk.py` (`qs.py`, `intl.txt` 사용) — Yahoo quoteSummary: 추정치·추정치 추이·재무 데이터 → `raw/`
3. `px.py` — 1년 주가 → `px.json`
4. `fx.py` — 환율 → `fx.json`
5. `parse.py` → `rows.json`
6. `metrics.py` — P/E·압축률·PEG·수정률 → `m.json`
7. `stage1.py` — 1단계 Growth Screen → `s1.json`
8. `fin.py` — 재무제표·실적 이력 → `fin/`
9. `quality.py` — ROIC/RONIC/FCF/레버리지 → `q.json`
10. `nq.py` — FY+3 추정치 (Nasdaq/Zacks) → `nq/`
11. `score.py` — 100점 채점 → `scored.json`
12. `final.py` — 촉매 수동 가점(뉴스 확인, 0~4점)·제외·Alpha 플래그 → `final.json`
13. `tables.py` — 보고서 표 생성 → `tables.json`

`final.py`의 수동 촉매 가점(`FMAN`)과 데이터 결함 제외(`EXCL`)는 애널리스트 판단이다. 근거 출처는 보고서 13장에 있다.
