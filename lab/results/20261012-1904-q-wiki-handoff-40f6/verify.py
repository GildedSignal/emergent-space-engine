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
    ("main lacks root keys", lambda: git(["grep", "-l", "-E", "shear_time|root_key", "origin/main", "--", "crates/"]) == ""),
    ("main ships changeover capture", lambda: "1 - LEVELS as i32" in git(["show", "origin/main:crates/universe/src/step.rs"])),
    ("no second checker for 6765", lambda: git(["for-each-ref", "--format=%(refname)", "refs/remotes/origin/claude/lab-*"]).find("second-20261011-1729-scout-6765") < 0),
]

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
