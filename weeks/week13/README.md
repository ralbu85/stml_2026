# Week 13. 🆕 안전·보안 (Safety & Security)

> **Part:** 프런티어 (개념 위주) · **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

## 📖 보조읽기 (발표 대상 아님)
*OWASP Top 10 for LLM Applications* (인젝션·과도한 권한 등) — 매우 접근성 높음

## 🛠 실습 (from-scratch)
내 에이전트에 가드레일 추가 + 인젝션 공격 테스트

## 💬 토론 포인트 (교수용 백업 질문)
행동하는 에이전트의 가장 위험한 실패는? 어디까지 자동화를 믿을 수 있나?

## 발표 논문
#### 🟡 Not What You've Signed Up For: Indirect Prompt Injection
- **출처:** Greshake et al., AISec 2023 · arXiv:2302.12173
- **발표 필수:** 간접 프롬프트 인젝션이 왜 근본적 위협인가
- **선택 심화:** 실제 공격 시나리오 분류
- **PDF:** [`W13_Indirect-Prompt-Injection_2302.12173.pdf`](../../papers/W13_Indirect-Prompt-Injection_2302.12173.pdf)

#### 🟡 InjecAgent: Benchmarking Indirect Injection in Tool Agents
- **출처:** Zhan et al., ACL 2024 · arXiv:2403.02691
- **발표 필수:** 도구 사용 에이전트의 인젝션 취약성 측정
- **선택 심화:** 공격 성공률, 방어 프롬프트 효과
- **PDF:** [`W13_InjecAgent_2403.02691.pdf`](../../papers/W13_InjecAgent_2403.02691.pdf)

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
