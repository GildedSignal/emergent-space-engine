Working...
Check complete. **Grade: gold**, written to `lab/results/20261019-2339-second-20261019-2017-inversion-cc9d-ee4d/check.md`; the author's wiki page needed no correction; tree restored clean.

**What I did (45-min budget):**

- **Reproduced from scratch** (patch applied to a clean tree, private build): disease 1e5 max **849 ms** — one player item `[0,0,0,1,0]` carrying 16,132 nested kicks — vs cure **16.0 ms**, p99 11.9, **0 mega-frames**; identity at 5e4 `796b472e…fcd` off == on, counters equal; test hygiene 8/2 exactly as claimed, and with the flag unset the patch is the shipped path by construction.
- **Four adversarial cases outside the author's domain, all holding:** identity at **2e5** (four arms, `265303ce…`), a **2× deeper cut** (60k game-s, `9dc5ff9a…`), collapse at **3e5** (max 13.9 ms, 1.0 GB), and the rtf price (0.694×, inside the disclosed band).
- **One boundary found:** at **rtf 2000** the cure's term is dead (mega-frames 0, crest = 1,247 cheap ship items inside budget) but a different unbudgeted cost takes over — `encounters: capture` at **41.8 ms inside one player item**, p99 39.6. The claim's domain (rtf ≤ 1000) is untouched; this names the true next wall for adoption.
- **Novelty:** the wiki carried the direction open from cc9d; no prior run built the cure or proved identity through a wave. Page diff is two append-only additions, faithful, caveats kept visible.

Gold because: independently reproduced at every rung including three out-of-domain extensions; the spike moves 50–120× and deletes the 8.1–9.5 µs × K law; adoption is one named step. The naive control's powerlessness is a scene property, disclosed against the author's own prediction, and the order-freedom it leaves unproven rests on the shipped code's own documented invariant plus bit-equality across five scene-settings.
