Working...
Check complete. **`Grade: silver`** — written to `lab/results/20261021-1551-spacex-eb24/check.md`, with the author's wiki page trimmed into budget (Current best 23→15 lines, 61 total) in place.

**Reproduction (all bit- or count-exact):** digests identical on A/B/C across off/v1/v2/v3 (`c1e220b4…` on C); eligible 861, miss_me 861/861, miss_near 721–723 / miss_reg 138–140; memo 855 (37.7%); overpayment 37%→60% of walk time rtf100→rtf2000; regen.log agrees with the dossier on every count-level number (timings shift with shared-machine load, orderings don't).

**Controls I added:** pristine-source (fully unpatched lib) digests identical — "off = shipped" verified at behavior level; A/B pre-form digest identity filled; code-verified both kill mechanisms (`apply`→`put` at universe.rs:661 precedes `encounters_for_player` at 772; `binding_at` reads through retired history, body.rs:152–161).

**Adversarial:** 3e5 coast (3× largest tested — fences hold, radial 73%, walk N-independent); 3e3 burn (untested corner — fences too, so the fallback is flight-dependent, not belt-N alone; kill attribution identical → 0 hits); B coast v2: miss_me 188/188, 0 hits — the kill extends to the coast arm the author never attributed.

**Why not gold:** the physics is decisive and the premise (scan-news od 3) is genuinely dead — but the predictions scoring overstates: P3 ("radial ≤ 15% everywhere") failed on B (73%) and C (52/48) and is scored held by silently narrowing it; P5 ("D's per-capture costs match C") failed ~100× and is omitted entirely. Same pattern that cost the 1 Oct red-team and r3 v3 their gold. The one step to gold is the record amendment, not an experiment. Also found: v1 is dead by construction (no quiet scene can fire it — refutation stronger than the dossier claims), the epoch bookkeeping is always-on cost despite "off = shipped paths" wording, and regen.sh's D arm runs with `PRE=3` leaked from the for-loop.
