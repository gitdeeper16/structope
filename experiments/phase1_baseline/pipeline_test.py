"""
Pipeline Test (Item 1.1) — Mock-only integration test.

This script exercises the full StructOPE data flow:

    MockAdapter -> StateBuilder -> RewardLogger -> Utility -> CSV/LOG

It does NOT:

    - make scientific claims about HeMAC,
    - use Fault Injection (Item 0.5),
    - validate OPE estimators,
    - define the final Utility range.

Utility is computed with the MOCK-PROVISIONAL [0, 100] range
declared in design/utility.md §4.3 and §8. It is labeled `mock`
throughout the output.

Determinism:

    - The seed is passed explicitly.
    - All inputs (config, n_steps, seed) are recorded in the LOG.
    - The CSV is written with a fixed column order.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from src.envs.mock_adapter import MockAdapter
from src.envs.interfaces import Action, AgentId
from src.eval.state_builder import StateBuilder
from src.eval.reward_logger import RewardLogger


# ---------------------------------------------------------------------
# Constants — MOCK-PROVISIONAL, not HeMAC
# ---------------------------------------------------------------------

MOCK_ENERGY_MIN = 0.0
MOCK_ENERGY_MAX = 100.0
MOCK_W_S = 0.5
MOCK_W_E = 0.5


# ---------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------

def make_actions(env: MockAdapter) -> Dict[AgentId, Action]:
    """Deterministic action policy: move toward the POI.

    Not a learned policy. Not evaluated. Used only to drive the
    environment deterministically so that the pipeline test can
    exercise both the energy and the completion branches of the
    utility function.

    Observation layout (MockAdapter):
        [x, y, dx_to_poi, dy_to_poi, charge]
    """
    actions: Dict[AgentId, Action] = {}
    for agent in env.agents:
        if not agent.is_active:
            continue
        obs = env.observation(agent.agent_id)
        dx = float(obs.vector[2])
        dy = float(obs.vector[3])
        norm = float(np.hypot(dx, dy))
        if norm > 1e-9:
            vx = float(np.clip(dx / norm, -1.0, 1.0))
            vy = float(np.clip(dy / norm, -1.0, 1.0))
        else:
            vx, vy = 0.0, 0.0
        actions[agent.agent_id] = Action(
            agent_id=agent.agent_id,
            vector=np.array([vx, vy, 0.0], dtype=float),
        )
    return actions


def compute_energy(events: List[Dict[str, Any]]) -> float:
    """Compute total absolute energy change across active agents.

    Uses the `charge_level` field of observations (index 4 in the
    MockAdapter observation vector). This is a MOCK placeholder.
    """
    total = 0.0
    prev: Dict[AgentId, float] = {}
    for e in events:
        if e["event"] != "step":
            continue
        for aid, obs in e["observations"].items():
            charge = float(obs.vector[4])
            if aid in prev:
                total += abs(charge - prev[aid])
            prev[aid] = charge
    return total


def compute_utility(events: List[Dict[str, Any]]) -> Dict[str, float]:
    """Compute U = s * (w_s + w_e * (1 - E_norm)).

    MOCK-PROVISIONAL.
    """
    # s(π): 1.0 if any agent reached POI within 1.0 unit, else 0.0.
    # In MockAdapter, POI is fixed per episode; check final distances.
    last_step = None
    for e in reversed(events):
        if e["event"] == "step":
            last_step = e
            break

    s = 0.0
    if last_step is not None:
        for obs in last_step["observations"].values():
            # obs.vector = [x, y, dx_to_poi, dy_to_poi, charge]
            dist = float(np.hypot(obs.vector[2], obs.vector[3]))
            if dist < 1.0:
                s = 1.0
                break

    E = compute_energy(events)
    if MOCK_ENERGY_MAX == MOCK_ENERGY_MIN:
        E_norm = 0.0
    else:
        E_norm = (E - MOCK_ENERGY_MIN) / (MOCK_ENERGY_MAX - MOCK_ENERGY_MIN)
        E_norm = float(np.clip(E_norm, 0.0, 1.0))

    U = s * (MOCK_W_S + MOCK_W_E * (1.0 - E_norm))
    return {
        "s": s,
        "E": E,
        "E_norm": E_norm,
        "U": U,
        "w_s": MOCK_W_S,
        "w_e": MOCK_W_E,
        "energy_min": MOCK_ENERGY_MIN,
        "energy_max": MOCK_ENERGY_MAX,
    }


def run_pipeline(seed: int, n_steps: int = 10,
                 config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Run the full pipeline for one seed."""
    if config is None:
        config = {"n_drones": 2, "max_cycles": 100}

    env = MockAdapter(config=config, seed=seed)
    builder = StateBuilder(env)
    logger = RewardLogger()

    # Reset
    reset_result = env.reset()
    logger.log_reset(reset_result)

    # Steps
    for _ in range(n_steps):
        actions = make_actions(env)
        step_result = env.step(actions)
        logger.log_step(step_result)
        # Build and validate the joint state.
        _ = builder.build()

    events = logger.get_events()
    utility = compute_utility(events)

    return {
        "seed": seed,
        "n_steps": n_steps,
        "config": config,
        "events": events,
        "utility": utility,
        "n_events": len(events),
        "n_steps_logged": sum(1 for e in events if e["event"] == "step"),
    }


# ---------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------

CSV_COLUMNS = [
    "seed", "n_steps", "n_events", "n_steps_logged",
    "s", "E", "E_norm", "U",
    "w_s", "w_e", "energy_min", "energy_max",
    "mock_label",
]


def write_csv(results: List[Dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for result in results:
            row = {
                "seed": result["seed"],
                "n_steps": result["n_steps"],
                "n_events": result["n_events"],
                "n_steps_logged": result["n_steps_logged"],
                "s": result["utility"]["s"],
                "E": result["utility"]["E"],
                "E_norm": result["utility"]["E_norm"],
                "U": result["utility"]["U"],
                "w_s": result["utility"]["w_s"],
                "w_e": result["utility"]["w_e"],
                "energy_min": result["utility"]["energy_min"],
                "energy_max": result["utility"]["energy_max"],
                "mock_label": "MOCK-PROVISIONAL",
            }
            writer.writerow(row)


def compute_events_hash(events: List[Dict[str, Any]]) -> str:
    """Deterministic hash of the event stream (for traceability)."""
    payload = json.dumps(events, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


# ---------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261125)
    parser.add_argument("--n-steps", type=int, nargs="+",
                        default=[10, 50],
                        help="Number of steps to test (default: 10 50)")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("results/tables/pipeline_test_mock.csv"),
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("results/logs/pipeline_test_mock.log"),
    )
    args = parser.parse_args()

    args.log.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(args.log),
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logging.info("Pipeline Test (Item 1.1) — Mock only")
    logging.info("MOCK-PROVISIONAL — not a HeMAC measurement")
    logging.info("timestamp_utc=%s", datetime.now(timezone.utc).isoformat())
    logging.info("seed=%d", args.seed)
    logging.info("n_steps=%s", args.n_steps)

    results = []
    for n_steps in args.n_steps:
        logging.info("running n_steps=%d", n_steps)
        result = run_pipeline(seed=args.seed, n_steps=n_steps)
        logging.info("n_steps=%d n_events=%d n_steps_logged=%d",
                     n_steps, result["n_events"], result["n_steps_logged"])
        logging.info("utility=%s", json.dumps(result["utility"], sort_keys=True))
        logging.info("events_hash_sha256=%s", compute_events_hash(result["events"]))
        results.append(result)

    write_csv(results, args.csv)
    logging.info("csv_written=%s", args.csv)

    print("Pipeline Test complete.")
    print(f"  seed={args.seed}")
    for r in results:
        print(f"  n_steps={r['n_steps']:3d} | s={r['utility']['s']:.0f} | E={r['utility']['E']:.4f} | U={r['utility']['U']:.4f}")
    print(f"  csv={args.csv}")
    print(f"  log={args.log}")


if __name__ == "__main__":
    main()
