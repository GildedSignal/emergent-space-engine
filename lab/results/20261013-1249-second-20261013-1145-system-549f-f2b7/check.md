Grade: gold

**Abstract.** The checker-named experiment refutes 549f's readout half: the stored acceleration word wired at both write points (free kick-written a(B−len/2); boundary-refreshed a(B)) fails the three frozen readout gates — across-boundary velocity jump 3.85e-2 (v1 5.07e-2) against 1e-4, map-ratio 356x against 3x — while the bounded and clock gates pass: the per-read mid evaluation is load-bearing. The census's magnitude model falls too: the plane's only written word is hours stale (windows 7.7 h, err 8.3e-5 = 40% of the term, 1e4x the census). All numbers reproduce bit-exact. Deletion worth 1.45x on the gather; one write amortizes ~480 reads; at r ≤ 20 M the partial step is unreachable (holds at 10 M). Adoption: the page update — direction 1 refuted, slot to the news payload and the two-word variant.

## Reasons

**1. Reproduction (clean tree, `git apply work/patch.diff` myself; the tree was pristine at c51d3491).**
- Gates, v2: the same three failures with identical numbers — across-boundary jump 3.05e-6 of the radius / **3.85e-2 of the velocity** (frozen 5e-7 / 1e-4), worst ratio to the map **356.07x** (frozen 3x), step-squared fall FAILED; 5 passed including `the_readout_between_kicks_is_bounded` (2e-3); clock 2 passed.
- v1, rebuilt by disabling the boundary refresh (a number regen.sh does **not** regenerate): across-boundary velocity jump **5.07e-2**, exact; same three gates fail.
- Wired census: median 5.457e-7 / p99 6.402e-5 / max 8.280e-5 doll units; reads/window/body 480 coast and fwd, median 2 on the dive; digests 2437d7b2…, c4d3c2e8…, 9d4748f1… identical wired vs pristine.
- Instrument control (pristine build, same probe): error exactly **0.0**, same digests — the probe measures the wiring, not itself.
- Bench, interleaved, one round of my own on top of the runner's three: 25,829→17,127 ns/emitter scratch (**1.51x**), 12,702→8,771 memo (**1.46x**); dossier says 1.44–1.51x. 1.69 readouts/body.
- Strong field r=20 M: 4,345,751 events, 0 windows, 0 gated reads, ship alive, digest identical to regen.

**2. Predictions.** `predictions.md` predates the decisive artifacts in the folder (scripts and patch saved after it) and discloses run order inside (v1's outcome already known at write time, honestly separated from the predictions). P1 failed by its own pre-registered kill criterion — that failure **is** the refutation; P2 and P5 held; P3 half-held (1.45x vs 40–60%, multiplicity 480 vs 2–6); P4 failed the informative way (steps collapse 10^5x). All four outcomes reported accurately in the dossier.

**3. Adversarial cases (three, each outside the author's tested range).**
- **v1 rebuild** (above): the claimed 5.07e-2 is real, not an extrapolation.
- **The dive held 5x longer** (2400 frames, 40 s, β reaching 0.83, ship alive, 0 refusals — the author stopped at 8 s): wired error reaches 2.07e-3 doll units, 25x the 8-s max, but the ratio to the term stays **exactly 0.407** — a first-order quadrature whose error grows with the term it replaces, no saturation and no blow-up. The refutation's mechanism extends.
- **Strong field one decade deeper, r = 10 M** (β_circ 0.316, author tested 20 and 4000): ship survives 240 frames, ~2.84e6 events/orbit — essentially the same as r = 20 M's 3.06e6 (my 240-frame control reproduces the author's per-orbit figure) — and 0 gated reads. The "partial step unreachable at frame cadence" finding is r-independent across the tested decade.
- **Bonus instrumentation** (counters in `boundary_clock`, reverted): in the gate scene the v2 refresh fires **56,027 times** and the gate still fails 3.85e-2 — the freshest possible word, written at every handover, still breaks continuity; on plane coast/fwd it fires **0 times** — the hours-stale word is mechanically confirmed, not inferred.

**4. Novelty.** 7b86 measured the term invisible on shipped scenes and priced a pure deletion; 549f (silver; the a-word page's open direction 1, "the cheapest", expected to pass with digest identity) proposed the stored word as the accuracy-keeping replacement. No run had wired the word and faced the frozen gates, and no one had measured the plane's window length — 549f's census priced `a(B)`, which no in-flight event writes (windows 7.7 h ≫ an 8-s flight; 0 refreshes fired). docs/HISTORY.md holds no a-word entry. This run converts the page's top open direction into two refuted lines with a mechanism, and adds the unpriced cost side (1.45x, ~480x amortization). Not a repetition of either.

**5. The page.** Faithful to the evidence (every number I re-derived appears in regen.log or my reruns). Two overstatements corrected in place: "no per-window stored acceleration" → **one-word**, at either write point (the (a, ȧ) two-word completion is open direction 1 and untested); "nothing anywhere its readout is gated" → the two measured poles, with the middle regime (gated reads, visible term) named as unmeasured.

**6. Goal fit.** The shared slot of three board bottlenecks (view, gravity-news, frame-cost). Gold prong: **shows that a premise is wrong** — 549f's readout half and its magnitude model both fall, on frozen gates, with the mechanism identified (the gates freeze continuity, and a window-constant word is a first-order quadrature that jumps at every handover). PRINCIPLES 2: "Behaviours matter, not continuum fidelity: error type over error size" — the census judged by error size and missed the continuity behaviour. PRINCIPLES 9: "A failed experiment kills that configuration, never the method" — the dossier redirects to the surviving consumers instead of burying the slot. Adoption within one step: the page update; nothing enters the shipped code (the wiring is deleted with the patch — tree restored pristine).

## What the author missed

- The refutation's strongest form was one instrumentation away and was not measured: the v2 refresh fires 56k times in the gate scene and the gate still fails. The dossier argues this; a counter would have shown it.
- The claim section says "windows are 2.8×10⁹ ticks ≈ 7.7 h"; the evidence section says len = 5.6×10⁹ ticks (7.7 h). 2.8×10⁹ ticks is len/2 = 3.85 h — the claim-section figure is a typo; the evidence figure is the consistent one (1 tick ≈ 4.93 µs).
- The strong-field 0-read diagnosis (read gate vs non-clock bindings) stays unseparated (author-flags it; my r=10 M run extends the phenomenon without separating it either — counting frames with `k.clock == false` would).
- The "~480 reads amortize the write" is a plain-scene number; on the dive's own windows the median is 2, so the boundary word's extra field evaluation per step is not amortized exactly where the term is largest. The page scopes this correctly ("plain scenes"); the dossier's multiplicity paragraph could be read more broadly.
- `regen.txt` was overwritten by the runner's exit-status line; the actual regen output lives in `regen.log` (a runner artifact, not the author's — noted for the second checker).
- The wired `partial` silently falls back to the raw tube for windows no clock word covers; irrelevant to the refutation (the gates' scenes carry words), but any future variant must decide that case explicitly rather than inherit it.
