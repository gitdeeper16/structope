"""Quickstart for the StructOPE PyPI package."""

import numpy as np
from structope import mmd, comparable_states, ranking_fidelity

# 1. MMD between two samples
rng = np.random.default_rng(42)
X = rng.normal(size=(100, 2))
Y = rng.normal(loc=1.0, size=(100, 2))
print(f"MMD(X, Y) = {mmd(X, Y):.4f}")

# 2. Comparable states
states_X = rng.integers(0, 20, size=500)
states_Y = rng.integers(0, 20, size=500)
comp = comparable_states(states_X, states_Y, n_min=30)
print(f"Comparable states: {comp.size} / 20")

# 3. Ranking fidelity
reference = {"B1a": 0.9, "B1b": 0.8, "B2": 0.7, "B3a": 0.6, "B3b": 0.5, "B4": 1.0}
estimated = {"B1a": 0.85, "B1b": 0.75, "B2": 0.65, "B3a": 0.55, "B3b": 0.45, "B4": 1.0}
metrics = ranking_fidelity(reference, estimated)
print(f"Spearman = {metrics['spearman']:.3f}")
print(f"Kendall  = {metrics['kendall']:.3f}")
