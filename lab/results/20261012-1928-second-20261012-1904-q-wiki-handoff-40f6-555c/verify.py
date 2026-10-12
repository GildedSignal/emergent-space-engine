#!/usr/bin/env python3
"""Verify every number/claim quoted in wiki/handoff.md against its source branch.

Each row: (label, ref, path_in_ref, needle). Refs are origin/claude/lab-<id> branches
or origin/main. Run from the repo root (regen.sh does). Zero network, zero build:
the wiki page is a compile, so its regenerable ground truth is the run record."""
import subprocess, sys, unicodedata

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("−", "-"), ("–", "-"), ("—", "-"), ("≈", "~"), ("×", "x"),
                 ("µs", "us"), ("\u00a0", " "), ("·", "*"), ("′", "'"),
                 ("∥", "||")):
        s = s.replace(a, b)
    return " ".join(s.split())

_cache = {}
def fetch(ref: str, path: str) -> str:
    key = (ref, path)
    if key not in _cache:
        r = subprocess.run(["git", "-C", REPO, "show", f"{ref}:{path}"],
                           capture_output=True)
        _cache[key] = r.stdout.decode("utf-8", "replace")
    return _cache[key]

def R(run_id):  # full checker-run ref
    return f"origin/claude/lab-{run_id}"
ROWS = [
    # --- fa4b: Kerr compiler, B19 (gold + gold) ---
    ("fa4b B19 cycles", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md", "advance worst 2.0e-13"),
    ("fa4b fates", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md", "fates 1680/1680"),
    ("fa4b dragging", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md", "frame dragging 379/379"),
    ("fa4b penrose", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md", "Penrose 85+73+27"),
    ("fa4b light", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md", "light worst 4.4e-13"),
    ("fa4b chi0 digest", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md", "59d54de0f9ead66f"),
    ("fa4b scalar ints", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/dossier.md", "bound/unbound/plunging/photons"),
    # --- 6586: second check adjudicates gold; edges; guard ---
    ("6586 gold adjudication", R("20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586"), "lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/check.md", "run.sh:99"),
    ("6586 isco edge", R("20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586"), "lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/check.md", "isco(1,pro)"),
    ("6586 double root", R("20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586"), "lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/check.md", "true double root"),
    ("6586 19-line guard", R("20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586"), "lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/check.md", "19-line guard"),
    ("6586 negative-a slide", R("20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586"), "lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/check.md", "7.5546/4.2330"),
    ("6586 whirl cap", R("20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586"), "lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/check.md", "1.1e-2"),
    # --- ae29: root-clock keys ---
    ("ae29 shear form", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/dossier.md", "sinh"),
    ("ae29 spread", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/dossier.md", "8,314..+6,002"),
    ("ae29 worst miss", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/dossier.md", "worst miss 0.500 of a tick"),
    ("ae29 identity control", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/dossier.md", "110.5"),
    ("ae29 tie 16384", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/dossier.md", "16,384"),
    ("ae29 moon -25", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/dossier.md", "25 ticks"),
    ("ae29 threads", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/dossier.md", "1, 4 and 8 threads"),
    ("ae29 cost lines", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/check.md", "~150 lines"),
    ("ae29 B13 identical", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/check.md", "B13's detail line identical"),
    # --- 4e9c: key_fault second check ---
    ("4e9c 52/200", R("20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c"), "lab/results/20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c/check.md", "52/200"),
    ("4e9c key_fault", R("20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c"), "lab/results/20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c/check.md", "key_fault"),
    ("4e9c patch 0 bytes", R("20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c"), "lab/results/20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c/check.md", "0 bytes"),
    ("4e9c rebuilt numbers", R("20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c"), "lab/results/20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c/check.md", "148/52"),
    ("4e9c events", R("20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c"), "lab/results/20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c/check.md", "943/928"),
    # --- 18d2: single-surface handoff ---
    ("18d2 predicate", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/dossier.md", "R_H/2"),
    ("18d2 simultaneity offset", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/dossier.md", "-w*x'||"),
    ("18d2 p5 4000", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/dossier.md", "4000 of 4000"),
    ("18d2 p5 0.9 deviant", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/dossier.md", "3999 of 4000"),
    ("18d2 deviant size", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/dossier.md", "6.3e"),
    ("18d2 moon never leaves", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/dossier.md", "handoffs 0"),
    ("18d2 checker 4000@0.9", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "4000/4000 at 0.9"),
    ("18d2 checker moon", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "0/52,237"),
    ("18d2 2.18 artifact", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "sorted = 0.998"),
    ("18d2 0.5-retro 20.0", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "20.0 with 21,403"),
    ("18d2 0.9-pro", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "4,455"),
    ("18d2 0.9-retro", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "104.5"),
    ("18d2 chatter", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "210 handoffs"),
    ("18d2 P4 2.18 author", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/dossier.md", "2.180"),
    # --- ecfd: 2PN premise + B11 ---
    ("ecfd +0.36%", R("20261008-0041-redteam-ecfd"), "lab/results/20261008-0041-redteam-ecfd/check.md", "+0.36% periastron"),
    ("ecfd oracle 34-718x", R("20261008-0041-redteam-ecfd"), "lab/results/20261008-0041-redteam-ecfd/check.md", "34-718x"),
    ("ecfd c2 gap", R("20261008-0041-redteam-ecfd"), "lab/results/20261008-0041-redteam-ecfd/dossier.md", "0.058"),
    ("ecfd apsidal drift", R("20261008-0041-redteam-ecfd"), "lab/results/20261008-0041-redteam-ecfd/dossier.md", "0.0044 rad/orbit"),
    ("ecfd tol/3.6", R("20261008-0041-redteam-ecfd"), "lab/results/20261008-0041-redteam-ecfd/dossier.md", "tol/3.6"),
    ("ecfd oracle family", R("20261008-0041-redteam-ecfd"), "lab/results/20261008-0041-redteam-ecfd/dossier.md", "5-170x"),
    # --- 6765: galaxy doll ---
    ("6765 16 panels", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/check.md", "16 panels"),
    ("6765 cycle err", R("2026111729-scout-6765-DUMMY"), "lab/results/20261011-1729-scout-6765/check.md", "4.1e-12"),
    ("6765 rekey", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/check.md", "2.4e7"),
    ("6765 transit", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/check.md", "5e-10"),
    ("6765 disc", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/check.md", "5.1e-3"),
    ("6765 SOI", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/dossier.md", "0.13 of r_SOI"),
    ("6765 unmeasured half", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/check.md", "asserted, not measured"),
    # --- aac1: star doll at galaxy scale ---
    ("aac1 690x", R("20261012-0036-scout-aac1"), "lab/results/20261012-0036-scout-aac1/check.md", "660-690x"),
    ("aac1 churn 13.9", R("20261012-0036-scout-aac1"), "lab/results/20261012-0036-scout-aac1/check.md", "13.9%"),
    ("aac1 churn 55.5", R("20261012-0036-scout-aac1"), "lab/results/20261012-0036-scout-aac1/check.md", "55.5%"),
    ("aac1 recall", R("20261012-0036-scout-aac1"), "lab/results/20261012-0036-scout-aac1/check.md", "13.2% @ fpr 14.4%"),
    ("aac1 readout err", R("20261012-0036-scout-aac1"), "lab/results/20261012-0036-scout-aac1/check.md", "10-3"),
    # --- 2da8: churn second check ---
    ("2da8 switch-on low", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "0.008"),
    ("2da8 switch-on high", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "0.025"),
    ("2da8 27-35%", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "27-35%"),
    ("2da8 dL 53", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "53%"),
    ("2da8 E wobble", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "58%"),
    ("2da8 1200 periods", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "1200 periods"),
    ("2da8 census errors", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "9.1%"),
    # --- 3851 + 0d8c: Floquet certificate ---
    ("3851 hill", R("20261009-2348-scout-3851"), "lab/results/20261009-2348-scout-3851/check.md", "Hill's equation"),
    ("3851 0/24", R("20261009-2348-scout-3851"), "lab/results/20261009-2348-scout-3851/check.md", "0/24"),
    ("3851 kick32", R("20261009-2348-scout-3851"), "lab/results/20261009-2348-scout-3851/check.md", "0.646/orbit"),
    ("3851 e0.9", R("20261009-2348-scout-3851"), "lab/results/20261009-2348-scout-3851/check.md", "12.8/orbit"),
    ("3851 hold32", R("20261009-2348-scout-3851"), "lab/results/20261009-2348-scout-3851/check.md", "55/58"),
    ("0d8c 144/144", R("20261010-0100-second-20261009-2348-scout-3851-0d8c"), "lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md", "144/144"),
    ("0d8c quantization", R("20261010-0100-second-20261009-2348-scout-3851-0d8c"), "lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md", "fixed-point quantization"),
    ("0d8c averaging 127", R("20261010-0100-second-20261009-2348-scout-3851-0d8c"), "lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md", "127/144"),
    ("0d8c scalar 142", R("20261010-0100-second-20261009-2348-scout-3851-0d8c"), "lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md", "142/144"),
    ("0d8c ruin speed", R("20261010-0100-second-20261009-2348-scout-3851-0d8c"), "lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md", "2-4x"),
    ("0d8c monodromy form", R("20261010-0100-second-20261009-2348-scout-3851-0d8c"), "lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md", "monodromies"),
    # --- grades, as the page states them ---
    ("grade fa4b gold", R("20261006-1738-b-kerr-compiler-fa4b"), "lab/results/20261006-1738-b-kerr-compiler-fa4b/check.md", "Grade: gold"),
    ("grade 6586 gold", R("20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586"), "lab/results/20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586/check.md", "Grade: gold"),
    ("grade 3851 gold", R("20261009-2348-scout-3851"), "lab/results/20261009-2348-scout-3851/check.md", "Grade: gold"),
    ("grade 0d8c gold", R("20261010-0100-second-20261009-2348-scout-3851-0d8c"), "lab/results/20261010-0100-second-20261009-2348-scout-3851-0d8c/check.md", "Grade: gold"),
    ("grade 2da8 gold", R("20261012-0138-second-20261012-0036-scout-aac1-2da8"), "lab/results/20261012-0138-second-20261012-0036-scout-aac1-2da8/check.md", "Grade: gold"),
    ("grade 6765 gold-first", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/check.md", "Grade: gold"),
    ("grade ae29 gold-first", R("20261006-2240-b-root-keys-ae29"), "lab/results/20261006-2240-b-root-keys-ae29/check.md", "Grade: gold"),
    ("grade 4e9c silver", R("20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c"), "lab/results/20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c/check.md", "Grade: silver"),
    ("grade 18d2 lead", R("20261006-1738-b-handoff-surface-18d2"), "lab/results/20261006-1738-b-handoff-surface-18d2/check.md", "Grade: lead"),
    ("grade ecfd silver", R("20261008-0041-redteam-ecfd"), "lab/results/20261008-0041-redteam-ecfd/check.md", "Grade: silver"),
    ("grade aac1 silver", R("20261012-0036-scout-aac1"), "lab/results/20261012-0036-scout-aac1/check.md", "Grade: silver"),
    ("6765 rtf bound", R("20261011-1729-scout-6765"), "lab/results/20261011-1729-scout-6765/check.md", "2e10"),
    ("3851 domain grid", R("20261009-2348-scout-3851"), "lab/results/20261009-2348-scout-3851/dossier.md", "r_p/M = 10"),
    # --- a7f7: consistent handoff atlas (folded this run) ---
    ("a7f7 grade silver", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "Grade: silver"),
    ("a7f7 mirrored boosts", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "mirrored boosts"),
    ("a7f7 mirrored size", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "~sinhη*|s|"),
    ("a7f7 carry drift corrected", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "97 not 58 at 1024 loops"),
    ("a7f7 carry slope", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "0.095/loop"),
    ("a7f7 2 units per 20", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "2 units/20 crossings"),
    ("a7f7 beta 0.85 carry", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "80 vs 4172"),
    ("a7f7 inverse subtlety", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "negated coefficients 0/500"),
    ("a7f7 NB mechanism", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "0.0547"),
    ("a7f7 direction-blind", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/check.md", "direction-blind"),
    ("a7f7 wigner leak", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/dossier.md", "10,376 units"),
    ("a7f7 nocarry exponent", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/dossier.md", "exponent 0.989"),
    ("a7f7 sigma-delta", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/dossier.md", "sigma-delta remainder"),
    ("a7f7 66x", R("20261005-1540-m-macro-structure-a7f7"), "lab/results/20261005-1540-m-macro-structure-a7f7/dossier.md", "66x at 10³ loops"),
    # --- 13ae: evection slow flow + changeover (folded this run) ---
    ("13ae grade silver", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "Grade: silver"),
    ("13ae retro boundary", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "0.18-0.20"),
    ("13ae crossover kicks", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "kick-8 is 3.8%"),
    ("13ae kick32 0.6", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "kick-32 0.6%"),
    ("13ae avg1Q 46.7", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "46.7%"),
    ("13ae crossover band", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "0.22-0.26 R_H"),
    ("13ae retro e015", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "already broken at 0.20 R_H"),
    ("13ae events range", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "0.39-2.92"),
    ("13ae lie/deprit", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "Lie/Deprit"),
    ("13ae trunc budget", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/check.md", "2.8-4.7%"),
    ("13ae 14-127", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/dossier.md", "14-127%"),
    ("13ae evection", R("20261003-0520-components-13ae"), "lab/results/20261003-0520-components-13ae/dossier.md", "evection"),
    # --- 21db: tide kernel form (folded this run) ---
    ("21db grade silver", R("20261002-0539-redteam-fermi2-21db"), "lab/results/20261002-0539-redteam-fermi2-21db/check.md", "Grade: silver"),
    ("21db radial tide", R("20261002-0539-redteam-fermi2-21db"), "lab/results/20261002-0539-redteam-fermi2-21db/check.md", "-w(3γ²-1)"),
    ("21db factors", R("20261002-0539-redteam-fermi2-21db"), "lab/results/20261002-0539-redteam-fermi2-21db/check.md", "1.50 at 6M"),
    ("21db O(1)-wrong", R("20261002-0539-redteam-fermi2-21db"), "lab/results/20261002-0539-redteam-fermi2-21db/check.md", "O(1)-wrong"),
    ("21db errors halve", R("20261002-0539-redteam-fermi2-21db"), "lab/results/20261002-0539-redteam-fermi2-21db/check.md", "member errors halve"),
    # --- 3d2c: boundary placement (folded this run) ---
    ("3d2c grade silver", R("20260930-2250-taleb-3d2c"), "lab/results/20260930-2250-taleb-3d2c/check.md", "Grade: silver"),
    ("3d2c 100x chatter", R("20260930-2250-taleb-3d2c"), "lab/results/20260930-2250-taleb-3d2c/check.md", "100x in handoff chatter"),
    ("3d2c tau placement", R("20260930-2250-taleb-3d2c"), "lab/results/20260930-2250-taleb-3d2c/check.md", "0.25-0.30 R_Hill, not the 0.45"),
    # --- 3565: r3 v3, the two-body premise (folded this run) ---
    ("3565 grade silver", R("20260930-1250-rung-r3-two-body-doll-v3-3565"), "lab/results/20260930-1250-rung-r3-two-body-doll-v3-3565/check.md", "Grade: silver"),
    ("3565 kill eob-doll", R("20260930-1250-rung-r3-two-body-doll-v3-3565"), "lab/results/20260930-1250-rung-r3-two-body-doll-v3-3565/check.md", "KILL of eob-doll"),
    ("3565 handoff exponent", R("20260930-1250-rung-r3-two-body-doll-v3-3565"), "lab/results/20260930-1250-rung-r3-two-body-doll-v3-3565/check.md", "exponent 0.23 across 100 handoffs"),
    # --- 7a46: Levi-Civita radial singular set (folded this run) ---
    ("7a46 grade gold", R("20261006-1135-scout-7a46"), "lab/results/20261006-1135-scout-7a46/check.md", "Grade: gold"),
    ("7a46 levicivita", R("20261006-1135-scout-7a46"), "lab/results/20261006-1135-scout-7a46/check.md", "Levi-Civita"),
    ("7a46 K events", R("20261006-1135-scout-7a46"), "lab/results/20261006-1135-scout-7a46/check.md", "at K events independent of depth"),
    ("7a46 fallback cost", R("20261006-1135-scout-7a46"), "lab/results/20261006-1135-scout-7a46/check.md", "18-93x"),
]
# fix the one intentionally-dummy ref (guard against copy slips)
ROWS = [("6765 cycle err", R("20261011-1729-scout-6765"), p, n) if "DUMMY" in r
        else (l, r, p, n) for (l, r, p, n) in ROWS]

def git(args):
    return subprocess.run(["git", "-C", REPO] + args, capture_output=True, text=True).stdout

MAIN_CHECKS = [
    ("main has kerr.rs", lambda: bool(git(["cat-file", "-e", "origin/main:crates/space/src/kerr.rs"]) or git(["ls-tree", "origin/main", "crates/space/src/kerr.rs"]))),
    ("main kerr unreviewed commit", lambda: "not reviewed, not merged" in git(["log", "-1", "--format=%B", "cd57fd7a"])),
    ("main kerr LACKS fa4b guard", lambda: "triple root" not in git(["show", "origin/main:crates/space/src/kerr.rs"])),
    ("main lacks handoff_params_derived", lambda: git(["grep", "-c", "handoff_params_derived", "origin/main", "--", "crates/"]) == ""),
    ("kick-jet page routes 4c5b to gravity-news", lambda: "gravity-news topic" in git(["show", "origin/main:lab/wiki/kick-jet.md"]) and "4c5b" in git(["show", "origin/main:lab/wiki/kick-jet.md"])),
]

# --- accounting: zero in-window hits unaccounted (this run's gold bar) ---
# The window is the union of: the regex snapshot (work/sweep-hits.txt, 84 ids at
# this run's snapshot), the original run's 16-run cluster (its own broader sweep;
# most of it never matches the narrow regex), and 13ae (checker-named; it misses
# the regex). routing.tsv holds exactly one decision per window id.
import os
RUNDIR = os.path.dirname(os.path.abspath(__file__))
CLUSTER = """20261006-1738-b-handoff-surface-18d2 20261006-1738-b-kerr-compiler-fa4b
20261006-2240-second-20261006-1738-b-kerr-compiler-fa4b-6586 20261006-2240-b-root-keys-ae29
20261007-0128-second-20261006-2240-b-root-keys-ae29-4e9c 20261008-0041-redteam-ecfd
20261009-2348-scout-3851 20261010-0100-second-20261009-2348-scout-3851-0d8c
20261011-1729-scout-6765 20261012-0036-scout-aac1
20261012-0138-second-20261012-0036-scout-aac1-2da8 20261006-0346-spacex-1381
20261006-0737-autoresearch-8d6e 20261011-1102-autoresearch-11de
20261007-0341-quant-24cd 20261007-1234-components-97bf""".split()

def _accounting():
    snap = [l.strip() for l in open(os.path.join(RUNDIR, "work/sweep-hits.txt")) if l.strip()]
    window = sorted(set(snap) | set(CLUSTER) | {"20261003-0520-components-13ae"})
    rows = {}
    for line in open(os.path.join(RUNDIR, "routing.tsv")):
        if not line.strip():
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            return False
        rows[parts[0]] = parts[1]
    unaccounted = [w for w in window if w not in rows]
    invented = [r for r in rows if r not in window]
    if unaccounted or invented:
        print(f"FAIL accounting: unaccounted={unaccounted} invented={invented}")
        return False
    n_cluster = sum(1 for c in rows.values() if c in ("PAGE-ORIG", "ROUTED-ORIG"))
    if n_cluster != 16:
        print(f"FAIL accounting: cluster count {n_cluster} != 16")
        return False
    folded = sorted(rid for rid, c in rows.items() if c == "FOLDED")
    per = {rid: sum(1 for _l, ref, _p, _n in ROWS if rid in ref) for rid in folded}
    if any(v < 2 for v in per.values()):
        print(f"FAIL accounting: folded runs without needles {per}")
        return False
    print(f"accounting: {len(window)} window ids all accounted; cluster 16; "
          f"folded {[r.split('-')[-1] for r in folded]}")
    return True

MAIN_CHECKS.append(("zero in-window hits unaccounted", _accounting))

fails = 0
for label, ref, path, needle in ROWS:
    hay = norm(fetch(ref, path))
    ok = norm(needle) in hay
    if not ok:
        fails += 1
    print(f"{'PASS' if ok else 'FAIL'}  {label}  [{needle}]")
for label, fn in MAIN_CHECKS:
    try:
        ok = bool(fn())
    except Exception as e:
        ok = False
    if not ok:
        fails += 1
    print(f"{'PASS' if ok else 'FAIL'}  {label}")

print(f"\n{len(ROWS)+len(MAIN_CHECKS)-fails}/{len(ROWS)+len(MAIN_CHECKS)} checks passed")
sys.exit(1 if fails else 0)
