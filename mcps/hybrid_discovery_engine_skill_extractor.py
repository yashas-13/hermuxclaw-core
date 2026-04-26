# AUTO-GENERATED HYBRID MCP
import sys, os
sys.path.append(os.path.expanduser("~/hermuxclaw"))
from skills.discovery_engine import run as run_a
from skills.skill_extractor import run as run_b

def run(input_data):
    # Pipeline: output of A becomes input of B
    res_a = run_a(input_data)
    if isinstance(res_a, dict) and res_a.get("status") == "success":
        # Attempt to pass result payload
        next_input = {"data": res_a.get("result", res_a)}
        return run_b(next_input)
    return res_a