#!/usr/bin/env python3
"""e517: fold the firing-sweep logs into the dossier numbers.

Per draw (.err from finpol/race with the fd35 instrument + the e517 `out=` field):
exit/FIRE, armed history (first/last positive-A publish, count), the fatal clash's
PRE D against the FIRE violation, the equality law on non-fatal clashes, and the
sibling-closure gap (`out=` non-empty RB events).
"""
import re
import sys
from pathlib import Path

HAZ = re.compile(r'^HAZ p=(\d+) t=([\d.]+) f=(-?\d+) F=(-?\d+) S=(-?\d+) g=(-?\d+) b=(\d+) A=(.*)$')
PRE = re.compile(r'^PRE id=(\d+) s=(-?\d+) e=(-?\d+) D=Some\(\((-?\d+), (\d+), (-?\d+)\)\)')
RB = re.compile(r'^RB lid=(\d+) s0=(-?\d+) s=(-?\d+) .* m=(-?\d+) out=(\[[^]]*\]) mo=(-?\d+)')
FIRE = re.compile(r'^FIRE id=(\d+) s0=(-?\d+) fin_hi=(-?\d+)')


def draw(p: Path) -> dict:
    txt = p.read_text(errors='replace').splitlines()
    haz_a = []          # (p, t, A) per publish
    pre = []            # (id, D, tline, s0)
    fires = []          # (id, s0, fin_hi)
    rbs = []            # (m, out_nonempty, mo)
    fire_ln = None
    for i, ln in enumerate(txt):
        if m := HAZ.match(ln):
            a = m.group(8)
            if a != '-':
                haz_a.append((int(m.group(1)), float(m.group(2)), int(a.split()[0])))
        elif m := PRE.match(ln):
            pre.append((int(m.group(1)), int(m.group(4)), i))
        elif m := RB.match(ln):
            rbs.append((int(m.group(4)), m.group(5) != '[]', int(m.group(6))))
        elif m := FIRE.match(ln):
            fires.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
            fire_ln = fire_ln or i
    armed = [h for h in haz_a if h[2] > 0]
    # fatal PREs: D>0 lines that precede the first FIRE line
    fatal_pre = [pp for pp in pre if fire_ln is not None and pp[2] < fire_ln and pp[1] > 0]
    viol = [f[2] - f[1] for f in fires]
    return {
        'draw': p.stem,
        'pub': len(haz_a),
        'armed': len(armed),
        'first_armed': armed[0][:2] if armed else None,
        'last_armed': armed[-1][:2] if armed else None,
        'pre_d_pos': len(fatal_pre),
        'd_adjacent': bool(fatal_pre) and fire_ln is not None and (fire_ln - max(pp[2] for pp in fatal_pre)) <= 9,
        'pre_d_fatal': sorted({pp[1] for pp in fatal_pre}),
        'fire_viol': sorted(set(viol)),
        'd_match': bool(fatal_pre) and bool(viol) and set(pp[1] for pp in fatal_pre) >= set(viol),
        'rb': len(rbs),
        'm_nonzero': sum(1 for r in rbs if r[0] != 0),
        'out_open': sum(1 for r in rbs if r[1]),
        'mo_max': max((r[2] for r in rbs), default=0),
        'nd0': sum(1 for pp in pre if pp[1] == 0),
        'nd_neg': sum(1 for pp in pre if pp[1] < 0),
        'nd_pos_nonfatal': sum(1 for pp in pre if pp[1] > 0 and (fire_ln is None or pp[2] > fire_ln)),
    }


def main() -> None:
    rows = [draw(p) for p in sorted(Path(sys.argv[1]).glob('*.err'))]
    print(f"{'draw':<12} {'pub':>5} {'armd':>5} {'firstA(p,t)':>13} {'rb':>4} {'m!=0':>5} {'outOpen':>7} {'D=0':>5} {'D<0':>4} {'fatalD':>7} {'viol':>5} {'D=viol':>6}")
    fired = 0
    for r in rows:
        fa = f"{r['first_armed'][0]},{r['first_armed'][1]}" if r['first_armed'] else '-'
        fired += bool(r['fire_viol'])
        print(f"{r['draw']:<12} {r['pub']:>5} {r['armed']:>5} {fa:>13} {r['rb']:>4} {r['m_nonzero']:>5} {r['out_open']:>7} {r['nd0']:>5} {r['nd_neg']:>4} {str(r['pre_d_fatal']):>7} {str(r['fire_viol']):>5} {str(r['d_match']):>6}")
    tot_rb = sum(r['rb'] for r in rows)
    print(f"\nfired draws: {fired}/{len(rows)}")
    print(f"armed-before-fire fails (P2): {sum(1 for r in rows if r['fire_viol'] and (r['first_armed'] is None or r['armed'] == 0))}")
    print(f"D=viol fails (P3): {sum(1 for r in rows if r['fire_viol'] and not r['d_match'])}")
    print(f"out= opened (P4): {sum(r['out_open'] for r in rows)} of {tot_rb} RB events; mo_max={max(r['mo_max'] for r in rows)}")
    print(f"equality law (P5): m!=0 events={sum(r['m_nonzero'] for r in rows)}, D<0={sum(r['nd_neg'] for r in rows)}, D>0 non-fatal={sum(r['nd_pos_nonfatal'] for r in rows)}")
    print(f"armed no fire (P6): {[r['draw'] for r in rows if r['armed'] > 0 and not r['fire_viol']]}")


if __name__ == '__main__':
    main()
