Grade: gold

**Abstract.** Claim: representation.md thesis 3 + L50 as the attitude law, shipped as
`thrust.rs`'s heading accumulator, cannot carry the non-abelian part of SO(2,1); the frame
rotates by exactly (γ−1)·ψ per constant-γ turn, and at the game's flights the error reaches
12–74° nose, 0.27 c, 48% of path. Reproduced: regen bit-identical (8.4 s), plus two
from-scratch instruments (FW-transport RK4; scaling-and-squaring exponentials) matching
every number to the digit and the law to <0.0001°. Predictions pre-registered; 9/10 held.
Beyond the swept range (γ 10–62, the record's pump speeds) the brake's nose
error grows to 120–156°. Wiring verified in shipped source. Cost of adopting: one unit
split-quaternion per thrusting body plus one view rotation — the doc's own §1 algebra
(cheaper in argument, not measured).

**Reasons.**

1. **Reproduction, twice independent.** `python3 falsifier.py` regenerates results.json
   bit-identically (only `timing_s` differs: 8.63 → 8.33 s; every command ≤ 60 s). My own
   instruments share no code with the author: (a) Fermi–Walker transport RK4-integrated
   along the analytic constant-γ worldline gives sky = −(γ−1)·ψ to <0.0001° at β 0.1/0.5/
   0.6/0.866 (contam 1e−14), and agrees mod 360° at every β up to 0.99987 (γ 62) — e.g.
   β 0.99, ψ 180°: −15.986° vs −1095.986° = −15.986 − 3·360; (b) exact held-key flights via
   scaling-and-squaring exponentials (author: Taylor-8) reproduce the γ 2 flights exactly:
   off45 sky −18.04°, nose 12.06°, pos 6.61%; off135 sky −26.18°, nose 55.78°, β_err 0.2748,
   pos 22.25% — the author's numbers are algorithm-independent. Two-boost Wigner angle
   42.8961988683° = 2·atan(tanh²(φ/2)) confirmed by my own arithmetic and hand derivation.
2. **The shipped-law replica is faithful.** I read the shipped code: `owed`
   (`thrust.rs` L134–146) advances the heading additively (`heading.wrapping_add(dh)`, burn
   at the midpoint heading); `burn` is exact boost composition — the falsifier's
   `shipped_step` matches it verbatim in the flat limit (u₂ = u·ch + (n + u(u·n)/(γ+1))·sh).
   `view.rs` L293 takes the heading from the same accumulator, L309 aberrates with velocity
   only, L420 renders `heading` from it; `lorentz.rs`'s `Frame` is rotation–boost–rotation.
   Grep: no Thomas/Wigner term anywhere in the tree. So the missing rotation is
   player-visible in both the nose and the whole sky, and the author's disclosed gap ("a
   tree run should fly one burn") is closed by direct source verification: letter = wiring.
3. **Held-out predictions.** predictions.md (17 m before falsifier.py's final write, log
   order consistent). P1/P2 controls exact (0.0, −1.8e−13); P3 42.9° ∈ (20°,60°); P4 180° >
   90°; P5 90° ∈ [50°,130°]; P7 48.2% > 5%; P8 monotone (0.45° → 548° at ψ 90°). P6 missed
   and reported as missed. One slip: the dossier's P6 explanation says the off45 burn turns
   the velocity "~45° in total"; the author's own trajectory data (and my instrument) give
   10.8° — prose error only, it strengthens, not weakens, the reported miss; the wiki page
   does not repeat it.
4. **Adversarial, beyond the author's domain.** (a) The record's pump speeds, γ 10 and
   γ 31.6 (author swept flights only at γ 2, turns to γ 7.09): off135 brake nose error
   119.9°/155.7°, position 20.5%/20.2%, sky −45.5°/−49.7° (step-halving stable) — the claim
   is understated at the game's daily speeds. (b) The (γ−1)ψ law verified by independent
   FW transport to γ 62. (c) Path-reversal control: +120° then −120° at β 0.9 returns the
   sky to 0.000000° — the effect is structural rotation, not integrator drift. The
   semantic counterattack ("the accumulator is the law by fiat") fails: under that reading
   the trajectory is legal but the seen sky is still wrong by the same closed form
   (principle 30), and the state (h, u) forces R = I in B = R·B_pure — one constraint the
   physics violates; whichever semantics is intended, sky or trajectory is wrong.
5. **Novelty.** No H entry or wiki page carries Thomas rotation in the player's flight.
   Nearest: e8f7 (20261014-1631) falsified additive doll-key shears and explicitly deferred
   the "Wigner axis error … owned by the spatial turn machinery if anyone's" as
   second-order for keys; this run is that owner — different organ (thrust/view vs
   re-emit), first-order, player-visible, with the closed forms e8f7 lacked. 1885 on the
   same page refuted a different letter (aggregate readout). The proposed page fold is
   faithful: every number in the new block matches results.json; one NEW block, one
   Refuted entry, one Runs line.
6. **Goal fit.** A premise of bottleneck 0 shown wrong with controls on both sides and a
   freezable bar ("a turning flight at γ ≥ 1.1 must carry (γ−1)ψ in sky and nose; negative
   control: the accumulator, missing by exactly (γ−1)ψ" — behaviour-judged, no trajectory
   identity, complying with the r2 lessons). Principle 30: "what really matters is
   navigation, knowledge and dynamics those need to be perfect" — the dynamics themselves
   are wrong by half a path in one maneuver; principle 19: "if you find yourself fixing
   things that's oftentimes a signal that it is the wrong representation"; principle 2/13:
   a whole missing component of the Lorentz group, an error of type, not size — no carry
   width shrinks it.

**What the author missed.** The "cheaper cure" (closed-form held burns as one-parameter
subgroups) is argued, not measured — the rung should price one quaternion flush against
today's per-flush composition; the dossier's P6 velocity-turn figure is wrong in prose
(~45° vs the true ~11°); the field half (geodetic precession in curved dolls) is scoped
out but will add to the same accumulator's replacement — the freeze bar should state its
flat-frame domain so the curved extension is a new rung, not a silent extrapolation.
