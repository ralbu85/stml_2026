# Week 08. 메모리 (Memory)

> **Part:** 추론과 지식 · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
Letta (MemGPT) — *Agent Memory Blog* (3계층 메모리)

## 🛠 실습 (from-scratch)
메모리 스트림 구현(저장·검색), 외부 메모리 통합

## 💬 토론 포인트 (교수용 백업 질문)
무엇을 기억하고 무엇을 잊어야 하는가? 메모리 검색의 기준은?

## 발표 논문
#### 🟡 MemGPT: Towards LLMs as Operating Systems
- **출처:** Packer et al., 2023 · arXiv:2310.08560
- **발표 필수:** 가상메모리 비유의 계층적 메모리(core/archival)
- **선택 심화:** function-call self-editing, 페이징
- **PDF:** [`W08_MemGPT_2310.08560.pdf`](../../papers/W08_MemGPT_2310.08560.pdf)

#### 🟡 MemoryBank: Enhancing LLMs with Long-Term Memory
- **출처:** Zhong et al., AAAI 2024 · arXiv:2305.10250
- **발표 필수:** 망각 곡선 기반 메모리 갱신·검색
- **선택 심화:** 사용자 페르소나 유지
- **PDF:** [`W08_MemoryBank_2305.10250.pdf`](../../papers/W08_MemoryBank_2305.10250.pdf)

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
