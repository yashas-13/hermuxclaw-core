import os
import sys
import json
import time
import asyncio
import random
import ast
from datetime import datetime

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.sandbox import Sandbox
from core.ast_mutator import ast_mutate
from core.genetic_engine import GeneticEngine
from core.semantic_indexer import SemanticIndexer

class NanoTaskEngine:
    """
    Hermuxclaw Nano-Task Orchestrator.
    Runs continuously, executing micro-tasks every second to ensure non-stop progression.
    Optimized for high efficiency and low overhead.
    """
    def __init__(self):
        self.workspace = os.path.expanduser("~/hermuxclaw")
        self.genetic = GeneticEngine()
        self.indexer = SemanticIndexer()
        self.sandbox = Sandbox(timeout=1) # Extremely tight timeout for nano-tasks
        self.tasks_completed = 0

    async def run_forever(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚡ Nano-Task Engine Started. Continuous progression active.")
        while True:
            try:
                await self._execute_random_nano_task()
                self.tasks_completed += 1
                
                # Report heartbeat every 100 tasks to avoid log spam
                if self.tasks_completed % 100 == 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚡ Heartbeat: {self.tasks_completed} nano-tasks completed.")
                    
                # Sleep for 1 second to maintain steady, low-impact progression
                await asyncio.sleep(1)
            except Exception as e:
                # Suppress output to prevent log flooding, but keep the loop alive
                await asyncio.sleep(2)

    async def _execute_random_nano_task(self):
        """Picks a fast, lightweight task to push the system forward."""
        tasks = [
            self._nano_mutate,
            self._nano_prune_memory,
            self._nano_index_cleanup,
            self._nano_sandbox_warmup
        ]
        # Weight towards mutation (creation of new variants)
        weights = [0.6, 0.15, 0.15, 0.1]
        task = random.choices(tasks, weights=weights, k=1)[0]
        await task()

    async def _nano_mutate(self):
        """Micro-evolution: Take a random genome, apply a safe AST mutation, and test it."""
        if not self.genetic.population:
            return
            
        genome = random.choice(self.genetic.population)
        if not genome.get("code"):
            return
            
        # Apply 10% AST mutation (very fast, no LLM)
        mutated_code, changes = ast_mutate(genome["code"], mutation_rate=0.1)
        
        if changes and mutated_code != genome["code"]:
            # Fast sandbox evaluation
            result = self.sandbox.execute(mutated_code, {"data": "nano_test"})
            
            if result.get("status") == "success":
                # Only keep if it survives the mutation
                child_name = f"nano_{genome['name'][:6]}"
                self.genetic.add_to_population(
                    name=child_name,
                    code=mutated_code,
                    fitness=genome.get("fitness", 0.5) * 0.95, # Slight penalty for random mutation until verified
                    generation=genome.get("generation", 0) + 1,
                    parents=[genome["id"]]
                )

    async def _nano_prune_memory(self):
        """Micro-cleanup: Ensure population doesn't exceed bounds slightly faster than ecosystem loop."""
        if len(self.genetic.population) > self.genetic.max_population:
            # Sort and slice
            self.genetic.population = sorted(self.genetic.population, key=lambda x: x.get("fitness", 0), reverse=True)[:self.genetic.max_population]
            self.genetic._save_population()

    async def _nano_index_cleanup(self):
        """Micro-maintenance: Remove dead links from semantic index."""
        if not self.indexer.index:
            return
            
        # Check a random entry to see if the file still exists
        random_key = random.choice(list(self.indexer.index.keys()))
        file_path = random_key.split("::")[0]
        if not os.path.exists(file_path):
            del self.indexer.index[random_key]
            self.indexer._save_index()

    async def _nano_sandbox_warmup(self):
        """Micro-validation: Run a baseline test to ensure the sandbox subprocess overhead is cached/warm."""
        self.sandbox.execute("def run(d): return True", {"warmup": True})


def start_daemon():
    engine = NanoTaskEngine()
    try:
        asyncio.run(engine.run_forever())
    except KeyboardInterrupt:
        print("\n[!] Nano-Task Engine stopped.")

if __name__ == "__main__":
    start_daemon()
