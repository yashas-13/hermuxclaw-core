import os
import json
import sys

def print_tree(population):
    if not population:
        print("[!] No genetic lineage found. Population empty.")
        return

    print("\n" + "="*60)
    print("🧬 HERMUXCLAW GENETIC LINEAGE TRACKER")
    print("="*60 + "\n")

    # Group by generation
    generations = {}
    for genome in population:
        gen = genome.get("generation", 0)
        if gen not in generations:
            generations[gen] = []
        generations[gen].append(genome)

    max_gen = max(generations.keys()) if generations else 0

    for g in range(max_gen + 1):
        if g not in generations:
            continue
        print(f"▼ GENERATION {g}")
        for genome in sorted(generations[g], key=lambda x: x.get("fitness", 0), reverse=True):
            parents = genome.get("parents", [])
            parent_str = f" <- [{', '.join([p[:12]+'...' for p in parents])}]" if parents else " (Seed)"
            print(f"  ├─ {genome['id'][:12]}... | Score: {genome['fitness']:.2f} | {genome['name']}{parent_str}")
        print("  |")
        
    print(f"\nTotal Active Genomes: {len(population)}")
    print("="*60 + "\n")

if __name__ == "__main__":
    pop_file = os.path.expanduser("~/hermuxclaw/memory/population.json")
    if os.path.exists(pop_file):
        with open(pop_file, "r") as f:
            try:
                pop = json.load(f)
                print_tree(pop)
            except json.JSONDecodeError:
                print("[!] Error reading population.json")
    else:
        print("[!] No population file found.")
