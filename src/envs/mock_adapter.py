"""
Mock environment adapter for StructOPE.

This adapter implements the EnvironmentInterface with a minimal,
fully deterministic synthetic environment. It exists to:

    - validate the interface contract,
    - allow StructOPE's pipeline (StateBuilder, RewardLogger,
      evaluation code) to be tested end-to-end,
    - provide a reproducible testbed for structural-shift logic.

It is NOT a substitute for HeMAC. Results produced with this adapter
are labeled `mock` and are not used in Pilot Characterization or
Confirmatory Evaluation.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Dict, List, Mapping, Optional, Sequence

import numpy as np

from .interfaces import (
    Action,
    AgentId,
    AgentSpec,
    EnvironmentInterface,
    JointState,
    Observation,
    ResetResult,
    Reward,
    SeedState,
    StepResult,
    StructuralConfig,
    TeamId,
    validate_actions,
    validate_joint_state,
)


DEFAULT_CONFIG: Dict[str, Any] = {
    "n_drones": 2,
    "area_size": (100.0, 100.0),
    "max_speed": 1.0,
    "max_cycles": 50,
    "poi_position": None,
    "reward_scale": 0.01,
}


class MockAdapter(EnvironmentInterface):
    """Minimal synthetic environment conforming to
    EnvironmentInterface."""

    def __init__(self, config: Optional[Mapping[str, Any]] = None,
                 seed: int = 0):
        self._config = dict(DEFAULT_CONFIG)
        if config:
            self._config.update(dict(config))

        self._seed = int(seed)
        self._episode_id = f"mock-{seed}"

        self._structural = StructuralConfig(
            team_composition="T0",
            communication="C0",
        )

        self._rng = np.random.default_rng(self._seed)
        self._cycle = 0
        self._terminated = False
        self._truncated = False

        self._agents: List[AgentSpec] = []
        self._positions: Dict[AgentId, np.ndarray] = {}
        self._charges: Dict[AgentId, float] = {}
        self._poi_position: np.ndarray = np.zeros(2)

        self._init_agents()
        self._init_poi()

    def _init_agents(self) -> None:
        n = int(self._config["n_drones"])
        self._agents = []
        self._positions = {}
        self._charges = {}
        for i in range(n):
            agent_id = f"drone_{i}"
            spec = AgentSpec(
                agent_id=agent_id,
                team_id="drones",
                capabilities={
                    "max_speed": float(self._config["max_speed"]),
                },
                is_active=True,
            )
            self._agents.append(spec)
            self._positions[agent_id] = self._rng.uniform(
                low=0.0,
                high=float(self._config["area_size"][0]),
                size=2,
            )
            self._charges[agent_id] = 100.0

    def _init_poi(self) -> None:
        poi = self._config.get("poi_position")
        if poi is None:
            self._poi_position = self._rng.uniform(
                low=0.0,
                high=float(self._config["area_size"][1]),
                size=2,
            )
        else:
            self._poi_position = np.asarray(poi, dtype=float)

    @property
    def agents(self) -> Sequence[AgentSpec]:
        return tuple(self._agents)

    @property
    def teams(self) -> Sequence[TeamId]:
        return ("drones",)

    @property
    def structural_config(self) -> StructuralConfig:
        return self._structural

    @property
    def seed_state(self) -> SeedState:
        return SeedState(seed=self._seed, episode_id=self._episode_id)

    def reset(self, seed: Optional[int] = None) -> ResetResult:
        if seed is not None:
            self._seed = int(seed)
            self._rng = np.random.default_rng(self._seed)
            self._episode_id = f"mock-{self._seed}"

        self._cycle = 0
        self._terminated = False
        self._truncated = False

        self._init_agents()
        self._init_poi()

        # Re-apply the current structural configuration so that
        # reset() does not silently re-activate deactivated agents.
        self._apply_structural_to_agents(
            self._structural.team_composition
        )

        obs = self._build_observations()
        return ResetResult(observations=obs, info={})

    def step(
        self, actions: Mapping[AgentId, Action]
    ) -> StepResult:
        validate_actions(actions, self._agents)

        max_speed = float(self._config["max_speed"])
        area = float(self._config["area_size"][0])

        for agent_id, action in actions.items():
            v = np.asarray(action.vector, dtype=float)
            vx = float(np.clip(v[0], -max_speed, max_speed))
            vy = float(np.clip(v[1], -max_speed, max_speed))
            recharge = float(v[2]) if v.shape[0] > 2 else 0.0

            pos = self._positions[agent_id] + np.array([vx, vy])
            pos = np.clip(pos, 0.0, area)
            self._positions[agent_id] = pos

            # Energy model: C_{t+1} = clip(C_t + 0.1*r - 0.01*v, 0, 100)
            # where v = speed magnitude. Consumed energy is
            # |change in C|, recorded by the logger via observations.
            speed_mag = float(np.hypot(vx, vy))
            self._charges[agent_id] = float(
                np.clip(
                    self._charges[agent_id]
                    + recharge * 0.1
                    - 0.01 * speed_mag,
                    0.0,
                    100.0,
                )
            )

        self._cycle += 1

        if self._cycle >= int(self._config["max_cycles"]):
            self._truncated = True

        reward = self._compute_reward()
        obs = self._build_observations()
        return StepResult(
            observations=obs,
            reward=reward,
            terminated=self._terminated,
            truncated=self._truncated,
            info={"cycle": self._cycle},
        )

    def observation(self, agent_id: AgentId) -> Observation:
        if agent_id not in self._positions:
            raise KeyError(f"Unknown agent: {agent_id!r}")
        pos = self._positions[agent_id]
        poi = self._poi_position
        vec = np.array(
            [
                float(pos[0]),
                float(pos[1]),
                float(poi[0] - pos[0]),
                float(poi[1] - pos[1]),
                float(self._charges[agent_id]),
            ],
            dtype=float,
        )
        return Observation(
            agent_id=agent_id,
            vector=vec,
            metadata={"cycle": self._cycle},
        )

    def joint_state(self) -> JointState:
        obs = self._build_observations()
        state = JointState(
            cycle=self._cycle,
            observations=obs,
            global_vars={
                "poi_position": self._poi_position.copy(),
                "team_composition": self._structural.team_composition,
                "communication": self._structural.communication,
            },
        )
        validate_joint_state(state, self._agents)
        return state

    def apply_structural_config(
        self, config: StructuralConfig
    ) -> None:
        """Apply a structural configuration.

        T0, T1, T2 are absolute configurations, not operations.

            T0: all n agents active.
            T1: n - 1 agents active.
            T2: n - 2 agents active (requires n >= 3).

        Re-applying the same configuration is idempotent: it does
        not drop an additional agent.

        C0 is the only communication level supported by the mock.
        """
        supported_T = {"T0", "T1", "T2"}
        supported_C = {"C0"}

        if config.team_composition not in supported_T:
            raise NotImplementedError(
                f"MockAdapter does not support "
                f"team_composition={config.team_composition!r}"
            )
        if config.communication not in supported_C:
            raise NotImplementedError(
                f"MockAdapter does not support "
                f"communication={config.communication!r}"
            )

        n = int(self._config["n_drones"])
        if config.team_composition == "T1" and n < 2:
            raise NotImplementedError(
                "MockAdapter T1 requires at least 2 agents"
            )
        if config.team_composition == "T2" and n < 3:
            raise NotImplementedError(
                "MockAdapter T2 requires at least 3 agents"
            )

        self._structural = StructuralConfig(
            team_composition=config.team_composition,
            communication=config.communication,
            parameters=dict(config.parameters),
        )

        self._apply_structural_to_agents(
            config.team_composition
        )

    def _apply_structural_to_agents(
        self, team_composition: str
    ) -> None:
        """Set agent activation according to an absolute
        configuration."""
        n = len(self._agents)
        if team_composition == "T0":
            n_active = n
        elif team_composition == "T1":
            n_active = max(n - 1, 0)
        elif team_composition == "T2":
            n_active = max(n - 2, 0)
        else:
            raise ValueError(
                f"Unknown team_composition: {team_composition!r}"
            )

        new_agents = []
        for i, a in enumerate(self._agents):
            new_agents.append(replace(a, is_active=(i < n_active)))
        self._agents = new_agents

    def action_space(self, agent_id: AgentId) -> Any:
        max_speed = float(self._config["max_speed"])
        return {
            "shape": (3,),
            "low": np.array([-max_speed, -max_speed, -1.0]),
            "high": np.array([max_speed, max_speed, 1.0]),
        }

    def observation_space(self, agent_id: AgentId) -> Any:
        return {"shape": (5,)}

    def clone_with_seed(self, seed: int) -> "MockAdapter":
        new = MockAdapter(config=self._config, seed=seed)
        new._structural = replace(self._structural)
        new._apply_structural_to_agents(
            self._structural.team_composition
        )
        return new

    def _build_observations(self) -> Dict[AgentId, Observation]:
        result: Dict[AgentId, Observation] = {}
        for a in self._agents:
            if a.is_active:
                result[a.agent_id] = self.observation(a.agent_id)
        return result

    def _compute_reward(self) -> Reward:
        active_ids = [a.agent_id for a in self._agents if a.is_active]
        if not active_ids:
            return Reward(local={}, shared=0.0)

        local: Dict[AgentId, float] = {}
        for aid in active_ids:
            dist = float(
                np.linalg.norm(self._positions[aid] - self._poi_position)
            )
            local[aid] = -dist * float(self._config["reward_scale"])

        shared = float(np.mean(list(local.values())))
        return Reward(local=local, shared=shared)
