import os
import json
import sys

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.log_manager import get_logger
from core.scheduler import scheduler

class HealthMonitor:
    """
    Disciplined Health Monitor.
    Scans logs for systematic errors and schedules REPAIR tasks.
    """
    def __init__(self):
        self.log_path = os.path.expanduser("~/hermuxclaw/storage/system.log")
        self.logger = get_logger("HealthMonitor")

    def analyze_logs(self):
        if not os.path.exists(self.log_path):
            return

        print("[*] Health Monitor: Scanning for system anomalies...")
        errors_found = []
        
        with open(self.log_path, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("level") == "ERROR":
                        errors_found.append(entry)
                except:
                    continue

        if errors_found:
            # Deduplicate errors by type and message
            unique_errors = {}
            for e in errors_found:
                key = f"{e['component']}_{e['context'].get('error_type')}"
                unique_errors[key] = e

            print(f"  [!] Found {len(unique_errors)} unique error patterns.")
            
            for key, err in unique_errors.items():
                # Zero-waste: Schedule a disciplined repair task
                scheduler.add_task(
                    "REPAIR_PROTOCOL", 
                    priority=20, # High priority for healing
                    data=err
                )
                self.logger.info(f"Scheduled repair for: {key}")
        else:
            print("  [✓] No errors detected in logs.")
