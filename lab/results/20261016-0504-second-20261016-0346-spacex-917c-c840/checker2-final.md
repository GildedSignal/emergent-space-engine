Working...
**Grade: silver** — written to `check2.md`, with the wiki page's Refuted entry corrected in place (env-drop → stale-xtask mechanism + my bounded-variant result). Tree restored to clean.

**The check in brief:**

**Reproduced first-hand, bit-exact, on a clean tree + `work/patch.diff`:**
- B13 armed (engaged): **0/64, worst ΔE/ΔL 4.65e0** vs off 60/64 at 2.12e-2 — the dossier's headline, exact
- 13/13 armed `ladder_digest` digests change; my outputs byte-identical to the record's; off == pristine
- `analyze.py` output identical; moon rates recomputed (max |armed−off|/|ref| = 2.92e-2, escape classes 3/3/3)
- Mechanism verified: bare ship birth (`plane.rs:65-73`), engagement 64/64 in the author's trace, `stagger_hash(1) = 0.566561`

**Adversarial cases (one outside the author's range):**
1. **Bounded quarter-fraction stagger** (their named-but-unflown next falsifier): **2/64, worst 1.47e0** — the kill is first-order in *any* first-kick shift, generic to the configuration class, not the 0.5666 draw. This strengthens the kill.
2. `ES_STAGGER=0` == off exactly; engaged B14 armed: timeout (P3 holds engaged).
3. **The root cause of the record defect**: touching `step.rs` + regen.sh's build line compiles `xtask` **zero times** — the `--example` target filter drops it, so a warm target dir silently keeps a pre-stagger binary. That is why the runner's own regen printed `B13 armed: 60/64` identical to off, through the `env ES_STAGGER=1` form — which cannot drop a variable. The author's "env-drop" diagnosis is refuted; a stale binary explains every instance.

**Why silver, not gold:** the physics is real and decisive (the parent's adopt-as-birth-default direction is dead, the cure correctly routed to the birth program), but the run's own reproduction script printed the *opposite* verdict on the runner's execution — "a headline the log contradicts" is the lab's own recorded demotion. The gold step: build xtask unfiltered + an engagement canary in regen.sh, re-fly so regen.log itself prints the engaged 0/64.
