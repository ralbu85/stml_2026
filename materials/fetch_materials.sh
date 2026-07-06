#!/usr/bin/env bash
# 강의 참고자료 레포를 materials/repos/ 에 얕은 클론(--depth 1)으로 내려받는다.
# 용량 약 2.1GB. 재현/갱신용. 자세한 주차 매핑은 materials/README.md 참고.
set -e
cd "$(dirname "$0")"
mkdir -p repos && cd repos

REPOS=(
  "https://github.com/rdi-berkeley/llm-agents-mooc"       # Berkeley 강의 슬라이드 PDF 28개
  "https://github.com/microsoft/ai-agents-for-beginners"  # MS 12+강 (MIT) — 주차와 1:1
  "https://github.com/huggingface/agents-course"          # HF 유닛 코스 (한국어 포함)
  "https://github.com/NirDiamant/RAG_Techniques"          # RAG 노트북 42개
  "https://github.com/NirDiamant/GenAI_Agents"            # 에이전트 튜토리얼 53개
  "https://github.com/anthropics/anthropic-cookbook"      # 도구·RAG·에이전트 레시피
  "https://github.com/anthropics/courses"                 # Anthropic 코스
  "https://github.com/mlabonne/llm-course"                # LLM 기초
  "https://github.com/nhatnam2609/agentic_ai_andrew"      # Andrew Ng Agentic AI 미러(노트북)
)

for url in "${REPOS[@]}"; do
  name=$(basename "$url")
  if [ -d "$name" ]; then
    echo "skip (exists): $name"
  else
    echo "clone: $name"
    git clone --depth 1 --single-branch -q "$url" "$name"
  fi
done
echo "done -> $(du -sh .. | cut -f1)"
