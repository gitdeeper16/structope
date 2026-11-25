# Scenarios and Structural-Shift Design

**Status:** Item 0.3 CLOSED (2026-11-23). Item 0.7 OPEN.
**Item reference:** design/checklist.md §0.3, §0.7
**Blocking:** Item 0.3 resolved. Item 0.7 remains open.

## Purpose

This document defines:
1. The training strategy for structural shift (Item 0.3).
2. The reference execution protocol (Item 0.7).
3. The scenario grid used across all experimental stages.

---

## Part A — Training Strategy (Item 0.3)

### Decision

**Strategy: Baseline-only training (T0/C0), with held-out structural
shifts at evaluation.**

### Training Data

Trajectories recorded under (T0, C0) only. No exposure to any
structural shift during training.

### Validation Data

An independent split of (T0, C0) trajectories, disjoint from training.

### Hyperparameter Tuning

May use pilot data from structural shifts, provided:

- Pilot data are stored separately from training data.
- The use is documented in `preregistration/thresholds.md`.
- No test-time information leaks into the estimator.
- The same pilot data are not reused for a conflicting purpose.

### Confirmatory Evaluation

Structural shifts held out from training, validation, and
hyperparameter tuning.

### Pilot Data Usage

| Use | Permitted? |
|---|---|
| Pilot shift data in OPE training | No |
| Pilot shift data in hyperparameter tuning | Yes, documented |
| Pilot shift data in confirmatory evaluation | No |
| Pilot data for variance / sample size estimation | Yes |
| Pilot data for ε and τ_min calibration | Yes |

### Held-Out Full Cell Requirement

A structural-shift evaluation is considered independent only if at
least one full (T_k, C_l) combination has never entered any prior
stage: not training, not validation, not hyperparameter tuning, not
pilot data used for any of the above.

This full cell is withheld until the estimator architecture and
evaluation settings are frozen.

A difference in (T_k, C_l) label alone does not count as
independence if the same cell was seen in any prior stage.

### Interpretation

This configuration tests **OPE generalization across structural
shift**, not classical OPE validity within a fixed environment.

Classical OPE assumes that logging data and evaluation policy come
from the same environment. Baseline-only training deliberately
violates this assumption to test whether the estimator remains
valid when the structural configuration differs between recording
and evaluation.

### Impact on Hypotheses

- **H1** is interpreted as: ranking fidelity degrades when the
  structural configuration at evaluation differs from the training
  configuration.
- **H4** compares robustness profiles of Conventional OPE and
  Model-Based OPE under the same exposure conditions, with no
  assumption that either is superior.

### Decision Record — Item 0.3

- **Date:** 2026-11-23
- **Strategy:** Baseline-only training (T0/C0), held-out shifts at evaluation
- **Training data:** T0/C0 only
- **Validation data:** independent T0/C0 split
- **Hyperparameter tuning:** pilot shift data permitted, documented, isolated
- **Confirmatory test data:** held-out (T_k, C_l), including at least one fully unseen cell
- **Withheld full cell:** required, frozen until estimator and evaluation settings are locked
- **Interpretation:** OPE generalization across structural shift, not classical OPE validity
- **Preregistration impact:** Training strategy frozen; any change requires a new version and explicit exploratory labeling

---

## Part B — Scenario Grid

### Team Composition (T)

| Level | Description | Notes |
|---|---|---|
| T0 | Baseline composition | Training-visible |
| T1 | Agent dropout | One Quadcopter removed at episode start |
| T2 | Capability degradation | One sensor or movement range reduced |
| T3 | Agent replacement | One agent replaced by a lower-capability equivalent |
| T4 | Team-size change | One additional agent added or removed |

The choice of which specific agent is affected (e.g., which
Quadcopter drops out) must be documented per scenario, not left to
the implementation.

### Communication Structure (C)

| Level | Description | Notes |
|---|---|---|
| C0 | Baseline communication | Training-visible |
| C1 | Random packet loss | Probabilistic message drop |
| C2 | Communication delay | Added latency to message delivery |
| C3 | Partial partition | Subset of agents cannot communicate |
| C4 | Topology change | Communication graph structure altered |

### Severity

Three severity levels per applicable change:

- **Mild** — low parameter value, expected minimal ranking impact.
- **Moderate** — mid-range, expected to affect some policy pairs.
- **Severe** — high parameter value, expected to produce ranking
  inversions for at least some policy pairs.

Numerical definitions must be fixed during the pilot stage and
recorded in `preregistration/thresholds.md`. They are not fixed here.

### Distribution Conditions

| Condition | Definition |
|---|---|
| In-Distribution (ID) | (T, C) cells seen in training |
| Near-OOD | Mild deviations from training cells |
| OOD | (T, C) cells withheld from training |

The test split must contain unseen combinations, not merely new
random seeds from already observed configurations.

### Factorial Design Rule

- Stage 1: T0/C0 only.
- Stage 2a: Individual T changes (C0 fixed).
- Stage 2b: Individual C changes (T0 fixed).
- Stage 2c: Combined (T, C) changes, restricted to combinations that
  passed through 2a and 2b.

This ordering prevents an unnecessarily large initial experimental
space and allows attribution of observed failures.

---

## Part C — Reference Execution Protocol (Item 0.7)

**Status:** OPEN pending revision (2026-11-23). See §Decision Record.

### Purpose

The reference simulator is the source of truth for policy ranking.
It must be characterized before it can define a wrong-ranking event.

### Seeds and repeats

Two distinct levels of replication are used:

- **Seeds** measure between-seed variance. Each seed is a distinct
  environment realization.
- **Repeats** measure within-scenario variance using independent runs
  with the same seed.

Each (policy, scenario) cell is executed with:

- multiple seeds, and
- multiple repeats per seed.

The unit of experiment is the tuple `(policy, scenario, seed,
repeat_id)`. Both `seed` and `repeat_id` are logged.

**Re-running the same seed is not a substitute for seed diversity.**

### Number of executions

- **Pilot stage:** determine the number of seeds and repeats needed
  to obtain a stable ranking interval. Preliminary target: at least
  5 (seed, repeat) combinations per (policy, scenario) cell, with at
  least 2 distinct seeds.
- **Confirmatory stage:** the number of seeds and repeats is fixed
  from pilot results and recorded in `preregistration/thresholds.md`.

### Pairwise utility difference

For each scenario and each pair of policies (A, B), compute:

```

Delta_AB = Mean_Utility(A) - Mean_Utility(B)

```

where the mean is taken over the (seed, repeat) structure described
above.

- Construct a bootstrap confidence interval for `Delta_AB`.
- Use **hierarchical bootstrap**: resample seeds first, then
  repeats within each seed. Bootstrap over repeats alone is not
  used.
- If the CI for `Delta_AB` **excludes zero**, the pair (A, B) is
  **separated**.
- If the CI **includes zero**, the pair (A, B) is **rank-ambiguous**.

Rank ambiguity is a property of the pair, not of individual policy
intervals. Individual policy intervals are reported descriptively
but are not used to declare separation.

### Handling rank-ambiguous policies

- **Excluded from** ranking-fidelity metrics (Spearman's rho,
  Kendall's tau, Top-k accuracy) for that scenario.
- **Retained in** selection-regret analyses, with the ambiguity
  flagged.
- **Reported in** a dedicated table, per scenario, listing the
  rank-ambiguous pairs and the uncertainty in their ordering.

### Acceptance criteria

- A pilot reference table exists at
  `results/tables/reference_pilot.md`.
- The number of seeds and repeats used in the confirmatory stage is
  fixed and recorded in `preregistration/thresholds.md`.
- At least 80% of policy pairs are expected to be separable in
  baseline. This is a **provisional operational acceptance
  criterion**, not a statistical fact and not a general scientific
  standard.

### If the 80% criterion is not met

- The policy set is reviewed (Item 0.6).
- The utility distribution is inspected.
- Policies are **not** forced into an order the data do not
  support.
- The set is **not** changed on the basis of confirmatory evaluation
  results.

---

## Decision Record — Item 0.7

**Status:** OPEN pending revision (2026-11-23).

- Date: pending
- Seeds per (policy, scenario) cell (pilot): PILOT-DEPENDENT
- Repeats per (policy, scenario, seed) cell (pilot): PILOT-DEPENDENT
- Seeds per cell (confirmatory): fixed after pilot
- Repeats per (seed) cell (confirmatory): fixed after pilot
- Bootstrap: hierarchical (seeds, then repeats)
- Rank-ambiguity test: pairwise utility difference CI
- 80% separability: provisional operational acceptance criterion
- Preregistration impact: all PILOT-DEPENDENT quantities recorded
  in `preregistration/thresholds.md`

---

## Explicit Non-Goals

This document does not:
- Set numerical severity parameters (pilot-dependent).
- Choose the OPE estimator.
- Choose the candidate policy list.
- Define the statistical analysis plan.
