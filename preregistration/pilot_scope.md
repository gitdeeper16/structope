# Pilot Scope

**Status:** DRAFT (2026-11-25). To be frozen before Pilot-1 runs.
**Item reference:** `design/checklist.md` §1.1
**Related:** `design/scenarios.md`, `design/policy_set.md`,
`design/baselines.md`, `preregistration/thresholds.md`.

---

## 1. Purpose

This document fixes the scope of the Pilot stage. The Pilot exists
to:

- characterize variance and stability of the evaluation pipeline,
- estimate the thresholds that will be frozen for Confirmatory
  Evaluation,
- verify that the policy set is behaviorally distinguishable in
  baseline.

The Pilot does **not** test the hypotheses H1–H4. Pilot results
are labeled exploratory and are not merged into confirmatory data.

---

## 2. Scenario selection — 6 cells

| ID | T | C | Role |
|---|---|---|---|
| S1 | T0 | C0 | Reference |
| S2 | T1 | C0 | Mild T shift |
| S3 | T2 | C0 | Stronger T shift |
| S4 | T0 | C1 | Mild C shift |
| S5 | T0 | C2 | Stronger C shift |
| S6 | T1 | C1 | Combined shift |

**Why these six:**

- They cover single-axis shifts (S2, S3, S4, S5) and a combined
  shift (S6).
- They include two severity levels on each axis (mild: T1, C1;
  stronger: T2, C2).
- They do not exhaust the full grid. T3, T4, C3, C4 are reserved
  for Confirmatory Evaluation.
- The choice is fixed here. It is not adjusted after observing
  Pilot results.

**What is not included in the Pilot:**

- T3, T4 (larger team changes).
- C3, C4 (partial partition, topology change).
- Any (T, C) cell not listed above.

These are not excluded from Confirmatory Evaluation. They are
excluded from the Pilot to keep the Pilot scoped.

---

## 3. Policy selection — 6 policies

The six policies are drawn from `design/policy_set.md` §3. They
are named by their formal IDs, not by new labels.

| ID | Type | Source in policy_set.md | Role |
|---|---|---|---|
| P_RAND | Random | §3, "Random" | Lower reference |
| P_RULE_A | Rule-based | §3, "Rule-based" (first) | Coordination behavior A |
| P_SINGLE | Single-Agent / Partial-Team | §4, "Single-Agent / Partial-Team" | Partial-team reference |
| P_TRAIN_H | Trained | §3, "Trained" (high) | Upper reference |
| P_TRAIN_M | Trained | §3, "Trained" (mid) | Mid reference |
| P_DEGRADED | Degraded | §3, "Degraded/Ablated" | Degradation probe |

**Why these six:**

- They cover all four archetypes from `design/policy_set.md` §3
  (Random, Rule-based, Trained, Degraded).
- They include two Trained policies so that within-archetype
  variance can be observed.
- P_SINGLE is included as the mandatory partial-team reference
  from `design/policy_set.md` §4.
- They do not include the two remaining trained policies from the
  Full Policy Set of 8. Those are reserved for Confirmatory
  Evaluation.

**Formal IDs:** The IDs P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H,
P_TRAIN_M, P_DEGRADED are placeholders until the concrete policy
instances are selected from the HeMAC inventory (see
`design/policy_set.md` §8). When the inventory is complete, each
ID is replaced by a concrete policy identifier with a
reproducibility fingerprint. The mapping is recorded in
`preregistration/thresholds.md`.

**What is not included in the Pilot:**

- The remaining two trained policies from the Full Policy Set.
- Any policy not listed above.

These are not excluded from Confirmatory Evaluation.

---

## 4. Run configuration — two-stage

### 4.1 Pilot-1 — Variance Characterization

| Parameter | Value |
|---|---|
| Scenarios | 6 (S1–S6) |
| Policies | 6 (P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M, P_DEGRADED) |
| Seeds | 3 (fixed: see §5.1) |
| Repeats per (policy, scenario, seed) | 3 |
| Total runs | 6 × 6 × 3 × 3 = 324 |

**Goal:** characterize between-seed and within-seed variance,
data quality, and pipeline stability.

**Statistical note:** three repeats per seed is better than two,
but it does not make variance estimation precise automatically.
The nine runs per (policy, scenario) cell are not nine
independent samples. Seeds are the independent levels; repeats
are measurements within each seed. Variance is decomposed
accordingly (§5.2), and the hierarchical bootstrap respects this
structure.

### 4.2 Pilot-2 — Threshold Calibration

| Parameter | Value |
|---|---|
| Scenarios | 6 (S1–S6) |
| Policies | 6 (same as Pilot-1: P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M, P_DEGRADED) |
| Seeds | 3 (same as Pilot-1) |
| Repeats per (policy, scenario, seed) | 5 |
| Total runs | 6 × 6 × 3 × 5 = 540 |

**Goal:** estimate the thresholds (ESS, Support Overlap,
Distributional Distance, k, ε, τ_min) that will be frozen for
Confirmatory Evaluation.

### 4.3 Transition condition: Pilot-1 → Pilot-2

Pilot-2 does not start automatically. Before Pilot-2 begins, the
following must be recorded in `docs/decisions.md`:

- the variance estimates from Pilot-1,
- the number of seeds and repeats that Pilot-1 shows to be
  necessary,
- confirmation that the pipeline is stable (no systematic
  anomalies across Pilot-1 runs),
- confirmation that the policy set meets the baseline
  separability criterion (`design/policy_set.md` §7.3).

If Pilot-1 shows that 3 seeds × 2 repeats is insufficient, the
Pilot-2 configuration is revised and the revision is recorded.
The revision is **not** chosen on the basis of confirmatory
results (which do not exist yet).

### 4.4 What is not decided here

- The number of runs in Pilot-2 is a design target, not a
  binding commitment. It may be adjusted at the transition point.
- The exact seeds are fixed in §5.1.
- The exact thresholds are estimated in Item 1.2 and frozen in
  Item 1.3.

---

## 5. Seeds and repeats — statistical units

### 5.1 Seeds

The Pilot uses three fixed seeds:

| Seed ID | Value | Role |
|---|---|---|
| seed_a | 20261125 | Primary |
| seed_b | 20261126 | Replication |
| seed_c | 20261127 | Replication |

The seeds are fixed before any run. They are not chosen on the
basis of results.

### 5.2 Seeds and repeats are not interchangeable

This is a critical point:

- A **seed** is a distinct environment realization. Different
  seeds produce different initial states.
- A **repeat** with the same seed is an independent run of the
  same realization. It measures non-determinism in the pipeline
  (e.g., from parallel execution) but does not add a new
  environment sample.

**Statistical unit:** the pair (seed, repeat) is treated as an
observation, but the two levels are not pooled blindly. Variance
decomposition distinguishes:

- between-seed variance (across seed_a, seed_b, seed_c),
- within-seed variance (across repeats of the same seed).

The hierarchical bootstrap in `design/scenarios.md` Part C
resamples seeds first, then repeats within each seed. This is
required because seeds and repeats are not exchangeable units.

If MockAdapter is used in the Pilot (see §6), the pipeline is
deterministic given a seed, so within-seed variance is zero. This
is a property of Mock, not of HeMAC. It does not justify reducing
the repeat count in HeMAC runs.

### 5.3 Independence claim

The Pilot does not assume that:
- different seeds produce independent utility distributions
  without verification,
- repeats with the same seed are independent draws from the
  environment.

Both assumptions are checked in Pilot-1 and reported.

---

## 6. Data storage

| Path | Purpose |
|---|---|
| `results/pilot/raw/` | Per-run CSV files |
| `results/pilot/summary/` | Aggregated summaries |
| `results/pilot/MANIFEST.md` | List of all pilot runs |
| `results/pilot/logs/` | Execution logs |

Pilot data is **not** merged into confirmatory data. The
directories are separate and the filenames carry a `pilot_`
prefix.

---

## 7. Mock vs HeMAC in the Pilot

This document defines the Pilot **scope**. It does not decide
whether the Pilot runs on MockAdapter or on HeMAC.

- If HeMAC is available, Pilot runs on HeMAC. The scope above
  applies unchanged.
- If HeMAC is not available, the Pilot cannot run. MockAdapter
  may be used to test the pipeline, but Mock results are not
  used to update thresholds in Item 1.2.

**No Mock result is used to calibrate ε, τ_min, or any threshold
that enters Confirmatory Evaluation.** This is a hard boundary.

---

## 8. What the Pilot does not decide

- The full Confirmatory scenario grid (T3, T4, C3, C4 are
  reserved).
- The full Confirmatory policy set (two trained policies are
  reserved).
- The final threshold values (these are estimated in Pilot-2 and
  frozen in Item 1.3).
- The statistical correction family (defined in
  `preregistration/metrics.md` §B.6).

---

## 9. Criteria for Pilot-1 sufficiency

These criteria are fixed **before** Pilot-1 runs. They are
checked at the transition to Pilot-2.

| # | Criterion | How checked |
|---|---|---|
| C1 | Pipeline stability | No run raises an unexpected exception; all CSV/LOG files are complete |
| C2 | Data quality | All planned runs produce the expected number of events |
| C3 | Seed variance observable | Between-seed utility differences are nonzero in at least one (policy, scenario) cell |
| C4 | Policy separability | At least one pair of policies is separated by the pairwise utility difference CI in at least one scenario |
| C5 | Coverage measurable | All three coverage metrics (ESS, Support Overlap, Distributional Distance) are computable for all Pilot cells |

If any criterion fails, Pilot-2 is **not** started. The failure
is recorded in `docs/decisions.md`, and the scope is revised.

C3 and C4 are descriptive: their purpose is to confirm that the
Pilot can distinguish what it needs to distinguish. They are not
confirmatory tests.

---

## 10. Non-claims

- Pilot results do not test H1–H4.
- Pilot results do not validate any OPE estimator.
- Pilot results do not replace Confirmatory Evaluation.
- Pilot results from Mock are not used to calibrate thresholds.
- The Pilot scope is not adjusted after observing Pilot results.

---

## 11. Decision record — Item 1.1 (FROZEN)

**Status:** FROZEN (2026-11-25). Changes require a documented
amendment and a new version of this file.

- Date: 2026-11-25
- Scenarios: 6 (S1–S6, §2)
- Policies: 6 (P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M,
  P_DEGRADED, §3)
- Seeds: 3 (seed_a=20261125, seed_b=20261126, seed_c=20261127,
  §5.1)
- Pilot-1: 3 seeds × 3 repeats per (policy, scenario), 324 runs
- Pilot-2: 3 seeds × 5 repeats per (policy, scenario), 540 runs
  (design target, not binding; transition condition §4.3)
- C3 and C4 are excluded from Pilot (§2, §8) and reserved for
  Confirmatory Evaluation.
- Transition condition: §4.3
- Sufficiency criteria: §9
- Mock/HeMAC boundary: §7
- Preregistration impact: scope, seeds, and sufficiency criteria
  are recorded before Pilot-1 runs. No Mock result is used to
  calibrate thresholds.
- Freeze rule: no scope change after this date without a
  documented amendment in `docs/decisions.md` and a new version
  of this file.
