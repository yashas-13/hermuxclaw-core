
import os
import json
import importlib.util
from datetime import datetime

META = {
    "name": "set_model",
    "version": "harvested-1.1",
    "description": "Auto-harvested from brain.py",
    "inputs": ["model_name"],
    "outputs": ["result"]
}

def set_model(self, model_name: str):
    """Update the model being used"""
    self.model = model_name
    Config.ACTIVE_MODEL = model_name
    # If switching between HacxGPT and normal models, a reset might be best, 
    # but we'll try to just remove/add the system prompt if the history is fresh.
    if len(self.history) <= 1:
        self.reset()


def run(input_data):
    # Auto-generated wrapper
    try:
        # Map input_data to function args
        kwargs = {k: input_data.get(k) for k in META["inputs"] if k in input_data}
        # Note: If it was a method, this execution might fail without 'self' context.
        # This is a known limitation of the initial extraction phase.
        res = set_model(**kwargs)
        return {"status": "success", "result": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
