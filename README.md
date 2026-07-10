# 머신러닝 특론 — LLM 에이전트 (2026)

**논문 읽기와 함께 만들기** · 16주 · 주당 논문 2편 발표 + 매주 from-scratch 실습
**대상:** 부산대/부경대 대학원 · **최종 산출물:** RAG 문서 QA 에이전트

매주 3시간: **이론 · 실습 · 논문발표** 병행. 난이도 범례: 🟢 기초 · 🟡 중급 · 🔴 심화

## 문서

- [`docs/syllabus.md`](docs/syllabus.md) — **강의계획서(현행판)**: MS/Berkeley 흐름 기반 재구성
- [`docs/presentation-guide.md`](docs/presentation-guide.md) — **논문 발표 가이드**: 시간 배분·템플릿·이해 검증
- [`docs/practice-guide.md`](docs/practice-guide.md) — **실습 가이드**: 누적 빌드(문서 QA 에이전트) 주차별 설계
- [`docs/lecture-outlines.md`](docs/lecture-outlines.md) — **이론 강의 개요(30–40분)**: 주차별 핵심 개념·분 단위 진행·근거 자료
- [`materials/README.md`](materials/README.md) — 참고자료(MS·Berkeley·HF…) + 주차별 이론 플랜
- [`papers/README.md`](papers/README.md) — 발표 논문 38편 검증 매니페스트 (전량 arXiv 확인)

## 주차 지도

흐름: **Microsoft ai-agents-for-beginners + Berkeley LLM Agents** 재구성. 각 주차는 한 파일에서 다 보인다.

| 주 | 주제 | | 주 | 주제 |
|---|---|---|---|---|
| [01](weeks/week01.md) | 에이전트 개요 + ReAct | | [09](weeks/week09.md) | 메모리 |
| [02](weeks/week02.md) | 추론 모델 | | [10](weeks/week10.md) | 멀티에이전트 + LangGraph ⭐ |
| [03](weeks/week03.md) | 도구 사용 | | [11](weeks/week11.md) | 컴퓨터/웹 사용 |
| [04](weeks/week04.md) | 계획과 탐색 | | [12](weeks/week12.md) | 에이전트 강화학습 |
| [05](weeks/week05.md) | 자기반성·메타인지 | | [13](weeks/week13.md) | 평가·벤치마크 |
| [06](weeks/week06.md) | RAG 1부: 기초 | | [14](weeks/week14.md) | 신뢰·보안 |
| [07](weeks/week07.md) | 에이전틱 RAG + MCP | | [15](weeks/week15.md) | 프로덕션·단순함 |
| [08](weeks/week08.md) | 컨텍스트 엔지니어링(하네스) ⭐ | | [16](weeks/week16.md) | 최종 발표 |

## 저장소 구조

```
docs/          강의계획서 · 발표 가이드 · 이론 개요
labs/          실습 스캐폴드(docqa-agent 누적 빌드: 빈칸+테스트+체크포인트)
lectures/      주차별 강의 슬라이드(Marp)
papers/        발표 논문 PDF(gitignore) + 검증 매니페스트
scripts/       fetch_papers.py(논문 다운로드) · gen_weeks.py(주차 파일 생성)
weeks/weekNN.md  주차별 한 파일 (필요해지면 weekNN/ 폴더로 확장)
```

## 재현

```bash
python3 scripts/fetch_papers.py   # 논문 38편 arXiv 다운로드·검증 → papers/
python3 scripts/gen_weeks.py      # 16주 파일 생성 → weeks/
bash    materials/fetch_materials.sh  # 참고 강의자료 레포 → materials/repos/
```
