"""
Fault injection taxonomy: 8 types × 3 severity × 3 timing.

Reference:
- design/fault_injection.md
- StructOPE paper, Section 8.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class FaultType(str, Enum):
    AGENT_DROPOUT = "agent_dropout"
    CAPABILITY_DEGRADATION = "capability_degradation"
    AGENT_REPLACEMENT = "agent_replacement"
    TEAM_SIZE_CHANGE = "team_size_change"
    PACKET_LOSS = "packet_loss"
    COMMUNICATION_DELAY = "communication_delay"
    NETWORK_PARTITION = "network_partition"
    TOPOLOGY_CHANGE = "topology_change"


class Severity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Timing(str, Enum):
    BEFORE = "before"
    DURING = "during"
    BETWEEN = "between"


@dataclass(frozen=True)
class FaultConfig:
    fault_type: FaultType
    severity: Severity
    timing: Timing

    def as_cell(self) -> str:
        return f"{self.fault_type.value}__{self.severity.value}__{self.timing.value}"


def inject_fault(
    env: Any,
    config: FaultConfig,
    rng: Any = None,
) -> Any:
    """
    Apply a fault to the environment according to the config.

    This is a stub; the concrete implementation depends on the HeMAC adapter.
    In the protocol, fault injection is deterministic under a fixed seed.

    Args:
        env: environment instance (HeMAC or Mock adapter)
        config: FaultConfig
        rng: numpy random generator (for determinism)

    Returns:
        the environment, possibly modified
    """
    if not hasattr(env, "apply_fault"):
        raise NotImplementedError(
            "env must implement .apply_fault(config, rng). "
            "See design/fault_injection.md."
        )
    return env.apply_fault(config, rng)


def all_cells() -> list[FaultConfig]:
    """Return the 24 fault cells (8 types × 3 severity)."""
    return [
        FaultConfig(ft, sev, Timing.BEFORE)
        for ft in FaultType
        for sev in Severity
    ]
