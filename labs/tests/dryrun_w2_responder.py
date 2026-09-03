"""Canned responder for the W2 lab dry-run (stdlib only).

Emulates the source-lesson narrative: animal-legs eval scores rise across the
three prompt versions (verbose/wrong -> numeric/tricky-wrong -> tagged/correct);
sampled (temperature > 0) tagged calls on the fox scatter so the vote has work
to do; every assignment starter fails and every reference solution passes.
"""

import itertools
import re

# golden answers keyed by distinctive substrings; order matters (specific first)
ANIMAL_KEYS = [
    ("octopus that lost two legs", "9"),
    ("two-headed", "8"),
    ("cat with two extra", "6"),
    ("spider that lost three legs", "5"),
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
VERBOSE = {"2": "Based on the statement, the animal has 2 legs."}  # format miss (v1)

_fox_samples = itertools.cycle(["5", "5", "6", "5", "5"])
_spider_samples = itertools.cycle(["5", "2", "5", "5", "5"])

EMAIL_LETTER = [
    ("strange noise", "B"),
    ("mix paint", "A"),
    ("MONTHLY CHARGES", "C"),
    ("not good with computer", "D"),
]

ROMAN = {  # expression -> (value a, value b, result)
    "XIV + IX": ("XIV = 14", "IX = 9", "23"),
    "XLII - XXIX": ("XLII = 42", "XXIX = 29", "13"),
    "CD + XC": ("CD = 400", "XC = 90", "490"),
    "MMXXVI - MCMXCIV": ("MMXXVI = 2026", "MCMXCIV = 1994", "32"),
    "XCIX + I": ("XCIX = 99", "I = 1", "100"),
    "LXXX / XVI": ("LXXX = 80", "XVI = 16", "5"),
}


def _animal_reply(text, temperature):
    statement = text.split("<animal_statement>")[1].split("</animal_statement>")[0]
    golden = next(g for key, g in ANIMAL_KEYS if key in statement)
    tagged = "<answer>" in text or "<thinking>" in text

    if tagged:
        value = golden
        if temperature and temperature > 0:
            if "fox lost a leg" in statement:
                value = next(_fox_samples)
            elif "spider that lost three legs" in statement:
                value = next(_spider_samples)
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
    temperature = kw.get("temperature", 0.0)

    if "Reply with exactly: ready" in text:
        return "ready"

    # §2.1 role prompting
    if "skateboarding" in text:
        if "You are a cat" in text:
            return "Skateboarding is a loud rolling thing that ruins a perfectly good nap."
        return "Skateboarding is a creative and athletic sport that builds balance and confidence."
    if "Jack is looking at Anne" in text:
        if "logic bot" in text:
            return "Yes. If Anne is married, she (married) looks at George (unmarried); if not, Jack (married) looks at Anne (unmarried)."
        return "We cannot determine this without knowing whether Anne is married."

    # §2.2 delimiters
    if "second item on the list" in text:
        if "<sentences>" in text:
            return "This sentence is about spiders"
        return "I like how cows sound"

    # §3.1–3.2 movie review
    if "living under a rock" in text:
        if "<positive-argument>" in text or "<negative-argument>" in text:
            return ("<positive-argument>The reviewer calls the movie fresh and "
                    "original.</positive-argument>\n<negative-argument>The reviewer "
                    "has been living under a rock since 1900, so everything seems "
                    "fresh; the praise is unreliable.</negative-argument>\n"
                    "The review sentiment is negative.")
        if "silence" in text:
            return "Positive"
        return "Positive. The reviewer praises the movie's freshness and originality."

    # §3.3 actor born 1956
    if "born in the year 1956" in text:
        if "<brainstorm>" in text:
            return ("<brainstorm>Tom Hanks (born 1956), Mel Gibson (born 1956), "
                    "Tom Cruise (born 1962)</brainstorm>\n"
                    "Forrest Gump, starring Tom Hanks, who was born in 1956.")
        return "Top Gun, starring Tom Cruise, who was born in 1962."

    # §4 / §6 / §8.3 animal-legs eval
    if "<animal_statement>" in text:
        return _animal_reply(text, temperature)

    # §5.1 parent bot
    if "Santa bring me presents" in text:
        if "tooth fairy" in text:
            return ("A: Yes, sweetie, as long as you are kind this year. Leave out "
                    "some cookies for him on Christmas Eve.")
        return ("Santa Claus is a legendary figure; whether presents appear depends "
                "on your family's traditions.")

    # §5.2 email classification
    for key, letter in EMAIL_LETTER:
        if key in text:
            if "(A) Pre-sale question" in text:   # solution-style prompt with categories
                return f"The correct category is: {letter}"
            return "It sounds blue to me."

    # §7 hallucination
    if "heaviest hippo" in text:
        if "certainty" in text or "I don't know" in text:
            return "I don't know with certainty; no reliable record identifies the heaviest hippo of all time."
        if "<thinking>" in text:
            return ("<thinking>Hippos weigh up to about 4,500 kg. Zoo records mention very "
                    "large males.</thinking>\nThe heaviest hippo of all time was a male "
                    "named Hubert at the Munich Zoo, weighing about 4,800 kg.")
        return "The heaviest hippo of all time was a male named Hubert, weighing about 4,800 kg."

    # §8.1 word problems
    if "library has 4 shelves" in text:
        if "ANSWER" in text:
            return "4 * 38 = 152 books. 152 - 47 = 105. 105 + 26 = 131.\nANSWER: 131"
        return "There are 131 books on the shelves now."
    if "bakery bakes 12 trays" in text:
        if "ANSWER" in text:
            return "12 * 24 = 288 muffins. 6 * 24 = 144 sold whole. 288 - 144 = 144. 144 - 37 = 107.\nANSWER: 107"
        return "107 muffins remain."

    # §8.2 date extraction
    if "March 10th, 2026" in text:
        return "DATE: 2026-03-10" if "DATE: 2026-06-09" in text else "The final date is March 10th, 2026."
    if "April 22nd, 2026" in text:
        return "DATE: 2026-04-22" if "DATE: 2026-06-09" in text else "The final date is April 22nd, 2026."

    # §8.4 Roman numerals
    for expression, (a, b, result) in ROMAN.items():
        if expression in text:
            exemplars = len(re.findall(r"^ANSWER:\s*\d+\s*$", text, re.M))
            if exemplars >= 2:
                return f"{a}, {b}. {result}.\nANSWER: {result}"
            return f"The result is {result} (ANSWER: {result})."

    return "A single-sentence canned reply for the offline dry-run."
