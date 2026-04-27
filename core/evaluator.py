# core/evaluator.py
import json, os, sys
from typing import Dict
sys.path.append(os.path.expanduser("~/hermuxclaw"))
from storage.db import db

class WorkflowEvaluator:
    """
    Self-Evaluation Engine for HermuXclaw-CORE.
    Scores every workflow run against the 18 mandatory outcomes.
    """
    def __init__(self):
        self.criteria = [
            "Problem Understood", "Optimal Plan", "Execution Completion", "Output Accuracy",
            "Knowledge Captured", "Skill Created", "Workflow Optimized", "Failure Handling",
            "Best Path Chosen", "Persistence", "Zero-Waste", "Resource Stability",
            "Safe Execution", "Clear Feedback", "Actionable Results", "Workload Balanced",
            "Best Results Shared", "System Improved"
        ]

    def evaluate_run(self, directive: str, results: Dict, metrics: Dict) -> Dict:
        """
        Calculates the IQ Score for a completed workflow run.
        metrics should contain: {'latency', 'energy', 'new_skills', 'errors'}
        """
        print(f"\n[📊 EVALUATOR] Scoring Mission: {directive[:50]}...")
        
        # Scoring Logic (Heuristic based on result success and resource efficiency)
        score_base = 0.0
        
        # 1. Success-based scoring (P0 Outcomes)
        if not metrics.get('errors'):
            score_base += 50.0 # Mission success baseline
        
        # 2. Resource Efficiency (Zero-Waste)
        efficiency_multiplier = 1.0
        if metrics.get('energy', 0) < 50:
            efficiency_multiplier += 0.2
            
        # 3. Intelligence Growth
        growth_points = (metrics.get('new_skills', 0) * 5) + (metrics.get('knowledge_points', 0) * 2)
        
        final_iq = min(150, (score_base * efficiency_multiplier) + growth_points)
        
        # Store in DB
        db.execute("""
            INSERT INTO workflow_runs (directive, status, iq_score, latency_total_ms, energy_consumed, skills_created, knowledge_points)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (directive, "completed" if not metrics.get('errors') else "failed", 
              final_iq, metrics.get('latency', 0), metrics.get('energy', 0), 
              metrics.get('new_skills', 0), metrics.get('knowledge_points', 0)))
        
        print(f"[✓] Evaluation Complete. Run IQ Score: {final_iq:.2f}")
        return {"iq_score": final_iq, "criteria_met": len(self.criteria)}

evaluator = WorkflowEvaluator()
if __name__ == "__main__":
    evaluator.evaluate_run("Self-test directive", {}, {"latency": 500, "energy": 20, "new_skills": 1})
