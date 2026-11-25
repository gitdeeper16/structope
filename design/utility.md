# Utility Function — Decision Document

**Status:** CLOSED (2026-11-25).
**Item reference:** design/checklist.md §0.1
**Blocking:** Yes. Resolved.

---

## 1. Purpose

Define the scalar utility used to compute:

- Regret@k (PROTOCOL.md §9.2)
- ε threshold (PROTOCOL.md §13.1)
- Wrong-ranking event (PROTOCOL.md §13.3)

Utility is not a metric chosen to favor any OPE method. It is a
statement about what "better coordination policy" means in the
HeMAC-based setting, and it must be defensible independently of
experimental outcomes.

---

## 2. Selected components

Two components are selected.

| Component | Role | Rationale | Known limitation |
|---|---|---|---|
| Task Completion Ratio `s(π)` | Primary operational objective | The task has a binary success condition; ratio captures partial completion | Completion is not the same as success; partial credit may be generous |
| Normalized Energy Consumption `E_norm(π)` | Resource dimension | HeMAC is energy-constrained; a policy that completes the task at excessive energy cost is not equivalent | Energy depends on episode length; normalization must be defined explicitly |

**Rejected components:**

- **Completion time.** Correlated with energy in this regime;
  including both would double-count the same resource pressure.
- **Communication cost.** Undefined under full communication
  partition (C3). A component undefined under a planned
  structural-shift condition cannot enter the primary utility.
- **Coverage / exploration.** Not required by every HeMAC task.
  Including it would bias the utility toward exploration-heavy
  policies.

---

## 3. Functional form

The selected form is **success-gated linear**:

```

U(π) = s(π) · [ w_s + w_e · (1 − E_norm(π)) ]

```

**Why this form:**

- **Success-gated**: task completion multiplies the entire utility.
  A policy that does not complete the task receives U = 0,
  regardless of energy. This reflects the operational priority:
  a failed mission is not redeemed by low energy consumption.
- **Linear within the success gate**: among successful policies,
  energy trade-offs are treated as compensable. This is a design
  choice, not a physical fact.
- **Bounded**: U ∈ [0, 1] when `w_s + w_e = 1` and
  `E_norm ∈ [0, 1]`.

**Rejected forms:**

- **Pure linear weighted sum.** Would allow a failed policy to
  score high if energy is low. Incompatible with the operational
  priority.
- **Lexicographic.** Discontinuous; incompatible with Regret@k,
  which requires a scalar.
- **Multiplicative.** Scale-sensitive; requires additional
  normalization beyond what is already specified.

---

## 4. Component definitions

### 4.1 `s(π)` — Task Completion Ratio

**Definition.** Fraction of the mission objective completed by
policy π over the episode.

**Range.** `s(π) ∈ [0, 1]`.

**In HeMAC.** Defined from the environment's completion
instrumentation (number of targets reached / total targets).

**In MockAdapter.** Defined as `1.0` if any active agent reaches
the POI within the episode, else `0.0`. This is a **simulation
placeholder**, not a HeMAC measurement. Mock results are labeled
`mock` and are never used in Pilot Characterization or
Confirmatory Evaluation.

### 4.2 `E_norm(π)` — Normalized Energy Consumption

**Definition.** Energy consumed by policy π, normalized to a
reference range.

```

E_norm(π) = (E(π) − E_min) / (E_max − E_min)

```

**Range.** `E_norm(π) ∈ [0, 1]`.

**In HeMAC.** `E(π)` is the total energy consumed by all active
agents over the episode.

**In MockAdapter.** `E(π)` is the total absolute change in
`charge_level` over the episode, summed across active agents.
Again, a simulation placeholder.

### 4.3 Normalization range

`E_min` and `E_max` are **PILOT-DEPENDENT**. They are computed
from baseline (T0/C0) runs over the Full Policy Set.

**Constraint.** The same `E_min` and `E_max` must be used for:

- OPE predictions,
- B4 reference outcomes,
- all (T, C) cells.

Asymmetric normalization would make Regret@k uninterpretable.

**Before Pilot.** `E_min` and `E_max` are recorded in
`preregistration/thresholds.md` as `PILOT-DEPENDENT`. No
confirmatory evaluation runs before they are fixed.

---

## 5. Weights

### 5.1 Selected weights

```

w_s = 0.5
w_e = 0.5

```

With `w_s + w_e = 1`, so `U ∈ [0, 1]`.

### 5.2 Justification

Equal weighting is chosen for three reasons:

1. **No prior operational justification for asymmetry.** The task
   documentation does not specify a priority between completion
   and energy efficiency. Imposing one without justification
   would make the utility a statement about the authors'
   preferences rather than about the task.
2. **Sensitivity analysis covers the alternative.** If the main
   conclusions change under unequal weights, that change is
   reported. Equal weights are the neutral starting point.
3. **Preregistration constraint.** Two alternative weightings
   must be preregistered as secondary analyses. The primary
   conclusion may not depend on the choice among them without an
   explicit sensitivity statement.

### 5.3 Secondary weightings (preregistered)

| ID | `w_s` | `w_e` | Purpose |
|---|---|---|---|
| W_primary | 0.50 | 0.50 | Primary analysis |
| W_success | 0.75 | 0.25 | Success-prioritized |
| W_energy | 0.25 | 0.75 | Energy-prioritized |

All three are computed. The primary conclusion is reported under
W_primary; if it does not hold under W_success or W_energy, that
is stated in the results.

---

## 6. Interaction with ε and τ_min

- ε is defined on normalized regret. The normalization range
  therefore determines ε's meaning.
- τ_min is defined on Kendall's Tau and is independent of the
  utility scale, but not of the ranking induced by the utility.
- If utility changes, both ε and the reference rankings may
  change. This is why Item 0.1 is blocking before threshold
  calibration.

---

## 7. Sensitivity analyses

At least the following are preregistered:

1. **Alternative weighting.** W_success and W_energy (§5.3).
2. **Alternative functional form.** Pure linear weighted sum,
   reported as a secondary analysis only. If the success-gate
   changes the ranking conclusion, that is reported.

If the main conclusions do not hold under either alternative,
this is stated explicitly in the results, not buried in an
appendix.

---

## 8. Uncertainty register

The following are uncertain and are recorded as such:

| Item | Uncertainty | How addressed |
|---|---|---|
| Equal weights | No operational justification for asymmetry; equal weights are neutral, not proven optimal | Sensitivity analysis (W_success, W_energy) |
| Success-gated form | Discontinuous; may be harder for Regret@k than a smooth form | Reported as design choice; alternative form in sensitivity |
| Normalization range | `E_min`, `E_max` are not yet known | PILOT-DEPENDENT; recorded in `preregistration/thresholds.md` |
| Mock placeholders | `s(π)` and `E(π)` in MockAdapter are not HeMAC measurements | Labeled `mock`; never used in Pilot or Confirmatory |

None of these uncertainties is hidden behind arbitrary numbers.

---

## 9. Explicit non-goals

This document does not:

- Decide the OPE method.
- Decide the policy set.
- Decide the structural-shift severity levels.
- Replace the statistical analysis plan.

---

## 10. Decision record

- **Date:** 2026-11-25
- **Selected components:** Task Completion Ratio `s(π)`,
  Normalized Energy Consumption `E_norm(π)`.
- **Selected functional form:** Success-gated linear:
  `U(π) = s(π) · [w_s + w_e · (1 − E_norm(π))]`.
- **Selected weights:** `w_s = 0.5`, `w_e = 0.5` (primary);
  `W_success` and `W_energy` preregistered as secondary.
- **Normalization range:** `E_min`, `E_max` PILOT-DEPENDENT,
  recorded in `preregistration/thresholds.md`.
- **Secondary analyses:** alternative weighting, alternative
  functional form.
- **Evidence path:** `design/utility.md` §4–§7;
  `docs/decisions.md` entry 2026-11-25.
- **Preregistration impact:** weights, functional form, and
  normalization range are recorded before any confirmatory
  evaluation.
