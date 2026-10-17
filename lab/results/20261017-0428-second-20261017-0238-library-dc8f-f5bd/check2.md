Grade: gold

**Abstract.** The checker's named fence flight, flown to 8×10⁶ game-s, kills both published
constants. No quantum fence exists: the debt (2.6×10⁻⁴° at 5,400 gs) always sat 3,000× above
the law's coarsest acting angle grid (the tube's 32-bit periapsis angle, 8.38×10⁻⁸°), and the
curve follows no law (t^2.15 dead past 2×10⁵ gs; 14.65° at 7.41×10⁶ vs 1,450° predicted; 18×
above linear; no saturation). k* ≤ 2^3.7 at every bar ≤ 1°; the 2^10–2^12 band needs a
~50–100° bar. Re-kick = 0.57× a fired kick. Adoption: delete the compose rung's scheduler
question — freeze the angle bar q instead. Cost: zero code on main.

**Reproduction.** The runner's regen (exit 0) hit every calibration bit-exactly: OFF 5,400 gs
334/136, 22,219/9,217; ARM 131/26, 6,580/1,382; 11,000-gs ARM 1,813/7,516; thread-4 states
identical; traced set 477; the exact-tick probe 2.620×10⁻⁴°/1.181×10⁻³°; the default regen's
curve to 1.5×10⁶ gs (4.294°) matches the flown 4.298°. Independently of the author's script I
re-parsed the flown 8×10⁶ traces: max 14.6516° at 7,414,159 gs (id 163, in-situ), median
1.059×10⁻³°, belt max 2.248×10⁻³°, crossings 1°→3.566×10⁵ gs, 0.1°→9.03×10⁴, 10⁻²°→2.55×10⁴
(k* +3.7/+1.7/−0.1), fits t^0.87/t^1.18 (max) and t^2.01 (median), still rising at the last
horizon — every headline number confirmed. I also re-flew the 1,900-gs record point that
regen.sh omits (it flies 11,000 instead): 240/146, 11,111/3,624 — exact; the inherited
calibration claim holds. The patch was audited: all probes env-gated; the OFF path is
untouched, and the calibration bit-identity is the proof.

**Adversarial cases (mine).** (1) The 1,900-gs point, above. (2) **N=4000 — outside the
author's tested range** (4,028 bodies, 1,687 deleted traced vs 477): the debt curve is
population-flat to 0.3% (10⁻²° crossing 2.555×10⁴ gs vs 2.547×10⁴; 0.1° at 9.027×10⁴ vs
9.032×10⁴; max again in-situ-owned, belt again ~3 orders under). The fence kill and k* are
not an N=1000 artifact. (3) Mechanism attack: the max is owned by a handful of in-situ bodies
(id 163 owns 33/96 horizons; top-5 all in-situ at 11–15°; 72/477 bodies >1° at the end, 233
≤10⁻³°) — the "staircase" is max-switching among a small secular-precessing set, which the
dossier admits measuring without explaining. (4) Extrapolation uncertainty: my own late fits
put the debt at the 2^10 edge (2.9×10⁷ gs) at 44°–108° across fit windows vs the author's
"~70°" — fit-sensitive, but every fit leaves the bar absurd (tens of degrees), so the band's
death survives. (5) ES_SECULAR_RES=1 control: not re-flown here before the window closed; the
author's falsifier structure stands untested (see Missed).

**Predictions.** Written 04:44; both decisive traces landed later (04:53, 05:07). Verdict-
bearing ones held: t^2.15 dead (1), k* far under 2^10 (2, arithmetic corrected honestly),
re-kick ≤36× (3: 0.57×), crossings inside range (4), spared set 540/540 bit-identical (5).
Misses reported by the author, not hidden: the linear law's magnitude (18× under) and the
naive k*(1°) arithmetic.

**Novelty.** Both killed constants are published and live: the nladder page's "goes live only
near ~2^16 carried kicks (~10⁷ game-s)" (with the 1637 checker note calling it probe-horizon-
bound — this run is the arbiter that note asked for) and "a sparse secular re-kick every
~2^10–2^12 kicks" (nladder page, open direction). No HISTORY entry had flown it; dc8f's page
said "flight pending". Not a repetition.

**Goal fit.** Board #1's compose decision. It deletes a component (the fence-horizon
scheduler the compose rung was to carry) and shows a premise wrong: the fence was a 3-decimal
print artifact, exactly the suspicion. PRINCIPLES: "Measure before claiming, and never
strawman" — both constants were unmeasured and now are; #19 "A fix signals the wrong
representation" — the fence was the wrong representation of an error that was live all along.
The wiki page folds the result in faithfully; I corrected one line in place (the 10⁻³°
crossing sits inside the trace's frame-jitter band: the exact-tick anchor at 5,400 gs is
2.6×10⁻⁴°, 4× below the trace reading, so the true crossing is later, k* nearer 2^−1.5 than
2^−2.4 — no verdict changes).

**What the author missed.** (a) The claim sentence "T* measured inside the flown range for
every such bar" is false for the two sub-traced bars (tube grid 67.5 gs, 10⁻⁶° 214 gs are
extrapolated); the wiki page says so, the dossier's table label "T* measured" should not.
(b) The max-debt mechanism is one small in-situ population, so the compose rung's bar q may
need to be per-population even in degrees — the run hints at this (in-situ vs belt split) but
does not derive the per-population k* table the mechanism implies. (c) The bench's headline
run (37,056/72,004 ns) was overwritten by regen and survives only as quoted numbers; the two
surviving raw runs agree at 0.57×, so the claim stands, but the raw evidence for 0.51× is
gone. (d) The 2×10⁷-gs ask was met at 8×10⁶ with the extension argued from fits whose spread
(44–108° at the band edge) is wider than the quoted "~70°" suggests. (e) The RES adversarial
control (resonance exclusion off, named in the patch) was never flown by anyone.
