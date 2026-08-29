# 실습 가이드 — 전반부 Ng, 후반부 프레임워크

> **목표:** 하나의 **연구보조 검색·종합 에이전트(`docqa-agent`)** 를 학기 내내 쌓는다.
> 코퍼스 = 이 수업의 발표 논문 PDF(`papers/`) — 발표를 준비하며 자기 에이전트를 실제로 쓴다.
> **구조:** 전반부(W1–10)는 Andrew Ng *Agentic AI* 강의를 거의 그대로 따라가며 우리 것을 덧붙이고,
> 후반부(W11–16)는 LangGraph 프레임워크 위에서 더 복잡한 작업을 수행한다.

## 실습 스타일 — 프롬프트·흐름 중심, 메커니즘은 한 번씩 열어본다 (2026-07 확정)

배관(LLM 호출·도구 실행·검색·메모리)은 제공 라이브러리 **`docqa/agent_lib.py`** 에 감추고,
학생은 노트북에서 **프롬프트와 흐름 배선**만 다룬다. 파서·임베딩·AST·토큰 산식을 재구현하지 않는다.

프롬프트 일변도가 되지 않도록 균형을 둔다:
- **깊이 셀("내부 열어보기")** — 핵심 메커니즘은 주당 한 번, 재구현이 아니라 *한 번 들여다본다*. 예: W6은 aisuite가 감춘 구조화된 `tool_calls`, W9는 코사인 유사도를 손으로 한 번 계산.
- **후반부(W11–16)는 아키텍처가 초점** — LangGraph의 노드·엣지·상태·조건 분기·체크포인트·HITL을 짠다. 프롬프팅이 아니라 시스템 구조를 다룬다. 전반부(프롬프트·흐름) + 후반부(아키텍처)로 강의 전체가 균형을 이룬다.
- 알고리즘의 수학(RL·GRPO·코사인·RRF·LLMLingua)은 **이론 노트와 논문 발표**가 담당한다. 실습은 직관과 하네스 조립에 집중한다.

매주 노트북: 관찰(제공 코드 실행) → 프롬프트/흐름 채우기(`### 여기를 채우세요 ###`) → 실행·관찰 → 측정 → **연습문제**(예측→실행→확인 + 창의 과제). 참조 답안은 `checkpoints/weekNN/solution.py`.

## 설계 원칙

1. **이론과 완전 분리.** 실습은 이론 주차와 정렬하지 않는다. Ng의 패턴(반성·계획·멀티에이전트)이 해당 이론 장보다 먼저 나와도 무방하다 — Ng 랩은 자체 설명을 갖춘 완결 자료다. 실습의 순서는 Ng 강의의 모듈 순서(M1→M5)와 docqa-agent 빌드의 공학적 순서만 따른다.

2. **Ng 자료의 재집필 활용.** 원본을 100% 복사하지 않는다. **코드 구조(함수명·시그니처·워크플로 형태)는 거의 그대로 유지**하고, **설명 마크다운은 우리가 다시 쓰며**(집필 규정 §2·6 적용), 덧붙임 절(우리 코퍼스 포팅·미니 evalset)을 더한다. 각 노트북 헤더에 출처를 명기한다. 원본은 `materials/repos/agentic_ai_andrew`(커뮤니티 미러, 수업 준비 참고용).

3. **후반부는 프레임워크가 값을 하는 일만.** 조건 분기 라우팅, 체크포인팅(세션 재개), interrupt 승인 게이트(HITL), supervisor 협업, 트레이스 관측은 from-scratch로 짜면 무겁고 LangGraph 추상으로는 짧다. 힘든 로직은 전반부에서 이미 손으로 짜 봤으므로, 후반부의 부담은 LangGraph 문법 1회 학습뿐이다.

## 전반부 (W1–10) — Ng *Agentic AI* 따라가기 + 우리 덧붙임

W4–8이 Ng의 다섯 모듈에 1:1로 대응한다. 각 주의 코드는 Ng 모듈의 구조를 그대로 이식하고, 설명과 덧붙임만 우리 것이다.

| 주 | 자료 | 추가 모듈 | 하는 일 | ✅ 완료 기준 |
|---|---|---|---|---|
| 1 | Ng 스택 | `llm.py` | 원시 API 1회 → `aisuite` 래퍼 | 양쪽 호출 성공 |
| 2 | 우리 | (프롬프트 실험) | 직접 질의 vs CoT vs exemplar 정답률 | 정답률 표 기록 |
| 3 | 우리 | `reasoning.py` | self-consistency(N샘플 다수결) | N=1 대비 정확도↑·비용 기록 |
| 4 | **Ng M1** | `research_tools.py`·`workflow.py` | 리서치 워크플로 전체 실행·해부 — `planner_agent` → `research_agent`(arXiv·위키·웹 도구) → `writer_agent` → `editor_agent`, `executor_agent_step` history 루프 | 우리 논문 주제로 보고서 1편 생성 |
| 5 | **Ng M2** | `reflect.py` | Reflection — `generate_draft` → `reflect_on_draft` → `revise_draft` | 반성 1회가 초안을 측정 가능하게 개선 |
| 6 | **Ng M3** | `tools.py` | Tool Use — aisuite `tools=`·`max_turns` 자동 실행, 수동 `tool_calls` 처리. **덧붙임: 수제 JSON 왕복**(블랙박스 열기 — 파싱·오류 재주입을 손으로) | `test_week06.py` 통과 + 오호출률 비교 |
| 7 | **Ng M4** | `evals.py` | 컴포넌트 평가 — `evaluate_…(min_ratio)` PASS/FAIL + 리포트. **덧붙임: docqa 미니 evalset 5문항**(이후 매주 누적) | 컴포넌트 평가 PASS + evalset 첫 채점 |
| 8 | **Ng M5** | `team.py` | Multi-agent — planner/executor 협업, 역할별 에이전트 팀 | 다단계 과제를 팀이 분담 처리 |
| 9 | 우리 📦 | `retriever.py` | RAG 검색기 — `papers/` 청킹→임베딩→top-k, 검색을 도구로 등록 (Ng `arxiv_search_tool`을 코퍼스 수집기로 차용) | 논문 질문만 검색해 답 |
| 10 | 우리 📦 | `memory.py`·`context.py` | 장기 메모리 + 토큰 예산. 🏁 **전반부 통합 데모** — Ng 워크플로 + 우리 검색·메모리 합체 | 이전 세션 기억 + 예산 내 품질 |

## 후반부 (W11–16) — LangGraph로 복잡한 작업

| 주 | 추가 모듈 | 하는 일 | 프레임워크라서 되는 것 | ✅ 완료 기준 |
|---|---|---|---|---|
| 11 | `graph.py` | 🔄 전환점 — 전반부 부품을 노드로 감싸 재구성 | 상태 딕셔너리·조건 엣지·관측 | from-scratch와 동일 동작 |
| 12 | `tools_web.py` | 웹 도구 노드(Ng arxiv·tavily 도구 재사용) | 검색↔웹 조건 분기 라우팅 | 웹 정보로 답 |
| 13 | `eval/harness.py` | Ng M4 방식을 정식 하네스로 확장 | 그래프 트레이스에서 비용·지연 자동 수집, pass^k 축소판 | 내 에이전트 점수표 출력 |
| 14 | `guardrails.py` | 입출력 필터 + 오염 문서 레드팀 | interrupt 승인 게이트(HITL) | 인젝션 차단/우회 기록 |
| 15 | `app.py` | 통합 CLI(Ng M1 FastAPI 앱의 우리 판) + 단순 파이프라인 베이스라인 비교 | supervisor 멀티에이전트 + 체크포인터 영속 메모리 | 앱 완성, 베이스라인 대비 평가 |
| 16 | — | 최종 발표 | — | 데모 + 평가 리포트 방어 |

## Ng 노트북 골격 — 매주 랩의 표준

각 주 노트북은 Ng 랩의 사다리를 따른다.

1. **학습 목표** — 만드는 것과 완료 기준 3~4줄.
2. **Setup** — `aisuite`(W11부터 LangGraph) 클라이언트·데이터 로드.
3. **관찰(빈칸 없음)** — 완성 코드를 실행해 현상·워크플로를 확인한다(Ng UGL 방식).
4. **구현(명세 + TODO)** — 채울 함수마다 Objective·Inputs·Output·Requirements 블록과 빈칸. **빈칸의 단위는 알고리즘이 아니라 프롬프트 작성과 호출 인자 구성**(Ng GL 방식). 힌트는 두텁게.
5. **조립·실행** — `run_workflow()`로 합쳐 돌리고, 중간 산출물(프롬프트 전문·원시 출력·도구 호출)을 `utils` 박스로 가시화.
6. **측정** — 이번 주 산출물의 컴포넌트 하나를 수치로(Ng M4 방식). W7부터 미니 evalset 누적.
7. **연습문제** — 예측 → 실행 → 확인.

**채점.** 오프라인 `pytest`(가짜 클라이언트 주입, API 키 불필요)로 배선 검증 + 실LLM 스모크 테스트(타입·키 존재 ✅/❌). 채점 대상은 코드 정확성이지 내용 품질이 아니다(Ng와 동일).

## 성장하는 아키텍처

```
docqa/
  # ── 전반부: Ng 따라가기 (aisuite) ──
  llm.py             # LLM 호출 래퍼(aisuite)              (W1)
  reasoning.py       # CoT 실험·self-consistency            (W2–3)
  research_tools.py  # arXiv·위키·웹 검색 도구 (Ng M1 구조)  (W4)
  workflow.py        # planner→research→writer→editor (M1)  (W4)
  reflect.py         # generate→reflect→revise (M2)         (W5)
  tools.py           # 도구 왕복 — aisuite + 수제 (M3)       (W6)
  evals.py           # 컴포넌트 평가·미니 evalset (M4)       (W7)
  team.py            # 멀티에이전트 협업 (M5)                (W8)
  retriever.py       # RAG — papers/ 코퍼스 (우리)           (W9)
  memory.py, context.py  # 메모리·토큰 예산 (우리)           (W10)
  # ── 후반부: LangGraph ──
  graph.py           # 노드 재구성 (전환점)                  (W11)
  tools_web.py       # 웹 도구 노드                          (W12)
  guardrails.py      # 가드레일·HITL 노드                    (W14)
eval/
  harness.py         # 정확도·비용·재현성                    (W13)
  testset.jsonl
app.py               # 통합 CLI                              (W15)
checkpoints/weekNN/  # 주차별 참조 구현(뒤처진 학생용)
```

## 난이도를 낮추는 장치

1. **스캐폴드 + TODO** — 매주 뼈대 코드(시그니처·테스트·데이터)를 제공하고 핵심 함수만 채운다.
2. **주차별 체크포인트** — `checkpoints/weekNN/` 참조 구현. 전주 실패가 다음 주를 막지 않는다.
3. **최소 의존성** — 전반부는 `aisuite`+`numpy`+`requests`. LangGraph는 W11부터.
4. **명확한 완료 기준** — 매주 데모 또는 통과 테스트 1개. 추가 코드 ~30–80줄/주.

## LLM API 래퍼 — `aisuite`

- `provider:model` 문자열로 OpenAI·Anthropic·Google·**Ollama(로컬·무료)** 교체. 학생마다 API 사정이 달라도 코드 동일.
- W6 전까지는 Chat Completions 계층만 쓰고, W6(Ng M3)에서 `tools=`·`max_turns` 자동 도구 실행 계층을 연다.
- W4의 `research_tools.py` 중 arXiv·위키백과는 키가 필요 없고, 웹 검색(Tavily)은 키가 있을 때만 활성화된다.

## 스택 / 준비물

- **Python 3.10+**, `aisuite`, `numpy`, `requests`
- W9부터: 임베딩 API(또는 `sentence-transformers` 로컬)
- W11부터: `langgraph` · `requirements.txt`는 스캐폴드에 포함. API 키는 `.env`(gitignore).

## 운영

- 실습은 수업 중 60~80분(발표·이론 후). 완료 못 하면 체크포인트로 다음 주 시작.
- 교수는 `checkpoints/`에 참조 구현을 유지하고 각 주 끝에 공개.
- 최종 과제 = 이 저장소 + `eval/harness.py` 점수 + 발표([발표 가이드](presentation-guide.md)).

> 스캐폴드는 [`labs/`](../labs/)에서 재구축 중(2026-07-13 전면 초기화, 직전 상태는 git `079ab0a`). 전반부 W1–9 완료, W10부터 위 표대로.
