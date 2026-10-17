Working...
**Grade: gold** — written to `check2.md`, second checker, blind to the first.

**Reproduction.** Clean tree at `3dc6f621` (= `base`) + `work/patch.diff`: builds, 14/14 shipped tests pass with arms off, and every dossier row regenerates (runner's regen, exit 0; my own interleaved reruns match at draw level). `predictions.md` (02:55:29) predates every decisive log (03:00:45+); P2/P6 inversions are reported as findings, not buried.

**E = 2^rollbacks is exact in every observation** — mine included: 7→128, 6→64, 9→512. Not a fit; the mechanism.

**Adversarials (5, one outside the author's range):**
- **28,160 bodies** (outside range): finishes 149 s at **10 chronons/s, E=512** — scale-coupling and collapse continue into the next decade.
- **stagger=300**: zero rollbacks, E=1, 356 regions, but 74 chr/s — wave simultaneity drives the latch, and the many-region state is itself slow.
- **margin=1.0**: digest `49f5fc2b…` identical across arms *and* margins; decay wedged again.
- **horizon 1000**: local grinds 30 rollbacks vs shipped's 7, digest still identical.
- **relativistic 8 cells**: finishes, zero rollbacks, E=1 — law-derived margin kills conflicts at every size tried.

**The wedge is real** — DNF > 240 s for both mirror arms at 14,080 bodies (shipped 56–74 s), plus three independent wedge draws in my own session.

**One dossier overstatement found**: frames "no separation in every arm" — ES_LOCAL has a player-visible ruin tail (regen: present 286/600, 64 misses); already corrected on the page, confirmed by my evidence. I made two further page corrections: the 28,160-body "DNF at 150 s" was a timeout artifact (it finishes at ~149 s/10 chr/s, E=512 — "saturation at 2⁶–2⁸" is a band, not a cap), and added the 8-cell relativistic datum to open direction 4. Tree restored clean; nothing else in the run folder touched.
