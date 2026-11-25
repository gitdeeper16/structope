"""
Contract tests for EnvironmentInterface validation helpers.

These tests verify only the abstract contract's validation
functions. They do not instantiate any adapter. Adapter-specific
tests live in separate files.
"""

import unittest

import numpy as np

from src.envs.interfaces import (
    Action,
    AgentSpec,
    JointState,
    Observation,
    validate_action,
    validate_actions,
    validate_joint_state,
)


def make_agents(n=2):
    return [
        AgentSpec(agent_id=f"drone_{i}", team_id="drones",
                  is_active=True)
        for i in range(n)
    ]


def make_action(agent_id, vector=None):
    if vector is None:
        vector = np.zeros(3, dtype=float)
    return Action(agent_id=agent_id, vector=vector)


class TestValidateAction(unittest.TestCase):

    def test_valid_action(self):
        agents = make_agents()
        validate_action(make_action("drone_0"), agents)

    def test_unknown_agent(self):
        agents = make_agents()
        with self.assertRaises(ValueError):
            validate_action(make_action("unknown"), agents)

    def test_non_ndarray(self):
        agents = make_agents()
        with self.assertRaises(ValueError):
            validate_action(
                Action(agent_id="drone_0", vector=[0.0, 0.0, 0.0]),
                agents,
            )

    def test_non_1d(self):
        agents = make_agents()
        with self.assertRaises(ValueError):
            validate_action(
                Action(
                    agent_id="drone_0",
                    vector=np.zeros((2, 3), dtype=float),
                ),
                agents,
            )

    def test_non_numeric(self):
        agents = make_agents()
        with self.assertRaises(ValueError):
            validate_action(
                Action(
                    agent_id="drone_0",
                    vector=np.array(["a", "b", "c"]),
                ),
                agents,
            )

    def test_nan(self):
        agents = make_agents()
        with self.assertRaises(ValueError):
            validate_action(
                Action(
                    agent_id="drone_0",
                    vector=np.array([np.nan, 0.0, 0.0]),
                ),
                agents,
            )

    def test_inf(self):
        agents = make_agents()
        with self.assertRaises(ValueError):
            validate_action(
                Action(
                    agent_id="drone_0",
                    vector=np.array([np.inf, 0.0, 0.0]),
                ),
                agents,
            )


class TestValidateActions(unittest.TestCase):

    def test_valid_actions(self):
        agents = make_agents()
        actions = {
            "drone_0": make_action("drone_0"),
            "drone_1": make_action("drone_1"),
        }
        validate_actions(actions, agents)

    def test_missing(self):
        agents = make_agents()
        actions = {"drone_0": make_action("drone_0")}
        with self.assertRaises(ValueError):
            validate_actions(actions, agents)

    def test_extra(self):
        agents = make_agents()
        actions = {
            "drone_0": make_action("drone_0"),
            "drone_1": make_action("drone_1"),
            "ghost": make_action("ghost"),
        }
        with self.assertRaises(ValueError):
            validate_actions(actions, agents)

    def test_key_mismatch(self):
        agents = make_agents()
        actions = {
            "drone_0": make_action("drone_1"),
            "drone_1": make_action("drone_1"),
        }
        with self.assertRaises(ValueError):
            validate_actions(actions, agents)


class TestValidateJointState(unittest.TestCase):

    def make_state(self, keys):
        obs = {}
        for k in keys:
            obs[k] = Observation(
                agent_id=k,
                vector=np.zeros(5, dtype=float),
            )
        return JointState(
            cycle=0,
            observations=obs,
            global_vars={},
        )

    def test_valid_state(self):
        agents = make_agents()
        state = self.make_state(["drone_0", "drone_1"])
        validate_joint_state(state, agents)

    def test_missing(self):
        agents = make_agents()
        state = self.make_state(["drone_0"])
        with self.assertRaises(ValueError):
            validate_joint_state(state, agents)

    def test_extra(self):
        agents = make_agents()
        state = self.make_state(["drone_0", "drone_1", "ghost"])
        with self.assertRaises(ValueError):
            validate_joint_state(state, agents)

    def test_key_mismatch(self):
        agents = make_agents()
        obs = {
            "drone_0": Observation(
                agent_id="drone_1",
                vector=np.zeros(5, dtype=float),
            ),
            "drone_1": Observation(
                agent_id="drone_1",
                vector=np.zeros(5, dtype=float),
            ),
        }
        state = JointState(cycle=0, observations=obs, global_vars={})
        with self.assertRaises(ValueError):
            validate_joint_state(state, agents)

    def test_non_ndarray_observation(self):
        agents = make_agents()
        obs = {
            "drone_0": Observation(
                agent_id="drone_0",
                vector=[0.0] * 5,
            ),
            "drone_1": Observation(
                agent_id="drone_1",
                vector=np.zeros(5, dtype=float),
            ),
        }
        state = JointState(cycle=0, observations=obs, global_vars={})
        with self.assertRaises(ValueError):
            validate_joint_state(state, agents)

    def test_nan_observation(self):
        agents = make_agents()
        vec = np.zeros(5, dtype=float)
        vec[2] = np.nan
        obs = {
            "drone_0": Observation(agent_id="drone_0", vector=vec),
            "drone_1": Observation(
                agent_id="drone_1",
                vector=np.zeros(5, dtype=float),
            ),
        }
        state = JointState(cycle=0, observations=obs, global_vars={})
        with self.assertRaises(ValueError):
            validate_joint_state(state, agents)


if __name__ == "__main__":
    unittest.main(verbosity=2)
