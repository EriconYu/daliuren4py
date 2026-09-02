import json, subprocess
from pathlib import Path
_ENGINE=Path(__file__).with_name("engine.cjs")
def calculate(input_data:dict)->dict:
    completed=subprocess.run(["node",str(_ENGINE)],input=json.dumps(input_data,ensure_ascii=False),text=True,capture_output=True)
    payload=json.loads(completed.stdout or "{}")
    if completed.returncode or not payload.get("ok"): raise RuntimeError(payload.get("error") or completed.stderr or "engine failed")
    return payload["data"]
def canonical(input_data:dict)->dict:
    completed=subprocess.run(["node",str(_ENGINE)],input=json.dumps(input_data,ensure_ascii=False),text=True,capture_output=True)
    payload=json.loads(completed.stdout or "{}")
    if completed.returncode or not payload.get("ok"): raise RuntimeError(payload.get("error") or completed.stderr or "engine failed")
    return payload["canonical"]
