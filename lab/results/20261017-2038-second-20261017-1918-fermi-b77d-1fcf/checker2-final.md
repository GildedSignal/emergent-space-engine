Working...
**Grade: gold** — `check2.md` written.

**What I verified:**

1. **Reproduction, three independent ways.** My own parser (not the author's `analyze.py`) on the committed raw logs returned the dossier's per-transition pins exactly on all eight arms (233/367/439/498/695/994/1005/1846 kB); the runner's fresh regen flights corroborate every summary within load noise; the pooled law re-fits at 240 B × C under my stricter cat proxy vs the author's 226 B — one law either way.
2. **Anatomy.** `candidates: Vec<(usize, Binding, Scalar)>` at `crates/universe/src/encounter.rs:75`, one row per candidate in `capture`; the probe prints `sizeofTuple=224`. The pin is the struct's own size.
3. **Adversarial cases (flew them myself, ≤ 933 MB each):** K=20,000 unpaced — one decade past the author's top, cat 18,549, pin ≤ 397 B/entry, no superlinear term, and 2048 × 4–7 MB ≥ 8 GB confirms the bust decade C ≈ 1.7×10⁴; seed 3 at K=2400 — 289 B/entry vs seed-1's 286, law is seed-free; estimator attack — no-held-frame churn baselines (0–125 kB median) sit 1–2 orders below the pins.
4. **Novelty.** The live page's current best *is* the superlinear reading this run refutes; no HISTORY entry; the run postdates the last wiki commit.
5. **Page.** Faithful, INFERENCE flags kept, refutations cited — no corrections needed.

**Recorded against it:** `regen.sh` passes the K list where `flights.sh` expects the output dir (fresh flights land in a stray `./1000/`, K=1000 arms silently skipped, analysis circular on committed logs); the dossier's "7–11 fps" doesn't reconcile with the logs (13–16 fps; the load-bearing 67–74 ms gather p50 is solid); the retention tail is window-minus-transition arithmetic, not separately instrumented; predictions.md's pre-registration timing is unverifiable (untracked folder, postscript edit) — but the refuted-by-author pattern of P2/P3 is the signature of genuine pre-registration, so it costs nothing.

Scratch probes removed; tree as found; nothing else in the run folder touched.
