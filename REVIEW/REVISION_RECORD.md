# Revision Record — Threshold Calibration

**Status:** IN PROGRESS (2026-11-25).
**Document:** `preregistration/threshold_calibration.md`
**Related:** `REVIEW/SELF_REVIEW.md`

This record documents each change made to the document in
response to the self-review (R1–R7). Each entry records:

- what was changed,
- why it was changed,
- what was **not** changed,
- what remains uncertain.

No change is recorded as "resolved" until the corresponding
recommendation is closed.

---

## Revision R1 — 10th/90th percentile

**Status:** ADDRESSED (2026-11-25).
**Sections modified:** §5.2, §6.2, §7.3.

### What was changed

- Added a justification for the 10th percentile (ESS, Support
  Overlap) and 90th percentile (Distributional Distance).
- Added a sensitivity analysis for each: 5th/95th, 10th/90th
  (primary), 20th/80th.
- Stated explicitly that 10th/90th is an **initial design
  choice**, not a statistical fact.
- Stated that any change in classification between the extreme
  percentiles is reported, not hidden.

### What was not changed

- The primary choice remains 10th/90th. It is not claimed to be
  optimal.
- No threshold value is fixed in this revision. The values are
  still PILOT-DEPENDENT.

### What remains uncertain

- Whether 10th/90th is robust across HeMAC scenarios. This is
  tested in Pilot-2.
- Whether the three percentile choices (5th, 10th, 20th) lead to
  materially different conclusions. This is recorded in the
  Pilot-2 analysis, not decided now.

---

## Revision R2 — τ_min = 0.70

**Status:** ADDRESSED (2026-11-25).
**Section modified:** §9.2.

### What was changed

- Added a justification: 0.70 is a provisional design choice,
  not a statistical fact.
- Explicitly rejected the inference from "Kendall's Tau >= 0.70
  is strong agreement" to "tau_min = 0.70 is an OPE threshold".
- Added a sensitivity analysis: 0.60, 0.70 (primary), 0.80.
- Added a freeze rule: not frozen until Pilot-2 data are
  available.

### What was not changed

- The primary provisional value remains 0.70.
- The rule (lower to 5th percentile if needed) is retained.

### What remains uncertain

- Whether 0.70 is achievable for the best OPE estimator under
  baseline. This is tested in Pilot-1.
- Whether 0.60 and 0.80 lead to materially different
  conclusions. This is recorded in the Pilot-2 analysis, not
  decided now.

---

## Revision R3 — ε = 1.5 × pilot baseline regret

**Status:** ADDRESSED (2026-11-25).
**Section modified:** §9.1.

### What was changed

- Added a justification: 1.5 is a design margin of 50%, not a
  statistical constant.
- Added a sensitivity analysis: 1.25, 1.5 (primary), 2.0.
- Added a freeze rule: not frozen until Pilot-2 data are
  available.

### What was not changed

- The primary provisional value remains 1.5.
- The rule structure is unchanged.

### What remains uncertain

- Whether 1.5 is the right margin for HeMAC. This is tested
  in Pilot-2.
- Whether 1.25 and 2.0 lead to materially different
  conclusions. This is recorded in the Pilot-2 analysis, not
  decided now.

---

## Revision R4 — k tied to Confirmatory set

**Status:** ADDRESSED (2026-11-25).
**Section modified:** §8.

### What was changed

- The provisional value of k changed from 3 to 4.
- k is now explicitly tied to the Confirmatory policy set
  (8 policies), not the Pilot set (6 policies).
- Added a sensitivity analysis: k = 3, 4 (primary), 5.
- Added a freeze rule: not frozen until Item 1.3.

### What was not changed

- k is still not chosen to maximize Top-k accuracy.
- The operational justification is still required.

### What remains uncertain

- Whether k = 4 is the best operational choice for HeMAC. This
  is reviewed after Pilot-1.
- Whether k = 3 and k = 5 lead to materially different
  conclusions. This is recorded in the Pilot-2 analysis, not
  decided now.

---

## Revision R5 — OPE estimator variance

**Status:** ADDRESSED (2026-11-25).
**Section modified:** §10 (rewritten as §10.1–§10.6).

### What was changed

- Added §10.1 (environment variance, existing).
- Added §10.2 (OPE estimator variance): bootstrap inside the
  estimator, with resampling unit chosen per estimator type.
  Agent-level observations are kept together. Temporal
  structure is preserved. Importance weights are resampled
  with their transitions.
- Added §10.3 (total variance): the covariance term is not
  assumed to be zero. The decomposition
  V_total = V_environment + V_OPE + 2*Cov is stated explicitly.
  When Cov cannot be estimated, the two components are
  reported separately and no total is reported.
- Added §10.4 (uncertainty on threshold selection): the
  percentile itself is reported with a confidence interval,
  and the threshold is computed at 5th, 10th, 15th, 20th (or
  80th, 85th, 90th, 95th) to check stability.
- Added §10.5 (reporting format): every threshold is reported
  with all fields, not collapsed.
- Added §10.6 (what is not done): no component is assumed
  zero; no total is reported without justification.

### What was not changed

- The primary threshold values are still PILOT-DEPENDENT.
- No threshold is frozen in this revision.

### What remains uncertain

- Whether the covariance term can be estimated reliably for
  HeMAC. This is tested in Pilot-2.
- Whether the percentile stability holds across HeMAC cells.
  This is recorded in the Pilot-2 analysis.

---

## Revision R6 — Pilot/Confirmatory separation mechanism

**Status:** PARTIAL (2026-11-25). Documented, not yet implemented.
**Sections modified:** §12.1, §12.2, §12.3, §12.4 (new).

### What was changed

- Added §12.1: six separation mechanisms (directory, prefix,
  checksum, provenance, frozen thresholds with version tag, seed
  separation with explicit exceptions).
- Added §12.2: verification procedure V1–V6.
- Added §12.3: what the mechanism does not prevent.
- Added §12.4: status (DOCUMENTED, not yet implemented).

### What was not changed

- The Mock/HeMAC boundary (§12) is unchanged.
- The calibration rules are unchanged.

### What remains to close R6

- A verification script that implements V1–V6.
- A test of the script on synthetic data.
- The result of the test recorded in `docs/decisions.md`.

### Verification

- Script: `scripts/verify_separation.py` (V1-V6).
- Tested on synthetic data (clean, pilot_ prefix, indirect
  reference).
- Result: recorded in `docs/decisions.md`.

### Status update

**R6 = ADDRESSED (2026-11-25).** The mechanism is documented,
implemented, and tested.

---

## Revision R7 — Distributional Distance measure

**Status:** ADDRESSED (2026-11-25).
**Section modified:** §7.2 (rewritten as §7.2.1–§7.2.7).

### What was changed

- §7.2.1: comparison unit fixed before distance choice (U1,
  U2, U3).
- §7.2.2: KL restriction — no ad-hoc smoothing; excluded if
  support overlap is not verified. MMD specification includes
  bandwidth rule.
- §7.2.3: evaluability test on Pilot-1 data only.
- §7.2.4: decision criteria applied to all passing candidates,
  all reported. No candidate selected for convenience.
- §7.2.5: decision authority is the researcher, with documented
  justification. Independent reviewer may comment but does not
  choose.
- §7.2.6: choice uses Pilot-1 data only, fixed before Pilot-2.
- §7.2.7: what is not done.

### What was not changed

- The threshold itself remains PILOT-DEPENDENT (90th percentile
  of baseline).
- The Mock/HeMAC boundary is unchanged.

### What remains uncertain

- Which distance and unit will pass the evaluability test on
  HeMAC data. This is determined in Pilot-1.
- Whether the chosen distance leads to a stable threshold.
  This is tested in Pilot-2.

---

## Revision R7 — addendum (2026-11-25): five methodological amendments

**Status:** ADDRESSED (2026-11-25). Freeze complete; V7 verified on four test cases (A: no V7_PASSED -> fail; B: with V7_PASSED -> pass; C: hash mismatch -> fail; D: spec missing -> fail).

**Sections modified:** §7.2.1, §7.2.2, new file `preregistration/r7_mmd_spec.md`,
`scripts/verify_separation.py` (V7 added).

### Amendments applied

1. **Comparison unit fixed to U2.** §7.2.1 previously listed U1/U2/U3
   without selection. U2 is now fixed in §7.2.1 and in
   `r7_mmd_spec.md` §1, with justification and rejection reasons for
   U1 and U3.

2. **Zero-support threshold defined.** §7.2.2 previously required
   "support overlap verified" without an operational definition.
   `n_min = 30` is defined with a planned sensitivity check at
   {20, 30, 50}. The result of the sensitivity check is recorded after
   Pilot-1 data are available, not assumed.

3. **MMD specification frozen.** New file `preregistration/r7_mmd_spec.md`
   specifies kernel (Gaussian RBF), bandwidth rule (median heuristic),
   data representation (L1-normalized p(a|s) on a fixed action grid),
   reference set (Pilot-1 seeds only), and insufficient-sample handling
   (<50 vectors → pooled bandwidth). The file is sha256-pinned before
   any Confirmatory run.

4. **V7 added to `verify_separation.py`.** V7 fails if the MMD spec
   file is missing, the sha256 does not match, or Confirmatory outputs
   exist without a `V7_PASSED` line in `results/RUN_LOG.md`.
   **V7 is a detection mechanism, not a prevention mechanism.** The
   Confirmatory launcher must call `verify_separation.py` and abort on
   failure.

5. **Decision authority explicit.** §7.2.5 already records the
   researcher as decision authority; the addendum does not change this,
   but confirms that the choice recorded here is the researcher's.

### What was not changed

- The threshold itself remains PILOT-DEPENDENT.
- KL remains excluded for this study (rule recorded, not used).
- The Mock/HeMAC boundary is unchanged.

### What remains uncertain

- Pilot-1 data are not yet available. The bandwidth values, the U2
  grid resolution in `thresholds.md`, and the sensitivity-check
  result for `n_min` are all recorded after Pilot-1.
- The freeze step (sha256) must be executed before Pilot-2. If the
  file is edited after freeze, V7 fails and the addendum is reopened.
