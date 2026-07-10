# Week 01. 에이전트 개요 + ReAct

> **Part:** 토대 · 난이도: 🟢 기초 · 🟡 중급 · 🔴 심화 · [📋 발표 가이드](../docs/presentation-guide.md)

## 🧭 개요
**강의소개(OT·발표 배정)** 와 함께 에이전트의 정의를 잡는 첫 주. 이론에서 에이전트 vs 워크플로우, 자율성 스펙트럼, ReAct의 **추론–행동–관찰 루프**(큰 그림)를 다루고, 실습은 **환경 세팅 + LLM 호출 래퍼**까지. ReAct 루프 구현은 W2 실습에서 한다. ReAct·CoT.

## 📖 보조읽기 (발표 대상 아님)
Anthropic — *Building Effective Agents* (워크플로우 vs 에이전트) · MS01

## 📄 이번 주 논문 — ⚠️ 학생 발표 없음 (배정 전)
1주차는 발표 배정 전이므로 학생 발표가 불가능하다. 대신:
- **ReAct** → 이론 강의(W1 덱)가 깊게 다룬다. 구현은 W2 실습.
- **CoT** → **교수가 6장 템플릿·15분 하드 스톱 그대로 시연 발표** — W2부터 시작될 학생 발표의 기대 수준을 보여준다.
- 이 시간에 **W2~W15 발표자·지정 토론자를 일괄 배정**한다. 상세 시간표는 [발표 가이드 §1](../docs/presentation-guide.md).

#### 🟢 ReAct: Synergizing Reasoning and Acting in LLMs
- **출처:** Yao et al., ICLR 2023 · arXiv:2210.03629
- **발표 필수:** Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유
- **선택 심화:** HotpotQA·ALFWorld 셋업
- **PDF:** [`W01_ReAct_2210.03629.pdf`](../papers/W01_ReAct_2210.03629.pdf)

#### 🟢 Chain-of-Thought Prompting Elicits Reasoning in LLMs
- **출처:** Wei et al., NeurIPS 2022 · arXiv:2201.11903
- **발표 필수:** CoT 핵심 아이디어와 추론 창발 조건
- **선택 심화:** 규모별 창발 곡선, self-consistency
- **PDF:** [`W01_Chain-of-Thought_2201.11903.pdf`](../papers/W01_Chain-of-Thought_2201.11903.pdf)

## 💬 토론 포인트 (교수 백업 질문)
에이전트와 단순 워크플로우의 경계는? CoT 없는 ReAct는 가능한가?

## 🛠 실습 — 누적 빌드 `docqa-agent`
**빌드 베이스:** from-scratch (내 모듈 직접 구현) · LLM 호출은 **aisuite** 래퍼(provider 무관)

*이번 주 주제:* 환경 세팅(Python 3.10+·aisuite·API 키/Ollama) → 원시 HTTP 호출로 API 내부 확인 → LLM 래퍼

**추가 모듈:** `llm.py` — (원시 API 1회 호출로 내부 확인 후) **aisuite**로 provider-무관 `chat()` 래퍼. *(ReAct 루프는 W2에서.)*
> ✅ **완료:** 원시 HTTP와 내가 채운 `chat()` 양쪽으로 같은 질문에 답을 받는다.

> 한 학기 하나의 앱을 쌓는다 · 스캐폴드 빈칸 채우기 + 주차별 체크포인트 → 상세는 [실습 가이드](../docs/practice-guide.md).

## 🎤 발표 진행 — 이번 주는 교수 시연 (상세는 [발표 가이드](../docs/presentation-guide.md))
- **학생 발표 없음** — CoT를 교수가 6장 템플릿·15분 하드 스톱 그대로 시연하고, 콜드 질문·지정 토론자 제도를 소개한다.
- 이 시간에 **W2~W15 발표자·지정 토론자 일괄 배정** (학생 발표는 W2부터).

## 📊 평가 루브릭 (W2부터 적용 — W1에 미리 공지)
| 항목 | 배점 | 기준 |
|---|---|---|
| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |
| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화는 직관 허용, 수식 생략 가능) |
| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |
| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |
