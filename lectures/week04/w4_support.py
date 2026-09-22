"""Provided Week 4 utilities: data, arithmetic, tool schema, and saved-trace display.

No model calls, agent loop, query planning, answer correction, or grading occur here.
Keep this file beside W4_lab_sql_manual.ipynb (upload both files in Colab).
"""
from pathlib import Path
import json
import random
import sqlite3

import ast
from decimal import Decimal, localcontext
import math
import operator


def calculate(expression: str) -> dict:
    """Calculate arithmetic on retrieved numbers using +, -, *, /, and parentheses only. For several scalar results, separate expressions with semicolons; all results are returned in one call. Functions such as round and max are not supported. Use SQL for calculations over database rows. Limit: 20,000 characters and 100 expressions.

    Args:
        expression: One numeric expression, or semicolon-separated expressions for several results. Each expression returns its final value, not intermediate values. Round returned values for presentation without another calculation.
    """
    operations = {ast.Add: operator.add, ast.Sub: operator.sub,
                  ast.Mult: operator.mul, ast.Div: operator.truediv}

    def evaluate(root):
        # An explicit stack handles long sums without recursive evaluation.
        pending, values = [(root, False)], {}
        while pending:
            node, ready = pending.pop()
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                values[id(node)] = Decimal(str(node.value))
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                if ready:
                    value = values.pop(id(node.operand))
                    values[id(node)] = value if isinstance(node.op, ast.UAdd) else -value
                else:
                    pending.extend([(node, True), (node.operand, False)])
            elif isinstance(node, ast.BinOp) and type(node.op) in operations:
                if ready:
                    left, right = values.pop(id(node.left)), values.pop(id(node.right))
                    values[id(node)] = operations[type(node.op)](left, right)
                else:
                    pending.extend([(node, True), (node.right, False), (node.left, False)])
            else:
                raise ValueError('Use numbers, +, -, *, /, and parentheses only.')
        return values[id(root)]

    try:
        if len(expression) > 20000:
            raise ValueError('Expression exceeds 20,000 characters; use SQL aggregation or smaller expressions.')
        expressions = expression.split(';')
        if len(expressions) > 100:
            raise ValueError('At most 100 expressions per request; use SQL aggregation.')
        results = []
        for part in expressions:
            tree = ast.parse(part.strip(), mode='eval')
            if sum(1 for _ in ast.walk(tree)) > 20000:
                raise ValueError('Expression exceeds 20,000 syntax nodes; use SQL aggregation or smaller expressions.')
            with localcontext() as context:
                context.prec = 40
                value = float(evaluate(tree.body))
            if not math.isfinite(value):
                raise ValueError('Result must be finite.')
            results.append({'expression': part.strip(), 'result': value})
        return {'expression': expression, 'result': results[0]['result']} if len(results) == 1 else {'results': results}
    except (SyntaxError, ValueError, ArithmeticError, RecursionError) as error:
        return {'error': f'{type(error).__name__}: {error}'}


DB_CONTEXT = """Database schema:
customers(customer_id INTEGER PRIMARY KEY, name TEXT, country TEXT)
products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT)
orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER REFERENCES customers,
       ordered_at TEXT, status TEXT)
order_items(order_id INTEGER REFERENCES orders, product_id INTEGER REFERENCES products,
            quantity INTEGER, unit_price REAL, PRIMARY KEY(order_id, product_id))

Row meanings: orders has one row per order; order_items has one row per product within an order. A customer may have multiple orders, and an order may have multiple item rows.
A join to order_items produces item-level rows: order_id and customer_id can repeat. Count each requested entity once; aggregate at the requested entity's level before taking an average. Do not average repeated entity totals after a one-to-many join.
"""

def prepare_shop(path: Path) -> Path:
    """Reset the generated teaching DB at path; return its Path. No API request."""
    DB_PATH = Path(path)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.unlink(missing_ok=True)
    with sqlite3.connect(DB_PATH) as db:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY, name TEXT, country TEXT);
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY, name TEXT, category TEXT);
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(customer_id),
            ordered_at TEXT, status TEXT);
        CREATE TABLE order_items (
            order_id INTEGER REFERENCES orders(order_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER, unit_price REAL,
            PRIMARY KEY (order_id, product_id));
        """)
        countries = ["USA", "Canada", "UK", "Germany", "France"]
        db.executemany("INSERT INTO customers VALUES (?, ?, ?)",
            [(i, f"Customer {i:02d}", countries[(i-1) % 5]) for i in range(1, 31)])
        products = [(1,"Desk lamp","Home"),(2,"Storage box","Home"),(3,"Mug","Home"),
            (4,"Notebook","Stationery"),(5,"Pen set","Stationery"),(6,"Planner","Stationery"),
            (7,"Headphones","Electronics"),(8,"Keyboard","Electronics"),(9,"Mouse","Electronics"),
            (10,"Cable","Electronics"),(11,"Desk mat","Home"),(12,"Folder","Stationery")]
        db.executemany("INSERT INTO products VALUES (?, ?, ?)", products)
        prices = {1:25,2:15,3:10,4:5,5:10,6:15,7:80,8:50,9:25,10:10,11:20,12:5}
        rng = random.Random(42)
        order_id = 0
        for month, count in [(1,80),(2,100),(3,65)]:
            for i in range(count):
                order_id += 1
                status = "cancelled" if i % 9 == 0 else "completed"
                db.execute("INSERT INTO orders VALUES (?, ?, ?, ?)",
                    (order_id, rng.randint(1,28), f"2025-{month:02d}-{1+i%28:02d}", status))
                choices = list(prices) if month < 3 else [1,2,3,4,5,6,10,11,12]
                for product_id in rng.sample(choices, rng.randint(1,3)):
                    db.execute("INSERT INTO order_items VALUES (?, ?, ?, ?)",
                        (order_id, product_id, rng.randint(1,3), prices[product_id]))
    return DB_PATH


def finish(answer: str) -> dict:
    """Return a submitted answer, or an error for an empty answer; no grading."""
    if not answer.strip():
        return {"error": "Supply a nonempty final answer."}
    return {"answer": answer}


def action_tools(react=False) -> list:
    """Describe one act request to the API; ReAct adds a thought field before action.

    This is a JSON schema, not a Python executor. The notebook dispatches actions.
    """
    fields = {}
    if react:
        fields["thought"] = {
            "type": "string",
            "description": "Assess current evidence, what is still missing, and why the next action or final answer follows."
        }
    fields["action"] = {"type": "string", "enum": ["run_sql", "calculate", "finish"]}
    fields["action_input"] = {
        "type": "string",
        "description": "run_sql: one read-only SQLite query. calculate: numbers, + - * / and parentheses (semicolon separates expressions). finish: final answer text."
    }
    return [{"type": "function", "function": {
        "name": "act",
        "description": "Choose an operation and supply its input. Python executes it and returns the result.",
        "strict": True,
        "parameters": {"type": "object", "properties": fields,
                       "required": list(fields), "additionalProperties": False}
    }}]


def show_exchange(request, result):
    """Print one request and its actual result; no execution or truncation."""
    if "thought" in request:
        print("Thought:", request["thought"])
    print("Action:", request["action"])
    print("Input:", request["action_input"])
    print("Observation:", json.dumps(result, ensure_ascii=False, indent=2))


def show_trace(messages):
    """Read stored messages and display each matched request/result; no API call."""
    requests = {}
    turn = 0
    for message in messages:
        for call in message.get("tool_calls", []):
            requests[call["id"]] = json.loads(call["function"]["arguments"])
        if message["role"] == "tool":
            turn += 1
            print(f"\n--- Exchange {turn} ---")
            show_exchange(requests[message["tool_call_id"]], json.loads(message["content"]))
