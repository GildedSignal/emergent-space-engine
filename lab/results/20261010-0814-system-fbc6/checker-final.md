Working...
Check complete. **Grade: silver** — written to `lab/results/20261010-0814-system-fbc6/check.md`.

**Basis:**

- **Reproduced bit-for-bit.** All three runs (`a`: 34.8 s, `b`, `c`) regenerate identical JSON (`cmp` clean); `check.py` reproduces every dossier number: keep-forever 38.3/198.7/806, flatline 200.0 vs exact 199.7, frontier 220→2,620 (+400/frame) vs naive 221→9,941, parent chain 108 predicted / 99–123 steady.
- **Five adversarial cases, all passed:** held-out λ=2.0 (211 vs 200 predicted, over-retention 9.4× = R/r_q); eccentric readers e=0.6 (zero misses at the bound — the author's untested claim holds); no-resolvable-reader edge; v=0.9c (constant +100/frame); non-nested cones from two players (constant +800/frame).
- **Why not gold:** the load-bearing sentence — retention = influence radius / c, the cursor, the ghost mechanism — is R5 of the Opus math memo already in the repo (cited honestly). The run operationalizes the radius as r_q = √(G·m/Q) and quantifies the naive doll-radius over-retention, but its headline 44× is against KEEP-FOREVER, a strawman; vs the real alternative (TTL=R, itself bounded) the gain is a workload-dependent constant. And three of the six "held" predictions are definitional: run C's zero contribution is an `if` statement, run A's zero-miss is a one-line theorem of the toy's own premises.
- **One experiment to gold:** wire the death rule into the real `b-news-gravity` chain (queued, unbuilt) on the B12 scene with the accumulator (sub-quantum news crossing the parent's quantum) actually modeled — the link run C assumes and the one place the bound could break.
- **Minor reporting slips recorded:** half-bound miss range is actually 528–1,324,779; run C's t=500 transient (60) sits outside the quoted 99–123; predictions promised 4 λ values, 3 ran.

Folder state: only `check.md` added; `work/` and all author files untouched; scratch removed; no git commands run.
