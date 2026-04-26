
import os
import json
import importlib.util
from datetime import datetime

META = {
    "name": "load_providers",
    "version": "harvested-1.1",
    "description": "Auto-harvested from config.py",
    "inputs": ["cls"],
    "outputs": ["result"]
}

def load_providers(cls):
    """Loads provider configuration from providers.json (checks local and package paths)"""
    try:
        # Order of preference: 
        # 1. Local providers.json in CWD
        # 2. .hacx_providers.json in home folder
        # 3. Bundled providers.json in package
        
        paths_to_check = [
            os.path.join(os.getcwd(), 'providers.json'),
            os.path.join(os.path.expanduser("~"), '.hacx_providers.json'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'providers.json')
        ]
        
        json_path = None
        for path in paths_to_check:
            if os.path.exists(path):
                json_path = path
                break
        
        if json_path:
            with open(json_path, 'r') as f:
                cls.PROVIDERS = json.load(f)
        else:
            # Critical Fallback
            cls.PROVIDERS = {
                "hacxgpt": {
                    "base_url": "https://api.hacxgpt.com/v1",
                    "key_var": "HACXGPT_API_KEY",
                    "models": [{"name": "hacxgpt-lightning-flash", "alias": "Lightning Flash"}],
                    "default_model": "hacxgpt-lightning-flash"
                }
            }
    except Exception as e:
        print(f"Warning: Could not load providers.json: {e}")
@classmethod


def run(input_data):
    # Auto-generated wrapper
    try:
        # Map input_data to function args
        kwargs = {k: input_data.get(k) for k in META["inputs"] if k in input_data}
        # Note: If it was a method, this execution might fail without 'self' context.
        # This is a known limitation of the initial extraction phase.
        res = load_providers(**kwargs)
        return {"status": "success", "result": res}
    except Exception as e:
        return {"status": "error", "message": str(e)}
