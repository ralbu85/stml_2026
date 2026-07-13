# docqa-agent 실습 스캐폴드 — 초기화 상태 (2026-07-13)

스캐폴드 코드는 전면 재구축을 위해 초기화되었다 (직전 상태는 git 이력 커밋 `079ab0a`).
재구축 기준: 주차 설계는 [실습 가이드](../docs/practice-guide.md), 노트북 표준은
Andrew Ng *Agentic AI* 실습 스타일(관찰 랩 → 작성 과제 사다리, 프롬프트 작성형 빈칸,
중간 산출물 가시화, 스모크 채점 셀 — `materials/repos/agentic_ai_andrew` 조사 기록 참조)과
[집필 규정 §5·6](../docs/style-guide.md).

## 설치 (유지되는 인프라)

**Python 3.10 이상 필수** (aisuite 요구사항).

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

- `data/` — 실습용 샘플 문서 (유지)
- `requirements.txt` · `.env.example` — 환경 설정 (유지)
