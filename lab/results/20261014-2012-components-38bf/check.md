Grade: silver

**Abstract.** Claim: with `ES_PULL_CAP` (bf21's cap re-derived, default-unset), a player decision
landing mid-wave is O(1) — 0.168 ms once, ≤ 0.229 ms every frame through the wave, max frame 12.5 ms
against 1,487 ms uncapped — so the checker-2-bf21 input exposure needs no deferral machinery.
Reproduced: every counter (kicks 225,949; encounters; decisions) and the P1/P2 digest identity
(`c2b834bb…`) regenerate; bf21's certificate holds on this build. Checker adds: the uncapped input
control (0.154–0.158 ms at rtf 100 **and** 200 — the exposure never fires even uncapped), the
key-changing turn the author left untested (0.20–0.26 ms; 657 turns at 3×10⁵ hold 11.97 ms max,
1.38 GB RSS), and 3×10⁵ (0.161 ms). Adoption cost: none beyond bf21's cap. Not gold: two quoted
numbers do not regenerate and the exposure's "reality" was asserted, not measured.

## Reproduction

Clean tree, `git apply work/patch.diff`, `regen.sh` re-flown by the runner (exit 0) and by me
(8 further flights). The dossier's substance regenerates throughout:

- P1/P2: digest bit-identical `c2b834bb…` both runs, kicks 225,949 both, encounters 1,624 both;
  monsters 1,884.7 ms (regen) / 1,295–1,643 ms (my uncapped arms) vs the author's 1,486.9 — shared-box
  spread on a wall-clock number, same order. The `events` counter is pace-dependent exactly as
  disclosed (258,939/259,477/259,529/259,494 across runs at equal digest-relevant state).
- P3/P4 equivalents: input cost 0.154–0.371 ms across five runs (author 0.168/0.229), always
  ≤ 2 events resolved inside the call, max frame ≤ 12.7 ms, kicks always 225,949.
- The player sits in the root doll from frame ~888 in every flight (the exposure's precondition).
- `belt_first 300000`: the wave window is N-independent (13,376/14,072/14,473 — the stock bench
  constants are valid at 3×10⁵).

## Adversarial cases (mine)

1. **The uncapped input control — the exposure itself** (`one`, `ES_PULL_CAP` unset): 0.154 ms,
   2 events, at rtf 100 **and** at rtf 200 (0.158 ms; the uncapped engine's frame monsters are
   1,642 ms there, so the drain is demonstrably behind). The checker-2-bf21 exposure **does not
   fire even uncapped** at this scene and phasing: the scheduled pulls (the monsters themselves)
   keep the ship lane tiled up to the player's key, so `input` finds ≤ 2 due items. The dossier's
   "real as a mechanism and bounded by the same cap" is half right: the bound is real; the
   mechanism's *cost* never manifests in any regime I could provoke, capped or not. The claim's
   conclusion survives; its stated basis does not.
2. **The key-changing decision** (the run's named untested arm; `word(5,8)`, not the burn's
   `word(1,8)`): 0.201 ms at 2×10⁵, encounters −3 (a real decision moves the player's own scan),
   kicks equal, max frame 12.483. At 3×10⁵, 657 key-changing decisions every frame of the window:
   max 0.260 ms a call, max frame 11.971 ms, 0 over. Open direction 0 on the proposed page is
   answered affirmatively on this scene.
3. **Outside the tested range** (N = 3×10⁵, one decade direction on the board's own ladder; the
   author tested 2×10⁵ only): `one` 0.161 ms, max frame 12.107, RSS 1.38 GB; `theld` bounded the
   same. The seam is O(1) in N over the reachable range.
4. **P4 repeat** (the author's own named reproduction test): encounters 1,626 vs P2's 1,624 — the
   margin is **+2 this time, not +1** (author and regen both had +1). The direction holds (no-op
   decisions add a small log-level encounter delta; kicks bit-equal); "exactly one" does not
   regenerate. The author's criterion — "it is in the digest's chain, so it must reproduce, or the
   instrument is unstable" — resolves to: the instrument is unstable at this margin.
5. **Digest stability of decision-bearing flights**: the P3 digest in the dossier (`19ac13e7…`)
   did not regenerate — regen got `2bcaada8…`, I got `8955ad52…` at the same frame 8445 (and my
   *uncapped* one-decision flight reproduced `2bcaada8…`, the regen's capped value, at the same
   frame). So the one-decision digest is bistable-to-unstable across runs while every counter is
   stable — the wall-schedule instability 4487 documented for this instrument (page direction 12),
   here confined to decision-bearing flights (P1/P2 plain digests reproduced across three runs;
   my P4 digest `83da3109…` ≠ the author's `6cd32209…` either). The bench's own comment knows
   this ("the digest also hashes the input log, so it cannot be compared directly") — but the
   evidence table still lists P3/P4 digests as if they were certificates.

## Predictions

`predictions.md` predates `dossier.md` (10 m vs 4 m before session end; the author's raw
`out/flights.txt` was overwritten by the runner's regen, so the log order cannot be fully audited).
Content is consistent with pre-registration (failure arms pre-stated; the misses are informative,
not cosmetic): P1 held in substance (9 over vs "≥ 10"); P2 held in substance (digest equal; "0 over"
missed by 1–2 edge frames); P3 over-predicted the call ~20× (2–8 ms guessed, ~0.16 measured) —
honestly reported; P4 **missed in the informative direction** (hundreds over / 15–40 ms predicted;
1 over / 12.5 ms measured); P5's verdict (bounded; falsifier > 100 ms / > 1,000 events never fired)
held, and my uncapped and rtf-200 arms push it further than the author tested.

## Novelty

Checked against the page and the record: bf21 measured the *frame-path* pull (the monsters) and its
cap; 4487 built a different fix shape (drain inside `advance` + `Waiting` scans) and named the
wall-instability; checker-2-bf21 explicitly left `input` as "the real untested exposure". Nobody
had measured the input path. This run measures it, and the +encounter margin ("same keys is not
no event") is new. Not a repetition. Note one bad citation: **`session.rs:118` does not exist in
this tree** and no shipped caller of `Universe::input` exists outside examples — the realism caveat
("the shipped page calls `input` on key change only") is unverifiable here.

## Goal fit

The board's top line is the wave seam on the N ladder; this closes the last unbudgeted
player-facing path on it and removes an adoption caveat on bf21's cap. PRINCIPLES #5 ("The player
is the only wildcard, and their influence travels at c" — the wildcard's entry point costs O(1))
and #12 ("i care about the p95/99 results" — the every-frame adversarial case leaves the frame
profile flat). Judged on behaviours and counters, not trajectory identity (#2). The lens honestly
names what it nearly missed. The gain is a de-risking plus a design-option deletion, not a new 10×:
the 118× monster kill is bf21's, re-derived.

## The one experiment that would make it gold

Fold in the two arms the run left out — the uncapped-input control and the key-changing decision
(both flown by this check: 0.154–0.158 ms uncapped at rtf 100/200; 0.20–0.26 ms for turns at
2–3×10⁵, 657 of them holding 11.97 ms max) — and restate the margins as they are: encounters
+1 to +2 (pace-dependent), the one-decision digest non-regenerating (decision-bearing digests at
the 16 k cut are not comparable; use counters). With that, the input seam is closed from both
sides and the cap adopts with no input caveat — that version is gold.

## What the author missed

- The uncapped input control: the single flight that would have tested "real as a mechanism"
  directly; its absence leaves the run's framing claim resting on code reading (and my control
  shows the mechanism never fires as a cost on this scene).
- The turn arm (their own named held-out case, one flag away in their bench).
- "Exactly one encounter" stated as exact on one seed when their own dossier flags the
  reproduction test — and it fails it (+2 on re-run).
- Decision-bearing digests quoted in the evidence table as if regenerable.
- `session.rs:118` cited twice (dossier, bench header, wiki block) for a file that does not exist
  in the tree.
- Lens bias, correctly self-identified on the schedule half; the log-level margin was found by
  counter comparison, which deserves the emphasis it gets.

Grades on the corrected page restored from the truncated tail the resolve script dropped:
6138 silver, 7f99 gold, a2c1/0e37/b29a/effb/3071 silver.
