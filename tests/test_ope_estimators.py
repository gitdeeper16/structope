import numpy as np
from structope.ope_estimators import ranking_fidelity


def test_ranking_fidelity_perfect():
    ref = {"a": 1.0, "b": 0.8, "c": 0.6, "d": 0.4}
    est = {"a": 1.0, "b": 0.8, "c": 0.6, "d": 0.4}
    m = ranking_fidelity(ref, est)
    assert abs(m["spearman"] - 1.0) < 1e-6
    assert abs(m["kendall"] - 1.0) < 1e-6
    assert m["topk_overlap"] == 1.0
    assert m["regret"] == 0.0
