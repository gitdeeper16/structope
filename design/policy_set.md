# Policy Set Design

**Status:** Item 0.6 CLOSED at design level (2026-11-23). Policy
list is a template; final list is conditional on HeMAC inventory
inspection (see §9).
**Date:** 2026-11-23
**Blocking:** Item 0.6 was blocked by Item 0.2 (CLOSED). Item 0.6
unblocks Item 1.x (Pilot).
**Related:** `design/checklist.md` §0.6; `design/baselines.md`;
`docs/decisions.md`.

---

## 1. Purpose

This document fixes the composition of the policy set used in
StructOPE. It does not fix the statistical plan (Item 0.8) or the
exact policy instances (pending HeMAC inventory). It specifies:

- how many policies,
- what kind of behavioral diversity is required,
- which reference policies are mandatory,
- how the set is used across evaluation stages,
- what conditions must hold before the set is frozen.

---

## 2. Decision summary

| # | Decision | Choice |
|---|---|---|
| 1 | Policy source | Hybrid — existing HeMAC policies + generated policies |
| 2 | Policy count | 8 (within protocol range 8–12) |
| 3 | Policy diversity | Random + Rule-based + Trained + Degraded/Ablated |
| 4 | Mandatory references | Random, Strong Coordinated Team, Single/Partial Team |
| 5 | Evaluation usage | Full Set (primary) + Reduced Set (Pilot only) |

The 8 policies are **not** eight pre-ordered performance levels.
They are eight **behavioral archetypes**. Whether OPE estimators
can recover the true ordering is what StructOPE tests, not what
StructOPE assumes.

---

## 3. Composition

Initial template (subject to §9):

| Type | Count | Purpose |
|---|---:|---|
| Random | 1 | Low-complexity reference |
| Rule-based | 3 | Distinct coordination behaviors |
| Trained | 3 | Different performance and coordination levels |
| Degraded / Ablated | 1 | Coordination-degradation test |
| **Total** | **8** | |

---

## 4. Mandatory reference policies

Three reference policies are mandatory in the Full Policy Set:

1. **Random policy** — low-complexity baseline.
2. **Strong coordinated team policy** — high team-performance
   reference.
3. **Single-agent / partial-team policy** — reference for missing
   agents or weakened coordination. Must be behaviorally definable
   in HeMAC.

**No-op policy** is an *optional diagnostic*, not a mandatory
member. Reason: if executing it causes automatic mission failure,
it may not be comparable to the other policies.

---

## 5. Mandatory references in the Reduced Policy Set

The Reduced Policy Set (3–4 policies, Pilot only) must include:

- the Random policy,
- the Strong coordinated team policy,
- at least one Rule-based or Trained policy that differs
  behaviorally from both.

This ensures that Pilot-stage work does not exclude the extremes
of the performance spectrum.

---

## 6. Evaluation usage

### 6.1 Full Policy Set (primary)

Used for the primary evaluation of all applicable baselines:
B1a, B1b, B2, B3a, B4. B3b remains conditional on methodological
distinctness from B3a.

### 6.2 Reduced Policy Set (Pilot only)

Used for:

- Pilot experiments (Items 1.1–1.3),
- debugging and iteration on the evaluation pipeline,
- early estimator characterization.

### 6.3 Rules

- The Reduced Policy Set **must not** replace the Full Policy Set
  in confirmatory results.
- The Full Policy Set **must not change** between B1a, B1b, B2,
  B3a, and B4.
- B3b may use a subset only if its methodological distinctness from
  B3a has already been established.

---

## 7. Conditions before freezing the policy set

Item 0.6 is closed at the design level. The set is **not yet
frozen**. Three conditions must be satisfied before the set is
considered final:

### 7.1 Policy identity

Every policy must have:

- a fixed definition,
- parameters,
- source,
- version,
- a reproducibility fingerprint.

No policy is accepted on name alone.

### 7.2 Behavioral diversity

Policies must be shown to differ **behaviorally**, not only in
name, code, or hyperparameters. A pre-registered behavioral
signature (to be specified in `preregistration/metrics.md`) is
required.

### 7.3 Baseline separability

The policy set must achieve a Baseline Utility Range above the
threshold fixed in `preregistration/thresholds.md`.

Provisional threshold (from the protocol): `Baseline Utility
Range > 0.01`.

If the range is below the threshold, the set is reviewed and
revised before any Confirmatory Evaluation.

**No policy may be selected on the basis of confirmatory test
performance.** Selection is based on behavioral diversity and
Baseline utility only.

---

## 8. Source policy inventory

Before the final list is fixed, HeMAC must be inspected for:

- existing trained policies that are reproducible,
- existing rule-based policies,
- whether local rewards exist for each agent (relevant to B1a in
  `design/baselines.md`),
- whether the joint action space is enumerable or
  approximable (relevant to B2).

If HeMAC provides no usable policy inventory, the 8 policies are
generated. The generated policies follow the same archetype
distribution as §3.

---

## 9. Non-claims

- StructOPE does not claim that the 8 policies span a linear
  performance spectrum.
- StructOPE does not claim that the policy set is representative
  of all coordination behaviors.
- StructOPE does not select policies based on their confirmatory
  performance.
- StructOPE does not treat the Reduced Policy Set as a substitute
  for the Full Policy Set in any confirmatory result.

---

## 10. Open items tied to this document

- **`preregistration/metrics.md`** (Item 0.4): must specify the
  behavioral signature used to verify behavioral diversity
  (§7.2), and the aggregation rule used in B1a/B1b.
- **`preregistration/thresholds.md`**: must record the numeric
  Baseline Utility Range threshold (§7.3) and the final policy
  list with fingerprints.
- **HeMAC inventory**: must be completed before the final policy
  list is fixed (§8).

---

## 11. Decision record — Item 0.6

- **Date:** 2026-11-23
- **Item 0.6 status:** CLOSED at design level.
- **Policy source:** hybrid — HeMAC existing + generated.
- **Policy count:** 8 (template), final within 8–12.
- **Policy diversity:** Random + Rule-based + Trained + Degraded.
- **Mandatory references:** Random, Strong Coordinated Team,
  Single/Partial Team.
- **Optional reference:** No-op (diagnostic only).
- **Evaluation usage:** Full Policy Set primary; Reduced Policy Set
  for Pilot only.
- **Pre-conditions for freezing:** policy identity, behavioral
  diversity, baseline separability.
- **Preregistration impact:** behavioral signature and threshold
  recorded in `preregistration/` before any Confirmatory
  Evaluation.
