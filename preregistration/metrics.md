# Metrics

**Status:** Item 0.4 (Coverage Metric) — CLOSED at design level (2026-11-23).
**Item 0.8 (Statistical Plan) — OPEN.** This file will be extended
when Item 0.8 is addressed.
**Date:** 2026-11-23
**Related:** `design/policy_set.md` §7.2; `design/baselines.md` §4;
`docs/decisions.md`.

---

## Part A — Coverage (Item 0.4)

### A.1 Purpose

Coverage metrics tell us whether the logged data support a defensible
evaluation of the target policy under a given structural
configuration. They do not replace OPE. They bound the interpretation
of OPE results.

If the target policy is outside the behavioral or structural support
of the logged data, an OPE failure may be attributable to lack of
support, not to structural shift. Without coverage metrics, the two
cannot be distinguished.

### A.2 Position on combining metrics

Coverage is reported as **three independent dimensions**. They are
**not** combined into a single index.

| Metric | What it measures |
|---|---|
| Importance-Weight Effective Sample Size (ESS) | Quality of the importance weights; effective sample size |
| Support Overlap | Existence of behavioral support for the target policy |
| Distributional Distance | Divergence between logged and target behavior distributions |

A high value on one dimension does **not** compensate for a low value
on another. Coverage is considered adequate only when all three
dimensions pass their (pilot-dependent) thresholds.

### A.3 Two distinct kinds of coverage

Coverage is evaluated on two axes.

#### A.3.1 Behavioral Coverage

Does the logged data support the **actions and behaviors** of the
target policy?

- Evaluated on the action distribution and, where applicable, on the
  state-action visitation distribution.
- Fails when the target policy takes actions that are not represented
  (or are severely underrepresented) in the logged data.

#### A.3.2 Structural Coverage

Does the logged data represent the **team structure and communication
structure** present in the evaluation environment?

- Evaluated on the (T, C) cell labels defined in
  `design/scenarios.md` and on their observable proxies (e.g., agent
  presence, communication graph structure).
- Fails when the evaluation configuration (T_k, C_l) is not
  represented in the logged data.

Behavioral Coverage and Structural Coverage are reported separately.
Neither is folded into the other.

This distinction is specific to StructOPE. Structural shift is the
object of study; treating structural coverage as part of behavioral
coverage would make the failure mode we are testing invisible.

### A.4 Definitions and computation spaces

The following are fixed at the design level. Numerical thresholds are
**PILOT-DEPENDENT** (§A.6). The distributions and spaces on which
each metric is computed are declared here so that no number is
reported without a clear interpretation.

#### A.4.1 Importance-Weight Effective Sample Size (ESS)

- **Definition:** ESS = (Σ w_i)² / Σ w_i², where w_i is the
  importance weight of the i-th logged transition under the target
  policy.
- **Space:** computed over the logged dataset used by the estimator
  (per-agent for B1a/B1b; joint for B2).
- **Normalized ESS:** ESS / N, where N is the number of logged
  transitions in the relevant dataset. Reported alongside ESS.
- **Interpretation:** low normalized ESS indicates that a small
  fraction of the data dominates the estimate. It does not, by
  itself, prove the estimate is wrong; it bounds how much of the
  data is contributing.

#### A.4.2 Support Overlap

- **Definition:** the fraction of target-policy action samples that
  fall in the support (or a defined ε-neighborhood of the support)
  of the logged action distribution, per state (or per joint state
  for B2).
- **Space:** action space (per-agent) for B1a/B1b; joint action space
  for B2. The joint action space must be enumerated or approximated;
  the approximation is recorded in `preregistration/thresholds.md`.
- **ε-neighborhood:** required for continuous action spaces; ε is
  pilot-dependent and recorded in `preregistration/thresholds.md`.
- **Interpretation:** low overlap indicates that the target policy
  visits actions that the logged data does not cover. The estimate
  is then an extrapolation.

#### A.4.3 Distributional Distance

- **Definition:** a distance between the logged behavior distribution
  and the target policy's action distribution, per state (or per
  joint state for B2).
- **Distance choice:** the distance is **not** fixed at the design
  level. Candidates include KL divergence, MMD, and total variation.
  The choice depends on the representability of the relevant
  distribution in HeMAC (discrete vs. continuous, per-agent vs.
  joint). The chosen distance(s) must be recorded in
  `preregistration/thresholds.md` before any confirmatory experiment.
- **Space:** as in §A.4.2.
- **Interpretation:** the distance quantifies how far the target
  behavior is from the logged behavior. It does not by itself say
  whether the target policy can be evaluated; it says how much
  extrapolation the estimate requires.

#### A.4.4 What is not assumed about KL / MMD

The design does **not** assume that KL or MMD is directly applicable
to all HeMAC representations. Before either is used:

- the distribution to be compared must be specified (per-agent
  action distribution, joint action distribution, state-action
  visitation distribution),
- the space on which it lives must be specified (discrete,
  continuous, mixed),
- the estimator of the distance must be specified.

If a distance cannot be defined meaningfully on the relevant space,
it is not reported. Reporting a number without a defined space is
prohibited.

### A.5 Structural coverage is reported as a cell map

Structural Coverage is reported as a table over (T, C) cells:

| (T_k, C_l) | In logged data? | Behavioral Coverage | Structural Coverage |
|---|---|---|---|
| ... | yes / no | high / medium / low | high / medium / low |

This table is produced for each (policy set × evaluation scenario)
combination. It is part of the descriptive results, not the
confirmatory test.

### A.6 Thresholds are PILOT-DEPENDENT

Numeric thresholds for ESS, Support Overlap, and Distributional
Distance are **not fixed at the design level**. They are determined
in the pilot stage and recorded in `preregistration/thresholds.md`
before any confirmatory experiment.

Until then, the metrics are reported descriptively.

### A.7 Coverage classifies; it does not exclude

Coverage metrics are used to **classify and interpret** OPE results,
not to exclude difficult cases from the confirmatory analysis.

Specifically:

- A low-coverage cell is **not** removed from the confirmatory
  analysis.
- It is **flagged** in the results table.
- The interpretation of an OPE failure in that cell distinguishes
  between (i) failure attributable to weak support and (ii) failure
  attributable to structural shift.

Excluding low-coverage cells would remove exactly the cases
StructOPE exists to test.

### A.8 How coverage enters the evaluation

- **B1a, B1b, B2, B3a:** coverage metrics are computed on the
  logged data used by the estimator, per scenario.
- **B3b:** coverage is computed only if B3b is included (Item 0.2,
  §4).
- **B4:** coverage does not apply to the reference evaluation; B4 is
  a direct execution. Coverage of the OPE data relative to B4 is
  reported descriptively.

Coverage metrics are **not** used as a filtering criterion at any
stage.

### A.9 Non-claims

- StructOPE does not claim that the three coverage metrics are
  sufficient to guarantee valid OPE.
- StructOPE does not claim that a high ESS, high overlap, or small
  distributional distance implies accurate evaluation.
- StructOPE does not claim that a low-coverage cell produces a wrong
  estimate; it claims that the estimate cannot be interpreted
  without acknowledging the coverage limitation.
- StructOPE does not fix numerical thresholds at the design level.

### A.10 Decision record — Item 0.4

- **Date:** 2026-11-23
- **Item 0.4 status:** CLOSED at design level.
- **Metrics:** ESS, Support Overlap, Distributional Distance —
  reported independently, not combined.
- **Coverage axes:** Behavioral Coverage and Structural Coverage,
  reported separately.
- **Thresholds:** PILOT-DEPENDENT; recorded in
  `preregistration/thresholds.md`.
- **Use:** classifies and interprets OPE results; does not exclude
  cells.
- **Distance choice:** not fixed; chosen per HeMAC representation and
  recorded before confirmatory experiments.
- **Preregistration impact:** metrics, spaces, thresholds, and
  distance choices recorded in `preregistration/`.

---


## Part B — Statistical Plan (Item 0.8)

**Status:** Item 0.8 CLOSED at design level (2026-11-23).
**Date:** 2026-11-23
**Related:** `design/scenarios.md` §Part C; `design/policy_set.md`;
Part A of this file; `docs/decisions.md`.

---

### B.1 Purpose

This part fixes the pre-registered statistical plan for the
confirmatory evaluation. It specifies:

- ranking-fidelity metrics,
- selection-regret metrics,
- treatment of rank-ambiguous policies,
- multiple-comparison correction,
- eligibility rules for coverage-conditioned analysis.

It does **not** fix numeric thresholds (PILOT-DEPENDENT, see Part A
§A.6) and does **not** fix the value of k for Top-k accuracy
(PILOT-DEPENDENT, see §B.2.3). Both must be recorded in
`preregistration/thresholds.md` before any confirmatory experiment.

---

### B.2 Ranking-fidelity metrics

Three metrics are pre-registered.

#### B.2.1 Spearman's rho

- **Definition:** rank correlation between the OPE-estimated policy
  ranking and the reference (B4) policy ranking.
- **Computed over:** the set of policies in the Full Policy Set,
  excluding rank-ambiguous policies (§B.4).
- **Reported with:** a bootstrap confidence interval over (T, C)
  cells.
- **Not used as:** the sole indicator of ranking fidelity.

#### B.2.2 Kendall's tau

- **Definition:** pairwise rank agreement between the OPE-estimated
  ranking and the reference ranking.
- **Computed over:** the same policy set as Spearman's rho.
- **Reported with:** a bootstrap confidence interval.
- **Not used as:** the sole indicator of ranking fidelity.

Spearman's rho and Kendall's tau are reported together. A
discrepancy between them is informative and is reported, not
resolved.

#### B.2.3 Top-k ranking accuracy

- **Definition:** the fraction of the top-k policies in the
  reference (B4) ranking that also appear in the top-k of the
  OPE-estimated ranking.
- **k value:** PILOT-DEPENDENT. Recorded in
  `preregistration/thresholds.md` before any confirmatory
  experiment. k is not chosen on the basis of confirmatory
  results.
- **Computed over:** the set of eligible policies (§B.5).
- **Not used as:** a replacement for Spearman's rho or Kendall's
  tau.

---

### B.3 Selection-regret metrics

Two selection-regret metrics are pre-registered.

#### B.3.1 Coverage-conditioned Selection Regret (primary)

- **Definition:**

```

Regret_eligible =
Best_B4_Utility(Eligible_Policies)
- Selected_OPE_Policy_Utility

```

- **What it measures:** the quality of policy selection **inside
  the coverage-acceptable range**.
- **Eligibility:** fixed pre-registration (§B.5). Not adjusted after
  observing results.
- **What it does not measure:** the cost of failing to select the
  best policy in the full set.

#### B.3.2 Full-set Selection Regret (secondary)

- **Definition:**

```

Regret_full =
Best_B4_Utility(All_Policies)
- Selected_OPE_Policy_Utility

```

- **What it measures:** the cost of being unable to select the best
  policy available in the full set, regardless of coverage.
- **Relationship to B.3.1:** `Regret_full >= Regret_eligible`. The
  difference is the cost of coverage restriction. It is reported
  descriptively, not as a confirmatory test.

#### B.3.3 Why two metrics

Restricting comparison to eligible policies alone would hide
failures caused by the policy set itself (e.g., the best policy
being outside the coverage range). Reporting only the full-set
regret would overstate the failure of OPE when the best policy is
unreachable by construction. Both are reported; neither is
collapsed into the other.

---

### B.4 Rank-ambiguous policies

A policy is **rank-ambiguous** in a given (T, C) cell when its B4
utility interval overlaps with another policy's B4 utility interval
(per `design/scenarios.md` §Part C).

Handling:

- **Excluded from:** Spearman's rho, Kendall's tau, Top-k accuracy.
- **Retained in:** both selection-regret metrics (B.3.1, B.3.2),
  with the ambiguity flagged in the results table.
- **Reported in:** a dedicated table per (T, C) cell listing the
  rank-ambiguous policies and the uncertainty in their ordering.

Rank ambiguity is **not** silently resolved into a success or
failure. It is reported as a property of the scenario.

---

### B.5 Eligibility rules

Eligibility for the coverage-conditioned analysis (§B.3.1) is
fixed **before** the confirmatory evaluation.

#### B.5.1 Definition of eligible policy

A policy is eligible in a (T, C) cell when all three coverage
dimensions (Part A §A.2) pass their pilot-fixed thresholds for
that cell:

- Importance-Weight ESS above the pilot threshold,
- Support Overlap above the pilot threshold,
- Distributional Distance below the pilot threshold.

The thresholds are recorded in `preregistration/thresholds.md`
before any confirmatory experiment.

#### B.5.2 If no policy is eligible in a cell

- `Regret_eligible` is **not defined** for that cell.
- `Regret_full` is reported for that cell as a descriptive
  secondary metric.
- The cell is flagged as **coverage-ineligible**.
- The cell is **not** removed from the analysis; it is reported as
  a case in which the OPE estimate cannot be conditioned on
  coverage.

#### B.5.3 If the selected policy is not eligible

- `Regret_eligible` is reported as a defined positive value (the
  gap between the best eligible policy and the selected policy),
  not as undefined. This is intentional: selecting an ineligible
  policy is a failure mode that must be recorded, not hidden.
- The cell is flagged as **selection outside coverage**.

#### B.5.4 Eligibility is not an exclusion criterion

A policy that is ineligible in one cell may be eligible in another.
Eligibility is cell-specific. It is not used to remove policies
from the Full Policy Set.

---

### B.6 Multiple-comparison correction

Two regimes are pre-registered.

| Analysis regime | Correction |
|---|---|
| Confirmatory | Bonferroni |
| Exploratory / Pilot | Benjamini-Hochberg (FDR) |

#### B.6.1 Family of confirmatory tests

The family of confirmatory tests is fixed before the confirmatory
evaluation. It includes, per (T, C) cell:

- Spearman's rho test (B.2.1),
- Kendall's tau test (B.2.2),
- Top-k accuracy test (B.2.3),
- Coverage-conditioned selection-regret comparison (B.3.1).

`Regret_full` (B.3.2) is reported descriptively and is **not** part
of the Bonferroni family.

The family size is reported alongside the corrected p-values.

#### B.6.2 No post-hoc adjustment

Correction is applied to the pre-registered family. It is not
applied selectively after results are seen. If an additional
analysis is added after the pre-registration, it is labeled
**exploratory** and does not enter the confirmatory family.

---

### B.7 What is not fixed in this part

- **Numeric thresholds** for coverage (Part A §A.6) and for
  ranking-fidelity / regret acceptance. PILOT-DEPENDENT.
- **k** in Top-k accuracy (B.2.3). PILOT-DEPENDENT.
- **The number of bootstrap resamples** for confidence intervals.
  PILOT-DEPENDENT.
- **The precise eligibility threshold values**. PILOT-DEPENDENT.

All of these are recorded in `preregistration/thresholds.md` before
the confirmatory evaluation.

---

### B.8 What this part does not do

- It does not define pass or fail thresholds. Those are fixed in
  `preregistration/thresholds.md`.
- It does not choose the OPE estimator or the baselines. Those are
  fixed in `design/baselines.md`.
- It does not select the policy set. That is fixed in
  `design/policy_set.md`.
- It does not replace the pilot. Pilot results are labeled
  exploratory and do not enter the confirmatory family.

---

### B.9 Non-claims

- StructOPE does not claim that Spearman's rho, Kendall's tau, and
  Top-k accuracy exhaust ranking fidelity.
- StructOPE does not claim that `Regret_eligible` and
  `Regret_full` measure the same thing.
- StructOPE does not claim that rank-ambiguous policies are
  unimportant; it claims that their ordering cannot be treated as a
  resolved fact.
- StructOPE does not claim that Bonferroni is the only defensible
  correction; it claims that the correction is pre-registered.

---

### B.10 Decision record — Item 0.8

- **Date:** 2026-11-23
- **Item 0.8 status:** CLOSED at design level.
- **Ranking fidelity:** Spearman's rho + Kendall's tau + Top-k
  accuracy. k is PILOT-DEPENDENT.
- **Selection regret:** two metrics.
  `Regret_eligible` (coverage-conditioned, primary) and
  `Regret_full` (full-set, secondary).
- **Rank-ambiguous policies:** excluded from ranking metrics,
  retained in regret metrics, reported separately.
- **Multiple comparisons:** Bonferroni for confirmatory family;
  Benjamini-Hochberg for exploratory/Pilot.
- **Eligibility rules:** fixed before confirmatory evaluation.
  No-eligible-policy and ineligible-selection cases are reported,
  not excluded.
- **Preregistration impact:** all PILOT-DEPENDENT quantities
  recorded in `preregistration/thresholds.md` before confirmatory
  experiments.
