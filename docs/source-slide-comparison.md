# MS·버클리 원자료 실물 내용 비교 (슬라이드/레슨 단위)

> ⚠️ **주차 번호 주의:** 이 문서는 재배열(2026-07-10) *이전* 번호 기준이다. 변환: 구 W1~W11 → 신 W2~W12 (+1), 구 W12(RL)는 삭제·흡수, W13~16 동일.

> 2026-07-10 작성. MS ai-agents-for-beginners **레슨 16개 전문** + 버클리 LLM Agents MOOC(F24·SP25) **슬라이드 PDF 17덱 전량**(수학 4연강·로보틱스 제외)을 직접 읽고 대조한 기록.
> 용도: 주차별 이론 덱을 만들 때 "무엇을 어느 자료에서 가져올지"의 근거. 수치는 모두 원본 슬라이드 페이지 확인 완료.

## 한 줄 결론

**MS = 운영 어휘·체크리스트 공급원(우리 '현장 노트' 층), 버클리 = 형식화·실패 수치·논문 계보(이론 층).** 두 자료는 거의 겹치지 않는 상호보완 관계이며, 우리 덱의 2층 구조(이론 + 현장 노트)가 이 분업과 일치한다.

## MS 레슨 판정표

| 판정 | 레슨 | 요지 |
|---|---|---|
| **뼈대로 사용** | 04 도구 | raw API 함수호출 왕복 전체(스키마→`tool_calls`→실행→`role:"tool"` 재주입) + 6빌딩블록. 코스 최고 레슨 |
| **뼈대로 사용** | 10 프로덕션 | Trace/Span, 지표 7종(암묵적 피드백 포함), 오프라인→온라인 평가 루프, 비용 3전략(SLM·라우터·캐싱), OTel |
| **뼈대로 사용** | 12 컨텍스트 | 컨텍스트 5유형, 전략 6종(스크래치패드·메모리·압축·분리·샌드박스·상태객체), **실패 4종(Poisoning/Distraction/Confusion/Clash)**, "도구 30개 미만" |
| **뼈대로 사용** | 13 메모리 | **7유형 분류**(Working/Short/Long/Persona/Episodic/Entity/Structured-RAG), Mem0 2단계(추출→LLM이 add/modify/delete), 실노트북 2개 |
| 사용 | 15 CUA | Browser-Use+Playwright 하이브리드, **agent vs actor 판단표**(동적 레이아웃→에이전트 / 알려진 구조→스크립트) |
| 개념만 발췌 | 01, 05, 06, 08, 11 | 01: 7유형 분류+"언제 에이전트" 3기준 · 05: maker-checker 루프(유일하게 논문 인용: Self-Refine/Reflexion/CRITIC) · 06: 위협 5분류 · 08: Group Chat/Hand-off/Collaborative Filtering 3패턴 · 11: MCP(Hosts/Clients/Servers + Tools/Resources/Prompts)·A2A(Agent Card)·NLWeb 구성요소 수준 |
| **강등** | 02, 03, 09, 14, 18 | 02: MS 제품 비교(마케팅) · 03: UX 원칙론 · 09: 1434줄 최장이나 목업 의사코드(전략 전환 사례 하나만 건짐) · 14: 자사 SDK · 18: 일반 보안 아님(암호학적 영수증 단일 주제) |

**중대 사실관계:** 현행 MS 레포는 **AutoGen/Semantic Kernel 삭제 → Microsoft Agent Framework(MAF)로 전면 재작성**됨. W10 프레임워크 지형도에 반영 필요.

**MS의 구멍(버클리가 메움):** 추론 모델(W2), RL(W12), 벤치마크·평가 수치, 보안 깊이, 논문 인용 전반.

## 버클리 덱별 핵심 (주차순)

### W1 — Shunyu Yao "LLM Agents: Brief History" (71장, F24)
- 3단 포섭: 텍스트 에이전트 ⊃ LLM 에이전트 ⊃ **추론 에이전트**. **Â = A ∪ L** — 추론은 무한 언어공간의 *내부 행동*(컨텍스트만 갱신).
- QA 사례연구: 패치 난립(PoT·RAG·Toolformer·Self-ask) → "추상화가 필요하다" → ReAct.
- 어드버서리얼 관찰 데모(가짜 검색결과 → 추론으로 우회), ALFWorld pepper-shaker(Act-only 무한루프 vs ReAct).
- ReAct PaLM-540B: HotpotQA 35.1 / FEVER 64.6 / ALFWorld 71 (p.31). Reflexion HumanEval 67→91 (p.38).
- 5대 과제: 훈련(FireAct 21.2→34.4), 인터페이스(ACI), 강건성(τ-bench pass^k 붕괴, p.68), 인간협업, 벤치마크. 임팩트 피라미드.

### W2 — Denny Zhou "LLM Reasoning" (87장, F24)
- 마지막 글자 잇기: CoT 시연 1개로 100% (p.15). Least-to-Most: SCAN 16.7→**99.7** (p.25).
- 이론 근거: 충분히 긴 중간 스텝이면 상수 깊이 트랜스포머도 직렬 문제 해결(Li et al. ICLR 2024, p.28-30).
- CoT-Decoding(프롬프트 없이 top-k 안에 추론 경로, GSM8K 34.8→61.5, p.47). Self-consistency: PaLM-2+SC GSM8K 92 (p.53).
- **한계 3종**: 무관 문맥 20+pt 하락(p.63) · **오라클 없인 자기교정 불가**(GPT-4 95.5→89.0 악화, CSQA 75.8→38.1, p.69; 오라클이면 95.5→97.5, p.70) · 전제 순서 30+pt(p.77). 멀티에이전트 토론(9응답) 83.0 < SC(9) 88.2 (p.71).
- 마지막 장: "이 기법들을 **스스로 학습**하는 모델을 만들라" — 우리 W2 도입과 접합.

### W2 심화 — Xinyun Chen "Inference-Time Techniques" (74장, SP25)
- test-time compute 3분류: ①단일 해 프롬프팅 ②병렬 샘플+선택 ③순차 자기개선 — 우리 W2 5–15분 구간과 동일 구조.
- o1 도입 수치: AIME 13.4→83.3, Codeforces 11→89 percentile (p.2); ARC-AGI o3 87.5%인데 **태스크당 $1k+** (p.3) — 비용축 강의에 인용.
- **PRM > ORM**: MATH best-of-1860에서 78.2 > 72.4 > 다수결 69.6 (p.51-52). ToT game-of-24: 4%→74% (p.56).
- "Don't think. Just feel." → MultiArith 18.8로 추락 (p.23); OPRO "Take a deep breath" 80.2 (p.27).
- Snell et al. 순차/병렬 최적 배합은 난이도 의존 (p.69). Bitter Lesson으로 마무리.

### W2/W12 — Jason Weston "Learning to Reason" (106장, SP25)
- 하나의 연구 프로그램: 모델이 **자기 훈련신호를 스스로 생성** — Self-Rewarding(judge 루브릭+반복 DPO, AlpacaEval 9.94→20.44%) → Iterative RPO(검증가능 보상+DPO+NLL, GSM8K 55.6→81.6; **STaR 직접 비교 65.2 vs 73.1**, p.76) → R1 요약(p.79-82) → TPO → Meta-Rewarding → EvalPlanner.
- 핵심 그림: SFT는 *거부된* 체인의 확률도 올린다 — DPO+NLL이 분리(p.74). 병목 = 검증 불가 태스크의 자기평가.

### W2/W12 — Hanna Hajishirzi "Open Training Recipes" (155장, SP25)
- Tulu-3 전체 레시피 공개: SFT→DPO→**RLVR** (405B avg 80.7 ≈ GPT-4o 81.6). 단계별 기여: 76.3→79.0→80.0.
- **검증기 실제 코드 슬라이드**(p.105-106): GSM8K 정규식 마지막 숫자 추출, IF 규칙 채점기 ~25종. "과최적화 없음" 곡선(p.110).
- "RLVR은 새 게 아니다 — **베이스 모델 품질이 달라진 것**": GRPO 정답률 강한 베이스 0.37→0.5 vs GPT2-XL 평평(p.115).
- **s1 budget forcing**: 생각 종료 억제+"Wait" 추가 → 1K 선별 예제로 MATH500에서 o1 초과(p.141); 순차 스케일링 > 병렬 다수결(GPQA 60 vs 51, p.138). 데이터 선별 승리: 1K 선별 ≈ 59K 전체(p.139).
- OLMo-2 mid-training(예산 1%로 GSM8K 37.3→75.1, p.151).

### W3 — 전담 덱 없음
- MS 04가 실질 뼈대(위 판정표). Chapados의 API vs Web 에이전트 이분법(p.8), Tian의 "솔버=도구"(TTG: NL→MILP, 번역 2.5s+풀이 0.6s)가 보조.
- 논문 수치는 별도 검증 완료(Toolformer·ToolLLM — W3 덱 작성 노트 참조): Toolformer 6.7B 수학에서 GPT-3 175B 초과(ASDiv 40.4 vs 14.0, Table 4), 필터 = "호출 삽입 시 후속 토큰 loss 감소"; ToolLLM 16,464 API, DFSDT 35.3→63.8(ReAct 대비, Table 3), ToolLLaMA 7B ≈ ChatGPT.

### W4 — Yuandong Tian "Neural & Symbolic Decision Making" (87장, F24)
- **도입 카드**: TravelPlanner GPT-4-Turbo 통과율 **0.6%** (p.6); o1-preview 15.6%; NATURAL PLAN에서 o1도 계획 길이 14에서 0%, 고전 플래너는 100% (p.8).
- 3갈래: 스케일링 / 하이브리드(솔버를 도구로·솔버 데이터로 학습·엔드투엔드) / 창발적 심볼릭 구조.
- **Searchformer**: A* 탐색 동역학을 토큰으로 학습 → 부트스트랩 후 A*보다 짧은 트레이스(ILR 1.343). **Dualformer**: 트레이스 무작위 드롭 훈련 → **System 1/2 자동 전환**(30×30 미로 96.6% vs 해답만 30.0%).
- 마무리: 모듈러 덧셈에서 Fourier 기저·세미링 구조 창발 — "신경망은 속으로 심볼릭일지도".

### W4/W9 — Yu Su "Memory, Reasoning, Planning" (80장, SP25)
- **계획 3분법**(p.60-62): 반응형 / 실제 환경 트리탐색(느리고 비가역 행동 위험) / **월드모델 시뮬레이션**. "웹 행동은 비가역적('주문하기') → 클릭 말고 상상하라" → WebDreamer: VWA 23.6%(트리탐색 26.4%의 정확도를 1/4 시간에, p.71).
- **메모리 앵커**: 해마 인덱싱 이론 → HippoRAG(신피질=LLM, 해마=KG+Personalized PageRank; multi-hop Recall@5 +7.3, p.32). **path-following vs path-finding 질문** 진단(p.33).
- 그로킹 반전: 파라메트릭 메모리가 깊은 multi-hop에서 99.3% vs GPT-4+RAG 33.3(p.79-80) — "RAG가 항상 답은 아니다" 토론 카드.
- 자기반성 = 메타 추론 행동(inner monologue) 프레임(p.7, 11) — W5 개념 틀.
- 핵심 역량 피라미드(p.15) — 과목 전체 지도와 유사.

### W5 — 전담 덱 없음 (조합으로 구성)
- Zhou의 "자기교정 불가 + 오라클이면 가능"(반전 카드) + Yao의 Reflexion="verbal RL"(67→91) + Yu Su의 메타 추론 프레임 + Chen 덱 Reflexion ALFWorld 0.63→0.97(p.61)·Self-debugging(TransCoder 77.3→90.4, p.64 — 단위테스트=오라클).
- MS 09는 사용하지 않음.

### W6 — Burak Gokturk (Google, 91장, F24) + Jerry Liu 앞부분
- Burak: **환각 최소화 = 3문제(올바른 컨텍스트/더 나은 모델/UX-출처표시)**(p.51); pre-hoc/post-hoc 그라운딩(NLI로 문장별 검증+인용, p.54); Félicette 우주 고양이 출처표시 예시(p.55-56). 4대 구성요소 격자: Fine-Tuning/Distillation/Grounding/Function Calling. "API 비용 0으로 수렴" 트렌드(Flash $0.075/1M).
- Jerry Liu: 기초 RAG 파이프라인과 **5대 결함**(나이브 파싱·원시적 검색·질의계획 부재·도구 없음·무상태)(p.4-5); "LLM 앱은 데이터 품질만큼만 좋다".

### W7 — Jerry Liu "Multimodal Knowledge Assistant" (40장, F24)
- 복잡 입력 분류(요약·비교·다부분·리서치, p.26); 단순→고급 에이전트 스펙트럼(라우팅→ReAct·동적 계획, p.27); **"모든 데이터 인터페이스는 도구다"**(p.28).
- **제약형 vs 비제약형 플로우**(신뢰성↔표현력 다이얼, p.29-30) — W7 뼈대.
- 프로덕션: 컨트롤플레인+메시지큐 멀티에이전트 아키텍처(llama-deploy, p.38) — W10 후반 연결.

### W8 — 버클리 전담 덱 없음. MS 12가 유일한 조직적 자료 (판정표 참조) + Anthropic 블로그로 구성 (기존 계획 유지).

### W10 — Chi Wang "AutoGen" (37장, F24) + DSPy 대조
- "대화 프로그래밍" 추상화; 4패턴(Sequential/Nested/Group/Hierarchical Chat); StateFlow = 상태기계로서의 태스크(p.25); **오케스트레이션 6차원**(정적/동적·NL/PL·공유/격리·협력/경쟁·중앙/분산·개입/자동, p.14); 프레임워크 지형(AutoGen vs LangGraph vs CrewAI, p.16).
- 멀티 vs 싱글 수치: F1 96 vs 88 (GPT-4, p.10). Captain Agent 84.25 vs 바닐라 40.98 (p.35).
- **DSPy (Omar Khattab, 92장)**: 반대 입장 카드 — "프롬프트는 5역할의 결합(Signature/Predictor/Adapter/Metrics/Optimizer), 손튜닝 말고 컴파일" — MIPROv2로 37%→55%; 손제작 ReAct 33% vs 최적화 MultiHop 55%(GPT-3.5). "부트스트랩된 시연을 못 이긴다(Show don't tell)". 토론 포인트: 우리 from-scratch 철학과의 긴장.

### W11 — Ruslan (126장) + Caiming (106장, SP25)
- Ruslan(웹 축): VisualWebArena — 인간 88.7% vs GPT-4V+SoM 16.4%(p.33-34); Set-of-Marks 프롬프팅(p.29); **오류 복리 표**: 스텝당 90%면 10스텝 34.9%, 30스텝 4.2%(p.39-42); 트리 탐색 +51% 상대 개선하되 느리고 **비가역 행동은 되돌릴 수 없음**(p.75); InSTA 인터넷 규모 합성 훈련(150k 사이트).
- Caiming(OS 축): **OSWorld** — VM 기반 실행형 벤치마크, 태스크=JSON(초기상태+실행 기반 채점기)(p.16-19); 인간 72.4% vs GPT-4 12.2%(p.24); Claude computer use 14.9→22%(스텝 늘리면), OpenAI CUA 19.7→38.1 스텝 스케일링(p.29-31); AgentTrek(튜토리얼 2.24M→검증 궤적 10,398개로 GPT-4 초과); Aguvis 순수 비전 그라운딩(ScreenSpot 84.4 vs GPT-4o 18.3) — 관찰 표현 논쟁(a11y tree는 목발, 장기적으론 스크린샷)이 우리 W11 "DOM vs 스크린샷" 논점 그 자체.

### W13 — 3렌즈 분업
- **Percy Liang (88장, F24)**: 접근성 3단계(API=인지과학자/가중치=신경과학자/오픈소스=컴퓨터과학자); MLAgentBench(Claude 3 Opus 37.5); **Cybench**(40 CTF, Claude 3.5 Sonnet 17.5%/43.9% 서브태스크); 1,000명 생성 에이전트 시뮬레이션(GSS 재현 85%); HELM.
- **Ben Mann (30장, F24)**: SWE-bench Verified 49%(당시 SOTA), **가격 병기**($3/$15 vs o1 $15/$60); METR 시간 환산(인간 30분 태스크); "벤치마크는 오래 못 간다"(포화 차트); RSP/ASL 거버넌스.
- **Chapados (72장, F24)**: **WorkArena++ L3 전 모델 0.0% vs 인간 93.9%**(p.41) — 벤치마크 과장 대 현실 카드; 평가 3세대(MiniWoB 비현실→트레이스 기반→라이브 환경); BrowserGym/AgentLab 통일 하네스; GREADTH 지표.

### W14 — Dawn Song "Safe & Secure Agentic AI" (99장, SP25) — 사실상 교과서
- 안전 vs 보안 구분(p.7); LLM 출력 공격 체인 U1–U5(SQL 인젝션/SSRF/RCE, p.28); 모델 보안 레벨 L0–L4(p.29).
- **실제 CVE**: LlamaIndex Text-to-SQL(CVE-2024-23751), Vanna-ai(CVE-2024-7764, CVSS 8.1), SuperAGI `eval` RCE(CVE-2024-21552)(p.32-38).
- 인젝션 분류(휴리스틱/최적화 기반, USENIX Sec 2024, p.41); "명령과 데이터의 혼합"이 근본 문제(p.44-49); AgentPoison(RAG 메모리 오염 백도어).
- 방어: 심층방어+최소권한+설계상 안전 3원칙 → 8메커니즘; **Progent**(최소권한 DSL, ~10줄 추가로 AgentDojo ASR 41.2%→2.2%, ASB 70.3%→0.0% 수동 정책)(p.77-93); DataSentinel(게임이론적 인젝션 탐지).
- Mann RSP/ASL(거버넌스 축) + Neubig 안전 3종(샌드박스/최소권한 토큰/이벤트 감사)과 조합.

### W15 — Neubig (53장, F24) + Sutton (55장, SP25)
- Neubig: 개발자 시간 사용(코딩 ~15%); Copilot RCT 55% 단축; **CodeAct**(JSON 도구호출 대신 실행가능 코드가 행동); SWE-agent ACI(100줄 뷰어·린트 가드); OpenHands 이벤트 스트림; 파일 로컬라이제이션 4해법(Agentless 계층적 위치추적 포함); "테스트를 지워서 테스트를 통과시킨다" — 사고적 해악의 정석 예.
- Sutton: **"하네스 양의 연속체"**(셸 프롬프트=모델이 전부 제어 ↔ ACI ↔ Agentless=코드가 전부 제어) + **"최적점은 베이스 모델이 좋아질수록 이동한다"**(p.25-29) — 우리 W15 논지의 이론화. 리더보드+비용: Agentless GPT-4o 32% $0.70 vs SWE-agent 23% $1.62(p.24). pass@k 불편추정량; "모든 평가에는 유통기한이 있다"(p.15). Big Sleep 실궤적(strcpy 오버플로 발견→입력 제작→실패→자기수정→ASan 크래시)과 SQLite 제로데이(p.46-54).
- Chapados 교사-학생 증류: 405B 테이프→8B 파인튜닝 2.0%→76.6%(GPT-4o 74.9 초과), **비용 1/300**(p.22-24) — "단순함·작은 모델이 이긴다" 최강 수치.

## 우리 덱 실행 항목 (우선순위)

1. **W10 프레임워크 지형 수정** — AutoGen+SK→MAF 통합 반영 (사실관계, 필수)
2. **W4 도입** = TravelPlanner 0.6% · **W5 반전** = 자기교정 불가→오라클 피드백(Zhou p.69-70) · **W1 보강** = Â=A∪L 1장
3. **W2 보강 후보**(작성 완료 덱): o1/o3 도입 수치(ARC-AGI $1k+/task 비용축), s1 "Wait" budget forcing(현장 노트 ①의 학술 버전) — 분량 여유 시
4. **W12**는 Hajishirzi 검증기 코드 슬라이드 + "베이스 품질이 달라진 것" + Weston STaR→RPO→R1 계보로 구성 확정
5. **W11 오류 복리 표**(90%^30=4.2%), **W13 WorkArena++ 0.0% vs 인간 93.9%**, **W14 Progent 41.2→2.2%** — 각 주차 도입/절정 카드로 예약
6. MS 02·03·09·14·18은 참고 목록에서 강등

## 원자료 위치

- MS: `materials/repos/ai-agents-for-beginners/<NN-lesson>/README.md`
- 버클리: `materials/repos/llm-agents-mooc/slides/*.pdf` (F24/SP25 구분은 `f24.md`·`sp25.md`)
