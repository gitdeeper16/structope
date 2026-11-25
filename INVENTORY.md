# StructOPE — Inventory

**Version:** 1.0.0 (executed protocol)
**Date:** 2026-11-25 (last updated)
**Author:** Samir Baladi
**ORCID:** [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
**License:** CC-BY-4.0 (documentation) + MIT (code)
**DOI (this version):** [10.5281/zenodo.24473998](https://doi.org/10.5281/zenodo.24473998)
**DOI (all versions):** [10.5281/zenodo.24473997](https://doi.org/10.5281/zenodo.24473997)

---

## Research Status

| Item | Status |
|---|---|
| Document type | Pre-registered protocol, executed |
| Phase | ✅ Published (v1.0.0) |
| Item 0.1 (Utility) | ✅ CLOSED |
| Item 0.2 (Baselines) | ✅ CLOSED (6 estimators: B1a, B1b, B2, B3a, B3b, B4) |
| Item 0.3 (Training strategy) | ✅ CLOSED |
| Item 0.4 (Coverage metric) | ✅ CLOSED (MMD Gaussian RBF, n_min = 30; sensitivity 20/50) |
| Item 0.5 (Fault injection) | ✅ CLOSED (8 types × 3 severities × 3 timings) |
| Item 0.6 (Policy set) | ✅ CLOSED (6 policies: P_RAND, P_RULE_A, P_SINGLE, P_TRAIN_H, P_TRAIN_M, P_DEGRADED) |
| Item 0.7 (Reference execution) | ✅ CLOSED (frozen + sha256) |
| Item 0.8 (Statistical plan) | ✅ CLOSED |
| Experiments | ✅ 1,296 runs (Pilot-1: 324, Pilot-2: 540, Confirmatory: 432) |
| Pilot | ✅ Completed |
| Confirmatory | ✅ Completed |
| Final verdict | 🟡 Under review (Decision E) |

---

## Root Files

| File | Purpose | Status |
|------|---------|:-:|
| `README.md` | Main documentation (18.5 kB) | ✅ |
| `PROTOCOL.md` | Full protocol (19.4 kB) | ✅ |
| `AUTHORS.md` | Contributors (1.5 kB) | ✅ |
| `CHANGELOG.md` | Version history (1.7 kB) | ✅ |
| `CONTRIBUTING.md` | Contribution guidelines (1.5 kB) | ✅ |
| `INVENTORY.md` | This file | ✅ |
| `ROADMAP.md` | Phase + item status (3.2 kB) | ✅ |
| `PROJECT_SUMMARY.txt` | One-page summary (4.8 kB) | ✅ |
| `OSF_REGISTRATION.md` | OSF preregistration text (48.3 kB) | ✅ |
| `CITATION.cff` | Citation metadata (1.0 kB) | ✅ |
| `VERSION` | Version identifier (`1.0.0`) | ✅ |
| `LICENSE` | CC-BY-4.0 (docs) + MIT (code) | ✅ |
| `verify_separation.py` | V1–V7 separation verifier | ✅ |

---

## Directories

| Directory | Contents | Status |
|-----------|----------|:-:|
| `docs/` | `paper/`, `figures/` (12 PNG), `decisions.md`, `SELF_REVIEW.md` | ✅ |
| `preregistration/` | `r7_mmd_spec.md`, `pilot_scope.md`, `thresholds.md` | ✅ |
| `design/` | `fault_injection.md`, `policy_set.md` | ✅ |
| `src/` | `ope_estimators.py`, `mmd_distance.py`, `fault_injection.py` | ✅ |
| `tests/` | 66 automated tests | ✅ |
| `experiments/` | `pilot1/`, `pilot2/`, `confirmatory/` | ✅ |

---

## Package Distribution

| Artifact | Size | Status |
|----------|------|:-:|
| `structope-1.0.0-py3-none-any.whl` | 25.4 kB | ✅ PyPI |
| `structope-1.0.0.tar.gz` | 41.4 kB | ✅ PyPI |
| `structope.zip` (full bundle) | 11.7 MB | ✅ Zenodo |
| `StructOPE_Research_Paper_v1.0.0.pdf` | 1.7 MB | ✅ Zenodo |

---

## Persistent Identifiers

| Resource | Identifier | Status |
|---|---|---|
| Zenodo (this version) | [10.5281/zenodo.24473998](https://doi.org/10.5281/zenodo.24473998) | ✅ |
| Zenodo (all versions) | [10.5281/zenodo.24473997](https://doi.org/10.5281/zenodo.24473997) | ✅ |
| OSF Preregistration | [10.17605/OSF.IO/EZJKF](https://doi.org/10.17605/OSF.IO/EZJKF) | ✅ |
| Figshare | [10.6084/m9.figshare.35117266](https://doi.org/10.6084/m9.figshare.35117266) | ✅ |
| PyPI | [pypi.org/project/structope](https://pypi.org/project/structope/) | ✅ |
| ORCID | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) | ✅ |

---

## Repository Mirrors

| Platform | URL | Status |
|---|---|---|
| GitHub | https://github.com/gitdeeper16/structope | ✅ Primary |
| GitLab | https://gitlab.com/gitdeeper16/structope | ✅ Mirror |
| Gitea | https://gitea.com/gitdeeper16/structope | ✅ Mirror |
| Codeberg | https://codeberg.org/gitdeeper16/structope | ✅ Mirror |
| Bitbucket | https://bitbucket.org/gitdeeper16/structope | ✅ Mirror |
| Website | https://structope.netlify.app | ✅ |

---

## Verification Summary

| Check | Status |
|---|:-:|
| Automated tests | ✅ 66 passed |
| V1–V7 separation checks | ✅ Passed |
| Fault-injection determinism | ✅ Confirmed |
| Paper (PDF) | ✅ 1.7 MB |
| Figures (PNG) | ✅ 12 |
| Experiments executed | ✅ 1,296 runs |
| Stage separation enforced | ✅ |

---

**StructOPE v1.0.0 — pre-registered protocol, executed.**
© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance
DOI: [10.5281/zenodo.24473998](https://doi.org/10.5281/zenodo.24473998)
