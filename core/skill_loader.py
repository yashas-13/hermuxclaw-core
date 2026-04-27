# core/skill_loader.py
import importlib.util
import os
import sys
from typing import Optional
from skills.base_skill import BaseSkill

class SkillLoader:
    """
    Dynamic loader for HermuXclaw skills.
    Resolves skill names to instantiated Python classes in the skills/ directory.
    """
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = os.path.expanduser(os.path.join("~/hermuxclaw", skills_dir))

    def load(self, skill_name: str) -> Optional[BaseSkill]:
        """Import a skill file and return an instance of the skill class."""
        file_path = os.path.join(self.skills_dir, f"{skill_name}.py")
        if not os.path.exists(file_path):
            return None

        try:
            # Dynamic import
            spec = importlib.util.spec_from_file_location(skill_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the class that inherits from BaseSkill
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseSkill) and attr is not BaseSkill:
                    return attr()
            return None
        except Exception as e:
            print(f"[!] Error loading skill {skill_name}: {e}")
            return None
