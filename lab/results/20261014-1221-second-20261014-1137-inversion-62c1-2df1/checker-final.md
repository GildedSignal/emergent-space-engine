Working...
Check complete. `check.md` written: **Grade: silver.**

**What I did** (45 min, clean tree, patch applied by me):

- **Reproduced everything I ran**: steady map p50 1.18/1.39/1.69/**1.67 ms** at 10³–10⁶ (author: ~1–3), belt 10⁶ at 1.15 ms/64 served, fills 21 ms→23.7 s, wire 19–29 KB, turn free (40.9 ms max ≈ steady p99), sky honestly non-collapsed (19.9 ms, 1,778 readouts), baseline 22.6 ms ≈ 62c1's 21.5.
- **Proved byte-identity independently**: the author's blake3 digest `8387a46c…` reproduces, *and* my own dependency-free hash of the same View stream is identical on pristine vs patched trees (`9bc02df6…`, half and final). The refactor is genuinely verbatim — `gather_rows` shares `gather_cached`'s own helpers.
- **Adversarial**: (1) rtf 1000 — a decade above the author's only rtf — holds (4.8/5.6 ms p50 at 10⁴/10⁵); (2) **the steady p99 is Θ(N)**: 37/360/3,483 ms at 10⁴/10⁵/10⁶ from the birth/death scan stand-in (~3.5 µs/body, every 240 frames) — the collapse is p50-only, and smoothness is explicitly p99 (PRINCIPLES #12); (3) diagnosed the author's "undiagnosed" belt-zoom residue via `DISP_DEBUG`: single-pixel anchor drift on accelerating near-field rows, zero misses/ghosts — slack calibration, not structure; (4) the 10⁶ audit (author ran none) didn't finish in my window — 10⁶ display-exactness stays unverified by either of us.

**Silver, not gold**: the flyability claim rests on an unbuilt engine half (the birth feed — the run's own code says the event counter is useless for births at belt scale), and adoption needs policy + feed + client wiring, not one step. Named experiment for gold: build the feed, delete the scan, show steady **p99** ≤ 16.7 ms at 10⁵–10⁶ with the audit on.

**Corrections made to the run's wiki page**: p99 caveat added to Current best; the Refuted line's "the page can now carry it" qualified to p50 + feed; the birth feed named as the missing half in Open directions; the belt residue diagnosis folded into Contradictions. Also recorded: the dossier's evidence table was left empty (`fill-dossier.sh` never run) and `regen.sh` overruns the harness timeout (exit 124), though every command reproduces individually.

Tree restored to the runner's state (patch applied, my probe example removed); nothing else in the run folder touched beyond `check.md` and `wiki/view.md`.
