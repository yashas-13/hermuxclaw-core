import subprocess
import os
import sys
import time
import json

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from storage.db import db
from core.log_manager import get_logger

class SwarmController:
    """
    Dynamic Auto-Scaling Controller.
    Spawns additional swarm nodes based on task backlog metrics.
    """
    def __init__(self, backlog_threshold=20, max_nodes=5):
        self.backlog_threshold = backlog_threshold
        self.max_nodes = max_nodes
        self.active_nodes = [] # List of PIDs
        self.base_port = 8100
        self.logger = get_logger("SwarmController")

    def monitor_and_scale(self):
        print("[*] Swarm Controller: Monitoring Hive Workload...")
        
        while True:
            # 1. Check Backlog
            rows = db.query("SELECT COUNT(*) FROM tasks WHERE status='pending'")
            backlog = rows[0][0] if rows else 0
            
            # 2. Check Node Health (remove dead PIDs)
            self.active_nodes = [pid for pid in self.active_nodes if self._is_running(pid)]
            
            print(f"  [Metrics] Backlog: {backlog} | Active Nodes: {len(self.active_nodes)}")

            # 3. Decision Logic: Scale Up
            if backlog > self.backlog_threshold and len(self.active_nodes) < self.max_nodes:
                self._spawn_node()
                
            # 4. Decision Logic: Scale Down (optional, if backlog is 0 for X cycles)
            
            time.sleep(10) # Monitor every 10s

    def _spawn_node(self):
        port = self.base_port + len(self.active_nodes)
        print(f"  [🚀] WORKLOAD HIGH: Spawning new worker node on port {port}...")
        
        # Spawn swarm_node.py as a detached process
        log_file = os.path.expanduser(f"~/hermuxclaw/storage/node_{port}.log")
        with open(log_file, "w") as f:
            proc = subprocess.Popen(
                [sys.executable, os.path.expanduser("~/hermuxclaw/core/swarm_node.py")],
                stdout=f,
                stderr=f,
                start_new_session=True # Detach
            )
        
        self.active_nodes.append(proc.pid)
        self.logger.info(f"Scaled up: Node spawned at port {port}", context={"pid": proc.pid})

    def _is_running(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

if __name__ == "__main__":
    controller = SwarmController()
    controller.monitor_and_scale()
