import sys
import os
import json
from datetime import datetime

class RuntimeTracer:
    """
    Hermuxclaw Behavioral Tracer.
    Captures actual execution flow at the function level.
    """
    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or os.path.expanduser("~/hermuxclaw")
        self.call_stack = []
        self.trace_data = [] # List of (caller, callee, timestamp)

    def trace_calls(self, frame, event, arg):
        if event == 'call':
            code = frame.f_code
            func_name = code.co_name
            filename = code.co_filename
            
            # Only trace code within our workspace to avoid library noise
            if self.workspace_root in filename:
                rel_path = os.path.relpath(filename, self.workspace_root)
                
                # Get caller info
                caller_frame = frame.f_back
                caller_name = "external"
                if caller_frame:
                    caller_name = caller_frame.f_code.co_name
                
                self.trace_data.append({
                    "caller": caller_name,
                    "callee": func_name,
                    "file": rel_path,
                    "timestamp": datetime.now().isoformat()
                })
        return self.trace_calls

    def start(self):
        print("[*] Runtime Tracer: INITIALIZED")
        sys.settrace(self.trace_calls)

    def stop(self):
        sys.settrace(None)
        print(f"[*] Runtime Tracer: STOPPED. Captured {len(self.trace_data)} execution events.")

    def save_trace(self, output_path=None):
        path = output_path or os.path.expanduser("~/hermuxclaw/memory/runtime_trace.json")
        with open(path, "w") as f:
            json.dump(self.trace_data, f, indent=2)
        return path

if __name__ == "__main__":
    # Test Tracer
    tracer = RuntimeTracer()
    tracer.start()
    
    # Simple workload
    def alpha(): return bravo()
    def bravo(): return "Hello"
    alpha()
    
    tracer.stop()
    print(json.dumps(tracer.trace_data, indent=2))
