# 실습 가이드 — 한 학기 하나의 앱을 쌓아 올린다

> **목표:** 매주 from-scratch로 **모듈 하나**씩 추가해, 16주 뒤 **문서 QA 에이전트(`docqa-agent`)** 를 완성한다.
> **원칙:** 밑바닥부터 다 짜지 않는다 — **스캐폴드의 빈칸(핵심 함수 1~2개)을 채운다.**

## 왜 누적 빌드인가

매주 독립 실습은 서로 안 이어져 "만든 느낌"이 안 남는다. 대신 **하나의 저장소가 매주 자란다.**
학생은 학기 내내 자기 에이전트가 똑똑해지는 걸 눈으로 본다 → 동기부여 + 최종 발표에서 방어할 자기 작품.

## 너무 어렵지 않게 만드는 4가지 장치 ★

1. **스캐폴드 + TODO** — 매주 뼈대 코드(시그니처·테스트·데이터)를 제공. 학생은 핵심 함수만 채운다. *(빈칸 채우기, 백지 아님)*
2. **주차별 체크포인트** — 각 주 시작 시 `checkpoints/weekNN/` 참조 구현을 받을 수 있다. **전주 실패가 다음주를 막지 않는다**(주차 간 디커플링).
3. **최소 의존성** — LLM SDK + `numpy`(코사인 유사도) 중심. 무거운 벡터DB·LangGraph는 필요한 주(6·10)에만.
4. **명확한 완료 기준** — 매주 "이 쿼리가 되면 끝" 데모 또는 통과 테스트 1개. 추가 코드 분량 **~30–80줄/주**.

## 성장하는 아키텍처

```
docqa/
  llm.py         # LLM 호출 래퍼            (W1)
  loop.py        # ReAct 제어 루프          (W1)
  reasoning.py   # self-consistency         (W2)
  tools.py       # 도구 레지스트리·실행     (W3) → 검색도구 등록 (W7)
  planner.py     # 계획 분해                (W4)
  reflect.py     # 재시도·자기반성          (W5)
  retriever.py   # 임베딩·검색              (W6)
  context.py     # 컨텍스트 예산·압축       (W8)
  memory.py      # 단기·장기 메모리         (W9)
  graph.py       # LangGraph 재구현         (W10)
  tools_web.py   # 웹 도구                  (W11)
  guardrails.py  # 가드레일·인젝션 방어     (W14)
eval/
  harness.py     # 평가(정확도·비용·재현성) (W13)
  testset.jsonl
notebooks/
  sim_rl.ipynb   # 보상 기반 도구선택 시뮬  (W12, 개념)
app.py           # 통합 CLI                 (W15)
checkpoints/weekNN/   # 주차별 참조 구현(뒤처진 학생용)
```

## 프레임워크 전환 경계 (W10) ★

**"감싸기(wrap), 버리기 아님."** from-scratch로 짠 코드를 W10에서 LangGraph 노드의 '속'으로 재사용한다.

| 구간 | 빌드 베이스 |
|---|---|
| **W1–9** | **from-scratch** — `retriever.py`·`memory.py`·`tools.py` 등을 직접 구현 (LLM 호출만 aisuite) |
| **W10** | 🔄 **전환점** — 위 모듈들을 **LangGraph 노드로 감싼다**. 오케스트레이션·상태만 프레임워크에 위임 |
| **W11·13·14·15** | **LangGraph 위에서 확장** — 웹도구·가드레일=노드, eval=바깥에서. **W1–9 모듈 그대로 재사용** |
| **W12** | 개념 노트북 (프레임워크 무관) |

> **왜 후반이 더 쉬워지나:** 멀티에이전트·메모리 연결·웹도구 같은 복잡한 후반 기능은 그래프/상태 모델로 하면 from-scratch보다 간단하다. 힘든 로직은 이미 W1–9에서 손으로 짜서 이해한 상태이므로, W10의 부담은 *LangGraph 기본 문법 1회 학습*뿐이다.
> **대안:** 프레임워크 의존을 피하려면 W10을 비교용 1회 실습으로만 두고 W11–16을 from-scratch 본선으로 유지할 수 있다(후반 난이도 ↑).

## LLM API 래퍼 — Andrew Ng `aisuite` 채택 ★

`llm.py`는 [**aisuite**](https://github.com/andrewyng/aisuite)(Andrew Ng, 얇은 통합 래퍼)로 감싼다.

- **왜:** `provider:model` 문자열 하나로 OpenAI·Anthropic·Google·**Ollama(로컬·무료)** 를 교체. 학생마다 API 사정이 달라도 코드 동일 → 접근성 ↑.
- **from-scratch 유지:** aisuite는 **provider 호출 배관만** 감싼다. 에이전트 로직(루프·도구·메모리)은 학생이 직접 구현하므로 철학과 충돌 없음.
- **주의:** aisuite의 **Agents/tools 레이어는 사용하지 않는다**(그건 W3에서 학생이 직접 만들 부분). **Chat Completions 계층만** 사용.
- **W1 순서:** 원시 provider API를 1회 호출해 내부를 본 뒤 → aisuite로 감싼다.

## 주차별 빌드 (📦 = 최종 앱 핵심 부품)

| 주 | 추가 모듈 | 하는 일 | ✅ 완료 기준 |
|---|---|---|---|
| 1 | `llm.py`·`loop.py` | ReAct while 루프 골격 | 간단한 질문에 루프가 한 바퀴 돌아 답 |
| 2 | `reasoning.py` | self-consistency(N샘플 다수결) | 애매한 질문 정확도 ↑ |
| 3 | `tools.py` | 도구 등록·파싱·실행(계산기 등) | 루프가 계산기 도구를 실제 호출 |
| 4 | `planner.py` | 질문→하위 단계 분해·실행 | 2단계 질문을 계획대로 처리 |
| 5 | `reflect.py` | 실패→피드백→재시도 | 처음 틀린 답을 재시도로 교정 |
| 6 | `retriever.py` 📦 | 청킹→임베딩→코사인 top-k | 문서 속 사실을 물으면 관련 청크로 답 |
| 7 | (retriever→도구) 📦 | 검색을 도구로, 필요시만 호출 | 상식은 검색 안 함 / 문서질문만 검색 |
| 8 | `context.py` | 토큰 예산·정렬·압축 | 문서 많아도 예산 내 품질 유지 |
| 9 | `memory.py` 📦 | 단기+장기 메모리 | 이전 세션 정보를 다음 세션에서 기억 |
| 10 | `graph.py` | LangGraph 재구현·비교 | from-scratch와 동일 동작을 그래프로 |
| 11 | `tools_web.py` | URL fetch/웹검색 도구 | 웹에서 정보 가져와 답(간단) |
| 12 | `notebooks/sim_rl.ipynb` | 보상 기반 도구선택 시뮬(개념) | 보상으로 선택이 개선됨을 관찰 |
| 13 | `eval/harness.py` | 정확도·비용·지연·재현성 측정 | 내 에이전트 점수표 출력 |
| 14 | `guardrails.py` | 가드레일 + 간접 인젝션 레드팀 | 오염 문서의 인젝션이 막힘 |
| 15 | `app.py` | 전체 통합 + 베이스라인 비교 | 앱 완성, 단순 파이프라인 대비 평가 |
| 16 | — | 최종 발표 | 데모 + 평가 리포트 방어 |

## 스택 / 준비물

- **Python 3.10+**, **`aisuite`**(통합 LLM 래퍼, 키 없으면 Ollama 로컬), `numpy`
- 6주부터: 임베딩 API (또는 `sentence-transformers` 로컬)
- 10주: `langgraph` (여기서부터 빌드 베이스) · 11주: `requests`/`beautifulsoup4`
- `requirements.txt`는 스캐폴드에 포함 예정. API 키는 `.env`(gitignore).

## 운영 팁

- 실습은 **수업 중 60~80분** 진행(발표·이론 후). 완료 못 하면 그 주 체크포인트로 다음주 시작.
- 교수는 `checkpoints/`에 참조 구현을 유지, 각 주 끝에 공개.
- 최종 과제 = 이 저장소 + `eval/harness.py` 점수 + 발표([발표 가이드](presentation-guide.md)).

> 스캐폴드는 [`labs/`](../labs/)에서 제작 중 — **W1·W2 완료**(빈칸 + 오프라인 테스트(가짜 LLM, 키 불필요) + 체크포인트 참조 구현). W3부터는 해당 주 덱과 함께 한 세트로 추가한다.
