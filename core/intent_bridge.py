import os
import sys
import subprocess
import json
import time

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.scheduler import scheduler

class AndroidIntentBridge:
    """
    Hardware-level peripheral for HermuXclaw-CORE.
    Connects Android system events (Battery, SMS, Location) to the Agent's trigger system.
    """
    def __init__(self):
        self.workspace = os.path.expanduser("~/hermuxclaw")

    def monitor_battery(self):
        """Monitors battery status to influence Energy Engine decisions."""
        try:
            res = subprocess.check_output(["termux-battery-status"]).decode()
            data = json.loads(res)
            # If battery is low, schedule a GRACEFUL_DEGRADATION task
            if data.get("percentage", 100) < 15 and data.get("status") != "CHARGING":
                scheduler.add_task("GOVERN_RESOURCES", priority=30, data={"reason": "Low Battery"})
            return data
        except:
            return None

    def listen_for_sms(self):
        """Scans for new SMS commands (if permission granted)."""
        try:
            # Note: Requires 'termux-api' and SMS permissions
            res = subprocess.check_output(["termux-sms-list", "-l", "1"]).decode()
            messages = json.loads(res)
            if messages:
                msg = messages[0]
                body = msg.get("body", "").lower()
                if "hx evolve" in body:
                    scheduler.add_task("TRIGGER_EVOLUTION", priority=25)
        except:
            pass

    def run_bridge_cycle(self):
        while True:
            self.monitor_battery()
            self.listen_for_sms()
            time.sleep(30) # High-efficiency polling

if __name__ == "__main__":
    bridge = AndroidIntentBridge()
    print("[*] Android Intent Bridge Active.")
    bridge.run_bridge_cycle()
