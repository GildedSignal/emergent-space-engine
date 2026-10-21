#!/usr/bin/env python3
"""The e094 checker's named gold experiment, replayed on the shipped record.

Named (check.md, e094): "patch `lab/wiki.py apply`'s Runs union (line 129) to
dedupe by run id, preferring the compiled variant ... then push this page
through the real `apply` + `index` and record the landed state (no flag, no
duplicated ids). Until then, the published page carries 32 run lines and 13
dup ids."

wiki.py variants (all rebuilt from git + stored diffs, no drift):
  pristine : git show DISEASED:lab/wiki.py   — the shipped publisher
  c6ccc    : pristine + work/6ccc-fold.diff  — wiki-memory's flight-proven patch
  b327     : c6ccc + work/b327-ext.diff      — + the skip-as-heal extension (this run)
Corpora (pinned):
  PRE0212  : e094's own base file (what the 02:12 publish started from)
  DISEASED : this run's base file (the shipped record, post-02:12-publish)
Staged runs mirror the publisher's artifact (DONE first line "Grade: …"):
  e094 8179 4c5b 9141 (all graded silver on their branches) and b327 (this
  folder; its grade token is a declared mechanism replay — the publisher only
  folds gold/silver, and this run's real grade is not yet written).

Every step asserts; any failure exits non-zero. Record: work/record.json.
"""
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
E094 = "20261021-0142-q-compile-promotion-e094"
SWEEP = [  # the 02:12 window's four graded runs, in the publisher's sorted order
    "20261021-0142-q-compile-budget-1e9-8179",
    "20261021-0142-q-compile-cell-rebind-4c5b",
    E094,
    "20261021-0142-second-20261021-0106-q-compile-kick-jet-53a2-9141",
]
B327 = os.path.basename(HERE)
REC, FAILURES = {}, []
ID = re.compile(r"\d{8}-\d{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*?-[0-9a-f]{4}")


def ok(name, cond, detail=""):
    REC[name] = {"pass": bool(cond), "detail": detail}
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        FAILURES.append(name)


def sh(*cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr, sep="\n", file=sys.stderr)
        raise SystemExit(f"command failed: {' '.join(cmd)} (cwd={cwd})")
    return r.stdout


def show(rev, path):
    return sh("git", "show", f"{rev}:{path}")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()



DISEASED = open(os.path.join(HERE, "base")).read().strip()
PRE0212 = show(f"origin/claude/lab-{E094}", f"lab/results/{E094}/base").strip()


# ---- the wiki.py module under test (the patched tree's, == b327 variant) ------
spec = importlib.util.spec_from_file_location("wiki_b327", os.path.join(ROOT, "lab", "wiki.py"))
wiki = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wiki)
split_runs, fold_runs = wiki.split_runs, wiki.fold_runs

def runs_of(path_or_text, is_path=True):
    text = open(path_or_text, encoding="utf-8").read() if is_path else path_or_text
    return split_runs(text)[1]


def ids_in(path):
    return set(ID.findall("\n".join(runs_of(path))))



def stats(lines):
    ids = [re.match(r"^- (\S+)", l).group(1) for l in lines if re.match(r"^- (\S+)", l)]
    return {"lines": len(lines), "ids": len(set(ids)), "dups": len(ids) - len(set(ids))}



def apply_patch(patch, d):
    """Apply a git diff inside dir d, POSIX-relative to d (git apply inside a
    repo is repo-root-relative, which would miss d)."""
    sh("patch", "-p1", "-s", "-d", d, "-i", patch)


def mkbox(name, corpus, variant_text):
    """A self-contained publisher box: lab/wiki.py + lab/wiki/ + results/."""
    box = os.path.join(WORK, name)
    shutil.rmtree(box, ignore_errors=True)
    os.makedirs(f"{box}/lab/wiki"); os.makedirs(f"{box}/results")
    open(f"{box}/lab/wiki.py", "w").write(variant_text)
    subprocess.run(["bash", "-c", f"git -C {ROOT} archive {corpus} lab/wiki | tar -x -C {box}"], check=True)
    return box


def stage(box, run, grade="silver", local=False):
    d = os.path.join(box, "results", run)
    shutil.rmtree(d, ignore_errors=True); os.makedirs(f"{d}/wiki")
    open(f"{d}/DONE", "w").write(f"Grade: {grade} | branch claude/lab-{run}\n")
    if local:
        shutil.copy(os.path.join(HERE, "base"), f"{d}/base")
        for p in os.listdir(os.path.join(HERE, "wiki")):
            shutil.copy(os.path.join(HERE, "wiki", p), f"{d}/wiki/{p}")
    else:
        open(f"{d}/base", "w").write(show(f"origin/claude/lab-{run}", f"lab/results/{run}/base"))
        for p in sh("git", "ls-tree", "-r", "--name-only", f"origin/claude/lab-{run}", f"lab/results/{run}/wiki/",
                    cwd=ROOT).splitlines():
            if p.strip():
                open(f"{d}/wiki/{os.path.basename(p)}", "w").write(show(f"origin/claude/lab-{run}", p.strip()))

def publish(box, fallback=DISEASED):
    """The publisher's exact invocation (glm-lab.yml:98): apply, then index."""
    out = sh("python3", "lab/wiki.py", "apply", "results", fallback, cwd=box)
    return out


def measure(wiki_dir):
    out = json.loads(sh("python3", os.path.join(HERE, "measure.py"), wiki_dir))
    return out


def best_len(path):
    text = open(path, encoding="utf-8").read()
    seg = split_runs(text)[0].split("## Current best", 1)[-1].split("\n## ", 1)[0]
    return len([l for l in seg.splitlines() if l.strip()])


def main():
    os.makedirs(WORK, exist_ok=True)
    # variants rebuilt from git + stored diffs; the tree's patched wiki.py must equal b327's
    d = os.path.join(WORK, "variants"); shutil.rmtree(d, ignore_errors=True); os.makedirs(f"{d}/lab")
    open(f"{d}/lab/wiki.py", "w").write(show(DISEASED, "lab/wiki.py"))
    apply_patch(os.path.join(WORK, "6ccc-fold.diff"), d)
    c6ccc = open(f"{d}/lab/wiki.py").read()
    apply_patch(os.path.join(WORK, "b327-ext.diff"), d)
    b327 = open(f"{d}/lab/wiki.py").read()
    ok("variants: tree wiki.py == pristine+6ccc+b327ext", open(os.path.join(ROOT, "lab", "wiki.py")).read() == b327,
       "otherwise work/patch.diff has drifted from the stored diffs")

    # the disease on the shipped record, and what the 02:12 window added to it
    boxD = mkbox("corpus", DISEASED, b327)
    boxP = mkbox("corpusP", PRE0212, b327)
    m, mP = measure(f"{boxD}/lab/wiki"), measure(f"{boxP}/lab/wiki")
    added = {k: m["pages"][k]["dups"] - mP["pages"].get(k, {"dups": 0})["dups"]
             for k in m["pages"] if m["pages"][k]["dups"] != mP["pages"].get(k, {"dups": 0})["dups"]}
    REC["disease"] = {"corpus": DISEASED[:8], "pages": m["n_pages"], "diseased": m["n_diseased"],
                      "dup_lines": m["dup_lines_total"], "promotion": m["pages"]["promotion.md"],
                      "window_added": added}
    print(f"disease at {DISEASED[:8]}: {m['n_diseased']}/{m['n_pages']} pages, {m['dup_lines_total']} dup lines; "
          f"promotion {m['pages']['promotion.md']['lines']}L/{m['pages']['promotion.md']['ids']}ids/"
          f"{m['pages']['promotion.md']['dups']}dups; 02:12 window added {sum(added.values())}: {added}")

    # P1 — harness fidelity: pristine replay of e094's first publish == what shipped
    box = mkbox("p1", PRE0212, show(DISEASED, "lab/wiki.py")); stage(box, E094)
    publish(box, PRE0212)
    ok("P1 pristine replay of e094's publish == shipped page byte-for-byte",
       open(f"{box}/lab/wiki/promotion.md", "rb").read() == show(DISEASED, "lab/wiki/promotion.md").encode())

    # P2 — shipped publisher on the diseased record: re-present is a no-op, disease stands
    box = mkbox("p2", DISEASED, show(DISEASED, "lab/wiki.py")); stage(box, E094); publish(box)
    ok("P2 shipped publisher re-present: no-op, disease stands (32L/13dups)",
       open(f"{box}/lab/wiki/promotion.md", "rb").read() == show(DISEASED, "lab/wiki/promotion.md").encode(),
       str(stats(runs_of(f"{box}/lab/wiki/promotion.md"))))

    # P3 — 6ccc's patch alone: the skip no-ops, nothing heals (the gap b327 closes)
    box = mkbox("p3", DISEASED, c6ccc); stage(box, E094); out = publish(box)
    ok("P3 6ccc-only re-present: skip no-op, no heal",
       open(f"{box}/lab/wiki/promotion.md", "rb").read() == show(DISEASED, "lab/wiki/promotion.md").encode()
       and "healed" not in out)

    # P4 — the named experiment: b327 patch, re-present e094, record the landed state
    box = mkbox("p4", DISEASED, b327); stage(box, E094); out = publish(box)
    p4 = f"{box}/lab/wiki/promotion.md"
    st, lines = stats(runs_of(p4)), runs_of(p4)
    want = runs_of(show(f"origin/claude/lab-{E094}", f"lab/results/{E094}/wiki/promotion.md"), is_path=False)
    body_same = split_runs(open(p4).read())[0] == split_runs(show(DISEASED, "lab/wiki/promotion.md"))[0]
    row = next(l for l in open(f"{box}/lab/wiki/index.md") if "promotion" in l)
    ok("P4 healed: 14 lines / 14 ids / 0 dups", st == {"lines": 14, "ids": 14, "dups": 0},
       f"{st}; heal printed: {'healed' in out}")
    ok("P4 healed Runs == e094 proposal's Runs (the compiled variants win)", lines == want)
    ok("P4 body untouched", body_same)
    ok("P4 index row: open, 14 runs, no flag", "| open | 14 |" in row and "over budget" not in row, row.strip()[:80])

    # P5 — idempotence: the same sweep again is byte-identical
    h1 = {p: sha(f"{box}/lab/wiki/{p}") for p in os.listdir(f"{box}/lab/wiki")}
    publish(box)
    h2 = {p: sha(f"{box}/lab/wiki/{p}") for p in os.listdir(f"{box}/lab/wiki")}
    ok("P5 second identical sweep byte-identical", h1 == h2)

    # P6 — the whole 02:12 sweep through the patched publisher heals every page it compounded
    box = mkbox("p6", DISEASED, b327)
    for r in SWEEP:
        stage(box, r)
    publish(box)
    mA = measure(f"{box}/lab/wiki")
    four = ("promotion.md", "budget-1e9.md", "cell-rebind.md", "kick-jet.md")
    healed_dups = sum(m["pages"][k]["dups"] for k in four)
    ok("P6 every page the 02:12 window compounded is fully healed (0 dups each)",
       all(mA["pages"][k]["dups"] == 0 for k in four)
       and mA["dup_lines_total"] == m["dup_lines_total"] - healed_dups,
       f"corpus {m['dup_lines_total']} -> {mA['dup_lines_total']} (-{healed_dups}); the rest are older topics', "
       f"healed by their own next sweep or the one-time `heal` (P7b)")
    for run, page in [(SWEEP[0], "budget-1e9.md"), (SWEEP[1], "cell-rebind.md"), (E094, "promotion.md"), (SWEEP[3], "kick-jet.md")]:
        got = runs_of(f"{box}/lab/wiki/{page}")
        want = runs_of(show(f"origin/claude/lab-{run}", f"lab/results/{run}/wiki/{page}"), is_path=False)
        ok(f"P6 {page} Runs == its compiled proposal's as a set ({len(got)} lines)",
           sorted(got) == sorted(want), f"{stats(got)}; byte-identical: {got == want}")
        REC[f"p6_{page}_byteidentical"] = got == want
    REC["p6_healed"] = {k: {"before": m["pages"][k], "after": mA["pages"][k]} for k in four}

    # P7 — corpus bound: folding every page's own Runs list loses no id
    lost, cleared = [], 0
    for name in sorted(os.listdir(f"{boxD}/lab/wiki")):
        if not name.endswith(".md") or name in ("index.md", "README.md"):
            continue
        p = f"{boxD}/lab/wiki/{name}"
        body, lines = split_runs(open(p, encoding="utf-8").read())
        before, after = set(ID.findall("\n".join(lines))), set(ID.findall("\n".join(fold_runs(lines, []))))
        if before != after:
            lost.append((name, sorted(before - after)[:3]))
        cleared += len(lines) - len(fold_runs(lines, []))
    ok("P7 fold clears every dup line, zero ids lost corpus-wide", not lost and cleared == m["dup_lines_total"],
       f"cleared {cleared}/{m['dup_lines_total']}, lost {lost}")

    # P7b — the one-time `heal` command clears the standing corpus: every page, no id lost
    boxH = mkbox("p7b", DISEASED, b327)
    before_ids = {n: ids_in(f"{boxH}/lab/wiki/{n}") for n in os.listdir(f"{boxH}/lab/wiki")
                  if n.endswith(".md") and n not in ("index.md", "README.md")}
    sh("python3", "lab/wiki.py", "heal", cwd=boxH)
    mH = measure(f"{boxH}/lab/wiki")
    lostH = [n for n, ids in before_ids.items() if ids_in(f"{boxH}/lab/wiki/{n}") != ids]
    ok("P7b `wiki.py heal` clears the whole corpus (468 -> 0), zero ids lost, idempotent",
       mH["dup_lines_total"] == 0 and not lostH, f"{mH['dup_lines_total']} left, lost {lostH}")
    h1 = {p: sha(f"{boxH}/lab/wiki/{p}") for p in os.listdir(f"{boxH}/lab/wiki")}
    sh("python3", "lab/wiki.py", "heal", cwd=boxH)
    ok("P7b heal idempotent", h1 == {p: sha(f"{boxH}/lab/wiki/{p}") for p in os.listdir(f"{boxH}/lab/wiki")})

    # P8 — patched index() on the untouched corpus is byte-identical to shipped
    sh("python3", "lab/wiki.py", "index", cwd=boxD)
    ok("P8 patched index == shipped index", open(f"{boxD}/lab/wiki/index.md", "rb").read()
       == show(DISEASED, "lab/wiki/index.md").encode())

    # P9 — the next real publish (mechanism replay: this folder's pages, declared grade token)
    stage(box, B327, grade="silver (MECHANISM REPLAY — the real grade is not yet written; the publisher folds gold/silver only)", local=True)
    publish(box)
    pm, wm = f"{box}/lab/wiki/promotion.md", f"{box}/lab/wiki/wiki-memory.md"
    sp, sw = stats(runs_of(pm)), stats(runs_of(wm))
    idx = open(f"{box}/lab/wiki/index.md").read()
    rpro = next(l for l in idx.splitlines() if "promotion" in l)
    rmem = next(l for l in idx.splitlines() if "wiki-memory" in l)
    ok("P9 promotion lands 15 Runs lines, one per id, b327 added",
       sp == {"lines": 15, "ids": 15, "dups": 0} and B327 in open(pm).read(), f"{sp}")
    ok("P9 wiki-memory healed: one line per id (4+b327)", sw == {"lines": 5, "ids": 5, "dups": 0}, f"{sw}")
    ok("P9 both pages under budget, no flags", best_len(pm) <= 15 and best_len(wm) <= 15
       and "over budget" not in rpro + rmem, f"current best {best_len(pm)}/{best_len(wm)} lines")

    REC["verdict"] = "PASS" if not FAILURES else f"FAIL: {FAILURES}"
    json.dump(REC, open(os.path.join(WORK, "record.json"), "w"), indent=1)
    print(f"\nVERDICT: {REC['verdict']}")
    sys.exit(1 if FAILURES else 0)


if __name__ == "__main__":
    main()
