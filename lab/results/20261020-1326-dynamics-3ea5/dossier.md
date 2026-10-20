# Dossier — 20261020-1326-dynamics-3ea5

**Claim.** The collapsed belt core's attractor is a *standing sub-quantum droplet*: on the
shipped wiring (Bounce contacts + clamped per-chronon tide, e3b7/c644's scene verbatim,
digest lineage reproduced bit-for-bit) the remnant holds ~90-115 bodies below r = 0.5q —
one position quantum — indefinitely; they bill f·C(n_sub,2) contacts per chronon
(f ≈ 1.8-1.9, stable within 8% over 115k ch), which is 99% of the whole system's contact
work (86-90% on sub-quantum members alone); they sit in the clamp zone (~85% of their
member-chronons clamped) without being ejected (4 of 534 dead bodies ever clamped); the
per-body death hazard keeps DECAYING (7.4e-6 → 1.4e-6 → 3.5e-7/ch over 0-49k/49-98k/
98-147k on the cold seed), so the droplet is not a grinder and not a transient: it is the
end-state — the belt's mass slowly evaporates through it while its own bill stays
quadratic in the resident count and grows only as it absorbs the skirt (+9-10 residents
per 49k ch).

**Bottleneck.** c644's named leftover #3 (the core's own evaporation tail past 49k), the
half 19b9's ledger run did not fly (it took only N(t): 308→273 and "rate holds ~4700/ch").
On the belt decision path: c644 closed with "the decision is whether a contact-collisional
belt is wanted at all … the re-birth cadence bound is 1/λ". This run supplies the end-state
that decision prices: a permanent f·C(n_sub,2) ≈ 1.9·n_sub²/2 contact hot spot at the
quantization floor (11.5k contacts/ch at n_sub = 114), clamping ~every chronon, with a
decaying evaporation hazard — no re-acceleration, so the rebirth-cadence question is
answered by the *bill*, not by a death spiral. Not a 10× cost mover by itself: it converts
"the belt relaxes in ~3 dynamical times" into "and then holds a ~1.9·C(n_sub,2)/ch standing
bill for ≥ 3× that, hazard → 3.5e-7/ch".

**Evidence.** Harness `crates/lattice/examples/coretail.rs` (beltewalk's genesis and tide
VERBATIM; measurement only: band tallies per stride, per-body droplet residence, first-clamp
marks, digest checkpoints at t=49152/98304). Arms: MAIN cold s1 H=147456 (c644's B lineage
at 3× its horizon, 19b9's B at 1.5×), SEED thermal s2 H=98304 (c644's C at 2×), CTRL Pass
s1 H=147456 (the negative). Regenerate: `bash regen.sh` (~11 min wall; MAIN dominates).
All flights deterministic; a first MAIN attempt was killed by the launcher shell's
process-group cleanup at t≈49k (no numbers taken from it), and the rerun reproduced the
t=49152 checkpoint bit-for-bit.

- **Lineage:** MAIN ck49152 = c644's B exactly (contacts 63,461,214, digest `434f69bf…`);
  SEED ck49152 = c644's C exactly (88,881,906, `0845a045…` = 19b9's C, itself bit-for-bit
  c644's); MAIN ck98304 contacts = 288,352,399 = 19b9's B counter exactly (their digest
  file was dropped; the counter plus the two 49152 digest matches carry the proof). MAIN
  final: digest `4760731c…`, 550,463,165 contacts over 147456 ch.
- **P1 (the droplet is the bill) HELD in form, with the honest constant above my band:**
  zone members' share of member-contact-increments 0.986-0.993 at every epoch past 16k on
  both arms (bar ≥ 0.6); sub-quantum share 0.86-0.90. f = ct_tot/(stride·C(n_sub,2)):
  SEED 1.93→1.80 over 16k-98k ch; MAIN 1.95→1.81 over 32k-147k ch, tail (t>98304) median
  1.82, per-epoch spread 1.797-1.830. My pre-registered band was [0.4, 1.3]: the engine
  fires ~1.85 contacts per overlapping pair per chronon (a pair can rattle more than once
  per chronon) — the LAW held, the constant was under-guessed by 1.4×.
- **P2 (quench, no grinder) HELD:** windowed per-body hazard (8192-ch windows). MAIN:
  7.4e-6 (32-49k) → 1.0-1.4e-6 (65-106k) → 3.5e-7 (last three windows, one death each;
  peak 1.9e-5 at 24-32k). SEED: 6.1e-5 → 1.1e-5 → 3.6e-6 → 1.6e-6 → 6.5e-7 → 0. No window
  above 1.4e-6 past 98k on either seed; the inversion branch (λ > 5e-6, grinder) never
  fired. Point prediction N(147456) ∈ [230,270]: measured 266.
- **P3 (the droplet holds) HELD:** n_sub median per 4096-ch epoch: SEED 82→94 over
  49k-98k (+10/49k); MAIN 82→114 over 49k-147k, tail slope +9.1/49k, range [105,115] over
  98-147k (bar: [60,175], |slope| < 25/49k). The remnant absorbs the skirt slowly and does
  not dissolve; the near-core rms radius holds ~8.4-8.6q on MAIN (grows 6.3→9.7q on
  SEED): the core is not contracting — it sits at the quantum while the skirt puffs.
- **P4 (death channel) HELD, strongest form:** MAIN's 7 deaths past 98304 are 7/7 never
  clamped, 0/7 sub-resident within 512 ch of death — 100% relaxation-born, 0%
  droplet-ejected (bars ≥70% / ≤30%). All-run: 4 of 534 dead bodies ever clamped (0.7%):
  the pump has killed at most 4 bodies in 147k ch while clamping ~85% of droplet
  member-chronons.
- **P5 (Pass control) held where it loads, missed on a rate constant:** 0 deaths, n_sub = 0
  at every one of 1152 strides, min r over all bodies 35.3q (nobody even approaches the
  center): the droplet is the Bounce+tide wiring's, not genesis geometry. My "<150
  contacts/ch" bar failed: the Pass belt's own thermal rate grows to 288/ch (16,973,365
  contacts over 147k, avg 115/ch) — the flat control is flat in *state*, not in rate.
- **The pump stays loaded but disarmed:** among MAIN's 266 final survivors, 152 have
  clamped at least once, 147 ever entered the sub-quantum band, 98 are sub-resident
  (r<0.5q for ≥ half of all strides ≈ 74k ch); cl_zone accrues ~10-15k clamped
  member-chronons per 8192 ch. c644's "the applied clamped tide is not the field inside
  r < 2.1q" is the standing *condition* of the attractor, not a transition: the droplet
  LIVES in the clamp zone. It is not ejected because it is already below the law's own
  resolution there: bodies have radius 1q, so below r = 0.5q every pair permanently
  overlaps, positions differ by ~0-1 quanta (min r hit exactly 0), and the capped kick
  (q/16 per component) is re-absorbed by contact exchanges faster than it can pump anyone
  out — a degenerate gas the field cannot resolve, held by contacts. c644's 108 survivors
  below 0.5q at 49k are this object at birth: 114 at 147k.

**Predictions.** `predictions.md` written before the flights (one H=2048 format smoke,
disclosed there). Verdicts: P1 held in law, constant 1.4× over my band (honest miss on f);
P2 held (both seeds, N=266 inside [230,270]); P3 held (both seeds); P4 held (7/0 of 7);
P5 held on state (0 deaths, 0 droplet, min r 35q), failed on the 150/ch rate constant
(measured 288 max).

**What would make it wrong.** The attractor is measured on one law (RelativisticV1), one
scene family (e3b7's 800-body belt), two seeds, to 147k ch ≈ 21 dynamical times at 70q: a
horizon 4× longer could still show slow absorption or evaporation of the droplet (the
hazard decay says not by 147k); the bill law f·C(n_sub,2) is measured at n_sub ≈ 60-115 —
a much denser collapse (n_sub ≥ 300) could change the rattle statistics; and 3D or
self-gravity wiring could change both the relaxation rate and the droplet's confinement.
Cost of adopting: none for the engine (a measurement on shipped code); the belt wiring
decision gets the standing-bill number and the closed form. Fit: PRINCIPLES 3 ("compute
only surprises" — the droplet is a permanent surprise generator the allocator must price,
and its bill is now a closed form in n_sub) and 33 ("each scale resolves only what matters
at that scale" — below one quantum the core stops being orbits at all; it is one object,
yet the law still pays n_sub² pairwise work for it: the representation gap the fix list
already names).

**The lens.** The attractor framing predicted the pair-capacity law (bill = f·C(n_sub,2))
and the quench-vs-grinder fork, and both held. What the lens missed: the constant f ≈ 1.85
(rattle fires more than once per pair per chronon — an engine detail, not a dynamics one);
and that the clamp zone would turn out to be the droplet's *habitat* rather than its
executioner — the pump is loaded every chronon and still cannot eject a sub-quantum
resident, the strongest form yet of c644's "not the field down there".

## Numbers (all regenerate from regen.sh)

| quantity | SEED (th s2, 98304) | MAIN (cold s1, 147456) | CTRL (Pass, 147456) |
|---|---|---|---|
| contacts total | 267,106,591 | 550,463,165 | 16,973,365 |
| live at end | 284 | 266 | 800 |
| n_sub at end | 93 | 114 | 0 |
| zone share of contacts | 0.986-0.991 | 0.986-0.993 | — |
| sub share | 0.87-0.90 | 0.86-0.90 | — |
| f_pair (tail median) | 1.80 | 1.82 | — |
| contacts/ch final epoch | 7,292 | 11,533 | 115 avg / 288 max |
| hazard peak → 49k / 49-98k / 98-147k | 6.1e-5→3.6e-6 / 1.6e-6→6.5e-7 / — | 1.9e-5→7.4e-6 / 1.4e-6 / 3.5e-7 | 0 |
| dead ever clamped | 4 (c644: 3/498) | 4/534 | 0 |
| dead ever clamped | 4/516 (c644: 3/498) | 4/534 | 0 |
