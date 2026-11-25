import numpy as np
from structope import comparable_states, zero_support_fraction


def test_comparable_states():
    X = np.array([1, 1, 1, 2, 2, 2, 3])
    Y = np.array([1, 1, 2, 2, 2, 4])
    result = comparable_states(X, Y, n_min=2)
    assert set(result.tolist()) == {1, 2}


def test_zero_support_fraction():
    X = np.array([1, 2, 3])
    Y = np.array([1, 2, 3])
    frac = zero_support_fraction(X, Y, n_min=30)
    assert frac == 1.0
