# dashboard/server.py
import os
import sys
from flask import Flask, jsonify

# Ensure paths are correct
sys.path.append(os.path.expanduser("~/hermuxclaw"))

from memory.skill_registry import SkillRegistry
from core.config import config

app = Flask(__name__)
registry = SkillRegistry()

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Returns all skills currently in the persistent registry."""
    try:
        skills = registry.get_all()
        return jsonify({"status": "success", "skills": skills})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Returns the current system health and configuration."""
    return jsonify({
        "status": "active",
        "core_version": "1.0.0",
        "port": config.HX_PORT,
        "db_path": config.DB_PATH
    })

def run():
    print(f"[*] Starting HermuXclaw Dashboard API on port {config.HX_PORT}...")
    app.run(host='0.0.0.0', port=config.HX_PORT)

if __name__ == "__main__":
    run()
