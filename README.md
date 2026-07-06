# 머신러닝 특론 — LLM 에이전트 (2026)

**논문 읽기와 함께 만들기** · 16주 · 주당 논문 2편 발표 + 매주 from-scratch 실습
**대상:** 부산대/부경대 대학원 · **최종 산출물:** RAG 문서 QA 에이전트

매주 3시간: **이론 · 실습 · 논문발표** 병행. 난이도 범례: 🟢 기초 · 🟡 중급 · 🔴 심화

## 문서

- [`docs/syllabus-v2.md`](docs/syllabus-v2.md) — **강의계획서(현행판)**: 커버리지 검증 + 난이도 재조정
- [`papers/README.md`](papers/README.md) — 발표 논문 34편 검증 매니페스트 (34/34 arXiv 확인)

## 주차 지도

| 주 | 주제 | | 주 | 주제 |
|---|---|---|---|---|
| [01](weeks/week01) | 에이전트란 무엇인가 | | [09](weeks/week09) | 체화·평생학습 |
| [02](weeks/week02) | 도구 사용 | | [10](weeks/week10) | 멀티에이전트 + LangGraph ⭐ |
| [03](weeks/week03) | 피드백·자기반성 | | [11](weeks/week11) | 에이전트 강화학습 |
| [04](weeks/week04) | 계획과 탐색 | | [12](weeks/week12) | 🆕 GUI·컴퓨터/웹 사용 |
| [05](weeks/week05) | 🆕 추론 모델 | | [13](weeks/week13) | 🆕 안전·보안 |
| [06](weeks/week06) | RAG 1부: 기초 | | [14](weeks/week14) | 평가·벤치마크 |
| [07](weeks/week07) | RAG 2부: 에이전틱 | | [15](weeks/week15) | 단순함의 힘 |
| [08](weeks/week08) | 메모리 | | [16](weeks/week16) | 최종 발표 |

## 저장소 구조

```
docs/          강의계획서
papers/        발표 논문 PDF(gitignore) + 검증 매니페스트
scripts/       fetch_papers.py(논문 다운로드) · gen_weeks.py(주차 구조 생성)
weeks/weekNN/  README.md + theory/ + practice/ + presentation/
```

## 재현

```bash
python3 scripts/fetch_papers.py   # 논문 34편 arXiv 다운로드 → papers/
python3 scripts/gen_weeks.py      # 16주 디렉토리 구조 생성 → weeks/
```
