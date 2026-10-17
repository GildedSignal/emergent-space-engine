#!/usr/bin/env python3
"""All sims for run 20261016-2327-taleb-87d0. Deterministic; writes only under work/sim
(and transiently lab/wiki during S2, restored from git immediately).

S2  arming control: the REAL 20261016-1637 window (two silver runs, real pages, real
    base 2ac3c8d2) replayed through SHIPPED apply() -> markers deepen?
S3  patched heal on copies of today's three real damaged pages -> zero markers of all
    three kinds, content preserved, Runs lists identical, index readable.
S4  post-heal concurrent publish (the gold case): two crafted next-runs editing the
    same Current-best region, patched apply, sandbox repo -> zero markers.
S5  E-case: a fresh publish starting from TODAY's damaged page through patched apply.
S6  amplifier: re-presenting an already-folded run (skip fires) vs no-skip control.
"""
import os, re, shutil, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
RUN = ROOT / "lab/results/20261016-2327-taleb-87d0"
W = RUN / "work"
SIM = W / "sim"
DAMAGED = ["nladder.md", "encounters.md", "scan-queue.md"]
BASE1637 = "2ac3c8d2a4b1a87b1d66ed28f8fdffd46b6fdf04"
sys.path.insert(0, str(W))
import census as C

shutil.rmtree(SIM, ignore_errors=True)
SIM.mkdir(parents=True)


def sh(cmd, cwd=ROOT, env=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, env=dict(os.environ, **(env or {})),
                       capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"FAILED {cmd}\n{r.stdout}\n{r.stderr}")
    return r.stdout


def grab(branch, path, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(subprocess.run(["git", "show", f"{branch}:{path}"], cwd=ROOT,
                                    capture_output=True, check=True).stdout)


# ---------- C1: today's census ----------
print("== C1: today's damage (independent census)")
pages = {}
for name in DAMAGED:
    t = (ROOT / "lab/wiki" / name).read_text(encoding="utf-8")
    pages[name] = t
    print(f"  {name}: {C.census(t)}")
idx = (ROOT / "lab/wiki/index.md").read_text(encoding="utf-8")
leak = [l for l in idx.splitlines() if "<<<" in l]
print(f"  index rows leaking marker text: {len(leak)} of {len([l for l in idx.splitlines() if l.startswith('| [')])} topic rows")

# ---------- S2: arming control, shipped apply, real inputs ----------
print("== S2: real 1637 window through SHIPPED apply (control)")
res = SIM / "results-1637"
for run in ["20261016-1637-dynamics-87fd", "20261016-1637-second-20261016-1319-fermi-1051-1a46"]:
    br = f"origin/claude/lab-{run}"
    (res / run / "DONE").parent.mkdir(parents=True, exist_ok=True)
    (res / run / "DONE").write_text("Grade: silver\n")
    grab(br, f"lab/results/{run}/base", res / run / "base")
    grab(br, f"lab/results/{run}/wiki/nladder.md", res / run / "wiki/nladder.md")
shutil.copy(W / "wiki-pristine.py", SIM / "wiki-pristine-run.py")
out = sh(["python3", str(SIM / "wiki-pristine-run.py"), "apply", str(res), BASE1637])
print("  " + "  ".join(out.strip().splitlines()))
after = (ROOT / "lab/wiki/nladder.md").read_text(encoding="utf-8")
c2 = C.census(after)
print(f"  nladder after shipped replay: {c2}")
sh(["git", "checkout", "--", "lab/wiki"])  # restore the real tree
restored = (ROOT / "lab/wiki/nladder.md").read_text(encoding="utf-8")
print(f"  tree restored byte-identical: {restored == pages['nladder.md']}")

# ---------- S3: patched heal on the real pages ----------
print("== S3: patched heal on copies of the real pages")
hw = SIM / "heal-wiki"
shutil.copytree(ROOT / "lab/wiki", hw)
out = sh(["python3", str(ROOT / "lab/wiki.py"), "heal"], env={"LAB_WIKI": str(hw)})
print("  " + "  ".join(out.strip().splitlines()))
ok3 = True
for name in DAMAGED:
    before, after = pages[name], (hw / name).read_text(encoding="utf-8")
    c = C.census(after)
    good, lost, added = C.preserved(before, after)
    runs_ok = C.runs_list(before) == C.runs_list(after)
    ok = c["markers"] == 0 and good and runs_ok
    ok3 &= ok
    print(f"  {name}: markers={c['markers']} (o{c['open']}/m{c['mid']}/c{c['close']}), "
          f"banners={c['banners']} labels={c['labels']}, content-lost={len(lost)}, runs-identical={runs_ok} -> {'OK' if ok else 'FAIL'}")
    if lost:
        print(f"    LOST e.g. {lost[0][:90]!r}")
untouched = all((ROOT / "lab/wiki" / p.name).read_bytes() == (hw / p.name).read_bytes()
                for p in (ROOT / "lab/wiki").glob("*.md") if p.name not in DAMAGED + ["index.md"])
print(f"  unmarked pages byte-identical: {untouched}")
sh(["python3", str(ROOT / "lab/wiki.py"), "index"], env={"LAB_WIKI": str(hw)})
hidx = (hw / "index.md").read_text(encoding="utf-8")
hrows = [l for l in hidx.splitlines() if any(f"[{n[:-3]}]" in l for n in DAMAGED)]
print(f"  healed index marker leak: {len([l for l in hidx.splitlines() if '<<<' in l])}")
for l in hrows:
    print(f"    {l[:120]}")

# ---------- sandbox repo helper ----------
def repo(name, wiki_src):
    d = SIM / name
    (d / "lab/wiki").mkdir(parents=True)
    shutil.copytree(wiki_src if isinstance(wiki_src, pathlib.Path) else ROOT / "lab/wiki",
                    d / "lab/wiki", dirs_exist_ok=True)
    env = {"GIT_AUTHOR_DATE": "2026-10-17T03:00:00", "GIT_COMMITTER_DATE": "2026-10-17T03:00:00"}
    sh(["git", "init", "-q"], cwd=d)
    sh(["git", "-c", "user.email=sim@lab", "-c", "user.name=sim", "add", "-A"], cwd=d)
    sh(["git", "-c", "user.email=sim@lab", "-c", "user.name=sim", "commit", "-qm", "sim base"], cwd=d, env=env)
    return d, sh(["git", "rev-parse", "HEAD"], cwd=d).strip()


def mkrun(repo_dir, run_id, page_text, base):
    d = repo_dir / "results" / run_id
    (d / "wiki").mkdir(parents=True)
    (d / "DONE").write_text("Grade: silver\n")
    (d / "base").write_text(base + "\n")
    (d / "wiki/nladder.md").write_text(page_text, encoding="utf-8")


def next_page(healed, run_id, sentence):
    """a plausible next run's page: healed standing page + one new current-best line + its runs line"""
    t = healed
    t = re.sub(r"^## Current best\n", f"## Current best\n\n{sentence}\n", t, count=1, flags=re.M)
    t = t.rstrip("\n") + f"\n- {run_id} (silver): the post-heal publish flight (sim).\n"
    return t


healed_nl = (hw / "nladder.md").read_text(encoding="utf-8")

# ---------- S4: the gold case — concurrent publishes on the healed wiki ----------
print("== S4: two concurrent next-runs on healed nladder through PATCHED apply")
r4, H4 = repo("nextrepo", hw)
A = "20261017-0300-fermi-c3d4"
B = "20261017-0300-taleb-a1b2"
mkrun(r4, A, next_page(healed_nl, A, "**Held-out flight A:** the fermi arm's check on the healed page."), H4)
mkrun(r4, B, next_page(healed_nl, B, "**Held-out flight B:** the taleb arm's check on the healed page."), H4)
out = sh(["python3", str(ROOT / "lab/wiki.py"), "apply", "results", H4], cwd=r4, env={"LAB_WIKI": str(r4 / "lab/wiki")})
print("  " + "  ".join(out.strip().splitlines()))
t4 = (r4 / "lab/wiki/nladder.md").read_text(encoding="utf-8")
c4 = C.census(t4)
runs_before, runs_after = C.runs_list(healed_nl), C.runs_list(t4)
gained = [l for l in runs_after if l not in runs_before]
ok4 = c4["markers"] == 0 and len(gained) == 2
print(f"  markers={c4['markers']} (o{c4['open']}/m{c4['mid']}/c{c4['close']}), banners={c4['banners']}, "
      f"runs gained={len(gained)} (expect 2) -> {'OK' if ok4 else 'FAIL'}")
good, lost, _ = C.preserved(healed_nl, t4)
print(f"  healed content still fully present: {good}" + (f" LOST {lost[:2]}" if not good else ""))

# ---------- S5: E-case — a fresh publish starting from TODAY's damaged page ----------
print("== S5: fresh publish from today's DAMAGED page through PATCHED apply")
r5, D5 = repo("dmgrepo", ROOT / "lab/wiki")
E = "20261017-0300-inversion-e5f6"
grab("origin/claude/lab-20261016-1637-dynamics-87fd", "lab/results/20261016-1637-dynamics-87fd/wiki/nladder.md",
     SIM / "e-page.md")
ep = SIM / "e-page.md"
t = ep.read_text(encoding="utf-8").replace("20261016-1637-dynamics-87fd", E)
mkrun(r5, E, t, D5)
out = sh(["python3", str(ROOT / "lab/wiki.py"), "apply", "results", D5], cwd=r5, env={"LAB_WIKI": str(r5 / "lab/wiki")})
print("  " + "  ".join(out.strip().splitlines()))
t5 = (r5 / "lab/wiki/nladder.md").read_text(encoding="utf-8")
c5 = C.census(t5)
print(f"  markers={c5['markers']} (o{c5['open']}/m{c5['mid']}/c{c5['close']}), banners={c5['banners']}")
out = sh(["python3", str(ROOT / "lab/wiki.py"), "heal"], cwd=r5, env={"LAB_WIKI": str(r5 / "lab/wiki")})
t5h = (r5 / "lab/wiki/nladder.md").read_text(encoding="utf-8")
c5h = C.census(t5h)
good5, lost5, _ = C.preserved(t5, t5h)
ok5 = c5h["markers"] == 0 and good5
print(f"  after heal: markers={c5h['markers']}, content-lost={len(lost5)} -> {'OK' if ok5 else 'FAIL'}")
sh(["python3", str(ROOT / "lab/wiki.py"), "heal"], env={"LAB_WIKI": str(r5 / "lab/wiki")})
t5h2 = (r5 / "lab/wiki/nladder.md").read_text(encoding="utf-8")
print(f"  heal idempotent: {t5h2 == t5h}")
ns = W / "wiki-noskip.py"
src = (ROOT / "lab/wiki.py").read_text(encoding="utf-8")
assert 'if any(l.split(" ")[1:2] == [run] for l in body["ours"][1]):' in src
ns.write_text(src.replace('if any(l.split(" ")[1:2] == [run] for l in body["ours"][1]):', 'if False:'), encoding="utf-8")
print("== S6: re-presenting an already-folded run")
r6, H6 = repo("amprepo", hw)
mkrun(r6, "20261016-1637-dynamics-87fd",
      (res / "20261016-1637-dynamics-87fd/wiki/nladder.md").read_text(encoding="utf-8").replace("\n", "\n"),
      "does-not-matter-skip-fires-first")
# give the old run a plausible base: the pre-window commit
(r6 / "results/20261016-1637-dynamics-87fd/base").write_text(BASE1637 + "\n")
mkrun(r6, B, next_page(healed_nl, B, "**Amplifier probe:** the new run's content."), H6)
out = sh(["python3", str(ROOT / "lab/wiki.py"), "apply", "results", H6], cwd=r6, env={"LAB_WIKI": str(r6 / "lab/wiki")})
print("  patched: " + "  ".join(out.strip().splitlines()))
t6 = (r6 / "lab/wiki/nladder.md").read_text(encoding="utf-8")
c6 = C.census(t6)
runs6 = [l for l in C.runs_list(t6) if l not in C.runs_list(healed_nl)]
print(f"  patched: markers={c6['markers']}, banners={c6['banners']}, runs gained={len(runs6)} (expect 1)")
# no-skip control
r6b, H6b = repo("amprepo-ctl", hw)
mkrun(r6b, "20261016-1637-dynamics-87fd", (res / "20261016-1637-dynamics-87fd/wiki/nladder.md").read_text(encoding="utf-8"), BASE1637)
mkrun(r6b, B, next_page(healed_nl, B, "**Amplifier probe:** the new run's content."), H6b)
out = sh(["python3", str(ns), "apply", "results", H6b], cwd=r6b, env={"LAB_WIKI": str(r6b / "lab/wiki")})
print("  no-skip control: " + "  ".join(out.strip().splitlines()))
t6b = (r6b / "lab/wiki/nladder.md").read_text(encoding="utf-8")
c6b = C.census(t6b)
print(f"  no-skip: markers={c6b['markers']}, banners={c6b['banners']}, lines={c6b['lines']} vs patched {c6['lines']}")

print("== VERDICTS: S3", "OK" if ok3 else "FAIL", "| S4", "OK" if ok4 else "FAIL", "| S5", "OK" if ok5 else "FAIL")
