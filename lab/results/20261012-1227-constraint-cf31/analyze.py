#!/usr/bin/env python3
"""constraint-cf31: reproduce the numbers in dossier.md from the saved runs.

Usage: python3 analyze.py [run-folder]
Each xtask invocation below is the exact command; the saved JSONs are its output.
The decisive probe needs the patched tree (see work/patch.diff): the patch reads
ES_PROBE_NO_CROSSING from the environment; without it the binary runs intact.
"""
import json, re, sys, statistics as st, os, subprocess

folder = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
xtask = "/home/glmlab/lab-target-1/release/xtask"

def bench(rtf, seconds, probe=False, out="/tmp/cf31.json"):
    env = dict(os.environ, **({"ES_PROBE_NO_CROSSING": "1"} if probe else {}))
    subprocess.run([xtask, "universe", "--bench", "--seconds", str(seconds), "--rtf", str(rtf)],
                   check=True, capture_output=True, env=env)
    # the JSON goes to the captured stdout in-process; rerun with shell redirect
    return None

def parts(path, kind):
    """kind in {intact, probe}: per-frame bodies_ms/us-body and readouts/seen."""
    rows, cur = [], {}
    for line in open(path):
        m2 = re.match(r'DIAG2 bodies_ms=([\d.]+)', line)
        m1 = re.match(r'DIAG gather_ms=([\d.]+) readouts=(\d+) seen=(\d+)', line)
        if m2: cur['b'] = float(m2.group(1))
        if m1 and cur:
            cur['g'], cur['ro'], cur['sn'] = map(float, m1.groups())
            rows.append(cur); cur = {}
    if not rows: return None
    per = [(r['b']/r['sn'])*1000 for r in rows if r['sn'] > 5]
    return dict(us_body_p50=st.median(per), readouts_per_seen=st.median([r['ro']/r['sn'] for r in rows if r['sn'] > 5]))

def report():
    print(f"{'rtf':>5} {'gather p50 intact':>18} {'probe':>7} {'drop':>6} {'frame cpu intact':>17} {'probe':>7} {'shares(intact e/g/j/w)':>24}")
    for rtf, sec, f_intact, f_probe in [(1, 12, None, 'probe-diag-rtf1.txt'), (100, 20, 'diag3-rtf100.txt', 'probe-diag-rtf100.txt'), (1000, 20, None, 'probe-diag-rtf1000.txt')]:
        intact = json.load(open(os.path.join(folder, {1: 'bench-paced-30s.json', 100: 'bench-paced-rtf100.json', 1000: 'bench-paced-rtf1000.json'}[rtf])))
        probe = json.load(open(os.path.join(folder, {1: '/tmp/probe-rtf1.json', 100: 'probe-rtf100.json', 1000: 'probe-rtf1000.json'}[rtf]))) if os.path.exists(os.path.join(folder, {100: 'probe-rtf100.json', 1000: 'probe-rtf1000.json'}[rtf]) if rtf != 1 else '/nonexistent') else None
        if probe is None:
            print(f"{rtf:>5} (probe json for rtf=1 not kept; see predictions.md: gather 2.363 -> 1.259 ms)")
            continue
        gi, gp = intact['where_the_time_goes_ms']['view_gather']['p50'], probe['where_the_time_goes_ms']['view_gather']['p50']
        ci, cp = intact['frame_cpu_ms']['p50'], probe['frame_cpu_ms']['p50']
        sh = intact['where_the_time_goes_ms']
        shares = f"{sh['engine']['share']:.2f}/{sh['view_gather']['share']:.2f}/{sh['view_json']['share']:.2f}/{sh['wire']['share']:.2f}"
        digest_same = intact['digest'] == probe['digest']
        print(f"{rtf:>5} {gi:>18.3f} {gp:>7.3f} {gi/gp:>5.1f}x {ci:>17.3f} {cp:>7.3f} {shares:>24} digest_same={digest_same}")

if __name__ == '__main__':
    report()
    for f, tag in [('diag3-rtf100.txt', 'intact rtf=100'), ('diag4-rtf100.txt', 'intact rtf=100 rerun'), ('probe-diag-rtf100.txt', 'probe rtf=100'), ('probe-diag-rtf1000.txt', 'probe rtf=1000')]:
        p = parts(os.path.join(folder, f), tag)
        if p: print(f"{tag:>22}: {p['us_body_p50']:.1f} us/body/frame p50, readouts/seen {p['readouts_per_seen']:.2f}")
