#!/usr/bin/env python3
"""Replay the 16c3/901c publish collision through shipped vs patched wiki.py.

P1: shipped apply, publisher order (16c3 then 901c, both base 046d8d9c)
    reproduces the committed conflicted page byte-for-byte. The shipped tool is
    run UNMODIFIED inside a scratch mini-repo that holds the base page as a
    commit (the shipped apply reads its base via `git show <sha>:lab/wiki/...`,
    so the sandbox must be a real repo — an absolute WIKI override would break
    the base lookup and fabricate conflicts; that instrumentation bug was the
    first attempt, discarded).
P2: patched apply on the same inputs: no marker lands, Runs fold to 18 ids
    (one line each — the colon-attached stale variants fold too, via run_id).
P3: patched re-apply is a no-op (already-folded guard, id-keyed).

Usage: replay_publish.py <shipped|patched> <sandbox-root>
No mutation outside <sandbox-root>.
"""
import os, re, shutil, subprocess, sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
RUN = os.path.dirname(os.path.abspath(__file__))
PAGE = "representation-premises.md"
BASE = "046d8d9c829b4cd9a231e0b3bea960e0446b3011"
RUNS = ["20261021-0213-q-compile-representation-premises-16c3",
        "20261021-0213-redteam-901c"]  # publisher order: sorted(os.listdir)

mode, root = sys.argv[1], os.path.abspath(sys.argv[2])
shutil.rmtree(root, ignore_errors=True)

page_at_base = subprocess.run(["git", "show", f"{BASE}:lab/wiki/{PAGE}"],
                              cwd=REPO, capture_output=True, text=True, check=True).stdout

# fake results tree: DONE (branch-true grade) + base + the run's own proposal
def fake_results(base_ref):
    fake = os.path.join(root, "results")
    for r in RUNS:
        subj = subprocess.run(["git", "log", "-1", "--format=%s", f"origin/claude/lab-{r}"],
                              cwd=REPO, capture_output=True, text=True).stdout
        g = re.search(r"Grade: (\w+)", subj).group(1)
        d = os.path.join(fake, r, "wiki")
        os.makedirs(d)
        open(os.path.join(fake, r, "DONE"), "w").write(f"Grade: {g}\n")
        open(os.path.join(fake, r, "base"), "w").write(base_ref + "\n")
        prop = subprocess.run(["git", "show", f"origin/claude/lab-{r}:lab/results/{r}/wiki/{PAGE}"],
                              cwd=REPO, capture_output=True, text=True, check=True).stdout
        open(os.path.join(d, PAGE), "w", encoding="utf-8").write(prop)
    return fake

if mode == "shipped":
    # scratch mini-repo: the base page is a real commit, so `git show` works
    os.makedirs(os.path.join(root, "lab", "wiki"))
    open(os.path.join(root, "lab", "wiki", PAGE), "w", encoding="utf-8").write(page_at_base)
    shutil.copy(os.path.join(RUN, "work", "wiki-pristine.py"), os.path.join(root, "lab", "wiki.py"))
    git = lambda *a: subprocess.run(["git", "-C", root, *a], capture_output=True, text=True, check=True)
    git("init", "-q")
    git("config", "user.email", "replay@lab"); git("config", "user.name", "replay")
    git("add", "-A"); git("commit", "-qm", "base")
    sha = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    fake = fake_results(sha)
    # the shipped apply, unmodified (index skipped: it needs the run branches)
    subprocess.run([sys.executable, "-c",
                   "import sys; sys.path.insert(0, 'lab'); import wiki; wiki.apply(sys.argv[1], sys.argv[2])",
                   fake, sha],
                   cwd=root, check=True)
    page = os.path.join(root, "lab", "wiki", PAGE)
else:
    os.makedirs(os.path.join(root, "wiki"))
    open(os.path.join(root, "wiki", PAGE), "w", encoding="utf-8").write(page_at_base)
    fake = fake_results(BASE)
    env = dict(os.environ, LAB_WIKI=os.path.join(root, "wiki"))
    subprocess.run([sys.executable, "lab/wiki.py", "apply", fake, BASE],
                   cwd=REPO, env=env, check=True)
    page = os.path.join(root, "wiki", PAGE)

t = open(page, encoding="utf-8").read()
ids = re.findall(r"^- (\d{8}-\d{4}-[a-z0-9-]+)", t, re.M)
cb = len([l for l in t.split("## Current best", 1)[-1].split("\n## ", 1)[0].splitlines() if l.strip()])
flags = ("conflict" if "<<<<<<<" in t else "clean", f"cb={cb}")
print(f"[{mode}] lines={len(t.splitlines())} bullets={len(ids)} distinct={len(set(ids))} "
      f"markers={t.count('<<<<<<<')} {flags[0]} {flags[1]}")
