# Message Semantics — Design Specification

**Item:** 0.5 (Design sub-item, related to fault injection)
**Version:** v1.1
**Status:** DESIGN SPECIFICATION — APPROVED
**Date:** 2026-11-26
**Related:** `design/fault_injection.md` Item 0.5, `design/scenarios.md` §Communication Structure, `design/checklist.md` Item 0.5, `docs/decisions.md`.

---

## 0. Scope and limitations

This document specifies the **semantics of the message** that flows from Observer to Drone through `world.observer_communication` in HeMAC. It defines what counts as a message, what counts as loss, what counts as delay, and how delivery order is interpreted.

This document does **NOT**:

- Implement any code.
- Test any mechanism.
- Modify HeMAC or `CommWrapper`.
- Define C3 (partition) or C4 (topology).
- Assign numeric severity values (Mild / Moderate / Severe).
- Claim that any fault has been implemented or tested.

It is a prerequisite for any implementation work on C1 (packet loss) and C2 (communication delay) in `CommWrapper`.

---

## 1. Message identity and source

### 1.1 Sender

`observer_0` (and `observer_i` for multiple observers).

The actual message content is the `goal_estimation` value written by the Observer in `world.observer_communication`.

### 1.2 Receiver

`drone_j` reads `world.observer_communication` inside `Drone.observe()` (drone.py:340).

Secondary receiver: `provisioner_k` (provisioner.py:249) reads the same variable.

Note: The current channel is a **broadcast channel** (single shared variable). It is not a network with per-pair links.

### 1.3 Message content

`world.observer_communication = (goal_x, goal_y)` — a tuple of two floats.

The message has no timestamp, no message ID, no sender/receiver fields. It is a shared variable, not a packet.

### 1.4 Write timing

Writing occurs inside `Observer.step()` (observer.py:102, 107), when `goal_estimation is not None` and the proximity condition holds (no-obstacle case: unconditional write; obstacle case: write only if within `comm_range` of a building).

If `goal_estimation is None` or the proximity condition fails, the Observer does **not** write.

This distinction (write event vs no-write) is fundamental for defining C1.

---

## 2. Message states — six explicit + one derived

### 2.1 Explicit event types (recorded in `comm_log`)

| Event | Definition |
|-------|------------|
| `INITIAL` | No message has been written since episode start. The channel holds the default `(500, 500)` from `world.py:47`. |
| `NO_EVENT` | Observer did not write in this step. A previous write occurred in an earlier step. |
| `TRANSMIT` | Observer wrote a new value in this step. |
| `DROP` | A `TRANSMIT` occurred, and the message was discarded by the fault injector (C1). |
| `DELAY` | A `TRANSMIT` occurred, and the message is held in a delivery queue (C2). |
| `DELIVER` | A message reaches the Drone (either immediately under C0, or after delay under C2). |

### 2.2 Derived state (not an event)

| State | Definition |
|-------|------------|
| `LAST_VALID` | The most recent successfully delivered value. Computed from the sequence of `TRANSMIT` and `DELIVER` events. Not recorded as its own event. |

**Crucial distinction:** `INITIAL` is not `LAST_VALID`. If the Observer has never written, the Drone reads `(500, 500)` as the initial default, not as a message. This distinction matters for measuring `loss_fraction` and `delayed_fraction` (see §6).

### 2.3 Transmission event count

The denominator for loss and delay fractions is the number of `TRANSMIT` events, not the number of steps and not the number of `INITIAL` or `NO_EVENT` states.

---

## 3. Decision 1 — New message

A "new message" is **every write operation** by the Observer, regardless of whether the value differs from the previous one.

**Rationale:** Fault injection is about the transmission event, not the message content. Two identical values sent in different steps have different transmission semantics (different timing, different potential for loss or delay).

---

## 4. Decision 2 — Last-valid message validity

The last valid message remains valid **without TTL** until it is replaced by a newer delivery.

**Rationale:** Simulates real-world "last-known information" that agents typically retain until update.

**Consequence:** If all subsequent transmissions are dropped (C1) or delayed (C2), the Drone continues using the last valid value.

---

## 5. Decision 3 — Delay unit

The unit of `delay_steps` is a **full team cycle**: one complete pass through all agents (Observer → Drone(s) → Provisioner(s) → back).

**Rationale:** This is the meaningful temporal unit in HeMAC's AEC loop. Using agent-step as the unit would conflate delay with agent ordering.

**Definition:** If `delay_steps = d`, a message sent in team cycle `t` becomes available to the Drone in team cycle `t + d`.

**Boundary case:** `d = 0` means immediate delivery (equivalent to C0).

---

## 6. Decision 4 — Delivery order policy

### 6.1 Fixed delay

When `delay_steps` is constant across all messages, delivery follows **FIFO delivery**: the order of arrival matches the order of transmission.

### 6.2 Variable delay

When `delay_steps` varies across messages, delivery follows **Arrival-order delivery**: messages are delivered at their actual `arrival_time`, which may invert the transmission order.

### 6.3 Independence of arrival times

Each message's arrival time is independent:

`arrival_time(msg_i) = send_time(msg_i) + delay_steps(msg_i)`

Arrival of one message does **not** reset the arrival time of another.

### 6.4 Read rule

The Drone reads the message with the **maximum `arrival_time`** among all delivered messages up to the current step.

Under fixed delay, this is equivalent to the most recently transmitted message. Under variable delay, this is the most recently arrived message, which may be older in transmission order.

---

## 7. Decision 5 — Absence vs loss

The following three states are explicitly distinguished:

| State | Transmission event? | Counted in denominator? | Counted as loss? |
|-------|---------------------|-------------------------|------------------|
| `INITIAL` | No | No | No |
| `NO_EVENT` | No | No | No |
| `TRANSMIT` + `DROP` | Yes | Yes | **Yes** |
| `TRANSMIT` + `DELAY` | Yes | Yes | No (counted as delayed) |

**Consequence:** `loss_fraction` measures the fraction of transmission events that were dropped, not the fraction of steps with no delivered message.

---

## 8. Decision 6 — Initial vs Last-Valid distinction

Two distinct states must never be conflated:

| State | Meaning | Channel holds | Counted in comm_log? |
|-------|---------|---------------|---------------------|
| `INITIAL` | No message has ever been written | Default `(500, 500)` | Yes, as an explicit event |
| `LAST_VALID` | A message was written and delivered | The delivered value | No, as a derived state |

**Impact on measurement:** A run that never transmits must not inflate the loss count. A run that transmits and then goes silent must not have its initial default counted as a "delivered message."

---

## 9. Decision 7 — Communication log structure

Every transmission-relevant step must be recorded with the following fields:

| Field | Type | Meaning |
|-------|------|---------|
| `step` | integer | Team cycle index |
| `event_type` | string | `INITIAL`, `NO_EVENT`, `TRANSMIT`, `DROP`, `DELAY`, `DELIVER` |
| `msg_id` | integer or None | Unique message ID (for FIFO and order verification) |
| `value` | tuple or None | The (x, y) tuple transmitted or delivered |
| `send_time` | integer or None | Team cycle of transmission |
| `arrival_time` | integer or None | Team cycle of delivery |
| `delay_steps` | integer or None | Applied delay (0 for C0, ≥0 for C2) |

The `comm_log` does not record `LAST_VALID` as an event. It can be derived by the analyzer from the sequence of `TRANSMIT` and `DELIVER`.

---

## 10. Decision 8 — Naming conventions

| Quantity | Notation | Definition |
|----------|----------|------------|
| Loss fraction | `loss_fraction` | `(# DROP events) / (# TRANSMIT events)` |
| Delayed fraction | `delayed_fraction` | `(# DELAY events) / (# TRANSMIT events)` |

The term "rate" is avoided to prevent confusion with delay magnitude (e.g., "delay rate" could be misread as the average `delay_steps`).

---

## 11. Example scenarios

### 11.1 C0 with periodic transmissions

| Step | Event | Value | Send | Arrival |
|------|-------|-------|------|---------|
| 0 | INITIAL | — | — | — |
| 1 | TRANSMIT | (300, 400) | 1 | 1 |
| 1 | DELIVER | (300, 400) | 1 | 1 |
| 2 | NO_EVENT | — | — | — |
| 3 | TRANSMIT | (350, 420) | 3 | 3 |
| 3 | DELIVER | (350, 420) | 3 | 3 |

`loss_fraction = 0 / 2 = 0.0`
`delayed_fraction = 0 / 2 = 0.0`
`LAST_VALID at step 4 = (350, 420)`

### 11.2 C1 with one drop

| Step | Event | Value |
|------|-------|-------|
| 0 | INITIAL | — |
| 1 | TRANSMIT | (300, 400) |
| 1 | DELIVER | (300, 400) |
| 2 | TRANSMIT | (320, 410) |
| 2 | DROP | — |
| 3 | TRANSMIT | (340, 430) |
| 3 | DELIVER | (340, 430) |

`loss_fraction = 1 / 3 ≈ 0.333`
`LAST_VALID at step 3 = (340, 430)`
(Step 2's value (320, 410) was not delivered; the Drone never sees it.)

### 11.3 C2 with fixed delay of 2

| Step | Event | Value | Send | Arrival |
|------|-------|-------|------|---------|
| 0 | INITIAL | — | — | — |
| 1 | TRANSMIT | (300, 400) | 1 | 3 |
| 2 | TRANSMIT | (320, 410) | 2 | 4 |
| 3 | DELIVER | (300, 400) | 1 | 3 |
| 4 | DELIVER | (320, 410) | 2 | 4 |

`delayed_fraction = 2 / 2 = 1.0`
At step 3, Drone reads (300, 400). At step 4, Drone reads (320, 410).

### 11.4 C2 with variable delay (Arrival-order)

| Step | Event | Value | Send | Arrival |
|------|-------|-------|------|---------|
| 1 | TRANSMIT | (300, 400) | 1 | 5 |
| 2 | TRANSMIT | (320, 410) | 2 | 3 |
| 3 | DELIVER | (320, 410) | 2 | 3 |
| 5 | DELIVER | (300, 400) | 1 | 5 |

At step 3, Drone reads (320, 410) — even though (300, 400) was transmitted first. This is Arrival-order delivery, not FIFO.

---

## 12. What this document does not define

- **C3 (partition):** Requires modeling multiple communication groups, which is not represented in HeMAC's single shared variable.
- **C4 (topology):** Requires a communication graph, which is not present in the current HeMAC structure.
- **Numeric severity values:** Mild / Moderate / Severe thresholds are PILOT-DEPENDENT and will be defined in Item 0.5b.
- **RNG seeding:** Whether the fault injector's RNG is seeded per experiment is a separate implementation concern, not a message semantics concern.
- **Observer position reset:** The current `CommWrapper` modifies `agent.x`/`agent.y` on reset, which is outside the communication scope and should be handled separately.

---

## 13. Decision record

**Status:** APPROVED (2026-11-26).

- Decisions 1–6 and the two terminology clarifications are recorded in `docs/decisions.md`.
- This document is a reference for any implementation of C1 and C2.
- C3, C4, and numeric severity remain out of scope.
- No code change, no test run, no Pilot action is claimed in this document.

**Reference basis for:** Any future work on `src/comm/wrapper.py` for C1 and C2. Any mismatch between the implementation and this document must be resolved before the implementation is considered valid.

---

**End of design/message_semantics.md (v1.1)**
