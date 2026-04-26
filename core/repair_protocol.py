import os
import sys
import ast

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.evolution_engine import HermuxclawCore
from core.log_manager import get_logger

class RepairProtocol:
    """
    Automated Self-Healing Protocol.
    Analyzes error logs and uses Neural Intelligence to apply fixes.
    """
    def __init__(self):
        self.core = HermuxclawCore()
        self.logger = get_logger("RepairProtocol")

    def execute_repair(self, error_entry):
        component = error_entry.get("component")
        error_msg = error_entry.get("message")
        traceback = error_entry.get("context", {}).get("traceback")
        
        print(f"  [💊] Healing Component: {component}")
        
        # 1. Identify Target File (This logic assumes component name matches skill name)
        skill_info = self.core.registry["skills"].get(component)
        if not skill_info:
            self.logger.error("Could not find file for component", "RepairFailure", context={"component": component})
            return False

        file_path = skill_info["path"]
        with open(file_path, "r") as f:
            source_code = f.read()

        # 2. Call Neural Intelligence for a Fix
        prompt = f"""
        Act as an elite Debugging Specialist. A Python component has failed.
        
        FILE: {file_path}
        ERROR: {error_msg}
        TRACEBACK: {traceback}
        
        SOURCE CODE:
        {source_code}
        
        Analyze the failure and return the complete corrected source code. 
        Ensure no other functionality is broken. Output ONLY the raw Python code.
        """
        
        print(f"    [🧠] Generating Fix via Neural Mutator...")
        fix_res = self.core.execute_skill("neural_mutator", {"raw_code": source_code, "context_description": f"Repair fix for {error_msg}"})
        
        if fix_res.get("status") == "success":
            corrected_code = fix_res.get("refined_code")
            
            # 3. Safety Check
            try:
                ast.parse(corrected_code)
                # 4. Apply Fix
                with open(file_path, "w") as f:
                    f.write(corrected_code)
                print(f"    [✓] Fix applied and validated for {component}.")
                self.logger.info(f"Successfully healed component: {component}")
                return True
            except Exception as e:
                print(f"    [!] Neural fix failed syntax check: {e}")
                self.logger.error("Neural fix invalid", "SyntaxError", context={"error": str(e)})
        
        return False
