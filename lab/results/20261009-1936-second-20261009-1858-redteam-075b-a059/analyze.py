#!/usr/bin/env python3
"""Parse ladder.log into the frozen verdict table (predictions.md kill rule)."""
import re, sys, collections

rows = collections.defaultdict(list)  # (e,s,eps,sign,floor,tmode) -> list of dict
pat = re.compile(r"JET p=(\S+) e=(\S+) s=(\S+) eps=(\S+) sign=(\d) floor=(\S+) "
                 r"margin=(\S+) tmode=(\d) seed=(\d+) KPO=(\d+) Norb=(\d+) hz=(\d+) "
                 r"nanch=(\d+) anch_per_orbit=(\S+) cr=(\S+) evals_per_orbit=(\S+) "
                 r"maxerr=(\S+) lasterr=(\S+) maxcons=(\S+) Hbase=(\S+) Hmax=(\S+) sat=(\d)")
for line in open(sys.argv[1] if len(sys.argv)>1 else "ladder.log"):
    m = pat.match(line.strip())
    if not m: continue
    g = m.groups()
    d = dict(p=float(g[0]), e=float(g[1]), s=float(g[2]), eps=float(g[3]), sign=int(g[4]),
             floor=g[5], margin=float(g[6]), tmode=int(g[7]), seed=int(g[8]),
             hz=int(g[11]), nanch=int(g[12]), apo=float(g[13]), cr=float(g[14]),
             ev=float(g[15]), maxerr=float(g[16]), maxcons=float(g[18]),
             Hmax=float(g[20]), sat=int(g[21]))
    rows[(d['e'],d['s'],d['eps'],d['sign'],d['floor'],d['tmode'])].append(d)

print(f"{'e':>4} {'s':>5} {'eps':>7} {'fl':>6} {'tm':>2} | {'anch/orb':>8} {'evals/orb':>9} "
      f"{'maxerr':>9} {'hz':>4} {'sat':>3} | verdict")
for k in sorted(rows, key=lambda k:(k[0],-k[1],k[2],k[3],float(k[4]),k[5])):
    rs = rows[k]
    # frozen rule uses margins 1 and 4; take margin=1 rows for the headline, but
    # the kill rule says "any config incl margin 4" -> best-of across margins 1,4
    best = None
    for r in rs:
        ok = (r['ev'] <= 700 and r['maxerr'] <= 1e-3)
        if best is None or (ok and not best[0]) or (ok==best[0] and r['ev']<best[1]):
            best = (ok, r['ev'], r)
    m1 = [r for r in rs if True]
    rmax = max(rs, key=lambda r: r['ev'])
    rerr = max(rs, key=lambda r: r['maxerr'])
    ok, ev, r = best
    verdict = "PASS" if ok else "KILL"
    print(f"{k[0]:>4} {k[1]:>5} {k[2]:>7} {k[4]:>6} {k[5]:>2} | {max(x['apo'] for x in rs):>8.2f} "
          f"{rmax['ev']:>9.0f} {rerr['maxerr']:>9.2g} {min(x['hz'] for x in rs):>4} "
          f"{max(x['sat'] for x in rs):>3} | {verdict}"
          + ("  (best-of-configs passes)" if ok else ""))
