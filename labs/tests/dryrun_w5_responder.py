"""Canned responder for the merged W5 reflection+evaluation lab (stdlib only).

Part A branches reproduce the essay reflection flow (V1 -> critique -> V2, judge
scores, second round, vague ablation). Part B branches reproduce the research-step
evaluation (tool calls return weak/strong sourcing by prompt; judge calls return a
fixed SCORE line).
"""

import json

V1_ESSAY = (
    "Social media platforms now mediate much of public debate. This essay "
    "argues that some government regulation is appropriate. Platforms are "
    "influential and their decisions affect many people. Regulation could "
    "make them behave better. In conclusion, social media matters and "
    "government attention to it is reasonable."
)

V2_ESSAY = (
    "Social media platforms now mediate much of public debate, and this essay "
    "argues that targeted government regulation is justified. For example, "
    "engagement-ranked feeds have been shown to amplify divisive content, and "
    "platform moderation decisions are made without public accountability. "
    "Critics argue that state regulation threatens free expression; that risk "
    "is real, which is why the regulation defended here targets transparency "
    "obligations rather than content itself. In conclusion, transparency-first "
    "regulation addresses documented harms while leaving speech decisions "
    "outside government hands."
)

V3_ESSAY = V2_ESSAY.replace("this essay argues", "this essay maintains")

V2_VAGUE_ESSAY = (
    "Social media platforms are a defining force of our time. They connect "
    "people and shape opinion in powerful and engaging ways. Whether the "
    "government should regulate them is an important and interesting "
    "question that deserves careful thought. In conclusion, this issue will "
    "remain important for years to come."
)

DRAFT_FEEDBACK = (
    "The draft asserts that platforms are influential and that regulation "
    "could help, but offers no evidence for either claim - a fix needs at "
    "least one concrete example of platform harm. It never addresses the "
    "opposing view that regulation endangers free expression - a fix needs "
    "to state and answer that objection. The conclusion restates the "
    "introduction instead of resolving the argument."
)

V2_FEEDBACK = (
    "The revised draft states a position, supports it with an example, and "
    "answers the free-expression objection. Remaining defect: the single "
    "example carries the whole argument - a fix would add one more "
    "independent line of evidence."
)

EXAMPLE_CRITIQUE = (
    "Defect 1 (evidence): the text asserts harm to democracy without any "
    "supporting fact - a fix needs a concrete example. Defect 2 (argument): "
    "the conclusion does not follow from a single unsupported premise - a fix "
    "needs the intermediate claim that regulation would reduce the harm. "
    "Defect 3 (counterargument): no opposing view is considered."
)

VAGUE_FEEDBACK = (
    "Make it more engaging and better overall. Improve the flow and polish "
    "the language so it reads well."
)

LOW_QUALITY_RESULT = """\
Here is what I found on the topic:
1. A recent overview - https://medium.com/@writer/black-holes-explained
2. Discussion post - https://scienceblog.example.com/post/123
3. Paper - https://arxiv.org/abs/2403.01234
4. News item - https://newsaggregator.example.net/item/998
"""

HIGH_QUALITY_RESULT = """\
Sources, each with its full URL:
1. Key paper - https://arxiv.org/abs/2401.11111
2. Key paper - https://arxiv.org/abs/2402.22222
3. Encyclopedic overview - https://en.wikipedia.org/wiki/Relevant_topic
4. Institutional report - https://www.nasa.gov/mission/science-article
5. Practitioner writeup - https://exampleblog.io/post/42
"""


def _prompt_text(messages):
    content = messages[-1]["content"]
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content
                        if isinstance(part, dict))
    return content


def responder(model=None, messages=None, **kw):
    text = _prompt_text(messages)

    if "Reply with exactly" in text:
        return "ready"

    # ---- Part B: research step (tools registered) ----
    if kw.get("tools"):
        if "You are a research function" in text:
            return LOW_QUALITY_RESULT
        return HIGH_QUALITY_RESULT

    # ---- Part B: judge over stored research outputs ----
    if "SCORE:" in text or "arxiv.org/abs" in text or "medium.com" in text:
        return "The sources are mostly reputable and linked.\nSCORE: 4"

    # ---- Part A: essay reflection flow ----
    if "You grade an essay" in text:
        essay = text.split("Essay:", 1)[-1].lower()
        return json.dumps({
            "thesis": 1,
            "structure": 1,
            "evidence": 1 if "for example" in essay else 0,
            "counterargument": 1 if "critics argue" in essay else 0,
        })

    if "Original Draft:" in text and "Feedback:" in text:
        if "more engaging" in text:          # revision from the vague critique
            return V2_VAGUE_ESSAY
        if "Critics argue" in text:          # second round: draft is already V2
            return V3_ESSAY
        return V2_ESSAY

    if "draft essay" in text and "Prompt:" in text:
        return V1_ESSAY

    if "Say how to improve this essay." in text:
        return VAGUE_FEEDBACK

    if "Social media is bad for democracy" in text:   # Section 3 worked example
        return EXAMPLE_CRITIQUE

    if "Critics argue" in text:              # critique of V2 (second round)
        return V2_FEEDBACK

    return DRAFT_FEEDBACK                    # critique of V1 (student fill-in)
