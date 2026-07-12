# docqa-agent 실습 스캐폴드 — 연구보조 검색·종합 에이전트

한 학기 동안 **연구보조 에이전트**(논문을 검색해 읽고 종합·답변)를 매주 모듈 하나씩 쌓아 완성한다.
코퍼스는 이 수업의 발표 논문 PDF(`papers/`) — 발표 준비하면서 자기 에이전트를 실제로 쓰게 된다.
설계 배경·전체 주차 계획은 [실습 가이드](../docs/practice-guide.md) 참고.

> **원칙:** 밑바닥부터 다 짜지 않는다 — 스캐폴드의 `TODO` 빈칸(주당 핵심 함수 1~2개)만 채운다.

## 1. 설치

**Python 3.10 이상 필수** (aisuite 요구사항 — `python3 --version` 으로 확인).

```bash
cd labs
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # 열어서 API 키 입력
```

API 키가 없으면 **Ollama(로컬·무료)** 로도 전 과정 진행 가능:

```bash
# https://ollama.com 설치 후
ollama pull llama3.2
# .env 에서: DOCQA_MODEL=ollama:llama3.2
```

## 2. 매주 하는 일

1. 그 주의 모듈 파일을 열고 `TODO(W주차)` 빈칸을 채운다.
2. **오프라인 테스트**로 로직을 검증한다 (API 키 불필요 — 가짜 LLM 주입):
   ```bash
   pytest tests/test_week01.py -v
   ```
3. 테스트가 통과하면 **데모**로 진짜 LLM과 돌려본다:
   ```bash
   python demos/week02_react.py "서울에서 부산까지 KTX로 몇 시간 걸려?"
   ```

## 3. 주차별 빈칸 · 완료 기준 (진행분)

| 주 | 파일 | 채울 함수 | ✅ 완료 기준 |
|---|---|---|---|
| 1 | (환경 세팅) + `docqa/llm.py` | `chat()` | 원시 HTTP와 aisuite 래퍼 양쪽으로 호출이 된다 (`test_week01.py` 통과) |
| 2 | `docqa/loop.py` | `parse_step()` | 루프가 한 바퀴 돌아 Final Answer를 낸다 (`test_week02.py` 통과) |
| 3 | `docqa/reasoning.py` | `majority_vote()` · `self_consistency()` | 애매한 질문에서 단일 답보다 정확도 ↑ (`test_week03.py` 통과) |
| 4 | `docqa/tools.py` | `run_tool()` · `calculator()` | 루프가 계산기를 **실제 호출**해 답한다 (`test_week04.py` 통과) |
| 5 | `docqa/planner.py` | `parse_steps()` · `run_plan()` | 2단계 질문을 계획대로 처리 (`test_week05.py`) |
| 6 | `docqa/reflect.py` | `reflect_retry()` | 처음 틀린 답을 재시도로 교정 (`test_week06.py`) |
| 7 | `docqa/retriever.py` 📦 | `cosine_topk()` · `Retriever.query()` | 논문 속 사실을 관련 청크로 답 (`test_week07.py`) |
| 8 | `docqa/tools.py` 📦 | `register_search()` | 논문 질문만 검색한다 (`test_week08.py`) |
| 9 | `docqa/context.py` | `fit_budget()` | 예산 내 선별 + 양끝 배치 (`test_week09.py`) + 🏁 중간 데모 |
| 10 | `docqa/memory.py` 📦 | `remember()` · `recall()` | 이전 세션 정보를 기억 (`test_week10.py`) |
| 11 | `docqa/graph.py` 🔄 | `build_graph()` | from-scratch와 동일 동작을 그래프로 (`test_week11.py`, langgraph 필요) |
| 12 | `docqa/tools_web.py` | `fetch_url()` | 웹에서 정보 가져와 답 (`test_week12.py`) |
| 13 | `eval/harness.py` | `grade()` · `run_eval()` | 내 에이전트 점수표 출력 (`test_week13.py`) |
| 14 | `docqa/guardrails.py` | `scan()` · `guard_observation()` | 오염 문서의 인젝션이 막힌다 (`test_week14.py`) |
| 15 | `app.py` | `agent_answer()` — 조립뿐 | 완성 + 베이스라인 대비 평가 (`test_week15.py`) |
| 16 | — | 최종 발표 | `demos/week13_eval.py` 점수표로 방어 |

W1은 빈칸을 채우기 전에 `demos/week01_raw_api.py`를 먼저 실행해 **원시 HTTP 호출의 내부**(우리가 감싸려는 것의 정체)를 눈으로 확인한다.

## 4. 뒤처졌을 때 — 체크포인트

`checkpoints/weekNN/`에 그 주의 **참조 구현**이 각 주가 끝난 뒤 공개된다.
전주를 못 끝냈으면 참조 구현을 자기 `docqa/`에 복사하고 이번 주를 시작하면 된다.
**전주 실패가 다음 주를 막지 않는다.**

```bash
cp checkpoints/week01/*.py docqa/
```

> (교수용 노트) 학생 배포 시에는 `checkpoints/`를 비우고 시작, 매주 종료 시점에 해당 주 폴더를 push한다.

## 5. 구조 (16주 후 최종 모습은 실습 가이드 참고)

```
labs/
  docqa/            # 매주 자라는 에이전트 패키지 ← 여기의 빈칸을 채운다
    llm.py          #  W1  LLM 호출 래퍼 (aisuite)
    loop.py         #  W2  ReAct 제어 루프
    reasoning.py    #  W3  self-consistency
    tools.py        #  W4  도구 레지스트리·실행 (+ W8 검색 도구 등록)
    planner.py      #  W5  계획 분해·실행
    reflect.py      #  W6  실패→피드백→재시도
    retriever.py    #  W7  청킹→임베딩→코사인 top-k 📦
    context.py      #  W9  토큰 예산·양끝 배치
    memory.py       #  W10 단기+장기 메모리 📦
    graph.py        #  W11 LangGraph 전환점 🔄
    tools_web.py    #  W12 웹 도구 (fetch·arXiv)
    guardrails.py   #  W14 인젝션 가드레일
  eval/             #  W13 평가 하네스 + 논문 QA 테스트셋(10문항)
  app.py            #  W15 통합 — 연구보조 에이전트 완성본
  data/             # 실습용 샘플 문서
  tests/            # 오프라인 테스트 (가짜 LLM — 키 불필요)
  demos/            # 진짜 LLM으로 돌리는 주차별 데모
  checkpoints/      # 주차별 참조 구현 (각 주 종료 후 공개)
```
