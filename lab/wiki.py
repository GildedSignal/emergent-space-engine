#!/usr/bin/env python3
"""The lab's wiki (lab/wiki/README.md): one page per topic, compiled from the runs, which stay immutable on their branches.

  wiki.py index                       rewrite lab/wiki/index.md from the pages' headers and the repository
  wiki.py apply <results-dir> <base>  merge each graded run's proposed pages (<results-dir>/<id>/wiki/*.md) into lab/wiki/,
                                      three-way against the page as it stood when the run started (<id>/base, else <base>)

A page's header is its first lines, `key: value`, until the first blank line:
  topic, status (open | closed), closed-by (three or more gold run ids), valid-while (paths @ commit), updated (run id).
The certificate: a closed page reopens by itself when any `valid-while` path changed on main after its commit.
"""
import os, re, subprocess, sys

WIKI = "lab/wiki"
SKIP = {"index.md", "README.md"}


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r


def header(text):
    h = {}
    for line in text.splitlines():
        if not line.strip():
            break
        m = re.match(r"^([a-z-]+):\s*(.*)$", line)
        if m:
            h[m.group(1)] = m.group(2).strip()
    return h


def grade(run):
    r = git("log", "-1", "--format=%s", f"origin/claude/lab-{run}", check=False)
    m = re.search(r"Grade: (\w+)", r.stdout)
    return m.group(1) if m else "unknown"


def certificate(h):
    """'closed', 'open', or 'reopened: <why>' (a broken certificate)."""
    if h.get("status") != "closed":
        return "open"
    golds = [r for r in h.get("closed-by", "").split() if grade(r) == "gold"]
    if len(golds) < 3:
        return f"reopened: closed by {len(golds)} gold runs, three needed"
    m = re.match(r"^(.*)@\s*([0-9a-f]{7,40})$", h.get("valid-while", ""))
    if not m:
        return "reopened: no valid-while certificate"
    paths, commit = m.group(1).split(), m.group(2)
    changed = git("diff", "--name-only", commit, "HEAD", "--", *paths, check=False)
    if changed.returncode:
        return f"reopened: certificate commit {commit} unknown"
    if changed.stdout.strip():
        return f"reopened: {changed.stdout.split()[0]} changed since {commit}"
    return "closed"


def split_runs(text):
    """(the page without its `## Runs` section, the section's run lines)."""
    m = re.search(r"^## Runs\s*$", text, re.M)
    if not m:
        return text, []
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    lines = [l for l in (rest[:end.start()] if end else rest).splitlines() if l.startswith("- ")]
    return text[:m.start()] + (rest[end.start():] if end else ""), lines


def summary(text):
    """The page's first line under '## Current best'."""
    m = re.search(r"^## Current best\s*\n+(.+)$", text, re.M)
    return m.group(1).strip()[:220] if m else "(no current best yet)"


def index():
    rows = []
    for name in sorted(os.listdir(WIKI)):
        if not name.endswith(".md") or name in SKIP:
            continue
        text = open(os.path.join(WIKI, name), encoding="utf-8").read()
        h = header(text)
        runs = len(re.findall(r"^- \d{8}-\d{4}-", text, re.M))
        conflict = " **conflict to resolve**" if "<<<<<<<" in text else ""
        best_lines = len([l for l in split_runs(text)[0].split("## Current best", 1)[-1].split("\n## ", 1)[0].splitlines() if l.strip()])
        if best_lines > 15 or len(text.splitlines()) > 300:
            conflict += f" **over budget ({len(text.splitlines())} lines, current best {best_lines})**"
        rows.append((certificate(h), name, runs, summary(text), conflict))
    out = ["# Lab wiki: index", "",
           "Written by `lab/wiki.py index` after every publish; never edited by hand. Open and reopened topics take new runs;",
           "closed ones do not, until their certificate breaks. Fewest runs first among the open.", "",
           "| Topic | State | Runs | Current best |", "|---|---|---|---|"]
    order = lambda r: (r[0] == "closed", r[2])
    for state, name, runs, best, conflict in sorted(rows, key=order):
        out.append(f"| [{name[:-3]}]({name}) | {state}{conflict} | {runs} | {best.replace('|', '/')} |")
    open(os.path.join(WIKI, "index.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")


def apply(results, base):
    for run in sorted(os.listdir(results)):
        done = os.path.join(results, run, "DONE")
        pages = os.path.join(results, run, "wiki")
        if not (os.path.isfile(done) and os.path.isdir(pages)):
            continue
        g = re.search(r"Grade: (\w+)", open(done).read())
        if not g or g.group(1) not in ("gold", "silver"):
            continue  # leads and missing runs keep their pages on their own branch
        for name in sorted(os.listdir(pages)):
            if not re.fullmatch(r"[a-z0-9-]+\.md", name) or name in SKIP:
                continue
            ours, theirs = os.path.join(WIKI, name), os.path.join(pages, name)
            if not os.path.exists(ours):
                open(ours, "w", encoding="utf-8").write(open(theirs, encoding="utf-8").read())
                print(f"wiki: {run} created {name}")
                continue
            start = os.path.join(results, run, "base")  # the commit the run started from (run.sh writes it)
            b = open(start).read().strip() if os.path.isfile(start) else base
            old = git("show", f"{b}:{WIKI}/{name}", check=False).stdout
            mine, theirs_text = open(ours, encoding="utf-8").read(), open(theirs, encoding="utf-8").read()
            # The append-only `## Runs` list is merged as a union; the rest of the page three-way.
            body = {k: split_runs(v) for k, v in (("ours", mine), ("base", old), ("theirs", theirs_text))}
            tmp = {k: os.path.join(results, run, f".{k}-{name}") for k in body}
            for k in body:
                open(tmp[k], "w", encoding="utf-8").write(body[k][0])
            r = subprocess.run(["git", "merge-file", "-p", "-L", "main", "-L", "run start", "-L", run, tmp["ours"], tmp["base"], tmp["theirs"]],
                               capture_output=True, text=True)
            runs = body["ours"][1] + [l for l in body["theirs"][1] if l not in body["ours"][1]]
            open(ours, "w", encoding="utf-8").write(r.stdout.rstrip("\n") + "\n\n## Runs\n" + "".join(l + "\n" for l in runs))
            for f in tmp.values():
                os.remove(f)
            print(f"wiki: {run} merged {name}{' with conflicts' if r.returncode else ''}")


if __name__ == "__main__":
    cmd = sys.argv[1:2]
    if cmd == ["index"]:
        index()
    elif cmd == ["apply"] and len(sys.argv) == 4:
        apply(sys.argv[2], sys.argv[3])
        index()
    else:
        raise SystemExit(__doc__)
