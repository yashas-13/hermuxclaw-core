import os
import json
import random
import sys
from datetime import datetime

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.sandbox import Sandbox
from core.evolution_engine import HermuxclawCore
from core.ast_mutator import ast_mutate

class GeneticEngine:
    """
    LLM-Guided & AST-Safe Genetic Evolution Engine.
    Handles the population of skills: Selection, Crossover, Mutation, Fitness Evaluation, Survival.
    """
    def __init__(self, max_population=50):
        self.pop_file = os.path.expanduser("~/hermuxclaw/memory/population.json")
        self.max_population = max_population
        self.sandbox = Sandbox(timeout=3)
        self.core = HermuxclawCore() # For accessing neural_mutator
        self.population = self._load_population()

    def _load_population(self):
        if os.path.exists(self.pop_file):
            try:
                with open(self.pop_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def _save_population(self):
        # Enforce max population
        self.population = sorted(self.population, key=lambda x: x.get("fitness", 0), reverse=True)[:self.max_population]
        with open(self.pop_file, "w") as f:
            json.dump(self.population, f, indent=2)

    def add_to_population(self, name, code, fitness=0.5, generation=0, parents=None):
        genome = {
            "id": f"{name}_g{generation}_{random.randint(1000, 9999)}",
            "name": name,
            "code": code,
            "fitness": fitness,
            "generation": generation,
            "parents": parents or [],
            "added_at": datetime.now().isoformat()
        }
        self.population.append(genome)
        self._save_population()
        return genome

    def crossover(self, genome_a, genome_b):
        """
        Intelligent crossover via Neural Mutator.
        """
        prompt_context = f"Crossover {genome_a['name']} and {genome_b['name']}"
        raw_code = f"# PARENT A\\n{genome_a['code']}\\n\\n# PARENT B\\n{genome_b['code']}"
        
        mutation_res = self.core.execute_skill("neural_mutator", {
            "raw_code": raw_code,
            "context_description": prompt_context
        })
        
        if mutation_res.get("status") == "success":
            return mutation_res.get("refined_code", "")
        else:
            # Fallback simple crossover
            a_lines = genome_a["code"].split("\\n")
            b_lines = genome_b["code"].split("\\n")
            return "\\n".join(a_lines[:len(a_lines)//2] + b_lines[len(b_lines)//2:])

    def mutate(self, code):
        """
        Applies either AST-safe exploratory mutation or LLM structural mutation.
        """
        if random.random() < 0.6: # 60% chance for AST-safe mutation
            print("    [⚡] Applying AST-Safe Mutation...")
            mutated_code, changes = ast_mutate(code, mutation_rate=0.2)
            if changes:
                for c in changes:
                    print(f"      - {c}")
            return mutated_code
        else: # 40% chance for Neural LLM structural mutation
            print("    [🧠] Applying Neural Mutation...")
            prompt_context = "Mutate and optimize this skill."
            mutation_res = self.core.execute_skill("neural_mutator", {
                "raw_code": code,
                "context_description": prompt_context
            })
            if mutation_res.get("status") == "success":
                return mutation_res.get("refined_code", code)
            return code

    def evaluate_fitness(self, code):
        """
        Test the code in the sandbox and calculate a fitness score.
        """
        # Test input
        test_input = {"data": "test_string", "val": 42}
        result = self.sandbox.execute(code, input_data=test_input)
        
        score = 0.0
        if result.get("status") == "success":
            score += 0.5
            output = result.get("result")
            if output:
                score += 0.2
            if isinstance(output, (list, dict)):
                score += 0.2
            if len(str(output)) > 20:
                score += 0.1
        else:
            # Error executing
            score = 0.0
            
        return min(score, 1.0)

    def evolve_cycle(self, generations=1):
        """
        Run the genetic evolution loop.
        """
        if len(self.population) < 2:
            print("[GENETIC ENGINE] Not enough population to evolve. Need at least 2.")
            return

        print(f"\n[🧬 EVOLUTION] Starting {generations} generation(s)...")
        
        for gen in range(generations):
            # Selection: Top 10
            parents = sorted(self.population, key=lambda x: x.get("fitness", 0), reverse=True)[:10]
            new_children = []
            
            # Create offspring
            for i in range(len(parents) - 1):
                p1 = parents[i]
                p2 = parents[i+1]
                
                print(f"  [🔀] Crossing over: {p1['name']} + {p2['name']}")
                child_code = self.crossover(p1, p2)
                
                print(f"  [⚡] Mutating child...")
                child_code = self.mutate(child_code)
                
                print(f"  [🧪] Evaluating fitness...")
                fitness = self.evaluate_fitness(child_code)
                
                child_name = f"evo_{p1['name'][:4]}_{p2['name'][:4]}"
                child_gen = max(p1.get("generation", 0), p2.get("generation", 0)) + 1
                
                new_children.append({
                    "name": child_name,
                    "code": child_code,
                    "fitness": fitness,
                    "generation": child_gen,
                    "parents": [p1["id"], p2["id"]]
                })
                print(f"  [✓] Child {child_name} evaluated. Fitness: {fitness:.2f}")

            # Integrate new children into population
            for child in new_children:
                self.add_to_population(
                    child["name"], 
                    child["code"], 
                    child["fitness"], 
                    child["generation"], 
                    child["parents"]
                )
                
        print(f"[🧬 EVOLUTION] Complete. Population size: {len(self.population)}")

if __name__ == "__main__":
    engine = GeneticEngine()
    # Seed with dummies if empty
    if len(engine.population) == 0:
        code1 = "def run(data):\n    return data.get('val', 0) * 2"
        code2 = "def run(data):\n    return f\"Processed {data.get('data', '')}\""
        engine.add_to_population("seed_multiplier", code1, fitness=0.7)
        engine.add_to_population("seed_stringer", code2, fitness=0.8)
    
    engine.evolve_cycle(generations=1)
