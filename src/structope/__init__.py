"""
StructOPE: Off-Policy Evaluation under Structural Shift.

A pre-registered, falsification-first protocol for auditing Off-Policy
Evaluation estimator rankings under structural shift in multi-agent
environments.

Key components:
- OPE estimators: B1a, B1b, B2, B3a, B3b, B4
- Distance: Maximum Mean Discrepancy (Gaussian RBF kernel)
- Support rule: zero-support threshold n_min = 30
- Fault injection: 8 types × 3 severity × 3 timing

References:
- Zenodo DOI: 10.5281/zenodo.24473998
- OSF Preregistration: 10.17605/OSF.IO/EZJKF
- Figshare DOI: 10.6084/m9.figshare.35117266
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__license__ = "CC-BY-4.0"

from structope.mmd_distance import mmd, median_heuristic_bandwidth
from structope.coverage import comparable_states, zero_support_fraction
from structope.fault_injection import FaultType, Severity, Timing, inject_fault
from structope.ope_estimators import (
    B1a, B1b, B2, B3a, B3b, B4,
    estimate_all, ranking_fidelity,
)

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "mmd",
    "median_heuristic_bandwidth",
    "comparable_states",
    "zero_support_fraction",
    "FaultType",
    "Severity",
    "Timing",
    "inject_fault",
    "B1a", "B1b", "B2", "B3a", "B3b", "B4",
    "estimate_all",
    "ranking_fidelity",
]
