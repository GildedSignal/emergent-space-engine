Working...
Check complete. **Grade: silver** — written to `lab/results/20261014-0450-scout-b29a/check.md`, page corrected in place, tree restored clean.

**Reproduction:** applied `work/patch.diff` myself in a clean tree at base 8498d1c. Every deterministic number bit-identical to the author's `run.log` (REL arms n=24576, WIDEGRADE 2189/1907/0, BYTES 40.00 B/event, QUANT 3.0/7.6, IDENT 0/4096, all six SCALE lines); timings within shared-box noise (refit 19.6 vs 19.8 µs, keykick 0.103 vs 0.104).

**Adversarial (5 cases, 3 outside the author's domain):**
- **N=65536:** linear, no new term; but arm-agreement tail hits 7.7e-8 (median 1e-11) — the author's "≤1e-9" was asserted on a log printing `0.000`.
- **Hot band [256,512) M:** holds everywhere.
- **Eccentric σ0.3/e≤0.9:** correctness holds, but composed cost ≈ 76 µs — the 13× headline is 6.4× there. The cost is σ-dependent; the dossier doesn't say so.
- **Δv/v=1:** refit refuses 9–26%, `Key::new` out-of-domain 10–13%, key-arm stays at the birth floor on survivors — the "refusal is the regime trigger" story is observed, not just asserted.
- **Far band [16384,18432) M: the composed path cannot enter** — `Key::darwin` caps at p ≤ 8192 M while the store's `Spec` allows to 65536 M. A hard domain edge the author never names; adoption needs band-splitting or an invariants-direct row→key path.

**Silver, not gold:** two of six pre-registered predictions failed at face value (P3, P6 — both disclosed, and I confirmed the author's mechanism readings: identity at 8.25e-13 relative E matches their 8e-13, though their L figure 1.4e-10 does not reproduce, I get 2.5e-9); the gold-carrying key-space arm still awaits the encounters tier's exact integer ΔE/ΔL (their own wrong-maker #1); the 13× is cold-belt-only. One experiment to gold: rerun both arms with c7eb's real contact impulse on cold + eccentric belts, with the darwin-domain statement folded in.

The 12 B scar is real, not hypothetical — my anchored-delta in-order run measures 12.07 B/event exactly. Novelty confirmed against the wiki (frame-cost priced only the sticky path; nladder rule 4 named but never built the ephemeral promotion; no prior key-space arm on the record). Page corrected: the "7.6 E-quanta" mislabel (it's the L floor; E's is 3.0), checker domain notes added, Runs entry graded.
