# Dossier — the storage layer's commit path: H_live measured, floor 60 bits/kick, write 88× over it

## Claim

In the plane as shipped, one committed kick carries ~60 bits of live distinguishing information
(the law's "+62 bits per kick" model is honest to 3%), but the store writes 660 B per kick
(88× that floor), and at a billion bodies the floor itself says one kick per body is the whole
8 GB budget — so distinctions per game-second, not body count, decide scale, now with numbers.

## Bottleneck

Board focus "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" and risk
"H_live: not measured yet". Storage component under the first-principles lens: requirement
(P6 "Store the generator, not the generated"; P24 "The memory floor is information"), floor,
distance, design within 10×.

## What was measured

The commit path (`Universe::apply`) of the plane (`xtask universe`), scripted player, 400 fleet
members, 100k–400k game-seconds per run. A 40-line read-only recorder (`Hlive`, `None` on every
digest path) counts events, written bytes and the kicks' exact `dv` pairs; entropy is measured
off-line. **Controls:** kick-bench digests bit-identical pristine vs patched; `--h-live` repeats
bit-identical; the entropy tool gives 0 on a constant stream and loses no order-1 structure on a
shuffled iid stream.

- **Events:** 1.89 per game-second: kicks 50.9%, boundaries 46.5%, opens 2.4%, handoffs 0.05%.
- **The floor of one kick.** The `dv` pair is a near-unique integer pair (98.7% of pairs distinct
  in-run), so frequency entropy saturates at log₂n and measures nothing. For a law that must
  replay bit-identically (B8) the floor is the description length: E[bitlen dv₀]+E[bitlen dv₁] =
  27.4+26.5 bits plus 6.2 bits of (sign, bit-length) shape = **60.1 bits/kick**; zlib on a varint
  stream achieves 64.3. Stable: 60.1 (seed 1), 57.2 (seed 7), 59.0 (rtf 100, seed 1) — ±5%,
  pace- and seed-independent as predicted (P5 held).
- **The write.** Per kick: one 192 B `Segment` retired + a 473 B `BodyRec`-with-plan rewrite =
  **659 B, an idiot index of 88×** (82× vs zlib). Boundaries (46% of events, no scars) still
  rewrite 481 B each — schedule state that is a pure function of the binding.
- **Live memory.** 7,277 B/body (428 bodies) against the law's 16 B tube: light-cone history
  (192 B × ~30 kicks retained), the 448 B `BodyRec`, and the compiled-shape share. History **is**
  pruned at twice the light distance every 64 frames — the retention design is sound; the write
  path is what is 88× off.

## Design within 10× of the floor

The scar as an append-only varint log of `dv` (measured 8.36 B/kick raw = 1.12× the exact floor):
bindings, plans and history-segments re-derived on read (the resolver already rebinds from exact
state; the plan is a pure function of the binding). At the goal's scale: 0.3 kicks/orbit (H0190)
× 60 bits ≈ 2.3 B/orbit/body of true distinctions; a 16 B tube is ~7 orbits of scars; 8 GB over
10⁹ bodies is 8 B/body — **the exact distinctions of a single kick per body**. Programs
(components-98bc, 0.126 bits/body) must cover the quiescent tail and scars must reabsorb or log;
this quantifies the board's "H_live decides" and calibrates B18's budget.

## Predictions (predictions.md, written before the decisive runs)

- P1 (≤ 24 bits/kick) **refuted** — the right reason: exactness, not frequency, sets the floor;
  sub-quantum sigma-delta carries make each kick's `dv` a full-width integer (~54 mantissa bits).
- P2 (≥ 120 B/kick written, ≥ 40× floor) **held** (659 B, 88×).
- P3 (history never pruned) **refuted** — the plane prunes at 2× light distance; live memory is
  bounded. Good: the shipped design was better than I predicted.
- P4 (kicks+boundaries ≥ 85%, kicks < 60%) **held** (97.4%, 50.9%).
- P5 (bits/kick stable ±25% across pace and seed) **held** (±5%).
- P6 (the law's 62 bits/kick ≥ 2× too big) **refuted** — the model matches the measured exact
  floor within 3%; the lab should keep it.

## What would make it wrong

The scene is one system, 400 members, a scripted player; belt-scale kicks (orbit-averaged,
secular) may differ in *rate* but the per-kick width is law arithmetic, not scene. Clock bodies
(motion law v2, 0.1% of kicks here) carry an `Ext` the recorder did not itemize. The floor
assumes no predictor of `dv`: a secular-average predictor would pay only the residual, but that
is a law change (the re-pay lesson, taste log 5 October), not a store change. Ship `Ext` bodies
were not separated in the byte counts.

## Cost of adoption, fit with PRINCIPLES

The recorder is already in `crates/universe` behind a `None` Option (zero digest impact, proven);
`b-h-live`'s dashboard build can read `Hlive` directly. The varint-scar store is a shipmem-layer
change, one step. P1 "the cheapest compute is compute not done"; P24 "the memory floor is
information-theoretic" — here the floor is *exact description length*, and the measurement
method (frequency entropy saturates; use description length) is itself a result for B18 and the
H_live definition: **H_live must be measured as description length, not frequency entropy.**

## The lens

First-principles, one component: it may have missed that the neighbour components (the compiled
shape share, the view's history reads) co-determine what a scar must hold; I measured the commit
path, not the read paths' constraints. And the neighbours were not re-measured after moving cost
to them (the lens's own blind spot) — a re-derived-history store shifts work to the view.

## Reproduce (each ≤ 60 s, Linux/x86, orders of magnitude only)

```
cargo build --release -p xtask
$CARGO_TARGET_DIR/release/xtask universe --h-live --seed 1 --rtf 1e4 --seconds 10 --members 400 --csv hlive-s1-rtf1e4.csv
$CARGO_TARGET_DIR/release/xtask universe --h-live --seed 7 --rtf 1e4 --seconds 10 --members 400 --csv hlive-s7-rtf1e4.csv
$CARGO_TARGET_DIR/release/xtask universe --h-live --seed 1 --rtf 1e5 --seconds 4 --members 400 --csv hlive-s1-rtf1e5.csv
gzip hlive-*.csv && zcat hlive-s1-rtf1e5.csv.gz | awk 'NR==1 || NR%2==0' | gzip > hlive-s1-rtf1e5.s2.csv.gz
python3 analyze.py   # reads the three .csv.gz and .json; prints table + analysis.json
# controls: kick-bench digests pristine vs patched; --h-live run twice
```

Files: `hlive-*.json` (run summaries), `hlive-*.csv.gz` (event streams, the 1e5 one stride-2),
`analyze.py`, `analysis.json`. The instrument patch is in `work/patch.diff`.
