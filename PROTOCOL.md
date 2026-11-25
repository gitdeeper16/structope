# Experimental Protocol v1.0

## Validity of Multi-Agent Off-Policy Policy Selection under Structural Changes in Team Composition and Communication

**Status:** Experimental Design — Pre-Implementation
**Version:** 0.1
**Research Stage:** Protocol Specification
**Primary Environment Candidate:** HeMAC
**Reference:** Independent simulator execution
**Protocol Type:** Comparative, controlled, reproducible experimental study

---

## 1. Research Question

Does multi-agent off-policy evaluation preserve its ability to rank
and select coordination policies when the structural configuration of
a cooperative team changes between data collection and policy
evaluation?

The investigation focuses on two structural changes:

1. **Team Composition Shift:** Changes in the number, identity,
   availability, or capabilities of participating agents.
2. **Communication Structure Shift:** Changes in communication
   availability, reliability, connectivity, or topology.

A secondary question concerns whether uncertainty-aware selective
evaluation can identify situations in which the resulting policy
ranking is statistically unreliable.

The study does not assume that Model-Based OPE is superior to
conventional OPE. Both are evaluated as competing approaches.

## 2. Scope and Boundaries

### Included

- Offline evaluation of candidate multi-agent coordination policies.
- Policy ranking and policy selection.
- Changes between data collection and evaluation conditions.
- Team composition and communication changes.
- Uncertainty estimation and selective policy selection.
- Comparison against actual execution in a reference simulator.

### Excluded

- Developing a new general-purpose MARL training algorithm.
- Proving that World Models are universally superior to conventional OPE.
- Claiming direct lunar or NASA operational validation.
- Treating policy generation as equivalent to policy evaluation.
- Claiming that the investigated research intersection is absent
  from all existing literature.

The literature-based novelty claim will remain qualified:

"To the best of our knowledge, the examined literature does not
directly establish the validity of multi-agent OPE-based policy
selection under combined team-composition and communication
structural changes."

## 3. Experimental Architecture

The experiment consists of five components:

1. **Reference Environment:** A simulator used to execute candidate
   policies and establish actual performance.
2. **Offline Dataset:** Recorded trajectories collected under
   specified baseline configurations.
3. **Candidate Policies:** A fixed set of coordination policies
   evaluated across experimental conditions.
4. **OPE Methods:** Competing methods estimating candidate policy
   performance from offline data.
5. **Evaluation Layer:** Statistical comparison of estimated
   rankings against reference rankings.

The reference simulator must remain independent of the learned
evaluation model.

No OPE method may access the reference outcomes of the test scenarios
before producing its predictions.

## 4. Experimental Environment

### 4.1 Initial Environment

HeMAC is the primary candidate because it provides heterogeneous
cooperative agents, partial observability, resource constraints, and
communication-range limitations.

However, HeMAC is not assumed to be a complete experimental
environment for this research question.

The implementation must document:

- Original environment capabilities.
- Added fault-injection mechanisms.
- Changes to agent interfaces.
- Communication simulation assumptions.
- Reproducibility of modified scenarios.

### 4.2 Reference Execution

The reference simulator will execute each candidate policy under the
same scenario and random seed conditions used for OPE evaluation.

Reference outcomes will be obtained through repeated execution rather
than a single rollout.

This is necessary because stochastic execution can make the true
ordering of two policies uncertain.

## 5. Candidate Policy Set

The candidate policy set is a controlled experimental variable.

The initial target is 8–12 policies, subject to feasibility and
statistical analysis.

The set must include:

1. Strong coordination policies.
2. Policies with different coordination strategies.
3. Policies with different communication requirements.
4. Policies with different resource-consumption profiles.
5. Deliberately fragile policies.
6. Policies that perform well under baseline conditions but
   deteriorate under selected structural changes.

### 5.1 Policy Diversity Criteria

The set must demonstrate:

- Behavioral diversity.
- Nontrivial performance differences.
- Sufficient coverage of relevant performance trade-offs.
- At least some meaningful policy-ranking inversions under
  structural changes.

The policy set must not be selected solely because it produces
favorable results for a particular OPE method.

### 5.2 Fixed Policy Set

The same candidate policy set must be used across all three
experimental stages.

Any modification requires:

- A documented justification.
- A new policy-set version.
- Explicit identification of affected experiments.

No silent policy replacement is permitted.

## 6. Offline Dataset Construction

### 6.1 Data Collection Conditions

The initial offline dataset will be collected under a defined
baseline configuration:

- Fixed team composition.
- Normal communication conditions.
- Defined resource constraints.
- Recorded observations, actions, rewards, and relevant environment
  states.

### 6.2 Dataset Coverage

The dataset must include trajectories generated by multiple behavior
policies.

This is important because evaluating candidate policies from data
generated by only one behavior policy may introduce severe coverage
limitations.

### 6.3 Information Available to Evaluation Models

The protocol must distinguish between:

- Full recorded trajectories.
- Partial trajectories.
- Aggregated statistics.
- Agent-level observations and actions.
- Team-level state and interaction information.

The primary experiment will use recorded trajectories with the
information available to the selected OPE method.

No method may receive additional test-time information unavailable
to competing methods unless that difference is explicitly documented
as a separate experimental condition.

### 6.4 Data Separation

The dataset will be divided into:

- Training data.
- Validation data.
- Test data.

Test scenarios and their reference outcomes must remain inaccessible
during model training and hyperparameter selection.

## 7. Structural Shift Variables

### 7.1 Team Composition

| Condition | Description |
|---|---|
| T0 | Original team composition |
| T1 | Agent dropout |
| T2 | Agent capability degradation |
| T3 | Agent replacement |
| T4 | Team-size change |

### 7.2 Communication Structure

| Condition | Description |
|---|---|
| C0 | Normal communication |
| C1 | Random packet loss |
| C2 | Communication delay |
| C3 | Partial communication partition |
| C4 | Changed communication topology |

### 7.3 Severity

Each applicable structural change will have three severity levels:

- Mild.
- Moderate.
- Severe.

The numerical definitions must be established from the simulator's
actual operating parameters before confirmatory experiments.

### 7.4 Distribution Conditions

Three evaluation conditions will be distinguished:

- **In-Distribution:** Conditions represented in training data.
- **Near-OOD:** Conditions with moderate deviations from training.
- **OOD:** Structural configurations withheld from training.

The test split must contain unseen combinations of conditions, not
merely new random seeds from already observed configurations.

### 7.5 Factorial Design

The experiment will initially examine individual structural changes.

Combined team-composition and communication changes will be
introduced after the individual effects have been characterized.

This avoids an unnecessarily large initial experimental space and
allows attribution of observed failures.

## 8. Evaluation Methods and Baselines

The following comparison methods are required.

### B0. Random Ranking

A random policy ordering establishes a minimal reference baseline.

### B1. Baseline-Performance Ranking

Policies are ranked according to their measured baseline performance,
without adapting the ranking to structural changes.

This tests whether the original ranking remains useful after the
system changes.

### B2. Conventional Multi-Agent OPE

An applicable conventional OPE estimator will be selected and adapted
to the cooperative multi-agent setting.

Its assumptions, supported policy class, and required data coverage
must be documented.

### B3. Model-Based OPE

A learned dynamics model will estimate candidate policy performance
through model-based evaluation.

The model architecture and training information must be documented.

### B4. Selective Policy Selection

An uncertainty-aware selection mechanism will be evaluated.

SIRV may inform its design, but the adapted method must not be
presented as a direct implementation of the original algorithm.

The adaptation must specify:

- The uncertainty signal.
- The selection or abstention rule.
- The calibration procedure.
- The criteria for issuing or withholding a ranking.

### B5. Reference Oracle

The reference simulator will provide the actual estimated performance
of every candidate policy under each test condition.

The oracle is an evaluation reference, not a deployable OPE method.

## 9. Primary Evaluation Metrics

### 9.1 Policy Ranking Fidelity

- Spearman Rank Correlation.
- Kendall's Tau.

Both will be reported with uncertainty intervals.

### 9.2 Policy Selection Regret

For scalar utility:

Regret@k will measure the difference between the reference
performance of the best available policy and the best policy selected
among the estimated top-k candidates.

The utility definition must be fixed before confirmatory evaluation.

### 9.3 Pairwise Ranking Calibration

The evaluation method must produce an explicit probability or
uncertainty estimate for pairwise policy comparisons.

For policies i and j:

P(U_i > U_j | offline data)

Pairwise calibration will be evaluated using:

- Pairwise Brier Score.
- Reliability diagrams.
- Expected Calibration Error, with predefined binning.

A generic model confidence score will not be treated as calibrated
pairwise confidence.

### 9.4 Selective Evaluation

The evaluation will measure:

- Risk-Coverage Curve.
- Area Under the Risk-Coverage Curve.
- Selection Regret at predefined coverage levels.
- Abstention frequency.

### 9.5 Error Detection

AUROC will measure whether the uncertainty mechanism can detect
predefined ranking failures.

OOD Detection will be reported separately.

Detecting an unfamiliar configuration is not equivalent to detecting
an incorrect ranking.

## 10. Multi-Objective Performance

The primary confirmatory analysis will use a predefined scalar
utility function.

Potential components include:

- Task success.
- Energy consumption.
- Completion time.
- Communication cost.

The utility weights must be fixed before the confirmatory
experiments.

A secondary analysis will examine Pareto-front recovery.

The Pareto front will be computed using explicit dominance relations
over the predefined objectives.

A total ranking will not be forced onto policies that are mutually
non-dominated.

## 11. Hypotheses

### H1 — Structural Shift and Ranking Fidelity

Policy-ranking fidelity decreases under structural changes between
offline data collection and evaluation.

The effect may differ between team-composition changes and
communication changes.

### H2 — Structural Shift and Selection Regret

Policy-selection regret increases under structural changes, with
potentially different failure patterns across OPE methods.

### H3 — Selective Evaluation

Selective policy evaluation reduces selection regret under structural
shift when its uncertainty signal is genuinely associated with
ranking error, rather than merely detecting unfamiliar
configurations.

### H4 — Method-Dependent Robustness

Conventional OPE and Model-Based OPE exhibit different robustness
profiles under team-composition and communication changes.

Neither method is assumed to dominate across all conditions.

## 12. Statistical Design

### 12.1 Experimental Repetitions

The initial planning target is at least 30 independent environment
seeds per confirmatory condition.

This is a planning target, not a demonstrated sufficient sample size.

A pilot study will estimate:

- Between-seed variance.
- Within-scenario variance.
- Policy-ranking variability.
- Expected effect sizes.
- Correlation between repeated policy executions.

### 12.2 Dependence Structure

Policy observations within the same scenario and random seed are not
independent.

Statistical analysis must preserve this dependence.

The preferred approach is paired, cluster-aware resampling at the
environment-seed or scenario-seed level.

Confidence intervals for rank correlations must not treat every
policy pair as an independent observation.

### 12.3 Power Analysis

Power analysis will be conducted using pilot variance estimates and
simulation of the planned experimental design.

The study will define:

- Minimum practically relevant effect size.
- Target statistical power.
- Significance level.
- Multiple-comparison correction strategy.

A difference between two correlation coefficients will not be
interpreted as meaningful solely because their numerical values
differ.

## 13. Preregistered Failure Definitions

The following thresholds are provisional and must be locked before
confirmatory evaluation.

### 13.1 Material Selection Error

Define normalized utility regret:

Normalized Regret =
    (Best Reference Utility - Selected Policy Utility)
    / Baseline Utility Range

The initial material-error threshold is:

**ε = 0.05**

A ranking failure occurs when the selected policy incurs normalized
regret greater than ε.

### 13.2 Ranking Fidelity Failure

The initial threshold is:

**τ_min = 0.70**

A ranking failure is recorded when Kendall's Tau falls below this
threshold.

### 13.3 Combined Failure Event

The primary ranking-failure event is:

A material selection error under ε, or a ranking-fidelity result
below τ_min.

Both components must also be reported separately.

The thresholds must not be adjusted after examining confirmatory test
results.

### 13.4 Important Qualification

The thresholds are operational definitions for the experiment, not
universal standards for acceptable OPE performance.

Their suitability must be checked during the pilot stage and locked
before the confirmatory stage.

## 14. Experimental Stages and Transition Gates

### Stage 1 — Baseline Validity

Objective:

Determine whether the selected evaluation architecture can
meaningfully estimate and rank the candidate policies under baseline
conditions.

Initial gate:

- Spearman correlation ≥ 0.70.
- At least 10 independent pilot seeds.
- Nontrivial performance differences among candidate policies.
- Stable reference rankings within estimated uncertainty.

If the gate fails, investigate:

1. Model architecture limitations.
2. Insufficient dataset coverage.
3. Candidate policy-set difficulty.
4. Reference execution variability.

A failed Stage 1 does not establish that the research hypothesis is
false.

### Stage 2 — Structural Shift Evaluation

Objective:

Measure ranking degradation and selection regret under team-
composition and communication changes.

The analysis will identify:

- Which structural changes cause ranking inversions.
- Which changes produce the largest regret.
- Which OPE methods are most sensitive.
- Whether combined changes produce effects beyond individual
  changes.

### Stage 3 — Selective Evaluation

Objective:

Test whether uncertainty-aware selection can recognize situations in
which the estimated ranking is unreliable.

The main comparison will be between:

- Non-selective OPE.
- Selective OPE.
- Reference execution.

The central result will be the relationship between coverage and
selection risk.

## 15. Preregistration Requirements

Before confirmatory experiments, the following must be frozen:

1. Research question.
2. Candidate policy set.
3. Simulator version.
4. Dataset construction procedure.
5. Training, validation, and test splits.
6. Structural-shift definitions.
7. Fault severity parameters.
8. OPE implementations.
9. Uncertainty estimation methods.
10. Primary and secondary metrics.
11. Utility function and weights.
12. ε and τ_min.
13. Statistical analysis plan.
14. Sample-size and power-analysis procedure.
15. Stage-transition criteria.
16. Exclusion and failure-handling rules.

Any subsequent modification must be documented with a version change
and its effect on the confirmatory status of the results.

## 16. Threats to Validity

### Simulator Validity

HeMAC is not a lunar robotics simulator. Results will establish
properties within the tested simulation environment, not operational
lunar reliability.

### Reference Validity

The reference simulator provides a controlled comparison but does not
eliminate model mismatch or simulation bias.

### Policy-Set Validity

Results may depend on the diversity and coverage of the candidate
policy set.

### Dataset Coverage

An OPE method may fail because the offline data do not adequately
cover the target policies, independently of structural shift.

### Method Selection

The choice of OPE estimator and uncertainty architecture may influence
the results.

### Structural-Shift Definition

Team composition changes and communication changes represent
different forms of system modification and must be analyzed
separately before combined conclusions are drawn.

### External Validity

Generalization beyond HeMAC requires replication in another
environment or simulator.

## 17. Expected Research Outputs

The investigation aims to produce:

1. A reproducible benchmark for multi-agent OPE under structural
   changes.
2. A comparative evaluation of conventional and model-based OPE.
3. An empirical characterization of policy-ranking failures.
4. A calibrated selective-evaluation mechanism, if supported by
   results.
5. A documented dataset and experimental protocol.
6. A clear account of limitations and unsuccessful hypotheses.

## 18. Decision Rule

The research will not be considered successful merely because one
method outperforms another.

The primary scientific contribution is the empirical
characterization of when multi-agent off-policy policy selection
remains valid, when it becomes unreliable under structural changes,
and whether this unreliability can be detected before a policy is
selected.

A negative result is scientifically meaningful if the experimental
design can distinguish structural-shift effects from insufficient
data coverage, policy-set limitations, and estimator-specific
weaknesses.

---

**Protocol Status:** v1.0 — Draft for methodological review.

**Implementation Status:** Not started.

**Confirmatory Experiments:** Not authorized until the protocol,
thresholds, policy set, dataset design, and statistical plan are
frozen.

**Research Principle:** The experiment must test the validity of the
selection process, not search for evidence supporting a predetermined
method.
