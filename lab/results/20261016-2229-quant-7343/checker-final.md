Working...
Check complete. Final state: tree restored (only `lab/results/` untracked), `check.md` written, the author's page corrected in place.

**Grade: gold** — `lab/results/20261016-2229-quant-7343/check.md`

What I did:

1. **Reproduced** from `work/patch.diff` on a clean tree: all deterministic cells bit-identical (candidates = distinct entries, 0 encounters, same probe bodies), timings in band.
2. **Held-out + adversarial, three of my own:**
   - **Seed 3** (held out): core holds — but the kept band-edge window reads at **6.0 µs/read** on 8.9-knot tables, falsifying the dossier's "3.6–4.5 µs everywhere"; the traj *share* (85.5%) is the invariant, not the price.
   - **N = 10⁶ seed 3** (a decade past the author's range): holds fully — fallback ×3, 999,714 candidates all distinct, 3.87–3.94 µs/read, traj 87–89%, warm 1.12–1.15×, reuse walk 310–321 ms, linear in N. (Note: this run of *mine* peaked at 3.0 GB RSS; the author's 10⁵ cap was wise.)
   - **Code audit**: the probe is verbatim the shipped decision path (`encounter.rs:174–194`, `Scan::compute`); the reuse-walk mechanism is real — `capture` builds the whole candidate list before `same_inputs`; `Cycle::state` matches the "structural, not wrapper" reading.
3. **Novelty**: no prior run splits the read (cdf0 timed whole reads; `cost_split.rs` is the kick).
4. **Page corrections** where it overstated: "89%" → 85–90% fallback / 74–86% kept (non-solve peaks at 26%, still never the 50% a 2× needs), per-read not a constant, "0.5 s/s" → 0.24–0.5 s/s, restored 1250's checker caveat lost in conflict resolution, and marked the kill's boundary (the closed-form-kernel cheaper read survives as a re-certified law, not an optimization).

The non-regenerating dossier cells (four timing cells, ≤10% off, all from disclosed single runs — including the "(89%)" annotation on a row that computes 80%) are recorded in the check but don't touch the verdict: this is the gold-4643 shape — a measured ceiling that kills one named cure and redirects effort to the phase-neighbour rank or the population answer.
