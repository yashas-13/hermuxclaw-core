
import os
import json
import importlib.util
from datetime import datetime

META = {
    "name": "_evolution_and_sync",
    "version": "harvested-1.1",
    "description": "Auto-harvested from ecosystem.py",
    "inputs": ["new_skills"],
    "outputs": ["result"]
}

def _evolution_and_sync(self, new_skills):
    print("  [🧬 EVOLUTION & SWARM] Integrating DNA...")
    # Add newly harvested skills to genetic population
    for skill_name in new_skills:
        skill_info = self.core.registry["skills"][skill_name]
        with open(skill_info["path"], "r") as f:
            code = f.read()
        self.genetic_engine.add_to_population(skill_name, code, fitness=0.6, generation=0)
    # Sync with peers
    self.swarm_node.sync_swarm()
    # Evolve
    if len(self.genetic_engine.population) >= 2:
        self.genetic_engine.evolve_cycle(generations=1)


def run(input_data):
    # Auto-generated wrapper
    try:
        # Map input_data to function args
        kwargs = {k: input_data.get(k) for k in META["inputs"] if k in input_data}
        # Note: If it was a method, this execution might fail without 'self' context.
        # This is a known limitation of the initial extraction phase.
        res = _evolution_and_sync(**kwargs)
        return {"status": "success", "result": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
