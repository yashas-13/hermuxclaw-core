
import os
import json
import importlib.util
from datetime import datetime

META = {
    "name": "register_skill",
    "version": "harvested-1.1",
    "description": "Auto-harvested from evolution_engine.py",
    "inputs": ["skill_file"],
    "outputs": ["result"]
}

def register_skill(self, skill_file):
    """Dynamic loading and registration of a skill"""
    skill_name = os.path.basename(skill_file).replace(".py", "")
    
    # Load the module
    spec = importlib.util.spec_from_file_location(skill_name, skill_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    if hasattr(module, "META") and hasattr(module, "run"):
        self.registry["skills"][skill_name] = {
            "meta": module.META,
            "path": skill_file,
            "added_at": datetime.now().isoformat(),
            "status": "verified"
        }
        self._save_registry()
        print(f"[✓] Skill registered: {skill_name}")
        return True
    return False


def run(input_data):
    # Auto-generated wrapper
    try:
        # Map input_data to function args
        kwargs = {k: input_data.get(k) for k in META["inputs"] if k in input_data}
        # Note: If it was a method, this execution might fail without 'self' context.
        # This is a known limitation of the initial extraction phase.
        res = register_skill(**kwargs)
        return {"status": "success", "result": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
