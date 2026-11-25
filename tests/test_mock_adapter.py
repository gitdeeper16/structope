"""
Tests for MockAdapter.

MockAdapter is a minimal synthetic environment. These tests verify:

    - conformance to EnvironmentInterface,
    - deterministic reset by seed,
    - correct step semantics (full team advance),
    - joint-state consistency with per-agent observation,
    - structural-shift in-place application,
    - clone_with_seed reproducibility.

MockAdapter is NOT HeMAC. Results from these tests do not
constitute evidence about OPE validity or about HeMAC behavior.
"""

import unittest

import numpy as np

from src.envs.interfaces import (
    Action,
    EnvironmentInterface,
    SeedState,
    StructuralConfig,
    validate_actions,
    validate_joint_state,
)
from src.envs.mock_adapter import MockAdapter


def make_actions(env, vx=0.5, vy=0.0, recharge=0.0):
    actions = {}
    for agent in env.agents:
        if not agent.is_active:
            continue
        actions[agent.agent_id] = Action(
            agent_id=agent.agent_id,
            vector=np.array([vx, vy, recharge], dtype=float),
        )
    return actions


class TestMockAdapterConformance(unittest.TestCase):

    def test_is_environment_interface(self):
        env = MockAdapter(seed=0)
        self.assertIsInstance(env, EnvironmentInterface)

    def test_agents(self):
        env = MockAdapter(seed=0)
        self.assertEqual(len(env.agents), 2)
        self.assertEqual(
            {a.agent_id for a in env.agents},
            {"drone_0", "drone_1"},
        )

    def test_teams(self):
        env = MockAdapter(seed=0)
        self.assertEqual(env.teams, ("drones",))

    def test_structural_config_default(self):
        env = MockAdapter(seed=0)
        cfg = env.structural_config
        self.assertEqual(cfg.team_composition, "T0")
        self.assertEqual(cfg.communication, "C0")

    def test_seed_state(self):
        env = MockAdapter(seed=42)
        s = env.seed_state
        self.assertEqual(s.seed, 42)
        self.assertIn("42", s.episode_id)


class TestMockAdapterReset(unittest.TestCase):

    def test_reset_returns_observations(self):
        env = MockAdapter(seed=0)
        res = env.reset()
        self.assertEqual(set(res.observations.keys()),
                         {"drone_0", "drone_1"})

    def test_same_seed_same_initial_state(self):
        a = MockAdapter(seed=123)
        b = MockAdapter(seed=123)
        ra = a.reset()
        rb = b.reset()
        for aid in ra.observations:
            np.testing.assert_array_equal(
                ra.observations[aid].vector,
                rb.observations[aid].vector,
            )

    def test_different_seeds_different_initial_state(self):
        a = MockAdapter(seed=1)
        b = MockAdapter(seed=2)
        ra = a.reset()
        rb = b.reset()
        different = False
        for aid in ra.observations:
            if not np.array_equal(
                ra.observations[aid].vector,
                rb.observations[aid].vector,
            ):
                different = True
                break
        self.assertTrue(different)

    def test_reset_with_new_seed(self):
        env = MockAdapter(seed=0)
        env.reset()
        res = env.reset(seed=999)
        self.assertEqual(env.seed_state.seed, 999)
        self.assertIn("999", env.seed_state.episode_id)
        self.assertEqual(set(res.observations.keys()),
                         {"drone_0", "drone_1"})


class TestMockAdapterStep(unittest.TestCase):

    def test_step_returns_observations(self):
        env = MockAdapter(seed=0)
        env.reset()
        actions = make_actions(env, vx=0.5)
        res = env.step(actions)
        self.assertEqual(set(res.observations.keys()),
                         {"drone_0", "drone_1"})

    def test_step_advances_all_agents(self):
        env = MockAdapter(seed=0)
        env.reset()
        before = {a.agent_id: env.observation(a.agent_id).vector.copy()
                  for a in env.agents if a.is_active}
        actions = make_actions(env, vx=0.5, vy=0.5)
        env.step(actions)
        for aid in before:
            after = env.observation(aid).vector
            # x and y must have changed.
            self.assertNotEqual(before[aid][0], after[0])
            self.assertNotEqual(before[aid][1], after[1])

    def test_step_validates_actions(self):
        env = MockAdapter(seed=0)
        env.reset()
        with self.assertRaises(ValueError):
            env.step({})

    def test_reward_has_local_and_shared(self):
        env = MockAdapter(seed=0)
        env.reset()
        actions = make_actions(env)
        res = env.step(actions)
        self.assertIn("drone_0", res.reward.local)
        self.assertIn("drone_1", res.reward.local)
        self.assertIsInstance(res.reward.shared, float)

    def test_truncation_at_max_cycles(self):
        env = MockAdapter(seed=0, config={"max_cycles": 3})
        env.reset()
        for _ in range(3):
            res = env.step(make_actions(env))
        self.assertTrue(res.truncated)


class TestMockAdapterJointState(unittest.TestCase):

    def test_joint_state_matches_observations(self):
        env = MockAdapter(seed=0)
        env.reset()
        state = env.joint_state()
        validate_joint_state(state, env.agents)
        for aid, obs in state.observations.items():
            direct = env.observation(aid)
            np.testing.assert_array_equal(obs.vector, direct.vector)

    def test_joint_state_has_global_vars(self):
        env = MockAdapter(seed=0)
        env.reset()
        state = env.joint_state()
        self.assertIn("poi_position", state.global_vars)
        self.assertIn("team_composition", state.global_vars)
        self.assertIn("communication", state.global_vars)


class TestMockAdapterStructuralShift(unittest.TestCase):

    def test_t0_to_t1_drops_one_agent(self):
        env = MockAdapter(seed=0)
        env.reset()
        n_before = sum(1 for a in env.agents if a.is_active)
        env.apply_structural_config(
            StructuralConfig(team_composition="T1",
                             communication="C0")
        )
        n_after = sum(1 for a in env.agents if a.is_active)
        self.assertEqual(n_after, n_before - 1)

    def test_t0_to_t2_drops_two_agents(self):
        env = MockAdapter(seed=0, config={"n_drones": 4})
        env.reset()
        env.apply_structural_config(
            StructuralConfig(team_composition="T2",
                             communication="C0")
        )
        n_active = sum(1 for a in env.agents if a.is_active)
        self.assertEqual(n_active, 2)

    def test_unsupported_c_raises(self):
        env = MockAdapter(seed=0)
        env.reset()
        with self.assertRaises(NotImplementedError):
            env.apply_structural_config(
                StructuralConfig(team_composition="T0",
                                 communication="C1")
            )

    def test_unsupported_t_raises(self):
        env = MockAdapter(seed=0)
        env.reset()
        with self.assertRaises(NotImplementedError):
            env.apply_structural_config(
                StructuralConfig(team_composition="T3",
                                 communication="C0")
            )


class TestMockAdapterClone(unittest.TestCase):

    def test_clone_with_seed_same_state(self):
        a = MockAdapter(seed=7)
        ra = a.reset()
        b = a.clone_with_seed(7)
        rb = b.reset()
        for aid in ra.observations:
            np.testing.assert_array_equal(
                ra.observations[aid].vector,
                rb.observations[aid].vector,
            )

    def test_clone_with_different_seed_differs(self):
        a = MockAdapter(seed=7)
        a.reset()
        b = a.clone_with_seed(8)
        b.reset()
        ra = a.observation("drone_0").vector
        rb = b.observation("drone_0").vector
        self.assertFalse(np.array_equal(ra, rb))

    def test_clone_preserves_structural_config(self):
        a = MockAdapter(seed=0)
        a.reset()
        a.apply_structural_config(
            StructuralConfig(team_composition="T1",
                             communication="C0")
        )
        b = a.clone_with_seed(5)
        self.assertEqual(b.structural_config.team_composition, "T1")




class TestMockAdapterStructuralShiftIdempotence(unittest.TestCase):
    """Re-applying a structural configuration must be idempotent."""

    def test_t1_idempotent(self):
        env = MockAdapter(seed=0)
        env.reset()
        cfg = StructuralConfig(team_composition="T1",
                               communication="C0")
        env.apply_structural_config(cfg)
        n1 = sum(1 for a in env.agents if a.is_active)
        env.apply_structural_config(cfg)
        n2 = sum(1 for a in env.agents if a.is_active)
        self.assertEqual(n1, n2)

    def test_t2_idempotent(self):
        env = MockAdapter(seed=0, config={"n_drones": 4})
        env.reset()
        cfg = StructuralConfig(team_composition="T2",
                               communication="C0")
        env.apply_structural_config(cfg)
        n1 = sum(1 for a in env.agents if a.is_active)
        env.apply_structural_config(cfg)
        n2 = sum(1 for a in env.agents if a.is_active)
        self.assertEqual(n1, n2)

    def test_t1_to_t2(self):
        env = MockAdapter(seed=0, config={"n_drones": 4})
        env.reset()
        env.apply_structural_config(
            StructuralConfig(team_composition="T1",
                             communication="C0")
        )
        n1 = sum(1 for a in env.agents if a.is_active)
        env.apply_structural_config(
            StructuralConfig(team_composition="T2",
                             communication="C0")
        )
        n2 = sum(1 for a in env.agents if a.is_active)
        self.assertEqual(n1, n2 + 1)

    def test_t2_to_t0_restores(self):
        env = MockAdapter(seed=0, config={"n_drones": 4})
        env.reset()
        env.apply_structural_config(
            StructuralConfig(team_composition="T2",
                             communication="C0")
        )
        env.apply_structural_config(
            StructuralConfig(team_composition="T0",
                             communication="C0")
        )
        n = sum(1 for a in env.agents if a.is_active)
        self.assertEqual(n, 4)

    def test_t2_requires_three_agents(self):
        env = MockAdapter(seed=0, config={"n_drones": 2})
        env.reset()
        with self.assertRaises(NotImplementedError):
            env.apply_structural_config(
                StructuralConfig(team_composition="T2",
                                 communication="C0")
            )

    def test_reset_preserves_structural(self):
        env = MockAdapter(seed=0, config={"n_drones": 4})
        env.reset()
        env.apply_structural_config(
            StructuralConfig(team_composition="T1",
                             communication="C0")
        )
        n_before = sum(1 for a in env.agents if a.is_active)
        env.reset()
        n_after = sum(1 for a in env.agents if a.is_active)
        self.assertEqual(n_before, n_after)
        self.assertEqual(n_after, 3)

if __name__ == "__main__":
    unittest.main(verbosity=2)
