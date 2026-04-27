# core/orchestrator.py
import json, logging, os, sys
from typing import Dict

# Ensure paths are correct for local imports
sys.path.append(os.path.expanduser("~/hermuxclaw"))

from core.planner import Planner
from core.skill_loader import SkillLoader
from memory.skill_registry import SkillRegistry

# Configure detailed logging for observability
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [HX-CORE] %(levelname)s %(message)s')

class Orchestrator:
    """
    The main brain of HermuXclaw.
    Receives a task, decomposes it via the Planner, dispatches to Skills via the Loader,
    and records all metrics in the Registry.
    """
    def __init__(self):
        self.planner = Planner()
        self.loader = SkillLoader()
        self.registry = SkillRegistry()
        logging.info("HermuXclaw Orchestrator initialized")

    def execute(self, task: Dict) -> Dict:
        """Execute a high-level directive."""
        task_name = task.get('name', 'unknown')
        logging.info(f"Task received: {task_name}")
        
        # 1. Decompose directive into steps
        plan = self.planner.decompose(task)
        results = {}
        
        # 2. Execute each step
        for step in plan["steps"]:
            skill_name = step["skill"]
            logging.info(f"Loading skill: {skill_name}")
            
            skill = self.loader.load(skill_name)
            if not skill:
                results[skill_name] = {"error": f"Skill {skill_name} not found"}
                logging.error(f"Skill {skill_name} not found in path")
                continue
                
            try:
                # 3. Run skill and capture benchmark
                out = skill.benchmark(step["input"])
                results[skill_name] = out
                
                # 4. Record successful usage
                self.registry.record_usage(skill_name, success=(out["status"] == "success"))
                logging.info(f"✅ {skill_name} completed in {out['latency_ms']}ms")
                
            except Exception as e:
                results[skill_name] = {"error": str(e)}
                self.registry.record_usage(skill_name, success=False)
                logging.error(f"❌ {skill_name} failed: {e}")
                
        return results

if __name__ == "__main__":
    # Self-test if run directly
    orch = Orchestrator()
    # Execute a dummy health check with no steps to verify boot
    result = orch.execute({"name": "health_check", "steps": []})
    print(json.dumps(result, indent=2))
