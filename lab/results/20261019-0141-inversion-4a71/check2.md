Grade: gold

**Abstract.** d839's "memory wall is a constant, not a ratchet" holds only inside one light
diameter: the horizon rule both closes the door (`now ≤ deadline − 1`, deadline = event +
light distance, so `now − oldest ≤` the widest pending light gap: 2,302.5 s flat over 77k
game-s; 0–0.1 s at the corner and under burn) and opens it at scale. Reproduced exactly:
pins retain +1 generation/body per 27.6k game-s at ~2.2 KB a binding (N-independent, 2.3 KB
at K=10³); at D=6×10¹⁰ the census climbs linearly in play time, no saturation (148k retained,
RSS 204→381 MB), 20% of frames over budget. One item at 4 ly ⇒ ~9.2 MB/body [inference].
Adoption: `oldest`'s scope (per-body), a named one-line decision for E9; nothing to wire now.

**Reasons.**

1. **Reproduction** (regen exit 0; my own rebuild from `work/patch.diff`): the deterministic
   core matches the dossier — pins 3.00 and 5.04 retained/body at D=6e9/1.2e10 (author 2.93/
   5.04), RSS 281/383 MB (279/384), bpb end 1,726/2,221 (1,738/2,222), ctrl bpb 1,417 and
   census ~30.5k (1.02–1.07/body), `now − oldest` = D to the digit (29,552.9 / 59,105.9 s).
   Timing-derived digits vary on the shared box (ctrl max gap 1,655.1 vs 2,302.5; over
   0/83/724 vs 6/383/683) — disclosed as indicative; no claim rests on them.
2. **Predictions** existed before the decisive flights (file order and `flights.sh`/log times)
   and held: P1 on all three controls (and on my K=10³ control: 176.3 s, flat); P2's
   staircase, byte constant and no-return-while-pinned all reproduce. Two deviations: the
   disclosed +1 over the floor formula, and `hist_max` control ≤ ~2 vs measured 69 — a held-out
   miss the dossier reports only as an instrument note, not under Predictions. It is the
   locals (verified: K=10³ control holds 36 generations at 1.44/body total) and does not touch
   the belt-wide claim. P3 is labelled [INFERENCE] throughout.
3. **Attack** (three fresh arms, all outside the author's grid, `logs-check2/`):
   - **D = 6×10¹⁰** (a decade past the author's largest pin): gap 295,529.5 s = D exact; the
     census climbs monotonically with play time — 1,564 → 56k → 95k → 148k retained over
     59,933 gs, RSS 204 → 381 MB, ~57 MB per wave, **no saturation**; at equal elapsed it
     equals the 1.2×10¹⁰ arm (4.93 vs 5.04/body). So the law's correct form is
     1 + ⌊min(D, elapsed)/27.6k gs⌋ + ~1: the ratchet is linear in play time whenever one far
     item is pending — stronger and cleaner than the dossier's reading. 20% of frames over
     budget at 3×10⁴ (p50 7.7 ms vs 2.3 control).
   - **K = 10³** (a rung below the grid), same pin D=6e9: RSS 14 → 119 MB (8.5× at a tenth of
     the bodies), 44.8 retained/body, and the per-binding constant is N-independent:
     (119−14) MB / 44,600 extra bindings ≈ 2.3 KB. The dashboard bpb (10.3 KB) under-counts
     the ratchet again (~5× here, ~12× at 3×10⁴).
   - **Code mechanism** (the lens-independent half): `deadline_of` = `t + light_distance`
     (universe.rs:564) and the presented time is the horizon (universe.rs:1033–1046, 1085–1088)
     — the certificate's proof is in the shipped code. The frame cost is also code-confirmed:
     while pinned, `key_prune`'s `at = droppable_until + keep` stays behind `now`, so every
     history-holding body is re-walked each frame (p50 2.3 → 4.4 → 7.7 ms across D).
4. **Novelty.** The standing page's own Open directions (d839) name the pinned-`oldest` probe
   as unflown, and no HISTORY entry covers it. This run flies it, proves the bound
   structurally, prices the ratchet and corrects the current best's domain — a genuine
   extension of d839, not a repetition.
5. **Page.** The proposed `wiki/nladder.md` folds the result in faithfully (header, Refuted,
   Open directions, Runs). Corrected in place: "byte-identical no-op" → inert by mechanism
   (`keep ≥ 2²⁶` for every body, so the pinned horizon never binds; the kept logs are not
   byte-comparable), and appended the second-checker note with my arms. No other line
   overstates against the evidence.
6. **Goal fit.** Board item 4 (memory at 10⁹) and the bodies gap: the retention horizon
   couples every body's memory floor to the single oldest pending item in the universe, and
   the fix is a scope decision, not a margin. PRINCIPLES: "Nothing past c … it allows to
   cheaply partition compute, even gravity is light speed" (OCC#10) — the same cone that
   partitions compute must partition retention; and "a failed expectation is not automatically
   a failed method" — d839's constant is right inside its domain, whose edge this run measures.

**What the author missed.**
- The staircase's cleanest law — linear in play time, capped by min(D, elapsed) — his two pins
  both sat at or beyond the flight length, so the table reads as a function of D alone.
- The `hist_max` held-out prediction (control ≤ ~2 vs 69) is a miss and should have been
  listed under Predictions, not only refiled as an instrument note.
- The ctrl's 2,302.5 s is one timing-elastic sample (regen 1,655.1; K=10³ 176.3); the
  certificate's invariant (bounded, never growing) is what reproduces, not the digit.
- "Byte-identical" overstated the negative control (inert by code and census; no byte compare
  exists) — corrected on the page.
- The far-doll wiring remains the open half (the pin simulates the item; `apply`'s
  `ship_ticks` split is the code fact that decides it) — properly disclosed as such.
