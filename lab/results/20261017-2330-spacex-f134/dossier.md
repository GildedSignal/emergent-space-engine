# Dossier — 20261017-2330-spacex-f134 (spacex lens)

## Claim

The page's cheapest named rung is flown: delete + chain compose with **zero interference**, and
the composed law (ES_SECULAR + ES_CHAIN + ES_LOCAL_STAGGER, one patch carrying both prior arms
verbatim) is **strictly dominant on every instrument** — max events/frame **41** against 52
(chain alone) and 131 (delete alone), p99 **12**, the ledger at **−72%** of OFF *without* chain's
+20% slice bill, and the standing comb **dies instead of spreading** (envelope decays
41→11→10→4→4→3→3; both arms alone leave standing structure) — closing the nladder comb
question: no further comb work has content.

## Bottleneck

The board's #1 (bodies in the flyable engine, 28 against 10⁹) via the page's own open
direction 1: "compose them (delete the legal set, chain what remains) — the cheapest next rung
on this page" (1a46). The comb is the locals' 334-event storm; the two measured cures trade
against each other (delete: 131 max, −70% ledger, but the spared set's comb stands and beats at
frame 3,173; chain: 52 max, but a +20% one-time slice bill and 26,670 total events). The
question was whether they interfere. Answer: they compose multiplicatively — chain de-phases
exactly the population delete spares. The run also resolves the page's standing three-way
merge conflict (both entries stand, complementary) and prices the held-out burn arm.

## Evidence (Linux/x86, 8 vCPU shared; event counts and digests are deterministic, wall is
order-of-magnitude only; every number from `regen.sh`, ~10 min)

Instrument: the shipped `nladder` example with 4fa8's and 1a46's env-gated probes composed into
one patch (`work/patch.diff`, a 335-line diff, applies cleanly to pristine main; flags default off).
Flights: N=1000 coast, rtf 100, seed 1, budget-free (budget 1e6 ms), 5,400 game-s.

**Arming controls reproduce both priors exactly** (the composition's baseline):

| arm (5,400 game-s) | max ev/frame | p99 | events | kicks |
|---|---|---|---|---|
| OFF | 334 | 136 | 22,219 | 9,217 |
| ES_SECULAR (delete) | 131 | 26 | 6,580 | 1,382 |
| ES_CHAIN+STAGGER | 52 | 24 | 26,670 | 9,270 |
| **BOTH (composed)** | **41** | **12** | **6,298** | **1,420** |

Envelope (max events per 500-frame slice): OFF `212 240 207 251 229 195 334`; SECULAR
`46 37 21 48 26 9 131`; CHAIN `52 27 26 12 13 13 12`; **BOTH `41 11 10 4 4 3 3`**. The only
≥40 beat under BOTH is the birth transient at frame 61 (41); SECULAR's standing 131-beat at
frame 3,173 and CHAIN's residual 12–13 class both disappear — the composed law is the only arm
with **no standing structure at all**: past frame ~1,000 the storm is a 3–4-event floor (the
spared quarter, the fleet, the belt stream), which no comb lever can touch.

**Held-out (not tuned on; written in predictions.md as expected classes):**
- N-flat: BOTH at N=0/600/10⁴ → max 43/40/40, p99 11/12/13 — all **below OFF's own N=0 floor
  (51)**: the plane's own locals are deleted and de-phased too.
- Horizon: 10,900 game-s → max 41, p99 10, marginal event rate past 5,400 ≈ 0.18/game-s
  (OFF at the same horizon: 334/135, 39,071 events).
- Burn (1,900 game-s): BOTH 105/41 with the lowest ledger (9,495) — max ties delete-only (105),
  p99 beats both priors (47/49); the partial-collapse burn tail is **arm-invariant**, i.e. not
  a comb object (its owner is the player's own kick re-timing, the 5 October memo finding).
- Engine ms (within-window, shared box): p90 1.794→0.700, p99 5.421→1.847 (OFF→BOTH); p50 at
  noise floor both arms.

**Controls.** (1) The composed patch with all flags off reproduces the frozen 13-case
`ladder_digest` record bit for bit (digests, kicks, encounters, contacts; whitespace-normalized
set-equality against `artifacts/runs/nladder/ladder_digests_wave.txt`) — the patch is inert
when off. (2) The composed law is deterministic across schedules: 13/13 digest cases, 4
schedules agree. (3) Under BOTH the digest cases' kick ledgers collapse 4–10× (wave 32,537→3,367;
belt crossing 38,106→3,205) — the delete's effect extends to the digest scenarios' belts, as
1a46's legality measurement predicted (the quiet belt is 5.5–6.4× under τ₀).

Commands (each ≤ 60 s except the digest passes, ~3 min each): see `regen.sh`; the decisive
flight is `env ES_SECULAR=1 ES_CHAIN=1 ES_LOCAL_STAGGER=1 nladder 1000 coast 55 100 1000000`.

## Predictions

`predictions.md` written before the decisive flight, with pre-registered kill criteria. **All
four predictions held**: P1 max 41 < 52, p99 12 ≤ 26 (kill was >131/>30); P2 events 6,298 ≤
7,500, kicks 1,420 ≤ 1,600 (kill was >11,110); P3 N-flat held (43/40/40, all ≤ 55); P4 p99
engine ms 1.847 < OFF's 5.421. The burn arm was flown after predictions as a held-out case and
is reported as such.

## What would make it wrong

- The composition could hide an interaction only at longer horizons or other seeds: the 2×
  horizon (10,900 gs) shows no re-formation, but the nladder example fixes seed 1 (no seed
  knob); prior checkers found seed 2 digit-identical for both component arms, and the composed
  arm inherits that only by inference, not measurement.
- The ledger win assumes delete's legality domain (r9's τ₀ per perturber, resonance exclusion
  ±2%) is correct as frozen; 1a46's checkers verified it three ways, but the r9→belt transfer
  is still unmeasured (the page's direction 2) — a wrong belt margin changes *which* bodies are
  deleted, not the composition's interference result.
- The adoption debt is unchanged and now single: the B13/B14-class legality gates and the
  doll-born drift band (87fd's direction 1, with its checker's horizon correction) are unflown
  under the composed law; the delete's sub-quantum fence debt (~2¹⁶ carried kicks) is also
  inherited untouched.
- The wall numbers are Linux/x86 on a shared box: orders of magnitude only; the M1 re-measure
  stands.

## Cost of adoption, and fit with PRINCIPLES

The patch is the two prior arms in one env-gated change (~60 lines of law between them, both
already independently checked); flags off = pristine bits. What it deletes: the comb (8× on max
events/frame, 30× past frame 1,000), 72% of the event ledger, chain's slice bill, and the
page's comb question itself — "The cheapest compute is compute not done. Delete before
optimizing" (§1), "the best part is no part" (§17). Parsimony is served twice over: no per-body
phase grid (chain's win over ES_LOCAL_PHASE, 21a7) and no metronome at all for the legal set
(delete's win). What it does not delete: the memory wall (1.2–1.65×10⁶ binds flyable N
regardless, fermi-1051) and the legality-gate debt.

## The lens

SpaceX's compose-the-cheapest-rung bias may have missed that the composed law's *residual*
(3–4 events/frame forever) is now so far below every gate's bar that the next marginal rung is
legality, not performance — the lens tends to keep optimizing what should be declared done. It
also biases against noticing that "strictly dominant" here closes a *decision*, not a
bottleneck: the flyable-N gap (28 vs 10⁹) moves only at the memory wall, and one more comb run
would be polishing what is already deleted.

## Files

`predictions.md`; `flights/` (all arms + `digest_off_patched.txt`, `digest_both.txt`);
`work/dump_*.csv` (per-frame event dumps); `work/patch.diff` (the composed patch, applies
cleanly to pristine main); `work/{secular,chain_clean,chain}.patch` (the two priors as fetched);
`wiki/nladder.md` (the page with the standing three-way conflict resolved and this result
folded in).
