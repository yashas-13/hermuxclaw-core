import sys, os; sys.path.append(os.path.expanduser("~/hermuxclaw"))
# core/brain.py
import json, logging
from typing import List, Dict
from core.config import config

class Brain:
    """
    The High-Level Reasoning Engine.
    Handles goal setting, psychological intent analysis, and self-reflection.
    """
    def __init__(self):
        self.active_goals = []
        self.state_history = []
        self.iq_baseline = 100 # Internal metric for reasoning depth

    def analyze_intent(self, user_input: str) -> Dict:
        """Analyze user behavior and input using psychological heuristics."""
        # This simulates deep cognitive analysis
        analysis = {
            "intent": "solve_problem",
            "urgency": "high" if "ensure" in user_input.lower() or "never stop" in user_input.lower() else "normal",
            "psychology": "directive_assertive",
            "primary_objective": user_input,
            "sub_goals": []
        }
        
        # Self-Reflection loop to increase "Mind" depth
        self.reflect("Does this input require deep system access?")
        return analysis

    def reflect(self, query: str):
        """Self-reflection mechanism to improve reasoning accuracy."""
        logging.info(f"[BRAIN-SOUL] Reflecting: {query}")
        self.state_history.append({"reflection": query, "iq_delta": +1})
        self.iq_baseline += 1

    def set_goals(self, analysis: Dict):
        """Decompose intent into a persistent goal stack."""
        self.active_goals = [analysis["primary_objective"]]
        logging.info(f"[BRAIN] Persistent Goals set: {self.active_goals}")
