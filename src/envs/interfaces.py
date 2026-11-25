"""
Environment Interface for StructOPE.

This module defines the abstract contract that any environment must
satisfy to be used by StructOPE. It is intentionally independent of
any specific simulator (HeMAC or otherwise). The interface is designed
from StructOPE's research needs, not from any simulator's internal
structure.

Design constraints:

- No simulator-specific type is imported or referenced.
- No assumption is made about the internal representation of state.
- The interface exposes the minimum needed for:
  - policy evaluation (action, reward, termination),
  - joint state construction (per-agent and global),
  - structural shift generation (team composition, communication),
  - reproducibility (seed control, episode reset),
  - logging (reward events, agent events).

Conformance:

- A conforming environment implements every method in
  `EnvironmentInterface` and every attribute in the type
  definitions.
- A conforming environment does not raise on a valid action or
  query.
- A conforming environment does not leak simulator-specific objects
  through the public interface.

This file does not implement any environment. It defines the
contract. Implementations live in separate modules
(`mock_adapter.py`, `hemac_adapter.py`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np


# ---------------------------------------------------------------------
# Type definitions
# ---------------------------------------------------------------------

AgentId = str
"""Stable identifier for an agent (e.g., "drone_0", "observer_1")."""

TeamId = str
"""Identifier for a team (e.g., "drones", "observers")."""


@dataclass(frozen=True)
class AgentSpec:
    """Static specification of one agent.

    Attributes:
        agent_id: stable identifier, unique within the environment.
        team_id: team the agent belongs to.
        capabilities: capability descriptor (e.g., max speed, sensor
            range). Interpreted by StructOPE, not by the interface.
        is_active: whether the agent participates in the episode.
    """

    agent_id: AgentId
    team_id: TeamId
    capabilities: Mapping[str, Any] = field(default_factory=dict)
    is_active: bool = True


@dataclass(frozen=True)
class Observation:
    """Per-agent observation returned by the environment.

    Attributes:
        agent_id: the agent this observation belongs to.
        vector: a flat numeric vector (1-D np.ndarray). The interface
            does not impose a dimensionality; the adapter documents it.
        metadata: optional non-numeric data (e.g., labels, masks).
    """

    agent_id: AgentId
    vector: np.ndarray
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class JointState:
    """Joint state of the team at a given cycle.

    The interface does not prescribe the internal layout. It requires
    that the joint state expose:

        - all active agents' identities,
        - each agent's observation,
        - any global variables the adapter deems part of the state,
        - a timestamp (cycle index or environment time).

    The joint state is produced by the StateBuilder, not by the
    environment directly. The environment is responsible for
    exposing the raw components; the StateBuilder assembles them.
    """

    cycle: int
    observations: Mapping[AgentId, Observation]
    global_vars: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Action:
    """Action for a single agent.

    Attributes:
        agent_id: the agent this action belongs to.
        vector: a flat numeric vector (1-D np.ndarray).
        metadata: optional non-numeric data.
    """

    agent_id: AgentId
    vector: np.ndarray
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Reward:
    """Reward returned by the environment.

    Two reward scopes are exposed:

        - local: per-agent reward (may be empty).
        - shared: team reward (single scalar).

    The interface does not assume that local rewards exist. If they
    do not, `local` is empty and only `shared` is meaningful.
    """

    local: Mapping[AgentId, float] = field(default_factory=dict)
    shared: float = 0.0
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StepResult:
    """Result of a single environment step.

    Attributes:
        observations: per-agent observations after the step.
        reward: reward produced by the step.
        terminated: whether the episode ended (success or failure).
        truncated: whether the episode was cut short (time limit).
        info: optional diagnostic information.
    """

    observations: Mapping[AgentId, Observation]
    reward: Reward
    terminated: bool
    truncated: bool
    info: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResetResult:
    """Result of an environment reset.

    Attributes:
        observations: per-agent observations at the initial cycle.
        info: optional diagnostic information.
    """

    observations: Mapping[AgentId, Observation]
    info: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StructuralConfig:
    """Structural configuration of the environment.

    This is the (T, C) cell descriptor used by StructOPE. It is not
    a simulator-specific configuration. It is the minimal set of
    parameters needed to identify a structural configuration in
    StructOPE's own terms.

    Attributes:
        team_composition: identifier (e.g., "T0", "T1").
        communication: identifier (e.g., "C0", "C1").
        parameters: additional parameters (interpreted by StructOPE).
    """

    team_composition: str
    communication: str
    parameters: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SeedState:
    """Reproducibility state.

    Attributes:
        seed: the seed used to construct the environment.
        episode_id: stable identifier for the episode.
    """

    seed: int
    episode_id: str


# ---------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------

class EnvironmentInterface(ABC):
    """Abstract contract for any environment usable by StructOPE.

    A conforming environment:

        - exposes its agents and teams,
        - exposes per-agent observations and a joint state,
        - accepts per-agent actions and produces a StepResult,
        - reports rewards with an explicit local/shared scope,
        - supports deterministic reset by seed,
        - supports structural configuration (T, C),
        - does not leak simulator-specific objects through the public
          interface.

    The interface does not require a specific observation layout. It
    requires that observations are numeric vectors and that their
    dimensionality is documented by the adapter.

    The interface does not require a specific reward definition. It
    requires that rewards be reported with an explicit scope
    (local/shared) and that missing local rewards are represented as
    an empty mapping, not as zero.
    """

    # -----------------------------------------------------------------
    # Identity and structure
    # -----------------------------------------------------------------

    @property
    @abstractmethod
    def agents(self) -> Sequence[AgentSpec]:
        """Return all agent specifications in the environment."""

    @property
    @abstractmethod
    def teams(self) -> Sequence[TeamId]:
        """Return all team identifiers."""

    @property
    @abstractmethod
    def structural_config(self) -> StructuralConfig:
        """Return the current structural configuration."""

    @property
    @abstractmethod
    def seed_state(self) -> SeedState:
        """Return the current seed state."""

    # -----------------------------------------------------------------
    # Reset and step
    # -----------------------------------------------------------------

    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> ResetResult:
        """Reset the environment.

        If `seed` is provided, the environment must reinitialize all
        internal random generators with that seed. If `seed` is None,
        the environment must reuse the constructor seed.

        The reset must return a complete initial observation set for
        all active agents.
        """

    @abstractmethod
    def step(self, actions: Mapping[AgentId, Action]) -> StepResult:
        """Advance the environment by one cycle.

        The environment must advance all active agents before
        returning. A partial step is not allowed.

        The returned StepResult must include observations for all
        active agents after the cycle.
        """

    # -----------------------------------------------------------------
    # Observation and state
    # -----------------------------------------------------------------

    @abstractmethod
    def observation(self, agent_id: AgentId) -> Observation:
        """Return the current observation for a single agent."""

    @abstractmethod
    def joint_state(self) -> JointState:
        """Return the current joint state.

        The joint state is assembled from the environment's
        components by the adapter. The interface does not require
        that the environment expose a joint state directly.
        """

    # -----------------------------------------------------------------
    # Structural shift
    # -----------------------------------------------------------------

    @abstractmethod
    def apply_structural_config(
        self, config: StructuralConfig
    ) -> None:
        """Apply a structural configuration to the environment.

        This may require re-creating the environment. If the
        environment cannot apply the configuration in-place, it
        must raise NotImplementedError and the caller must create a
        new environment.

        The environment must document which configurations are
        supported in-place and which require re-creation.
        """

    # -----------------------------------------------------------------
    # Space descriptors
    # -----------------------------------------------------------------

    @abstractmethod
    def action_space(self, agent_id: AgentId) -> Any:
        """Return a space descriptor for the agent's action.

        The descriptor must expose `shape` and, where applicable,
        `low` and `high`. The exact type is adapter-dependent but
        must be inspectable without simulator-specific knowledge.
        """

    @abstractmethod
    def observation_space(self, agent_id: AgentId) -> Any:
        """Return a space descriptor for the agent's observation."""

    # -----------------------------------------------------------------
    # Reproducibility helpers
    # -----------------------------------------------------------------

    @abstractmethod
    def clone_with_seed(self, seed: int) -> "EnvironmentInterface":
        """Return a fresh environment constructed with the given seed.

        This is the preferred way to obtain a reproducible
        environment. Reusing an existing environment via reset is
        not guaranteed to be equivalent if the underlying simulator
        does not fully reset internal state.
        """


# ---------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------

def validate_action(
    action: Action,
    agents: Sequence[AgentSpec],
) -> None:
    """Validate one agent action.

    Rejects:
        - unknown agent_id,
        - non-ndarray vector,
        - non-1-D vector,
        - non-numeric dtype,
        - NaN or Inf in the vector.
    """
    known = {a.agent_id for a in agents}

    if action.agent_id not in known:
        raise ValueError(f"Unknown agent_id: {action.agent_id!r}")

    if not isinstance(action.vector, np.ndarray):
        raise ValueError("Action vector must be a numpy.ndarray")

    if action.vector.ndim != 1:
        raise ValueError(
            f"Action vector must be 1-D, got {action.vector.shape}"
        )

    if not np.issubdtype(action.vector.dtype, np.number):
        raise ValueError("Action vector must be numeric")

    if not np.all(np.isfinite(action.vector)):
        raise ValueError("Action vector contains NaN or Inf")


def validate_actions(
    actions: Mapping[AgentId, Action],
    agents: Sequence[AgentSpec],
) -> None:
    """Validate a complete action mapping for active agents.

    Rejects:
        - missing actions for any active agent,
        - unknown agents in the mapping,
        - action.agent_id that does not match its dict key,
        - any per-action violation (via validate_action).
    """
    active = {a.agent_id for a in agents if a.is_active}
    provided = set(actions.keys())

    missing = active - provided
    extra = provided - active

    if missing:
        raise ValueError(f"Missing actions: {sorted(missing)}")

    if extra:
        raise ValueError(f"Unknown agents in actions: {sorted(extra)}")

    for agent_id, action in actions.items():
        if action.agent_id != agent_id:
            raise ValueError(
                f"Action key {agent_id!r} does not match "
                f"action.agent_id {action.agent_id!r}"
            )
        validate_action(action, agents)


def validate_joint_state(
    state: JointState,
    agents: Sequence[AgentSpec],
) -> None:
    """Validate joint-state observations for all active agents.

    Rejects:
        - missing observations for any active agent,
        - unknown agents in the joint state,
        - observation.agent_id that does not match its dict key,
        - non-ndarray, non-1-D, non-numeric, or NaN/Inf observation
          vectors.
    """
    active = {a.agent_id for a in agents if a.is_active}
    provided = set(state.observations.keys())

    missing = active - provided
    extra = provided - active

    if missing:
        raise ValueError(
            f"Joint state missing agents: {sorted(missing)}"
        )

    if extra:
        raise ValueError(
            f"Joint state has unknown agents: {sorted(extra)}"
        )

    for agent_id, observation in state.observations.items():
        if observation.agent_id != agent_id:
            raise ValueError(
                f"Observation key {agent_id!r} does not match "
                f"observation.agent_id {observation.agent_id!r}"
            )

        if not isinstance(observation.vector, np.ndarray):
            raise ValueError(
                f"Observation for {agent_id!r} must be a numpy.ndarray"
            )

        if observation.vector.ndim != 1:
            raise ValueError(
                f"Observation for {agent_id!r} must be 1-D"
            )

        if not np.issubdtype(observation.vector.dtype, np.number):
            raise ValueError(
                f"Observation for {agent_id!r} must be numeric"
            )

        if not np.all(np.isfinite(observation.vector)):
            raise ValueError(
                f"Observation for {agent_id!r} contains NaN or Inf"
            )
