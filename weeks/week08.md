# Week 08. 컨텍스트 엔지니어링 (하네스) ⭐

> **Part:** 지식·컨텍스트·기억 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
⭐ 컨텍스트를 유한 자원으로 다루는 **컨텍스트 엔지니어링 = 하네스**. 이론에서 LLM이 긴 컨텍스트를 어떻게(못) 쓰는지와 압축·큐레이션을 다루고, 실습에서 컨텍스트 예산·압축을 하네스에 넣는다. Lost-in-the-Middle·LLMLingua.

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Effective Context Engineering* + HumanLayer — *Skill Issue: Harness Engineering* · MS12

## 📄 발표 논문
#### 🟡 Lost in the Middle: How LMs Use Long Contexts
- **출처:** Liu et al., TACL 2024 · arXiv:2307.03172
- **발표 필수:** LLM이 긴 컨텍스트의 중간 정보를 잘 못 쓰는 현상
- **선택 심화:** 위치별 성능 곡선, 검색 문서 수 효과
- **PDF:** [`W08_Lost-in-the-Middle_2307.03172.pdf`](../papers/W08_Lost-in-the-Middle_2307.03172.pdf)

#### 🟡 LLMLingua: Compressing Prompts for Accelerated Inference
- **출처:** Jiang et al., EMNLP 2023 · arXiv:2310.05736
- **발표 필수:** 프롬프트를 압축해 비용·지연을 줄이면서 성능 유지
- **선택 심화:** 예산 제어 압축, perplexity 기반 토큰 선택
- **PDF:** [`W08_LLMLingua_2310.05736.pdf`](../papers/W08_LLMLingua_2310.05736.pdf)

#### 🔴 Agentic Context Engineering (선택읽기·프런티어) *(선택읽기)*
- **출처:** 2025 · arXiv:2510.04618
- **발표 필수:** 컨텍스트 자체를 진화시켜 자기개선
- **선택 심화:** context 업데이트 정책
- **PDF:** [`W08_opt-Agentic-Context-Engineering_2510.04618.pdf`](../papers/W08_opt-Agentic-Context-Engineering_2510.04618.pdf)

#### 🔴 ReasoningBank (선택읽기·프런티어) *(선택읽기)*
- **출처:** 2025 · arXiv:2509.25140
- **발표 필수:** 추론 메모리를 쌓아 에이전트가 진화
- **선택 심화:** 메모리 항목 추출·재사용
- **PDF:** [`W08_opt-ReasoningBank_2509.25140.pdf`](../papers/W08_opt-ReasoningBank_2509.25140.pdf)

## 💬 토론 포인트 (교수 백업 질문)
컨텍스트는 왜 유한 자원인가? 무엇을 넣고 무엇을 버려야 하나?

## 🛠 실습 (from-scratch)
컨텍스트 예산·압축·큐레이션을 하네스에 내장 (긴 컨텍스트 관리)

> 실습 코드·노트는 이 파일 아래에 이어 적거나, 분량이 커지면 `week08/` 폴더로 분리한다.

## 🎤 발표 진행 (요약 · 상세는 [발표 가이드](../docs/presentation-guide.md))
- 편당 **25분**: 발표 15분(슬라이드 6장 상한·하드 스톱) + 이해검증 8분 + 정리 2분
- 발표 템플릿 6장: ①한 문장 기여 ②문제·동기 ③핵심 메커니즘(직접 그린 그림) ④결과 1개 ⑤약한 가정·한계 ⑥연결
- 교수 콜드 질문(슬라이드 끄고): *X 단계 빼면? / 처음부터 구현 첫 3단계? / 실패하는 입력?*
- 지정 토론자 1명 사전 배정 → 발표 후 2분 반박·보완

## 📊 평가 루브릭
| 항목 | 배점 | 기준 |
|---|---|---|
| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |
| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화는 직관 허용, 수식 생략 가능) |
| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |
| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |
