import os
import time
import sys
from datetime import datetime

# HERMUXCLAW ADAPTIVE TRIGGER
# Monitors the workspace for changes and triggers autonomous evolution

WORKSPACE = os.path.expanduser("~")
ECOSYSTEM_PATH = os.path.join(WORKSPACE, "hermuxclaw/core/ecosystem.py")

def get_dir_state(path):
    state = {}
    for root, dirs, files in os.walk(path):
        if "hermuxclaw" in root or ".git" in root or ".cache" in root:
            continue
        for f in files:
            fpath = os.path.join(root, f)
            try:
                state[fpath] = os.path.getmtime(fpath)
            except:
                pass
    return state

def run_watcher():
    print(f"[*] Hermuxclaw Adaptive Trigger: Monitoring {WORKSPACE}...")
    last_state = get_dir_state(WORKSPACE)
    
    while True:
        time.sleep(10) # Poll every 10 seconds
        current_state = get_dir_state(WORKSPACE)
        
        changes = []
        for path, mtime in current_state.items():
            if path not in last_state or mtime > last_state[path]:
                changes.append(path)
        
        if changes:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚡ User Action Detected: {len(changes)} files changed.")
            print(f"[*] Triggering autonomous refinement...")
            # Run the ecosystem cycle in response to user activity
            os.system(f"python3 {ECOSYSTEM_PATH}")
            last_state = current_state
        else:
            # Update state for deleted files
            if len(current_state) != len(last_state):
                last_state = current_state

if __name__ == "__main__":
    try:
        run_watcher()
    except KeyboardInterrupt:
        print("\n[!] Watcher stopped.")
