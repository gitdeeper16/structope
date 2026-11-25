"""
Maximum Mean Discrepancy (MMD) with Gaussian RBF kernel.

Reference:
- Gretton et al. (2012). A kernel two-sample test. JMLR 13: 723-773.
- Garreau et al. (2017). Large sample analysis of the median heuristic.
"""

from __future__ import annotations

import numpy as np
from scipy.spatial.distance import pdist, squareform


def median_heuristic_bandwidth(X: np.ndarray, Y: np.ndarray) -> float:
    """
    Compute the median-heuristic bandwidth for the Gaussian RBF kernel.

    Args:
        X: array of shape (n, d)
        Y: array of shape (m, d)

    Returns:
        bandwidth (float)
    """
    Z = np.vstack([X, Y])
    pairwise = pdist(Z, metric="euclidean")
    if len(pairwise) == 0:
        return 1.0
    sigma = float(np.median(pairwise))
    return sigma if sigma > 0 else 1.0


def _rbf(X: np.ndarray, Y: np.ndarray, sigma: float) -> np.ndarray:
    """Gaussian RBF kernel matrix."""
    d2 = squareform(pdist(np.vstack([X, Y]), metric="sqeuclidean"))
    n = X.shape[0]
    K = np.exp(-d2 / (2.0 * sigma ** 2))
    return K[:n, n:], K[:n, :n], K[n:, n:]


def mmd(
    X: np.ndarray,
    Y: np.ndarray,
    sigma: float | None = None,
    biased: bool = True,
) -> float:
    """
    Compute MMD^2 between two samples using a Gaussian RBF kernel.

    Args:
        X: array of shape (n, d)
        Y: array of shape (m, d)
        sigma: bandwidth (if None, uses median heuristic)
        biased: if True, include diagonal terms (biased estimator)

    Returns:
        MMD^2 (float, >= 0)
    """
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)

    if sigma is None:
        sigma = median_heuristic_bandwidth(X, Y)

    Kxy, Kxx, Kyy = _rbf(X, Y, sigma)

    if biased:
        n, m = X.shape[0], Y.shape[0]
        term_x = Kxx.sum() / (n * n)
        term_y = Kyy.sum() / (m * m)
        term_xy = Kxy.mean()
        return float(term_x + term_y - 2.0 * term_xy)

    n, m = X.shape[0], Y.shape[0]
    Kxx_off = Kxx[~np.eye(n, dtype=bool)].sum() / (n * (n - 1))
    Kyy_off = Kyy[~np.eye(m, dtype=bool)].sum() / (m * (m - 1))
    return float(Kxx_off + Kyy_off - 2.0 * Kxy.mean())
