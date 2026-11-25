# StructOPE — Roadmap

**Version:** 1.0.0
**Phase:** Pre-registration (Protocol v1.0) — complete for design items
**Status:** Infrastructure complete. Pilot scope frozen. No experiments run.

---

## Phase Overview

| Phase | Description | Status |
|---|---|---|
| Pre-registration | Protocol + design items | ✅ 0.1–0.8 (0.5a COMPLETE 2026-11-25; 0.5b/0.5c deferred until HeMAC) |
| Infrastructure | Interfaces, adapters, eval components | ✅ Complete (66 tests) |
| Pilot Scope | Scenario/policy/run configuration | ✅ FROZEN (2026-11-25) |
| Pilot-1 (Variance) | 324 runs, 6 scenarios × 6 policies × 3 seeds × 3 repeats | ❌ Not started |
| Pilot-2 (Thresholds) | 540 runs, 6 scenarios × 6 policies × 3 seeds × 5 repeats | ❌ Not started |
| Preregistration Freeze | Item 1.3 | ❌ Not started |
| Confirmatory | Held-out evaluation | ❌ Not started |
| Analysis | Pre-registered statistical plan | ❌ Not started |
| Report | Pre-registered report | ❌ Not started |

---

## Design Items

| # | Item | Status | Blocking? |
|:-:|---|:-:|:-:|
| 0.1 | Utility | ✅ CLOSED | Yes |
| 0.2 | Baselines | ✅ CLOSED | Yes |
| 0.2a | Reward scope in B1 | ✅ CLOSED (B1a conditional) | No |
| 0.3 | Training strategy | ✅ CLOSED | Yes |
| 0.4 | Coverage metric | ✅ CLOSED | No |
| 0.5 | Fault injection | ⏳ PARTIAL (0.5a ✅, 0.5b/0.5c deferred) | No |
| 0.6 | Policy set | ✅ CLOSED (design level) | No |
| 0.7 | Reference execution protocol | ✅ CLOSED | No |
| 0.8 | Statistical plan | ✅ CLOSED | Yes |

---

## Pilot Items

| # | Item | Status | Notes |
|:-:|---|:-:|---|
| 1.0 | Pipeline Integration Test | ✅ CLOSED | Mock only; 66 tests |
| 1.1 | Pilot Scope | ✅ FROZEN | `preregistration/pilot_scope.md` |
| 1.2 | Threshold Calibration | ⏳ Waiting | Needs Pilot data |
| 1.3 | Preregistration Freeze | ⏳ Waiting | Needs 1.1 + 1.2 |

---

## Infrastructure

| Component | Tests | Status |
|---|:-:|:-:|
| `EnvironmentInterface` | 17 | ✅ |
| `MockAdapter` | 29 | ✅ |
| `StateBuilder` | 4 | ✅ |
| `RewardLogger` | 7 | ✅ |
| `Pipeline Test` | 9 | ✅ |
| **Total** | **66** | ✅ |

---

## What is not on this roadmap

- Any confirmatory experiment before Pilot-2 completes and
  Item 1.3 freezes the thresholds.
- Any implementation of an OPE estimator before HeMAC is
  available.
- Any claim of structural robustness before the confirmatory
  phase.
- Any Mock result used to calibrate thresholds.
- Any Pilot scope change after the 2026-11-25 freeze without a
  documented amendment.

---

## Open questions before Pilot-1

| # | Question | Status |
|:-:|---|---|
| Q1 | Is HeMAC available? | ❌ No (as of 2026-11-25) |
| Q2 | If HeMAC becomes available, which adapter is written first? | TBD |
| Q3 | If HeMAC is not available, is Pilot-1 run on Mock? | No — Mock results cannot calibrate thresholds |
| Q4 | What blocks Item 0.5 (Fault Injection) from closing? | 0.5a done. 0.5b (implementation) and 0.5c (determinism test) require HeMAC source tree. Not blocking for Pilot; blocks Confirmatory. |

---

**StructOPE v1.0.0 — pre-registration**
© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance
DOI: [10.5281/zenodo.24473998](https://doi.org/10.5281/zenodo.24473998)
