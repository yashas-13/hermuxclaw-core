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

    def forge_tool(self, intent, test_payload):
        print(f"\n[🔨 TOOLSMITH] Forging new capability: {intent}")
        
        # 1. Generate Varieties (Simulation of LLM variety generation)
        varieties = self._generate_varieties(intent)
        print(f"  [🧪] Testing {len(varieties)} variations in sandbox tournament...")
        
        best_variant = None
        best_score = -1
        
        for i, code in enumerate(varieties):
            # 2. Tournament Test
            start_time = time.time()
            result = self.sandbox.execute(code, input_data=test_payload)
            elapsed = time.time() - start_time
            
            if result.get("status") == "success":
                # Optimal result criteria: Success + Speed + Output Validity
                score = 1.0 / (elapsed + 0.001) # Faster is better
                print(f"    - Variant {i+1}: SUCCESS (Score: {score:.2f})")
                
                if score > best_score:
                    best_score = score
                    best_variant = code
            else:
                print(f"    - Variant {i+1}: FAILED")

        if best_variant:
            # 3. Store Technique as Auto Tool
            tool_name = intent.lower().replace(" ", "_")
            tool_path = os.path.join(self.toolkit_dir, f"{tool_name}.py")
            
            with open(tool_path, "w") as f:
                f.write(best_variant)
            
            print(f"  [✓] Optimal tool stored in toolkit: {tool_name}")
            self.logger.info(f"Forged new tool: {tool_name}", context={"intent": intent, "score": best_score})
            return True
            
        return False

    def _generate_varieties(self, intent):
        """Calls Neural Intelligence to provide multiple code implementations."""
        # For the prototype, we use the neural_mutator skill via the core engine logic
        # Here we mock the result to show the tournament logic
        return [
            f"def run(data):\\n    # Variant 1 (Direct)\\n    return f'Processed {{data}}'",
            f"def run(data):\\n    import time\\n    time.sleep(0.1)\\n    # Variant 2 (Robust but slower)\\n    return {{'result': data, 'status': 'ok'}}"
        ]

if __name__ == "__main__":
    smith = ToolSmith()
    smith.forge_tool("Echo Service", "Hello World")
