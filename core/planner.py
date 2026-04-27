# core/planner.py
from typing import Dict, List

class Planner:
    """
    Task Decomposition Engine.
    Translates high-level directives into ordered execution steps.
    """
    def decompose(self, task: Dict) -> Dict:
        """
        Receives a task dictionary and returns a plan.
        Plan Format: {"name": "task_name", "steps": [{"skill": "skill_name", "input": {...}}]}
        """
        # If steps are already provided (direct execution mode)
        if "steps" in task and task["steps"]:
            return task

        # Default mapping logic (can be expanded with LLM)
        name = task.get("name", "unknown")
        
        # Simple rule-based planner for bootstrapping
        if name == "inventory_check":
            return {
                "name": name,
                "steps": [
                    {"skill": "sap_inventory_skill", "input": task.get("input", {})}
                ]
            }
        elif name == "alert_client":
            return {
                "name": name,
                "steps": [
                    {"skill": "whatsapp_alert_skill", "input": task.get("input", {})}
                ]
            }
            
        # Return empty plan if unknown
        return {"name": name, "steps": []}
