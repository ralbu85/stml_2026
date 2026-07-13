# 강의 참고자료 (materials/)

주차별 **이론 강의(30분)** 를 전개할 때 근거로 삼을 공개 강의자료 모음.
용량이 커서(약 2.1GB) 레포 본체는 `.gitignore` 처리 — 이 인덱스와 `fetch_materials.sh`만 버전관리.
재다운로드: `bash materials/fetch_materials.sh`

> ⚠️ **저작권:** 아래 자료는 각자 라이선스(대부분 MIT/Apache/CC)를 따른다. **강의 준비 참고용**으로 쓰고,
> 슬라이드·그림을 수업에 재사용할 때는 출처 표기. Berkeley 슬라이드는 각 강연자 저작으로 배포 조건 확인 권장.

## 자료 인벤토리

| 폴더 | 출처 | 무엇 | 우리 활용 |
|---|---|---|---|
| `repos/llm-agents-mooc/slides/` | UC Berkeley CS294 (MOOC) | **대학원 강의 슬라이드 PDF 28개** | 이론 백본 |
| `repos/ai-agents-for-beginners/` | Microsoft (MIT) | **12+강 구조화 레슨**(주차와 1:1) | 이론 구성·강의노트 |
| `repos/agents-course/` | Hugging Face | 유닛형 코스(한국어 `units/ko` 포함) | 이론+실습 |
| `repos/RAG_Techniques/` | NirDiamant | RAG 노트북 42개 | W5–6 실습·데모 |
| `repos/GenAI_Agents/` | NirDiamant | 에이전트 튜토리얼 53개 | 데모·최종프로젝트 예시 |
| `repos/anthropic-cookbook/` | Anthropic | 도구사용·RAG·에이전트 패턴 | 실습 레시피 |
| `repos/courses/` | Anthropic | 프롬프트·도구 코스 | 기초 보강 |
| `repos/llm-course/` | mlabonne | LLM 기초(양자화·파인튜닝) | 선수지식 보강 |
| `repos/agentic_ai_andrew/` | 커뮤니티 미러 | Andrew Ng Agentic AI 노트북 | 패턴 참고 |

> Andrew Ng/DeepLearning.AI 정식 슬라이드는 플랫폼 전용(비공개). 위 미러는 companion 노트북 수준.

## 주차별 이론 30분 플랜 (무엇을 강의할지 + 근거 자료)

> ⚠️ **구판 — 옛 주차 순서 기준.** 현행 순서(v4 · 프롬프팅과 추론 W2, 도구 W3, 루프 W4, RAG W5–6, 계획 W7, 반성 W8)로 재작성한 확정판은
> [`docs/lecture-outlines.md`](../docs/lecture-outlines.md) 참조. 아래 표는 자료 매핑 기록용으로만 남긴다.

| 주 | 이론 30분에 다룰 핵심 개념 | 근거 자료 |
|---|---|---|
| **1** 에이전트란 | ① 에이전트 vs 워크플로우 정의 ② 자율성 스펙트럼 ③ ReAct 추론–행동–관찰 루프 | Berkeley `intro.pdf`·`llm_agent_history.pdf` · MS `01`,`03` · HF `unit1` |
| **2** 도구 사용 | ① 함수 호출 메커니즘 ② 도구 스키마·파싱·에러 ③ 도구 선택 문제(절벽) | MS `04-tool-use` · anthropic-cookbook `tool_use` · Berkeley `agentworkflows.pdf` |
| **3** 자기반성 | ① 생성→비평→개선 루프 ② 언어 피드백 vs gradient ③ 메타인지 | MS `09-metacognition` · `agentic_ai_andrew`(reflection) |
| **4** 계획·탐색 | ① 과제 분해 ② 계획–실행 분리 ③ 트리 탐색(BFS/DFS/MCTS 직관) | MS `07-planning-design` · Berkeley `language_agents_YuSu`·`102824-yuandongtian.pdf` |
| **5** 추론 모델 | ① CoT→self-consistency→test-time compute ② RL로 추론 창발(R1) ③ STaR 부트스트랩 | Berkeley `inference_time_techniques_lecture_sp25.pdf`·`llm-reasoning.pdf`·`Jason-Weston-Reasoning...pdf`·`OLMo-Tulu-Reasoning-Hanna.pdf` |
| **6** RAG 기초 | ① 임베딩·벡터검색 ② retriever–reader ③ 컨텍스트 엔지니어링 | MS `12-context-engineering` · `RAG_Techniques`(기초 노트북) · Berkeley `MKA.pdf` |
| **7** 에이전틱 RAG | ① 검색을 '도구'로 ② adaptive/self 검색 ③ MCP | MS `05-agentic-rag`+`11-agentic-protocols` · HF `unit3` · `RAG_Techniques`(고급) · GenAI `mcp-tutorial.ipynb` |
| **8** 메모리 | ① 단기 vs 장기 ② 계층적 메모리(OS 비유) ③ 검색 기준(최신성·중요도·관련성) | MS `13-agent-memory` · GenAI `memory-agent-tutorial.ipynb` · Berkeley `language_agents_YuSu` |
| **9** 체화·평생학습 | ① 스킬 라이브러리 누적 ② automatic curriculum ③ 시뮬 환경 상호작용 | Voyager·Generative Agents 논문 · GenAI `self_improving_agent.ipynb` |
| **10** 멀티에이전트+LangGraph | ① 협업 아키텍처(핸드오프·라우터) ② 그래프 실행 모델 ③ 프레임워크 비교 | MS `02`+`08-multi-agent` · HF `unit2` · Berkeley `autogen.pdf`·`dspy_lec.pdf` · GenAI `langgraph-tutorial.ipynb` |
| **11** 에이전트 RL(개념) | ① 보상 설계 직관 ② RLHF→RLVR ③ 도구학습 보상 *(수식 생략)* | Berkeley `OLMo-Tulu-Reasoning-Hanna.pdf`·`dawn-agentic-ai.pdf` |
| **12** GUI·웹 사용 | ① 화면 관찰–행동 루프 ② DOM vs 스크린샷 ③ 벤치마크(WebArena/OSWorld) | MS `15-browser-use` · Berkeley `ruslan-multimodal.pdf`·`Multimodal_Agent_caiming.pdf` |
| **13** 안전·보안 | ① 프롬프트 인젝션(직접/간접) ② 신뢰 경계·최소권한 ③ 가드레일·RSP | MS `06-building-trustworthy`+`18-securing` · Berkeley `antrsp.pdf`·`dawn-agentic-ai.pdf` |
| **14** 평가 | ① 능력 평가 vs 회귀 평가 ② 비용–정확도 Pareto ③ 재현성 | Berkeley `percyliang.pdf` · MS `10`(일부) · 논문 AI Agents That Matter |
| **15** 단순함·프로덕션 | ① 언제 에이전트가 과한가 ② 프로덕션 하네스 ③ ACI 설계 | MS `10-ai-agents-production` · Berkeley `neubig24softwareagents.pdf`·`Burak_slides.pdf` |
| **16** 최종 발표 | ① 학기 회고 ② brain/perception/action 프레임 ③ 에이전트 재정의 | HF `unit4` · Survey(Xi et al.) 논문 |

## 사용법 제안

1. **Berkeley 슬라이드**를 그 주 이론의 뼈대로 삼되, 30분에 맞게 3~4개 개념만 발췌.
2. **Microsoft 레슨**의 서술형 텍스트를 강의노트 초안으로 활용(주차와 거의 1:1).
3. **노트북(RAG_Techniques·GenAI_Agents)** 은 이론 중 라이브 데모 1개로 활용 → 이후 실습으로 연결.
4. 슬라이드는 `weeks/weekNN.md`의 `theory` 자리에 요지·출처를 적어 확정.
