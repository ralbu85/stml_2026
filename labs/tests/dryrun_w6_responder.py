"""Canned responder for the W6 notebook dry-run (stdlib only)."""

import json


def _lookup_step(name, n=1):
    return {
        "step_number": n,
        "description": f"Lookup product '{name}'",
        "tools": [{"use": "get_inventory_data", "args": {"product_name": name},
                   "result_key": "prod"}],
        "validations": [{"name": "product_found", "use_tool": "assert_true",
                         "args": {"value_from": "context.prod.item"}}],
    }


def _trade_plan(name, qty, kind):
    """kind 'purchase' -> compute_total/delta=-qty; 'return' -> compute_refund/delta=+qty."""
    compute = "compute_total" if kind == "purchase" else "compute_refund"
    delta = -qty if kind == "purchase" else qty
    verb = "Purchase" if kind == "purchase" else "Return"
    return {
        "reasoning": f"{verb} {qty} {name} sunglasses.",
        "steps": [
            _lookup_step(name, 1),
            {"step_number": 2, "description": f"Compute amount for qty={qty}",
             "tools": [{"use": compute,
                        "args": {"qty": qty, "price_from": "context.prod.item.price"},
                        "result_key": "amount"}],
             "validations": []},
            {"step_number": 3, "description": "Update inventory",
             "tools": [{"use": "update_inventory",
                        "args": {"item_id_from": "context.prod.item.item_id",
                                 "delta": delta},
                        "result_key": "inv_after"}],
             "validations": [{"name": "stock_nonnegative",
                              "use_tool": "assert_nonnegative_stock",
                              "args": {"inventory_df_from": "context.__frames__.inventory_df",
                                       "item_id_from": "context.prod.item.item_id"}}]},
            {"step_number": 4, "description": "Append the transaction",
             "tools": [{"use": "append_transaction",
                        "args": {"customer_name": "WALK_IN_CUSTOMER",
                                 "summary": f"{verb} {qty} {name} sunglasses",
                                 "amount_from": "context.amount.amount"},
                        "result_key": "txn"}],
             "validations": [{"name": "transaction_created", "use_tool": "assert_true",
                              "args": {"value_from": "context.txn.transaction.transaction_id"}}]},
        ],
    }


def _inquiry_plan(name):
    return {"reasoning": f"Inquiry about {name}.", "steps": [_lookup_step(name, 1)]}


def _browse_plan():
    return {
        "reasoning": "Browse the full catalog.",
        "steps": [{"step_number": 1, "description": "List full inventory",
                   "tools": [{"use": "get_inventory_data", "args": {},
                              "result_key": "all"}],
                   "validations": [{"name": "catalog_nonempty", "use_tool": "assert_true",
                                    "args": {"value_from": "context.all.match_count"}}]}],
    }


PLANS = [
    ("return two Aviator", _trade_plan("Aviator", 2, "return")),
    ("buy 2 Aviator", _trade_plan("Aviator", 2, "purchase")),
    ("return two Sport", _trade_plan("Sport", 2, "return")),
    ("Mystique glasses in stock", _inquiry_plan("Mystique")),
    ("everything you have available", _browse_plan()),
    ("buy 999 Wayfarer", _trade_plan("Wayfarer", 999, "purchase")),
    ("return one Round", _trade_plan("Round", 1, "return")),
]

DRAFT_MARKER = "Draft plan (JSON):"
TASK_MARKER = "\n\nTask:"


def responder(model=None, messages=None, **kw):
    text = " ".join(m.get("content", "") for m in (messages or []))
    if "Reply with exactly: ready" in text:
        return "ready"
    if DRAFT_MARKER in text:                       # reflection call: echo the draft
        segment = text.split(DRAFT_MARKER, 1)[1]
        raw = segment.split(TASK_MARKER, 1)[0].strip()
        try:
            draft = json.loads(raw)
        except json.JSONDecodeError:
            draft = {"steps": []}
        return json.dumps({"critique": "Draft reviewed against the tools-only spec; "
                                       "argument names canonical, validations present.",
                           "revised_plan": draft})
    if "Customer query:" in text and "TOOLS-ONLY" in text:   # planning call
        query = text.split("Customer query:", 1)[1]
        for marker, plan in PLANS:
            if marker.lower() in query.lower():
                return json.dumps(plan)
        return json.dumps(_browse_plan())
    if "Explain in simple terms" in text:
        return ("The requested quantity exceeds the stock on hand, so the order was "
                "stopped before any sale was recorded. Offer the available quantity "
                "or restock first.")
    if "Write the reply now." in text:
        return ("Thanks for your visit! Your request has been taken care of — "
                "let us know if we can help with anything else.")
    return "A single-sentence canned reply for the offline dry-run."
