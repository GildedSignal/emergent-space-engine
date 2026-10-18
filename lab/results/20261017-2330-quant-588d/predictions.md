# Predictions — 20261017-2330-quant-588d

Question: what is the sharing rate of the fit's compile keys on flown inputs
(read-stream open direction 2: "measure shape-key sharing on flown fit inputs
before designing anything")? The census counts, at `from_state` (the one compile
site the fit owns), three levels: exact `ShapeKey`, the 44-bit `MemoCode`, and
the memo's actual shape-class key (`shape_bits`, 17-bit on the weak branch).
Instrument: print-only, env-gated (`FIT_CENSUS=1`), at `space/src/binding.rs`;
controls: `ladder_digest "N=3000 coast through"` identical pristine vs patched
with the census OFF and ON; positive control: the N=0 plane arm must reproduce
memo.rs's kick-rebind finding (quantized hit > 0.9), since the plane's heavy
rebinders (planets, moons) are in both censuses.

Cases not tuned on (I have not run anything yet; these are pre-registered):

- P1 (exact level, belt): over ALL from_state fits on `nladder 3000 coast`
  the exact-key hit rate is > 0.5 — because boundaries/word rebinds re-fit the
  body's unchanged orbit between kicks (kick-cadence's no-op boundary
  "reproduces the previous interval and step exactly" implies the same key),
  unlike memo.rs's kick-only census (< 0.05). If P1 fails, boundaries do not
  re-enter from_state, and the exact memo stays dead on the bind path too.
- P2 (shape level, belt): the shape-class hit (what an `Arc<OrbitShape>` memo
  would serve) is >= 0.95 at N=3000 — the weak-branch 17-bit class is coarser
  than one belt birth-band, and ENVELOPE.md says weak shapes share tables.
- P3 (memory): distinct shape classes over a 60-s window scale sub-linearly in
  N between 3000 and 10^4 (<= 2x for 3.3x bodies) — classes are shared across
  bodies, so the memo's memory is class-count x shape bytes, not per-body.
- P4 (held-out N and horizon): N=10^4 has hit rates within 0.02 of N=3000;
  a longer horizon (rtf 1800 vs 600) moves the shape hit by < 0.05 (the belt
  rebinds its own cells; the wave does not mint new classes at depth).
- P5 (negative control, exact level on kicks): on the N=0 plane the exact hit
  stays < 0.1 while the quant hit is > 0.9 — memo.rs's law, extended from the
  kick path to every from_state call the plane makes.

Kill criterion (written before the run): if the shape-class hit at N=3000 and
N=10^4 is < 0.5, the shape memo is dead on the bind path (the compile's 49%
must fall another way) and this run records the kill. If it is >= 0.9 with
distinct classes << bodies, the memo's design space is priced (hit, classes,
bytes) and adoption is the law-change decision memo.rs already names.
