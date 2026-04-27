import os
import sys
import json
import time

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.sandbox import Sandbox
from core.log_manager import get_logger

class ToolSmith:
    """
    Proactive Evolution Engine.
    Generates variety outputs for an intent, finds optimal logic, and stores it as a permanent skill.
    """
    def __init__(self):
        self.toolkit_dir = os.path.expanduser("~/hermuxclaw/toolkit")
        self.sandbox = Sandbox(timeout=5)
        self.logger = get_logger("ToolSmith")

    def forge_tool(self, intent, test_payload, turbo=False):
        print(f"\n[🔨 TOOLSMITH] Forging {'TURBO ' if turbo else ''}capability: {intent}")
        
        # 1. GENERATE VARIETIES
        count = 15 if turbo else 5
        varieties = self._generate_varieties(intent, count=count)
        print(f"  [🏟️] Entering Tournament Arena: {len(varieties)} competitors detected.")
        
        best_variant = None
        best_time = float('inf')
        
        for i, code in enumerate(varieties):
            # 2. TOURNAMENT TEST
            start_time = time.time()
            result = self.sandbox.execute(code, input_data=test_payload)
            elapsed = time.time() - start_time
            
            if result.get("status") == "success":
                print(f"    - Competitor {i+1:02}: SUCCESS in {elapsed:.4f}s")
                if elapsed < best_time:
                    best_time = elapsed
                    best_variant = code
            else:
                print(f"    - Competitor {i+1:02}: DISQUALIFIED")

        if best_variant:
            # 3. STORAGE
            tool_name = intent.lower().replace(" ", "_")
            tool_path = os.path.join(self.toolkit_dir, f"{tool_name}.py")
            with open(tool_path, "w") as f:
                f.write(best_variant)
            
            print(f"  [👑] TOURNAMENT WINNER: {tool_name} (Time: {best_time:.4f}s)")
            return True
        return False

    def _generate_varieties(self, intent, count=10):
        """Generates multiple strategies for the same objective."""
        # Correctly formatted code for the sandbox
        varieties = []
        for i in range(count):
            jitter = f"\n    # Jitter variation {i+1}\n"
            if i % 2 == 0:
                code = f"def run(data):{jitter}    return f'Result: {{data}}'"
            else:
                code = f"def run(data):{jitter}    return {{'payload': data, 'ver': {i}}}"
            varieties.append(code)
        return varieties

if __name__ == "__main__":
    smith = ToolSmith()
    smith.forge_tool("Echo Service", "Hello World")
