import os
import sys
from datetime import datetime

class EnergyEngine:
    """
    Predictive Resource Governor for HermuXclaw-CORE.
    Uses trend analysis to forecast compute capacity.
    """
    def __init__(self, max_energy=100):
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.history = [] # List of (timestamp, value)
        self.trend = 0.0 # Positive = charging/regen, Negative = depleting

    def consume(self, amount):
        if self.current_energy >= amount:
            self.current_energy -= amount
            self._record_history()
            return True
        return False

    def regenerate(self, amount=5):
        self.current_energy = min(self.max_energy, self.current_energy + amount)
        self._record_history()

    def _record_history(self):
        self.history.append((datetime.now(), self.current_energy))
        if len(self.history) > 20: self.history.pop(0)
        self._calculate_trend()

    def _calculate_trend(self):
        if len(self.history) < 5: return
        # Simple linear slope over last 5 points
        start = self.history[-5][1]
        end = self.history[-1][1]
        self.trend = (end - start) / 5.0

    def predict_capacity(self, minutes_ahead=10):
        """Predicts energy level N minutes in the future based on trend."""
        # Assume 1 cycle per minute for simplicity
        prediction = self.current_energy + (self.trend * minutes_ahead)
        return max(0, min(self.max_energy, prediction))

    def get_status(self):
        state = "STABLE"
        if self.trend < -1.0: state = "DEPLETING"
        if self.trend > 0.5: state = "REGENERATING"
        return f"{self.current_energy}/{self.max_energy} [% {state}]"

