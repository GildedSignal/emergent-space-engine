Grade: silver

**Abstract (for the integrator).** Claim: the lattice's only gravity wiring (per-body,
per-chronon rounded 1/r² kicks through `Kickable::kick`) cannot hold a cold belt — a
contact-free-looking cold belt self-destructs by t ≈ 10–25k chronons (reproduced
digest-identical, both seeds; 449/800 evicted, 72.9M contacts), so chaos-shadowing's
gravity-held-belt leftover is unanswerable on today's wiring, and the fleet crossing
evicts 86% with no bound halo. Gain: a missing gate named before any belt wiring; cost:
one harness, no crate change. Checker correction: with `Response::Pass` the same belt is
flat for 32k ch and isolated orbits are stable, so the instability is contact-triggered,
tide-fed (cadence ruled out); "season peak 183685" is the grinder's; "esc 0 always" is
false at genesis. Adopt the corrected page, not the dossier's mechanism sentence.

## Reasons

**Reproduction (full).** The runner's regen.sh exited 0 and every digest matches the
author's stored artifacts: G_s1 `e3462444…` (= the author's preserved ladder.log), C0
`e8a69ff7…`, C_s1 `634d9918…`, GW `79b89629…`. I rebuilt the harness from
`work/patch.diff` in the clean tree and my variant binary at `--every 1` reproduces C0
s1 bit-for-bit. The dossier's claimed slim/non-slim 512-ch digest pair `37cfa9f0…`
reproduces exactly on my rerun. Dossier numbers verified exact against the TSVs: C0 maxk
ladder 99194/151731/379827/726985, rms 77.7→91.8q, first esc t=13022; C s1 449/800
evicted (max), n_in 309, maxk 686460, 72.9M contacts; G esc 1327 at t=4096, esc50 at
2211/2222 both seeds, n_in 224, 96.0M contacts; GW 78.3M contacts, 14 896 wall hits
(header; note analysis.json's `walls_total` 216M sums a cumulative column — garbage,
harmless), wall rate 0.88→0.31/ch, n_in 1189→1360, rms 72–90q.

**Predictions.** predictions.md predates the ladder (file times and log order). P1's
kill branch fired and was reported honestly — the run's best property. P2 held
(174× same-window; see correction below). P3 resolved to (b) with the cause reattributed
by the author's own C0 arm. P5 held in the fleet window and was honestly overridden at
horizon.

**Numbers that are wrong as written** (all minor, all corrected on the page):
- "Season peak 64-ch window 183685 ≈ 2276× the cold mean window in the same window of
  the control": 183685 is the **late grinder's** peak (t ≈ 47.7k), where the cold
  control's own window is 184250 — ratio 1.0. The real season peak (t ≤ 8192) is 102874
  at t ≈ 7808 = 174× the cold same-window (P2 still holds).
- "esc = 0 always" (GW): 301 bodies start beyond 250q by genesis geometry (fleet tail);
  esc reaches 0 at t ≈ 400 and stays. No permanent escape — but "always" is false.
- "86% at saturation (1376)": no artifact holds 1376 (esc_max 1379, esc_last 1371; s2
  1374/1373).
- "140–250q shell empty from t ≈ 4k": 77 bodies (4.8%) at 4096, 21 at 8192 — draining,
  not empty; "no persistent halo" survives.
- The discriminator sentence "ladder established by t=12k when cumulative contacts
  ≈ 20k": at t=12k cumulative contacts are 1352 and maxk is 380k; the 727k/21862 pair
  is at 16k.

**Adversarial cases (mine; one outside the author's range).**
1. **Isolated orbits — outside the author's range (never flew below 800 bodies).**
   Single body, exact circular at 70q and 36q, and with a +1-quantum tangential seed
   (e ≈ 3×10⁻⁵, the belt's own rounding scale): all bounded for 49k ch (7 orbits at 70q,
   19 at 36q), maxk drift ≤ 0.25%, radius constant. Since belt bodies interact only
   through contacts, any C0 body that never contacted follows exactly this bounded
   dynamics — so **contacts are necessary** for the observed self-destruction.
2. **Ensemble control (the decisive one): `Response::Pass`** (contacts recorded,
   velocities untouched), same 800-body cold belt, same seeds, same field, H=32768:
   **flat** — maxk 92159→92196 (+0.04%), rms constant 77.7q, esc 0, total ke +0.02%
   (digest `b73b06dc…`, 12 s flight). The dossier's mechanism sentence ("a contact-free
   cold belt self-heats … the pump is the tide representation, not contact noise") is
   **refuted in its attribution**: the tide alone holds the belt; the instability is
   contact-TRIGGERED, tide-FED. The energy half stands — elastic `Bounce` impulses
   cannot raise max speed, so only the field injects the energy — but the seeds are
   contact impulses, not quantization noise.
3. **Cadence (the author's own lens-note check, flown):** kicks every 4th chronon at 4×
   magnitude: onset 12236 vs 13022 (unchanged; the "< 4×" prediction held), final maxk
   higher (841k), digest `e98306bb…`. Cadence is ruled out as the pump — consistent with
   a per-pericenter error.
4. **Seed 2, thermal 0:** reproduces the kill (first esc t=12422, maxk→755k, 102k
   contacts) — the C0 result is seed-robust.

**Novelty.** chaos-shadowing's open direction 2 names "the gravity-held belt — confined
without walls — the plateau's lifetime" as e56b's leftover; this run flies it first. No
HISTORY entry or wiki page measures the lattice's `Chronon`+`kick` gravity surface (the
law-lab tide entries are a different surface). Novel; the page folds it in, and I
corrected the overstatements in place (mechanism block, verdict line, esc-always, season
peak, esc_max numbers, shell, cadence in the next-run pointer). The Runs-list changes
are a legitimate dedup of stale "(this run…)" twins — no entry lost.

**Goal fit.** Real: it names a gate any belt wiring must pass before the question can be
asked (PRINCIPLES 19, "a fix signals the wrong representation", measured at the law's
own surface), on the board's smoothness line. It respects the lab rules (patch-only, no
crate change, `main` untouched, digests regenerable). But as submitted it would teach
the integrator a wrong mechanism — that is what holds it below gold.

## The one experiment that would make it gold

Fold in the contact-triggering control as the run's own result (I have flown it;
digests above): C0 with `Response::Pass` (a one-line harness change) — the belt is then
flat for 32k+ ch — plus the corrected season/shell/esc numbers. That converts the claim
from "the tide self-destructs a contact-free belt" to the measured truth "Bounce+tide
together fail the cold-belt gate; the kicks alone hold it", which is adoptable in one
step and redirects the fix (pericenter pump on contact-eccentricized orbits, or Pass
bodies for gravitating-only scenes — not cadence, not "gravity wholesale").

## What the author missed

- The decisive control was one line away: `Response::Pass` isolates contacts from the
  tide, and it inverts the mechanism sentence. The dossier's own caveat saw the
  possibility but "bounded" it with wrong numbers (1352 contacts by 12k, not ≈20k).
- "Contact-free" was load-bearing and unchecked: C0 has 21 862 contacts; the phrase
  covered the attribution error.
- The season peak was the grinder's peak: `max(gw)` over the whole run lands at t≈47.7k
  where the cold control grinds equally hard; "same window" comparisons must be
  same-time, not global-max vs early-mean.
- Genesis geometry (fleet tail born beyond r_esc) makes any "esc = 0 always" claim
  false by construction; check esc at t=1 before writing "always".
- analysis.json's `walls_total` sums a cumulative column (216M against the header's
  14896); harmless here because the dossier quoted the header, but the script would
  mislead the next user.
