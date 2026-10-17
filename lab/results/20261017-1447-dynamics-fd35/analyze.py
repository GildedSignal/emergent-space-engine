#!/usr/bin/env python3
"""Lab 20261017-1447-dynamics-fd35: fold the matrix logs into the dossier numbers.

Reads every .err produced by the arms (HAZ/PRE/RB/FIRE lines from the alloc.rs
instrument) and prints one row per arm plus totals. Pure parsing; no engine.
"""
import re
import sys
from pathlib import Path
PRE_D = re.compile(r'D=Some\(\((-?\d+), (\d+), (-?\d+)\)\)')
HAZ_A = re.compile(r' A=(-?\d+)')
HAZ_G = re.compile(r' g=(-?\d+)')
RB_M = re.compile(r' m=(-?\d+)')


def arm(p: Path) -> dict:
    txt = p.read_text(errors='replace')
    haz = txt.count('\nHAZ ') + txt.startswith('HAZ ')
    pre = txt.count('\nPRE ') + txt.startswith('PRE ')
    A = [int(m) for m in HAZ_A.findall(txt)]
    G = [int(m) for m in HAZ_G.findall(txt) if int(m) != -9223372036854775808]
    D = [int(m.group(1)) for m in PRE_D.finditer(txt)]
    M = [int(m) for m in RB_M.findall(txt)]
    return {
        'arm': p.stem,
        'pub': haz,
        'pre': pre,
        'rb': txt.count('\nRB ') + txt.startswith('RB '),
        'fire': txt.count('\nFIRE ') + txt.startswith('FIRE '),
        'maxA': max(A) if A else None,
        'posA': sum(1 for a in A if a > 0),
        'maxg': max(G) if G else None,
        'nD': len(D),
        'minD': min(D) if D else None,
        'maxD': max(D) if D else None,
        'maxm': max(M) if M else None,
    }


def main() -> None:
    rows = [arm(p) for p in sorted(Path(sys.argv[1]).glob('*.err'))]
    print(f"{'arm':<12} {'pub':>6} {'pre':>6} {'rb':>5} {'fire':>4} {'maxA':>6} {'posA':>5} {'maxg':>6} {'nD':>6} {'minD':>5} {'maxD':>5} {'maxRBm':>6}")
    for r in rows:
        print(f"{r['arm']:<12} {r['pub']:>6} {r['pre']:>6} {r['rb']:>5} {r['fire']:>4} {str(r['maxA']):>6} {r['posA']:>5} {str(r['maxg']):>6} {r['nD']:>6} {str(r['minD']):>5} {str(r['maxD']):>5} {str(r['maxm']):>6}")
    tot = {k: sum(r[k] for r in rows) for k in ('pub', 'pre', 'rb', 'fire', 'posA', 'nD')}
    print(f"\ntotals: arms={len(rows)} publishes={tot['pub']} precerts={tot['pre']} rollbacks={tot['rb']} fires={tot['fire']} posA_publishes={tot['posA']} clashes={tot['nD']}")
    print(f"equality law: minD={min((r['minD'] for r in rows if r['minD'] is not None), default=None)} maxD={max((r['maxD'] for r in rows if r['maxD'] is not None), default=None)} maxA={max((r['maxA'] for r in rows if r['maxA'] is not None), default=None)}")


if __name__ == '__main__':
    main()
