import os
import json
import sys

# Ensure core is accessible
sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.evolution_engine import HermuxclawCore

class HarvesterMCP:
    """
    Modular Capability Plugin (MCP) for automated skill harvesting.
    Orchestrates Discovery -> Analysis -> Extraction -> Registration.
    """
    def __init__(self):
        self.core = HermuxclawCore()

    def run(self, target_dir=None):
        if not target_dir:
            target_dir = os.path.expanduser("~")
            
        print(f"\n[MCP] Initiating Capability Harvest in: {target_dir}")
        
        # 1. DISCOVER
        discovery_res = self.core.execute_skill("discovery_engine", {"search_path": target_dir, "max_depth": 2})
        if discovery_res["status"] != "success":
            return discovery_res
        
        candidates = discovery_res["candidates"]
        modules = [c for c in candidates if c["type"] == "module"]
        
        print(f"[*] Found {len(modules)} potential modules.")
        
        harvested_count = 0
        for mod in modules[:5]: # Limit to first 5 for the initial run
            # 2. EXTRACT (Skill Extractor uses AST Analyzer internally)
            print(f"[*] Attempting harvest from: {os.path.basename(mod['path'])}")
            extract_res = self.core.execute_skill("skill_extractor", {"module_path": mod["path"]})
            
            if extract_res["status"] == "success":
                # 3. NEURAL MUTATION (Intelligence Layer)
                skill_path = extract_res["file_path"]
                with open(skill_path, "r") as f:
                    raw_code = f.read()
                
                mutation_res = self.core.execute_skill("neural_mutator", {
                    "raw_code": raw_code,
                    "context_description": f"Skill: {extract_res['skill_name']}"
                })
                
                if mutation_res["status"] == "success":
                    refined_code = mutation_res["refined_code"]
                    with open(skill_path, "w") as f:
                        f.write(refined_code)
                    print(f"    [✨] Neural Refinement complete for {extract_res['skill_name']}")

                # 4. REGISTER
                if self.core.register_skill(skill_path):
                    harvested_count += 1
                    print(f"[✓] Harvested and Registered: {extract_res['skill_name']}")
        
        # Final evolution cycle update
        self.core.run_evolution_cycle()
        
        return {
            "status": "success",
            "total_harvested": harvested_count,
            "registry_size": len(self.core.registry["skills"])
        }

if __name__ == "__main__":
    mcp = HarvesterMCP()
    # Harvest from the hermuxclaw directory itself to start
    result = mcp.run(os.path.expanduser("~/hermuxclaw"))
    print("\n" + "="*50)
    print("HARVEST SUMMARY")
    print("="*50)
    print(json.dumps(result, indent=2))
