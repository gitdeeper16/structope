
Pilot-1 Summary (2026-11-26)
=============================

Executed: 216 runs
Scenarios: 6 (S1_1q1o, S2_3q1o, S3_3q1o_obst, S4_10q3o, S5_3q1o1p, S6_5q2o1p)
Policies: 4 (P_RAND, P_RULE_A, P_SINGLE, P_DEGRADED)
Seeds: 3 (42, 123, 456)
Repeats: 3

Rewards:
  min: -30.00
  max: 1420.00
  mean: 11.85
  std: 108.72

Ranking stability:
  NOT uniform across scenarios
  Rankings per scenario:
    S1_1q1o: P_SINGLE > P_RAND > P_DEGRADED > P_RULE_A
    S2_3q1o: P_SINGLE > P_RULE_A > P_DEGRADED > P_RAND
    S3_3q1o_obst: P_SINGLE > P_RULE_A > P_RAND > P_DEGRADED
    S4_10q3o: P_SINGLE > P_RULE_A > P_RAND > P_DEGRADED
    S5_3q1o1p: P_SINGLE > P_RAND > P_DEGRADED > P_RULE_A
    S6_5q2o1p: P_RAND > P_SINGLE > P_RULE_A > P_DEGRADED

Conclusion:
  Structural shift DOES affect policy ranking (supports StructOPE hypothesis)
