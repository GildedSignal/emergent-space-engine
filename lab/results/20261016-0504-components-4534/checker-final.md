Working...
**Grade: silver** — written to `lab/results/20261016-0504-components-4534/check.md`, with a checker block appended to the proposed wiki page. Tree restored clean.

What I did and found:

**Reproduction** — applied `work/patch.diff` to a clean tree, rebuilt, re-flew all ten arms. Every deterministic column reproduces bit-exactly, twice (my flights and the runner's regen.log): OFF 335/229/28 with kicks 17,209 bit-identical across N=600/1e4/1e5; BEGIN leaves the storm untouched (max 335, frames 317/634, +26 stub events); GRID 141 flat in N, +0.3% kicks; seed 7 both arms exact. Only the ms column drifts with box load (regen's own 16.4 ms worst vs the dossier's 12.9) — disclosed, and the deterministic columns carry the claim.

**Gate neutrality** — main's example doesn't even link on Linux (`proc_pid_rusage`), so I flew the honest control: main's physics + the print-only Linux port. Identical columns. The author's "pre-patch binary" wording overstated what was executable; the substance holds.

**Adversarial (3+, one beyond the flown domain)** — GRID at 10⁵×seed 7: 176 (2.04×), and the +73% event inflation persists; N=3×10⁵: 143, 2.34×, storm and cure both N-flat; burn composes (p99 96→75 ms) without touching the burn's own 719-event monster; N=0 control exposed that the staggered class includes the plane's own doll≠0 ships — broader than "the 300 locals", unremarked by the author.

**Why silver** — the refutation of the page's begin-lock conjecture is real and two-sided, but the positive lever is 2.0–2.4× (not 10×), the author's own pre-registered >150 kill bar fired at seed 7 (177, honestly reported), and adoption is blocked on the slice inflation (which I traced to the fleet battle's advance quantum: +32,914 of +32,977 events are slices) and the unflown legality gates. The gold step is named: a coarser offset lattice or slice-merging rule plus the gates.
