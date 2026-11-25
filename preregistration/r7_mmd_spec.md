# R7 — Distributional Distance Specification (MMD)

**Status:** FROZEN (date filled after sha256 step).
**Decision authority:** Samir Baladi (researcher).
**Data source for the choice:** Pilot-1 only.
**Fixed before:** Pilot-2 start and before any Confirmatory run.
**Related:** `preregistration/threshold_calibration.md` §7.2.1–§7.2.7.

## 1. Comparison unit (fixed)

**U2 — state-conditioned action distributions p(a|s).**

- Distances are computed between p(a|s) of two policies at matched states.
- U1 (policy distributions) rejected: couples policy with environment.
- U3 (state-action visitation) rejected: frequency ≠ behavior.

### 1.1 Operational definition of "matched states"

For discrete HeMAC state spaces: exact state identity (s_i = s_j).

For continuous or large discrete HeMAC state spaces:

- State space is discretized **using a fixed grid defined in
  `preregistration/thresholds.md` before Pilot-1**, not learned from data.
- The grid resolution is fixed at design time and is not adjusted after
  seeing Pilot-1 or Pilot-2 data.
- Two observations are "matched" if they fall in the same grid cell.
- If HeMAC states are only partially observed, the observed component is
  used for matching; the hidden component is not imputed.

This definition is repeated in `preregistration/thresholds.md` under
"U2 operational definition", and both files must agree at freeze time.

## 2. Zero-support threshold (KL only)

KL is **not** the primary distance in this study. It is listed as a
candidate in §7.2.2. If KL is selected later (it is not selected here),
the following rule applies:

- A bin is "unsupported" if it has fewer than `n_min = 30` reference
  observations.
- KL is computed only if no target bin falls in an unsupported reference bin.
- Sensitivity: `n_min ∈ {20, 30, 50}` is evaluated on Pilot-1 data.
- **The result of this sensitivity check is recorded after Pilot-1 data
  are available, not assumed in advance.** If the three values disagree
  on any exclusion decision, the most conservative (largest `n_min`) is
  used and the disagreement is documented.

**This study does not select KL.** The rule above is recorded because
§7.2.2 lists KL as a candidate and the rule must exist for completeness.

## 3. Primary distance: MMD with Gaussian RBF kernel

### 3.1 Kernel

- Family: **Gaussian RBF**, k(x, y) = exp(-||x - y||² / (2σ²)).
- Bandwidth σ is set by the **median heuristic** on the reference set.
- No other kernel is used in the primary analysis.

### 3.2 Data representation and normalization

- Input to MMD is the **action distribution vector** p(a|s) over the
  fixed action grid (see `preregistration/thresholds.md`).
- Vectors are L1-normalized so each sums to 1.
- **No additional feature normalization is applied** to the p(a|s)
  vectors. They are already probability vectors.
- If the action grid differs between cells (T, C), the union grid is
  used, with zero-padding for missing actions. This is recorded as a
  design choice, not inferred from data.

### 3.3 Bandwidth computation (median heuristic)

- Reference set: the **Pilot-1 confirmatory-style sample** for each cell
  (T, C), using seeds `seed_a`, `seed_b`, `seed_c` only.
- Pairwise squared distances are computed between all p(a|s) vectors in
  the reference set.
- σ² = median of the **off-diagonal** pairwise squared distances.
- The bandwidth is computed **once per cell** and frozen.
- Bandwidth is **not recomputed** on Pilot-2 or Confirmatory data.

### 3.4 Handling insufficient samples

- If a reference cell has fewer than **50 p(a|s) vectors**, the bandwidth
  for that cell is **not computed from that cell**. Instead:
  - The pooled Pilot-1 bandwidth (across all cells with ≥50 vectors) is
    used, and the substitution is recorded.
  - If pooled is also insufficient (<50 vectors total), the cell is
    excluded from MMD-based reporting and this exclusion is documented.
- An "insufficient" cell is reported, not silently dropped.

### 3.5 Distance computation

- MMD² is the unbiased estimator with the Gaussian kernel above.
- Bootstrap CI: 1000 resamples over seeds (not repeats), per §7.2.3.
- Computation is done once per cell pair and stored in
  `results/tables/mmd_pilot1.csv` before any Pilot-2 data exist.

## 4. What this specification does not do

- It does not select KL. KL remains excluded for this study.
- It does not select the distance threshold. The threshold is
  PILOT-DEPENDENT per `threshold_calibration.md` §5.
- It does not fix the U2 grid resolution. That is in
  `preregistration/thresholds.md` and must be frozen before Pilot-1.
- It does not authorize Confirmatory runs. Authorization requires V7 pass
  (see §5) and `verify_separation.py` success.

## 5. Freeze procedure

1. `preregistration/thresholds.md` is updated with the U2 operational
   definition and the grid resolution (see §1.1 above).
2. The sha256 of this file is computed and stored in
   `preregistration/r7_mmd_spec.sha256`.
3. `verify_separation.py` V7 checks that:
   - this file exists,
   - the sha256 matches,
   - `RUN_LOG.md` records a `V7_PASSED` line **before** the first
     Confirmatory output appears (enforced by the Confirmatory launcher,
     not by V7 alone).
4. After freeze, this file is read-only. Changes require a new version
   with a documented addendum in `REVIEW/REVISION_RECORD.md`.

## 6. Post-Pilot-1 additions (do not edit this file)

The following are recorded in `preregistration/thresholds.md` **after**
Pilot-1 data are available, not in this frozen file:

- Sensitivity result for `n_min ∈ {20, 30, 50}`.
- Per-cell median bandwidth values.
- The union action grid actually used.
- Any cell excluded under §3.4.
