topic: budget-1e9
status: open
closed-by:
valid-while:
updated: 20261021-0312-fermi-614b

# The assembled 10⁹ ledger: the board's interlocking budget, composed on measured laws

## Current best

1. **The composed CPU budget at 10⁹, λ = 4×10⁻⁵/body/game-s [0659], rtf 100 = 4×10⁶ events/wall-s [3aec]: the stream row alone is 193 cores at shipped item cost (39.3 after split8×survival = 4.92×; checker 21.3 at the belt's own item); today-cost totals 22.5–43.4 cores = 5.6–10.9× the 4-core budget, cd3b-letter cost 6.5–12.5 (1.6–3.1×), arithmetic-floor closure 6.1–9.0 (1.5–2.3×). Rows: churn 0.35–1.4 [08d0 → 73b5], mint ≤ 1.9 [cd3b], view serve ≤ ~0.1 [e3a4], frame ≤ 0.72; the belt's boundary items are unpriced.**
2. **Closure requires both owned levers [3aec]: the cadence cut is mandatory (24 cores at the 6 µs floor on the shipped cadence) and with it the cost bar is ≤ 4.9 µs/event, so the Carlson adoption is equally mandatory. Floor ladder at the same rate: write floor (50 ns) 0.20 cores; cd6e's composed kick (8–19 µs) split8 6.5–15.4; 262f's native 4 µs split8 3.3 ✓.**
3. **Kick item costs, measured [3aec]: fired kick item stage 82.5 µs x86, N-flat to 4×10⁵ (checker 83.4–86.5); the belt's own clock item 44.7 µs x86 ≈ 26 µs M1; the player's WH item 40 µs dense; boundary 18.4 µs x86 ≈ 10.8 µs M1 (fast path unwired), apply 7.6, root walk 7.0; frames idle-cheap (p50 0.046 ms), the stream hides in event frames (p99 5.3 ms).**
4. **The belt's own stream: Γ = 6.21 per root of reach per game-s (band 5.4–7.0), flat across d = 10⁴–10⁵ root [f876]; λ is the belt's own steady rate (1.30× cross-checked [f80a via d4ff]); encounters change no orbit.**
5. **At the priced reaches [f876]: TP bar ≈ 422 pair-events/game-s at 100 km; contacts 0.41/game-s → ≤ +0.03% of every composed total; contacts wake at N ≈ 2.6–3×10⁷; a fleet's contact stream equals its own clock stream at C ≈ 4.3–5×10⁴. Bound: no mutual ship gravity is wired [d4ff].**
6. **Machine floors, both closed [f623]: at 10⁹, rtf 100 — allocator 0.6–1.7 cores, byte traffic 13.6–28.5 GB/s marginal = 23–48% of 60 GB/s (after split8 3–6%); no pooling subsystem is machine-mandated; malloc floor 11.6 ns/alloc+touch+free.**
7. **Naive per-kick churn law [f623; checker-reproduced]: 17.6–19.3 allocs + 12.3–12.7 KB per fired kick; heap-call family {88, 240, 304, 352, 384², 704, 832} B; net live 0.55–1.6 KB/kick (the ratchet).**
8. **Scope split [8994]: the fired item's own scope carries 91% of naive coast bytes; the frame base 2.0–2.2 KB/game-s coast is NOT N-flat; only the ship marginal extrapolates to 10⁹. Player item scratch 193–199 KB/item, K-flat, realloc 79–92% [8994, 5f76, 6e76]; at 10⁹ a negligible constant rate.**
9. **Residency [0659]: promotion fraction 1.0 measured; τ = 43.6 game-s at 8 GB; the kick must be absorbable by the compact row, not skippable.**
10. **The past-cap chains, named with stacks and an exact law [614b; checker-corrected]: the belt-scaled chain is the per-universe tables' capacity doubling at a handout — `resolve_handout`'s `pos.push([0.0;2])` (universe.rs:896; 16-B entries doubling from cap = N_bodies, i.e. 32.0 B × bodies per crossing, exact at N = 10⁴–6×10⁵ and seeds 1–3, one chain per crossing, burn-INDEPENDENT, crossing frame 2.1–2.3 ms vs 60–70 µs; the author's `info.push`/BodyInfo-32-B reading is wrong: info is parallel-full so its crossing would realloc 2×size_of::<BodyInfo>()×N, absent from every dump) and `PlainBodies::push` (recs, 464-B entries: 928 B × len at a crossing). Both-in at len N: 960 B/body realloc ≈ 1.44 TB traffic ≈ 24 s of bus at 10⁹ (pos alone 48 GB ≈ 0.8 s; the author's 496 B/992 GB/16.5 s counted one doubling — order right, constant 1.5× low); on the ladder ~24 ms at 10⁶, 240 ms at 10⁷, 2.4 s at 10⁸ — births must leave per-universe Vecs before ~10⁷. The capture chain (224-B tuples `(usize, Binding, Scalar)`; 57,344 = 224×256) is fleet-scaled (max 134/267 at every belt N, m48, belt-flat; 329→629 at members 400, where the belt doubles it): never a 10⁹ row at the shipped genesis. The radial index served every belt capture (fallback 0); the 94–96% die-off is the full-scan path (~11k iters/gs at fleet+belt scale).**
11. **Memory [097e]: build 2,348–2,464 B/body = 2.35 TB (294× the machine) on the shipped build, 0.2–2.0× on the wired compact store; wired terms: 1.7–2.4 B/body self-stirred ✓, 15.8 GB driven-worst = 2.0×. Domain: one Linux box, x86→M1 anchors page-cited, orders of magnitude only; coast arms unless the burn is named.**
12. **The radial with_capacity(hit + unbounded.len()) fix is flown and checker-reproduced [6e76]: −7.1% player bytes, −11.5% reallocs, kicks bit-identical; family A's allocator fix is refuted (over-allocates 23×) — its fix is od 4's read set.**
13. **Ship stream marginal [5f76 + checker]: per fired kick it RISES with K — 1.45–1.53 (10⁴) → 2.18 (3×10⁴) → 2.99 (10⁵) → 3.88 KB/kick (3×10⁵; no saturation measured) — cite the range, never the point; the 10⁹ byte row re-bases to 10–42% of 60 GB/s, still closing.**

## Refuted

- **"The burn chains are doll-scaled ~244–366 B per pulled body, 0.25–0.37 TB a chain at 10⁹" (8994/6e76's rung reading; carried by lines 9–12 of the old page): refuted in mechanism and trigger by 614b** — the belt-scaled chain is the per-universe tables' capacity doubling at a handout (`resolve_handout` → `pos.push`, 32 B/body exact; recs 928 B/len at its own crossing), it fires on coast exactly as on burn, and at 10⁹ it is ~1.4 TB of traffic when both tables cross (0.8 s pos alone; the author's 16.5 s both-in constant is 1.5× low, order right). The order stood; the site, the trigger and the fix (chunked tables / compact-store births, mandatory before ~10⁷) are new.
- Prior refutations stand: family-B doubling [6e76]; the OLS marginal [8994]; the naive-vs-marginal gap [8994]; the one-ladder scratch [5f76]; the ~1.6 KB/kick constant [5f76]; the mint heap anatomy [f623]; the inert belt [d4ff]; the unpriced conjunction rate [f876]; d4ff's anchor table [f876]; cd3b's closure bar [3aec]; the 363-core epoch arm [73b5]; a small promotion fraction [0659].

## Open directions

1. **The cadence cut + the ≤ 4.9 µs/event kick** (kicks row, ~10³): in flight (Opus `wt/cadence`, GPT `kickcost`).
2. **Wire the compact store, and with it own the births** (live set and memory, ~10²–10³): 614b prices the alternative — every wired birth beyond table headroom is a table crossing (960 B × N per crossing both-in, ~24 s of bus at 10⁹), so the compact store or chunked (dyadic) tables are mandatory before the ladder passes ~10⁷; the wired row must still absorb a ~1.5×10¹¹-quantum kick every 27.6k gs or promote [0659].
3. **Make the kick absorbable** (same row): p = 1.0 today [0659, 3aec].
4. **Family A's read set** (the full-scan path): the full scan has two gates into `0..bodies` — the window closure's error path in `capture` (a `?` before the radial call; dominant at m400 without a belt: 409 iters/gs vs 28 bodies × 933 fallbacks ≈ 30) and `Radial::candidates`' None (fallback 0 on every m48 belt arm; at m400 + belt 10⁴ the fallback carries ~98% of the weight: 906 fallbacks × 10,028 bodies ≈ the measured 11,029 iters/gs [checker]). Filter before the tuple build, or fix both gates.
5. **Fly a stirred belt with an in-loop conjunction counter; price the belt's boundary items** [f876, d4ff, 3aec].
6. **The concentration allowance row** (families): C ≈ 4.3×10⁴ contact tail, belt-temperature critical at C ≈ 42 [d4ff, f876].
7. **Measure the ship marginal's saturation** (1.45→3.88 KB/kick rising; band top 42–54% of bus) [5f76].

## Contradictions

- None open. Standing resolution (614b, checker-checked): 614b's "capture is belt-flat" holds at m48 (134 at every belt N to 6×10⁵) and 8994/6e76's "doll-scaled capture chains" read arms that scaled the fleet — capture tracks the fleet's handed-out population (329 at m400-n0 → 629 at m400-n1e4, where the belt doubles it); their 8–16k-entry contents need members ~10⁴ and were not re-flown.

## Runs
- 20261021-0312-fermi-614b (fermi, silver): the past-cap chains named — the belt-scaled chain is `pos.push`'s table doubling at handouts (32.0 B×N exact, burn-independent, ~1.4 TB ≈ 24 s of bus at 10⁹ both tables; checker: pos not info, 224-B tuples, seed 3 and N=6×10⁵ exact); capture is fleet-scaled; births must leave per-universe Vecs before ~10⁷.
- 20261019-0141-fermi-097e (fermi): the 10⁹ ledger composed — CPU, memory 294× shipped / 0.2–2.0× wired, build/floor 978×; superseded by 3aec's re-composition.
- 20261019-0435-fermi-0659 (fermi): promotion fraction 1.0 measured; τ = 43.6 game-s; the kick must be absorbed, not skipped.
- 20261019-1551-fermi-73b5 (fermi, gold): churn row 0.35–1.4 cores at E* = 1024–256, leak-certified; the 363-core epoch arm dead.
- 20261019-1656-components-3aec (components, silver): post-73b5 re-composition — the stream dominates and is rate-bound; closure = cadence cut AND ≤ 4.9 µs/event.
- 20261019-1817-fermi-d4ff (fermi, silver): the belt's own stream bounded; contacts ≤ +0.006 cores at 10⁹; "inert belt" refuted, λ stands.
- 20261019-1906-second-20261019-1817-fermi-d4ff-f876 (second, on d4ff): Γ = 6.21/root/game-s flat; TP bar 422/game-s; θ-mixing and anchor artifacts named.
- 20261019-2339-fermi-f623 (fermi, silver): allocator and byte floors both close; per-kick churn law; OLS split later refuted by 8994.
- 20261020-1002-fermi-8994 (fermi, silver): the allocation wave is marginal (item-scope 91%); player item scratch 194 KB/item; burn-chain rungs (mechanism corrected by 614b).
- 20261020-1621-fermi-5f76 (fermi): the player constant is law-grade (three seeds, three decades of K); two array-builds per item; ship marginal rises with K.
- 20261020-2102-fermi-6e76 (fermi): ladders named (capture tuples, radial ids); radial with_capacity exact (−7.1%); family A over-allocates 23×; burn site open (named by 614b).
