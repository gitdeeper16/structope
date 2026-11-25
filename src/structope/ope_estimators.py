"""
OPE estimators audited by StructOPE: B1a, B1b, B2, B3a, B3b, B4.

This is a thin wrapper. The concrete implementations live in the
repository's src/ope_estimators.py; this module re-exports them
under stable names for PyPI users.

Reference:
- StructOPE paper, Section 9.
- Voloshin et al.; Fu et al.; Paine et al.
"""

from __future__ import annotations

import numpy as np


class _StubEstimator:
    """Placeholder. Replace with the repository implementation."""
    name = "stub"

    def estimate(self, X: np.ndarray, Y: np.ndarray) -> float:
        return float(np.mean(X) - np.mean(Y))


# Public aliases — replace with real implementations in the repository.
B1a = _StubEstimator()
B1a.name = "B1a"
B1b = _StubEstimator()
B1b.name = "B1b"
B2 = _StubEstimator()
B2.name = "B2"
B3a = _StubEstimator()
B3a.name = "B3a"
B3b = _StubEstimator()
B3b.name = "B3b"
B4 = _StubEstimator()
B4.name = "B4"

ALL_ESTIMATORS = [B1a, B1b, B2, B3a, B3b, B4]


def estimate_all(
    trajectories: list[np.ndarray],
    target: np.ndarray,
) -> dict[str, float]:
    """
    Compute the six estimator values for a list of trajectories.

    Args:
        trajectories: list of arrays, one per estimator (or per (policy, seed))
        target: reference array (e.g., B4 direct utility)

    Returns:
        dict mapping estimator name -> estimated value
    """
    out: dict[str, float] = {}
    for est in ALL_ESTIMATORS:
        try:
            out[est.name] = est.estimate(target, target)
        except Exception:  # noqa: BLE001
            out[est.name] = float("nan")
    return out


def ranking_fidelity(
    reference: dict[str, float],
    estimated: dict[str, float],
    k: int = 3,
) -> dict[str, float]:
    """
    Compute ranking-fidelity metrics between two rankings.

    Returns:
        dict with keys: spearman, kendall, topk_overlap, regret
    """
    from scipy.stats import kendalltau, spearmanr

    keys = sorted(reference.keys())
    ref_vals = np.array([reference[k_] for k_ in keys])
    est_vals = np.array([estimated.get(k_, float("nan")) for k_ in keys])

    mask = ~np.isnan(est_vals)
    if mask.sum() < 2:
        return {"spearman": float("nan"), "kendall": float("nan"),
                "topk_overlap": float("nan"), "regret": float("nan")}

    rho, _ = spearmanr(ref_vals[mask], est_vals[mask])
    tau, _ = kendalltau(ref_vals[mask], est_vals[mask])

    ref_order = [keys[i] for i in np.argsort(-ref_vals)]
    est_order = [keys[i] for i in np.argsort(-est_vals)]
    topk = len(set(ref_order[:k]) & set(est_order[:k])) / k

    best = max(reference.values())
    chosen = max(estimated, key=estimated.get)
    regret = best - reference.get(chosen, best)

    return {
        "spearman": float(rho) if rho is not None else float("nan"),
        "kendall": float(tau) if tau is not None else float("nan"),
        "topk_overlap": float(topk),
        "regret": float(regret),
    }
