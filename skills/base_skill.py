# skills/base_skill.py
import abc, time, json
from typing import Any, Dict

class BaseSkill(abc.ABC):
    """
    Abstract base class for all HermuXclaw skills.
    Enforces a strict metadata and execution contract.
    """
    META: Dict = {}  # Must be overridden by subclasses

    @abc.abstractmethod
    def run(self, input_data: Dict) -> Dict:
        """Execute the primary logic of the skill."""
        pass

    def validate_meta(self):
        """Ensure the skill provides required metadata for registry integration."""
        required = ["name", "version", "inputs", "outputs", "dependencies"]
        # Claude-inspired optional advanced fields
        # effort: low, medium, high, max
        # context: global, fork (isolated subagent)
        # when_to_use: trigger phrases for autonomous invocation
        for key in required:
            assert key in self.META, f"META missing required field: {key}"

    def benchmark(self, input_data: Dict) -> Dict:
        """Execute logic and measure performance (latency)."""
        start = time.perf_counter()
        try:
            result = self.run(input_data)
            status = "success"
        except Exception as e:
            result = {"error": str(e)}
            status = "failed"
            
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "result": result, 
            "status": status,
            "latency_ms": round(elapsed, 2)
        }
