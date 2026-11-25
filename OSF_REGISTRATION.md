# StructOPE: Off-Policy Evaluation under Structural Shift — A Pre-Registered Protocol for Auditing Estimator Rankings under Team-Composition and Communication Faults in Multi-Agent Environments

---

**Registration DOI:** [10.17605/OSF.IO/EZJKF](https://doi.org/10.17605/OSF.IO/EZJKF)
**Registration Type:** OSF Preregistration
**Registry:** OSF Registries
**Date Created:** Nov 25, 2026, 10:26 AM
**Date Registered:** Nov 25, 2026, 10:26 AM
**License:** CC-By Attribution 4.0 International
**Contributor:** Samir Baladi

---

## Data / Analytic Code / Materials / Papers / Supplements

The following files were attached to this registration:

- `README.md`
- `fig01_conceptual_framework.png`
- `fig02_pipeline_architecture.png`
- `StructOPE_Research_Paper_v1.0.0.pdf`

---

## Overview

### Research questions or hypotheses

This pre-registration describes a falsification-first protocol for auditing Off-Policy Evaluation (OPE) estimator rankings under structural shift in multi-agent environments. Six research questions are formulated as hypotheses of the protocol:

RQ1 — Ranking fidelity under structural shift.
Does the ranking fidelity of an OPE estimator change when the scenario changes from a baseline to a structurally shifted scenario? Falsification: if no estimator shows a statistically meaningful change in ranking fidelity under structural shift, RQ1 is not supported.

RQ2 — Coverage as explanatory factor.
Is a drop in ranking fidelity associated with loss of support (low coverage) more than with differences in behaviour among policies? Falsification: if fidelity drops are uncorrelated with coverage measures, RQ2 is not supported.

RQ3 — MMD separation of behaviour and exposure.
Do state-conditioned MMD distances (Gaussian RBF kernel, median-heuristic bandwidth) separate policies whose behaviour differs from policies that differ only in frequency of observation? Falsification: if MMD distances do not separate the two classes, RQ3 is not supported.

RQ4 — Threshold stability on held-out scenarios.
Are thresholds calibrated on the Pilot scenarios stable when applied to the held-out scenarios C3 and C4? Falsification: if calibrated thresholds produce out-of-range behaviour on held-out scenarios, RQ4 is not supported.

RQ5 — Sensitivity to zero-support threshold.
How sensitive are comparability decisions and conclusions to the zero-support threshold n_min (20, 30, 50)? Falsification: if conclusions are qualitatively invariant across the three values, RQ5's concern is reduced; if they flip, the choice of n_min is reported as a forking-path risk.

RQ6 — Determinism of fault injection.
Can the fault-injection design generate structural shift deterministically and in the intended severity ranges? Falsification: if repeated executions with the same seed produce different structural-shift outcomes, RQ6 is not supported.

Each question is stated so that the observed outcome would bear directly on it. No new OPE estimator is proposed; the protocol audits a fixed set (B1a, B1b, B2, B3a, B3b, B4). The question is ranking preservation, not performance gain.

### Foreknowledge of data or evidence

Authors have observed the data. The authors cannot certify meeting any of the levels above given prior access and observation of the data relevant to this analysis plan.

### Explanation of foreknowledge and managing unintended influences

The experiments described in this protocol (Pilot-1: 324 runs, Pilot-2: 540 runs, Confirmatory: 432 runs) have been executed. The authors have observed the resulting data. This is therefore a retrospective registration of a pre-registered protocol.

To reduce the risk of unintended influences on analysis decisions, the following measures were taken:

1. The R7 decision (comparison unit = state-conditioned action distributions p(a|s); distance = MMD with Gaussian RBF kernel) was frozen before Pilot-2 and pinned by a sha256 digest (4981d02a...927e77c).
2. The zero-support threshold n_min = 30 was fixed before Pilot-1, with a pre-specified sensitivity analysis at n_min = 20 and n_min = 50.
3. Pilot and Confirmatory stages were separated by construction: Pilot work is removable (dashed borders, trash icon in the architecture diagram), Confirmatory work is frozen (solid borders, lock icon). This separation was verified by verify_separation.py (V1–V7 checks).
4. 66 automated tests were run and passed before any result was reported.
5. The fault-injection design was specified as a taxonomy (8 types × 3 severity ranges × timing matrix = 24 cells) before implementation.
6. The utility specification (documented in the paper) bounds the effect of energy on rankings; this bound was derived from the definitions, not from the data.

No new OPE estimator is proposed. The protocol audits a fixed set (B1a, B1b, B2, B3a, B3b, B4) and reports ranking fidelity, regret, and coverage. The question is ranking preservation, not performance gain.

The repository (https://github.com/gitdeeper16/structope) and the pre-registration DOI (10.5281/zenodo.24473998) contain the full frozen specifications and the verification records.

---

## Research Design

### Study type

Simulation study: Using existing or synthetic data to assess performance of a model, mimic operation of an existing or proposed system, or predict possible outcomes in a controlled context. This may include demonstration of methods, many varieties of modeling, prediction of policy impacts, simulating behavior or outcomes in a population, and other designs.

### Intention for causal interpretation

No causal relationship inferred: This study is not intended to inform a causal relationship.

### Blinding of experimental treatments

No blinding is involved.

### Additional blinding during research or analysis

No traditional blinding is involved because StructOPE does not use human subjects, human coders, or human analysts during execution. All execution, measurement, and verification are automated. However, several structural safeguards are employed to remove unintended influences that could be introduced by foreknowledge of the design, thresholds, or outcomes. These safeguards are enforced by construction and by automated checks:

1. Pre-registered thresholds. The zero-support threshold n_min = 30 was fixed before Pilot-1. The sensitivity analysis at n_min = 20 and n_min = 50 was also pre-specified. The ranking-fidelity threshold tau_min = 0.70 and the calibration point epsilon* ≈ 1.95 were fixed before Pilot-2. These values are recorded in preregistration/thresholds.md and are not modified after execution.

2. Frozen R7 specification. The R7 decision (comparison unit = state-conditioned action distributions p(a|s); distance = MMD with Gaussian RBF kernel and median-heuristic bandwidth) was frozen before Pilot-2 and pinned by a sha256 digest (4981d02a...927e77c). Any change to the specification would be detectable by digest mismatch.

3. Pilot/Confirmatory separation. Pilot and Confirmatory stages are physically separated in the file system. Pilot results are stored in results/pilot/ (removable, dashed borders in the architecture diagram). Confirmatory results are stored in results/confirmatory/ (frozen, solid borders, lock icon). The separation is verified by verify_separation.py (checks V1–V7), which enforces, for example, that no confirmatory result exists before the freeze timestamp, and that pilot results cannot be copied into the confirmatory directory.

4. Automated test suite. 66 automated tests were written before any result was reported. These tests verify the separation invariants (V1–V7), the fault-injection determinism, the threshold values, and the MMD computation. Any attempt to modify a frozen value after execution would fail the test suite.

5. Seed and repeat control. Seeds (3) and repeats (3) were fixed before execution and recorded in the repository. Randomness is confined to the environment simulator (HeMAC) and is controlled by the fixed seed set. No seed was selected or discarded after observing outcomes.

6. No post-hoc threshold adjustment. No threshold was adjusted after observing the confirmatory results. The calibration of epsilon* used only Pilot-2 data. The confirmatory stage used the frozen thresholds as-is.

7. Analysis code separation. The analysis code that produces the ranking-fidelity metrics is separate from the code that produces the utility estimates. This separation is intended to reduce the risk that an analyst, knowing the estimated ranking, adjusts the utility computation in a way that changes the ranking.

8. Deterministic fault injection. The fault-injection implementation uses fixed seeds and deterministic schedules. The determinism test (part of the 66 automated tests) verifies that repeated executions with the same seed produce identical structural-shift outcomes.

9. Transparent reporting of failures. The protocol reports ranking violations, coverage failures, and support failures explicitly. A violation is recorded as a violation, not repaired or reinterpreted. The README and the paper record all such failures without editing.

These safeguards do not replace blinding in the traditional sense; they are structural and procedural controls that make unintended influences detectable and, in most cases, prevent them from affecting the reported results. The repository (https://github.com/gitdeeper16/structope) and the pre-registration DOI (10.5281/zenodo.24473998) contain the full verification records, including the 66 passing tests and the V1–V7 checks.

### Study design

StructOPE uses a simulation-based design in which a fixed set of coordination policies is evaluated by a fixed set of OPE estimators under structural shift. The environment is HeMAC (Heterogeneous Multi-Agent Challenge), with a Mock adapter used for development only.

Design factors (fully crossed):

1. Scenarios (6): S1, S2, S3, S4, S5, S6, including held-out structural cells C3 and C4.
2. Policies (6): P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M, P_DEGRADED.
3. Estimators (6): B1a, B1b, B2, B3a, B3b, B4.
4. Seeds (3): fixed seed set.
5. Repeats (3): fixed repeat set.

The design is between-subject (unpaired) at the level of (scenario, policy, seed, repeat) units: each unit generates a trajectory independently, and no unit shares a random seed with another. There is no counterbalancing because the design is fully crossed and each cell is executed independently.

Three execution stages are separated by construction:

- Pilot-1: 324 runs. Exploratory: thresholds are calibrated. Removable.
- Pilot-2: 540 runs. Exploratory: further calibration and sensitivity analysis (n_min = 20, 30, 50). Removable.
- Confirmatory: 432 runs. Frozen: thresholds are held fixed. Locked.

The separation is verified by verify_separation.py, which enforces checks V1–V7 on the file system (e.g., confirmatory results cannot exist before the freeze timestamp; pilot results are isolated in a separate directory).

Outcome measures per run:

- Ranking fidelity: Spearman rho, Kendall tau, top-k overlap, regret.
- Coverage: MMD distance with Gaussian RBF kernel (median-heuristic bandwidth); zero-support threshold n_min = 30.
- Support: fraction of comparable states under the U2 comparison unit (state-conditioned action distributions p(a|s)).

Structural shift is injected through a fault-injection taxonomy:

- Team composition faults: agent dropout, capability degradation, agent replacement, team-size change.
- Communication faults: packet loss, communication delay, network partition, topology change.

Each fault type is instantiated at three severity levels (mild, moderate, severe) and at three timing points (before, during, between), giving 24 cells per fault type in the implementation matrix.

No new OPE estimator is proposed. The protocol audits the six listed estimators and reports whether their rankings are preserved under structural shift, and whether loss of support explains any observed loss of fidelity.

No causal inference is attempted: the protocol measures association between structural shift and ranking fidelity, and documents where the data cannot support a comparison (low coverage).

**Attached:** `README.md`, `fig01_conceptual_framework.png`, `fig02_pipeline_architecture.png`, `StructOPE_Research_Paper_v1.0.0.pdf`

### Randomization

No randomization of subjects or treatments is performed. Seeds (3) and repeats (3) are fixed before execution and recorded in the repository. Randomness is confined to the environment simulator (HeMAC) and is controlled by the fixed seed set.

---

## Sampling

### Data collection procedures

StructOPE is a simulation-based study. No human subjects are involved; no recruiting, no eligibility criteria for participants, and no geographic sampling frame apply. "Data" in this study are trajectories generated by the HeMAC multi-agent environment (Heterogeneous Multi-Agent Challenge) under a fixed set of coordination policies, seeds, and structural-shift scenarios.

Data source and location:

- Environment: HeMAC (primary); Mock adapter used for development only, never for reported results.
- Repository: https://github.com/gitdeeper16/structope
- Data generation code: src/ope_estimators.py, src/mmd_distance.py, src/fault_injection.py
- Fault-injection specification: design/fault_injection.md

Generation procedure:

For each (scenario, policy, seed, repeat) unit, a trajectory is generated by the HeMAC environment. The unit is the atomic sampling unit. The four factors are fully crossed:

1. Scenarios (6): S1, S2, S3, S4, S5, S6. Scenarios S5 and S6 include the held-out structural cells C3 and C4.
2. Policies (6): P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M, P_DEGRADED.
3. Seeds (3): fixed before execution, recorded in preregistration/pilot_scope.md.
4. Repeats (3): fixed before execution, recorded in preregistration/pilot_scope.md.

Structural shift is injected deterministically through the fault-injection taxonomy:

- Team-composition faults: agent dropout, capability degradation, agent replacement, team-size change.
- Communication faults: packet loss, communication delay, network partition, topology change.

Each fault type is instantiated at three severity levels (mild, moderate, severe) and three timing points (before, during, between), giving 24 cells per fault type. Fault injection is deterministic under fixed seeds.

Stages and run counts:

- Pilot-1: 324 runs (exploratory; thresholds calibrated; removable).
- Pilot-2: 540 runs (exploratory; sensitivity analysis at n_min = 20, 30, 50; removable).
- Confirmatory: 432 runs (frozen; thresholds held fixed; locked).

Separation between Pilot and Confirmatory is enforced by verify_separation.py (checks V1–V7), which verifies that no confirmatory result exists before the freeze timestamp and that pilot results are stored separately.

Expected duration:

- Pilot-1: approximately 20 days.
- Pilot-2: approximately 25 days.
- Confirmatory: approximately 30 days.
- Total: approximately 75 days from Pilot-1 start to Confirmatory end, excluding analysis and writing time.

Data storage:

- results/pilot/ (removable; dashed borders in the architecture diagram).
- results/confirmatory/ (frozen; solid borders; lock icon).
- Raw trajectories, seed records, and fault-injection schedules are archived with each run.
- Verification records (66 passing tests, V1–V7 check outputs) are stored in the repository.

No data were collected from human participants. No personal data are generated or stored. No ethics approval is required for this study.

### Data collection procedures — File upload

No files selected.

### Sample size

The unit of analysis is the run: one (scenario, policy, seed, repeat) tuple.

Planned sample sizes:

- Pilot-1: 324 runs. Composition: 6 scenarios × 6 policies × 3 seeds × 3 repeats = 324 runs.
- Pilot-2: 540 runs. Composition: 6 scenarios × 6 policies × 3 seeds × 5 repeats = 540 runs. (Repeats increased from 3 to 5 to support the n_min sensitivity analysis at 20, 30, 50.)
- Confirmatory: 432 runs. Composition: 6 scenarios × 6 policies × 3 seeds × 4 repeats = 432 runs. (Repeats fixed at 4 for the confirmatory stage to keep total runtime bounded while preserving per-cell stability.)

Sample size is the same across scenarios, policies, seeds, and repeats within each stage. There is no nesting across levels; the design is fully crossed.

At the run level, the sample size per (scenario, policy) cell is:

- Pilot-1: 3 seeds × 3 repeats = 9 runs per cell (54 cells total).
- Pilot-2: 3 seeds × 5 repeats = 15 runs per cell (54 cells total).
- Confirmatory: 3 seeds × 4 repeats = 12 runs per cell (54 cells total).

No multi-level or mixed structure exists beyond the fully crossed design.

### Sample size rationale

Sample size was determined by three considerations, in order:

1. Pilot/Confirmatory separation requirement. The protocol requires that thresholds be calibrated on Pilot data and held fixed on Confirmatory data. Pilot-1 must therefore be large enough to produce stable threshold estimates; Pilot-2 must be large enough to support the sensitivity analysis at n_min = 20, 30, 50; Confirmatory must be large enough to test threshold stability on held-out scenarios C3 and C4.

2. Support threshold n_min. The zero-support threshold n_min = 30 is the minimum number of observations per state required for a comparison to be considered supportable. To achieve n_min = 30 in expectation for a target cell, and given the state visitation distribution of HeMAC, the per-cell sample size was set to at least 9 runs (Pilot-1) and increased to 15 (Pilot-2) and 12 (Confirmatory). These values were chosen so that the expected number of comparable states per cell exceeds the threshold by a margin that allows the sensitivity analysis at n_min = 20 and n_min = 50 to be meaningful.

3. Bounded total runtime. The total number of runs was bounded to keep the full experimental programme (Pilot-1 + Pilot-2 + Confirmatory) executable within approximately 75 days on the available hardware, while preserving per-cell stability.

No formal power analysis was performed because no inferential test is the primary outcome; the primary outcomes are ranking-fidelity metrics (Spearman rho, Kendall tau, top-k overlap, regret) and coverage metrics (MMD-based), which are reported descriptively per scenario and per estimator, not tested against a single null hypothesis.

No adaptive or Bayesian stopping rule is used. The sample sizes were fixed before execution and are recorded in preregistration/pilot_scope.md.

### Starting and stopping rules

Starting rules:

- Pilot-1 begins after: (a) the R7 specification is frozen and pinned by sha256 digest; (b) n_min = 30 is fixed and recorded in preregistration/thresholds.md; (c) verify_separation.py passes V1–V7 on the empty results directories; (d) the 66 automated tests pass.

- Pilot-2 begins after: (a) Pilot-1 is complete and archived in results/pilot/; (b) the n_min sensitivity analysis (20, 30, 50) is specified; (c) the fault-injection determinism test passes.

- Confirmatory begins after: (a) Pilot-2 is complete and archived in results/pilot/; (b) thresholds (tau_min = 0.70, epsilon* ≈ 1.95, n_min = 30) are frozen and recorded; (c) the freeze is timestamped and hashed; (d) verify_separation.py confirms that no confirmatory result exists before the freeze; (e) the 66 automated tests still pass on the frozen codebase.

Stopping rules:

- A stage stops when its pre-specified run count is reached:
  - Pilot-1: 324 runs.
  - Pilot-2: 540 runs.
  - Confirmatory: 432 runs.

- A stage also stops early (and the early stop is reported) if:
  - The fault-injection determinism test fails on the current codebase.
  - verify_separation.py fails any of V1–V7.
  - A frozen threshold is detected to have been modified after the freeze (by digest mismatch).
  - A pipeline error occurs that cannot be resolved without changing the frozen codebase.

- No stage is extended or reduced after observing intermediate outcomes. The run counts are fixed in advance and recorded.

- If a run fails (e.g., environment exception), the run is re-executed with the same seed and repeat identifier. The re-execution is logged. If re-execution also fails, the run is recorded as a failure and excluded from per-cell aggregates; the exclusion is reported.

- The decision to exclude a failed run is made by the pre-specified rule above, not by inspecting the outcome. This is intended to prevent outcome-dependent exclusion.

---

## Variables

### Manipulated variables

StructOPE is a simulation study; no randomization of human subjects is involved. The "manipulated variables" are the experimental factors that are set by design and fully crossed. Each factor is a categorical variable with pre-specified levels.

Factor 1 — Scenario (6 levels): S1, S2, S3, S4, S5, S6. Scenarios S5 and S6 include the held-out structural cells C3 and C4. The baseline scenario is S1.

Factor 2 — Policy (6 levels): P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M, P_DEGRADED. These are coordination policies, not learned during the study. They are fixed before execution.

Factor 3 — Estimator (6 levels): B1a, B1b, B2, B3a, B3b, B4. These are the OPE estimators whose rankings are audited. No new estimator is proposed.

Factor 4 — Structural-shift fault (8 types × 3 severity × 3 timing = 72 conditions per fault type, aggregated as 24 cells in the implementation matrix):
- Team-composition faults: agent dropout, capability degradation, agent replacement, team-size change.
- Communication faults: packet loss, communication delay, network partition, topology change.
- Severity levels: mild, moderate, severe.
- Timing: before, during, between.

Factor 5 — Seed (3 levels): Three fixed seeds, recorded in preregistration/pilot_scope.md before execution. Seeds are not selected or discarded after observing outcomes.

Factor 6 — Repeat (3 levels in Pilot-1; 5 in Pilot-2; 4 in Confirmatory): Fixed before execution, recorded in preregistration/pilot_scope.md.

Stage (3 levels, between-stage, not crossed with the above within a stage):
- Pilot-1 (324 runs; exploratory; removable).
- Pilot-2 (540 runs; exploratory; removable).
- Confirmatory (432 runs; frozen; locked).

The design is fully crossed within each stage. There is no randomization of treatment assignment because all cells are executed; there is no counterbalancing because the design is not a within-subject comparison of human participants.

No manipulated variable is adjusted after execution. All levels are pre-registered in preregistration/pilot_scope.md.

### Measured variables

For each run (one (scenario, policy, seed, repeat) tuple), the following variables are measured and recorded.

Primary outcome — Ranking fidelity:
- Spearman rho: rank correlation between the OPE-estimated ranking and the reference ranking (B4 direct utility).
- Kendall tau: rank correlation between the OPE-estimated ranking and the reference ranking.
- Top-k overlap: overlap between the top-k policies under OPE and under the reference ranking, for k = 1, 2, 3.
- Regret: difference in true utility between the best policy in the reference ranking and the policy selected by the OPE-estimated ranking.

Secondary outcome — Coverage:
- MMD distance: Maximum Mean Discrepancy with Gaussian RBF kernel and median-heuristic bandwidth, computed between state-conditioned action distributions p(a|s) under the evaluated policy and under the behaviour policy.
- Coverage label: binary label (covered / not covered) assigned by comparing MMD distance to the frozen threshold (0.070 in the current calibration).
- Zero-support fraction: fraction of states where the number of observations is below n_min = 30.

Support variable:
- Comparable-state count: number of states where the number of observations is at least n_min = 30.
- Comparable-state fraction: comparable-state count divided by the total number of visited states.

Utility variable:
- True utility U(pi; omega): documented utility for policy pi in scenario omega, computed by the utility specification (B4 direct).
- Estimated utility: utility estimated by each OPE estimator (B1a, B1b, B2, B3a, B3b) for the same policy and scenario.

Fault-injection variables:
- Fault type (categorical): one of 8 types.
- Severity (categorical): mild, moderate, severe.
- Timing (categorical): before, during, between.
- Fault applied (binary): whether the fault was successfully applied in a given run.
- Fault determinism flag (binary): whether the same seed produced the same structural-shift outcome across repeated executions.

Metadata variables (recorded per run, not analyzed as outcomes):
- Run identifier: (scenario, policy, seed, repeat).
- Stage: Pilot-1, Pilot-2, Confirmatory.
- Freeze timestamp (for Confirmatory runs only).
- sha256 digest of the R7 specification.
- Software version: Python version, matplotlib version, NumPy version.
- Timestamp of run completion.

No variables are measured on human participants. No personal data are collected. No ethics approval is required.

All measured variables are recorded in the run log and archived with each run. The analysis code that produces the ranking-fidelity metrics is separate from the code that produces the utility estimates, to reduce the risk of outcome-dependent adjustment.

### Indices

Three derived indices are computed from the measured variables.

Index 1 — Ranking Fidelity Score (RFS):
RFS is a composite of the four ranking-fidelity metrics:
RFS = (1/4) * [ Spearman_rho_normalized + Kendall_tau_normalized + Top_k_overlap + (1 - Regret_normalized) ]
where:
- Spearman_rho_normalized = (Spearman_rho + 1) / 2 (maps [-1, 1] to [0, 1]).
- Kendall_tau_normalized = (Kendall_tau + 1) / 2 (maps [-1, 1] to [0, 1]).
- Top_k_overlap = top-k overlap for k = 3 (fraction of the top-3 policies that agree).
- Regret_normalized = Regret / (max possible regret in the scenario), where max possible regret is the difference between the best and worst true utility in the scenario.
RFS lies in [0, 1]; higher values indicate better ranking fidelity.
RFS is reported per (scenario, estimator) cell; it is not tested against a single null hypothesis.

Index 2 — Coverage Separation Score (CSS):
CSS = (mean MMD distance for not-covered states) / (mean MMD distance for covered states)
CSS > 1 indicates that the MMD distance separates covered from not-covered states; CSS ≈ 1 indicates no separation.
CSS is reported per (scenario, estimator) cell.

Index 3 — Fidelity-Coverage Association (FCA):
FCA = Spearman rank correlation between the per-cell Coverage Fraction (fraction of comparable states) and the per-cell RFS.
FCA is computed across the 54 (scenario, estimator) cells within a stage.
FCA > 0 indicates that ranking fidelity is associated with coverage; FCA ≈ 0 indicates no association.
FCA is reported per stage (Pilot-1, Pilot-2, Confirmatory).

All three indices are pre-specified. No index is selected after observing the results. The formulas above are recorded in preregistration/r7_mmd_spec.md and are not modified after execution.

Indices are reported descriptively. No inferential test is the primary outcome. The primary outcomes are the per-cell metrics and the per-cell indices, and the pattern of their variation across scenarios, estimators, and stages.

No index is used to exclude runs. Run exclusion follows the pre-specified rule in the "Starting and stopping rules" section (re-execution of failed runs; exclusion only after repeated failure, with the exclusion reported).

---

## Analysis Plan

### Statistical models

StructOPE is a descriptive simulation study. No single null hypothesis is the primary target. The primary outcomes are per-cell descriptive metrics (ranking fidelity and coverage) reported across scenarios, estimators, and stages. The statistical models below are used to summarize variation and to test pre-specified associations; they are not used to claim causal effects.

Model 1 — Per-cell ranking fidelity (descriptive).
For each (scenario, estimator) cell within a stage, the following are reported:
- Mean and standard deviation of Spearman rho.
- Mean and standard deviation of Kendall tau.
- Mean and standard deviation of top-k overlap (k = 3).
- Mean and standard deviation of regret.
- 95% bootstrap confidence intervals (1000 bootstrap resamples) for each metric.
No inferential test is applied at this level. The purpose is to describe the distribution of ranking fidelity per cell.

Model 2 — Ranking Fidelity Score (RFS) across cells.
The composite RFS (defined in the Indices section) is computed per (scenario, estimator) cell. A two-way linear model is fit to RFS:
RFS ~ Scenario + Estimator + Scenario:Estimator
The model is fit separately within each stage (Pilot-1, Pilot-2, Confirmatory). It is used to describe the proportion of variance in RFS associated with scenario, with estimator, and with their interaction. No p-values are used as decision criteria; the model is reported descriptively (R-squared, partial R-squared, coefficient estimates with bootstrap CIs).

Model 3 — Fidelity-Coverage Association (FCA).
The association between coverage fraction and RFS across cells is measured by Spearman rank correlation (FCA, defined in the Indices section). This is computed separately per stage. A 95% bootstrap confidence interval is reported. FCA > 0 indicates that ranking fidelity is associated with coverage; FCA ≈ 0 indicates no association. No inferential test is applied; the confidence interval is the primary summary.

Model 4 — Threshold stability (Confirmatory only).
For the Confirmatory stage, the frozen thresholds (tau_min = 0.70, epsilon* ≈ 1.95, n_min = 30) are applied to the held-out scenarios C3 and C4. The proportion of cells that satisfy each threshold is reported. A cell is classified as "stable" if the threshold is satisfied; "unstable" otherwise. The proportion of stable cells is reported per threshold and per scenario. No inferential test is applied; the proportion is the primary summary.

Model 5 — Fault-injection determinism.
The determinism test (part of the 66 automated tests) verifies that repeated executions with the same seed produce identical structural-shift outcomes. This is a binary check per fault type, not a statistical model. It is reported as pass/fail per fault type.

No positive or negative controls are used as inferential anchors. No manipulation checks are relevant (no human participants). No convergence criteria apply beyond the bootstrap (1000 resamples) and the deterministic execution of the simulation.

If a model fails to fit (e.g., due to a degenerate cell with zero variance), the failure is reported and the cell is described by its raw mean and standard deviation instead. No model is added or removed after observing the results.

### Transformations

No raw data are transformed before aggregation. The following transformations are applied only to produce the indices defined in the "Indices" section:

1. Spearman rho normalization: rho_norm = (rho + 1) / 2. Maps rho from [-1, 1] to [0, 1]. Used only inside the RFS composite.
2. Kendall tau normalization: tau_norm = (tau + 1) / 2. Maps tau from [-1, 1] to [0, 1]. Used only inside the RFS composite.
3. Regret normalization: regret_norm = regret / max_possible_regret, where max_possible_regret is the difference between the best and worst true utility in the scenario. Used only inside the RFS composite.
4. Categorical coding: Scenario, estimator, policy, fault type, severity, and timing are treated as categorical variables in the two-way model (Model 2). Reference categories are: S1 (scenario), B1a (estimator), mild (severity), before (timing). No dummy coding is applied outside Model 2.
5. No centering, scaling, or recoding of raw metrics. Spearman rho, Kendall tau, top-k overlap, regret, MMD distance, and coverage fraction are reported on their original scales. No z-scoring, no log transformation, no winsorization.

All transformations are pre-specified. No transformation is added or modified after observing the results.

### Inference criteria

StructOPE is a descriptive simulation study. The primary outcomes are per-cell descriptive metrics and pre-specified indices. The following inference criteria are used:

1. No p-values are used as decision criteria. The study does not test a single null hypothesis. The two-way model (Model 2) is reported descriptively (R-squared, partial R-squared, bootstrap CIs). No p-values, no Bayes factors, and no model-fit indices are used to accept or reject hypotheses.

2. Confidence intervals are the primary summary. 95% bootstrap confidence intervals (1000 resamples) are reported for all metrics and indices. A metric is described as "clearly positive" if the lower bound of its 95% CI is above zero, "clearly negative" if the upper bound is below zero, and "uncertain" otherwise. This is a descriptive label, not a decision criterion.

3. Threshold-satisfaction proportions are the primary summary for Confirmatory. For each threshold (tau_min = 0.70, epsilon* ≈ 1.95, n_min = 30), the proportion of cells that satisfy the threshold is reported. No hypothesis test is applied. A stage is described as "stable" if a high proportion of cells satisfy the threshold; "unstable" otherwise. The exact threshold for "high proportion" is not pre-specified; the full distribution is reported.

4. Multiple comparisons are not corrected. Because no p-values are used as decision criteria, no multiple-comparison correction is applied. The full set of per-cell metrics and per-stage indices is reported. Any pattern across cells is described as a pattern, not as a significant finding.

5. One-tailed vs two-tailed tests: not applicable. No hypothesis test is applied. The study reports the full distribution of metrics and indices.

6. Pre-specified associations: The Fidelity-Coverage Association (FCA) is the primary pre-specified association. Its 95% bootstrap CI is reported. If the CI excludes zero, the association is described as "present"; otherwise "not clearly present". No causal interpretation is attached.

All inference is descriptive. The study does not claim causal effects. The question is ranking preservation, not performance gain. Any violation of a threshold is recorded as a violation and reported, not repaired or reinterpreted.

### Data inclusion and exclusion

The unit of analysis is the run: one (scenario, policy, seed, repeat) tuple.

Inclusion criteria:
- A run is included if it completed without error and its fault-injection flag matches the intended configuration (i.e., the fault was applied as specified).
- All runs that meet the inclusion criteria are used. No run is excluded based on its outcome.

Exclusion criteria (pre-specified):
- A run is excluded if the fault-injection flag does not match the intended configuration (i.e., the fault was not applied as specified). The exclusion is reported.
- A run is excluded if it failed (environment exception) and re-execution with the same seed and repeat identifier also failed. The exclusion is reported.
- No run is excluded based on its outcome value (no outcome-dependent exclusion).

Outliers:
- No outlier removal is applied. All metrics are reported on their original scales, with means, standard deviations, and bootstrap CIs. Extreme values are visible in the reported distributions and are not removed.

Failed runs:
- If a run fails, it is re-executed with the same seed and repeat identifier. The re-execution is logged.
- If re-execution also fails, the run is recorded as a failure and excluded from per-cell aggregates. The exclusion is reported in the run log and in the analysis output.
- The decision to exclude a failed run is made by the pre-specified rule above, not by inspecting the outcome.

No human subjects are involved. No participant exclusion applies. No ethics approval is required.

### Missing data

Missing data in StructOPE can arise from two sources:

1. Failed runs. A run is considered missing if it fails twice (see Data inclusion and exclusion). Failed runs are recorded and excluded from per-cell aggregates. The exclusion is reported. No imputation is applied.

2. Missing metric values within a completed run. If a metric cannot be computed for a completed run (e.g., MMD distance is undefined because the comparable-state count is zero), the run is retained but the metric is recorded as "NA". The NA is reported in the analysis output. No imputation is applied. The number of NA values per metric is reported per (scenario, estimator) cell.

No imputation (mean, median, multiple imputation, or model-based) is applied. The analysis is conducted on all available data. Missingness is reported explicitly, not hidden.

If the number of NA values per cell exceeds 20% of the planned runs for that cell, the cell is described as "sparse" and the summary statistics for that cell are reported with a warning. No cell is dropped based on its outcome.

### Other planned analysis

The following secondary analyses are planned. They are exploratory and are reported separately from the primary outcomes.

1. Per-policy analysis. The ranking-fidelity metrics are aggregated per policy (P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M, P_DEGRADED) to describe which policies are most affected by structural shift. This analysis is descriptive; no hypothesis test is applied.

2. Per-fault-type analysis. The ranking-fidelity metrics are aggregated per fault type (8 types) to describe which fault types are most disruptive. This analysis is descriptive; no hypothesis test is applied.

3. Per-severity analysis. The ranking-fidelity metrics are aggregated per severity level (mild, moderate, severe) to describe the effect of severity on ranking fidelity. This analysis is descriptive; no hypothesis test is applied.

4. Per-timing analysis. The ranking-fidelity metrics are aggregated per timing point (before, during, between) to describe the effect of timing on ranking fidelity. This analysis is descriptive; no hypothesis test is applied.

5. Estimator-level comparison. The ranking-fidelity metrics are compared across the six estimators (B1a, B1b, B2, B3a, B3b, B4) to describe which estimators are most robust to structural shift. This analysis is descriptive; no hypothesis test is applied.

6. Sensitivity to n_min. The comparability decisions are recomputed at n_min = 20, 30, and 50 to describe the sensitivity of the conclusions to the choice of threshold. This analysis is pre-specified and is reported as a sensitivity analysis, not as a primary outcome.

7. Reproducibility check. A subset of runs (e.g., 10% of each stage) is re-executed with the same seeds to confirm that the results are reproducible. Any discrepancy is reported.

All secondary analyses are descriptive and do not modify the primary outcomes. No secondary analysis is used to accept or reject a hypothesis. The full set of secondary analyses is reported in the analysis output, regardless of whether the results are positive, negative, or null.

---

## Other

### Context and additional information

StructOPE is a pre-registered, falsification-first research protocol, not a hypothesis-testing study. Its contribution lies in the precision of its definitions, the derivations that follow from them without data, and the specification of the planned experiments. The experiments described in this registration have been executed; the protocol is registered retrospectively with the full record of execution and verification.

Context on the origin of the protocol:

StructOPE was formulated in response to two practical questions that arise in policy selection for multi-agent systems. The first is whether an Off-Policy Evaluation (OPE) estimator that ranks policies correctly under one structural condition continues to do so under another. The second is how to tell whether an observed difference between two policies reflects genuinely different behaviour or merely a difference in what was observed. The protocol treats the second question as the more basic of the two: a ranking built on comparisons that the data cannot support is uninformative however it is scored.

The choice of comparison object (state-conditioned action distributions p(a|s), labelled U2 in the record) and the choice of distance (Maximum Mean Discrepancy with a Gaussian RBF kernel and median-heuristic bandwidth) follow from this stance. Both choices are frozen in the protocol, pinned by a sha256 digest, and verified by automated checks.

Pilot/Confirmatory separation:

The protocol enforces a strict separation between exploratory pilot work (Pilot-1: 324 runs; Pilot-2: 540 runs) and a frozen confirmatory stage (432 runs). The separation is not a matter of convention: it is enforced by the file system layout (results/pilot/ and results/confirmatory/), by a timestamped freeze (Item 1.3 + sha256), and by an automated verifier (verify_separation.py, checks V1–V7) that runs as part of the 66-test suite. Any attempt to modify a frozen threshold after the freeze is detected by digest mismatch.

The freeze does not certify that the protocol is correct. It certifies that the protocol was fixed before the confirmatory data were analyzed. The distinction matters: a frozen protocol can still be wrong, and the paper records where it might be wrong (Threats to Validity, Section 14).

Reproducibility and verification:

The repository contains the full source code (src/), the test suite (tests/), the experimental artifacts (experiments/), the pre-registration specifications (preregistration/), and the design documents (design/). The 66 automated tests cover the separation invariants (V1–V7), the fault-injection determinism, the threshold values, and the MMD computation. The verification records are archived with each run.

No new OPE estimator is proposed. The protocol audits a fixed set (B1a, B1b, B2, B3a, B3b, B4) and reports ranking fidelity, regret, and coverage. The question is ranking preservation, not performance gain.

Limits of the study:

- The study does not claim that multi-agent OPE fails under structural shift. It measures whether and where ranking fidelity degrades, and whether loss of support explains the degradation.
- The study does not claim that any specific estimator is superior. It audits the fixed set and reports the pattern.
- The study does not claim that uncertainty-aware selective evaluation improves selection. It measures whether selective evaluation detects indefensible comparisons.
- The study does not claim causal effects. The design is descriptive; associations are reported as associations.
- The study does not propose a reference implementation before the protocol is frozen. The implementation is a realization of the frozen protocol, not a proposal for a new standard.

Open items (recorded, not resolved in this registration):

- The independent review of the threshold calibration remains open. The thresholds used in the Confirmatory stage (tau_min = 0.70, epsilon* ≈ 1.95, n_min = 30) were frozen before execution and are recorded, but they have not been independently reviewed.
- The HeMAC integration was verified at the time of execution, but HeMAC itself is an evolving benchmark. Results may not transfer to future HeMAC versions.
- The fault-injection determinism test passed on the current codebase; independent replication is pending.

Repository and persistent identifiers:

- Repository: https://github.com/gitdeeper16/structope
- Zenodo DOI (pre-registration): 10.5281/zenodo.24473998
- Figshare DOI (alternative): 10.6084/m9.figshare.35117266
- Paper: docs/paper/StructOPE_Research_Paper_v1.0.0.pdf
- Figures: docs/figures/ (12 figures, fig01–fig12)

The registration is intended to document the protocol as it was frozen, and to make the execution record transparent. It does not replace the paper, the repository, or the pre-registration DOI. It is a companion record, intended for readers who want to see the protocol as it was specified, executed, and verified.

Acknowledgments:

The author thanks the developers of the Heterogeneous Multi-Agent Challenge (HeMAC) for providing the primary environment, and the maintainers of the open-source tools used in this project (Python, matplotlib, NumPy).

No funding was received for this study. No conflicts of interest are declared.

---

## Metadata

### Contributors

Samir Baladi

### Resource type

No resource type

### Description

StructOPE is a pre-registered, falsification-first research protocol for auditing Off-Policy Evaluation (OPE) estimator rankings under structural shift — changes in team composition (T0–T4) and communication structure (C0–C4) between data collection and evaluation in multi-agent environments.

The protocol fixes the comparison object (state-conditioned action distributions p(a|s)), the distance metric (Maximum Mean Discrepancy with a Gaussian RBF kernel and median-heuristic bandwidth), an explicit rule for insufficient support (zero-support threshold n_min = 30, with sensitivity analysis at 20 and 50), a documented utility, a six-scenario Pilot design, a fault-injection specification, and a strict separation between exploratory pilot work and a frozen confirmatory stage.

Executed experiments: Pilot-1 (324 runs), Pilot-2 (540 runs), Confirmatory (432 runs).

Verification: 66 automated tests passed; V1–V7 separation checks passed; fault-injection determinism confirmed.

The protocol treats a fixed set of OPE estimators (B1a, B1b, B2, B3a, B3b, B4) as objects whose rankings are audited. No new OPE estimator is proposed. The question is ranking preservation, not performance gain.

Status: Pre-registered protocol, executed. Final verdict under review.

Repository: https://github.com/gitdeeper16/structope
Pre-registration DOI: 10.5281/zenodo.24473998
Figshare DOI: 10.6084/m9.figshare.35117266

### Registration Type

OSF Preregistration

### Registry

OSF Registries

### Date Created

Nov 25, 2026, 10:26 AM

### Date registered

Nov 25, 2026, 10:26 AM

### Subjects

- Research Methods in Life Sciences
- Artificial Intelligence and Robotics
- Social and Behavioral Sciences
- Computer Sciences
- Life Sciences
- Physical Sciences and Mathematics
- Statistics and Probability

### Tags

- falsification-first
- fault injection
- maximum mean discrepancy
- multi-agent systems
- off-policy evaluation
- pilot-confirmatory separation
- preregistration
- ranking fidelity
- structural shift
- support and coverage

### Affiliated Institutions

No affiliated institutions

### Funder Names

No information

### Language

No language

### License

CC-By Attribution 4.0 International

### Registration DOI

10.17605/OSF.IO/EZJKF

---

## Citations

### APA

Baladi, S. (2026, November 25). StructOPE: Off-Policy Evaluation under Structural Shift — A Pre-Registered Protocol for Auditing Estimator Rankings under Team-Composition and Communication Faults in Multi-Agent Environments. OSF. https://doi.org/10.17605/OSF.IO/EZJKF

### MLA

Baladi, Samir. "StructOPE: Off-Policy Evaluation under Structural Shift — A Pre-Registered Protocol for Auditing Estimator Rankings under Team-Composition and Communication Faults in Multi-Agent Environments." OSF, 25 Nov. 2026. Web.

### Chicago

Baladi, Samir. 2026. "StructOPE: Off-Policy Evaluation under Structural Shift — A Pre-Registered Protocol for Auditing Estimator Rankings under Team-Composition and Communication Faults in Multi-Agent Environments." OSF. November 25. doi:10.17605/OSF.IO/EZJKF.

### BibTeX

```bibtex
@misc{baladi2026structope_osf,
  author       = {Baladi, Samir},
  title        = {{StructOPE: Off-Policy Evaluation under Structural Shift --- A Pre-Registered Protocol for Auditing Estimator Rankings under Team-Composition and Communication Faults in Multi-Agent Environments}},
  year         = {2026},
  month        = nov,
  day          = {25},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/EZJKF},
  url          = {https://doi.org/10.17605/OSF.IO/EZJKF},
  note         = {OSF Preregistration}
}
```

---

Source: Center for Open Science · OSF Registries
Retrieved: 2026-11-25
