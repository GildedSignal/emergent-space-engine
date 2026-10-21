topic: chaos-shadowing
status: open
closed-by:
valid-while:
updated: 20261021-0312-dynamics-485f

# Chaos, the shadowing clause, and trapping statistics under quantization

## Current best

**The contact carry is a bounded attractor in the storm class, not a walk (485f).** Through 293M contacts (cold s1, 98,304 ch) and 79M (thermal s2): per-body |Δres| vs Δcontacts α = 0.029, r² = 0.005 (4,788 intervals; a walk reads 0.5); mean |res|/alive 1.13× from 70k to the end while ~129M contacts flow; |Σres|/Σ|res| 0.93 at therm2's first transient (cold1: 0.55, max 0.57), 0.32 mid-storm, 0.014 at the end. Max |residual| 1.56e6 = 2^20.6 (cold1 onset t = 15,872, post-onset ceiling 1.49e6 at t = 60,928, one body holding 1,003,170 stationary t ≈ 43–77k; final-16k mode 825,425 at 23/32 strides, excursions to 1.24e6; therm2 763,377 at 58/60 strides from t = 18,944, its global max 1.09e6 mid-run at t = 42,496); max |carry_c| 5.2e6 — ≥ 2^40 of i64 headroom. Mechanism: `resolve` scores candidates by |owed + e| — a first-order sigma-delta whose control authority is one candidate energy step ≈ 2m|k| (1.3e5 at belt speed q/16, 6–8e5 at rattle speed). Equal-mass class only — at mass contrast the carry walks (contact-carry page). Licenses: narrow/frozen carry fields (no retirement protocol, no overflow watch), dead bodies take ≤ 2^23 away each (momentum carry 2^22.3, energy 2^20.6).
**The terminal rattle is one crowd, not pairs (485f):** 4,618 c/ch over 274 hot bodies = 16.9 contacts/hot body/ch, median 42 distinct partners per 64 ch (therm2 6.5), top single pair 0.02–0.03% of window contacts, 24,363 distinct pairs over the run — compiled/deferred contact response must be per-crowd (PRINCIPLES 6), not per-pair.
**The belt's fate is terminal (3b67, checker-extended to 147k):** one storm, then a permanent sub-quantum clump (~150 bodies, 95% within 2.1q) carrying a standing 3.7–5.1k+ c/ch rattle (still +15% at 147k — a lower bound, not an asymptote); escape hazard decays to zero (λ 0.21/0.12 vs the storm's 3.3×10⁻⁵); the death ledger retires at ~2× the storm's duration.
**Deaths are relaxation unbinds ordered by ε = 0, not the clamp zone (c644: 2/492, 3/498 dead ever clamped; hazard λ 3.3×10⁻⁵/ch, self-quench remnant ~310).** The storm class rides e3b7's rounded 1/r² tide, which fails its own cold-belt gate; formation energy persists as an extensive 15.5× plateau (e56b); the coherent burst is one-shot (90b7); the box ringdown is genesis-shock decay, extinct at n = 12,800 (84b2). [Checker 485f — clean-tree regen bit-for-bit (digests 98fd7fe0…/bbbca241…); seed 5: α = 0.033; uniform m = 64: α = −0.003, ceiling ×64 (res 5.9e7, carry 2.7e8 — still 2^34 headroom): the m·|k| scaling holds; "frozen band" letters corrected against the TSVs (see check.md). Checker notes of superseded blocks are in this page's git history.] [Checker2 485f — own regen bit-for-bit (all six TSVs identical, digest 98fd7fe0…); 2× horizon, 196 608 ch / 800.9M contacts: still no exposure law (per-body α = 0.078, r² = 0.04), bias 0.038, rattle denser (5 839 c/ch, median 126 partners/64 ch, top pair 0.02%) — but body 751 ramps to 6.55e6 = 2^22.6 at t ≈ 139k and returns, and again near 190k: the amplitude tracks the intensifying clump, not 2m|k| (≤ 2q = 2.1e6 at m = 1; ~20 contacts/chronon defeat the per-contact authority), so the narrow-field license is horizon-scoped; the ≥2^40 i64 headroom, no-retirement and per-crowd licenses hold. Thermal ±64: α = 0.125, peak 1.32e6. N = 200 sparse: no storm (243 contacts), pair-like — the stated domain boundary is real. Letter fixes: post-onset ceiling 1.49e6, therm2 58/60 strides, carries need 23+sign bits.]

## Refuted

- "The quench is a standing leak / the remnant keeps evaporating at the post-32k plateau rate" — the hazard decays to zero by 98k (λ_tail 0.21/0.12 vs the plateau reading 0.6–1.0); the endpoint is a terminal rattle (3b67).
- "Bounce contacts walk bodies' e to ~0.97 and the tide's inner clamp zone is the sole energy injector" (as the contact-bearing belt's mechanism) — the zone is never reached (2/492, 3/498 dead ever clamped); deaths are relaxation-driven unbinds ordered by |ε₀| (c644); 9b3b's isolated ladder stands for the zone itself.
- "Deaths order by the pericenter gate e_c = 1−2.1q/a, inner rings first" (c644's P3) — outer-first (49%→79% outward); the boundary that matters is ε = 0 (c644).
- "The gravity-held belt can be flown on the lattice's kick surface to answer the plateau-lifetime question" — the per-chronon rounded 1/r² tide self-destructs a contact-free belt by t ≈ 10–25k ch; late-time readings on this wiring measure the tide's error flow (e3b7).
- "The fleet's deposited energy holds the late contact load under gravity" — the cold belt alone reaches the same grinder (2871/ch at 49k); the fleet only buys earlier entry (e3b7).
- "The wall-reflection train" as the mixed fleet×belt mechanism, and "the fleet stays coherent through a dilute cloud forever" — no 4·w clock, no wall-bounce train; free space shows one season then dispersal; what persists confined is the energy, an extensive plateau at 15.5× the cold belt (e56b, 90b7).
- "Coherent formations keep bunching violently as a standing allocator-visible danger" — the crossing is one-shot for any transverse structure ≥ 1 quantum; the sustained train needs exactly matched columns (σ_y = 0) (90b7).
- "Whole-run m at n = 12800 reads 3.43%, so the m-bound does not extend past n = 6400" — the reading is the window: at horizon ∝ side it reads 2.00–2.10%, ringdown extinct, late F64 at the n-independent baseline (84b2-ded5).
- "The breathing mode's N-scaling is an allocator-visible danger that grows with the formation" — it is the identity Fano₆₄ = 64·ν·n·m² with m bounded; per-window max/p50 ≤ 1.08 at every n (84b2).
- "A long-lived coherent breathing mode" as a steady-state object — it is the genesis shock's ringdown, decaying 117 → 2.7 by n = 6400, period ∝ box side (84b2).
- "Denser contact work avalanches (Fano > 1, frames spike)" — measured anti-bunching for thermal genesis (834e); coherent formations do read Fano₁ 10–129 (checker2).
- "A cold dense gas collides at the equilibrium-fluid rate (Henderson g)" — falls to 0.42 at φ = 0.78 (834e).
- "A thicker layer at μ = 1e-2 raises the encounter rate" — first-entry rate falls 40 → 32 (80fe).
- "The plane's co-orbital deaths are false deaths" — kick-time planet-disk crossings; the P/256 instrument was blind by 180× (e846).
- "The deaths are spurious planned terminals" — 0% terminals, 100% planet_kick (e846).
- "The runaway is the planet doll's octave" — root-clock far-field kick ratchet + drift-interval collapse (taleb-6de0).
- "Zero-velocity confinement could prove some deaths impossible" — every IC 1.0–1.3% below J(L1) (e846).
- "A deterministic law with the right statistics is a true orbit of nearby ICs" in mixed phase space (5cad); statistics side holds on both shipped surfaces (f50d, b9be).
- "Deterministic rounding per event ≈ noise of same magnitude" — 14.1% vs 1.2% traps at Q = 10⁻³ (5cad).
- "The standard map's Q-scaling transfers to the shipped dense order" — engine-vs-exact statistics flat across Q = 2¹⁶→2²⁰ (3ca8, f50d).
- "State quantization is the channel" / "the integer response's ensemble behaviour" — refuted by the exact twin (3ca8, f50d).
- "The dense order deviates 15–45% with 5× max-dwell" / "every contact is continuum to 1e-5" / "the neg-scene rate gap is per-contact" — instrument errors and phase snapshots (3ca8, f50d).

## Open directions

1. **Freeze the trapping-statistics rung on the shipped dense order** — the exact twin (f50d) is the positive control; include the survival/death class (b9be's warning).
2. **ANSWERED (90b7; e56b; e3b7; c644; 3b67; 485f) — the formation/belt burst law is priced at walls, in free space, and in the gravity container, through the storm and past the quench: the belt's fate is terminal (one storm, then a permanent sub-quantum clump rattle; the death ledger retires at ~2× the storm's duration), and the carry ledger through the storm is a bounded attractor with the rattle one crowd.** Remaining for a next run: the clump's ultimate fate past 147k (does the rattle station, melt into fewer/faster pairs, or ignite a second storm? — checker2 at 196k: still intensifying, 5.8k c/ch, and the carry's amplitude follows it: body-level ramps to 2^22.6 that return; the amplitude-vs-clump-density law is the open measurement), the carry's bias structure (who holds the final Σres; DK_CAP interplay) and momentum-carry vector statistics (485f's lens section), rotational/symmetric rounding of the kick pair, a per-cell tide like the engine's frame — then re-fly the plateau-lifetime question on the fixed wiring. The engine-facing pricing question the clump opens: a standing ~85 partner-contacts/ch per hot body is a periodic surprise — the exact case for compiled/deferred **per-crowd** contact response (PRINCIPLES 3).
3. **The ringdown beyond n = 12800 and its onset law**: extinction at 12800 is flown (ded5); onset grew 1.7–2.5× across the octave vs side ratio 1.41, so the safe horizon rule is ~2× the 6400-relative horizon; detuning does NOT kill the mode (mass spread strengthens it; gapped genesis rings none) — the ringdown is the box's acoustic response (84b2, ded5).
4. The encounter-parity certificate's negative control (a law that skips at conjunction must fail it) and the μ = 1e-2 horizon past 4 P, blocked by the runaway tail.
5. The 3-IC driver discrepancy (b9be ↔ e846, one vote cleaner here: same crates code, later HEAD, reproduces e846 exactly).
6. The tilted oblique reflection: per-contact up to 0.155 rad, ensemble-invisible; integrator decision.
7. Stress the preservation: γ ≫ 250, resonant three-body, longer horizons.
8. Hunt a stronger cantorus (K near critical) to bound the Q → 0 distortion rate (toy).

## Contradictions

None open. e3b7's apparent tension with e56b (plateau vs no-plateau under gravity) is resolved by the wiring verdict: e56b's container is a wall (energy-exact), e3b7's is a leaking quantized field — different instruments, both correctly reporting their own law. The toy (5cad) and the shipped laws measure different error models at different Q, as recorded. c644's checker's post-32k hazard plateau and 3b67's decaying tail are the same series at different windows (17k vs 49k), as recorded above.

## Runs
- 20261014-2248-redteam-5cad (awaiting grade): shadowing clause false in mixed chaos;
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped law — trapping preserved
- 20261015-0128-inversion-3ca8 (silver, corrected in checking): shipped dense order
- 20261015-0128-dynamics-b9be (silver): dwell arm on the shipped plane law — trapping
- 20261015-0250-second-20261015-0128-inversion-3ca8-f50d (awaiting grade): exact
- 20261016-1319-dynamics-e846 (this run, awaiting grade): the 48 deaths decided —
- 20261016-1319-dynamics-e846 (gold): the 48 deaths decided —
- 20261018-0143-dynamics-80fe (this run, awaiting grade): the parity rate form — burst
- 20261018-0543-taleb-6de0 (this run, awaiting grade): the μ=1e-2 runaway is a clock
- 20261018-2040-dynamics-834e (this run): dense order to φ=0.78 — no avalanche, affine cost
- 20261015-0250-second-20261015-0128-inversion-3ca8-f50d (awaiting grade): exact twin
- 20261016-1319-dynamics-e846 (gold): the 48 deaths decided — real disk crossings
- 20261018-0143-dynamics-80fe (awaiting grade): the parity rate form — burst, two clocks
- 20261018-0543-taleb-6de0 (awaiting grade): the μ=1e-2 runaway is a clock storm
- 20261018-2040-dynamics-834e (awaiting grade): dense order to φ=0.78 — no avalanche
- 20261018-2312-dynamics-84b2 (this run): breathing mode priced — identity, ringdown
- 20261019-0141-second-20261018-2312-dynamics-84b2-ded5 (this run): 12800 flown to
- 20261019-0325-taleb-90b7 (taleb, awaiting grade): formation burst law — one-shot 3x; train needs swap symmetry
- 20261019-0435-dynamics-e56b (dynamics, awaiting grade): game case flown — one season, extensive hot plateau; no train; free space one-shot
- 20261018-2312-dynamics-84b2 (awaiting grade): breathing mode priced — identity, ringdown
- 20261019-0141-second-20261018-2312-dynamics-84b2-ded5 (awaiting grade): 12800 flown to
- 20261019-0325-taleb-90b7 (awaiting grade): formation burst law — one-shot 3x; train needs swap symmetry
- 20261019-0435-dynamics-e56b (awaiting grade): game case flown — one season, extensive hot plateau; no train; free space one-shot
- 20261019-1551-dynamics-e3b7 (awaiting grade): gravity-held belt — the kick tide fails its own cold-belt gate; fleet season evicts 86%
- 20261019-1656-second-20261019-1551-dynamics-e3b7-9b3b (awaiting grade): Pass belt flat to 49k (checker digests bit-for-bit); ladder: pump = the DK_CAP clamp zone below r≈2q (held e≤0.97, ejected e≥0.975, 3 clamped ch suffice; grinder speeds reproduced one-body)
- 20261020-0229-dynamics-c644 (dynamics, awaiting grade): the e-walk flown per body - killer is relaxation not the clamp zone (2/492 clamped); exponential hazard 3.3e-5/ch, self-quench remnant ~310
- 20261019-0435-dynamics-e56b (awaiting grade): game case flown — one season, extensive hot plateau; no train
- 20261020-1621-dynamics-3b67 (dynamics, awaiting grade): the quench is terminal — hazard→0, core ejects nobody, endpoint a sub-quantum ~150-body clump with a standing 3.7-5.1k c/ch rattle
- 20261021-0312-dynamics-485f (dynamics, awaiting grade): the contact carry ledger — bounded attractor (amplitude ~ 2m|k|), rattle is one crowd (median 42 partners/64ch, top pair 0.02%)
