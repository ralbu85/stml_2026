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
| 01 | [week01/slides.md](week01/slides.md) | ✅ 초안 (32장 / 40분 · 폼팩터 4형태 + 현장 노트 포함) |
| 02 | [week02/slides.md](week02/slides.md) | ✅ 초안 (26장 / 39분 · RL 입문 + 현장 노트 포함) |
| 03 | [week03/slides.md](week03/slides.md) | ✅ 초안 (27장 / 35분 · function calling 해부 + 현장 노트 포함) |
| 04–16 | — | 개요만 (`docs/lecture-outlines.md`) |
