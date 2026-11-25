# Changelog

All notable changes to StructOPE are documented in this file.

---

## [1.0.0] — 2026-11-23

### Added
- Initial pre-registration release.
- Research question: structural robustness of multi-agent OPE under
  team-composition and communication-structure shift.
- Sub-question: uncertainty-aware selective evaluation.
- `PROTOCOL.md` (677 lines) — full protocol.
- `design/checklist.md` — phase-0 items with BLOCKING / NON-BLOCKING
  classification.
- `design/utility.md` — utility specification (Item 0.1 CLOSED).
- `design/scenarios.md` — training strategy (Item 0.3 CLOSED) and
  scenario grid; reference execution protocol (Item 0.7 OPEN).
- `docs/decisions.md` — decision log.

### Closed Items
- Item 0.1 (Utility): Task Completion Ratio + Energy (Quadcopters
  only), completion-gated, 0.5/0.5 weights, normalized to baseline
  range without clipping, fixed regret denominator.
- Item 0.3 (Training Strategy): baseline-only training (T0/C0),
  held-out structural shifts at evaluation, at least one fully
  unseen (T, C) cell withheld from all prior stages.

### Open Items
- Item 0.2 (Baselines) — BLOCKING.
- Item 0.4 (Coverage metric).
- Item 0.5 (Fault injection).
- Item 0.6 (Policy set) — blocked by 0.2.
- Item 0.7 (Reference execution protocol) — partially specified.
- Item 0.8 (Statistical plan) — BLOCKING.

### Not Run
- No experiments.
- No implementations.
- No confirmatory evaluation.
- No pilot data yet.

### DOI
- 10.5281/zenodo.24473998

---

**StructOPE v1.0.0 — pre-registration**
© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance
DOI: [10.5281/zenodo.24473998](https://doi.org/10.5281/zenodo.24473998)
