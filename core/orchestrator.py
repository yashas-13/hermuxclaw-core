import os
import sys
import time
from datetime import datetime

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.scheduler import scheduler
from core.energy import EnergyEngine
from knowledge.graph_store import graph_store
from root.graph_builder import GraphBuilder
from core.health_monitor import HealthMonitor
from core.repair_protocol import RepairProtocol
from core.log_manager import get_logger

class Orchestrator:
    """
    HX-CORE Autonomous Execution Engine.
    Strictly follows: DISCOVER -> FILTER -> PARSE -> BUILD GRAPH -> SCHEDULE -> EXECUTE -> TRACE -> STORE -> EVALUATE -> EVOLVE
    """
    def __init__(self):
        self.energy = EnergyEngine(max_energy=100)
        self.workspace = os.path.expanduser("~/hermuxclaw")
        self.health_monitor = HealthMonitor()
        self.repair_protocol = RepairProtocol()
        self.logger = get_logger("Orchestrator")

    def run_cycle(self):
        """
        MANDATORY EXECUTION FLOW:
        DISCOVER -> FILTER -> PARSE -> BUILD GRAPH -> SCHEDULE -> EXECUTE -> TRACE -> STORE -> EVALUATE -> EVOLVE
        """
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚙️ HX-CORE: Energy {self.energy.get_status()}")
        
        # 1. REGENERATE (Resource Governance)
        self.energy.regenerate(5)
        
        # 2. DISCOVER & 3. FILTER (Zero-Waste)
        new_files = self._discover_and_filter()
        
        # 4. PARSE & 5. BUILD GRAPH & 6. SCHEDULE
        # (Handled within _discover_and_filter by queuing AST_PARSE tasks)
        
        # 7. EXECUTE (SANDBOX) & 8. TRACE
        task = scheduler.get_next_task()
        if not task:
            return

        if not self.energy.consume(10):
            scheduler.add_task(task['name'], priority=task.get('priority', 1), data=task.get('data'))
            return

        try:
            self._execute_task(task)
            # 9. STORE
            scheduler.complete_task(task["hash"])
            # 10. EVALUATE & EVOLVE
            self.health_monitor.analyze_logs()
        except Exception as e:
            import traceback
            self.logger.error(f"Task failed: {task['name']}", type(e).__name__, traceback.format_exc(), context=task)

    def _discover_and_filter(self):
        """
        DISCOVER: Scan workspace for high-signal sources.
        FILTER: Reject redundant/irrelevant inputs using O(1) content hashing.
        """
        queued = 0
        import hashlib
        
        for root, _, files in os.walk(self.workspace):
            if any(x in root for x in [".git", "__pycache__", "storage", "memory"]): continue
            for f in files:
                if f.endswith(".py"):
                    fpath = os.path.join(root, f)
                    
                    # Deterministic Zero-Waste Filter
                    with open(fpath, "rb") as f_obj:
                        file_hash = hashlib.md5(f_obj.read()).hexdigest()
                    
                    # Check if this specific version has already been indexed
                    existing = db.query("SELECT id FROM files WHERE path=? AND hash=?", (fpath, file_hash))
                    if not existing:
                        # New or modified file: Update DB and queue for structural parsing
                        db.execute("INSERT OR REPLACE INTO files (path, hash) VALUES (?, ?)", (fpath, file_hash))
                        if scheduler.add_task("AST_PARSE", priority=5, data=fpath):
                            queued += 1
        return queued

    def _execute_task(self, task):
        name = task['name']
        data = task.get('data')

        if name == "AST_PARSE":
            fpath = data
            # PARSE (AST) & BUILD GRAPH
            builder = GraphBuilder(fpath)
            builder.build()
            print(f"    [✓] PARSE & GRAPH: Mapped {os.path.basename(fpath)}")

        elif name == "REPAIR_PROTOCOL":
            print(f"    [💊] EXECUTE: Initiating Repair Protocol")
            self.repair_protocol.execute_repair(data)
            
        else:
            print(f"    [?] Unknown Task: {name}")

if __name__ == "__main__":
    hx = Orchestrator()
    while True:
        hx.run_cycle()
        time.sleep(3)
