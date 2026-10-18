Grade: gold

**Abstract.** The μ = 1e-2 runaway tail is an event storm of the root clock on minted
ejections, not captures. Blind reproduction from a clean tree: 10/144 capped ICs hold 52.3%
of 1.98 M events (median 7,329, 230 kicks/P, 9 dead); the μ = 1e-3 control at 64 P caps 0/144
(median 276 kicks/P). Traced: ejected at 9.4 sep, never inside 58 R_p, doll 0, handoffs 0,
2.0000 events/kick; dv/kick 6.44e-7 with zero sign changes in 32,824 samples; dt·y = 2.617
= Δs/b from shipped constants exactly (Δs = 2⁻²⁶); the two-term identity dt·y = Δs(1/y + 1/b)
closes to 2e-5; last 25,600 kicks advance 7.5e-9 P (579,431 ticks, exact). Held-out: 32 P
caps 31/144 (69.6%), μ = 3e-2 at 8 P caps 19/144 (79.6%) — beyond the author's domain.
Adoption: none (no code change); kills the capture/octave line, redirects direction 3 to the
clock's constants. μ = 1e-2 not flyable as built.

**Reasons.**

1. **Reproduced, bit-level.** I applied `work/patch.diff` myself, rebuilt, and regenerated
   everything into fresh scratch directories (since removed): both screens (all ensemble numbers exact:
   10/144 at 52.3%, median 7,329 events, 230/276 kicks/P, 9/10 dead), the grinder walk
   (424 → 964 events/P, lock to 400,000/P at 10.2 P), per-event cost 49 → 110 µs (×2.2),
   the deep trace (dolls {0} throughout, handoffs 0, r_star 9.44 sep, min r_pl 58 R_p,
   interval 232 → 22, freeze 579,431 ticks = 7.51e-9 P — the dossier's exact digits). The
   runner's regen.sh timeout was its own clock (only the build logged); the commands
   reproduce.

2. **Mechanism closed against shipped code.** ext.rs: `y = max(level + c, c/8)` clamps only
   from below; `ticks()` floors at 1; `constants()` are read once and never re-derived;
   MIN_STEP never enters `kick_clock`'s own step (step.rs:700-724). My arithmetic: c =
   1.8975e-10 (floor branch), b = 30c, Δs rounds **down to 2⁻²⁶**, so A = Δs/b = 2.6176 —
   measured dt·y mean 2.617 over 32,825 tail samples; the full two-term identity closes to
   2e-5 on both my traces. The dossier's "Δs/b = 3.69, 30% my-c-error" was the missing
   power-of-two floor (the page's checker bracket is right; I re-derived it independently).

3. **Held-out and adversarial (all pass, two beyond the author's domain).** (a) Horizon 32 P:
   31/144 capped, 69.6% of events, 21 new storms entering at 17.8–31.2 P — arrival continues
   with horizon. (b) μ = 3e-2, 8 P: 19/144 capped, 79.6% — a mass the author never ran. (c)
   An untraced capped IC (−0.955, 147.3): ejected at 11.7 sep, never inside 909 R_p, doll 0,
   already on dt = A/y with y = 1.33·v²/2 — the register-mint variant, independently
   confirming the page's bracket. (d) Chunk control: chunk 20000/5000/500 give identical
   kicks/events — caps are not budget artifacts. My 1.5 M trace also shows the ratchet
   continues past the dossier's β = 0.199 to v = 0.489 at interval 22 — the unboundedness
   was undersold, not overstated.

4. **Predictions.** `predictions.md` (05:51) predates the decisive outputs; the misses (P1
   captures, P3 top-1 share, P5a death concentration) are reported as refuted by the author
   himself — the deciding storm clause (P2) held exactly, with the wiki's 231/267 kicks/P
   reproduced on both masses as the instrument control.

5. **Novelty.** The live wiki's direction 3 posed exactly this question ("captures →
   ever-shorter radial periods" vs "a genuine event storm … decides whether μ = 1e-2 is
   flyable at all"); 80fe recorded only the cost wall, cause unknown; HISTORY and the docs
   hold nothing on the clock freeze. The mechanism, its exact closure, and the refutation of
   the capture reading are new. The proposed page folds the result in faithfully; every
   checker bracket in it matches my independent numbers — no correction needed.

6. **Goal fit.** The board's smoothness/allocator question behind direction 3, answered:
   no scheduling work pays at μ = 1e-2 until the law changes — "the allocator cannot
   schedule around a frozen tick". PRINCIPLES 13 ("Errors never compound … basically we
   don't want errors that can compound") — this is compounding minted energy, the exact
   forbidden class; and 19 ("a fix signals the wrong representation") — the run names the
   wrong representation (stepping an unbound body) and the fix shape, without patching it.

**What the author missed.** The Δs power-of-two round-down (the 30% "c" gap — resolved in
checking, twice independently). The ratchet's reach past β = 0.2 (v = 0.49 at 1.5 M events,
still one-signed). The register-mint variant among capped ICs (found by the first checker;
my unseen IC confirms it). Still open and admitted: the trigger rate at μ = 1e-3 over 512 P
(measured only as zero in 64 P), and no integrated truth exhibited on the capped ICs — the
impossibility argument is escape-speed arithmetic, which I verified (v_orb 4.33e-5, planet
surface escape 6.4e-4, minted v 0.49 = 1.3e8× orbital KE), not an integrated reference.
Minor: I could not hand-reproduce the kick branch's magnitude constant (6.4e-7) from the
outside (my naive tidal composition gives ~1.5e-8; likely incomplete field terms) — the
one-signed constancy, both branch identities, and every consequence are verified; the
storm's engine (the drift collapse) closes exactly.
