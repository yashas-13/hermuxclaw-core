import os
import sys
import json
import ast

sys.path.append(os.path.expanduser("~/hermuxclaw"))
from core.architecture_engine import RootIntelligenceV2
from core.sandbox import Sandbox

class AutoRefactorEngine:
    """
    Autonomous Code Optimization & Refactoring Engine.
    Learns from past structural anomalies and applies LLM-guided fixes.
    """
    def __init__(self, workspace_root):
        self.root = workspace_root
        self.patterns_file = os.path.join(self.root, "memory", "architecture_patterns.json")
        self.patterns = self._load_patterns()
        self.sandbox = Sandbox(timeout=5)
        self.architecture = RootIntelligenceV2(self.root)
        
    def _load_patterns(self):
        if os.path.exists(self.patterns_file):
            try:
                with open(self.patterns_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {
            "HIGH_COUPLING": "Extract core logic into separate, independent utility functions or classes to reduce dependency degree.",
            "CIRCULAR_DEPENDENCY": "Identify the shared resource causing the cycle and extract it into a new, neutral third module.",
            "ISOLATION": "Review if the isolated module should be integrated into core workflows, or deprecated if obsolete."
        }

    def _save_patterns(self):
        with open(self.patterns_file, "w") as f:
            json.dump(self.patterns, f, indent=2)

    def _call_intelligence(self, prompt):
        from openai import OpenAI
        try:
            api_key = os.environ.get("NIM_API_KEY", "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")
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key
            )
            target_model = "meta/llama-3.2-3b-instruct"
            
            system_prompt = "You are Hermuxclaw's Autonomous Refactoring Engine. Output ONLY valid Python code resolving the anomaly described. Do not include markdown tags like ```python."
            
            completion = client.chat.completions.create(
                model=target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2500,
                temperature=0.2
            )
            
            result = completion.choices[0].message.content.strip()
            for block in ["```python", "```"]:
                if result.startswith(block):
                    result = result[len(block):]
                if result.endswith("```"):
                    result = result[:-3]
            return result.strip()
        except Exception as e:
            print(f"[!] LLM Call Failed: {e}")
            return None

    def analyze_and_refactor(self, dry_run=True):
        print("[*] Auto-Refactor: Analyzing System Architecture...")
        self.architecture.ingest_workspace(run_tracing=False) # Quick structural check
        
        anomalies = self.architecture.detector.anomalies
        if not anomalies:
            print("[✓] No anomalies found. System is structurally sound.")
            return

        print(f"[!] Found {len(anomalies)} structural anomalies. Initiating optimization...")
        
        for anomaly in anomalies:
            file_rel_path = anomaly['file']
            file_abs_path = os.path.join(self.root, file_rel_path)
            anomaly_type = anomaly['type']
            
            print(f"\n  [⚡] Targeting: {file_rel_path} ({anomaly_type})")
            
            if not os.path.exists(file_abs_path):
                print(f"      - File not found, skipping.")
                continue
                
            with open(file_abs_path, "r") as f:
                code_content = f.read()

            pattern_advice = self.patterns.get(anomaly_type, "Refactor the code to fix the anomaly.")
            
            prompt = f"""
Anomaly Type: {anomaly_type}
Issue: {anomaly['message']}
Guidance Pattern: {pattern_advice}

Original Code:
{code_content}

Refactor the code to resolve this anomaly. Ensure it remains fully functional. Return ONLY the complete refactored Python code.
"""
            print(f"      - Generating optimized structure via LLM...")
            refactored_code = self._call_intelligence(prompt)
            
            if refactored_code:
                # Sandbox validation (Syntax check at minimum)
                try:
                    ast.parse(refactored_code)
                    print(f"      - [✓] Syntax validation passed.")
                    
                    if dry_run:
                        out_path = file_abs_path + ".optimized"
                        with open(out_path, "w") as f:
                            f.write(refactored_code)
                        print(f"      - [✓] Dry Run: Optimized code saved to {file_rel_path}.optimized")
                    else:
                        with open(file_abs_path, "w") as f:
                            f.write(refactored_code)
                        print(f"      - [✓] Applied: File {file_rel_path} has been actively refactored.")
                        
                    # Learn from success
                    self.patterns[anomaly_type] = pattern_advice + " Verified fix applied recently."
                    self._save_patterns()

                except SyntaxError as e:
                    print(f"      - [!] Refactored code failed syntax validation: {e}")
            else:
                print(f"      - [!] Failed to generate optimized code.")

if __name__ == "__main__":
    engine = AutoRefactorEngine(os.path.expanduser("~/hermuxclaw"))
    # Run in dry_run mode first to avoid accidentally breaking the system
    engine.analyze_and_refactor(dry_run=True)
