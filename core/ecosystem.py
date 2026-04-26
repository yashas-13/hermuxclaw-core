import os
import json
import time
from datetime import datetime
import sys

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.evolution_engine import HermuxclawCore
from core.genetic_engine import GeneticEngine
from core.swarm_node import SwarmNode
from core.root_intelligence import RootSystem

class EcosystemLifecycle:
    def __init__(self):
        self.core = HermuxclawCore()
        self.mcps_dir = os.path.expanduser("~/hermuxclaw/mcps")
        self.genetic_engine = GeneticEngine()
        self.swarm_node = SwarmNode()
        self.root_system = RootSystem(self.core)
        self.targets = [
            os.path.expanduser("~/lead_engine"),
            os.path.expanduser("~/HacxGPT-CLI"),
            os.path.expanduser("~/hermuxclaw") # Self-reflection
        ]

    def run_cycle(self):
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🌍 INITIATING ECOSYSTEM CYCLE")
        
        # 1. Germination & Growth (Discovery & Extraction)
        new_skills = self._germination_and_growth()
        
        # 2. Pollination (Combining skills into MCPs)
        if len(self.core.registry["skills"]) >= 2:
            self._pollination()
            
        # 3. Decay (Pruning weak skills)
        self._decay()

        # 4. Swarm Sync & Genetic Evolution
        self._evolution_and_sync(new_skills)
        
        # 5. Soil Enrichment (Memory update)
        self.core._save_registry()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌍 CYCLE COMPLETE. Active Skills: {len(self.core.registry['skills'])}, Population: {len(self.genetic_engine.population)}")

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

    def _germination_and_growth(self):
        print("  [🌱 GERMINATION & 🌿 GROWTH] Semantic AST Harvesting...")
        new_additions = []
        
        # Index fragments into the semantic index
        indexed_count = self.root_system.harvest_semantically(self.targets)
        
        if indexed_count >= 0:
            print("  [🔍] Seeking high-value structural concepts from Semantic Memory...")
            # Query the root intelligence for high-value targets to extract as standalone skills
            intents = ["core logic", "data processing", "network requests", "system utilities", "machine learning"]
            for intent in intents:
                matches = self.root_system.filter.find_relevant(intent, top_k=1)
                for m in matches:
                    frag = m['metadata']
                    if frag['type'] == 'function':
                        extract_res = self.core.execute_skill("skill_extractor", {
                            "module_path": frag['file'], 
                            "target_function": frag['name']
                        })
                        if extract_res.get("status") == "success":
                            skill_name = extract_res["skill_name"]
                            if skill_name not in self.core.registry["skills"]:
                                if self.core.register_skill(extract_res["file_path"]):
                                    # Initialize ecosystem stats
                                    self.core.registry["skills"][skill_name]["score"] = 1.0
                                    self.core.registry["skills"][skill_name]["usage_count"] = 0
                                    self.core.registry["skills"][skill_name]["last_used"] = datetime.now().isoformat()
                                    new_additions.append(skill_name)
                                    print(f"    [+] Semantically Grown: {skill_name} (Match Score: {m['score']:.2f})")
                                    
        return new_additions

    def _pollination(self):
        print("  [🌼 POLLINATION] Synthesizing MCPs...")
        skills = list(self.core.registry["skills"].keys())
        
        # Simple genetic cross: Combine two random/recent skills
        # In a real neural setup, this uses semantic matching. For now, adjacency.
        for i in range(min(len(skills)-1, 2)): # Max 2 new MCPs per cycle
            s1, s2 = skills[i], skills[i+1]
            mcp_name = f"hybrid_{s1}_{s2}.py"
            mcp_path = os.path.join(self.mcps_dir, mcp_name)
            
            if not os.path.exists(mcp_path):
                code = f'''
# AUTO-GENERATED HYBRID MCP
import sys, os
sys.path.append(os.path.expanduser("~/hermuxclaw"))
from skills.{s1} import run as run_a
from skills.{s2} import run as run_b

def run(input_data):
    # Pipeline: output of A becomes input of B
    res_a = run_a(input_data)
    if isinstance(res_a, dict) and res_a.get("status") == "success":
        # Attempt to pass result payload
        next_input = {{"data": res_a.get("result", res_a)}}
        return run_b(next_input)
    return res_a
'''
                with open(mcp_path, "w") as f:
                    f.write(code.strip())
                print(f"    [+] Pollinated: {mcp_name}")

    def _decay(self):
        print("  [🍂 DECAY] Pruning weak logic...")
        to_delete = []
        for name, data in self.core.registry["skills"].items():
            # Core system skills are immune to decay
            if name in ["ast_analyzer", "discovery_engine", "skill_extractor"]:
                continue
                
            # Age penalty
            added_at = datetime.fromisoformat(data["added_at"])
            age_hours = (datetime.now() - added_at).total_seconds() / 3600
            
            # Simple decay formula: score drops over time if unused
            data["score"] = max(0.1, data.get("score", 1.0) - (age_hours * 0.01))
            
            if data["score"] < 0.3:
                to_delete.append((name, data["path"]))
                
        for name, path in to_delete:
            print(f"    [-] Decayed: {name} (Score: {self.core.registry['skills'][name]['score']:.2f})")
            del self.core.registry["skills"][name]
            if os.path.exists(path):
                os.remove(path)

if __name__ == "__main__":
    eco = EcosystemLifecycle()
    eco.run_cycle()
