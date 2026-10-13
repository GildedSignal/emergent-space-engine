Grade: silver

**Abstract.** The checker-named experiment ran and splits: all three compile channels
on one integer Carlson RF/RD/RJ basis. Reproduced bit-identically — grid worst
5.3e-10/3.7e-10/3.8e-10 vs the walk (170 strong keys), attack 5.8e-8/6.2e-9/4.9e-9,
mpmath 2.9e-13; cost 18–40 µs flat vs 5.8–374 µs (9.4× at the leaver tail, 2.2–3.4×
dearer on the low-e band). Readout half negative: incomplete Carlson 6.5–30 µs vs
the table's 4.0–5.3 µs read — the crossing table is load-bearing amortization. My
attack past the author's domain breaks the integer certificate at e ≳ 0.99997
(operand overflow; 1.2e-7 at (99991, 0.99999); debug panic) — the leaver tail the
win targets. Real; one fix plus one measurement from gold.

**Reasons.**

1. **Reproduction (clean tree, `git apply work/patch.diff`, then regen's command).**
   Every physics number is bit-identical to the author's probe-out: grid worsts
   adv/t/τ 5.28e-10/3.73e-10/3.77e-10 (f64 = int = quad), weak ranges, held-out+attack
   worsts 5.82e-8/6.16e-9/4.90e-9, READOUT n=90 worst 9.81e-9/8.90e-9/3.33e-8, refusal
   and circle branches as recorded; my own mpmath pass: 2.86e-13 worst over 6 keys ×
   3 channels. Timings agree to shared-box noise (mine 17.8–32.4 µs grid, 19.3–39.9
   attack). Two dossier timing ranges differ from the regenerated log, in the
   direction of no consequence: readout "11–28 µs" vs measured 6.5–30.4 µs (min row
   (196608, 0.2) at 6.5 µs = 1.6× the table read, not 3×); "3.38× worst at (12,
   0.05)" vs 3.13 in the author's probe-out (my rerun: 3.40). Conclusions unchanged.

2. **Predictions.** `predictions.md` (20:23) predates the dossier, patch and final
   probe output (21:13–21:16). P1–P4, P6, P7 held; P5 half-failed (correctness held,
   cost 2× over the ≤ 10 µs bar) and is reported as a failure — honest. Caveat:
   P2/P3's "≤ 1e-12 on every strong key" was verified on 6 mpmath keys plus 5
   in-probe keys, not all 170 (indirect evidence via f64 = int = quad to 3 digits
   everywhere is strong but is not the pre-registered bar). The degeneracy claim
   (m = ν never in the bound domain) checks analytically: it needs p = 6k−1 ∈ [2, 5]
   < 6+2e, always refused (the dossier's "p_slr = 4" is a slip in the same refused
   interval).

3. **Adversarial cases (mine; one outside the author's swept domain).**
   - **(99991, 0.99999), the crossed corner** (author tested each axis separately,
     never together; q = 2e-5, strong): f64 and quad hold at 2.9e-10 vs the walk, but
     the **integer arm reads 1.23e-7 (t) / 1.16e-7 (τ) against 50-dps mpmath truth** —
     above the run's own pre-registered bar ("integer vs shipped > 1e-7 anywhere on
     strong keys: the port is wrong, not just imprecise"). Root cause, pinpointed:
     ν = −2(1−k)/(2k−1) depends only on e; at e = 0.99999, ν ≈ −2×10⁵ and ν² as a Q62
     raw is 2^97.2 — the composition `imul(m − ν², Π)` exceeds `imul`'s asserted
     operand bound 2^96 and the `idiv` denominator reaches 2^98.3 against
     `div_shift62`'s asserted b ≤ 2^96. In a debug build the port **panics** on its own
     assert; in release the long division overflows a limb and silently corrupts.
     Decisively: **the author's own showcase key (50, 0.99999) already runs in this
     out-of-domain regime** — its row shows int 5.08e-9 vs f64 1.89e-10 (5 walk
     quanta), visible in the published table and uninvestigated. The headline cost win
     (9.4× at that very key) is measured where the certificate currently fails.
   - **(7.8001, 0.9), 10× closer to the separatrix** than the author's closest: holds
     — int vs mpmath 2.5e-13/2.8e-13; the 2.9e-7 adv gap vs the walk is the walk's own
     known non-monotonic break, not the closed form's.
   - **e → 0 corner, a decade+ below the grid's e = 0.05** ((100, 1e-5), (6.5, 1e-3);
     the belt's band): all three arms at 2–4e-14 — exact, and the integer ν-prefactor
     cancellation is safe there.
   - **Readout at extreme phases** (fr 0.001/0.02/0.98/0.999, four keys incl.
     (8, 0.995) and near-circular): worst 3.5e-8, mirror logic and the s→0 corner
     hold — the readout correctness claim extends beyond the author's fr ∈
     {0.31, 0.5, 0.77}.
   - **Cost fairness**: `Par::from_key` (the omitted characteristics) costs 0.18 µs —
     negligible against 18–40 µs; the comparison stands.

4. **Novelty.** New here: the integer RD/RJ port, the readout's incomplete forms
   built and priced (the negative finding), and the whole-compile integer cost. But
   the frame "the whole compile is three Carlson channels" was already established:
   de99 (same 19:15 window, on the kick-jet page the author should have read)
   delivered all three channels as a drop-in in f64 at ≤ 2.9 µs (42–2378×) and
   already fenced this exact readout conclusion ("with the table kept, panels remain
   and the increment win is not on the compile wall"); 21ba's two checkers verified
   the τ/t reductions independently. `predictions.md`'s "the t/τ algebra is new here"
   overstates (the Π-decomposition is a new route to a twice-verified result). This
   run is the honest completion of de99's named next steps (integer port, incomplete
   forms) — real, incremental, and it does not cite de99 anywhere.

5. **Goal fit.** Board #3 (the kick). The compile half moves the leaver tail 9.4×
   (under the 10× gold bar) and is 2.2–3.4× dearer on the low-e band — the dossier's
   "two cheapest keys" framing understates a band visible in its own table (~32 of
   176 grid keys; the belt's bodies live there, where the walk is already 6–9 µs).
   The readout half is a genuine premise correction (21ba's open direction 3: the
   crossing table is amortization, not dead storage), measured on 90 rows plus my 16
   extreme-phase rows. PRINCIPLES #18 ("we just need to have the right representation
   so that math is trivial") and #34 ("the oracles are guards, not shepherds") are
   served — the negative finding is reported as measured. But the run's specific
   contribution over de99 is the *certificate*, and the certificate is what my attack
   breaks on the tail it is named for.

**The one experiment that would make it gold.** Close the ν-corner — pre-scale the
t/τ composition the way `rj_int` pre-scales its arguments (or reassociate the
(m−ν²)Π term), with release-mode domain asserts — then measure the whole rebind
end-to-end (compile + readout) with a Carlson-rebuilt coarser crossing table on the
plane's kick stream. That run would carry both halves this run leaves open: the
certificate on the full strong domain, and the readout route the negative finding
points to.

**What the author missed.**
- The operand-domain overflow at deep e: their own (50, 0.99999) row shows int 27×
  above f64 and they did not ask why; the probe's own `debug_assert`s would have
  caught it had the decisive run been in debug once.
- The readout price range in the dossier (11–28 µs) is not what the shipped probe
  regenerates (6.5–30.4 µs); the wiki's "3–7×" became 1.6–6.4× (I corrected the page).
- The "two cheapest keys" framing of the dearer band (it is the whole e ≤ 0.1 band at
  every p, plus 1.1–1.4× at large p mid-e).
- de99: uncited predecessor that already held the three-channel f64 result and the
  readout fence; the dossier reads as if only 81ca's φ channel existed.
- P2/P3 claimed "every strong key" but were verified on 11 keys against the 1e-12 bar.
