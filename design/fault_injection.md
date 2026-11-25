# Fault Injection — Design Specification

**Item:** 0.5 (Design)
**Phase:** 0.5a — Design Specification
**Status:** SPECIFICATION ONLY. No implementation. No testing.
**Date:** 2026-11-25
**Decision authority:** Samir Baladi (researcher).
**Related:** `design/checklist.md` Item 0.5, `design/scenarios.md` Part C,
`preregistration/thresholds.md`, `docs/decisions.md`.

---

## 0. Scope and phase split

This document specifies the fault-injection layer **for HeMAC**.
It does **not** implement it, and it does **not** test it.

Item 0.5 is split into three phases:

| Phase | Scope | Status |
|---|---|---|
| 0.5a | Design specification (this document) | IN PROGRESS → closes when this file is approved |
| 0.5b | Implementation on HeMAC | DEFERRED — requires HeMAC source tree |
| 0.5c | Determinism test | DEFERRED — requires 0.5b |

**This document makes no claim that any fault has been injected,
implemented, or tested.** It is a specification only.

No Mock is used. Fault injection on a Mock would test the injection
mechanism, not its ability to represent HeMAC faults, and would not
satisfy Item 0.5's acceptance criterion.

---

## 1. Design principles

### 1.1 Hybrid injection: Wrapper first, Patch only when required

- **Wrapper (preferred):** an external layer that intercepts the
  interface between HeMAC and the runner. The wrapper modifies actions,
  observations, or inter-agent messages **without modifying HeMAC code**.
- **Patch (exception):** a direct modification of HeMAC code. Used
  **only** when the fault cannot be represented faithfully at the
  wrapper boundary (e.g., faults that depend on HeMAC-internal
  scheduling or agent-internal state).
- Every patch must be:
  - minimal in scope (single file, single function where possible),
  - documented with the reason why a wrapper could not represent the
    fault,
  - recorded in §6 (Patch Register).

### 1.2 Two separate determinism claims

The specification distinguishes **two independent properties**:

1. **Fault-generator determinism.** Given the same seed, the same
   fault schedule is produced. This is a property of the fault
   generator, independent of HeMAC.
2. **Environment-response determinism.** Given the same seed and the
   same fault schedule, HeMAC responds identically. This is a property
   of HeMAC **under faults**, not of the fault generator.

The two are tested separately in 0.5c. A failure of (2) does not imply
a failure of (1), and vice versa. The specification requires (1); it
records (2) as an open question until HeMAC is available.

### 1.3 No numeric severity values before HeMAC inspection

Severity levels (Mild / Moderate / Severe) are defined as **ranges**
and **operational criteria**. No numeric values are invented in this
document. Numeric ranges are filled in 0.5b, after HeMAC's parameter
scales are known.

### 1.4 Timing dimension

Every fault type declares which timings it supports:

- **before an episode** — at episode initialization,
- **during an episode** — between two consecutive steps,
- **between episodes** — between episode termination and the next
  initialization.

The timing dimension is part of the specification, not an
implementation detail.

---

## 2. Team-composition injection

All four types are in scope. For each: trigger mechanism, severity
range, and supported timings.

### 2.1 Agent dropout

- **What it removes:** one or more agents from the active team for a
  bounded or unbounded duration.
- **Trigger mechanism:** declared at wrapper boundary. An external
  scheduler selects agents and a duration; the wrapper removes their
  actions from the joint action and their observations from the joint
  observation.
- **Severity (ranges, filled in 0.5b):**
  - Mild: fraction of active agents removed is small; duration is
    short relative to episode length.
  - Moderate: fraction and duration are both non-trivial.
  - Severe: fraction is large and/or duration spans the full episode.
- **Supported timings:** before episode, during episode, between
  episodes.
- **Determinism:** the selection of agents and durations is a
  deterministic function of (seed, episode index, step index).

### 2.2 Capability degradation

- **What it changes:** one or more agents remain present but their
  effective action set, sensing range, or action reliability is
  reduced.
- **Trigger mechanism:** wrapper intercepts the agent's action and
  either masks a subset of the action space, reduces the observation
  window, or applies a declared noise level to the action.
- **Severity (ranges):**
  - Mild: small reduction in effective action set or small noise.
  - Moderate: substantial reduction.
  - Severe: near-total loss of the agent's effective capability.
- **Supported timings:** before episode, during episode, between
  episodes.
- **Determinism:** the masked subset, window, and noise are functions
  of (seed, agent id, episode index, step index).

### 2.3 Agent replacement

- **What it changes:** one agent is replaced by a different agent
  (different policy, different capability profile) mid-run.
- **Trigger mechanism:** wrapper swaps the agent's policy reference at
  a declared boundary. The old agent's internal state is discarded or
  transferred according to a declared rule.
- **Severity (ranges):**
  - Mild: replacement with a similar-capability agent.
  - Moderate: replacement with a different-capability agent.
  - Severe: replacement with a degraded or adversarial agent.
- **Supported timings:** between episodes only. Replacement during an
  episode is not supported in 0.5a; if HeMAC requires it in 0.5b, a
  new decision entry is added.
- **Determinism:** the agent id, replacement target, and boundary are
  functions of (seed, episode index).

### 2.4 Team-size change

- **What it changes:** the number of agents is changed (increase or
  decrease). Distinct from dropout (which is temporary) and
  replacement (which is 1-for-1).
- **Trigger mechanism:** wrapper adds or removes agents at a declared
  boundary; added agents use a declared initialization policy.
- **Severity (ranges):**
  - Mild: small change relative to baseline team size.
  - Moderate: substantial change.
  - Severe: change that qualitatively alters the coordination
    problem (e.g., single-agent vs multi-agent).
- **Supported timings:** before episode, between episodes. **Not**
  during an episode in 0.5a (see 2.3 same restriction).
- **Determinism:** the size trajectory is a function of (seed,
  episode index).

---

## 3. Communication injection

All four types are in scope. For each: physical-layer model,
parameter range, determinism under seed.

### 3.1 Packet loss

- **Physical-layer model:** each outbound message is independently
  dropped with probability p_loss, or dropped in bursts according to a
  declared burst model.
- **Parameter range (filled in 0.5b):** p_loss ∈ [p_min, p_max] with
  burst parameters; values chosen after HeMAC's baseline message rate
  is known.
- **Severity:**
  - Mild: low p_loss, no bursts.
  - Moderate: moderate p_loss or short bursts.
  - Severe: high p_loss or long bursts.
- **Supported timings:** during episode, between episodes.
- **Determinism:** the drop decision is a function of
  (seed, sender, receiver, step index).

### 3.2 Communication delay

- **Physical-layer model:** each message is delayed by d steps or by a
  real-time amount, according to a declared delay distribution.
- **Parameter range (filled in 0.5b):** d ∈ [d_min, d_max] with a
  distribution family (fixed / uniform / heavy-tailed) declared here.
- **Severity:**
  - Mild: delay small relative to decision horizon.
  - Moderate: delay comparable to decision horizon.
  - Severe: delay exceeds decision horizon (messages arrive stale).
- **Supported timings:** during episode, between episodes.
- **Determinism:** the delay value is a function of
  (seed, sender, receiver, message sequence number).

### 3.3 Network partition

- **Physical-layer model:** the team is split into two or more
  groups; messages between groups are blocked for a declared duration.
- **Parameter range (filled in 0.5b):** number of partitions, group
  sizes, partition duration.
- **Severity:**
  - Mild: brief partition, small group split.
  - Moderate: substantial split or longer duration.
  - Severe: partition spans the full episode or isolates a critical
    agent.
- **Supported timings:** during episode, between episodes.
- **Determinism:** partition assignment and duration are functions of
  (seed, episode index, step index).

### 3.4 Topology change

- **Physical-layer model:** the communication graph changes (edges
  added or removed) according to a declared trajectory. Distinct from
  partition (which is a special case of edge removal).
- **Parameter range (filled in 0.5b):** number of edges changed,
  change schedule, whether changes are reversible.
- **Severity:**
  - Mild: small topology perturbation.
  - Moderate: substantial topology change.
  - Severe: topology becomes disconnected or star-like.
- **Supported timings:** before episode, during episode, between
  episodes.
- **Determinism:** the edge trajectory is a function of (seed,
  episode index, step index).

---

## 4. Severity definitions (operational criteria, no numeric values)

Severity is defined by **operational criteria** relative to the
baseline condition, not by absolute numeric values.

| Level | Operational criterion |
|---|---|
| Mild | The fault is present but does not change the qualitative nature of the coordination task; a reasonable policy can still solve it without adaptation. |
| Moderate | The fault changes the qualitative nature of the task; a reasonable policy needs to adapt (or accept degraded performance) to remain functional. |
| Severe | The fault substantially changes the task or removes capabilities required for baseline performance; without adaptation, the policy is expected to fail or degrade severely. |

Numeric thresholds corresponding to each level are **filled in 0.5b**,
after HeMAC's baseline scales are known. No value is invented in 0.5a.

---

## 5. Timing matrix

| Fault type | Before episode | During episode | Between episodes |
|---|---|---|---|
| Agent dropout | yes | yes | yes |
| Capability degradation | yes | yes | yes |
| Agent replacement | no | no | yes |
| Team-size change | yes | no | yes |
| Packet loss | no | yes | yes |
| Communication delay | no | yes | yes |
| Network partition | no | yes | yes |
| Topology change | yes | yes | yes |

Cells marked "no" are **design restrictions**, not implementation gaps.
If HeMAC requires a restriction to be lifted in 0.5b, a new decision
entry is added to `docs/decisions.md`.

---

## 6. Patch Register

**Status:** empty until 0.5b.

Each patch entry (added in 0.5b) must record:

- HeMAC file and function patched,
- fault type and severity level supported by this patch,
- reason why a wrapper could not represent this fault,
- the minimality argument (why this patch is the smallest possible),
- the seed determinism argument.

No patch is added in 0.5a. This section is a placeholder.

---

## 7. Determinism specification

### 7.1 Fault-generator determinism (required)

The fault generator is deterministic given:

- a seed,
- a fault configuration (types, severity levels, timing profile),
- a schedule of episodes and steps.

Formally: `fault_schedule = G(seed, config, episode_step_grid)`, where
`G` is deterministic. The same inputs produce the same schedule.

The generator's source of randomness is a single seeded PRNG,
independent of HeMAC's PRNG. This guarantees that the fault schedule
does not depend on HeMAC's internal random behavior.

### 7.2 Environment-response determinism (open, requires HeMAC)

Given the same seed and the same fault schedule, HeMAC's response is
expected to be identical, but this is **not** specified in 0.5a. It is
tested in 0.5c.

A failure of 7.2 does **not** imply a failure of 7.1. The two
properties are independent, and 0.5a only commits to 7.1.

### 7.3 Recording of schedules

Every fault schedule produced during a run is recorded as a structured
log with:

- the seed,
- the fault configuration,
- the full schedule (type, timing, target, parameters, outcome),
- a hash of the schedule.

The determinism test in 0.5c compares these hashes across repeated
runs with the same seed.

---

## 8. Acceptance criteria for 0.5a (this phase)

0.5a is closed when **all** of the following hold:

- This document exists and covers all eight fault types (four
  team-composition, four communication).
- Every fault type declares trigger, severity range (as criteria, not
  numbers), supported timings, and determinism arguments.
- The Patch Register (§6) is present and empty with the correct
  schema.
- Determinism (§7) distinguishes fault-generator determinism from
  environment-response determinism.
- No claim of implementation or testing is made anywhere in this
  document.
- `docs/decisions.md` records that 0.5a is complete and 0.5b/0.5c are
  deferred.

0.5a does **not** close Item 0.5. Item 0.5 remains PARTIAL until 0.5b
and 0.5c are complete.

---

## 9. Acceptance criteria for 0.5b and 0.5c (deferred)

Recorded here for traceability; not in scope of 0.5a.

- **0.5b:** wrapper and patches implemented; each fault type exercised
  at least once on HeMAC; Patch Register populated; numeric severity
  ranges filled in.
- **0.5c:** determinism test run with repeated seeds; fault schedule
  hashes compared; environment-response determinism recorded or its
  failure documented.

Both 0.5b and 0.5c require HeMAC source tree. Neither can be started
before HeMAC is available.

---

## 10. What this document does not do

- It does not implement any fault injection.
- It does not test any fault injection.
- It does not fix numeric severity values.
- It does not claim that HeMAC's response to faults is deterministic.
- It does not close Item 0.5.
