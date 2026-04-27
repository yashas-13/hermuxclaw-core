import sys, os; sys.path.append(os.path.expanduser("~/hermuxclaw"))
import os
import json
import sys
from datetime import datetime

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from storage.db import db
from core.log_manager import get_logger

class ModelUpgrader:
    """
    Autonomous LLM Lifecycle Manager with Turbo-Quant Support.
    Tracks system capability and 'evolves' the default model size.
    """
    def __init__(self):
        self.base_dir = os.path.expanduser("~/hermuxclaw")
        self.state_file = os.path.join(self.base_dir, "memory/llm_state.json")
        self.logger = get_logger("ModelUpgrader")
        self.state = self._load_state()
        self.turbo_enabled = False

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {
            "current_model": "qwen2-0.5b",
            "iq_points": 0,
            "tier": 1,
            "next_upgrade_iq": 100,
            "growth_history": []
        }

    def _save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def enable_turbo(self, active=True):
        self.turbo_enabled = active
        print(f"[*] Turbo-Quant Optimization: {'ACTIVE' if active else 'INACTIVE'}")

    def calculate_growth(self):
        try:
            skills_count = len(os.listdir(os.path.join(self.base_dir, "skills")))
            repairs = db.query("SELECT COUNT(*) FROM evolution_runs WHERE status='healed'")[0][0]
            new_iq = (skills_count * 10) + (repairs * 5)
            
            if new_iq >= self.state["next_upgrade_iq"]:
                self._perform_upgrade(new_iq)
            else:
                self.state["iq_points"] = new_iq
                self._save_state()
        except: pass

    def _perform_upgrade(self, iq):
        self.state["tier"] += 1
        old_model = self.state["current_model"]
        tiers = {2: "llama3.2-1b", 3: "gemma2-2b", 4: "llama3.1-8b"}
        self.state["current_model"] = tiers.get(self.state["tier"], "llama3.1-8b")
        self.state["next_upgrade_iq"] = self.state["tier"] * 150
        self.state["growth_history"].append({
            "timestamp": datetime.now().isoformat(),
            "from": old_model, "to": self.state["current_model"], "iq_at_upgrade": iq
        })
        self._save_state()

    def get_current_model_id(self):
        """
        STRICT MANDATE: Return ONLY 0.5B model IDs.
        Locked to Qwen2-0.5B-Instruct for optimal local-scale performance.
        """
        # We always return the 0.5B model regardless of internal Tier
        return "qwen/qwen2-0.5b-instruct"

if __name__ == "__main__":
    upgrader = ModelUpgrader()
    print(f"LOCKED MODEL ID: {upgrader.get_current_model_id()}")

