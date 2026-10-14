# Predictions — written after tuning on seed 3 flying only (and one OFF battle-pace arm)

Tuned on: s3/m400/rtf100 (policies 2/3/4 swept there; s3 battle OFF measured). Everything
below is about cases not yet measured: held-out seeds 7 and 11, battle pace ON arms, and the
composition with the warm start.

- **P1 (probes, the frozen rule's tail).** At every seed × pace, policy 3 (guarded AB-IQI)
  holds worst ≤ 20 probes per search (rule: ≤ 30) and mean ≤ 15 (s3 flying measured 10.7,
  worst 14). Held-out seeds behave like s3 because the crawl mechanism is geometric, not
  seed-specific; battle pace's worst stays ≤ 28 + slack.
- **P2 (leaver cut).** Leaver kick median falls ≥ 25 % vs OFF at flying pace at every seed
  (s3: −34.7 %). At battle pace the search share of a fired kick is smaller, so I predict
  ≥ 15 % there — and count it as a miss against the gold condition if < 25 %.
- **P3 (identity).** Canonical and replay digests bit-identical OFF vs ON at every seed ×
  pace; refused 0; the crate equality test passes for every policy 1–4 (fast = slow on every
  dipping tube of a settled plane, two surfaces, two starts).
- **P4 (kill rows regenerate).** Policy 1 (plain secant) reproduces the author's kill row
  exactly wherever re-measured (s3 flying: 35,621 probes, worst 57 — already confirmed);
  policies 2/4 replace the two unregenerable rows with correctly-wired variants that I
  predict *pass* the frozen rule (the earlier runs' Illinois/AB variants lost their gain to
  the retention discipline: the retained side must decay, the fresh side must reset).
- **P5 (composition with the warm start, 0b85).** Warm + policy 3 keeps every digest
  bit-identical to warm-off and to plain shipped, fires no fallback regression, and its
  total probe count is ≤ the warm start alone at the same arm (warm deletes whole searches
  that moved < 1 tick; policy 3 cuts the probes of those that did not — the two savings are
  on disjoint sets, so they add).
