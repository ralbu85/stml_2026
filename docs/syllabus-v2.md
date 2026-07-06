# 머신러닝 특론 — LLM 에이전트 (2026) · 개정판 v2

> **부제:** 논문 읽기와 함께 만들기 — 16주, 주당 논문 2편 발표 + 매주 from-scratch 실습
> **대상:** 부산대/부경대 대학원 (난이도 중도 조정 — 과도한 심화 지양)
> **최종 산출물:** RAG 문서 QA 에이전트
> **난이도 범례:** 🟢 기초 · 🟡 중급 · 🔴 심화

이 문서는 원본 `syllabus.docx`를 **커버리지 검증(Berkeley LLM Agents 3개 학기 기준선)** 과 **난이도 재조정** 결과에 따라 개정한 버전이다. 변경 요약은 문서 하단 [부록 C](#부록-c-원본-대비-변경-요약) 참고.

---

## 설계 원칙 (유지)

- **보조읽기 / 발표논문 분리** — 산업체 가이드·서베이는 '보조 읽기'(발표 대상 아님), 학술 논문만 발표.
- **from-scratch → 10주 LangGraph 전환점** — 먼저 직접 짜고, 이후 프레임워크로.
- **토론 포인트 = 교수용 백업 질문** — 학생 발표가 부실해도 토론으로 보완하는 안전망.
- **난이도-무관 4항목 루브릭** — 핵심기여·방법이해·비판분석·연결확장 ([부록 B](#부록-b-발표-평가-루브릭)).
- **1주차 ↔ 16주차 수미상관** — "에이전트란 무엇인가"로 열고 "What is an Agent?"로 닫는다.

## 재조정 원칙 (신규)

1. 어떤 주도 **심화+심화로 두지 않는다** — 매주 🟢/🟡 앵커 1편 이상.
2. **잘라낸 3주:** RL 2주→1주(개념만) · 자기진화 주 삭제 · 멀티에이전트 2주→1주.
3. **넣은 3주:** 추론 모델 · GUI/컴퓨터 사용 · 안전·보안 (커버리지 검증에서 확인된 3대 공백).
4. **미검증 2026 논문 → 검증된 유명 논문으로 교체.**

---

## 주차별 계획

### Part 1 — 에이전트 기초 (from-scratch)

#### Week 1. 에이전트란 무엇인가 — 추론과 행동의 결합
- 📖 **보조읽기:** Anthropic — *Building Effective Agents* (워크플로우 vs 에이전트)
- 🛠 **실습:** 환경 세팅, LLM API 단일 호출 → ReAct 루프 골격(while 루프)
- 💬 **토론:** 에이전트와 단순 워크플로우의 경계는? CoT 없는 ReAct는 가능한가?
- **발표 논문**
  - 🟢 **ReAct: Synergizing Reasoning and Acting in LLMs** — Yao et al., ICLR 2023 · arXiv:2210.03629
    - *필수:* Think–Act–Observe 루프 구조와 추론·행동을 엮는 이유 / *심화(선택):* HotpotQA·ALFWorld 셋업
  - 🟢 **Chain-of-Thought Prompting Elicits Reasoning in LLMs** — Wei et al., NeurIPS 2022 · arXiv:2201.11903
    - *필수:* CoT 핵심 아이디어와 추론 창발 조건 / *심화(선택):* 규모별 창발 곡선, self-consistency

#### Week 2. 도구 사용 (Tool Use)
- 📖 **보조읽기:** Anthropic — *Writing Effective Tools for Agents* (도구 설계는 에이전트 UX)
- 🛠 **실습:** 도구 등록·파싱·실행 직접 구현 (계산기·검색 함수)
- 💬 **토론:** 도구가 많아질수록 좋은가? 도구 절벽(tool cliff)이 생기는 이유는?
- **발표 논문**
  - 🟡 **Toolformer: LMs Can Teach Themselves to Use Tools** — Schick et al., NeurIPS 2023 · arXiv:2302.04761
    - *필수:* self-supervised로 API 호출 위치를 학습하는 방식 / *심화(선택):* 호출 필터링 손실, 데이터 파이프라인
  - 🟡 **ToolLLM: Mastering 16000+ Real-world APIs** — Qin et al., ICLR 2024 · arXiv:2307.16789
    - *필수:* 대규모 실세계 API 학습 프레임과 DFSDT 탐색 / *심화(선택):* ToolBench 구축, pass/win rate

#### Week 3. 피드백·자기반성 (Reflection)
- 📖 **보조읽기:** Anthropic — *Demystifying Evals for AI Agents* (검증 루프를 하네스에 내장)
- 🛠 **실습:** 실패→언어 피드백→재시도 루프를 ReAct에 추가
- 💬 **토론:** 자기반성은 진짜 개선인가, 아니면 같은 오류의 반복인가?
- **발표 논문**
  - 🟡 **Reflexion: Language Agents with Verbal RL** — Shinn et al., NeurIPS 2023 · arXiv:2303.11366
    - *필수:* 언어 피드백이 gradient 없이 학습되는 메커니즘 / *심화(선택):* actor-evaluator-reflection 구조
  - 🟢 **Self-Refine: Iterative Refinement with Self-Feedback** — Madaan et al., NeurIPS 2023 · arXiv:2303.17651
    - *필수:* 단일 모델의 생성→비평→개선 반복 / *심화(선택):* 과제별 개선 폭, 피드백 프롬프트 설계

#### Week 4. 계획과 탐색 (Planning & Search)
- 📖 **보조읽기:** LangChain — *Plan-and-Execute Agents* (계획·실행 분리 하네스 패턴)
- 🛠 **실습:** 탐색 기반 추론(트리 분기) 미니 구현
- 💬 **토론:** 탐색 비용 대비 성능 이득은 언제 정당한가?
- **발표 논문**
  - 🟡 **Tree of Thoughts: Deliberate Problem Solving with LLMs** — Yao et al., NeurIPS 2023 · arXiv:2305.10601
    - *필수:* 사고를 트리로 분기·탐색(BFS/DFS)하는 발상 / *심화(선택):* 상태 평가 함수, Game of 24
  - 🟡 **ReWOO: Decoupling Reasoning from Observations** — Xu et al., 2023 · arXiv:2305.18323 *(원안 LATS🔴 교체 — 난이도 완화)*
    - *필수:* 계획을 관찰과 분리해 토큰·호출을 줄이는 구조 / *심화(선택):* planner/worker/solver 모듈 분해

---

### Part 2 — 추론과 지식

#### Week 5. 🆕 추론 모델 (Reasoning Models / Test-time Compute)
> **신규.** 2025–26 에이전트의 토대. RL(11주) 개념도 미리 깔린다. DeepSeek-R1은 유명·readable해 동기부여가 좋다.
- 📖 **보조읽기:** Lilian Weng — *Why We Think* (또는 DeepSeek-R1 해설) — test-time compute 직관
- 🛠 **실습:** self-consistency / 간단한 다중 샘플 추론 비교
- 💬 **토론:** '더 오래 생각하기'는 왜 성능을 올리나? 언제 과한가?
- **발표 논문**
  - 🟡 **STaR: Self-Taught Reasoner** — Zelikman et al., NeurIPS 2022 · arXiv:2203.14465
    - *필수:* 스스로 만든 추론으로 추론을 부트스트랩하는 아이디어 / *심화(선택):* rationalization 트릭
  - 🟡 **DeepSeek-R1: Incentivizing Reasoning via RL** — DeepSeek-AI, 2025 · arXiv:2501.12948
    - *필수:* 순수 RL로 추론이 창발하는 큰 그림('aha moment') / *심화(선택):* GRPO, cold-start 데이터

#### Week 6. 검색 증강 (RAG) — 1부: 기초
- 📖 **보조읽기:** Anthropic — *Effective Context Engineering for AI Agents* (컨텍스트를 유한 자원으로 큐레이션 · 최종프로젝트 직결)
- 🛠 **실습:** 임베딩→유사도→컨텍스트 주입 검색 직접 구현
- 💬 **토론:** 언제 검색해야 하는가? 항상 검색이 답인가?
- **발표 논문**
  - 🟡 **Retrieval-Augmented Generation for Knowledge-Intensive NLP** — Lewis et al., NeurIPS 2020 · arXiv:2005.11401
    - *필수:* 파라메트릭 vs 비파라메트릭(검색) 지식 결합 / *심화(선택):* RAG-Sequence vs Token, retriever 공동학습
  - 🟡 **Precise Zero-Shot Dense Retrieval without Labels (HyDE)** — Gao et al., ACL 2023 · arXiv:2212.10496
    - *필수:* 가설 문서를 생성해 검색 품질을 올리는 발상 / *심화(선택):* dense retriever와의 결합

#### Week 7. 검색 증강 (RAG) — 2부: 에이전틱 RAG
- 📖 **보조읽기:** Anthropic — *Code Execution with MCP* (도구 호출 오버헤드를 코드 실행으로 줄이기)
- 🛠 **실습:** 검색을 '도구'로 노출하고 에이전트가 단계별로 호출하게 개조
- 💬 **토론:** RAG를 도구로 만들면 무엇이 좋아지고 무엇이 어려워지나?
- **발표 논문**
  - 🟡🔴 **Self-RAG: Learning to Retrieve, Generate, and Critique** — Asai et al., ICLR 2024 · arXiv:2310.11511
    - *필수:* reflection token으로 검색 여부·품질을 스스로 판단 / *심화(선택):* critic 학습, segment beam search
  - 🟡 **Adaptive-RAG: Adapting Retrieval to Query Complexity** — Jeong et al., NAACL 2024 · arXiv:2403.14403 *(원안 미검증 2026 논문 교체)*
    - *필수:* 질의 난이도에 따라 검색 전략을 바꾸는 에이전틱 구조 / *심화(선택):* complexity classifier

#### Week 8. 메모리 (Memory)
- 📖 **보조읽기:** Letta (MemGPT) — *Agent Memory Blog* (3계층 메모리)
- 🛠 **실습:** 메모리 스트림 구현(저장·검색), 외부 메모리 통합
- 💬 **토론:** 무엇을 기억하고 무엇을 잊어야 하는가? 메모리 검색의 기준은?
- **발표 논문**
  - 🟡 **MemGPT: Towards LLMs as Operating Systems** — Packer et al., 2023 · arXiv:2310.08560
    - *필수:* 가상메모리 비유의 계층적 메모리(core/archival) / *심화(선택):* function-call self-editing, 페이징
  - 🟡 **MemoryBank: Enhancing LLMs with Long-Term Memory** — Zhong et al., AAAI 2024 · arXiv:2305.10250 *(원안 MEM1🔴 교체 — 난이도 완화)*
    - *필수:* 망각 곡선 기반 메모리 갱신·검색 / *심화(선택):* 사용자 페르소나 유지

---

### Part 3 — 협업과 환경

#### Week 9. 체화·평생학습 (Embodied / Lifelong)
- 📖 **보조읽기:** Anthropic — *Effective Harnesses for Long-Running Agents* (장기 과제 패턴)
- 🛠 **실습:** 재사용 가능한 스킬 라이브러리(도구 누적) 구현
- 💬 **토론:** 누적된 스킬이 항상 도움이 되는가? 망각이 필요한 순간은?
- **발표 논문**
  - 🟡 **Voyager: An Open-Ended Embodied Agent with LLMs** — Wang et al., 2023 · arXiv:2305.16291
    - *필수:* 스킬 라이브러리를 누적하는 평생학습 메커니즘 / *심화(선택):* automatic curriculum, 코드형 스킬
  - 🟡 **Generative Agents: Interactive Simulacra of Human Behavior** — Park et al., UIST 2023 · arXiv:2304.03442
    - *필수:* 메모리·반성·계획을 한 시스템에 통합 / *심화(선택):* 최신성·중요도·관련성 점수화

#### Week 10. 멀티에이전트 + LangGraph 전환점 ⭐
> **전환점.** from-scratch에서 프레임워크로. 원안의 Debate·CAMEL은 선택읽기로 이동.
- 📖 **보조읽기:** LangChain — *Choosing the Right Multi-Agent Architecture* (서브에이전트·핸드오프·라우터 비교)
- 🛠 **실습:** 역할 분담 멀티에이전트를 **LangGraph로 재구현·비교** (직접 구현 대비)
- 💬 **토론:** 멀티에이전트가 단일 에이전트보다 정말 나은가? 언제 과한가?
- **발표 논문**
  - 🟡 **AutoGen: Multi-Agent Conversation Framework** — Wu et al., COLM 2024 · arXiv:2308.08155
    - *필수:* 대화 기반 멀티에이전트 추상화와 역할 분담 / *심화(선택):* conversable agent, human-in-the-loop
  - 🟡 **MetaGPT: Meta Programming for Multi-Agent Collaboration** — Hong et al., ICLR 2024 · arXiv:2308.00352
    - *필수:* SOP(표준운영절차)를 코드화한 협업 구조 / *심화(선택):* 역할별 산출물 스키마
  - *선택읽기:* Multiagent Debate (arXiv:2305.14325), CAMEL (arXiv:2303.17760)

---

### Part 4 — 프런티어 (개념 위주)

#### Week 11. 에이전트 강화학습 (개념 1주 · 수식 생략)
> 원안 2주(전부 심화)를 **1주 개념 위주로 압축.** "수식은 직관만."
- 📖 **보조읽기:** Lilian Weng — *Reward Hacking in RL* (보상 설계의 함정)
- 🛠 **실습:** 간단한 보상 기반 도구 선택 시뮬레이션
- 💬 **토론:** 도구 사용을 왜 RL로 배워야 하나? RL 에이전트 vs 프롬프트 에이전트?
- **발표 논문**
  - 🔴 **ReTool: RL for Strategic Tool Use in LLMs** — 2025 · arXiv:2504.11536 *(수식 유도 생략 가능)*
    - *필수:* 도구 사용 시점·방법을 RL로 최적화하는 핵심 직관 / *심화(선택):* 코드 인터프리터 통합, outcome 보상
  - *선택읽기(자기진화):* Agentic Context Engineering, ReasoningBank — 원안 13주에서 이동

#### Week 12. 🆕 GUI · 컴퓨터/웹 사용 에이전트
> **신규.** WebArena·OSWorld는 시각적·직관적이라 흥미 유발이 잘 됨. 어렵지 않게 구성.
- 📖 **보조읽기:** *OS Agents: A Survey on MLLM-based Agents* (ACL 2025) — 컴퓨터·폰·브라우저 사용 개관
- 🛠 **실습:** 브라우저/도구 환경에서 관찰-행동 루프 (간단한 웹 태스크)
- 💬 **토론:** 텍스트 도구 호출 vs 화면 클릭 — 무엇이 언제 나은가?
- **발표 논문**
  - 🟡 **WebArena: A Realistic Web Environment for Building Agents** — Zhou et al., ICLR 2024 · arXiv:2307.13854
    - *필수:* 실제 웹 태스크 벤치마크 구성과 왜 어려운가 / *심화(선택):* 4개 도메인, 성공률 격차
  - 🟡 **Mind2Web: Towards a Generalist Agent for the Web** — Deng et al., NeurIPS 2023 · arXiv:2306.06070
    - *필수:* 실세계 웹사이트 일반화 과제와 데이터 / *심화(선택):* DOM 후보 선택, cross-website 일반화

#### Week 13. 🆕 안전·보안 (Safety & Security)
> **신규.** flagship 강의 3학기 만장일치 필수 주제. 프롬프트 인젝션·OWASP는 오히려 쉽고 실전적.
- 📖 **보조읽기:** *OWASP Top 10 for LLM Applications* (인젝션·과도한 권한 등) — 매우 접근성 높음
- 🛠 **실습:** 내 에이전트에 가드레일 추가 + 인젝션 공격 테스트
- 💬 **토론:** 행동하는 에이전트의 가장 위험한 실패는? 어디까지 자동화를 믿을 수 있나?
- **발표 논문**
  - 🟡 **Not What You've Signed Up For: Indirect Prompt Injection** — Greshake et al., AISec 2023 · arXiv:2302.12173
    - *필수:* 간접 프롬프트 인젝션이 왜 근본적 위협인가 / *심화(선택):* 실제 공격 시나리오 분류
  - 🟡 **InjecAgent: Benchmarking Indirect Injection in Tool-Integrated Agents** — Zhan et al., ACL 2024 · arXiv:2403.02691
    - *필수:* 도구 사용 에이전트의 인젝션 취약성 측정 / *심화(선택):* 공격 성공률, 방어 프롬프트 효과

---

### Part 5 — 평가와 마무리

#### Week 14. 평가와 벤치마크 (Evaluation) — 비판적 시각
- 📖 **보조읽기:** LangChain — *Agent Evaluation Readiness Checklist* (능력 평가 vs 회귀 평가 · 최종프로젝트 직결)
- 🛠 **실습:** 최종 프로젝트 설계 + 평가 하네스(정확도·비용·재현성) 골격
- 💬 **토론:** 무엇을 측정해야 하는가? 우리 RAG 에이전트의 성공 기준은?
- **발표 논문**
  - 🟢 **AI Agents That Matter** — Kapoor et al., 2024 · arXiv:2407.01502
    - *필수:* 리더보드의 함정, 비용을 무시한 정확도의 문제 / *심화(선택):* Pareto(정확도-비용), 재현성
  - 🟡 **τ-bench: Tool-Agent-User Interaction Benchmark** — Yao et al., ICLR 2025 · arXiv:2406.12045
    - *필수:* 실세계 도메인 도구-에이전트-사용자 상호작용 평가 / *심화(선택):* pass^k, 일관성 측정

#### Week 15. 단순함의 힘 — 에이전트가 꼭 필요한가
- 📖 **보조읽기:** HumanLayer — *Skill Issue: Harness Engineering* (대부분의 실패는 모델이 아니라 설정)
- 🛠 **실습:** 최종 프로젝트 구현 집중 (검색·메모리·평가 통합)
- 💬 **토론:** 복잡한 에이전트 vs 단순 파이프라인 — 우리 과제엔 무엇이 맞나?
- **발표 논문**
  - 🟢 **Agentless: Demystifying LLM-based Software Engineering Agents** — Xia et al., 2024 · arXiv:2407.01489
    - *필수:* 복잡한 에이전트 없이 단순 파이프라인이 더 나을 수 있다는 반론 / *심화(선택):* localize-repair-validate, SWE-bench
  - 🟡 **SWE-agent: Agent-Computer Interfaces Enable Automated SE** — Yang et al., NeurIPS 2024 · arXiv:2405.15793
    - *필수:* 에이전트-컴퓨터 인터페이스(ACI)가 성능을 가른다는 발견 / *심화(선택):* 명령·관찰 인터페이스 설계

#### Week 16. 최종 발표 — 자기 하네스 관점에서 방어
- 📖 **보조읽기:** Anthropic — *What is an Agent?* (1주차와 수미상관)
- 🛠 **실습:** 최종 발표 + 동료 평가 + 평가 리포트 제출
- 💬 **토론:** 학기를 통해 '에이전트'의 정의는 어떻게 바뀌었는가?
- **발표:** (논문 발표 없음) 각자 RAG QA 에이전트 발표
  - *필수:* 자기 에이전트의 하네스 설계 선택과 근거를 방어 / *심화(선택):* 평가 결과(정확도·비용)와 한계
  - *(보조)* 🟢 The Rise and Potential of LLM Based Agents: A Survey — Xi et al., 2023 · arXiv:2309.07864 — 학기 전체를 brain/perception/action으로 정리

---

## 부록 A. 참고 논문 큐레이션 (편향 방지용 교차 출처)

- **WooooDyy/LLM-Agent-Paper-List** — 학계 표준 분류(brain/perception/action) 정전
- **luo-junyu/Awesome-Agent-Papers** — Methodology·Applications·Challenges 서베이, 지속 업데이트
- **weitianxin/Awesome-Agentic-Reasoning** — 에이전트 추론 집중
- **thinkwee/AgentsMeetRL** — 에이전트 RL 카테고리·레포 모음
- **OS-Agent-Survey/OS-Agent-Survey** — GUI·컴퓨터/폰/브라우저 사용 에이전트 (ACL 2025 Oral) 🆕
- **VoltAgent/awesome-ai-agent-papers** — 2026 최신(엔지니어링·메모리·평가)
- **ai-boost/awesome-harness-engineering** — 하네스 엔지니어링 결정판

## 부록 B. 발표 평가 루브릭

| 항목 | 배점 | 기준 |
|---|---|---|
| 핵심 기여 | 30% | 논문의 기여를 한 문장으로 정확히 압축했는가 |
| 방법 이해 | 25% | 핵심 아이디어·메커니즘을 정확히 설명했는가 (심화 논문은 직관 수준 허용, 수식 유도 생략 가능) |
| 비판적 분석 | 25% | 가장 약한 가정·한계를 스스로 짚었는가 |
| 연결·확장 | 20% | 후속 논문 또는 본인/연구실 주제와 연결했는가 |

## 부록 C. 원본 대비 변경 요약

**커버리지 검증 기준선:** Berkeley CS294 LLM Agents (F24/Sp25/F25) 3개 학기 + 서베이 택소노미. 검증된 3대 공백을 반영.

**삭제 / 압축 (난이도 완화 · 3주 확보)**
- 원 11·12주 심화 RL 2주 → **1주(현 11주) 개념 위주로 압축**
- 원 13주 자기진화(ACE·ReasoningBank, 둘 다 심화·미검증 2026) → **삭제** (현 11주 선택읽기로 흡수)
- 원 10주 멀티에이전트 2부(Debate·CAMEL) → **현 10주로 병합**, Debate·CAMEL 선택읽기

**추가 (검증된 3대 공백)**
- **현 5주 추론 모델** (STaR, DeepSeek-R1) — 토대급, 접근성 높음
- **현 12주 GUI·웹 사용** (WebArena, Mind2Web) — 2024–26 최대 화두, 시각적·흥미로움
- **현 13주 안전·보안** (Indirect Prompt Injection, InjecAgent) — flagship 만장일치 필수, 실전적

**논문 교체 (난이도·검증)**
- 4주: LATS 🔴 → ReWOO 🟡
- 7주: A-RAG·ACC (미검증 2026) → Adaptive-RAG 🟡
- 8주: MEM1 🔴 → MemoryBank 🟡

**난이도 곡선:** 원안 후반 8편이 심화 → 개정판은 심화가 사실상 11주 1편(그마저 직관만). 부산대/부경대 수준에 맞춤.

**최종프로젝트 runway:** RAG(6–7)·메모리(8) 부품이 8주에 완성 → 9–15주 통합 여유 (원안 14–15주 크런치 개선).

> ⚠️ **인용 검증 대기:** 위 arXiv ID·저자·연도·venue는 유명 논문 위주로 골랐으나 전수 검증 전임. 배포 전 32편 전체 검증 권장.
