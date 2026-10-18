Grade: gold

**Abstract.** The μ = 1e-2 runaway tail is a root-clock event storm on minted ejections —
not captures, not the doll's octave; chaos-shadowing direction 3 is answered. Reproduced
bit-for-bit: 10/144 ICs capped in 16 P holding 52.3% of 1.98M events; all 10 capped ICs end
ejected 9.2–19 sep (I traced the two the author skipped), doll 0, handoffs 0; the drift law
dt = Δs·f′(y) is exact once Δs's round-down to a power of two (2⁻²⁶) is applied — A = 2.6176
shipped against 2.618 measured, dissolving the dossier's "30% gap"; ratchet 6.52e-7/kick
one-signed, β up to 0.713; freeze 7.5e-9 P. Held-out: 32 P → 31/144 capped (70% of events);
μ = 3e-2 at 8 P → 19/144 (80%); μ = 1e-3 at 128 P → 0. Gain: μ = 1e-2 unflyable as built,
the capture-cascade line deleted, the fix redirected to one object. Adoption cost: none.

## Reasons

**Reproduction** (clean tree at `55972278`, `work/patch.diff` applied by me, fresh build):
- Both ensemble screens reproduce **bit-identically per IC** (events, kicks, capped, alive
  equal on all 288 ICs; only wall-clock differs): m2-16 totals 1,979,458 events, 10/144
  capped holding 52.3%, 9 dead, median 230 kicks/P; the μ=1e-3 control 0 capped, top IC
  0.9%, 10 dead, median 276 kicks/P.
- Deep traces identical to the tick: my ka2 ends t = 7.331 P, v = 0.1991, interval 132;
  my kb (1.5M) ends t = 14.982 P, v = 0.7133, interval 10 — same end states as the author's.
- `analyze.py` on the saved `work/` prints every dossier number (it is the fixed parser;
  the author disclosed the fix-phase repair).
- Determinism and chunk-invariance verified: an IC rerun is identical; CHUNK 20000 vs
  100000 identical physics ("chunking preserves canonical bits" holds).
- The runner's `regen.sh` exit 124 is its timeout, not a failure: the fixer's end-to-end
  regen exited 0, and every component reproduces here in well under 60 s each.

**Predictions.** `predictions.md` (05:51:43) predates `screen.sh` (05:51:49), the first
screen (05:51:56), the 16 P ensemble (05:52:40) and every trace (06:02+). The decisive P2
storm clause held exactly; P1 (captures — the wiki's leading hypothesis) honestly refuted;
P3's concentration number wrong (top-decile 52%, not top-1 ≥ 25%) with the fatness right;
P4 held and worsened; P5a refuted, P5b/P5c held. The control median 276 sits 2% above
their own 230–270 band (the wiki's 267 is a different grid and horizon), but the operative
control — zero caps, top ≤ 5% — passed.

**Attack** (three cases of my own, one beyond the author's domain):
- μ = 1e-2 at **32 P** (2× the horizon): 31/144 capped, **70% of all events**, 14 dead —
  the storm is an ongoing arrival process; the 16 P snapshot understates the ruin.
- μ = **3e-2** at 8 P: 19/144 capped, 80% of events — mass gates the arrival rate from the
  other side; μ = 3e-2 is catastrophically unflyable.
- μ = 1e-3 at **128 P** (2× the control): 0 capped, median 276 kicks/P — the μ gate holds
  (and e846/b9be already finished 512 P at μ = 1e-3).
- The two capped ICs the author never traced: both end ejected (14.82 sep, v 0.076;
  10.16 sep, v 4.0e-4 = 20× local escape), doll 0, handoffs 0 — "every capped IC ends
  ejected" is now 10/10. The second mints through the register first (y monotone
  1.8e-10 → 1.8e-7, intervals 5e11 → 1.5e7 falling) and obeys the **full two-term**
  identity dt·y = Δs·(1/y + 1/b) to 0.02% — the law reading is exact, not approximate.

**Novelty.** Wiki direction 3 was open ("captures → ever-shorter radial periods … or a
genuine event storm … decides whether μ = 1e-2 is flyable"); 80fe recorded only a cost
wall; no HISTORY entry diagnoses the mechanism. This run refutes the capture hypothesis
and answers the flyability question — new, and the page moves it to Refuted/answered
correctly.

**Goal fit.** The board's smoothness/allocator question: no scheduling work pays while a
tick is frozen. PRINCIPLES: "Errors never compound" (13) — this is compounding energy
minted by the law itself, the exact forbidden class; "A fix signals the wrong
representation" (19) — the run names the wrong object (the clock's constants and the
unbound body's representation, "you don't advance a ship tick by tick you just map where
it wants to go"). Mechanism verified in shipped code, not just data: ext.rs:87-90 (y
clamped from below only), ext.rs:100 (ticks ≥ 1 forever), step.rs:679 (kick weight),
step.rs:704-705 (drift interval; no MIN_STEP on the clock's own step — only thrusting
bodies clamp, step.rs:706-708), step.rs:628-633 (constants derived once at birth, never
re-derived).

**Page.** Faithful except one compression ("interval 10–22 ticks at the cap" — true only
of the 1.5M traces; the 100k-capped ICs are still collapsing, 1.5e7–1.9e6 ticks and
falling): corrected in place, and my held-out numbers added as a [Checker] note.

## What the author missed

- **The Δs round-down.** `constants()` rounds Δs down to a power of two (ext.rs:163-165):
  2.101e-8 → 2⁻²⁶ = 1.490e-8, giving Δs/b = 2.6176 — the measured A. Their "30%
  reconstruction gap" was their own missing rounding, not physics; the identity has no
  residual.
- **The kick weight sits at the guard, not at c.** U_P includes the origin-fall term
  −a_o·x (`force::field`), which drives U_P + c below the guard for a ship ejected along
  the planet's axis: y pins at c/8, w = Δs·f′(c/8) = 2.66e13, and the 6.52e-7/kick is
  w·|fall − pull| with the accel dominated by the frozen origin fall (3.6e-20 ≫ direct
  pull 4.9e-21). Same conclusion — constant, one-signed ratchet — but the dossier's
  "y → c" branch attribution is wrong at the magnitude level.
- Two of the ten capped ICs untraced (closed above: both ejected; one is the register-mint
  variant of the same freeze, an even cleaner "errors compound" exhibit).
- The horizon/mass extensions above (32 P, μ = 3e-2, μ = 1e-3 at 128 P).
- `regen.sh`'s ~9–11 min runtime exceeds the runner's regen window; splitting it (or
  lowering the deep-trace caps) would keep the runner path green.
