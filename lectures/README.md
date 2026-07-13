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

**2026-07-13 전면 초기화** — v4 순서 확정 후 16덱 전부 스텁 상태로 리셋(직전 상태는 git `079ab0a`).
재작성 기준: [`docs/lecture-outlines.md`](../docs/lecture-outlines.md)(주차 개요) · [`docs/style-guide.md`](../docs/style-guide.md)(집필 규정).

| 주 | 주제 | 상태 |
|---|---|---|
| 01 | 강의소개 · 에이전트 개요 | ⬜ 스텁 — 재작성 예정 |
| 02 | 프롬프팅과 추론 | ⬜ 스텁 — 재작성 예정 |
| 03 | 도구 사용 | ⬜ 스텁 — 재작성 예정 |
| 04 | 에이전트 루프 (ReAct) | ⬜ 스텁 — 재작성 예정 |
| 05 | RAG 1부: 기초 | ⬜ 스텁 — 재작성 예정 |
| 06 | 에이전틱 RAG + MCP | ⬜ 스텁 — 재작성 예정 |
| 07 | 계획과 탐색 | ⬜ 스텁 — 재작성 예정 |
| 08 | 자기반성·메타인지 | ⬜ 스텁 — 재작성 예정 |
| 09 | 컨텍스트 엔지니어링 ⭐ | ⬜ 스텁 — 재작성 예정 |
| 10 | 메모리 | ⬜ 스텁 — 재작성 예정 |
| 11 | 멀티에이전트 + LangGraph ⭐ | ⬜ 스텁 — 재작성 예정 |
| 12 | 컴퓨터/웹 사용 | ⬜ 스텁 — 재작성 예정 |
| 13 | 평가·벤치마크 | ⬜ 스텁 — 재작성 예정 |
| 14 | 신뢰·보안 | ⬜ 스텁 — 재작성 예정 |
| 15 | 프로덕션·단순함 | ⬜ 스텁 — 재작성 예정 |
| 16 | 최종 발표 | ⬜ 스텁 — 재작성 예정 |
