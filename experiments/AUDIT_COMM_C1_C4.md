# Communication Mechanism Audit — C1–C4

**Date:** 2026-11-26
**Status:** C1–C3 are NOT functionally implemented. C4 is partially implemented.

---

## What was tested

For each level C0–C4, we ran 50 steps with `Observer` NOT placed on top of the POI.
We tracked `world.observer_communication` after each step.

## Results

| Level | `observer_communication` | Unique values | Functional? |
|---|---|---|---|
| C0 | (500, 500) | 1 | ✅ baseline |
| C1 | (500, 500) | 1 | ❌ NOT functional |
| C2 | (500, 500) | 1 | ❌ NOT functional |
| C3 | (500, 500) | 1 | ❌ NOT functional |
| C4 | (500, 500) | 1 | ⚠️ partially (sensing_range changes) |

## Why C1–C3 are not functional

`observer_communication` is only updated by `Observer` when it detects the target.
When `Observer` does not detect the target (the normal case), `observer_communication`
remains at its default value `(500, 500)`.

The `CommWrapper` can only modify `observer_communication` AFTER it has changed.
Since it never changes (when Observer is not on top of the target), the wrapper has
no effect.

## What C4 does

C4 reduces `Observer.sensor.sensing_range` from 75 to 30. This affects whether
Observer can detect the target. But it does not directly modify `observer_communication`.

## What would be needed for functional C1–C4

1. **Modify `HeMAC.py`** to add a communication layer that can drop, delay, or
   partition messages before they reach the drone.
2. **Or** intercept `Observer.observe()` and `Drone.observe()` to filter messages.
3. **Or** modify `observer_communication` to be a queue with configurable
   delivery semantics.

None of these are implemented in the current `CommWrapper`.

## Recommendation

- **C0** is usable as baseline.
- **C4** is usable as a partial topology change (sensing_range reduction).
- **C1, C2, C3 are NOT usable** in their current form.

Do not report C1–C3 as "implemented" in any Pilot-1 or Confirmatory analysis
until they are functionally implemented and verified.

---

**Status of C1–C3: NOT FUNCTIONAL.**
**Status of C4: PARTIAL.**
