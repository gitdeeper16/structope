# Implementation Checklist — Decision and Acceptance Gate

**Status:** Draft for review
**Version:** 0.1
**Purpose:** Gate document. OPE implementation may not start until all
Pre-Implementation items marked "Blocking" are resolved and their
acceptance criteria are met.

**Reading key for Decision Status:**
- DECIDED — resolved, recorded in this document or a linked file.
- OPEN — decision required before the relevant stage; selection
  criteria must be documented here, not chosen ad hoc.
- PILOT-DEPENDENT — cannot be resolved without pilot data; must be
  preregistered as such.
- BLOCKING — implementation of the dependent stage may not begin
  until this item is closed.

**Rule:** An item is "closed" only when (a) a decision is recorded,
(b) the acceptance criterion is met, and (c) the evidence is stored
in the repository at the path given. Verbal agreement is not closure.

---

## Phase 0 — Pre-Implementation

### Item 0.1 — Utility Function and Weights

**Decision status:** CLOSED (2026-11-25). See `design/utility.md`.
**Why blocking:** Regret@k, ε, and AUROC wrong-ranking events all
depend on the scalar utility. If the utility changes after
confirmatory evaluation begins, every metric loses preregistered
meaning.

**Selection criteria (to be documented, not yet chosen):**
- Must combine at least task success and one resource dimension.
- Weights must be justified by operational relevance, not by
  producing favorable results for any OPE method.
- Must state whether the utility is linear or nonlinear in components.
- Must state the range used for normalization.

**Acceptance criterion:**
- A written utility definition exists in `design/utility.md`, with
  weights, normalization, and at least one sensitivity check
  planned.
- At least two alternative weightings are listed as secondary
  analyses, not as primary.

**Evidence required:** `design/utility.md`, plus a decision entry in
`docs/decisions.md`.

---

### Item 0.2 — Baseline OPE Estimator Selection

**Decision status:** CLOSED (2026-11-23). See `preregistration/metrics.md` Part B.
**Why blocking:** B2 (conventional multi-agent OPE) cannot be
compared against B3 and B4 unless its assumptions, supported policy
class, and adaptation from the original are documented. Otherwise
results reflect the adaptation, not the method.

**Selection criteria:**
- Must be applicable to cooperative multi-agent data, not only
  single-agent or two-player zero-sum.
- Must have a documented assumption set against which violations
  under structural shift can be assessed.
- Must be replicable from its published description alone.

**Candidate references (not final choices):**
- AAMAS 2021 Exploitability OPE (two-player zero-sum; applicability
  to cooperative N-agent must be argued, not assumed).
- A single-agent OPE adapted to multi-agent via agent-level or
  joint-action treatment; adaptation must be documented.

**Acceptance criterion:**
- `design/baselines.md` contains, for each baseline:
  - Original paper reference.
  - Assumption list.
  - Deviation table (original → StructOPE setting).
  - Expected failure modes under team-composition and communication
    shift.
- Any baseline that cannot be adapted without changing its core
  assumptions is marked as "reference only" and excluded from the
  primary comparison.

**Evidence required:** `design/baselines.md`, decision entry.

---


### Item 0.2a — Reward Scope in B1

**Decision status:** CLOSED (2026-11-23). See `preregistration/metrics.md` Part B.§4, §8.
**Why blocking:** B1a (local reward) and B1b (shared reward) are the
only way to isolate the effect of reward definition from the effect of
centralized representation in B2. Without this distinction, a
B1↔B2 comparison would confound reward scope with representation.
**Resolution:**
- B1a: local reward, sensitivity analysis.
- B1b: shared reward, sensitivity analysis.
- Technical acceptance condition: a meaningful local reward must exist
  in HeMAC. If not, B1a is documented as unavailable; B1b is retained
  without any local-performance claim.
**Evidence:** `design/baselines.md` §4.

### Item 0.3 — Training Strategy for Structural Shift

**Decision status:** CLOSED (2026-11-25). See `design/utility.md`.
**Why blocking:** The meaning of H1 and H4 depends on what the
evaluation model saw during training. Two distinct strategies:

- **Strategy A — Train on T0/C0 only.** Model is trained on baseline
  data. All structural shifts are test-time. This measures
  generalization to unseen structure, but conflates evaluation
  failure with generalization failure.
- **Strategy B — Train on a subset of shifts.** Model is trained on
  some T and C conditions and tested on held-out ones. This measures
  generalization across shifts and supports H4 more directly.

**Selection criteria:**
- The strategy must be justified against the research question in
  Section 1 of PROTOCOL.md.
- The split between training-visible and test-only shifts must be
  documented before any model training.
- In either strategy, at least one full (T, C) combination must be
  withheld from training.

**Acceptance criterion:**
- `design/scenarios.md` specifies:
  - Which T levels and C levels are training-visible.
  - Which are test-only.
  - Which combined (T, C) cells are withheld entirely.
- The split is stated in a form that can be copied verbatim into the
  preregistration document.

**Evidence required:** `design/scenarios.md`, decision entry.

---

### Item 0.4 — Dataset Coverage Metric

**Decision status:** CLOSED (2026-11-23). See `design/scenarios.md` Part C.  
**Implementation status:** PARTIAL — 0.5a (design spec) COMPLETE 2026-11-25. 0.5b (implementation) and 0.5c (determinism test) DEFERRED until HeMAC. See `design/fault_injection.md`.
**Why it matters:** H1 (ranking degradation under shift) is only
interpretable if coverage is quantified. Without a coverage metric,
a low Spearman score under shift can be attributed to either shift
or to insufficient offline data.

**Selection criteria (to be chosen, not fixed here):**
- Must be computable from the offline dataset alone.
- Must be comparable across policy pairs, not only per policy.
- Must have a documented interpretation limit: it measures coverage,
  not validity.

**Candidate metrics (not final):** effective sample size per target
policy; support overlap between behavior and target policies;
proportion of (state, action) pairs within the behavior support.

**Acceptance criterion:**
- `preregistration/metrics.md` contains the chosen coverage metric
  with formula and interpretation.
- The metric is reported for every (behavior policy, target policy)
  pair in the dataset description.

**Evidence required:** `preregistration/metrics.md` entry.

---

### Item 0.5 — Fault Injection Requirements for HeMAC

**Decision status:** CLOSED (2026-11-23). See `design/scenarios.md` Part C.
**Why it matters:** HeMAC does not ship with a fault-injection layer
for team-composition and communication shift. The added layer must
be specified before any dataset collection.

**Requirements to specify:**
- Team-composition injection: dropout, capability degradation,
  replacement, team-size change. For each: trigger mechanism,
  severity levels, and whether it applies before, during, or
  between episodes.
- Communication injection: packet loss, delay, partition, topology
  change. For each: physical-layer model, parameter range, and
  determinism under seed.
- Severity parameter ranges for mild/moderate/severe, initially as
  ranges, not fixed values.
- A determinism guarantee: same seed → same injected faults.

**Acceptance criterion:**
- `design/fault_injection.md` documents each injection type with
  trigger, severity range, and seed behavior.
- The implementation (once written) passes a determinism test:
  repeated runs with the same seed produce identical fault
  sequences.
- A note in `docs/decisions.md` states whether HeMAC modifications
  are invasive (patch) or additive (wrapper).

**Evidence required:** `design/fault_injection.md`, determinism test
log in `results/logs/`.

---

### Item 0.6 — Candidate Policy Set Acceptance

**Decision status:** CLOSED (2026-11-23). See `design/scenarios.md` Part C.
**Why it matters:** The policy set is a controlled variable. If it
is too easy, ranking is trivial; if too hard, Stage 1 cannot pass
for reasons unrelated to OPE. The set must be accepted before any
OPE method is run on it.

**Acceptance criteria (all must hold):**
- Size: 8–12 policies, or a documented justification for a
  different size.
- Diversity: at least three distinct coordination strategies
  represented.
- Nontrivial performance spread: baseline utility range across
  policies is documented and is not dominated by a single policy.
- At least two policies that are expected to invert ranking under
  at least one structural shift (based on design reasoning, not on
  pilot outcomes).
- Deliberately fragile policies present and labeled as such.
- The same policy set is used across all stages; any change requires
  a version bump and a documented justification.

**Acceptance criterion:**
- `design/policy_set.md` contains the policy list with:
  - Coordination strategy description.
  - Communication requirements.
  - Resource profile.
  - Expected fragility or robustness under shift.
  - Version tag.
- A peer-review note records that the diversity criteria above were
  checked.

**Evidence required:** `design/policy_set.md`, review note in
`docs/decisions.md`.

---

### Item 0.7 — Reference Execution Protocol

**Decision status:** CLOSED (2026-11-23). See `design/scenarios.md` Part C.
**Why it matters:** The reference simulator is the source of truth
for ranking. Its variance must be characterized before it can be
used to define "wrong ranking".

**Requirements:**
- Each candidate policy × scenario × seed executed more than once.
- Between-seed and within-scenario variance reported.
- Reference ranking is reported with an uncertainty interval, not
  as a point ranking.

**Acceptance criterion:**
- `design/scenarios.md` states the number of repeated executions
  per (policy, scenario) before confirmatory evaluation.
- Pilot output includes a table of reference ranking intervals.
- Policies whose reference rankings are not separable within their
  intervals are flagged and excluded from ranking-fidelity claims
  for that scenario.

**Evidence required:** pilot reference table in
`results/tables/`, plus a preregistered note in
`preregistration/hypotheses.md`.

---

### Item 0.8 — Statistical Analysis Plan

**Decision status:** CLOSED (2026-11-23). See `preregistration/metrics.md` Part B.
**Why blocking:** The analysis method (paired resampling,
cluster-aware bootstrap, multiple-comparison correction) determines
what counts as evidence. Choosing it after seeing results is not
permitted.

**Requirements to preregister:**
- Resampling unit (environment seed vs. scenario seed).
- Bootstrap or permutation procedure.
- Multiple-comparison correction strategy.
- Minimum practically relevant effect size.
- Interpretation rule: a numerical difference in Spearman or Tau is
  not evidence unless it exceeds the preregistered effect-size
  threshold with its interval.

**Acceptance criterion:**
- `preregistration/metrics.md` and `preregistration/hypotheses.md`
  contain the full analysis plan.
- A dry-run analysis on synthetic data confirms the pipeline runs
  end-to-end before real data is used.

**Evidence required:** analysis script in `src/eval/`, dry-run log
in `results/logs/`.

---

## Phase 1 — Pilot

The pilot is a separate, bounded stage. Its purpose is to estimate
variance and calibrate thresholds, not to test hypotheses.

### Item 1.0 — Pipeline Integration Test

**Decision status:** CLOSED (2026-11-25).
**Why it matters:** Before any Pilot can run, the four core
components (EnvironmentInterface, MockAdapter, StateBuilder,
RewardLogger) must be shown to work together end-to-end.
Without this, a Pilot failure could be attributed to integration
problems rather than to the research question.
**What was verified:**
- All four components integrate without modification.
- 29 MockAdapter unit tests pass after the energy-consumption
  extension.
- 17 EnvironmentInterface tests pass.
- 4 StateBuilder tests pass.
- 7 RewardLogger tests pass.
- 9 Pipeline Test tests pass.
- CSV and LOG consistency verified: 2 rows (n_steps=10, 50),
  formula U = s*(0.5+0.5*(1-E_norm)) holds to 1e-9,
  mock_label=MOCK-PROVISIONAL.
**Boundaries:**
- Mock only. Not a HeMAC measurement.
- Not evidence of OPE validity.
- Not used to update scientific thresholds.
- Fault Injection (Item 0.5) not exercised.
**Evidence:** experiments/phase1_baseline/pipeline_test.py,
tests/test_pipeline_test.py, results/tables/pipeline_test_mock.csv,
results/logs/pipeline_test_mock.log.

---

### Item 1.1 — Pilot Scope

**Decision status:** DRAFT (2026-11-25). See `preregistration/threshold_calibration.md`.
**Requirements:**
- Pilot uses a strict subset of scenarios and a strict subset of
  policies, documented before running.
- Pilot execution count is bounded and recorded.
- Pilot data are stored in a separate directory (`results/pilot/`)
  and are not merged into confirmatory data.

**Acceptance criterion:**
- Pilot subset and count are preregistered in `preregistration/`.
- A file `results/pilot/MANIFEST.md` lists all pilot runs.

---

### Item 1.2 — Threshold Calibration

**Decision status:** DRAFT (2026-11-25). See `preregistration/threshold_calibration.md`.
**Requirements:**
- ε and τ_min are updated from pilot variance estimates.
- The update rule must be preregistered before the pilot: e.g.,
  "ε = 1.5 × observed pilot selection regret under baseline" or a
  similar rule, not an outcome-driven adjustment.
- Final values are frozen before confirmatory evaluation.

**Acceptance criterion:**
- `preregistration/thresholds.md` contains:
  - Initial values (ε = 0.05, τ_min = 0.70).
  - The preregistered update rule.
  - Final frozen values with date and version tag.
- Any change from initial values is accompanied by the pilot
  statistic that justified it.

---

### Item 1.3 — Sample-Size Determination

**Decision status:** DRAFT (2026-11-25). See `preregistration/threshold_calibration.md`.
**Requirements:**
- Power analysis based on pilot variance estimates.
- Number of seeds per confirmatory condition fixed from this
  analysis, not from the "30" planning target.
- If the required sample size is infeasible, the protocol must
  document the reduced scope explicitly, not silently lower the
  target.

**Acceptance criterion:**
- `preregistration/thresholds.md` contains the power analysis
  summary and the final seed count.
- A feasibility note in `docs/decisions.md` records whether the
  target is achievable.

---

## Phase 2 — Confirmatory Evaluation

### Item 2.1 — Preregistration Freeze

**Decision status:** BLOCKING for any confirmatory run.
**Acceptance criterion:**
- All items in Section 15 of PROTOCOL.md are frozen and committed.
- A git tag `prereg-v1.0` marks the freeze point.
- Any post-freeze change requires a new tag and an explicit
  "exploratory, not confirmatory" label on affected results.

---

### Item 2.2 — Data Isolation

**Decision status:** BLOCKING.
**Acceptance criterion:**
- Confirmatory runs write only to `results/confirmatory/`.
- Pilot data at `results/pilot/` are read-only from the
  confirmatory pipeline's perspective.
- A check in the analysis script refuses to run if pilot data are
  included in confirmatory input paths.

---

## Decision Log Requirements

Every OPEN item that becomes DECIDED must be recorded in
`docs/decisions.md` with:
- Date.
- Item reference (e.g., 0.2).
- Decision summary.
- Evidence path.
- Preregistration impact (none / new version / freeze update).

## Summary Table

| Item | Phase | Status | Blocking | Evidence file |
|---|---|---|---|---|
| 0.1 Utility | Pre-Impl | CLOSED | Yes | design/utility.md |
| 0.2 Baselines | Pre-Impl | CLOSED | Yes | design/baselines.md |
| 0.2a Reward scope in B1 | Pre-Impl | CLOSED (B1a conditional) | No | design/baselines.md |
| 0.3 Training strategy | Pre-Impl | CLOSED | Yes | design/scenarios.md |
| 0.4 Coverage metric | Pre-Impl | CLOSED (design level) | No | preregistration/metrics.md |
| 0.5 Fault injection | Pre-Impl | PARTIAL (0.5a done; 0.5b/0.5c deferred) | No | design/fault_injection.md |
| 0.6 Policy set | Pre-Impl | CLOSED (design level) | No | design/policy_set.md |
| 0.7 Reference protocol | Pre-Impl | CLOSED | No | design/scenarios.md |
| 0.8 Statistical plan | Pre-Impl | CLOSED (design level) | Yes | preregistration/metrics.md |
| 1.0 Pipeline integration | Pilot | CLOSED | No | experiments/phase1_baseline/ |
| 1.1 Pilot scope | Pilot | FROZEN | No | preregistration/pilot_scope.md |
| 1.2 Threshold calibration | Pilot | DRAFT | No | preregistration/threshold_calibration.md |
| 1.3 Sample size | Pilot | PILOT-DEP | No | preregistration/thresholds.md |
| 2.1 Preregistration freeze | Confirm | BLOCKING | Yes | git tag |
| 2.2 Data isolation | Confirm | BLOCKING | Yes | analysis script |
