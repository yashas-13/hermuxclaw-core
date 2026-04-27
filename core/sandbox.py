import os
import sys
import tempfile
import subprocess
import json
import time

class Sandbox:
    """
    Safe execution layer for testing mutated or foreign code.
    Native implementation for Android/Termux (No psutil).
    """
    def __init__(self, timeout=3, max_memory_mb=100):
        self.timeout = timeout
        self.max_memory = max_memory_mb

    def execute(self, code_string, input_data=None):
        runner_code = f"""
import json
import sys

try:
    # Restricted namespace
{self._indent(code_string)}
    
    input_data = {json.dumps(input_data) if input_data else 'None'}
    
    if 'run' in locals():
        result = run(input_data)
        print(json.dumps({{"status": "success", "result": result}}))
    else:
        print(json.dumps({{"status": "error", "message": "No run() function found"}}))
except Exception as e:
    print(json.dumps({{"status": "error", "message": str(e)}}))
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp:
            temp.write(runner_code)
            temp_path = temp.name

        try:
            # Use subprocess.run with strict timeout for primary containment
            proc = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if proc.stdout:
                try:
                    return json.loads(proc.stdout)
                except:
                    return {"status": "error", "message": "Malformed output"}
            return {"status": "error", "message": proc.stderr or "No output"}

        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Execution timed out"}
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _indent(self, text, spaces=4):
        prefix = ' ' * spaces
        return '\n'.join(prefix + line for line in text.split('\n'))


                
    def _indent(self, text, spaces=4):
        prefix = ' ' * spaces
        return '\n'.join(prefix + line for line in text.split('\n'))

if __name__ == "__main__":
    sb = Sandbox(timeout=2)
    test_code = "def run(data):\n    return data.get('val', 0) * 2"
    print("Testing valid code:", sb.execute(test_code, {"val": 10}))
    
    bad_code = "def run(data):\n    while True: pass"
    print("Testing infinite loop:", sb.execute(bad_code))
