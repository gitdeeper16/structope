"""Episode-level reward and event logging for StructOPE."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

from src.envs.interfaces import ResetResult, StepResult


class RewardLogger:
    """Record reset and step events without merging reward scopes."""

    def __init__(self) -> None:
        self._events: List[Dict[str, Any]] = []

    def log_reset(self, reset_result: ResetResult) -> None:
        """Record the beginning of an episode."""
        self._events.append({
            "event": "reset",
            "observations": deepcopy(dict(reset_result.observations)),
            "info": deepcopy(dict(reset_result.info)),
        })

    def log_step(self, step_result: StepResult) -> None:
        """Record one environment step."""
        reward = step_result.reward

        self._events.append({
            "event": "step",
            "observations": deepcopy(dict(step_result.observations)),
            "reward": {
                "local": dict(reward.local),
                "shared": float(reward.shared),
                "metadata": deepcopy(dict(reward.metadata)),
            },
            "terminated": bool(step_result.terminated),
            "truncated": bool(step_result.truncated),
            "info": deepcopy(dict(step_result.info)),
        })

    def get_events(self) -> List[Dict[str, Any]]:
        """Return a defensive copy of the complete event history."""
        return deepcopy(self._events)

    def reset(self) -> None:
        """Clear the recorded history."""
        self._events.clear()
