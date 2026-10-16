#!/usr/bin/env python3
"""Heal today's real conflicted pages on a copy and verify content preservation.

Usage: heal-check.py <repo-root>   (writes nothing outside lab/results/<run>/work/healed)
"""
import os, re, shutil, subprocess, sys, pathlib

root = pathlib.Path(sys.argv[1]).resolve()
run_dir = pathlib.Path(__file__).resolve().parent
healed = run_dir / "healed"
if healed.exists():
    shutil.rmtree(healed)
healed.mkdir()
shutil.copy(root / "lab/wiki.py", healed / "wiki.py")

pages = [p for p in sorted((root / "lab/wiki").glob("*.md"))
         if "<<<<<<<" in p.read_text(encoding="utf-8")]
print(f"pages with conflict markers today: {len(pages)} ({', '.join(p.name for p in pages)})")

# per-block side accounting on the originals
def blocks(text):
    out, mode, ours, theirs = [], "copy", [], []
    for line in text.splitlines():
        if mode == "copy" and line.startswith("<<<<<<< "):
            mode, ours, theirs = "ours", [], []
        elif mode == "ours" and line == "=======":
            mode = "theirs"
        elif mode == "theirs" and line.startswith(">>>>>>> "):
            out.append((ours[:], theirs[:]))
            mode = "copy"
        elif mode == "ours":
            ours.append(line)
        elif mode == "theirs":
            theirs.append(line)
    return out

total_blocks = total_inside = 0
for p in pages:
    t = p.read_text(encoding="utf-8")
    bl = blocks(t)
    inside = set()
    for ours, theirs in bl:
        inside.update(ours)
        inside.update(theirs)
    total_blocks += len(bl)
    total_inside += len(inside)
    print(f"  {p.name}: {len(bl)} conflict blocks, {len(inside)} lines inside them")

# heal on a copy via LAB_WIKI
env = dict(os.environ, LAB_WIKI=str(healed / "wiki"))
for p in pages:
    shutil.copy(p, healed / "wiki" / p.name if (healed / "wiki").exists() else healed / p.name)
(healed / "wiki").mkdir(exist_ok=True)
for p in pages:
    shutil.copy(p, healed / "wiki" / p.name)
shutil.copytree(root / "lab/wiki", healed / "wiki" / "_all", dirs_exist_ok=True)  # not used; keep dir complete for index
r = subprocess.run([sys.executable, str(healed / "wiki.py"), "heal"],
                   capture_output=True, text=True, env=env, cwd=str(healed))
print(r.stdout.strip() or r.stderr.strip())

ok = True
kept = 0
for p in pages:
    orig = p.read_text(encoding="utf-8")
    new = (healed / "wiki" / p.name).read_text(encoding="utf-8")
    if "<<<<<<<" in new:
        print(f"  FAIL {p.name}: markers remain"); ok = False; continue
    for ours, theirs in blocks(orig):
        for side in (ours, theirs):
            kept += 1
            if all((not l.strip()) or l.startswith(("<<<<<<<", "=======", ">>>>>>>")) for l in side):
                continue  # pure marker syntax; rewriting it is the point
            content = [l for l in side if l.strip() and not l.startswith(("<<<<<<<", "=======", ">>>>>>>"))]
            missing = [l for l in content if l not in new]
            if missing:
                print(f"  FAIL {p.name}: lost {len(missing)} content lines, e.g. {missing[0][:80]!r}")
                ok = False
print(f"blocks checked: {total_blocks}, sides verified verbatim: {kept}, all preserved: {ok}")

# index regenerates readable rows on the healed copy
r = subprocess.run([sys.executable, str(healed / "wiki.py"), "index"],
                   capture_output=True, text=True, env=env, cwd=str(healed))
rows = [l for l in (healed / "wiki" / "index.md").read_text().splitlines() if p.name[:-3] in l or "topic" in l]
idx = (healed / "wiki" / "index.md").read_text()
leak = [l for l in idx.splitlines() if "<<<" in l]
print(f"healed index rows leak markers: {len(leak)}")
for name in [p.name for p in pages]:
    for l in idx.splitlines():
        if f"]({name[:-3]})" in l or f"[{name[:-3]}]" in l:
            print(" ", l[:150])
