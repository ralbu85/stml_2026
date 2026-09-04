#!/usr/bin/env bash
# Full offline validation of every first-half notebook (labs + homework).
set -euo pipefail
cd "$(dirname "$0")/.."
RUN=".venv/bin/python tests/dryrun_harness.py"

$RUN ../lectures/week01/W1_lab_setup.ipynb            tests/dryrun_w1_responder.py
$RUN ../lectures/week02/W2_lab_prompting.ipynb        tests/dryrun_w2_responder.py
$RUN ../lectures/week02/W2_hw_prompting.ipynb        tests/dryrun_w2_responder.py
$RUN ../lectures/week03/W3_lab_tools.ipynb            tests/dryrun_w3_responder.py
$RUN ../lectures/week03/W3_hw_new_tool.ipynb          tests/dryrun_w3_hw_responder.py
$RUN ../lectures/week04/W4_lab_loop.ipynb             tests/dryrun_w4_responder.py
$RUN ../lectures/week04/W4_hw_loop_guard.ipynb        tests/dryrun_w4_hw_responder.py
$RUN ../lectures/week05/W5_lab_reflection_evals.ipynb tests/dryrun_w5_responder.py

cp data/coffee_sales.csv coffee_sales.csv
cleanup() {
  rm -f coffee_sales.csv chart_v1.png chart_v2.png chart_v3.png \
    chart_v2_codeonly.png drink_sales_v1.png drink_sales_v2.png
}
trap cleanup EXIT
$RUN ../lectures/week05/W5_hw_chart_reflection.ipynb  tests/dryrun_w5_hw_responder.py

$RUN ../lectures/week06/W6_lab_multiagent.ipynb       tests/dryrun_w6_responder.py
$RUN ../lectures/week06/W6_hw_new_intent.ipynb        tests/dryrun_w6_hw_responder.py
$RUN ../lectures/week07/W7_lab_research_agent.ipynb   tests/dryrun_w7_responder.py
$RUN ../lectures/week07/W7_hw_own_topic.ipynb         tests/dryrun_w7_hw_responder.py
echo "ALL DRY-RUNS OK"
