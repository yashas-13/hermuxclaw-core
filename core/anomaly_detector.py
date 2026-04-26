import os
import json

class AnomalyDetector:
    """
    Structural Anomaly Detection for Hermuxclaw.
    Identifies architectural smells and risky code patterns.
    """
    def __init__(self, arch_map):
        self.arch_map = arch_map
        self.anomalies = []

    def detect(self):
        print("[*] Anomaly Detector: Analyzing System Integrity...")
        self._check_high_coupling()
        self._check_isolated_modules()
        self._check_circular_dependencies()
        return self.anomalies

    def _check_high_coupling(self):
        # Threshold: More than 8 dependencies or calls
        for file, data in self.arch_map.items():
            if data['score'] > 10:
                self.anomalies.append({
                    "type": "HIGH_COUPLING",
                    "severity": "medium",
                    "file": file,
                    "message": f"Module acts as a 'God Object' (Complexity: {data['score']})"
                })

    def _check_isolated_modules(self):
        for file, data in self.arch_map.items():
            if data['score'] == 0:
                self.anomalies.append({
                    "type": "ISOLATION",
                    "severity": "low",
                    "file": file,
                    "message": "Module is isolated (dead code or untapped capability)"
                })

    def _check_circular_dependencies(self):
        # Simplified circular detection
        for file, data in self.arch_map.items():
            for target in data['calls']:
                if target in self.arch_map and file in self.arch_map[target]['calls']:
                    self.anomalies.append({
                        "type": "CIRCULAR_DEPENDENCY",
                        "severity": "high",
                        "file": file,
                        "message": f"Direct circular call detected between {file} and {target}"
                    })

    def generate_report(self):
        if not self.anomalies:
            return "[✓] No major anomalies detected. System structure is healthy."
        
        report = ["⚠️ ARCHITECTURAL ANOMALIES DETECTED:"]
        for a in self.anomalies:
            report.append(f"  - [{a['type']}] ({a['severity']}): {a['file']} -> {a['message']}")
        return "\n".join(report)

if __name__ == "__main__":
    # Test with dummy data
    dummy_map = {
        "engine.py": {"score": 15, "calls": ["utils.py"], "layer": "core"},
        "utils.py": {"score": 2, "calls": ["engine.py"], "layer": "utility"}
    }
    detector = AnomalyDetector(dummy_map)
    detector.detect()
    print(detector.generate_report())
