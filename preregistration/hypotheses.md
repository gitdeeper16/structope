# Hypotheses

**Status:** DRAFT (2026-11-23). To be frozen in Item 1.3.
**Date:** 2026-11-23
**Related:** `PROTOCOL.md` §11; `preregistration/metrics.md`;
`design/baselines.md`; `design/scenarios.md`; `docs/decisions.md`.

---

## Freezing rules

- H1–H4 are frozen at Item 1.3 (Preregistration Freeze).
- Any change after Pilot results are seen requires a documented
  amendment in `docs/decisions.md`, with the reason and the
  affected tests.
- Pilot data are not used in confirmatory evaluation.

---

## H1 — Structural Shift and Ranking Fidelity

**Statement.** Policy-ranking fidelity decreases under structural
changes between offline data collection and evaluation. The effect
may differ between team-composition changes and communication
changes.

**Tested by.**
- Spearman's rho (`preregistration/metrics.md` §B.2.1)
- Kendall's tau (§B.2.2)
- Top-k ranking accuracy (§B.2.3)

**Comparison.** Baseline (T0, C0) versus structural-shift cells
(T_k, C_l). The (T, C) grid is defined in `design/scenarios.md`.

**Not claimed.**
- That the degradation is uniform across all (T_k, C_l).
- That the degradation is monotonic in the magnitude of the shift.
- That a particular estimator is responsible for the degradation.

---

## H2 — Structural Shift and Selection Regret

**Statement.** Policy-selection regret increases under structural
changes, with potentially different failure patterns across OPE
methods.

**Tested by.**
- `Regret_eligible` (`preregistration/metrics.md` §B.3.1)
- `Regret_full` (§B.3.2), reported descriptively

**Comparison.** Baseline (T0, C0) versus structural-shift cells
(T_k, C_l), across the applicable baselines.

**Not claimed.**
- That all estimators show the same regret profile.
- That `Regret_full` alone is sufficient to characterize failure.

---

## H3 — Selective Evaluation

**Statement.** Selective policy evaluation reduces selection regret
under structural shift when its uncertainty signal is genuinely
associated with ranking error, rather than merely detecting
unfamiliar configurations.

**Tested by.**
- Comparison of `Regret_eligible` between selective and
  non-selective evaluation on the same (T_k, C_l) cells.
- Relation between the uncertainty signal and ranking error
  (Spearman's rho between signal and error across cells).

**Comparison.** Selective evaluation versus non-selective evaluation,
within the same (T, C) cells.

**Not claimed.**
- That selective evaluation eliminates regret.
- That selective evaluation is always preferable.
- That an uncertainty signal that detects unfamiliarity necessarily
  detects ranking error.

---

## H4 — Method-Dependent Robustness

**Statement.** Conventional OPE and Model-Based OPE exhibit
different robustness profiles under team-composition and
communication changes. Neither method is assumed to dominate across
all conditions.

**Tested by.**
- Comparison of degradation profiles (H1 metrics and H2 metrics)
  between conventional OPE (B1a, B1b, B2) and model-based OPE (B3a).
- B3b is included only if its methodological distinctness from B3a
  is established (`design/baselines.md` §4).

**Comparison.** Conventional vs. model-based, across (T, C) cells.

**Not claimed.**
- That either method is universally superior.
- That one method dominates all others in all cells.
- That the comparison is valid in cells where coverage is
  inadequate (Part A).

---

## Relation to metrics and thresholds

Each hypothesis is associated with metrics defined in
`preregistration/metrics.md`. Numerical thresholds, acceptance
criteria, and effect sizes are **PILOT-DEPENDENT** and are recorded
in `preregistration/thresholds.md` before any confirmatory
evaluation.

No hypothesis is evaluated against Pilot results. Pilot is used to
characterize the pipeline and to fix thresholds, not to test H1–H4.

---

## What this file does not do

- It does not fix numerical thresholds (see
  `preregistration/thresholds.md`).
- It does not fix the statistical correction (see
  `preregistration/metrics.md` §B.6).
- It does not select the policy set (see `design/policy_set.md`).
- It does not choose the baselines (see `design/baselines.md`).
- It does not report any result.
