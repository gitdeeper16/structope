# Reduced Pilot-1 — Exploratory Data (Not Supporting Hypothesis)

**Date:** 2026-11-26
**Status:** Exploratory only. Does NOT support the structural shift hypothesis.
**Runs:** 216 (6 scenarios × 4 policies × 3 seeds × 3 repeats)

---

## ⚠️ Critical Finding

The results of this Reduced Pilot-1 **do NOT support** the hypothesis that 
structural shift affects policy ranking.

### Why?

1. **P_SINGLE ranks highest only due to a single outlier** (reward=100). 
   Without it, P_SINGLE's mean is -4.9, not -2.78.

2. **No other policy achieved any positive reward** (0/54 for P_RAND, P_RULE_A, 
   P_DEGRADED).

3. **The "non-uniform ranking" is statistical noise**, not a structural shift effect.

### What the data actually shows

| Policy | Mean | Std | Positive |
|---|---|---|---|
| P_RAND | -16.85 | 4.64 | 0/54 |
| P_RULE_A | -16.48 | 4.78 | 0/54 |
| P_SINGLE | -2.78 | 15.45 | 3/54 |
| P_DEGRADED | -17.22 | 4.48 | 0/54 |

**Only P_SINGLE achieved any positive reward** — and only 3 times out of 54.

---

## What this means

This Reduced Pilot-1 does **not** provide evidence for H1 (ranking fidelity 
degrades under structural shift). It provides evidence that:

- The current policy set (4 policies) is **not sufficiently diverse** in performance.
- The current environment setup (POI at 500,500, moving, no obstacles) 
  makes it **hard for any policy to reach the target**.
- P_SINGLE's apparent advantage is an **artifact** of one lucky run.

## What is needed for a valid Pilot-1

1. **Better policies**: P_TRAIN_H and P_TRAIN_M (trained PPO) to provide 
   meaningful upper/mid references.
2. **A more challenging but achievable environment**: obstacles, better POI 
   placement, or longer episodes.
3. **Statistical rigor**: more runs, outlier detection, hierarchical bootstrap.

## What was NOT modified

- ✅ `preregistration/pilot_scope.md` — unchanged.
- ✅ `design/scenarios.md` — unchanged.
- ✅ `design/policy_set.md` — unchanged.
- ✅ `results.json` — unchanged (raw data).

---

## File inventory

| File | Description | Size |
|---|---|---|
| `results.json` | 216 raw runs | ~80 KB |
| `README.md` | This file | (this file) |

---

**Status of Protocol-Compliant Pilot-1: NOT EXECUTED.**

**Status of this directory: Exploratory data only. Does NOT support hypothesis.**
