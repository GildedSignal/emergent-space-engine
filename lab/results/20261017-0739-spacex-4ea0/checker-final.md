Working...
Check complete. **Grade: gold** — written to `lab/results/20261017-0739-spacex-4ea0/check.md`.

**What I did:**

1. **Reproduced** — `regen.sh` (runner, exit 0): all four digests bit-identical patched↔pristine; every derived ratio re-derives (98.1 reads/build, 224.5 reads/gen, 77.4/69.7/68.1 reads per rebind-gen, observe 65.9% / secondaries 19.2% / step 12.0% / view 1.0%, never-read 0, kick-bench 30.1).
2. **Source-verified the structural kill** — `bind_in` at `crates/universe/src/bind.rs:276` decodes the freshly minted Entry at the binding event to build turn/residual, in pristine main. The mint-is-first-reader claim is the representation's own machinery, independent of the instrument.
3. **Four adversarial arms, three outside the author's range** — 8 members (36 bodies: view still only 1.5%, mint-first-reader 393/393), seed 42, 50 s flight (96.5 reads/rebind-gen), and `--members 2000` (clamps to the 400 scene — a bench cap the author missed). Digest controls on my arms: patched = pristine, bit-identical. Also attacked never-read-0 (discounting the birth-read still leaves ~67–77 later reads per generation).
4. **Novelty** — answers the kick-jet page's own open direction 2; refutes 0e37's "view is the reader" and b9ae's "read ~once per binding" readings; b8fc's earlier 48–60 readouts/compile had no attribution and no decision.
5. **Page** — faithful; I corrected one overstatement in place ("every generation" → "every rebind generation" in the lead).

**Gold because:** reproduced, pre-registered kill branch fired, shows a premise is wrong on the board's #3 bottleneck, adoptable at zero cost (a kill redirecting to the Carlson wiring). Precedent: `components-4643` gold for the same shape.

**Noted misses:** the bench's ~419-body ceiling (belt loop never censused), headline integers jitter ~0.1% and match neither the author's saved work file nor regen exactly (digests fixed; ratios reproduce), "98–224 reads per build" mixes per-build and per-generation granularities, "other" (1.4%) unexamined, eviction ruin priced at the orbit mean is a floor.

Tree restored to pristine at base d742a1b0; nothing else in the run folder touched; no commits.
