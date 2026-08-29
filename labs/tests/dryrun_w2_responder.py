"""Canned responder for the W2 lab dry-run (stdlib only).

Emulates the source-lesson narrative: animal-legs eval scores rise across the
three prompt versions (verbose/wrong -> numeric/tricky-wrong -> tagged/correct).
"""

import itertools

# golden answers keyed by distinctive substrings; order matters (specific first)
ANIMAL_KEYS = [
    ("octopus that lost two legs", "9"),
    ("two-headed", "8"),
    ("cat with two extra", "6"),
    ("spider", "10"),
    ("fox lost a leg", "5"),
    ("human", "2"),
    ("snake", "0"),
    ("a dog", "4"),
    ("elephant", "4"),
    ("bird", "2"),
    ("fish", "0"),
    ("octopus", "8"),
]

TRICKY_WRONG = {"9": "5", "10": "8", "5": "6"}      # reasoning misses pre-CoT
VERBOSE = {"2": "Based on the statement, the animal has 2 legs."}  # format miss (v1, bird/human)

_fox_samples = itertools.cycle(["5", "5", "6", "5", "5"])

EMAIL_LETTER = [
    ("strange noise", "B"),
    ("mix paint", "A"),
    ("MONTHLY CHARGES", "C"),
    ("not good with computer", "D"),
]


def _animal_reply(text):
    statement = text.split("<animal_statement>")[1].split("</animal_statement>")[0]
    golden = next(g for key, g in ANIMAL_KEYS if key in statement)
    tagged = "<answer>" in text or "<thinking>" in text
    temperature_sampled = "fox lost a leg" in statement and tagged

    if tagged:
        value = next(_fox_samples) if temperature_sampled else golden
        return (f"<thinking>Counting the legs step by step for: {statement.strip()}"
                f"</thinking>\n<answer>{value}</answer>")
    value = TRICKY_WRONG.get(golden, golden)
    if "numeric digit" in text:
        return value
    # v1: some formatting failures, as in the source run
    if "bird" in statement or "human" in statement:
        return VERBOSE["2"]
    return value


def responder(model=None, messages=None, **kw):
    text = " ".join(m.get("content", "") for m in (messages or []))

    if "Reply with exactly: ready" in text:
        return "ready"

    # §2.1 movie review
    if "living under a rock" in text:
        if "<positive-argument>" in text:
            return ("<positive-argument>The reviewer calls the movie fresh and "
                    "original.</positive-argument>\n<negative-argument>The reviewer "
                    "has been living under a rock since 1900, so everything seems "
                    "fresh; the praise is unreliable.</negative-argument>\n"
                    "The review sentiment is negative.")
        return "Positive. The reviewer praises the movie's freshness and originality."

    # §2.2 actor born 1956
    if "born in the year 1956" in text:
        if "<brainstorm>" in text:
            return ("<brainstorm>Tom Hanks (born 1956), Mel Gibson (born 1956), "
                    "Tom Cruise (born 1962)</brainstorm>\n"
                    "Forrest Gump, starring Tom Hanks, who was born in 1956.")
        return "Top Gun, starring Tom Cruise, who was born in 1962."

    # §3 / §5 animal-legs eval
    if "<animal_statement>" in text:
        return _animal_reply(text)

    # §4.1 parent bot
    if "Santa bring me presents" in text:
        if "tooth fairy" in text:
            return ("A: Yes, sweetie, as long as you are kind this year. Leave out "
                    "some cookies for him on Christmas Eve.")
        return ("Santa Claus is a legendary figure; whether presents appear depends "
                "on your family's traditions.")

    # §4.2 email classification
    for key, letter in EMAIL_LETTER:
        if key in text:
            if "(A) Pre-sale question" in text:   # solution-style prompt with categories
                return f"The correct category is: {letter}"
            return "It sounds blue to me."
    return "A single-sentence canned reply for the offline dry-run."
