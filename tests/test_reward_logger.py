"""
Tests for RewardLogger.

RewardLogger records reset and step events without merging local
and shared reward scopes. It must not lose a step record when the
next step is logged, and reset() must clear the history.
"""

import unittest

import numpy as np

from src.envs.interfaces import (
    Action,
    Observation,
    ResetResult,
    Reward,
    StepResult,
)
from src.eval.reward_logger import RewardLogger


def make_reset(agent_ids=("drone_0", "drone_1")):
    obs = {
        aid: Observation(
            agent_id=aid,
            vector=np.zeros(5, dtype=float),
        )
        for aid in agent_ids
    }
    return ResetResult(observations=obs, info={"seed": 0})


def make_step(
    local=None,
    shared=0.0,
    terminated=False,
    truncated=False,
    agent_ids=("drone_0", "drone_1"),
):
    if local is None:
        local = {aid: 0.0 for aid in agent_ids}
    obs = {
        aid: Observation(
            agent_id=aid,
            vector=np.ones(5, dtype=float),
        )
        for aid in agent_ids
    }
    return StepResult(
        observations=obs,
        reward=Reward(local=local, shared=shared),
        terminated=terminated,
        truncated=truncated,
        info={"cycle": 1},
    )


class TestRewardLogger(unittest.TestCase):

    def test_log_reset(self):
        logger = RewardLogger()
        logger.log_reset(make_reset())
        events = logger.get_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event"], "reset")

    def test_log_multiple_steps(self):
        logger = RewardLogger()
        logger.log_reset(make_reset())
        logger.log_step(make_step())
        logger.log_step(make_step())
        logger.log_step(make_step())
        events = logger.get_events()
        self.assertEqual(len(events), 4)
        self.assertEqual(events[1]["event"], "step")
        self.assertEqual(events[2]["event"], "step")
        self.assertEqual(events[3]["event"], "step")

    def test_local_and_shared_kept_separate(self):
        logger = RewardLogger()
        local = {"drone_0": 0.1, "drone_1": 0.2}
        shared = 0.15
        logger.log_step(make_step(local=local, shared=shared))
        event = logger.get_events()[0]
        self.assertEqual(event["reward"]["local"], local)
        self.assertEqual(event["reward"]["shared"], shared)
        # Shared must not equal the sum of local rewards.
        self.assertNotEqual(
            event["reward"]["shared"],
            sum(local.values()),
        )

    def test_termination_and_truncation_recorded(self):
        logger = RewardLogger()
        logger.log_step(make_step(terminated=True, truncated=False))
        logger.log_step(make_step(terminated=False, truncated=True))
        events = logger.get_events()
        self.assertTrue(events[0]["terminated"])
        self.assertFalse(events[0]["truncated"])
        self.assertFalse(events[1]["terminated"])
        self.assertTrue(events[1]["truncated"])

    def test_get_events_returns_defensive_copy(self):
        logger = RewardLogger()
        logger.log_step(make_step())
        events = logger.get_events()
        events.append({"event": "tampered"})
        self.assertEqual(len(logger.get_events()), 1)

    def test_no_step_lost_when_logging_next(self):
        logger = RewardLogger()
        for i in range(5):
            logger.log_step(make_step(shared=float(i)))
        events = logger.get_events()
        self.assertEqual(len(events), 5)
        shared_values = [e["reward"]["shared"] for e in events]
        self.assertEqual(shared_values, [0.0, 1.0, 2.0, 3.0, 4.0])

    def test_reset_clears_history(self):
        logger = RewardLogger()
        logger.log_reset(make_reset())
        logger.log_step(make_step())
        self.assertEqual(len(logger.get_events()), 2)
        logger.reset()
        self.assertEqual(logger.get_events(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
