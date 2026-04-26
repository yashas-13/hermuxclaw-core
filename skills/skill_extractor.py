import os
import json
import ast
import sys
import textwrap

# Ensure core is accessible
sys.path.append(os.path.expanduser("~/hermuxclaw"))
from skills import ast_analyzer

META = {
    "name": "skill_extractor",
    "version": "1.1",
    "description": "Extracts high-value logic from modules and wraps them as Hermuxclaw skills.",
    "inputs": ["module_path", "target_function"],
    "outputs": ["skill_file_path"]
}

def extract_code_block(file_path, start_line, end_line):
    with open(file_path, "r") as f:
        lines = f.readlines()
        block = lines[start_line-1:end_line]
        if not block:
            return ""
        # Find leading spaces of the first line
        first_line = block[0]
        leading_spaces = len(first_line) - len(first_line.lstrip())
        
        cleaned = []
        for line in block:
            if len(line) >= leading_spaces and line[:leading_spaces].isspace():
                cleaned.append(line[leading_spaces:])
            else:
                cleaned.append(line.lstrip())
        return "".join(cleaned)

def run(input_data):
    module_path = input_data.get("module_path")
    target_function = input_data.get("target_function")
    
    if not module_path or not os.path.exists(module_path):
        return {"status": "error", "message": "Invalid module path."}

    # 1. Analyze the module
    analysis = ast_analyzer.run({"file_path": module_path})
    if analysis["status"] != "success":
        return analysis

    data = analysis["data"]
    
    # 2. Find the target function or a high-value candidate
    found_func = None
    if target_function:
        found_func = next((f for f in data["functions"] if f["name"] == target_function), None)
    else:
        # Heuristic: Pick the first function with a docstring or multiple args
        for f in data["functions"]:
            # Skip common names that might be less useful in isolation
            if f["name"] in ["__init__", "main", "run"]:
                continue
            if f["docstring"] or len(f["args"]) > 1:
                found_func = f
                break

    if not found_func:
        return {"status": "error", "message": "No suitable function found for extraction."}

    # 3. Determine function boundaries
    start_line = found_func["line"]
    # Simple heuristic for end line
    next_func = next((f for f in data["functions"] if f["line"] > start_line), None)
    end_line = next_func["line"] - 1 if next_func else 9999
    
    code_content = extract_code_block(module_path, start_line, end_line)
    
    # 4. Clean up inputs (remove 'self' if it's a method)
    inputs = [a for a in found_func["args"] if a != "self"]
    
    # 5. Wrap into Skill Contract
    skill_name = found_func["name"].lower()
    wrapped_skill = f'''
import os
import json
import importlib.util
from datetime import datetime

META = {{
    "name": "{skill_name}",
    "version": "harvested-1.1",
    "description": "Auto-harvested from {os.path.basename(module_path)}",
    "inputs": {json.dumps(inputs)},
    "outputs": ["result"]
}}

{code_content}

def run(input_data):
    # Auto-generated wrapper
    try:
        # Map input_data to function args
        kwargs = {{k: input_data.get(k) for k in META["inputs"] if k in input_data}}
        # Note: If it was a method, this execution might fail without 'self' context.
        # This is a known limitation of the initial extraction phase.
        res = {found_func["name"]}(**kwargs)
        return {{"status": "success", "result": res}}
    except Exception as e:
        return {{"status": "error", "message": str(e)}}
'''
    
    # 5. Save to skills directory
    output_path = os.path.expanduser(f"~/hermuxclaw/skills/{skill_name}.py")
    with open(output_path, "w") as f:
        f.write(wrapped_skill)
    
    return {
        "status": "success", 
        "skill_name": skill_name, 
        "file_path": output_path,
        "extracted_from": module_path
    }

if __name__ == "__main__":
    # Test extraction from discovery_engine itself
    test_path = os.path.expanduser("~/hermuxclaw/skills/discovery_engine.py")
    res = run({"module_path": test_path, "target_function": "scan_directory"})
    print(json.dumps(res, indent=2))
