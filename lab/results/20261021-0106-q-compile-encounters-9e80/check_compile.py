#!/usr/bin/env python3
"""Audit of the compiled `encounters` page (this run's wiki/encounters.md) against the
old page (the tree's lab/wiki/encounters.md). Regenerates every number quoted in
dossier.md: budgets, run-id conservation, grade match, number conservation (curated +
seeded random sample). The curated sample and the P5 seed are fixed before the script's
first run and are never edited to pass; fixes go to the page. Instrument history (run 1
and run 2): grade strings differ only in punctuation and "2nd"/"second"; the scratch
index must run from the temp root (wiki.py's WIKI is the relative "lab/wiki") and the
stale copied index.md must be removed first; the citation check must accept the page's
own short run ids. The sample was never touched."""
import os, re, subprocess, sys, tempfile, shutil, random

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "..", "lab", "wiki", "encounters.md")
NEW = os.path.join(HERE, "wiki", "encounters.md")
WIKI_DIR = os.path.join(HERE, "..", "..", "..", "lab", "wiki")  # the tree's wiki, wherever OLD points

SUP = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9","⁻":"-"}
def norm(t):
    for k, v in SUP.items(): t = t.replace(k, v)
    return (t.replace("^", "").replace("×", "x").replace("−", "-").replace("–", "-")
             .replace("≈", "~").replace("·", "*").replace("’", "'").replace("‘", "'"))

def squash(t):  # punctuation-insensitive comparison for grade strings
    t = t.replace("2nd", "second")
    return re.sub(r"[^a-z0-9]+", " ", norm(t).lower()).strip()

old = open(OLD, encoding="utf-8").read()
new = open(NEW, encoding="utf-8").read()
no, nn = norm(old), norm(new)
fails = []

# ---- P1: budgets (lab/wiki.py's own expressions) -------------------------------
def split_runs(text):
    m = re.search(r"^## Runs\s*$", text, re.M)
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    lines = [l for l in (rest[:end.start()] if end else rest).splitlines() if l.startswith("- ")]
    return text[:m.start()] + (rest[end.start():] if end else ""), lines

best_lines = len([l for l in split_runs(new)[0].split("## Current best", 1)[-1]
                  .split("\n## ", 1)[0].splitlines() if l.strip()])
total = len(new.splitlines())
old_best = len([l for l in split_runs(old)[0].split("## Current best", 1)[-1]
                .split("\n## ", 1)[0].splitlines() if l.strip()])
print(f"P1 lines: {len(old.splitlines())} -> {total} (budget <= 300); "
      f"current best {old_best} -> {best_lines} (budget <= 15); "
      f"conflict markers in new: {'<<<<<<<' in new}")
if total > 300 or best_lines > 15 or "<<<<<<<" in new: fails.append("P1")

# scratch index: swap the page into a copy of lab/wiki and run wiki.py index
with tempfile.TemporaryDirectory() as td:
    labd = os.path.join(td, "lab"); os.makedirs(labd)
    shutil.copytree(WIKI_DIR, os.path.join(labd, "wiki"))
    os.remove(os.path.join(labd, "wiki", "index.md"))  # else a crash reads the stale copied row
    shutil.copy(os.path.join(HERE, "..", "..", "..", "lab", "wiki.py"), os.path.join(labd, "wiki.py"))
    shutil.copy(NEW, os.path.join(labd, "wiki", "encounters.md"))
    subprocess.run([sys.executable, os.path.join("lab", "wiki.py"), "index"], cwd=td, capture_output=True, text=True)  # WIKI is the relative "lab/wiki"
    idxp = os.path.join(labd, "wiki", "index.md")
    row = [l for l in open(idxp, encoding="utf-8").read().splitlines() if "encounters" in l] if os.path.exists(idxp) else []
    idx = (row[0] if row else "(no row)").strip()
    print(f"P1 scratch index row: {idx[:150]}")
    if "over budget" in idx or "conflict" in idx: fails.append("P1-scratch")

# ---- P2: run-id conservation --------------------------------------------------
def ids(text):
    out = []
    for m in re.finditer(r"^- (\d{8}-\d{4}-[A-Za-z0-9-]+?) \(", text, re.M):
        i = m.group(1).rstrip("-")
        if i == "20261017-1018-second": i = "20261017-1018-second-20261017-0839-inversion-2373-b509"
        if i == "20261007-1234-quant-7578": i = "20261007-1032-quant-7578"  # page typo, only 1032 has a branch
        out.append(i)
    return out

oi, ni = ids(old), ids(new)
print(f"P2 run lines: {len(oi)} -> {len(ni)}; distinct {len(set(oi))} -> {len(set(ni))}")
missing = set(oi) - set(ni)
extra = set(ni) - set(oi)
dupes = {i for i in ni if ni.count(i) > 1}
order_ok = ni == sorted(ni)
print(f"P2 missing={sorted(missing) or 'none'} extra={sorted(extra) or 'none'} "
      f"dupes={sorted(dupes) or 'none'} chronological={order_ok}")
if missing or extra or dupes: fails.append("P2")

# ---- P3: grades match the branches --------------------------------------------
def branch_grade(run):
    r = subprocess.run(["git", "log", "-1", "--format=%s", f"origin/claude/lab-{run}"],
                       capture_output=True, text=True)
    m = re.search(r"Grade: (.+)", r.stdout)
    return m.group(1).strip() if m else None

mism, nobranch = [], []
for m in re.finditer(r"^- (\d{8}-\d{4}-[A-Za-z0-9-]+?) \(([^)]+)\)", new, re.M):
    run, declared = m.group(1), m.group(2)
    g = branch_grade(run)
    if g is None: nobranch.append(run); continue
    if squash(g) not in squash(declared): mism.append((run, g, declared))
print(f"P3 grades: {len(ni)} run lines, {len(nobranch)} without branch ({', '.join(nobranch)}), "
      f"{len(mism)} mismatches: {mism if mism else 'none'}")
if mism: fails.append("P3")

# ---- P4: curated number conservation ------------------------------------------
# (token in the OLD page's spelling, run id that holds it if not inline)
CURATED = [
    # f2f1 paragraph
    ("0.57","20261019-1906-scout-f2f1"),("0.33",None),("0.03",None),("0.88",None),("2⁻²⁶",None),
    ("0.014",None),("0.003",None),("749",None),("0.088",None),("0.079",None),("0.931",None),("0.853",None),
    ("138:130",None),("0.49/kick",None),("0.999975",None),("8.7e5","20261019-1906-scout-f2f1"),
    ("1.9e3","20261019-1906-scout-f2f1"),("arXiv:2211.09164",None),("1.000",None),
    # 73b5 paragraph
    ("355.3",None),("0.7767",None),("53,946",None),("5.208×10⁻⁶",None),("8/1.54M",None),
    ("27.6k",None),("4,500",None),("5.60×10⁹",None),("1.1×10¹⁵",None),("a = 2.5",None),("2.0001",None),
    ("7×10⁻⁹",None),("2.6×10⁻⁸",None),("6×10⁻⁹",None),("2.3×10⁻⁸",None),("3×10⁻⁵",None),
    ("10⁸–10⁹",None),("7.2×10⁻⁹",None),("140× under",None),("7× OVER",None),("E_pair = 1,024",None),
    ("n/2 = 10³",None),("5×10³",None),("0.35 cores",None),("363 cores",None),("−1.4 to −5.1",None),
    ("4.1×10¹²",None),("10⁴× off",None),("0.7742",None),("0.169–0.174",None),("TAU·a^1.5·2³²",None),
    # e828 paragraph
    ("0/1.54M",None),("P ≥ 256",None),("3.4×10⁻⁵",None),("1.5×10⁻³",None),("6.9×10⁻²",None),
    ("P=1024",None),("1.4×10⁻³",None),("1.8×10⁻¹",None),("64×κ",None),("7.4×10⁻⁴",None),("6.7×10⁻⁵",None),
    ("512×κ",None),("×3.3",None),("2.6×10⁻⁶",None),("6.5×10⁻⁶",None),("3.3×10⁻⁶",None),("1.6×10⁻⁶",None),
    ("6.5×10⁻⁷",None),("2–20 events",None),("q10/q50/q90",None),("7.5×10⁴",None),("4.7×10⁵",None),
    ("1.8×10⁶",None),("0/40,796",None),("8×10⁻⁵",None),("10⁴–10⁵×",None),("armed(16)",None),
    ("5.7×10⁹",None),("E ≈ 64–256",None),("E=64 → 5.5",None),("2.8–5.5",None),
    ("768k",None),("9.2M",None),("21 MB",None),("seed 12345",None),("2⁻¹⁷",None),("1e-3",None),
    # 1176 paragraph
    ("2,000 bodies",None),("3.34×10⁻⁶",None),("2⁻²³·v",None),("2⁻¹⁴",None),("424242",None),
    ("0.48/0.49",None),("7.2×10⁻⁶",None),("147 events",None),("81 events",None),("7.9×10⁻⁶",None),
    ("9.5×10⁻⁵",None),("11× under",None),("0.13w/touch",None),("0.04–0.09",None),("5.5×10⁴",None),
    ("1.02 window",None),("20,000 pairs",None),("(1.1–1.4)×10⁻⁶",None),("2w/π",None),("200k pairs",None),
    ("H ≥ 64",None),("4×10⁴×",None),("0.036",None),("2.4×10⁴",None),("E ~ 16",None),("1/κ²",None),
    ("2⁻¹¹",None),("2⁻³⁰",None),("3.8×10⁴",None),("0.44w",None),("1.3–1.8×10⁻⁶",None),("1.5×10⁻⁶/touch",None),
    ("×2–3",None),("1 boundary artifact",None),("P=64",None),
    # 9fd1 paragraph
    ("0.49–0.59",None),("8–15×",None),("8192",None),("1.7–2.3×",None),("4–25%",None),("κ = 0.08",None),
    ("5.4e-7",None),("1.1e-5",None),("14.7M",None),("0.04/0.08/0.16",None),("×4.6",None),("99.99%",None),
    ("3.6 orders",None),("0.22–0.27",None),("0.28",None),("384–512",None),("2e-6",None),("3.5e-6",None),
    ("19× lower",None),("2.8e-7","20261018-2155-scout-9fd1"),("1.2e-6","20261018-2155-scout-9fd1"),
    ("2⁵³",None),("1e5",None),("[1.5,6]·10⁵",None),("7e-7",None),("2.3–7.3e-5",None),("E·h₀",None),
    # e87d paragraph + checkers
    ("(0.88–0.97)",None),("π/5",None),("2.7 window",None),("2.0 widths",None),("0.8",None),
    ("0.44·w",None),("0.19",None),("1.17",None),("0.18",None),("~2–4×10⁴",None),("2×10⁻³",None),
    ("1/8/64",None),("0.14·w",None),("240,000",None),("1,394",None),("1.13–1.42",None),("1,365–1,372",None),
    ("72%",None),("416 ns",None),("3.4×",None),("~105 cores",None),("~100 ns",None),("2⁻²³/2⁻¹⁷/2⁻¹⁴",None),
    ("2.27×10⁻¹",None),("4.5×10⁻¹",None),("0.32·w",None),("0.39·w",None),("26%",None),("2⁶³",None),
    ("74+",None),("1.7–2.2×10⁻³",None),("41%",None),("a=30 AU",None),("1.42–1.60×",None),("1.36–1.75×",None),
    ("0/400,000",None),("σ_e 0.3",None),("m·y",None),("0/100,000",None),("0.99–1.03",None),
    # 08d0 paragraph
    ("0.48·C/k²",None),("1.8%",None),("6.8%",None),("98.2%",None),("0.45–0.47",None),("128–256",None),
    ("Ew/C",None),("5.5–2.8",None),("5×10⁻⁶",None),("3×10⁻⁴",None),("E²·δd/C",None),("S₁",None),
    # 1a29 paragraph + c9c7/fbf9
    ("5–7×10⁻⁶",None),("~14%",None),("0.034 arm-evals",None),("1.2 µs",None),("4.4×10⁻⁵",None),
    ("3.3×10⁻⁶ AU",None),("0.484·N",None),("X ≈ 1.5",None),("92.5%",None),("10⁷–10⁹",None),
    ("0.5–0.75×",None),("1.1×",None),("w ≈ 23",None),("d ≈ 3×10⁵",None),("10⁵–4×10⁶",None),
    # standing stack + ledger + gate (old runs)
    ("93×",None),("188.6",None),("14.95",None),("142.3→17.1",None),("3.6×",None),("3.0–3.7×",None),
    ("427×",None),("1.39×",None),("144 TB",None),("20–80 ms",None),("12/12",None),("40–97%",None),
    ("0.105→0.247",None),("800 orbits",None),("2.7× median",None),("8 scenes",None),("0.969",None),
    ("206/289",None),("2.7e-10",None),("3/6",None),("1.2·a^2.6",None),("≤ 3.9",None),("rank 0.48",None),
    ("2e·n",None),("0.998",None),("1091",None),("1.3×10⁻¹⁷",None),("×1.02–1.49",None),("×43–312",None),
    ("9.3%",None),("46–92%",None),("99%",None),("0.6–0.8",None),("66/495",None),("23 scenes",None),
    ("~90%",None),("fA 0.067",None),("t^-0.25",None),("0.345·e^-0.215",None),("1.8× Poisson",None),
    ("1.01–1.11×",None),("20.2%",None),("7377→851",None),("0.07%",None),("~4 µs/pair",None),
    ("1.5–1.9 µs",None),("≈10⁴ bodies",None),("3 r_H",None),("Ψ^0.95",None),("78–91%",None),
    ("1.1–20×",None),("43k–3.97M",None),("38k",None),("1.94",None),("0.87–1.04",None),("1.6–2.1×",None),
    ("5.3–5.6",None),("6.8 ms",None),("98% defers",None),("0.0346·n",None),("(1+X)/(2(X−1))",None),
    ("0.077",None),("16 GB",None),("5,216",None),("3×10⁷",None),("1.00000",None),("34-km",None),
    ("D* = 1.3 km",None),("129×",None),("0.03–0.6",None),("1.9×10⁻⁶·v_k",None),("95.5–98.0%",None),
    ("+0.02%",None),("480–700",None),("0.017–0.025",None),("62–571",None),("14–24×",None),("0.003",None),
    ("0.377",None),("×52",None),("95.5–97.8%",None),("37–369",None),("6×10²–9×10³",None),("−73",None),
    ("3.17e-14",None),("2¹¹–2¹²",None),("5–15 bits",None),("36–4,500",None),("4·e_max",None),
    ("0.75·da",None),("3 digits",None),("F = 10⁵×10⁴",None),("0.89 µs",None),("r_p/32",None),
    ("6,144",None),("0.22 contacts/s",None),("1.1e3",None),("≤1.9 cores",None),("5.3–8.4",None),
    ("0.966/0.077",None),("taleb-09b5",None),("rank 4",None),("O(n·k)",None),
]
inline = behind = lost = 0
lost_list = []
for tok, run in CURATED:
    if norm(tok) in nn: inline += 1
    elif run and norm(run) in nn: behind += 1
    else: lost += 1; lost_list.append(tok)
print(f"P4 curated: {len(CURATED)} numbers — {inline} inline, {behind} behind a cited run, {lost} lost")
if lost: print("P4 LOST:", lost_list); fails.append("P4")

# ---- P5: seeded random sample (held-out) --------------------------------------
random.seed(20261021)
body = no
body = re.sub(r"^- \d{8}-\d{4}-[A-Za-z0-9-]+? \(", "RUNID(", body, flags=re.M)  # hide ids in old body
toks = re.findall(r"\d[\d.,:]*%?(?:e[+-]?\d+)?", body)
toks = [t for t in toks if len(t) >= 3 and not re.fullmatch(r"2026\d*", t) and not t.startswith("2026")]
uniq = sorted(set(toks))
sample = random.sample(uniq, 40)
found = [t for t in sample if norm(t) in nn]
miss = [t for t in sample if norm(t) not in nn]
print(f"P5 random sample (seed 20261021, {len(uniq)} candidate tokens): {len(found)}/40 inline; misses: {miss}")

# ---- P6: reader actions --------------------------------------------------------
short_ids = {i[-4:] for i in ni} | {"09b5"}  # the page's citation tokens (09b5: adopted gold cited from the taste log)
def cites_run(l):
    return any(re.search(r"\b" + re.escape(s) + r"\b", l) for s in short_ids) or bool(re.search(r"\d{8}-\d{4}-", l))
cb = new.split("## Current best", 1)[1].split("\n## ", 1)[0]
cb_lines = [l for l in cb.splitlines() if l.strip()]
nocite = [i for i, l in enumerate(cb_lines, 1) if not cites_run(l)]
ref = new.split("## Refuted", 1)[1].split("\n## ", 1)[0]
ref_lines = [l for l in ref.splitlines() if l.startswith("- ")]
noref = [i for i, l in enumerate(ref_lines, 1) if not cites_run(l)]
ods = new.split("## Open directions", 1)[1].split("\n## ", 1)[0]
od_lines = [l for l in ods.splitlines() if l.strip()]
print(f"P6 current-best lines citing runs: {len(cb_lines)-len(nocite)}/{len(cb_lines)} (uncited: {nocite}); "
      f"refuted entries naming a killing run: {len(ref_lines)-len(noref)}/{len(ref_lines)} (unnamed: {noref}); "
      f"open directions: {len(od_lines)} (budget <= 8)")
if nocite or noref or len(od_lines) > 8: fails.append("P6")

print("\nVERDICT:", "ALL CHECKS PASS" if not fails else f"FAILURES: {fails}")
sys.exit(1 if fails else 0)
