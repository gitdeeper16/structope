"""
Tests for StateBuilder.

StateBuilder retrieves and validates a JointState from an
EnvironmentInterface. It does not construct state from scratch.
"""

import unittest

import numpy as np

from src.envs.interfaces import (
    EnvironmentInterface,
    JointState,
    Observation,
    validate_joint_state,
)
from src.envs.mock_adapter import MockAdapter
from src.eval.state_builder import StateBuilder


class TestStateBuilder(unittest.TestCase):

    def test_build_returns_joint_state(self):
        env = MockAdapter(seed=0)
        env.reset()
        builder = StateBuilder(env)
        state = builder.build()
        self.assertIsInstance(state, JointState)

    def test_build_matches_env_joint_state(self):
        env = MockAdapter(seed=0)
        env.reset()
        builder = StateBuilder(env)
        state_built = builder.build()
        state_direct = env.joint_state()
        self.assertEqual(state_built.cycle, state_direct.cycle)
        self.assertEqual(
            set(state_built.observations.keys()),
            set(state_direct.observations.keys()),
        )
        for aid in state_built.observations:
            np.testing.assert_array_equal(
                state_built.observations[aid].vector,
                state_direct.observations[aid].vector,
            )

    def test_build_includes_all_active_agents(self):
        env = MockAdapter(seed=0, config={"n_drones": 4})
        env.reset()
        env.apply_structural_config(
            type(env.structural_config)(
                team_composition="T1",
                communication="C0",
            )
        )
        builder = StateBuilder(env)
        state = builder.build()
        active = {a.agent_id for a in env.agents if a.is_active}
        self.assertEqual(set(state.observations.keys()), active)

    def test_build_after_reset(self):
        env = MockAdapter(seed=0)
        env.reset()
        builder = StateBuilder(env)
        s1 = builder.build()
        env.reset(seed=999)
        s2 = builder.build()
        self.assertEqual(s2.cycle, 0)
        self.assertNotEqual(
            s1.observations["drone_0"].vector.tolist(),
            s2.observations["drone_0"].vector.tolist(),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
