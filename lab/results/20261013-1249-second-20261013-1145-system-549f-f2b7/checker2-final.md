Working...
Check complete. **Grade: gold** — written to `check2.md`, with the author's wiki page corrected in place and the tree restored to its runner state.

**What I reproduced independently (clean tree, patch applied by me):**
- **Gates, v2:** the same three frozen-readout failures with exact figures — boundary velocity jump 3.85e-2 (bound 1e-4), radius 3.05e-6 (bound 5e-7), map-ratio 356.07× (bound 3×); clock gates green.
- **Gates, v1** (kick write only — a dossier number regen.sh never covers): 5.07e-2, same three failures.
- **Digest identity, both sides built by me:** plane flights and — a control the author omitted — both strong-field scenes (57d16273…, 6bb30c1b…, identical event counts) bit-identical pristine vs wired; instrument control reads exactly 0.000.
- **Bench:** a fourth interleaved round gives 1.49×/1.45×, inside the author's ranges.
- Staleness arithmetic (err 40.7% of term, 2.7e4× the census figure) and multiplicity 480 check out.

**Two contributions of my own:**
1. **Stronger than the dossier:** v1 and v2 give a bit-identical 356.07× map-ratio while the boundary jump differs — the continuity break is structural to *any* window-constant word, which closes the fresher-write escape route the dossier left open.
2. **Corrective adversarial finding:** I instrumented the strong-field probe — `k.clock` is false at *every* frame, at r = 4000 M as much as r = 20 M. The 0 gated reads never consult the read gate; there are no clock steps to "collapse". The strong-field half's mechanism (dossier and wiki) was wrong; its measurements stand, but the strong-field readout question is untested. I fixed the page's Current best, Refuted, Contradictions and Runs lines accordingly.

Gold because: the integrator-named experiment, run to its answer, reproduced bit for bit, pre-registered kill clause fired and was led with — a premise kill on frozen gates that redirects the shared view/gravity-news/frame-cost slot, adoptable in one step (strike 549f's open direction 1; nothing to merge). PRINCIPLES 9 and 2 both honored.
