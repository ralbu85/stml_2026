"""Canned responder for the W7 notebook dry-run (stdlib only)."""

import re

CANNED_PLAN = (
    '["Search arXiv and Wikipedia for background on retrieval-augmented '
    'generation for question answering over private document collections.", '
    '"Search for evaluation methods and challenges of retrieval-augmented '
    'generation systems.", '
    '"Draft a structured research report in Markdown summarizing the findings.", '
    '"Review the draft, then revise it into the final Markdown research report."]'
)

CANNED_RESEARCH = (
    "Findings: retrieval-augmented generation (RAG) couples a language model "
    "with a document index so answers can cite private, up-to-date sources. "
    "Evaluation combines answer accuracy with retrieval recall, and the main "
    "challenges are chunking, index freshness, and grounding. Sources used: "
    "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks "
    "(https://arxiv.org/abs/2005.11401); Question answering "
    "(https://en.wikipedia.org/wiki/Question_answering)."
)

_REPORT_BODY = """# Retrieval-Augmented Generation for Private Document Question Answering

## Background

Retrieval-augmented generation couples a language model with a document index.
At query time the system retrieves the passages most relevant to the question
and places them into the model input, so the generated answer can cite
up-to-date, organization-specific sources instead of relying only on training
data. For private document collections this matters twice over: the material is
absent from any training corpus, and answers must be attributable to specific
internal documents. The foundational formulation appears in Lewis et al., 2020
(https://arxiv.org/abs/2005.11401), which combines a dense retriever with a
sequence-to-sequence generator and trains the two jointly on knowledge-intensive
tasks.

## System Design

A question-answering system over a private collection has two coupled stages. A
retriever indexes the collection, typically after splitting documents into
chunks and embedding each chunk into a vector space, and returns the top-ranked
chunks for a query. A reader model then composes the answer conditioned on the
retrieved chunks. Design quality depends on chunk size and overlap, on the
embedding model, and on how many passages are injected into the prompt. Hybrid
retrieval that merges lexical and vector scores improves robustness on named
entities, and a reranking stage tightens precision at small k.

## Evaluation and Challenges

Evaluation combines end-to-end answer accuracy with retrieval-level recall,
since a reader cannot recover from a retriever that never surfaced the relevant
passage (https://en.wikipedia.org/wiki/Question_answering). The recurring
challenges are index freshness as documents change, grounding the answer in the
retrieved text rather than parametric memory, and controlling context length as
more passages are injected.

## Conclusion

Retrieval-augmented generation is the standard architecture for question
answering over private collections. Its accuracy is bounded first by retrieval
quality, so improvement effort should start at the retriever, then move to
prompt construction and reranking, with evaluation tracking both stages
separately.
"""

CANNED_FEEDBACK = (
    "1. Add explicit section headings for background, design, evaluation, and "
    "conclusion. 2. Tie every claim to one of the gathered sources and keep the "
    "URLs. 3. Trim repetition in the design section and keep the report under "
    "1500 words."
)


def _route(instruction):
    if re.search(r"review|revise|critique|feedback|edit", instruction, re.IGNORECASE):
        agent = "editor_agent"
    elif re.search(r"draft|write|summar", instruction, re.IGNORECASE):
        agent = "writer_agent"
    else:
        agent = "research_agent"
    safe_task = instruction.replace('"', "'")
    return '{"agent": "%s", "task": "%s"}' % (agent, safe_task)


def responder(model=None, messages=None, **kw):
    messages = messages or []
    system = " ".join(m.get("content", "") for m in messages
                      if m.get("role") == "system")
    user = " ".join(m.get("content", "") for m in messages
                    if m.get("role") != "system")
    text = system + " " + user

    if "Reply with exactly: ready" in text:
        return "ready"
    if "execution manager" in text:
        match = re.search(r'Instruction: "(.*)"', user, re.DOTALL)
        return _route(match.group(1) if match else user)
    if "SCORE:" in text:
        return "SCORE: 5 — the report is grounded in its cited sources and covers the topic."
    if "research assistant with access" in text:
        return CANNED_RESEARCH
    if "writing agent" in system:
        return _REPORT_BODY
    if "You are editor_agent" in user or "editor" in system.lower():
        if re.search(r"revise|final", user, re.IGNORECASE):
            return _REPORT_BODY
        return CANNED_FEEDBACK
    if "Retrieval-augmented generation for question answering" in user:
        return CANNED_PLAN
    return "A single-sentence canned reply for the offline dry-run."
