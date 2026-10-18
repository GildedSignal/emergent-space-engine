# Run 20261018-0932-system-0d46 — lens: the whole system

## Claim

On the shipped plane the crowd is paid for three times over by one mechanism — the member-individual
read "body j's binding at t" — and the engine already mints the representation (the shared compiled
key + phase offset) that deletes all three prices at once: the view gather walks every member every
frame at **6.9 µs/body p50** (2.94 ms p50/frame, max 4.19 ms, at the CLI's own 400-member crowd of
428 bodies — the same per-body law b77d-1fcf measured at 10⁴), the scan re-reads **213 candidates
≈ 50% of all bodies per capture** (0.45 µs each at capture, 224 B pinned each), and the scan's
answer half (6.9 µs/candidate) is starved to `settle` — **12 answers in the whole 1,800-frame crowd
flight against 97 in the 32-body control** (the FLOW law). b083/5f36's phase-word tier, flown for the
scan only (4.4 µs → 19.2 ns), is the same lever for the gather's crowd term; no page has connected
them.

## Bottleneck

Board focus 1 (bodies in the flyable engine: 10⁶ → 10⁹). The crowd's linear-in-K per-member terms,
each patched on its own page (view's row-set deletion, promotion's phase window, memory-h-live's byte
fence), are one walk on one store. Unifying on the already-minted key: the gather's crowd term falls
~300× (6.9 µs → ~0.02 µs at b083's native compare) and the scan's capture pin (224 B × candidates)
rides the same word; what remains is O(visible) rows (~73–313, 62c1/649c) and the comb (its own page).

## Evidence (shipped code, print-only probe; regen: `regen.sh`, ~2.5 min)

`xtask universe --bench --seed 1 --rtf 100 --seconds 30 --members 400 --threads 1` (paced 60 Hz, the
bench's burn script, 1,800 frames, 30 probe windows; digest `4fb49739…`, canonical cut) vs the same
flight at `--members 4` (32 bodies). All aggregates over the full 30 windows (regen.sh's table):

- **Gather (the walk):** p50 2.94 ms/frame, max 4.19 ms = **25% of the 12-ms budget at 428 bodies →
  6.9 µs/body/frame**, against **16.6 µs/body at 32 bodies** (control; per-body falls as the fixed
  per-frame cost amortises — the walk never leaves). This anchors b77d-1fcf's 10⁴ law (66.8–74.1 ms
  ≈ 7 µs/member) on the shipped CLI's own crowd scene: **10⁶ crowd ⇒ ~6.9 s/frame on this term.**
- **Scan capture:** 157 captures over the flight (5.2/window), **213 candidates/capture ≈ 50% of all
  bodies**, 0.45 µs/candidate, each pinning a 224 B Binding (memory-h-live's law) ≈ 48 KB/scan.
- **Scan answer:** **12 answers in the whole crowd flight** (0.4/window; the drain is starved — the
  frame budget never leaves `2·max(scan_ns, 750 µs)`; 260 candidates per answered scan) against the
  control's 97 (3.2/window, 11 candidates each) at **6.1–6.9 µs/answered candidate** — the crowd's
  answers defer to `settle`, exactly the FLOW single-server-queue law (memory-h-live), now observed
  on the shipped crowd scene.

## Predictions (`predictions.md`, written before the run)

- **P1 held** (gather 0.5–10 ms/frame; per-body flat-or-falling: 6.9 vs 16.6 µs).
- **P2 held** (≥100 candidates/scan: 213).
- **P3 half-held:** the gather's walk is ~25,700 body-reads/window vs the scan's ~1,100 candidate
  reads — the duplication is real but one-sided at this load (the scan is held, not answered; its
  price is deferred memory and settle spikes, 260 candidates at once, not in-flight CPU). The "two
  equal walkers" reading was wrong: the gather owns the shipped crowd's frame; the scan owns its
  deferred memory.
- **P4 stands as cited** (efd4's flown census: 513 entries → 2 intern keys on a formation; the
  individual walks read member-individual copies of O(1)-distinct compiled content).

## What would make it wrong

The per-body gather cost is measured on one scene family (the fleet battle at the player's planet,
burn script, one seed) at the CLI's 400 clamp — not at 10⁴–10⁶ crowds (those need the patched
MEMBERS override; b77d's 7 µs agrees). If the gather's cost on a crowd were dominated by row math
rather than the per-emitter crossing/readout walk (51bf found the crossing loop 95% on the 28-body
plane), the phase word would delete less of it; that decomposition is the one measurement this run
does not make. Eccentric or kicked crowds break the shared key itself (efd4: the scattered belt
stands 2,044/2,036 distinct) — the lever is a keys-fleet/formation lever, not a belt lever.

## Cost of adopting, and fit

Cheapest next step (one probe, not a law change): extend b083/5f36's rigidring tier to the gather —
rows of a shared-key crowd derived from the stored phase word, bit-compared against the shipped
gather with 2df1's display-exactness audit (≤0.1–2% of drawn rows). Adoption proper touches
`view.rs`'s emitter loop and `encounter.rs`'s candidate build; digests are display-side (the view is
never evolved), so no gate re-freezes. PRINCIPLES 32 ("under the right representation many
symmetries can appear") and 3 ("compute only surprises" — a crowd on one orbit is not a surprise per
member); law.md's own letter: "The memo is keyed by (E, L) alone: a rotated orbit is the same cycle,
so orientation costs nothing" — the gather has no such key yet, and the engine already mints it.

## The lens (what it may have missed)

Elegant unifications hide a hard special case; mine is the **burn**: a kick scars a member off its
shared key (efd4's scattered belt), so a crowd under fire de-keys exactly when the player looks. The
phase-word tier must degrade to the individual read on members whose scar is live (the scar index
already exists), and the near-field draw (O(visible)) is untouched by it. I also did not measure the
gather's internal decomposition on this scene (crossing vs row math); if row math dominates, the
unification's gather half weakens to the scan half.
