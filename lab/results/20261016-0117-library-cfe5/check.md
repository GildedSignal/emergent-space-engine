Grade: silver

**Abstract.** Claim: the birth plan pass (board bottleneck #1's birth rail) is not an irreducible exact search — 30% is the planets' exact states re-derived once per body, deleted digest-identically by a birth-only hoist (33→23 µs/body); the searches are 0.1%; the bulk is the per-body clock derivation. Reproduced from a clean tree: every digest bit-identical on my own 8-arm grid and on adversarial arms beyond the author's domain (seed 3, N=10³, N=3×10⁵ flat at 30.4%, RSS 688 MB). Gain: 1.4× on the pass now; the named shared-readout rung predicts ≲13 µs/body (2.5×). Cost to adopt: ~60 lines, no behaviour change. Not gold: the author's central prediction failed (30%, not >50%) and the largest term is attributed by arithmetic, not a timer.

**Reasons.**

1. **Reproduction.** Applied `work/probe.patch` myself on a clean tree at the base commit (d8e7176), rebuilt, re-flew the full 8-arm grid: pass 33.68–33.94 µs/body (dossier 32.63–33.49, runner's regen 32.18–33.10 — box noise, orders identical), secondaries 10.17–10.35 = 30.2–30.5%, hoist-on 22.91–23.63, terminal 0.05 µs/body (0.15%), project 15.67–16.10 incl. its secondaries read, `sec_calls` = n+28 exactly, 7 memo keys, and every digest equal across hoist arms and equal to the runner's regen log. The regen path (patch travelling in regen.sh because run.sh's capture returned an empty patch.diff) is disclosed and works.

2. **Predictions.** `predictions.md` (mtime 01:22:28) precedes the author's flights (author-final 01:29:36) and reads as a pre-flight code read. Held: terminal <10% (0.15%), one secondaries call per body exactly, share flat in N and seed. Failed, reported honestly: secondaries >50% (it is 30%). Partially held: hoist <18 µs/body (got 22.8–25.4 — the `source()` reread is a second path the memo does not cover). A failed central prediction bars gold on the "held-out predictions held" rule, exactly as the dossier itself says.

3. **Attack (three cases outside the author's domain).** (a) Held-out seed 3 — 404b's held-out seed, never flown by this author: 10⁴/10⁵ give 30.2/30.3%, hoist 23.76/25.40, digests identical. (b) N=3×10⁵, the next decade up: 30.4%, hoist 23.79, digest identical, peak RSS 688 MB — flat in N holds. (c) N=10³, below the range: the share dips to 26.7% (8.40 of 31.49) and the hoisted pass is 22.93 — the mechanism holds but "30%" is a 10⁴–3×10⁵ number, not a constant of the ladder; at 10³ the recompute is cache-resident and cheaper.

4. **Mechanism, code-verified by me.** `Ctx::secondaries` (ctx.rs:79) recomputes every source's cartesian state per call and is called exactly once per body at birth (`open`, step.rs:487, for non-clock bodies; `project`, step.rs:614, for clock bodies). The memo key (doll, tick, except normalised to a source or none) is exact; `Universe::digest` (universe.rs:1266) hashes every body's plan, clock constants (ds/c/b), register and carries, so digest identity is a real behavioural check, not a tautology of a transparent memo. The second read path `ext::constants` → `source()` (ext.rs:133–153, called from `plan_clock`, step.rs:630) exists and runs once per clock body — but its µs share is unmeasured; the dossier says so, and I corrected the wiki page where it stated it as settled.

5. **Novelty.** The standing nladder page's open direction #1 is exactly this question ("attribute the plan pass's interior … irreducible exact search vs bookkeeping"); 404b's checker had only split replan 28.2 vs apply 4.2 µs/body. No prior run attributes the interior or flies a shared-state hoist — the 5 October kick-memo and 8b89's ES_LAZY_ALL are different mechanisms. The refutation of the "irreducible search" horn is new and closes the direction's first fork.

6. **Goal fit.** Bottleneck #1 (28 bodies against 10⁹). PRINCIPLES: "the cheapest compute is compute not done"; "Compute only surprises" — a body's birth re-derives per body what its own tick already knows. The cut is 1.4× on the pass (~23% of the whole birth rail), not 10×; its value is the attribution and the named next lever.

7. **The lens.** All five quotes verified verbatim in `work/library.json` (770 books) with correct authors: Asimov (Foundation and Earth), Taleb (Antifragile), Kaufman (Personal MBA), Jorgenson (Almanack of Naval Ravikant), Taylor (We Are Legion). Two lessons flown; three are mappings to named rungs, not measurements — honestly labelled.

**The one experiment to gold:** wire the shared "planets at t" readout as a real change serving *both* paths (`Ctx::secondaries` and `ext::constants`' `source`), fly it at 10⁵ with digest identity, and re-price the pass (predicted ≲13 µs/body) plus a timer on the remainder (constants vs kepler/field scalar chains). That deletes the reread as a component instead of measuring around it, and the 10⁹ arithmetic then rests on a flown number.

**What the author missed.**

- The 10³ corner: the share is not constant down the ladder (26.7%); at 10⁹ — the actual target — cache behaviour shifts again, so the hoist's value at scale is the deleted arithmetic, not this box's measured Δ.
- The probe's memo-hit path still pays a per-body `Vec` clone (Rc + clone) and HashMap lookup, so 23 µs/body overstates the true shared-readout floor; the ≲13 µs prediction should say so.
- `ES_BIRTH_SPLIT` is vestigial in the patch (the meters are unconditional; the env var gates nothing) — the dossier's "ES_BIRTH_SPLIT counters" phrasing suggests gating that is not there. Harmless (~0.1 µs/body overhead).
- The ~2.8-of-~6 core-hours at 10⁹ repeats 404b's ~6 without 404b's checker condition (that figure is M1-conditional, single-box until re-measured).
- `term_calls` ≈ 2 per body (19,740 at 10⁴), unremarked — immaterial at 0.05 µs/body but the "calls law" framing covered only secondaries.
