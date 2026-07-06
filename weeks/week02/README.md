# Week 02. 도구 사용 (Tool Use)

> **Part:** 에이전트 기초 · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Writing Effective Tools for Agents* (도구 설계는 에이전트 UX)

## 🛠 실습 (from-scratch)
도구 등록·파싱·실행 직접 구현 (계산기·검색 함수)

## 💬 토론 포인트 (교수용 백업 질문)
도구가 많아질수록 좋은가? 도구 절벽(tool cliff)이 생기는 이유는?

## 발표 논문
#### 🟡 Toolformer: LMs Can Teach Themselves to Use Tools
- **출처:** Schick et al., NeurIPS 2023 · arXiv:2302.04761
- **발표 필수:** self-supervised로 API 호출 위치를 학습하는 방식
- **선택 심화:** 호출 필터링 손실, 데이터 생성 파이프라인
- **PDF:** [`W02_Toolformer_2302.04761.pdf`](../../papers/W02_Toolformer_2302.04761.pdf)

#### 🟡 ToolLLM: Mastering 16000+ Real-world APIs
- **출처:** Qin et al., ICLR 2024 · arXiv:2307.16789
- **발표 필수:** 대규모 실세계 API 학습 프레임과 DFSDT 탐색
- **선택 심화:** ToolBench 구축, pass/win rate
- **PDF:** [`W02_ToolLLM_2307.16789.pdf`](../../papers/W02_ToolLLM_2307.16789.pdf)

## 폴더
- `theory/` — 이론 강의 자료 (슬라이드·노트)
- `practice/` — from-scratch 실습 코드
- `presentation/` — 학생 논문 발표 자료

## 발표 평가 루브릭
| 항목 | 배점 | 기준 |
|---|---|---|
| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |
| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화는 직관 허용, 수식 생략 가능) |
| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |
| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |
