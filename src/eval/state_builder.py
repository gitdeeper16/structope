"""Validated joint-state construction for StructOPE."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.envs.interfaces import JointState, validate_joint_state

if TYPE_CHECKING:
    from src.envs.interfaces import EnvironmentInterface


class StateBuilder:
    """Build and validate a joint state from an environment."""

    def __init__(self, env: "EnvironmentInterface") -> None:
        self._env = env

    def build(self) -> JointState:
        """Retrieve and validate the current joint state."""
        state = self._env.joint_state()
        validate_joint_state(state, self._env.agents)
        return state
