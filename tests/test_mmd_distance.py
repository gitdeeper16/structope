import numpy as np
from structope import mmd, median_heuristic_bandwidth


def test_mmd_zero_for_identical():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(100, 2))
    val = mmd(X, X.copy(), biased=True)
    assert val < 1e-6


def test_mmd_positive_for_shifted():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(100, 2))
    Y = rng.normal(loc=2.0, size=(100, 2))
    assert mmd(X, Y) > 0.1


def test_median_heuristic_positive():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(50, 2))
    Y = rng.normal(size=(50, 2))
    sigma = median_heuristic_bandwidth(X, Y)
    assert sigma > 0
