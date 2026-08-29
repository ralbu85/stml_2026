# API Key Setup Guide (complete before the Week 1 lab)

Every lab in this course calls a large language model through an API. An **API key** is a secret string that identifies your account to the model provider and bills your usage to it. Each student issues their own key once, before the first lab.

All labs run in **Google Colab** through `aisuite`, and using the key is a copy-paste: the first cell of every lab notebook has a `PASTE-YOUR-KEY-HERE` placeholder — replace it with your key and run. Nothing is installed on your machine and nothing is configured outside the notebook.

## 1. Create your key (once)

### Option A — OpenAI (course default)

1. Create an account at <https://platform.openai.com/signup>. This is the developer platform; a ChatGPT subscription is a separate product and does not include API credit.
2. Add prepaid credit: **Settings → Billing → Add payment details**, then purchase the minimum credit (currently $5). Without credit, every call fails with `insufficient_quota`.
3. Set a monthly usage limit of $5 (**Settings → Limits**), so the key can never cost more than that.
4. Create the key: **API keys → Create new secret key**, name it `stml2026`. The key (starts with `sk-`) is shown once — copy it into a private note; you will paste it into each lab notebook.

### Option B — Anthropic

Same shape: account at <https://console.anthropic.com>, $5 prepaid credit under **Settings → Billing**, key under **Settings → API keys** (starts with `sk-ant-`). In each lab notebook, set `ANTHROPIC_API_KEY` instead of `OPENAI_API_KEY` and switch `MODEL` to the commented value (`anthropic:claude-haiku-4-5`). Everything else is identical.

## 2. Paste it into the lab notebook

The setup cell of every lab notebook:

```python
import os

os.environ["OPENAI_API_KEY"] = "PASTE-YOUR-KEY-HERE"

MODEL = "openai:gpt-4o-mini"          # Anthropic accounts: "anthropic:claude-haiku-4-5"
```

Replace the placeholder with your key and run the cell. The key is your personal credential and your own responsibility: it sits in the notebook as plain text, so delete it from the cell before submitting or sharing the file. If a key leaks, revoke it on the provider's API-keys page (instant and free) and create a new one — the $5 limit from step A-3 caps any damage.

## Verify (do this once now)

In a fresh notebook at <https://colab.research.google.com>:

```python
%pip install -q "aisuite[openai,anthropic]"
import os
os.environ["OPENAI_API_KEY"] = "PASTE-YOUR-KEY-HERE"

import aisuite
r = aisuite.Client().chat.completions.create(
    model="openai:gpt-4o-mini",
    messages=[{"role": "user", "content": "Reply with exactly: ready"}])
print(r.choices[0].message.content)
```

Expected output: `ready`. If this prints, your setup is complete and every lab in the course will run.

## Expected cost

The labs use small models on short prompts; a full semester totals well under one million tokens. At current prices (gpt-4o-mini: $0.15 per million input tokens, $0.60 per million output; claude-haiku-4-5: $1 / $5), the $5 minimum credit covers the entire semester with a wide margin. There is no reason to top up more than the minimum.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `AuthenticationError` / HTTP 401 | Key mistyped or pasted with extra spaces | Paste again, exactly; rerun the cell |
| `insufficient_quota` / HTTP 429 (quota) | No prepaid credit on the account | Complete the billing step (A-2 or B) |
| `RateLimitError` / HTTP 429 (rate) | Too many calls per minute (new accounts have low limits) | Wait a minute and rerun |
| `KeyError` / auth error after a runtime restart | Colab reset wiped the environment | Rerun the setup cells from the top |
| Key shown once and lost | Providers show keys only at creation | Delete the old key, create a new one |
