import os
import sys

class EnergyEngine:
    """
    Resource Manager for Hermuxclaw.
    Enforces compute budgeting to ensure efficiency.
    """
    def __init__(self, max_energy=100):
        self.max_energy = max_energy
        self.current_energy = max_energy

    def consume(self, amount):
        if self.current_energy >= amount:
            self.current_energy -= amount
            return True
        print(f"[!] Insufficient Energy: {self.current_energy}/{amount}")
        return False

    def regenerate(self, amount=5):
        self.current_energy = min(self.max_energy, self.current_energy + amount)

    def get_status(self):
        return f"{self.current_energy}/{self.max_energy}"
