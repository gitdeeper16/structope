import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import unittest
import numpy as np

from gymnasium.utils import seeding

try:
    from hemac.environment.HeMAC import RawEnv
except ImportError as e:
    raise SystemExit(
        "Cannot import hemac.environment.HeMAC.RawEnv. "
        "Set PYTHONPATH to point to the HeMAC source tree. "
        f"Original error: {e}"
    )


class SeededRawEnv(RawEnv):
    """
    Supplies the seed before HeMAC constructs its internal agents.
    This avoids relying on RawEnv.reset(seed=...), which does not
    propagate the new RNG reference to already-created components.
    """

    def __init__(self, seed, **kwargs):
        self.constructor_seed = seed
        super().__init__(**kwargs)

    def _seed(self, seed=None):
        actual_seed = (
            self.constructor_seed if seed is None else seed
        )
        self.randomizer, _ = seeding.np_random(actual_seed)


CONFIG = {
    "n_drones": 2,
    "n_observers": 0,
    "n_provisioners": 0,
    "area_size": (1000, 1000),
    "max_cycles": 100,
    "render_mode": None,
    "min_obstacles": 0,
    "max_obstacles": 0,
    "rescuing_targets": False,
    "known_goals": False,
    "drone_config": {
        "drone_max_charge": 9999,
        "drone_max_speed": 14,
        "drone_max_thrust": 4,
        "drone_altitude": 30,
        "drone_ui_dimension": 40,
        "drones_starting_pos": [],
        "discrete_action_space": False,
    },
    "poi_config": [
        {
            "dimension": [8, 8],
            "speed": 1.0,
            "variable_speed": False,
            "spawn_mode": "random",
            "draw_expected_position": False,
            "draw_uncertainty": False,
        }
    ],
}

ACTIONS = {
    "drone_0": np.array([1.0, 0.25, -1.0], dtype=np.float32),
    "drone_1": np.array([-0.5, 0.5, -1.0], dtype=np.float32),
}


def object_snapshot(obj, fields):
    result = {}
    for field in fields:
        value = getattr(obj, field, None)
        if value is not None:
            if isinstance(value, (int, float, np.number)):
                result[field] = float(value)
            else:
                result[field] = repr(value)
    return result


def snapshot(raw):
    core = raw.env

    drone_fields = (
        "x", "y", "vx", "vy",
        "accel_x", "accel_y",
        "charge_level", "orientation",
        "carried_targets",
    )

    poi_fields = (
        "x", "y", "orientation", "speed",
    )

    return {
        "drones": [
            object_snapshot(agent, drone_fields)
            for agent in core.agents_list
            if agent.__class__.__name__ == "Drone"
        ],
        "pois": [
            object_snapshot(goal, poi_fields)
            for goal in core.goals
        ],
    }


def run_episode(seed, cycles=10):
    raw = SeededRawEnv(seed=seed, **CONFIG)
    raw.reset()

    trace = [snapshot(raw)]

    for _ in range(cycles):
        # Complete one AEC cycle: one action for every active agent.
        active_agents = list(raw.agents)

        for _ in active_agents:
            agent = raw.agent_selection
            action = ACTIONS[agent]
            raw.step(action)

        # Capture only after the complete team cycle.
        trace.append(snapshot(raw))

    return trace


class TestHeMACReproducibility(unittest.TestCase):

    def test_same_seed_produces_same_trajectory(self):
        seed = 20261124

        first = run_episode(seed)
        second = run_episode(seed)

        self.assertEqual(
            len(first),
            len(second),
            "Trajectory lengths differ",
        )

        for step, (a, b) in enumerate(zip(first, second)):
            self.assertEqual(
                a,
                b,
                f"Reproducibility mismatch at cycle {step}",
            )

    def test_different_seeds_are_not_assumed_identical(self):
        first = run_episode(101)
        second = run_episode(202)

        self.assertNotEqual(
            first[0],
            second[0],
            "Initial states unexpectedly identical; inspect spawn randomness",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
