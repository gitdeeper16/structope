"""
Tests for the Pipeline Test (Item 1.1).

These tests verify that the StructOPE data flow works end-to-end
on the MockAdapter. They do NOT verify OPE validity, HeMAC
integration, or any scientific claim.
"""

import csv
import unittest
from pathlib import Path

import numpy as np

from experiments.phase1_baseline.pipeline_test import (
    MOCK_ENERGY_MAX,
    MOCK_ENERGY_MIN,
    MOCK_W_E,
    MOCK_W_S,
    compute_energy,
    compute_events_hash,
    compute_utility,
    make_actions,
    run_pipeline,
    write_csv,
)
from src.envs.mock_adapter import MockAdapter


class TestPipelineIntegration(unittest.TestCase):

    def test_interface_integration(self):
        """All four components must work together."""
        result = run_pipeline(seed=20261125, n_steps=10)
        self.assertEqual(result["seed"], 20261125)
        self.assertEqual(result["n_steps"], 10)
        self.assertGreater(result["n_events"], 0)
        self.assertIn("utility", result)
        self.assertIn("events", result)

    def test_state_validation(self):
        """Every joint state built during the pipeline must be valid."""
        # run_pipeline calls builder.build() internally; if any state
        # were invalid, validate_joint_state would have raised.
        result = run_pipeline(seed=20261125, n_steps=10)
        self.assertEqual(result["n_steps_logged"], 10)

    def test_reward_persistence(self):
        """No reward event must be lost."""
        result = run_pipeline(seed=20261125, n_steps=50)
        events = result["events"]
        # 1 reset + 50 steps = 51 events
        self.assertEqual(len(events), 51)
        self.assertEqual(events[0]["event"], "reset")
        steps = [e for e in events if e["event"] == "step"]
        self.assertEqual(len(steps), 50)
        # Shared reward must be present in every step.
        for e in steps:
            self.assertIn("shared", e["reward"])
            self.assertIsInstance(e["reward"]["shared"], float)


class TestUtilityCalculation(unittest.TestCase):

    def test_utility_zero_branch(self):
        """s=0 must give U=0 regardless of energy."""
        result = run_pipeline(seed=20261125, n_steps=10)
        u = result["utility"]
        self.assertEqual(u["s"], 0.0)
        self.assertEqual(u["U"], 0.0)

    def test_utility_success_branch(self):
        """s=1 must give U in (0, 1] and follow the formula."""
        result = run_pipeline(seed=20261125, n_steps=50)
        u = result["utility"]
        self.assertEqual(u["s"], 1.0)
        expected = MOCK_W_S + MOCK_W_E * (1.0 - u["E_norm"])
        self.assertAlmostEqual(u["U"], expected, places=10)
        self.assertGreater(u["U"], 0.0)
        self.assertLessEqual(u["U"], 1.0)

    def test_utility_components(self):
        """Energy and normalization must match the constants."""
        result = run_pipeline(seed=20261125, n_steps=50)
        u = result["utility"]
        self.assertEqual(u["w_s"], MOCK_W_S)
        self.assertEqual(u["w_e"], MOCK_W_E)
        self.assertEqual(u["energy_min"], MOCK_ENERGY_MIN)
        self.assertEqual(u["energy_max"], MOCK_ENERGY_MAX)
        self.assertGreaterEqual(u["E"], 0.0)
        self.assertGreaterEqual(u["E_norm"], 0.0)
        self.assertLessEqual(u["E_norm"], 1.0)


class TestReproducibility(unittest.TestCase):

    def test_same_seed_same_result(self):
        """Same seed must produce identical events and utility."""
        a = run_pipeline(seed=20261125, n_steps=50)
        b = run_pipeline(seed=20261125, n_steps=50)
        self.assertEqual(
            compute_events_hash(a["events"]),
            compute_events_hash(b["events"]),
        )
        self.assertEqual(a["utility"], b["utility"])

    def test_different_seed_different_events(self):
        """Different seeds must produce different event streams."""
        a = run_pipeline(seed=20261125, n_steps=50)
        b = run_pipeline(seed=20261126, n_steps=50)
        self.assertNotEqual(
            compute_events_hash(a["events"]),
            compute_events_hash(b["events"]),
        )


class TestResultExport(unittest.TestCase):

    def test_csv_export(self):
        """CSV must contain the expected columns and rows."""
        import tempfile
        results = [
            run_pipeline(seed=20261125, n_steps=10),
            run_pipeline(seed=20261125, n_steps=50),
        ]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "test_pipeline_mock.csv"
            write_csv(results, path)
            with path.open() as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[0]["seed"], "20261125")
                self.assertEqual(rows[0]["n_steps"], "10")
                self.assertEqual(rows[1]["n_steps"], "50")
                self.assertEqual(rows[0]["mock_label"], "MOCK-PROVISIONAL")
                for col in ("s", "E", "E_norm", "U", "w_s", "w_e"):
                    self.assertIn(col, rows[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
