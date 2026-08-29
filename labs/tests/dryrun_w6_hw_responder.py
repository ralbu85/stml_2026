"""Canned responder for the W6 new-intent homework dry-run (stdlib only)."""

import json

PLANS = {
    "Sell two blue mugs": [{"tool": "sell_item", "args": {"product": "blue mug", "qty": 2}}],
    "How many tea pots": [{"tool": "check_stock", "args": {"product": "tea pot"}}],
    "returns one red mug": [{"tool": "return_item", "args": {"product": "red mug", "qty": 1}}],
}


def responder(model=None, messages=None, **kw):
    text = " ".join(str(m.get("content", "")) for m in (messages or []))
    if "Reply with exactly: ready" in text:
        return "ready"
    for key, plan in PLANS.items():
        if key in text:
            return json.dumps(plan)
    if "exchanges one blue mug for one tea pot" in text:
        if "exchange_item" in text:   # planner has been extended
            return json.dumps([{"tool": "exchange_item",
                                "args": {"old_product": "blue mug",
                                         "new_product": "tea pot", "qty": 1}}])
        # planner never heard of exchanges: plans a bare sale (wrong on purpose)
        return json.dumps([{"tool": "sell_item",
                            "args": {"product": "tea pot", "qty": 1}}])
    return json.dumps([])
