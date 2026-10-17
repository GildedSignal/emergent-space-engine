# dossier — 20261017-2142-taleb-8fb9 (taleb lens)

**Claim.** The compact store's period/phase quantization is innocent of the comb on the shipped
chained clock: a belt of 99,700 bodies sharing as few as ~25 period classes and 4 phase classes
(~100 combos; a draw-battalion of ~1,000) flies inside the shipped draw's frame envelope at every
fire window and on both seeds — because the chained clock's next-due word carries per-body integer
state (first-plan bits plus the measured ~2.6×10⁻⁴/fire step drift) that no draw class determines,
so the comb's home is the law's anchor rule (`aligned`), not the store's quantization. Calendar
open direction 4 closes negative; the checker's "train lifetime vs step spread" rule resolves to:
lifetime ≤ 2 fires at every tested quantization, the operative spread being the per-body per-fire
step change, not the population's draw spread.

**Bottleneck.** Memory at 10⁹ (the scoreboard's ~10^2.6 gap): the 21–40-bit belt store was the one
population where the chained clock could still comb (calendar od 4), so the store-class decision
(od 3) carried an unpriced frame-letter risk. This run prices it at zero on the live law: no
schedule-bit fence exists at any quantization down to ~6.6 bits of (period, phase). What it lets us
delete: any comb-motivated extra bits or de-phase machinery on the compact belt's schedule axis.

**Evidence** (all from `belt_comb`, a new example flying the shipped `scenario::plane_extra`
population, N = 100,000 — 99,700 belt bodies, 300 locals, seed 1 unless said — one rtf-100 frame at
a time with `Budget::unlimited`, so the frame's count is the true dues; 5 fire windows of 6×10⁹
ticks each ≈ 5 belt fires; the belt draw quantized in `scenario::ladder_ship` by env: A-shift =
log₂ coarsening of the semi-major-axis grid (Python replica of the shipped mix64 draw: 194 classes
at s=27, 97 at s=28, 49 at s=29, 25 at s=30), PHASE-shift = low-bit zeroing of the Q32 genesis
phase):

| arm (seed 1) | w0 max | steady max (w2–4) | steady ge≥400 | total events |
|---|---|---|---|---|
| CTRL shipped draw | 487 | 343–367 | 0 | 1,455,164 |
| PER s=27 (194 periods) | 517 | 344–369 | 0 | 1,455,149 |
| PHASE p=8 | 487 | 343–367 | 0 | 1,455,164 |
| BOTH s=28 p=2 | 507 | 351–373 | 0 | 1,455,131 |
| BOTH s=29 p=1 (49 periods) | 482 | 341–365 | 0 | 1,455,099 |
| BOTH s=30 p=1 (25 periods) | 492 | 336–371 | 0 | 1,455,023 |
| ANCHOR s=30 p=30 (25×4 ≈ 100 combos) | 501 | 334–368 | 0 | 1,454,966 |
| ANCHOR s=30 p=29 (25×8 ≈ 200 combos) | 478 | 340–364 | 0 | 1,455,052* |
| CTRL seed 7 | 487 | 358–387 | 0 | 1,605,791 |
| BOTH96 seed 7 | 480 | 348–369 | 0 | 1,605,710 |

*anchor200 total = the file's own events_total counter; every arm's total is within 0.01% of CTRL's — quantization
moves where dues land, never how many (P7 held). Steady max in every arm is the locals comb's own
range (the 334-class standing storm, reproduced as a built-in control — max exactly 334 at
N=2,000, the record's number), not belt structure. The genesis train (w0: 21–31 frames ≥ 400
events, max ~490–517 in every arm) decays to ≤ 1 frame by w1 and 0 by w2 **in every arm including
the 100-combo anchors**: the train's lifetime is ≤ 2 fires at every quantization. Wall cost of the
worst steady frames 10–15 ms at ~30 µs/event (Linux x86, order-of-magnitude only), identical
across arms. Machine: 8 vCPU, load 0.4–1.5, 14.2 GB available (`work/arms/machine.txt`); runs
~60 s each, peak well under the 2 GB budget.

**Predictions** (`predictions.md`, written before any flight): P1 held (CTRL reproduces the
genesis-train shape and the quant run's census). P2 held (PER innocent). P3 **refuted as
worded**: phase quantization at p=8 is invisible (487 = CTRL's 487) — my parameterization error,
p bits leave 2^(32−p) phase classes, so p=8 is near-continuous; the predicted rails needed p ≥ ~24.
P4/P5's intent (shared-anchor battalions) was tested by the ANCHOR arms after the error was found:
**no battalion at fire 1 either** — w0 max 501/478 ≈ CTRL's 487, where an aligned anchor would put
a ~1,000-event (or ~12,500, for the phase-0 class) frame. The pre-written kill criterion fired:
steady max ≤ 1.03× CTRL (criterion: ≤ 3× ⇒ kill the standing-comb premise). P6 held (seed 7
identical in structure). P7 held (totals ±0.01%).

**What would make it wrong.** (1) The census is frame-level (338,343 ticks/frame): a battalion
narrower than a frame would still show as one counted frame — none exceeds CTRL — but tick-level
alignment was not directly censused (b4a8's next-due instrument saw per-body spread on the
continuous draw; mine infers it). (2) Five fires only: a comb forming late (past 5 fires) has no
mechanism — the drift only spreads, and every body's step already changed by fire 3 (b4a8) — but
it is not excluded by measurement. (3) The live engine's promotion path does not exist yet: my
claim scopes the live law, where every body carries its own next-due word. A compact store that
**regenerates** next-due = anchor + full(class) at promotion, discarding per-body state, would
re-manufacture shared ticks by construction — that door is open, and it is the one measurement the
promotion topic should take (see the wiki fold). (4) One draw family (uniform a in [2,3) AU,
Rayleigh e); other families could correlate e with the classes, though e does not enter `full`.

**Cost of adopting.** None: the patch is env-gated and inert at 0/0 (shifts by zero are the
identity — CTRL is the shipped draw, and its stream reproduces the record's locals comb exactly).
What may be deleted downstream: schedule-bit fences and de-phase machinery on the compact belt's
store axis.

**Fit with PRINCIPLES.** "A fix signals the wrong representation" (19) — the comb was a property of
`aligned`'s absolute grid, and chasing it into the store's quantization was chasing the wrong
representation; "delete before optimizing" (1) — the fence this run deletes was unbuilt weight on
the store design; "behaviours over many seeds" (20) — two seeds, identical structure; "the
simulation decides" (22) — the law's own per-body word, not the draw, decides the schedule.

**The lens.** Taleb: I looked for the composition ruin (store quantization × chained clock) and
found the engine antifragile to it by construction — the per-body carry is a self-staggering
mechanism older than any design intent. What the lens may have missed: I nearly shipped the
phase-parameterization error as a positive result (P4/P5 "confirmed" by arms that tested nothing);
the pre-registered combo arithmetic (P4's battalion sizes) is what exposed it — the falsifier, not
the lens. And the blind spot named in the card cuts both ways: a no-op result is only gold if the
instrument can see the effect it denies (the 334-control and the ANCHOR re-run are that proof).
