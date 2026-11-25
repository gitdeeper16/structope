# Baselines and Reference Evaluation

**Status:** Item 0.2 CLOSED (design level). Item 0.2a CLOSED (design level,
with technical acceptance condition on B1a).
**Date:** 2026-11-23
**Blocking:** Item 0.2 blocked Item 0.6 (Policy Set). Item 0.6 is now unblocked.
**Related:** `design/checklist.md` §0.2, §0.2a; `docs/decisions.md`.

---

## 1. Purpose

This document fixes the set of OPE estimators and the reference
evaluation used throughout StructOPE. It does not choose the policy
set (Item 0.6) or the statistical plan (Item 0.8). It specifies:

- what each baseline is,
- what it assumes,
- what it can and cannot support,
- how it is used in the evaluation.

---

## 2. Position on AAMAS 2021

Abe & Kaneko (AAMAS 2021), *Off-Policy Exploitability-Evaluation in
Two-Player Zero-Sum Markov Games*, is adopted as a **theoretical
reference only**. It is **not** used as a practical baseline.

Reason: the paper provides DR and Double Reinforcement Learning
estimators for two-player zero-sum Markov games with exploitability
objectives. It does not provide a ready baseline for a heterogeneous
cooperative system such as HeMAC.

Consequence: no result in StructOPE is reported as "the AAMAS 2021
baseline". The paper is cited where its estimators inform the
construction of B1 and B2, nothing more.

---

## 3. Terminology constraint

A single-agent OPE estimator (FQE, DR) applied to a multi-agent
representation is **not** a native multi-agent OPE method. It is an
application of a known OPE estimator to a multi-agent representation.

This constraint applies to B1a, B1b, and B2. None of them is described
as a "native multi-agent OPE method" in any result or report.

---

## 4. Baseline set

| ID  | Reward scope | Representation        | Role                |
|-----|--------------|-----------------------|---------------------|
| B1a | Local        | Per-agent (factorized)| Sensitivity analysis|
| B1b | Shared       | Per-agent (factorized)| Sensitivity analysis|
| B2  | Shared       | Centralized joint     | Primary             |
| B3a | Model-based  | Policy-conditioned    | Primary             |
| B3b | Model-based  | Multi-agent world     | Secondary, conditional |
| B4  | Direct       | Simulator             | Reference           |

### B1a — Local-Reward Factorized OPE

- **Estimator:** FQE and DR applied per agent.
- **Reward:** each agent's local reward, as defined in HeMAC.
- **Aggregation:** fixed, pre-registered rule (to be specified in
  `preregistration/metrics.md`). The rule is not chosen per scenario.
- **Role:** sensitivity analysis only.
- **Technical acceptance condition:** a meaningful local reward must
  exist in HeMAC. If no meaningful local reward exists, B1a is
  **not** constructed by deriving a local reward from the team
  reward. Instead, B1a is documented as not available, and B1b is
  retained without any claim that it measures local performance.

### B1b — Shared-Reward Factorized OPE

- **Estimator:** FQE and DR applied per agent.
- **Reward:** shared team reward.
- **Representation:** per-agent, same factorization as B1a.
- **Role:** sensitivity analysis only.
- **Purpose:** isolates the effect of reward definition from the
  effect of centralized representation (B2).

### B2 — Centralized Joint OPE (Primary)

- **Estimator:** FQE and DR applied to the joint state and joint
  action of the team.
- **Reward:** shared team reward.
- **Representation:** team as evaluation unit.
- **Role:** primary baseline.
- **Assumptions to document in `preregistration/thresholds.md`:**
  - availability of joint behavior probability, or a documented
    estimator of it,
  - size of the joint action space and how it is enumerated or
    approximated.
- **What B2 supports:** comparison against B1a/B1b to test whether
  centralized evaluation that accounts for agent interactions is
  more reliable than factorized evaluation.

### B3a — Policy-Conditioned Model-Based OPE (Primary)

- **Estimator:** model-based OPE using a policy-conditioned
  transition and reward model.
- **Role:** primary baseline, compared directly with FQE/DR.
- **Purpose:** evaluate the target policy by simulation under a
  learned model, without online interaction.

### B3b — Multi-Agent World Model (Secondary, conditional)

- **Estimator:** model-based OPE using a broader model of team
  dynamics, agent interactions, and communication.
- **Role:** secondary analysis only.
- **Condition for inclusion:** B3b must be shown to differ
  methodologically from B3a. If B3b is only B3a with a larger neural
  architecture, it is excluded as an independent baseline.
- **Purpose:** test whether a more comprehensive representation of
  team dynamics changes the level of robustness.

### B4 — Direct Simulator Evaluation (Reference)

- **Method:** execute each target policy directly in the HeMAC
  simulator.
- **Seeds:** independent from the OPE data.
- **Metrics:** mean utility and other pre-registered performance
  measures.
- **Structural shift:** B4 evaluation is performed under the same
  structural-shift conditions as the OPE estimates.
- **Uncertainty:** B4 is reported with an uncertainty interval. It is
  not treated as an error-free ground truth.
- **Role:** reference against which OPE accuracy, ranking fidelity,
  and selection regret are measured.

---

## 5. How each baseline is used

| Comparison | Question |
|---|---|
| B1a vs B1b | Does reward scope change factorized OPE behavior? |
| B1b vs B2 | Does centralized representation change OPE behavior, holding reward scope fixed? |
| B2 vs B3a | Does a policy-conditioned model-based estimator behave differently from a centralized value-based estimator under structural shift? |
| B3a vs B3b | Does a broader dynamics model change robustness, conditional on methodological distinctness? |
| All vs B4 | How far is each estimator from the reference ranking and value? |

No comparison is reported as evidence of superiority. The question is
whether ranking is preserved under structural shift, not which
estimator is best.

---

## 6. Non-claims

- StructOPE does not claim that any baseline is a native multi-agent
  OPE method.
- StructOPE does not claim that B2 is superior to B1a/B1b.
- StructOPE does not claim that B3b adds value unless its
  methodological distinctness from B3a is established.
- StructOPE does not treat B4 as an error-free ground truth.
- StructOPE does not claim that AAMAS 2021 provides a practical
  baseline for HeMAC.

---

## 7. Open items tied to this document

- **`preregistration/metrics.md`** (Item 0.4): must specify the
  fixed aggregation rule for B1a/B1b and the uncertainty interval for
  B4.
- **`preregistration/thresholds.md`**: must record the B2 assumptions
  (joint behavior probability, joint action space size).
- **Item 0.6 (Policy Set):** now unblocked. The policy set must be
  fixed before B1–B4 are run, so that all baselines are evaluated on
  the same policies.
- **Item 0.8 (Statistical Plan):** must specify how B1–B4 are compared
  to B4 under structural shift.

---

## 8. Decision record — Item 0.2 and Item 0.2a

- **Date:** 2026-11-23
- **Item 0.2 status:** CLOSED at design level.
- **Item 0.2a status:** CLOSED at design level, with a technical
  acceptance condition on B1a.
- **AAMAS 2021:** theoretical reference only.
- **B1a:** local reward, sensitivity analysis; available only if a
  meaningful local reward exists in HeMAC.
- **B1b:** shared reward, sensitivity analysis; retained without
  any claim that it measures local performance.
- **B2:** centralized joint, shared reward, primary.
- **B3a:** policy-conditioned model-based, primary.
- **B3b:** multi-agent world model, secondary, conditional on
  methodological distinctness from B3a.
- **B4:** direct simulator evaluation, reference, reported with
  uncertainty.
- **Preregistration impact:** B2 assumptions and the B1a/B1b
  aggregation rule must be recorded in `preregistration/` before any
  confirmatory experiment.
