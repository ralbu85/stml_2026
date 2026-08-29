# 머신러닝 특론 — LLM 에이전트 (STML 2026)

**논문 읽기와 함께 만들기** · 15주 · 매주 논문 발표 + Colab 실습
**대상:** 부경대학교 대학원 · **최종 산출물:** 연구보조 검색·종합 에이전트(수업 논문 코퍼스 기반 RAG)

매주 3시간: 이론 강의 30–40분 · 논문 발표 2편 · 실습 80분.

**강의 사이트: <https://stml.tailcce2b.ts.net>** — 주차별 강의노트·실습·과제·발표 안내가 모두 사이트에서 열린다. 실습 노트북은 각 주차 페이지의 **Open in Colab** 링크로 브라우저에서 바로 실행한다.

## 자료 구성

이론 자료는 주차별 영문 강의노트 단일본이다: `lectures/weekNN/notes.en.md` (슬라이드 없음). 실습(`WN_lab_*.ipynb`)과 과제(`WN_hw_*.ipynb`)는 같은 폴더에 있다. 집필 기준은 [`docs/style-guide.md`](docs/style-guide.md).

## 주차 지도 (v10.1 · 14개 장)

순서 원칙: 개념 의존성 — 각 주는 직전 주까지 배운 것만으로 이해 가능하다.

| 주 | 장 | 주제 | | 주 | 장 | 주제 |
|---|---|---|---|---|---|---|
| 01 | 1 | 에이전트란 무엇인가 | | 09 | 8 | 검색 증강(RAG) |
| 02 | 2 | 프롬프팅과 추론 | | 10 | 9·10 | 컨텍스트 엔지니어링 · 메모리 |
| 03 | 3 | 도구 사용 | | 11 | 11 | 추론 모델과 강화학습 |
| 04 | 4 | 에이전트 루프(ReAct) | | 12 | 12·13 | 추론 경제학 · 벤치마크 |
| 05 | 5 | 자기반성과 평가 | | 13 | 14 | 안전·보안 · 회고 |
| 06 | 6 | 멀티에이전트 시스템 | | 14 | — | 최종 발표 |
| 07 | 7 | 계획과 탐색 | | 15 | — | 기말고사 |
| 08 | — | 중간고사(1–7주 범위) | | | | |

## 문서

- [`docs/syllabus.md`](docs/syllabus.md) — 강의계획서(현행판 v10.1): 주차·발표·평가 배치
- [`docs/presentation-guide.md`](docs/presentation-guide.md) — 논문 발표 가이드: 시간 배분·템플릿·이해 검증
- [`docs/style-guide.md`](docs/style-guide.md) — 강의자료 집필 규정
- [`labs/README.md`](labs/README.md) — 실습 표준과 오프라인 검증 방법
- [`papers/README.md`](papers/README.md) — 발표 논문 매니페스트(전량 arXiv 확인)

## 저장소 구조

```
lectures/weekNN/  notes.en.md(강의노트) + 실습·과제 노트북
labs/             실습 인프라: 데이터 · 드라이런 테스트(tests/) · 참조답안(checkpoints/)
site/             Quarto 강의 사이트 (site/build.sh로 빌드)
docs/             강의계획서 · 가이드 · 집필 규정
papers/           발표 논문 PDF(gitignore) + 매니페스트
scripts/          fetch_papers.py(논문 다운로드) · gen_weeks.py
```

## 재현

```bash
python3 scripts/fetch_papers.py       # 발표 논문 arXiv 다운로드·검증 → papers/
bash    materials/fetch_materials.sh  # 참고 강의자료 레포 → materials/repos/
bash    site/build.sh                 # 강의 사이트 빌드 → site/_site
bash    labs/tests/dryrun_all.sh      # 전체 노트북 오프라인 검증(키 불필요)
```
