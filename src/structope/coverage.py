"""
Coverage and zero-support rule (n_min = 30).

Reference:
- StructOPE preregistration/thresholds.md
"""

from __future__ import annotations

import numpy as np


def comparable_states(
    X: np.ndarray,
    Y: np.ndarray,
    n_min: int = 30,
) -> np.ndarray:
    """
    Return the set of states where both X and Y have at least n_min observations.

    Args:
        X: array of shape (n,) of state identifiers
        Y: array of shape (m,) of state identifiers
        n_min: minimum number of observations per state

    Returns:
        sorted array of comparable state identifiers
    """
    unique_x, counts_x = np.unique(X, return_counts=True)
    unique_y, counts_y = np.unique(Y, return_counts=True)
    set_x = set(unique_x[counts_x >= n_min].tolist())
    set_y = set(unique_y[counts_y >= n_min].tolist())
    return np.array(sorted(set_x & set_y))


def zero_support_fraction(
    X: np.ndarray,
    Y: np.ndarray,
    n_min: int = 30,
) -> float:
    """
    Fraction of states where the number of observations is below n_min.

    Args:
        X: array of shape (n,)
        Y: array of shape (m,)
        n_min: minimum support threshold

    Returns:
        fraction in [0, 1]
    """
    all_states, counts = np.unique(np.concatenate([X, Y]), return_counts=True)
    if len(all_states) == 0:
        return 0.0
    return float(np.mean(counts < n_min))
