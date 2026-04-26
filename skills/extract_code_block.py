
import os
import json
import importlib.util
from datetime import datetime

META = {
    "name": "extract_code_block",
    "version": "harvested-1.1",
    "description": "Auto-harvested from skill_extractor.py",
    "inputs": ["file_path", "start_line", "end_line"],
    "outputs": ["result"]
}

def extract_code_block(file_path, start_line, end_line):
    with open(file_path, "r") as f:
        lines = f.readlines()
        raw_code = "".join(lines[start_line-1:end_line])
        return textwrap.dedent(raw_code)



def run(input_data):
    # Auto-generated wrapper
    try:
        # Map input_data to function args
        kwargs = {k: input_data.get(k) for k in META["inputs"] if k in input_data}
        # Note: If it was a method, this execution might fail without 'self' context.
        # This is a known limitation of the initial extraction phase.
        res = extract_code_block(**kwargs)
        return {"status": "success", "result": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
