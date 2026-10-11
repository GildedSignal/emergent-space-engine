Working...
Check complete. `check.md` written; tree restored to its starting state (only untracked `lab/results/`).

**Grade: silver.**

What I did, and what it showed:

- **Reproduced everything.** All four dossier commands in a clean tree with the patch applied by me: lattice 20/20 (new equivalence test included), lattice-event 19/19 (Chronon bit-identity), scaling table matches, engine cost test passes. Every mean in the dossier's table recomputes exactly from the author's raw 3-rep files.
- **Timings confirmed — interleaved.** My first sequential A/B was polluted by co-scheduling (gas 16384 showed −46%, impossible for a pure arithmetic change). Alternating the two binaries 5× each: medians **+10.2–14.5% on all five contact-dense tracks, every dense rep positive**; dilute tracks +5–10% and noisy — same order as the author's numbers, which stand.
- **Exactness attacked independently.** 340k-case differential fuzz with my own RNG at the guard's exact corners, tangency-heavy sweeps, and deep axis-aligned searches — all equal to the i128 truth. Six engine worlds the author never ran (new seeds, fills, both relativistic laws, Bounce): digests bit-identical across trees. Re-derived the domain proof: no i64 product can overflow inside the guard, and the `xb−xa` subtraction adds no new envelope.
- **Why not gold:** a constant factor that deletes nothing (the author concedes this); all four held-out magnitude predictions failed 2–4× low (only the bit-identity constraint held); and the gain sits on dense CPU tracks that the barbell routes to Metal, while the real consumer (the plane's cost test) measures ≈0.
- **The gold experiment:** the profile's own map — a covering certificate that batches re-predictions per cell's pairs (the visit loop's 43%) or a calendar without per-later sift-down; a ≥10× cut in visits per fired event at unchanged digests is the next run's lever.
