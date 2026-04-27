# skills/skill_validator_skill.py
import importlib.util
import sys
import time
import os
from skills.base_skill import BaseSkill

class SkillValidatorSkill(BaseSkill):
    """
    Registry Gatekeeper.
    Validates any skill file against the BaseSkill contract before it is officially registered.
    """
    META = {
        "name": "skill_validator_skill",
        "version": "1.0.0",
        "inputs": ["skill_path", "test_input"],
        "outputs": ["valid", "errors", "latency_ms"],
        "dependencies": []
    }

    def run(self, input_data):
        path = os.path.expanduser(input_data["skill_path"])
        errors = []
        
        try:
            # 1. Attempt to load the module dynamically
            spec = importlib.util.spec_from_file_location("candidate", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            
            # 2. Check for BaseSkill implementation
            cls = [v for v in vars(mod).values()
                   if isinstance(v, type) and issubclass(v, BaseSkill)
                   and v is not BaseSkill]
            
            if not cls:
                errors.append("No class inheriting from BaseSkill found in file.")
                return {"valid": False, "errors": errors, "latency_ms": 0}
            
            # 3. Instantiate and validate metadata
            instance = cls[0]()
            instance.validate_meta()
            
            # 4. Perform a dry-run test
            start = time.perf_counter()
            instance.run(input_data.get("test_input", {}))
            ms = round((time.perf_counter() - start) * 1000, 2)
            
            return {"valid": True, "errors": [], "latency_ms": ms}
            
        except Exception as e:
            errors.append(str(e))
            return {"valid": False, "errors": errors, "latency_ms": 0}
