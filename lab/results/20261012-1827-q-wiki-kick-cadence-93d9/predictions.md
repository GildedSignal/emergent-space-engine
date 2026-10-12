# predictions.md — 20261012-1827-q-wiki-kick-cadence-93d9 (compiler run)

The decisive act of this run is the page `wiki/kick-cadence.md`, not an
experiment. What is held out is its **faithfulness**: the checker samples five
claims against their dossiers. My predictions, written before the page is
finalised, about checks I have not tuned on:

1. **Every graded run line matches its branch.** For all 24 runs I list as
   graded, `origin/claude/lab-<id>:lab/results/<id>/check.md` exists and its
   `Grade:` line equals the grade in my `## Runs` list.
   `20261007-0128-b-b17-parallel-cee8` has **no branch at all** (already
   probed once); it is listed as missing and cites nothing.
2. **Every number I quote appears verbatim in its source.** Spot targets:
   213× / 29 µs / N_max 1.4e10 (a4ed); 29/30 rows, 1.14×/1.24× (67be);
   1,548× (54d9); +0.5% at K=32, Δė 84–134 MADs (2eb1); 60/64 at N=7,
   ×2 per step (c01c); N_lib 4–10 (5030); rho ~ 0.5·n^-2.1 (ad35);
   N* = 4/8/16 at f = 0.2/0.3/0.45 R_H (7d0d); floor 8/orbit (06a8);
   1.4–30× over-spend (0713); 1.92× (51bf); 1.65× (a2ec); 2.8–6.7× and
   14–18× w (2d94); 2.303e-2/orbit (cd52); 33/132/704 (213e); 2/orbit vs
   128 (1db4); 5×/8× split (7f97); vr-flip 71.7–75.2% (0102).
3. **Routing holds.** The three runs I route away (b727, 887d → kick-jet;
   0ae6 → belt) make no cadence-*rule* claim in their dossiers: their claims
   are per-kick cost (kernel ≤3%, decode deletion −20%) and belt-carried
   bits/body, all of which kick-jet's and belt's pages already own.
4. **No page claim cites only a lead.** Every sentence in `## Current best`
   cites at least one gold or silver run; leads appear only as refuted
   claims' evidence of non-support or in `## Runs`.
5. **The page contradicts no check.md grade.** In particular scout-9abe's
   surviving 2.5–4/orbit off-resonance result is presented as superseded by
   67be (its resonance contrast was an artifact), and cd52's mechanism claim
   as split by f2e3 — both exactly as the checkers wrote them.

If (3) fails for any run, that run returns to this page's `## Runs`.
