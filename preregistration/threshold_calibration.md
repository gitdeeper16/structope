# Threshold Calibration

**Status:** DRAFT (2026-11-25). To be reviewed before Pilot-1
runs. Final values frozen in Item 1.3.
**Item reference:** `design/checklist.md` §1.2
**Related:** `preregistration/pilot_scope.md`,
`preregistration/metrics.md` Part A and Part B,
`preregistration/thresholds.md`, `design/scenarios.md` Part C.

---

## 1. Purpose

This document specifies **how** the numerical thresholds used in
Confirmatory Evaluation will be estimated from Pilot data. It does
**not** set the thresholds themselves. It defines:

- the calibration procedure for each threshold,
- the uncertainty that must be attached to each estimate,
- the conditions under which Pilot-1 suffices to proceed to
  Pilot-2,
- the boundary between Mock and HeMAC data.

All numerical values below are **provisional targets**. They are
replaced by the calibrated values in Item 1.3.

---

## 2. Status and scope

### 2.1 What this document does

- Defines the calibration method for ε, τ_min, ESS threshold,
  Support Overlap threshold, Distributional Distance threshold,
  and k (Top-k).
- Defines the procedure to estimate these from Pilot-1 data.
- Defines the transition condition from Pilot-1 to Pilot-2.
- Fixes the Mock/HeMAC boundary.

### 2.2 What this document does not do

- It does not set final values. Those are set in Item 1.3.
- It does not replace `preregistration/metrics.md`.
- It does not replace `preregistration/pilot_scope.md`.
- It does not authorize Confirmatory Evaluation.

---

## 3. Provisional initial values

These values are used **only** to run Pilot-1 and Pilot-2. They
are not the confirmatory values.

| Parameter | Provisional value | Source |
|---|---|---|
| ε (normalized regret) | 0.05 | `design/checklist.md` §1.2 |
| τ_min (Kendall's Tau) | 0.70 | `design/checklist.md` §1.2 |
| ESS normalized threshold | TBD | estimated in Pilot-2 |
| Support Overlap threshold | TBD | estimated in Pilot-2 |
| Distributional Distance threshold | TBD | estimated in Pilot-2 |
| k (Top-k accuracy) | 3 | see §8 |

None of these is used in Confirmatory Evaluation without
calibration.

---

## 4. Calibration procedure — overview

The calibration has two stages:

**Stage 1 (Pilot-1, 324 runs):** variance characterization.

- The pipeline is exercised.
- Between-seed and within-seed variance is estimated.
- Whether the planned Pilot-2 size is sufficient is checked.
- **No threshold is fixed at this stage.**

**Stage 2 (Pilot-2, 540 runs):** threshold calibration.

- The thresholds are estimated using the procedure in §5–§9.
- Each estimate is reported with a bootstrap confidence interval.
- The estimates are frozen in Item 1.3.

**Transition condition from Pilot-1 to Pilot-2** is defined in
§11. It is checked before Pilot-2 runs.

---

## 5. ESS threshold

### 5.1 Definition

The ESS threshold is the minimum normalized ESS below which an
OPE estimate is flagged as **coverage-inadequate** for
interpretation (`preregistration/metrics.md` §B.5).

### 5.2 Calibration method

The threshold is the **10th percentile of normalized ESS values
observed in the baseline cell (T0, C0)** in Pilot-2, computed
across:

- all 6 policies,
- all 3 seeds,
- all 5 repeats.

**Justification for the 10th percentile.**

The 10th percentile is chosen as an **initial design choice**,
not a statistical fact. It flags the lowest decile of baseline
coverage as "coverage-inadequate". The choice reflects a
preference for a conservative flag: a threshold at the 5th
percentile would flag fewer cases; a threshold at the 20th would
flag more.

The choice is **not** asserted to be optimal. It is tested for
sensitivity in §5.4. If the choice of percentile materially
changes the ranking conclusions, this is documented and not
hidden.

**Sensitivity analysis.**

The sensitivity analysis compares three choices:

| Choice | Percentile | Rationale |
|---|---|---|
| Narrow flag | 5th | Only the most extreme cases are flagged |
| **Primary** | **10th** | **Initial design choice** |
| Broad flag | 20th | A wider set of cases is flagged |

For each choice, the ESS threshold is computed and the effect on
the coverage-inadequate classification (Part A §B.5) is
recorded. If the classification of any (policy, scenario) cell
changes between 5th and 20th, this is reported explicitly, not
resolved by choosing the "convenient" percentile.

### 5.3 Uncertainty

The 10th percentile is reported with a bootstrap confidence
interval. The interval is computed with the hierarchical
bootstrap described in `design/scenarios.md` Part C (seeds
first, then repeats).

---

## 6. Support Overlap threshold

### 6.1 Definition

The Support Overlap threshold is the minimum overlap between
logged and target behavior below which an OPE estimate is
flagged as **coverage-inadequate** (`preregistration/metrics.md`
§B.5).

### 6.2 Calibration method

The threshold is the **10th percentile of Support Overlap values
observed in the baseline cell (T0, C0)** in Pilot-2, computed
across the same axes as §5.2.

**Justification and sensitivity.**

The rationale and the sensitivity analysis are the same as for
ESS (§5.2, §5.4). The 10th percentile is an initial design
choice; the effect of 5th and 20th percentile is compared; and
any change in classification between 5th and 20th is reported
explicitly.

### 6.3 Uncertainty

Bootstrap confidence interval, as in §5.3.

---

## 7. Distributional Distance threshold

### 7.1 Definition

The Distributional Distance threshold is the maximum distance
between logged and target behavior above which an OPE estimate
is flagged as **coverage-inadequate** (`preregistration/metrics.md`
§B.5).

### 7.2 Distance choice — decision procedure

The distance is **not fixed here**. It is selected by a
pre-registered procedure, applied to HeMAC data **before**
Pilot-2 runs and **before** Pilot-2 results are seen.

#### 7.2.1 Comparison unit

The first step is to fix what the distance is computed
**between**. Three units are possible, and they are not
equivalent:

| Unit | What it measures | When appropriate |
|---|---|---|
| U1. Policy distributions | Distance between the distributions of two policies | Comparing policies directly |
| U2. State-conditioned action distributions | Distance between action distributions conditioned on state | Comparing behavior at matched states |
| U3. State-action visitation | Distance between full visitation distributions | Comparing coverage of the (state, action) space |

The unit is fixed **before** the distance is chosen. The choice
of unit is recorded with its justification in
`preregistration/thresholds.md`.

The distance and the unit are not independent choices. A
distance that is well-defined on one unit may be undefined on
another.

**Fixed unit for this study: U2 (state-conditioned action distributions).**

Justification: the coverage question is whether the policy set exercises
distinct behaviors at matched states. U1 couples policy with the state
distribution it happens to visit. U3 mixes coverage with visitation
frequency. U2 isolates the action choice at matched states, which is what
the T/C shift is expected to perturb.

Operational definition of "matched states" is fixed in
`preregistration/r7_mmd_spec.md` §1.1 and mirrored in
`preregistration/thresholds.md`. It is fixed before Pilot-1, not inferred
from data.

Rejected units: U1 (environment-coupled), U3 (frequency ≠ behavior).

#### 7.2.2 Candidate distances and their restrictions

| Distance | Valid units | Restrictions |
|---|---|---|
| KL divergence | U1, U2 | Requires support overlap. Not used when the target has mass outside the logged support. No ad-hoc smoothing or clipping. |
| Total Variation | U1, U2, U3 | Defined whenever the distributions are defined on the same space |
| MMD | U1, U2, U3 | Requires a kernel choice and bandwidth selection; see §7.2.3 |

**KL restriction.** KL is used only when:

- the logged distribution has non-zero mass wherever the target
  has non-zero mass (support overlap is verified, not assumed),
- the densities can be estimated reliably on the relevant space.

If either condition fails, KL is **excluded**. It is not rescued
by additive smoothing or clipping, because these change the
quantity being measured.

**MMD specification.** If MMD is a candidate:

- the kernel family is fixed in advance (e.g., Gaussian),
- the bandwidth selection rule is fixed in advance (e.g.,
  median heuristic, fixed bandwidth from a pilot-independent
  rule),
- the rule is recorded in `preregistration/thresholds.md`
  before any distance is computed on Pilot-2 data.

Naming "Gaussian kernel" is not sufficient. The bandwidth rule
is part of the specification.

#### 7.2.3 Evaluability test

For each candidate distance and unit, the following are
checked on HeMAC data **from Pilot-1 only**:

- Can the distance be computed without undefined values?
- Can a bootstrap confidence interval be computed?
- Does the computation complete within the Pilot budget?

A distance that fails any check is excluded, with the reason
recorded. Excluded candidates and the reason for exclusion are
documented in `preregistration/thresholds.md`.

#### 7.2.4 Decision criteria

The candidates that pass §7.2.3 are compared on **pre-registered
criteria**, applied to Pilot-1 data:

| Criterion | What it tests | How it is measured |
|---|---|---|
| Interpretability | Does the distance have a clear meaning for the coverage question? | Recorded qualitatively, with examples |
| Stability across seeds | Does the distance give similar values on different seeds of the same cell? | Between-seed coefficient of variation |
| Sensitivity to structural shift | Does the distance change when the (T, C) cell changes? | Difference between cells, compared across candidates |

**All passing candidates are reported** with these three
measurements. The final choice is justified in
`preregistration/thresholds.md` with reference to the
measurements, not to the confirmatory outcome.

**No candidate is selected because it produces a convenient
threshold.** If two candidates give materially different
thresholds, both are reported and the disagreement is recorded.

#### 7.2.5 Decision authority

The choice is made by the **researcher** (Samir Baladi), not by
an automated procedure. The researcher:

- records the chosen distance and unit,
- records the excluded candidates and the reason,
- records the measurements from §7.2.4,
- signs the decision entry in `preregistration/thresholds.md`
  with the date and the data source used (Pilot-1 only).

The decision may be reviewed by the independent reviewer. The
reviewer's comments are recorded in `REVIEW/INDEPENDENT_REVIEW.md`.
The reviewer does not make the choice; the researcher does.

#### 7.2.6 Data source for the choice

The distance is chosen using **Pilot-1 data only**. It is fixed
**before** Pilot-2 runs and **before** Pilot-2 results are seen.

If Pilot-1 data are insufficient to apply §7.2.3 or §7.2.4,
Pilot-1 is extended and the extension is recorded. The choice
is not deferred to Pilot-2.

The data source used in the choice is recorded in
`preregistration/thresholds.md`.

#### 7.2.7 What is not done

- The distance is not chosen because it produces a convenient
  threshold.
- The distance is not chosen because it is familiar.
- The choice is not revisited after Pilot-2 or Confirmatory
  results are seen.
- KL is not used without verified support overlap.
- MMD is not used without a fixed bandwidth rule.

### 7.3 Calibration method

Once the distance is chosen, the threshold is the **90th
percentile of Distributional Distance values observed in the
baseline cell (T0, C0)** in Pilot-2.

**Justification.**

The 90th percentile (not the 10th) reflects that distance is a
divergence: higher values mean worse coverage. A threshold at
the 10th percentile would flag the *best* coverage, which is the
opposite of what is intended.

The 90th percentile is an **initial design choice**, not a
statistical fact. It is tested for sensitivity in §7.5.

**Sensitivity analysis.**

The sensitivity analysis compares three choices:

| Choice | Percentile | Rationale |
|---|---|---|
| Broad flag | 80th | Fewer cases are flagged |
| **Primary** | **90th** | **Initial design choice** |
| Narrow flag | 95th | More cases are flagged |

The effect of the choice on the coverage-inadequate
classification is recorded. If any (policy, scenario) cell
changes classification between 80th and 95th, this is reported
explicitly.

### 7.4 Uncertainty

Bootstrap confidence interval, as in §5.3.

---

## 8. Top-k value

### 8.1 Definition

k is the number of top policies used in Top-k ranking accuracy
(`preregistration/metrics.md` §B.2.3).

### 8.2 Calibration method

The provisional value is **k = 4**.

**Justification.**

k is tied to the **Confirmatory policy set**, not the Pilot
policy set. The Confirmatory set has 8 policies
(`design/policy_set.md` §3). k = 4 selects the top half of the
Confirmatory set.

The Pilot policy set has 6 policies. If k were tied to the
Pilot set, it would be 3. This would make k inconsistent
between Pilot and Confirmatory, and would change the meaning of
Top-k accuracy between the two stages. Tying k to the
Confirmatory set avoids this inconsistency.

The choice is a **design decision**, not a statistical fact.
It reflects an operational judgment: "top of the ranking" means
the top half of the policies under evaluation.

### 8.3 Sensitivity analysis

The sensitivity analysis compares three values:

| Choice | k | Rationale |
|---|---|---|
| Tighter | 3 | Top 3 of 8 (about 37%) |
| **Primary** | **4** | **Top half of Confirmatory set** |
| Looser | 5 | Top 5 of 8 (about 62%) |

For each value, the effect on the Top-k accuracy metric
(Part B.2.3) is recorded. If the conclusion about Top-k
accuracy changes between k = 3 and k = 5, this is reported
explicitly.

### 8.4 What is not decided here

The final k is not decided by a formula. It is reviewed after
Pilot-1 and fixed in Item 1.3. The choice is recorded with a
justification, not just a number.

**k is not chosen to maximize the observed Top-k accuracy.** It
is chosen to reflect what "top of the ranking" means
operationally. If the operational meaning changes, k changes,
and the change is recorded.

**Freeze rule.** k is not frozen until Item 1.3.

---

## 9. ε and τ_min calibration

### 9.1 ε (normalized regret)

The provisional value is **ε = 0.05**. The calibration rule, as
recorded in `design/checklist.md` §1.2, is:

```

ε = 1.5 × observed pilot selection regret under baseline

```

where "pilot selection regret under baseline" is the mean
`Regret_eligible` in (T0, C0) across Pilot-2 runs.

**Justification.**

The multiplier 1.5 is a **design margin** of 50% above baseline
regret. It is not a statistical constant and not an empirically
established value. The margin is intended to allow the threshold
to accommodate normal variability in OPE estimates without
flagging every small deviation as a failure.

The 1.5 multiplier is chosen as an initial design choice. It is
not asserted to be optimal.

This rule is preregistered. It is not adjusted after observing
confirmatory results.

**Sensitivity analysis.**

The sensitivity analysis compares three multipliers:

| Choice | Multiplier | Rationale |
|---|---|---|
| Tighter | 1.25 | Smaller margin; flags smaller deviations |
| **Primary** | **1.5** | **Initial design choice** |
| Looser | 2.0 | Larger margin; flags only larger deviations |

For each value, the effect on `Regret_eligible` classification
(Part B.3.1) is recorded. If the classification of any
(policy, scenario) cell changes between 1.25 and 2.0, this is
reported explicitly. The choice among the three is not resolved
by picking the value that yields the most favorable result.

**Freeze rule.**

ε is not frozen until Pilot-2 data are available. The final
value is recorded in Item 1.3 with the pilot statistic that
justified it.

### 9.2 τ_min (Kendall's Tau)

The provisional value is **τ_min = 0.70**. The calibration rule
is:

```

τ_min = 0.70, unless Pilot-1 shows that this is
unachievable for the best-performing OPE estimator under
baseline. In that case, τ_min is lowered to the 5th percentile
of baseline Kendall's tau across all estimators.

```

**Justification.**

The value 0.70 is a **provisional design choice**, not a
statistical fact. It is not adopted because Kendall's Tau ≥ 0.70
is sometimes described as "strong agreement" in the literature.
That description concerns interpretive labels, not OPE acceptance
thresholds, and it does not justify using 0.70 as a cutoff for
OPE validity.

The rule is preregistered. It is not adjusted after observing
confirmatory results.

**Sensitivity analysis.**

The sensitivity analysis compares three values:

| Choice | τ_min | Rationale |
|---|---|---|
| Stricter | 0.80 | OPE must track the reference ranking closely |
| **Primary** | **0.70** | **Provisional design choice** |
| Looser | 0.60 | OPE may deviate more from the reference ranking |

For each value, the effect on the ranking-fidelity
classification (Part B.4) is recorded. If the classification
of any (policy, scenario) cell changes between 0.60 and 0.80,
this is reported explicitly. The choice among the three is
not resolved by picking the value that yields the most
favorable result.

**Freeze rule.**

τ_min is not frozen at any of these values until Pilot-2 data
are available. The final value is recorded in Item 1.3 with the
pilot statistic that justified it.

---

## 10. Uncertainty

Uncertainty is reported in three components, not collapsed into
a single number.

### 10.1 Environment variance

The environment variance is estimated from the (seed, repeat)
structure:

- **Between-seed variance**: computed across seed_a, seed_b,
  seed_c.
- **Within-seed variance**: computed across repeats of the same
  seed.
- **Hierarchical bootstrap**: resamples seeds first, then
  repeats within each seed (`design/scenarios.md` Part C).

This component is not optional. It is reported for every
threshold.

### 10.2 OPE estimator variance

The OPE estimator has its own variance, distinct from the
environment variance.

**Source.** Importance weights, bootstrap inside the estimator,
and model misspecification.

**Method.** A bootstrap is run **inside the OPE estimator**, on
the logged data used by that estimator.

**Resampling unit.** The unit depends on the estimator type:

| Estimator | Resampling unit |
|---|---|
| B1a, B1b (factorized) | Episodes, with agent-level observations kept together |
| B2 (centralized joint) | Episodes, with joint observations kept together |
| B3a (model-based) | Episodes used to fit the model, kept together |
| B3b (world model, if included) | Same as B3a |

**Constraints.**

- The agent-level observations within one episode are **not**
  resampled independently. They are kept together, because they
  share an environment realization.
- The temporal structure within an episode is preserved. If the
  data are treated as a time series, a block bootstrap is used
  instead of an iid bootstrap.
- Importance weights are not resampled independently of the
  transitions they weight. They are resampled with the episode.

**Why this matters.** Independent resampling of observations
would break the statistical dependence induced by the
environment and by the policy. The resulting variance estimate
would be optimistic.

### 10.3 Total variance

The total variance is **not** assumed to be the sum of the
environment variance and the OPE variance.

The correct decomposition is:

```

V_total = V_environment + V_OPE + 2 * Cov(environment, OPE)

```

The covariance term is not assumed to be zero. If it cannot be
estimated reliably, the two components are **reported
separately**, and no total is reported.

**When a total is reported.** A total is reported only when:

- the covariance term has been estimated with an acceptable
  bootstrap confidence interval, **or**
- the covariance is shown to be negligible relative to both
  components, with the evidence recorded.

**When a total is not reported.** The two components are
reported side by side, with a note that a total is not provided
because the covariance is not reliably estimated.

**No single-number summary.** The document does not reduce the
three components (V_environment, V_OPE, Cov) to a single number
without an explicit justification.

### 10.4 Uncertainty on threshold selection

The threshold is a percentile of an observed distribution. The
uncertainty in the percentile itself is reported, not only the
uncertainty in the value it produces.

For each threshold:

- The bootstrap confidence interval for the percentile is
  reported.
- The threshold is also computed at 5th, 10th, 15th, and 20th
  percentiles (for 10th-based thresholds) or at 80th, 85th,
  90th, and 95th (for 90th-based thresholds).
- The stability of the threshold across these percentiles is
  recorded.
- If the threshold changes materially between adjacent
  percentiles, this is reported explicitly.

**Example.** If the 10th percentile of ESS is 0.40 and the 15th
percentile is 0.65, the threshold is **unstable** in this range.
This is reported, not hidden by picking one value.

### 10.5 Reporting format

Every calibrated threshold is reported as:

| Field | Content |
|---|---|
| Value | The chosen percentile value |
| V_environment | Environment variance component |
| V_OPE | OPE estimator variance component |
| Cov(env, OPE) | Covariance, or "not estimated" |
| V_total | Total variance, or "not reported" |
| Percentile stability | Change across adjacent percentiles |
| Bootstrap CI | Confidence interval on the percentile |

No field is omitted. No field is collapsed into another.

### 10.6 What is not done

- Environment variance is not assumed to be zero.
- OPE variance is not assumed to be zero.
- Covariance is not assumed to be zero.
- The three components are not summed into a single number
  without justification.
- A single percentile value is not reported without its
  stability across adjacent percentiles.

---

## 11. Pilot-1 → Pilot-2 transition condition

Pilot-2 does not start automatically. Before Pilot-2 begins, the
following are recorded in `docs/decisions.md`:

- **T1.** Variance estimates from Pilot-1: between-seed and
  within-seed variance for the primary metrics.
- **T2.** Whether the planned Pilot-2 configuration (3 seeds × 5
  repeats) is sufficient. If not, a revised configuration is
  recorded, with justification.
- **T3.** Pipeline stability: no run in Pilot-1 raised an
  unexpected exception; all CSV/LOG files are complete.
- **T4.** Policy separability: at least one pair of policies is
  separated by the pairwise utility difference CI in at least
  one scenario (per `preregistration/pilot_scope.md` §9, C4).
- **T5.** Coverage measurability: all three coverage metrics are
  computable for all Pilot cells (per §9, C5).

If any of T1–T5 fails, Pilot-2 is **not** started. The failure
is recorded, and the scope is revised.

The transition condition is checked **before** Pilot-2 runs.
It is not adjusted after Pilot-2 results are seen.

---

## 12. Mock / HeMAC boundary

**No Mock result is used to calibrate any threshold.**

- If Pilot-1 and Pilot-2 run on HeMAC, the procedures in §5–§9
  apply as written.
- If Pilot runs on MockAdapter, the procedures in §5–§9 do not
  apply. Mock results are used only to test the pipeline
  (Item 1.0), not to estimate any threshold.
- No threshold in `preregistration/thresholds.md` is filled from
  Mock data.

This boundary is not negotiable. Violating it would convert an
integration test into a calibration step without disclosure.

### 12.1 Data separation mechanism

Pilot and Confirmatory data are separated by six mechanisms.

**1. Directory separation.**

`results/pilot/` and `results/confirmatory/` are distinct
directories. Confirmatory scripts do not read from
`results/pilot/`.

**2. Filename prefix.**

Every Pilot file is prefixed with `pilot_`. Every Confirmatory
file is prefixed with `confirm_`. This is checked at file
creation and before Confirmatory Evaluation.

**3. Checksums.**

Every output file is hashed (SHA-256) at creation. The hash is
recorded in `results/RUN_LOG.md`.

**4. Provenance record.**

Every entry in `results/RUN_LOG.md` records not only the file
path and hash, but also:

- the input files used to produce the output,
- the configuration file(s) used,
- the code version (git commit or equivalent),
- the run_id.

A checksum proves file identity. It does not prove provenance.
The provenance record is required.

**5. Frozen thresholds with version tag.**

`preregistration/thresholds.md` contains, for each threshold:

- the value,
- the date it was frozen,
- a version tag,
- a SHA-256 hash of the frozen file.

Before Confirmatory Evaluation begins, a check verifies that
the file being read matches the frozen hash. If the file has
changed, the check fails and Confirmatory does not start.

**6. Seed separation with explicit exceptions.**

Seeds are not automatically forbidden from being shared between
Pilot and Confirmatory. A shared seed is permitted if it is
declared in advance for a specific purpose (e.g., a replication
comparison).

What is forbidden is an **undeclared** overlap. The verification
step checks that:

- every Confirmatory seed is either from a separate seed pool,
  or is declared in `preregistration/thresholds.md` as a
  shared seed with a stated purpose.

The check does not mechanically forbid sharing. It mechanically
detects undeclared sharing.

### 12.2 Verification procedure

Before Confirmatory Evaluation begins, a verification script
checks:

- **V1.** No Confirmatory file has a `pilot_` prefix.
- **V2.** No Confirmatory file is located in `results/pilot/`.
- **V3.** No Confirmatory script reads from `results/pilot/` —
  including indirect reads via configuration files, intermediate
  data, or paths built at runtime.
- **V4.** Every Confirmatory seed is either from a separate pool
  or declared as a shared seed in `preregistration/thresholds.md`.
- **V5.** The hash of `preregistration/thresholds.md` matches
  the frozen hash.
- **V6.** Every Confirmatory output file has a corresponding
  provenance entry in `results/RUN_LOG.md`.

If any check fails, Confirmatory Evaluation does not start. The
failure is recorded in `docs/decisions.md`.

### 12.3 What this does not prevent

- A human can still copy a Pilot file to the Confirmatory
  directory. The mechanism does not prevent deliberate
  violation; it makes accidental or undeclared violation
  detectable.

- The mechanism does not certify that the calibration values in
  `preregistration/thresholds.md` were actually derived from
  Pilot-2. It certifies that the Confirmatory runs did not
  directly access Pilot data, and that the frozen file is the
  one that was reviewed.

- The mechanism does not make Pilot and Confirmatory
  independent in a statistical sense. Calibration values
  derived from Pilot are used in Confirmatory by design. What
  is prevented is undeclared access, not declared transfer.

### 12.4 Status of this mechanism

**Status:** DOCUMENTED (2026-11-25). Not yet implemented.

R6 remains **OPEN** until:

- the verification script is written,
- the verification procedure is tested on synthetic data,
- the result of the test is recorded in
  `docs/decisions.md`.

---

## 13. Freeze conditions

Thresholds are frozen in Item 1.3 when:

- Pilot-2 is complete.
- All thresholds in §5–§9 have been calibrated and reported
  with uncertainty.
- `preregistration/thresholds.md` contains the final values
  with date and version tag.
- `docs/decisions.md` contains the calibration entry with the
  pilot statistic that justified each value.

After freeze, no threshold changes without a documented
amendment and a new version of `preregistration/thresholds.md`.

---

## 14. Non-claims

- This document does not set final thresholds.
- This document does not authorize Confirmatory Evaluation.
- The provisional values (ε = 0.05, τ_min = 0.70, k = 3) are
  not scientific claims. They are starting points for Pilot.
- The calibration rules are design choices, not statistical
  facts.
- No Mock result is a calibration result.

---

## 15. Decision record — Item 1.2 (DRAFT)

**Status:** DRAFT. To be reviewed before Pilot-1 runs.

- Date: 2026-11-25
- Provisional values: ε = 0.05, τ_min = 0.70, k = 3
- ESS threshold: 10th percentile of baseline, hierarchical
  bootstrap CI
- Support Overlap threshold: 10th percentile of baseline,
  hierarchical bootstrap CI
- Distributional Distance threshold: 90th percentile of baseline,
  hierarchical bootstrap CI; distance chosen per §7.2
- ε calibration rule: 1.5 × pilot baseline selection regret
- τ_min calibration rule: 0.70, lowered to 5th percentile only
  if needed
- Transition condition: §11, checked before Pilot-2
- Mock/HeMAC boundary: §12, not negotiable
- Freeze condition: §13, in Item 1.3
- Preregistration impact: calibration procedure is recorded
  before Pilot-1; final values recorded before Confirmatory.
