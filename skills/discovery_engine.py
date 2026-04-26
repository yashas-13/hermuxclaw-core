import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor

META = {
    "name": "discovery_engine",
    "version": "1.1",
    "description": "High-speed workspace scanner for capability discovery.",
    "inputs": ["search_path", "max_depth"],
    "outputs": ["candidates"]
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
    search_path = input_data.get("search_path", os.path.expanduser("~"))
    max_depth = input_data.get("max_depth", 3)
    
    print(f"[*] Discovery Engine: Scanning {search_path} (depth={max_depth})...")
    
    # Using ThreadPoolExecutor for fast scanning of large directory trees
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(scan_directory, search_path, 0, max_depth)
        results = future.result()
    
    # Filter and deduplicate
    repos = [c for c in results if c["type"] == "repository"]
    modules = [c for c in results if c["type"] == "module"]
    
    return {
        "status": "success",
        "counts": {"repos": len(repos), "modules": len(modules)},
        "candidates": results
    }

if __name__ == "__main__":
    res = run({"search_path": os.path.expanduser("~"), "max_depth": 2})
    print(json.dumps(res["counts"], indent=2))
