# Self-Review — Threshold Calibration (Item 1.2)

**Status:** RECORDED (2026-11-25). R1–R7 ADDRESSED.
**Document under review:** `preregistration/threshold_calibration.md`
**Reviewer:** Samir Baladi (author; internal review)
**Date:** 2026-11-25

This self-review is recorded **before** any modification to
`threshold_calibration.md`. The purpose is to preserve the
original problems so that the revision record can be compared
against them.

No modification was made to the document during this recording.

---

## 1. Review axes

The document was reviewed on five axes:

1. Statistical validity
2. Calibration methodology
3. OPE compatibility
4. MARL considerations
5. Data leakage

---

## 2. Axis-by-axis assessment

### 2.1 Statistical validity

**Strengths:**
- The use of 10th/90th percentiles from baseline is a standard
  approach.
- Hierarchical bootstrap respects the (seed, repeat) structure.
- Between-seed and within-seed variance are separated.

**Weaknesses:**
- **W1.** The choice of 10th percentile (for ESS and Support
  Overlap) and 90th percentile (for Distributional Distance) has
  no stated justification. Why 10/90 and not 5/95 or 20/80?
- **W2.** τ_min = 0.70 has no justification in the document.
  It appears in `design/checklist.md` as an initial value, but
  the reason for 0.70 is not stated.
- **W3.** k = 3 is justified only by "half of 6 policies". If the
  Confirmatory policy set has 8 policies, k = 3 is no longer
  half. k should be tied to the Confirmatory set, not the Pilot
  set.

### 2.2 Calibration methodology

**Strengths:**
- Each threshold has a specified calibration method.
- Provisional values are documented.
- Transition conditions T1–T5 are specified.

**Weaknesses:**
- **W4.** The ESS threshold may not be meaningful if the
  importance-weight distribution is not well-behaved (e.g.,
  heavy-tailed). No diagnostic is required before computing the
  10th percentile.
- **W5.** The Distributional Distance choice (KL / MMD / TV) is
  not fixed. The criterion in §7.2 depends on the HeMAC
  distribution type, which is not yet known. This is acceptable
  as a DRAFT, but the final choice needs a documented
  justification.

### 2.3 OPE compatibility

**Strengths:**
- Thresholds are linked to Regret_eligible and ranking fidelity,
  which are OPE metrics.
- Coverage thresholds are linked to OPE assumptions.

**Weaknesses:**
- **W6.** The document does not address OPE estimator variance.
  Environment variance is estimated (via seeds and repeats), but
  OPE variance (from importance weights, bootstrap in the
  estimator, model misspecification) is not.
- **W7.** Confidence intervals are attached to threshold values,
  not to the threshold selection itself. The uncertainty in
  "which percentile" is not quantified.

### 2.4 MARL considerations

**Strengths:**
- The six policies cover different archetypes.
- Hierarchical bootstrap acknowledges structure.

**Weaknesses:**
- **W8.** No agent-level variance is estimated. Different
  policies may have different variance profiles; this is not
  accounted for.
- **W9.** No team-size effect is estimated. When T changes
  (T0 → T1), the thresholds may need to change. The document
  does not address this.

### 2.5 Data leakage

**Strengths:**
- Mock / HeMAC boundary is explicit.
- Pilot-1 / Pilot-2 separation is clear.
- Confirmatory Evaluation does not use Pilot data.

**Weaknesses:**
- **W10.** No mechanism verifies that Confirmatory Evaluation
  did not use Pilot data (e.g., checksums, run IDs).
- **W11.** The rule `ε = 1.5 × pilot baseline regret` uses Pilot
  data. This is permitted because it is preregistered. However,
  the risk is not that Pilot is used, but that calibration
  information leaks into Confirmatory in an **unrecorded** way.
  The document does not specify how calibration-derived values
  are kept separate from Confirmatory inputs.

---

## 3. Recommendations

| ID | Recommendation | Priority | Status |
|:-:|---|---|:-:|
| **R1** | Justify 10th/90th percentile choice; add sensitivity analysis | High | ADDRESSED (see REVISION_RECORD) |
| **R2** | Justify τ_min = 0.70 | High | ADDRESSED (see REVISION_RECORD) |
| **R3** | Justify the 1.5 multiplier in ε = 1.5 × pilot baseline regret | High | ADDRESSED (see REVISION_RECORD) |
| **R4** | Tie k to the Confirmatory policy set (8 policies), not the Pilot set (6) | Medium | ADDRESSED (see REVISION_RECORD) |
| **R5** | Add OPE estimator variance and uncertainty intervals | Medium | ADDRESSED (see REVISION_RECORD) |
| **R6** | Add a mechanism to verify Pilot/Confirmatory data separation | High | ADDRESSED (see REVISION_RECORD) |
| **R7** | Fix the Distributional Distance measure and justify the choice | High | ADDRESSED (see REVISION_RECORD) |

---

## 4. What is not a problem

The following were considered and are **not** flagged:

- Using Pilot data to calibrate thresholds is permitted when
  preregistered. The concern is unrecorded leakage, not the use
  itself.
- The provisional values (ε = 0.05, τ_min = 0.70, k = 3) are
  not scientific claims. They are starting points.
- The document is a DRAFT. Some open choices (e.g., distance
  measure) are expected at this stage.

---

## 5. What this review does not do

- It does not modify `threshold_calibration.md`.
- It does not close Item 1.2.
- It does not replace independent review.
- It does not authorize Pilot-1.

---

## 6. Next steps (recorded, not executed)

1. Address R1–R7 in `threshold_calibration.md`.
2. Record each change in `REVIEW/REVISION_RECORD.md` with the
   reason.
3. Send the revised document and this self-review to an
   independent reviewer (Muhammad Talha).
4. Record the independent review in `REVIEW/INDEPENDENT_REVIEW.md`.
5. Close Item 1.2 only after the independent review is complete.

No threshold changes on the basis of a reviewer's suggestion
alone. Each change requires a methodological justification and
documentation.

---

## 7. Open questions for the independent reviewer

These are recorded here so that the independent review can
address them explicitly:

- Q1. Is the 10th/90th percentile approach defensible for the
  three coverage metrics, given that they are not identically
  distributed across policies?
- Q2. Is τ_min = 0.70 a defensible initial value for Kendall's
  Tau, given that the number of policies is small (6 in Pilot,
  8 in Confirmatory)?
- Q3. Is the ε = 1.5 × pilot baseline regret rule defensible,
  or does it introduce a hidden dependence on the pilot?
- Q4. How should OPE estimator variance be combined with
  environment variance in the threshold uncertainty?
- Q5. What mechanism reliably separates Pilot-derived
  calibration values from Confirmatory inputs?
