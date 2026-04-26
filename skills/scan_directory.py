
import os
import json
import importlib.util
from datetime import datetime

META = {
    "name": "scan_directory",
    "version": "harvested-1.1",
    "description": "Auto-harvested from discovery_engine.py",
    "inputs": ["path", "depth", "max_depth"],
    "outputs": ["result"]
}

def scan_directory(path, depth, max_depth):
    if depth > max_depth:
        return []

    candidates = []
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir():
                    if entry.name.startswith('.'):
                        if entry.name == '.git':
                            candidates.append({"type": "repository", "path": path})
                        continue
                    candidates.extend(scan_directory(entry.path, depth + 1, max_depth))
                elif entry.is_file() and entry.name.endswith('.py'):
                    # Check for "interesting" signals in file
                    if os.path.getsize(entry.path) > 500: # Ignore tiny files
                        candidates.append({"type": "module", "path": entry.path})
    except PermissionError:
        pass
    return candidates



def run(input_data):
    # Auto-generated wrapper
    try:
        # Map input_data to function args
        kwargs = {k: input_data.get(k) for k in META["inputs"] if k in input_data}
        # Note: If it was a method, this execution might fail without 'self' context.
        # This is a known limitation of the initial extraction phase.
        res = scan_directory(**kwargs)
        return {"status": "success", "result": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
