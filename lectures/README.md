# 강의 슬라이드 (lectures/)

주차별 이론 강의(30–40분) 슬라이드. 설계 근거는 [`docs/lecture-outlines.md`](../docs/lecture-outlines.md).

- 형식: **Marp 마크다운** (`weekNN/slides.md`) — git으로 diff 가능, 슬라이드 주석(`<!-- -->`)이 발화 대본 겸 타이머
- 수치·인용은 `papers/`의 검증된 PDF에서 직접 추출한 값만 사용

## 렌더링

```bash
# VS Code: "Marp for VS Code" 확장 → 미리보기·내보내기
# CLI:
npm i -g @marp-team/marp-cli
marp lectures/week01/slides.md --pdf --allow-local-files   # PDF
marp lectures/week01/slides.md --pptx                      # PPTX (강의실 호환)
```

## 현황

| 주 | 슬라이드 | 상태 |
|---|---|---|
| 01 | [week01/slides.md](week01/slides.md) | ✅ 개념중심 (16장 / 25분 · 정의·자율성 스펙트럼·폼팩터) |
| 02 | [week02/slides.md](week02/slides.md) | ✅ 개념중심 (17장 / 35분 · CoT→ReAct 계보 + 트레이스 리딩) |
| 03 | [week03/slides.md](week03/slides.md) | ✅ 개념중심 (17장 / 35분 · 추론 두 갈래 — test-time·STaR·R1) |
| 04 | [week04/slides.md](week04/slides.md) | ✅ 개념중심 (18장 / 35분 · 함수호출 원리·도구 정의·학습) |
| 05 | [week05/slides.md](week05/slides.md) | ✅ 초안 (22장 / 35분 · 계획과 탐색 — ToT·ReWOO + 현장 노트 포함) |
| 06 | [week06/slides.md](week06/slides.md) | ✅ 초안 (22장 / 35분 · 자기반성 — Self-Refine·Reflexion + 오라클 반전 카드 + 현장 노트 포함) |
| 07 | [week07/slides.md](week07/slides.md) | ✅ 초안 (21장 / 35분 · RAG 기초 — 임베딩·코사인 유사도·파이프라인 + 현장 노트 포함) |
| 08 | [week08/slides.md](week08/slides.md) | ✅ 초안 (22장 / 35분 · 에이전틱 RAG + MCP — Self-RAG·Adaptive-RAG + 현장 노트 포함) |
| 09 | [week09/slides.md](week09/slides.md) | ✅ 초안 (22장 / 35분 · 컨텍스트 엔지니어링 ⭐ — Lost in the Middle·LLMLingua + 현장 노트·🏁 중간 데모 포함) |
| 10 | [week10/slides.md](week10/slides.md) | ✅ 초안 (22장 / 30분 · 메모리 — MemGPT·Mem0 + 현장 노트 포함) |
| 11 | [week11/slides.md](week11/slides.md) | ✅ 초안 (22장 / 40분 · 멀티에이전트 + LangGraph 전환점 ⭐ — 감싸기 원칙 + 현장 노트 포함) |
| 12 | [week12/slides.md](week12/slides.md) | ✅ 초안 (22장 / 35분 · 컴퓨터/웹 사용 — DOM vs 스크린샷·WebArena·OSWorld + 현장 노트 포함) |
| 13 | [week13/slides.md](week13/slides.md) | ✅ 초안 (22장 / 35분 · 평가 — Pareto·pass^k, W3/W4/W12 복선 회수 + 현장 노트 포함) |
| 14 | [week14/slides.md](week14/slides.md) | ✅ 초안 (22장 / 35분 · 신뢰·보안 — 간접 인젝션·trifecta·방어 4계층 + 현장 노트 포함) |
| 15 | [week15/slides.md](week15/slides.md) | ✅ 초안 (22장 / 35분 · 프로덕션·단순함 — Agentless·SWE-agent + 폼팩터 회귀 + 현장 노트 포함) |
| 16 | [week16/slides.md](week16/slides.md) | ✅ 초안 (11장 / 15분 · 학기 회고 + 최종 발표 운영 — 발표 주) |
