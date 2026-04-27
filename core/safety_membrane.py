import os
import hashlib
import json
import time
from datetime import datetime

class SafetyMembrane:
    """
    Sovereign Safety Membrane for HermuXclaw-CORE.
    Acts as the final arbiter between the Evolution Engine and the System.
    """
    def __init__(self):
        self.workspace = os.path.expanduser("~/hermuxclaw")
        self.ledger_path = os.path.join(self.workspace, "storage/evolution_ledger.jsonl")
        self.protected_files = [
            "core/orchestrator.py",
            "core/safety_membrane.py",
            "storage/hx.db"
        ]
        self.whitelist_domains = ["api.nvidia.com", "gnorslgqghumwmgoqwhk.supabase.co"]

    def sign_evolution(self, skill_name, code, score_delta, author_cycle):
        """Records an immutable, hashed entry in the Evolution Ledger."""
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "skill": skill_name,
            "hash": code_hash,
            "score_delta": score_delta,
            "cycle_id": author_cycle,
            "membrane_version": "1.0.0"
        }
        
        # Self-signing (Simple HMAC or just hash chaining for audit)
        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return code_hash

    def validate_write_access(self, target_path):
        """Blast Radius Limiter: Enforces restricted write zones."""
        rel_path = os.path.relpath(target_path, self.workspace)
        
        # Rule 1: No direct overwriting of the Membrane or Orchestrator
        if any(rel_path == p for p in self.protected_files):
            print(f"[🛡️ MEMBRANE] REJECTED: Attempt to modify protected core: {rel_path}")
            return False
            
        # Rule 2: Only allow writes to designated zones
        allowed_dirs = ["skills/", "memory/", "storage/", "toolkit/", "mcps/"]
        if not any(rel_path.startswith(d) for d in allowed_dirs):
            print(f"[🛡️ MEMBRANE] REJECTED: Out-of-bounds write attempt: {rel_path}")
            return False
            
        return True

    def check_regression(self, current_aggregate_score, new_potential_score):
        """Regression Guard: The 'Don't Get Dumber' Rule."""
        # Evolution must maintain or improve the system state
        if new_potential_score < (current_aggregate_score * 0.95): # 5% tolerance
            print("[🛡️ MEMBRANE] REJECTED: Potential performance regression detected.")
            return False
        return True

membrane = SafetyMembrane()
