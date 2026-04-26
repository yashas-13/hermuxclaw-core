import logging
import os
import json
from datetime import datetime

class HermuxclawLogger:
    """
    Standardized Disciplined Logger.
    Produces machine-parsable JSON logs for the Self-Healing Engine.
    """
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        log_path = os.path.expanduser("~/hermuxclaw/storage/system.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        # File Handler
        fh = logging.FileHandler(log_path)
        self.logger.addHandler(fh)

    def _log_json(self, level, msg, context=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "component": self.logger.name,
            "message": msg,
            "context": context or {}
        }
        self.logger.info(json.dumps(entry))

    def info(self, msg, context=None):
        self._log_json("INFO", msg, context)

    def error(self, msg, error_type, traceback=None, context=None):
        ctx = context or {}
        ctx.update({"error_type": error_type, "traceback": traceback})
        self._log_json("ERROR", msg, ctx)

# Global logging utility
def get_logger(name):
    return HermuxclawLogger(name)
