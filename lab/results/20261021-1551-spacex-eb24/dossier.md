# The scan's walk, attributed; and the pre-check's three dead certificates

- **Claim.** The scan-news page's od 3 (the exact pre-check that "deletes 47–50% of captures'
  walks") is dead as any mutation-counting certificate — three forms wired, all measured at
  **0 hits** on the shipped plane, each killed by a named mechanism — and the deletion it
  promised is real but reachable only by the value-equality domain the memo already implements,
  i.e. the walk itself; meanwhile od 1's attribution says the news-fed window must eat the whole
  walk (radial query included), whose price I measure per arm, with the waste at the wall
  measured at **60% of walk time**.
- **Bottleneck.** The scan row (`scan-locality` od 3: the scan is the pull's successor at rtf
  2000, 38.8 ms worst item under the cure, p99 35.6 ms against a 12 ms budget). The lever the
  page named: the walk's overpayment (9b03: news fraction 1.2–11.4%, memo 47% same-tick).

## Evidence (Linux cloud x86, i7-4790, seed 1, 20 s wall, 12 ms budget — orders of magnitude)

Instrument: `examples/scanpre.rs` (nladder's scene and flight loop, `plane_extra`), the walk's
halves timed under `ES_SCAN_SPLIT=1`; the pre-check under `ES_SCAN_PRECHECK=1|2|3`; the settled
`digest` (schedule-independent by construction) is the identity control. Clock-pair calibration:
**36.2 ns** a timed call (`/tmp/clkcal`), so per-call lookup numbers below carry that bias;
`build = loop − lookup` is bias-free. Full commands: `regen.sh` (~3.5 min).

| arm | captures | near/cap | cands/cap | me | radial | loop | lookup (bias 36 ns/call) | build | memo hits |
|---|---|---|---|---|---|---|---|---|---|
| A 3e3 coast rtf100 | 377 | 2992 (fallback 97%) | 325 | 55 ns | 28.3 µs (10%) | 252 µs (90%) | 131 µs (44 ns/call → real ~24 µs) | 121 µs | 0 |
| B 3e4 coast rtf100 | 377 | 201 (fences) | 178 | 55 ns | **79.2 µs (73%)** | 28.5 µs (26%) | 9.9 µs (real ~3.4 µs) | 18.6 µs | 0 |
| C 1e5 burn rtf100 | 2266 | 71 | 66 | 44 ns | 11.6 µs (52%) | 10.9 µs (48%) | 3.4 µs (real ~1.1 µs) | 7.4 µs | 855 (37.7%) |
| D 1e5 burn rtf2000 | 3427 | 3933 (max 100,076; fallback 129 = the wave-era bail) | 3911 | 43 ns | 16.7 µs | **1.155 ms** | 662 µs (real ~520 µs) | 493 µs | 1307 (38.1%) |

1. **The walk's overpayment, in time.** `memo walk_ns` — walk time on captures the memo then
   discards: C **18.7 ms of ~51 ms** total walk (37%); D **2.43 s of ~4.0 s (60%)**, with the
   fallback captures (near up to 100,076 = the whole doll, 7b6f's channel) exactly where the
   repeats concentrate. The ceiling for any pre-walk reuse on these arms is 37–60% of walk time.
2. **Od 3 refuted as a cheap certificate.** Three exact forms, one binary, digest identical to
   off on every arm (C: `c1e220b4…` across pre=0/1/2/3 and two builds):
   - **v1, one global epoch** (bumped by every put/push/retire/prune): **0 hits** — the belt
     kicks between same-tick captures.
   - **v2, per-row epochs over the near list + per-doll registration epoch:** **0 hits**;
     miss attribution on C's 861 memo-eligible captures: **miss_me 861/861** —
     `encounters_for_player` runs immediately after the player's own `apply`, which always
     `put`s the player's row, so the player's own epoch is always dirty at this call site.
   - **v3, `me` compared by value** (one `binding_at`, the walk's cheapest term) **+ per-row
     epochs:** miss_me 0, but **miss_near 723, miss_reg 138 → 0 hits.** The near rows are
     bumped by rebinds that change no reading at t: history-retiring rebinds preserve
     `binding_at(j, t)` through the retired segment — the memo's value compare sees identity
     where every mutation counter sees change. **The reuse law is value-equality through
     history, not absence of mutation; the exact pre-walk certificate costs the walk it means
     to skip.**
3. **Od 1's attribution (the news-fed ceiling).** No arm is build-dominated: the fence arm B is
   **radial-dominated (73%)** — a news-fed candidate list that keeps re-querying the radial
   index caps at ~26% there; the fallback arm A is **loop-dominated (90%, build 43%)**; C is
   radial 52% / loop 48%. A news-fed window must replace the radial query and the row reads
   together (membership maintained at kick/birth events, as 9b03 proposed) — that is the whole
   walk, priced above per arm.
4. **Identity controls.** Settled digest bit-identical across pre forms on A/B/C (A
   `cb15b4dc…`, B `37bb4a62…`, C `c1e220b4…`; also identical between the v2 and v3 builds) —
   the pre-checks are inert by construction and measured. Coasts memo-hit 0 (9b03's reading:
   same-tick coast captures have bodies resolved in between).
5. **Disclosed:** arm D peaked at 2.36 GB RSS (VmHWM) against the 2 GB guidance and still
   completed; 126/1200 frames over budget at rtf 2000 without the pull cure (the known wall,
   not this run's target).

## Predictions

`predictions.md`, written before the decisive arms. **Held:** digest identity (1); the global
epoch dead, <5% (2 — 0%); build 35–65% of the loop on A/C (3); overpayment ≥20% of walk time on
C (4 — 37%). **Missed:** P2's "per-body form earns ~the memo rate" — v2/v3 measured the two
mechanisms above instead (the call site's own apply and history-preserving rebinds); the
prediction named the per-body refinement as sufficient, and it is not.

## What would make it wrong

The three dead certificates are measured on `plane_extra` scenes (coast/burn, 3e3–1e5, rtf
100–2000); a scene whose same-tick captures are separated by truly quiet stretches (no resolves
at all — e.g. a settled universe between kick waves) would let even v1 fire, but that saving is
the ramp's, not the steady law's. The attribution's per-call lookup numbers carry the 36.2 ns
bias (subtracted where quoted); loop/build/radial totals are single-timed and bias-light.

## Cost of adopting, and fit

Nothing to adopt as code: the pre-check is refuted, and the instrument (`scanpre` + the
`stat` module, print-only and env-gated, off = shipped paths) is the deliverable. The design
consequence is negative and cheap: stop looking for the pre-walk certificate; the news-fed
window (membership at events) is the one lever, and its target is now priced — the whole walk
per arm above, with 37–60% of it currently pure repeat. PRINCIPLES: "Compute only surprises…
Nothing is evolved that can be derived when looked at" (3) — the walk re-derives what the store's
own history mechanism already preserves; and via negativa: the certificate hunt itself was the
thing to delete.

## The lens (SpaceX)

Delete-and-rebuild is cheap for a rocket; here the "2-line pre-check" hid a representation fact
— the scan's reuse domain is the store's history semantics, not its mutation log. The idiot
index still points where the lens expected (the walk at 1.15 ms a capture at the wall), but the
part to delete is the walk's *inputs* (the candidate set as a maintained record), not its
*guard*.

## Runs

- 20261021-1443-system-9b03 (the page this executes against: news_frac 1.2–11.4%, memo 47%, od 1 + od 3).
