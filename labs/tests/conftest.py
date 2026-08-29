import sys
from pathlib import Path

# labs/ 를 import 경로에 추가 — 어디서 pytest를 실행해도 docqa 를 찾는다
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
