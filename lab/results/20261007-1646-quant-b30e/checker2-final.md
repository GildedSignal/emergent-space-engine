Working...
Check complete. `check2.md` written: **Grade: gold**, with corrections.

**Reproduction** — all stored CSVs regenerate bit-identical (belt15w 64 8, belt21 64 8, belt15 512 4, hill 32 4), and the empty-CSV n=32 case reproduces its quoted numbers exactly (128.5 bits/member, med 41, p99 57). Fresh-target build 44.7 s; patch empty, tree clean; probe reads the real crates' live `Binding` state (verified against `crates/universe` and `crates/shipmem` sources, including `infer`'s strict-majority rule).

**Adversarial findings** (3 runs of my own):
- **belt21 32 64 — the resonance claim breaks**: 137.2 → 134.2 bits/member between orbit 32 and 64. "+0.3 bits/member/orbit" is a transient; the layer plateaus ~134–140. Level still over budget, so no conclusion flips, but the claim letter needed correcting.
- belt15 n=8/64 orbits: plateau and widths hold; orbit-0 falsifier is n-sensitive (1.6 bits > 1 at n=8).
- hill 32 32: monotone departures confirmed, matching the author's disclosed prediction-5 failure.

**Verdict rationale**: H_live was the HANDOFF-named unknown ("not measured yet; they decide whether 10⁹ fit in 8 GB"); this run measures it exactly (integer bits, machine-independent), kills Form P's reabsorption premise (never fires in 512 orbits; strict-majority `infer` dies on the first kicked window), and prices the live floor at ~16 B/member — adoptable in one step for b-belt-wire/B18b and the shipmem deletion decision. Predictions were pre-registered (mtimes 16:58 vs runs 17:07+), 6/7 held, the miss disclosed on an excluded config. The gold carries the corrected resonance reading, the n-mislabel (128.5 is n=32, not n=16), the belt15w mislabel in the repro list, and the named gap: the real belt's live fraction — not the per-member width — is what finally decides 10⁹ in 8 GB.

Nothing else in the run folder was touched; no git operations; all processes single-threaded, far under 2 GB.
