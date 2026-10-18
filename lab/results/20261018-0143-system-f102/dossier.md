# Dossier — 20261018-0143-system-f102 (system lens)

**Claim.** The scan memo's reuse walk — repaired separately by the scan-queue page (direction (d),
"memo the candidate list") and the memory-h-live page (the byte-fence at capture) — is one
mechanism re-derived twice, and it cannot be made cheap: no change-signal coarser than the
candidate set certifies a duplicate (global, binding-guarded and per-doll versions all miss
every duplicate: 0/220), because between two same-tick captures the frame always mutates the
scan's own doll outside its candidate window; the walk IS the proof, the duplicate class is
manufactured upstream by the player's kick re-timing (48% of burn captures, 220/460), and the
sound lever is deleting the duplicates, not memoizing the walk.

**Bottleneck.** Not a new one: this closes a wrong turn on two open directions. The scan-queue
page's direction (d) and the memory page's capture fence both assume the eager candidate build
is overhead around the memo; measured, it is the memo's soundness proof at exactly the
granularity of the read set, so "memo the candidate list" is either unsound (an unvalidated key
returns stale answers after a kick rebinds the player) or saves nothing (a validated key is the
walk). What would have bought 10×: nothing here — the duplicate class costs 44 µs each, 9.7 ms
per 2-s flight, 0.24% of wall at the plane's scene (N=10³ burn): a non-bottleneck at the flown
N, killed as a direction, not promoted.

**Evidence** (all from `regen.sh`, Linux/x86, loadavg 8-11 on 8 vCPU recorded in the log; the
scene is `scenario::plane_extra` seed 1, threads 1, members 48, the shipped flight loop at rtf
100, 12 ms budget, 120 frames; every digest below regenerates bit-identically):

- The duplicate class, measured with the shipped memo's own verdict (`ES_MEMO_FIRST=verify`
  builds the candidates AND compares, then classifies against the cheap key):
  - burn N=10³: `captures=460 both_hit=0 cheap_only_soundness=0 rebuild_only_lost=220 fresh=240
    walk_repaid_ms=9.71 walk_repaid_per_dup_us=44.1` — 47.8% of captures are duplicates whose
    full candidate walk is re-paid (44 µs each ≈ the fallback walk over 1,028 bodies at ~43
    ns/body);
  - coast N=10³: `captures=19 fresh=19` — no duplicates at coast; the memo is inert there;
  - the interleaved mutations are exactly the 5 October class: same-`t` recaptures whose
    inter-capture `put`s changed no binding any reader at `t` can see (the shipped comparison
    granted reuse 220/220 in those slots) while the store's mutation count moved anyway.
- The cheap-key family, measured to miss everything it was meant to certify:
  1. global store+radial version: 0 hits (`rebuild_only_lost=209` in the first arm, before the
     guards below — every duplicate follows some mutation somewhere);
  2. binding-guarded `put` (bump only when the binding or alive moved, `same()` in `put`):
     still 0/217 — the mutations between duplicates are other bodies' kicks, not plan re-times
     alone;
  3. per-doll versions on both the store and the radial index (a scan reads only its own doll's
     bodies): still 0/220 — the frame kicks the scan's OWN doll outside its candidate window
     (belt ships in the root doll, far radial bins), which no doll-level counter can exclude.
  - Soundness held everywhere: `cheap_only_soundness=0` on every capture of every arm (a
    version-certified reuse always agreed with the shipped comparison — it just never fired).
- Outcomes are unchanged by construction and measured: within each run of the three modes the
  digest is bit-identical per flight (first run at loadavg 8-11: `d976e91f…` burn 10³ ×3,
  `be73e0a8…` coast 10³ ×3, N=10⁴ verify `81e5739a…`; regen rerun at loadavg 5.4: `a961253c…`
  ×3, `2389ab28…` ×3, `86690d0c…`), and the flag-on flight's engine cost is unchanged (p50
  6.1 ms on/off) because the cheap key never hits. SCOPE, disclosed: the digest of a whole
  flight moves with machine load across runs (the 12 ms budget is wall-time; the canonical
  determinism harness is the wiki's budget-free `ladder_digest`, not this loop) — the
  probe-innocence evidence is the within-run mode equality, which held at both load levels.
  The per-duplicate walk price accordingly spans 17-74 µs across loads (44.1 at load 11, 29.2
  and 74.3 at load 5.4); orders of magnitude only, per the lab's rule.
- The shipped crate's own suites pass on the patched tree (`cargo test --release -p
  emergent-universe --lib --tests`: 40 passed, 0 failed — including the frame-loop
  digest-equality tests, the patch-innocence control at test level). `held_max` differs across
  modes (20/34/17) — the drain is wall-budget-interleaved; the digest is the canonical outcome
  and is identical (the wiki's own standing result: peak held is not canonical).
- Held-out (predictions.md, written before these runs): N=10⁴ burn — the duplicate FRACTION
  held (220/460, as predicted: the re-timed pending kick is the player's own, N-independent),
  but the per-duplicate walk FELL 2.5× (17.5 µs vs 44.1) instead of growing 8-12× as I
  predicted: at 10³ the capture is in cdf0's fallback regime (walks every body), at 10⁴ the
  apsidal filter holds (threshold ~25,081) — my prediction ignored the page's own threshold
  finding. Prediction 4 wrong on price, right on fraction; predictions 1-3 held exactly.

**What would make it wrong.** A change-signal at candidate-set granularity (per radial bin, or
per-body versions joined against the near list) could certify reuse below the walk's price; the
run does not measure one — it measures that every natural coarse grain (world, binding, doll)
fails, and argues the bin-joined form re-derives the near list itself. Also: at belt scale
(3999/7343's band) the walk's price is the fallback disease (30-34 ms at 10⁵), where a
population-level answer or the phase-neighbour rank deletes the whole capture, duplicates
included — there the walk dies as a side effect, without any memo.

**Cost of adopting.** Nothing to adopt as a cure; the patch is a print-only probe plus dead
sound counters (u64 bumps in `put`/`push`/`retire`/`prune`, `note`/`rebuild`, two loads per
capture) — keep or drop both ways, digests identical. The ADOPTION the run argues for is
negative: strike scan-queue direction (d) as stated, and spend the effort where the duplicates
are made (the player's kick re-timing — already the burn tail's owner on the nladder page: the
same one mechanism named twice by two pages).

**Fit with PRINCIPLES.** "Compute only surprises" (§3) is why the walk looked like waste — but
the surprise here is manufactured (same-t recaptures), and the engine's own change signal is
the surprise detector; "a fix signals the wrong representation" (§19): two pages fixing one
walk was the signal, and the representation error is upstream (the re-timed pending kick that
re-scans a tick), not in the memo. Via negativa: the cheapest compute here is the duplicates
never taken.

**The lens.** The whole-system lens found the unification (two pages, one function,
`encounter.rs:174-199`) and the elegant trap: the unification I wanted (one cheap signal, two
cures collapsed) is exactly what the measurements refuse — elegant unifications can hide a hard
special case; here the case is ordinary (a frame kicks its own doll while re-scanning one
tick). What the lens missed until the data: the duplicate class is small at the flown N — the
systems view said "two repairs, one mechanism", but the mechanism was never load-bearing at
this scale.

Commands: see `regen.sh` (8 flights, ~90 s wall on the loaded box).
