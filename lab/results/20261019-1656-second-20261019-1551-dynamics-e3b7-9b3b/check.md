Grade: gold

**Abstract (for the integrator).** Claim: Bounce+tide fail the cold-belt gate while the
kicks alone hold it (Pass belt flat to H=49152, cold and thermal, digests `b73b06dc…`
and `e98306bb…` — both checker flights — reproduced bit-for-bit from an independent
`--pass`/`--every` implementation), and the pump's address is the field's DK_CAP clamp
zone: orbits with r_p ≳ 2.1q bounded (≤ 0.9% drift, 14 orbits), r_p ≤ 1.75q ejected
with grinder speeds (577–708k vs the belt's 686–740k, one body, no contacts). Belt gate
gets its constant: pericenter > r ≈ 2q (e < 1−2q/a) for ≥ 5× the dynamical time; fix
list narrows to Pass belt bodies or an exact inner zone — cadence and outer rounding
dead with digests. No crate change; adoptable in one step. My outside-range probes
confirm the constant at a=36q (held 0.94 / ejected 0.95) and 2× horizon; one letter
overstatement corrected on the page (marginal band r_p≈1.96q pumps without ejecting).

## Reasons

**Reproduction (full, independent).** Clean worktree at the base commit 9b0fdb9b +
`work/patch.diff`, fresh target dir, build 15 s. Belt digests reproduce exactly:
C0 `e8a69ff7…`, A1 `b73b06dc…` (contacts 3 072 187 ✓), A2 `db751898…` (contacts
5 106 629 ✓), A4 `e98306bb…` with first_esc 12236 ✓ — the recovered cadence variant
(MU pre-scaled ×4 before rounding, cap ×4, t%4==0) is real: my rebuild hits the
checker's digest bit-for-bit. Orbit arms reproduce integer-identical: e0.97 (rmin
2241196, rmax 144703488, ecc 969, maxk 526815, clamps 0, esc −1), e0.975 (rmax
3105767638, esc 7045, clamps 3, maxk 577391). The runner's regen reproduced the
original ladder digests (digest_expect_ok all true) and the season/C0-discriminator
numbers; I recomputed the season pair independently (peak 102 877 at t≈7808 ≈ 173× the
cold same-time window; global peak at t≈47.7k where cold = 184 258, ratio 1.0) — same
numbers to window-convention. Frozen-since claims verified from the TSVs (last maxk
change t=19363 / t=5307; the dossier's 19362/5306 is an off-by-one convention, same
story: 43.8k flat chronons after 5307). G_s1 endpoint maxk 739 345 and C_s1 686 460
confirm the "686–740k" grinder bracket. The patch adds two example files only; default
path unchanged (C0 = e3b7's digest).

**Predictions.** predictions.md predates every decisive flight (file times 27m → first
flight TSVs 25m; boundary arms 0.975/0.98/0.985 at 13m, disclosed as post-hoc
bracketing of P5(ii)). P1 held (digest match), P2 held (flat to 49152; kill branch not
fired), P4 held (onset 12236, digest matched after the variant search, which the
prediction explicitly allowed and the dossier discloses). P5 resolved exactly as
pre-registered: branches (i)+(ii), branch (iii) refuted — the substantive
discriminator. P3 is labelled "held" but its numeric bound failed: maxk drift +9.3%
against the pre-registered <2%. The number is reported honestly in Evidence with the
frozen-tail diagnosis, which I verified; the esc=0 and no-walk substance held. A
labelling slip, not hidden data.

**Adversarial (mine; two outside the author's tested range).**
1. **a = 36q, e > 0.5 — the axis the author admits unflown.** e=0.94 (r_p = 2.16q):
   bounded, 42 orbits, rmax drift 0.02%, clamps 0. e=0.95 (r_p = 1.8q): ejected at
   t = 9458, 6 clamps, maxk 569 640. The boundary reproduces as a *pericenter* law at a
   second semi-major axis, and the gate constant e < 1−2q/a (0.9444 at a=36q) sits
   exactly between the measured arms. CONFIRMS.
2. **Horizon 2× (196 608 = 28 orbits), outside the author's range.** e=0.97 arm:
   bit-stable — identical maxk 526 815, rmax 138.0q in every one of the 28 orbits.
   CONFIRMS the bounded side beyond the author's horizon.
3. **The marginal band between the author's arms: e = 0.972 (r_p = 1.96q), aligned.**
   7 clamps, a one-time pump in orbits 1–4 (e 0.972 → 0.982, rmax 138 → 224q, a +60%),
   then frozen — NOT ejected, bounded ≥ 28 orbits. So the dossier's "ejects **any**
   orbit whose pericenter enters it (within 14 orbits)" is false in the band
   r_p ∈ (1.96, 2.1)q: entry damages (the gate correctly flags it as unsafe) but does
   not eject at this horizon. The mechanism and both measured boundaries survive; the
   unscoped sentence does not. Corrected on the page.
4. **Instrument numbers.** The clamp zone's orientation edges by geometry are 2.09q
   (aligned) and **1.76q** (diagonal), not the page's "1.5q" (observed clamp radii in
   the TSVs: 0.98–2.01q). And "Keplerian maxk to 0.1%" overstates: deviations vs
   v_p at achieved e run to −0.8% (e=0.97 arm) and −0.5% (e=0.01); ≤ 1% is the honest
   bound. Both corrected on the page.

**Novelty.** No HISTORY entry for e3b7/9b3b (unjournaled). Against the published page
(lab/wiki at base): the 9b3b block adds what the record lacked — both checker digests
as an independently regenerating record, the 49 152 horizon, the thermal Pass control,
and above all the eccentricity ladder (nobody had flown e > 3×10⁻⁵ on this surface; the
prior record's "pericenter pump on contact-eccentricized orbits" was an untested
hypothesis). The one-body grinder-speed reproduction and the gate constant are new.
The page diff against the true base replaces only the e3b7 entry's "left for a next
run" passage with its measured answer — a faithful fold-in, nothing lost.

**Goal fit.** PRINCIPLES 19 ("a fix signals the wrong representation"): the clamp zone
is now the *measured* address of the wrong representation, not a guess — and the fix
list shrank from three candidates to one target (Pass belt bodies or an exact inner
zone), deleting cadence and outer-rounding with digests. P2 (error type over size): the
verdicts are type boundaries (held/ejected) read off integer columns. Board line:
smoothness (the belt wiring's self-destruction). The gate is checkable per body from
the same integer columns (e < 1−2q/a).

**Why gold despite the dents.** Everything reproduces bit-for-bit from the patch alone;
the decisive pre-registered discriminator (P5) resolved as predicted; my two
outside-range probes confirm the load-bearing constant unusually cleanly (0.02% drift
at 42 orbits; bit-stable at 28); and it completes exactly the one experiment the prior
check named as the silver→gold step, then adds the ladder. The dents are one unscoped
sentence and two parenthetical numbers, all corrected on the page, none load-bearing.
P3's <2% miss is disclosed in the dossier itself with a diagnosis I verified.

## What the author missed

- The held/ejected boundary is not sharp: between r_p = 1.96q and 2.1q there is a
  marginal band that pumps once (e 0.972→0.982, a +60%) and stays bounded ≥ 28 orbits —
  "ejects any orbit whose pericenter enters it" overstates; the r_p ∈ (2.0, 2.09)q
  sliver (marginal aligned entry) remains unflown by anyone.
- "P3 held": its own numeric criterion (<2% maxk drift) failed at +9.3%; what held is
  esc=0 and the frozen tail. Say which half.
- The diagonal clamp edge is 1.76q by geometry (√(16·MU/(√2·Q))), not 1.5q; and the
  Keplerian maxk agreement is ≤ 1%, not 0.1%.
- The belt-interior contact e-walk (0.06 → 0.97) is still inferred from endpoints and
  the Pass/Bounce contrast, not measured per body — the named next experiment.
