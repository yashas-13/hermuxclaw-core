import os
import time
import signal
import subprocess
import sys

class Watchdog:
    """
    HermuXclaw Dead Man's Switch.
    Monitors heartbeat and manages clean recovery from infinite loops or freezes.
    """
    def __init__(self, target_pid, heartbeat_file, timeout=60):
        self.target_pid = target_pid
        self.heartbeat_file = heartbeat_file
        self.timeout = timeout

    def monitor(self):
        print(f"[*] Watchdog Active: Monitoring PID {self.target_pid}...")
        while True:
            if not self._check_process():
                print("[!] Process vanished. Watchdog shutting down.")
                break
                
            last_heartbeat = self._get_last_heartbeat()
            if time.time() - last_heartbeat > self.timeout:
                print(f"[🚨] DEAD MAN'S SWITCH TRIGGERED: PID {self.target_pid} is unresponsive.")
                self._kill_and_snapshot()
                break
                
            time.sleep(10)

    def _get_last_heartbeat(self):
        if not os.path.exists(self.heartbeat_file):
            return time.time() # Assume just started
        return os.path.getmtime(self.heartbeat_file)

    def _check_process(self):
        try:
            os.kill(self.target_pid, 0)
            return True
        except OSError:
            return False

    def _kill_and_snapshot(self):
        try:
            print(f"[*] Terminating unresponsive process {self.target_pid}...")
            os.kill(self.target_pid, signal.SIGKILL)
            
            # Create recovery marker
            snapshot_path = os.path.expanduser("~/hermuxclaw/storage/crash_snapshot.txt")
            with open(snapshot_path, "w") as f:
                f.write(f"CRASH DETECTED: {time.ctime()}\n")
                f.write(f"Last Heartbeat: {time.ctime(self._get_last_heartbeat())}\n")
            print(f"[✓] Crash snapshot saved to {snapshot_path}. System ready for manual recovery.")
        except Exception as e:
            print(f"[!] Kill failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 watchdog.py <PID> <HEARTBEAT_FILE>")
    else:
        wd = Watchdog(int(sys.argv[1]), sys.argv[2])
        wd.monitor()
