# core/evolution_engine.py
import concurrent.futures, logging, copy, os, sys

# Ensure paths are correct for local imports
sys.path.append(os.path.expanduser("~/hermuxclaw"))

from skills.ast_extractor_skill import ASTExtractorSkill
from skills.skill_validator_skill import SkillValidatorSkill
from memory.skill_registry import SkillRegistry

class EvolutionEngine:
    """
    The Sandbox Tournament engine.
    Generates multiple skill variants, benchmarks them in parallel, 
    and crowns the winner based on execution speed and validity.
    """
    def __init__(self):
        self.extractor = ASTExtractorSkill()
        self.validator = SkillValidatorSkill()
        self.registry = SkillRegistry()

    def evolve(self, source_code: str, target_func: str,
               test_input: dict, variants: int = 3) -> dict:
        """Execute the tournament loop for a specific code fragment."""
        
        # 1. Extraction Pass
        extracted = self.extractor.run({
            "source_code": source_code,
            "target_function": target_func
        })
        
        # 2. Variant Generation (Currently clones, expandable to LLM-mutation)
        candidates = [extracted["skill_template"]] * variants
        results = []
        
        # 3. Parallel Benchmarking (The Tournament)
        with concurrent.futures.ThreadPoolExecutor(max_workers=variants) as ex:
            futures = {ex.submit(self._bench, c, test_input): i
                       for i, c in enumerate(candidates)}
            
            for future in concurrent.futures.as_completed(futures):
                idx = futures[future]
                try:
                    r = future.result()
                    r["variant_id"] = idx
                    results.append(r)
                except Exception as e:
                    results.append({
                        "variant_id": idx, "error": str(e),
                        "latency_ms": 9999, "valid": False
                    })
        
        # 4. Selection: The fastest valid variant wins
        valid_results = [r for r in results if r.get("valid")]
        if not valid_results:
            return {"status": "error", "message": "No variants passed validation."}
            
        winner = min(valid_results, key=lambda x: x.get("latency_ms", 9999))
        
        # 5. Registration
        # Note: In production, we'd map the winner to a real file path
        self.registry.register({
            "name": f"evolved_{target_func}",
            "latency_ms": winner["latency_ms"],
            "status": "active"
        })
        
        logging.info(f"🏆 Evolution winner: variant {winner['variant_id']} "
                     f"| {winner['latency_ms']}ms")
                     
        return winner

    def _bench(self, skill_code: str, test_input: dict) -> dict:
        """Internal worker to execute a single candidate in isolation."""
        tmp = os.path.expanduser("~/hermuxclaw/storage/hx_candidate.py")
        os.makedirs(os.path.dirname(tmp), exist_ok=True)
        
        with open(tmp, "w") as f:
            f.write(skill_code)
            
        return self.validator.run({
            "skill_path": tmp, 
            "test_input": test_input
        })

    def run_evolution_cycle(self):
        """Stub for compatibility."""
        logging.info("Evolution cycle triggered manually.")

