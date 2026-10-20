#!/usr/bin/env python3
"""Compile-check: does wiki/kick-cadence.md (this run) hold every supported number
of lab/wiki/kick-cadence.md (the page it compiles) and stay under the budgets?

Numbers are either INLINE (verbatim in the compiled page) or BEHIND a cited run
(the run id — full or the page's short alias — appears in the compiled page; the
run's own dossier holds the number). Sample curated from every section of the old
page BEFORE the first run of this script; the kill criterion in predictions.md
forbids editing the sample to make it pass.
"""
import re, subprocess, sys, tempfile, os, shutil

RUN = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(RUN, "../../wiki/kick-cadence.md")
NEW = os.path.join(RUN, "wiki/kick-cadence.md")

old = open(OLD, encoding="utf-8").read()
new = open(NEW, encoding="utf-8").read()

fail = []


def section(text, name):
    m = re.search(rf"^## {name}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def best_lines(text):
    body = [l for l in section(text, "Current best").splitlines() if l.strip()]
    return body


# --- budgets (mirrors lab/wiki.py) ------------------------------------------
old_total, new_total = len(old.splitlines()), len(new.splitlines())
old_best, new_best = len(best_lines(old)), len(best_lines(new))
new_open = [l for l in section(new, "Open directions").splitlines() if re.match(r"^\d+\.", l.strip())]
new_refuted = [l for l in section(new, "Refuted").splitlines() if l.startswith("- ")]
print(f"lines: old {old_total} -> new {new_total} (budget <= 300)")
print(f"current best: old {old_best} -> new {new_best} (budget <= 15)")
print(f"open directions: {len(new_open)} (budget <= 8); refuted lines: {len(new_refuted)}")
if new_total > 300: fail.append("page over 300 lines")
if new_best > 15: fail.append("current best over 15 lines")
if len(new_open) > 8: fail.append("over 8 open directions")
if "<<<<<<<" in new: fail.append("conflict marker in page")

# --- runs -------------------------------------------------------------------
rid = re.compile(r"^- (\d{8}-\d{4}-\S+)")
old_ids = [m.group(1) for l in old.splitlines() if (m := rid.match(l))]
new_ids = [m.group(1) for l in new.splitlines() if (m := rid.match(l))]
dups = sorted({i for i in old_ids if old_ids.count(i) > 1})
print(f"run lines: old {len(old_ids)} ({len(set(old_ids))} distinct; duplicates: {dups}) -> new {len(new_ids)} ({len(set(new_ids))} distinct)")
if set(old_ids) - set(new_ids): fail.append(f"runs lost: {set(old_ids) - set(new_ids)}")
if set(new_ids) - set(old_ids): fail.append(f"runs invented: {set(new_ids) - set(old_ids)}")
if len(new_ids) != len(set(new_ids)): fail.append("duplicate run lines in new page")
# append-only order: old distinct order must be a subsequence of new order
it = iter(new_ids)
if not all(any(x == y for y in it) for x in dict.fromkeys(old_ids)):
    fail.append("old run order not preserved")
truncated = [l for l in section(new, "Runs").splitlines() if l.startswith("- ") and len(l) < 60]
if truncated: fail.append(f"suspiciously short run lines: {truncated}")

# --- every current-best line cites a run; every refuted line names one ------
for l in best_lines(new):
    if not re.search(r"\d{8}-\d{4}-|[a-z0-9]{4}-\d{4}|(?:^|\W)(?:7076|3b88|cca6|8ffc|4093|9e75|98cb|e7ef|4e2d|de7b|f790|3570|16ec|49e9|9edc|225d|3294|f82a|71b4|67be|a4ed|1db4|06a8|7f97|5030|2eb1|ad35|f341|5cbd|13ae|0510|53f6|cd52|f2e3|b7a4|27ce|83f9|a9c2)(?=\W|$)", l):
        fail.append(f"current-best line without run citation: {l[:70]}...")
for l in new_refuted:
    if not re.search(r"\(\d{8}|\d{4}\)|[a-z0-9]{3,4}, gold|[a-z0-9]{3,4}\)|→ `", l) and not re.search(r"\b(7076|3b88|cca6|8ffc|4093|9e75|98cb|e7ef|4e2d|de7b|f790|3570|16ec|49e9|9edc|225d|3294|f82a|71b4|67be|a4ed|1db4|06a8|7f97|5030|2eb1|ad35|f341|5cbd|13ae|0510|53f6|cd52|f2e3|b7a4|27ce|83f9|a9c2|0102|9205|e5a2|8685|bb03|65fd|524e|54d9|67f2|0713|ed3a|1a46|efd4)\b", l):
        fail.append(f"refuted line without a killing run: {l[:70]}...")

# --- sampled numbers ---------------------------------------------------------
# (number, expected) where expected is True (must be inline) or the run alias
# that must appear in the new page because the run's dossier holds the number.
SAMPLE = [
    # frontier / wall
    ("0.99049", True), ("1.00282", True), ("0.981", True), ("0.023", True),
    ("5.30e-3", True), ("1.33e-3", True), ("3.32e-4", True), ("8.41e-5", True),
    ("2.12e-2", True), ("2.87e3", True), ("3.9e-13", True), ("1.5e20", True),
    ("9.22e18", "20261020-1326-inversion-3b88"), ("3.195e19", "20261020-1326-inversion-3b88"),
    ("-1.17e-9", "20261020-1326-inversion-3b88"),
    ("1.65e-3", "20261020-1503-second-20261020-1326-inversion-3b88-cca6"),
    ("4.49e-3", "20261020-1503-second-20261020-1326-inversion-3b88-cca6"),
    ("601/1202/2405", "20261020-1503-second-20261020-1326-inversion-3b88-cca6"),
    # two-comb / crest
    ("51.6", True), ("28,141.5", True), ("14,071", True), ("310,224", True),
    ("20.9–23.5", True), ("69–73", True), ("19.2–20.3", True), ("176–187", True),
    ("49.9–54.7", True), ("3.08–3.09", True), ("197,543", True), ("0.988/body", True),
    ("2.5–2.6", True), ("5.9 GB", True), ("21.1 → 0.1 s", True), ("36,748 → 806", True),
    ("1,100–1,179", True), ("84–89", True),
    ("16.7 s", "20261017-0005-dynamics-8ffc"), ("0.903 ms", "20261017-0005-dynamics-8ffc"),
    ("0.993", "20261017-0005-dynamics-8ffc"), ("1,635 game-s", "20261017-0005-dynamics-8ffc"),
    ("10,112", "20261017-0005-dynamics-8ffc"),
    ("46.5–48.7", "20261016-2229-second-20261016-2138-fermi-e7ef-98cb"),
    ("2.34 GB", "20261016-2229-second-20261016-2138-fermi-e7ef-98cb"),
    ("34.8 µs", "20261016-1835-fermi-4093"), ("20.8–21.6", "20261016-1835-fermi-4093"),
    ("1.4 ms", "20261016-2138-second-20261016-1835-fermi-4093-9e75"),
    ("3.33×", "20261016-2138-second-20261016-1835-fermi-4093-9e75"),
    # ledger
    ("10.3 M1 cores", True), ("1.13 µs", True), ("808×", True), ("4.85–5.06", True),
    ("1.19–1.65×10⁶", True), ("274/712", True), ("14.6 µs", True), ("19.9", True),
    ("2.14", "20261016-2138-fermi-e7ef"), ("73.8k", True), ("86–88k", True),
    # boundary comb
    ("167,609", True), ("99.88", True), ("0.117", True), ("202 ns", True),
    ("4,077", True), ("19,423/19,423", True), ("5,126", True), ("12,549", True),
    ("0.166–0.187", True), ("41.3", True), ("96.9", True), ("0c3b1c7dcd0dfeeb", True),
    ("1198b23ec9b91432", True), ("1,200 swept cycles", True),
    ("247,463,935", "20261018-0143-components-16ec"),
    ("a725217f1dcd9f2a", "20261018-0143-components-16ec"),
    ("1.2×10¹⁰", "20261018-0143-components-16ec"),
    ("4.4–5.6 µs", True), ("0.21–0.27 µs", True), ("9.96", True),
    # split lever
    ("0.2500×/1.0000×/4.0003×", True), ("112,565", True), ("0.1250×", True),
    ("29,700/29,700", True),
    ("6.0001", "20261017-1240-second-20261017-1149-fermi-de7b-f790"),
    ("56,282", "20261017-1240-second-20261017-1149-fermi-de7b-f790"),
    ("14,075", "20261017-1240-second-20261017-1149-fermi-de7b-f790"),
    # kick comb / mint
    ("2,037,393", True), ("1,399,871", True), ("57,783", True), ("511/513", True),
    ("2⁻²⁵·v", True), ("1,921/3,719/7,432/14,917/29,794", True), ("58 → 119 MB", True),
    ("192 B + Segment 208 B + Entry 288 B", True), ("688 B", True),
    ("492,362", True), ("1,544,512", True),
    ("19,637", "20261019-2017-second-20261019-1906-spacex-9edc-225d"),
    ("1,143,306", "20261019-2017-second-20261019-1906-spacex-9edc-225d"),
    ("2,044/2,036", "20261019-1906-spacex-9edc"), ("self_ok", "20261019-1906-spacex-9edc"),
    # sub-quantum / train
    ("29,143/29,143", True), ("9,730/9,730", True), ("2⁻²³", True), ("3,570", True),
    ("3.64e-5", True), ("215–277", True), ("0.0015–0.006", True),
    ("246.6", True), ("13,904.8", True), ("820 → 35.5 ms", True), ("0.49·I", True),
    ("16.7–17.7×", "20261015-0128-fermi-ed3a"),
    # regime record
    ("0.5·n^-2.1", True), ("1.14× in tide evals / 1.24×", True), ("0.539", True),
    ("N_lib 4–10", True), ("1,613", True), ("2.303e-2", True), ("fb 2.0e6", True),
    ("1.11–1.56", True), ("0.5Ω", True), ("213×", True), ("3047 → 421", True),
    ("1.65×", True), ("2.8–6.7×", True),
    ("0.65–0.88", "20261014-2012-dynamics-71b4"), ("0.013", "20261014-2012-dynamics-71b4"),
    ("3.1–7.3", "20261014-2012-dynamics-71b4"), ("WS=128", "20261014-2012-dynamics-71b4"),
    # refuted section
    ("1,548×", True), ("71.7–75.2", True), ("2,047/2,049", True), ("0.42–0.47", True),
    ("33/132/704", True), ("0.999", True),
]

inline = behind = missed = 0
for num, exp in SAMPLE:
    if num in new:
        inline += 1
        if exp is not True:
            print(f"  NOTE {num}: inline (also behind {exp})")
        continue
    if exp is True:
        missed += 1
        fail.append(f"number lost, expected inline: {num}")
        continue
    if exp in new:
        behind += 1
    else:
        missed += 1
        fail.append(f"number neither inline nor behind a cited run: {num} (run {exp} not cited)")
print(f"sample: {len(SAMPLE)} numbers — inline {inline}, behind a cited run {behind}, LOST {missed}")

# --- scratch wiki.py index: budget + conflict flags --------------------------
tmp = tempfile.mkdtemp()
try:
    os.makedirs(f"{tmp}/lab/wiki")
    shutil.copy(os.path.join(RUN, "../../wiki.py"), f"{tmp}/lab/wiki.py")
    for f in os.listdir(os.path.join(RUN, "../../wiki")):
        shutil.copy(os.path.join(RUN, "../../wiki", f), f"{tmp}/lab/wiki/{f}")
    shutil.copy(NEW, f"{tmp}/lab/wiki/kick-cadence.md")
    r = subprocess.run([sys.executable, "lab/wiki.py", "index"], cwd=tmp,
                       capture_output=True, text=True, timeout=120)
    row = [l for l in r.stdout.splitlines() if False]  # index writes a file
    idx = open(f"{tmp}/lab/wiki/index.md", encoding="utf-8").read()
    line = next(l for l in idx.splitlines() if "kick-cadence" in l)
    print(f"scratch index row: {line}")
    if "over budget" in line or "conflict" in line:
        fail.append(f"index flags the compiled page: {line}")
    if r.returncode != 0:
        fail.append(f"wiki.py index exited {r.returncode}: {r.stderr[:200]}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n" + ("PASS" if not fail else "FAIL"))
for f in fail:
    print(f"  - {f}")
sys.exit(1 if fail else 0)
