#!/usr/bin/env python3
"""Build the resolved representation-premises page.

Base: 16c3's checker-verified 75-line compile (from its published branch — the
'ours' side of the standing conflict). Folded in: 901c's kink-law result (the
'theirs' side), the 16c3 checker's assigned citation fix (drop a4ed), and this
run's own line. Output: the page, printed to stdout.

The editorial rule (wiki README): a conflict is resolved by the next run on
the topic; numbers and qualifiers are copied, not paraphrased.
"""
import re, subprocess, sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
SRC = ("origin/claude/lab-20261021-0213-q-compile-representation-premises-16c3:"
       "lab/results/20261021-0213-q-compile-representation-premises-16c3/wiki/representation-premises.md")
ME = "20261021-0312-second-20261021-0213-q-compile-representation-premises-16c3-1fc6"

text = subprocess.run(["git", "show", SRC], cwd=REPO,
                      capture_output=True, text=True, check=True).stdout

# --- header
text = text.replace("updated: 20261021-0213-q-compile-representation-premises-16c3",
                    f"updated: {ME}", 1)

# --- headline gains the kink clause
text = text.replace(
    "its kick and memo cost claims are dead; its motion premises survive.**",
    "its kick and memo cost claims are dead; its kink work-rule clause is dead "
    "(901c, gold: the shipped burn is exact and implements the FW nose, not the "
    "letter); its motion premises survive.**", 1)

# --- two Current-best bullets for the kink law (after the standing-kills bullet)
KILL = ('- **The kink law\'s work-rule clause is dead (901c, gold):** L50 "in a field, E and L '
        'change by the work done" under-reads a prograde burn\'s ΔE/ΔL at 0.51/0.43 (r=6M, η=0.05/0.25), '
        '0.85/0.76 (20M), 0.97/0.95 (10⁴M) and 0.62/0.52 in flat space (the SR kinetic channel, ~1/γ³, '
        'any r), deepening toward the hole (letter ratio 0.19–0.24 at 4M, 0.09–0.12 at 3.5M; sign flips: '
        '−0.17 on an E = 1 radial-infall event at 6M, ΔL at −0.33 on an eccentric-event radial burn); it '
        'over-calls the burn-to-escape 3.04× at 6M, 1.61× (10M), 1.22× (20M), 1.04× (100M); the exact '
        'replacement is one multiply-add in the frame the boost already lives in: ΔE = √f·Δγ, ΔL = r·Δp_φ.')
SHIPPED = ('- **The shipped `burn` is exact and implements something else (901c, gold):** its algebra '
           'matches the exact invariants to 0.0–1.3e-13 (float replica; controls green: geodesic drift 0.0, '
           'flat lump composition 1.3e-15 at any cadence, ≤ 3e-15 at every checker2 out-of-range case); its '
           '`along = n + u(u·n)/(γ+1)` satisfies |along|²−s² = 1 ⇒ felt α exactly at any attitude, so the '
           'rapidity clause is exact in the engine\'s FW-nose convention (speed-rapidity linear only '
           'prograde; at oblique attitude a finite lump is not the flow of its own field — flat 45°, '
           'η = 0.25: |Δu| 1.7e-3, first order in the flush quantum) while `thrust.rs` L7\'s comment '
           'repeats the dead sentence; cosh_sinh is a 6th-order truncation whose error is 0.0 at the '
           'engine\'s per-flush η ≤ 2⁻⁶ and ~4e-10 (3.7e-10) at η = 0.25; flush deferral is '
           'first order in the flush quantum (relerr_E −0.184% at q=2⁻⁶ → −0.047% at 2⁻⁸ at 6M, '
           '−0.0016%→−0.0004% at 20M, exact in flat prograde); no rung has any thrust arm (r1–r13).')
text = re.sub(r"(- \*\*Standing kills on cost premises:\*\*.*\n)",
              r"\1" + KILL + "\n" + SHIPPED + "\n", text, count=1)

# --- checker 16c3's assigned fix: a4ed's cost claim is dead (kick-cadence a765); 3294 carries the rate half
text = text.replace("(fire rate 1.000, one rebind per doll interval — a4ed/3294)",
                    "(fire rate 1.000, one rebind per doll interval — 3294)", 1)

# --- Refuted gains the work-rule entry (newest first)
REF = ('- **"In a field, E and L change by the work done" (901c, gold; representation.md L50 — the same '
       'sentence at law.md:42, plane.md:21, and repeated by thrust.rs L7\'s comment; the checker found the '
       'extra copies):** dead as written at two stacked channels — the SR kinetic one (Newtonian ½v² '
       'under-reads dγ longitudinally: 38–48% at w 0.5–0.577 flat, 94% at γ 2.3, any r; 0.059 flat at '
       'γ 2.3 and 0.0019 at γ 7) and the GR one (√f, and the γ in L = r·p_φ) — worst 0.43 of the true ΔE '
       'at r = 6M, η = 0.25, deepening to 0.09–0.24 at r = 3.5–4M (0.09 at 3.5M, toward the photon '
       'sphere); the letter flips ΔE\'s sign on an E = 1 radial-infall event at 6M (ratio −0.17) and reads '
       'ΔL at −0.33 on an eccentric-event radial burn, and over-calls the escape burn 3.04× at 6M; the '
       'sentence also under-determines direction (at a radial impulse, 6M, η = 0.25: ΔL = 0 axis-boost vs '
       '+3.14% of L₀ shipped/FW; the two clause-1-consistent continuous readings, FW-nose vs gimbal-held '
       'compass, differ 13% of ΔE at the radial case and 10–15% oblique). The shipped code does not '
       'implement it (exact to 1.3e-13; checker2, blind: every dossier number regenerates in 0.7 s). Cure: the exact closed form ΔE = √f·Δγ, ΔL = r·Δp_φ, plus naming '
       'the nose convention (FW-carried, the shipped choice). No rung has any thrust arm.')
text = text.replace("## Refuted\n\n", "## Refuted\n\n" + REF + "\n", 1)

# --- Open directions: the burn rung becomes OD1, the standing eight renumber
OD1 = ('1. **Commit a burn rung — none exists (901c, gold; off-board: guards, the integrator alone).** '
       'r16-burn: the engine\'s burn against an exact powered-geodesic oracle at one event and over a '
       'held-heading burn, oracle side converged (q→0; the shipped-quantum lump sits 1.8e-4 from its own '
       'limit at the radial case); the letter\'s work rule as the negative (its flat-space 0.52 ratio at '
       'w 0.5, 0.06 at γ 2.3, is the cleanest bar); the axis-boost vs FW-nose arm (ΔL = 0 vs +3.14% of '
       'L₀ at a radial impulse, 6M, η = 0.25) and the FW vs compass arm (13% of ΔE at the radial case, '
       '10–15% oblique); the deferral scaling arm (first order in q: 0.184%→0.047%). Amend the dead '
       'sentence in all four copies (representation.md L50, law.md:42, plane.md:21, thrust.rs L7) to the '
       'closed form ΔE = √f·Δγ, ΔL = r·Δp_φ + the nose convention, and fix thrust.rs\'s comment to the FW '
       'map — one pass with the letter amendments of OD2.')
def bump(m):
    return f"{int(m.group(1)) + 1}. "
text = re.sub(r"^(\d+)\. ", bump, text, flags=re.M)
text = re.sub(r"(^Ranked by the board row each moves.*\n\n)", lambda m: m.group(1) + OD1 + "\n", text, count=1, flags=re.M)

# --- Contradictions gains 901c's closing clause
text = text.replace("and no prior run claimed a centre direction.",
                    "and no prior run claimed a centre direction. 901c's letter kill does not contradict "
                    "the engine's exactness — the code never implemented the sentence; the finding is a "
                    "doc/code divergence plus a rung gap.", 1)

# --- Runs: 901c (branch-true grade: gold) + this run
RUNS_ADD = (
    '- 20261021-0213-redteam-901c (gold): the kink law measured against GR — the letter\'s work-rule '
    'clause dead (0.43× at 6M, escape over-called 3×, flat-space 0.52× channel), the shipped thrust.rs '
    'exact (FW nose, felt-α identity) and not implementing its own comment, no rung has any thrust arm.\n'
    f'- {ME} (this run): the checker\'s named step done — fold_runs landed on wiki.py (id-keyed: 6ccc\'s '
    'raw-token key split colon variants, 23 lines for 18 runs), the 16c3/901c publish collision reproduced '
    'byte-for-byte from shipped code and resolved, then published through a real wiki.py apply; index row '
    '64 → 19 true runs, no flags.')
text = text.rstrip("\n") + "\n" + RUNS_ADD + "\n"

sys.stdout.write(text)
