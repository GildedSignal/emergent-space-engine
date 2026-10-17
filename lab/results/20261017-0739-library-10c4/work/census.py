#!/usr/bin/env python3
"""Boundary outcome-class census from one shipped nladder flight's stats line."""
import re, sys

log = open(sys.argv[1]).read()
m = re.search(r'stats \{opens (\d+), boundaries (\d+), handoffs (\d+), lost (\d+), refused (\d+), slices (\d+)\}', log)
if not m:
    sys.exit('no stats line')
opens, boundaries, handoffs, lost, refused, slices = map(int, m.groups())
plain = boundaries - handoffs - lost
mk = re.search(r'kicks (\d+) \(', log)
kicks = int(mk.group(1)) if mk else 0
print(f'boundaries {boundaries} | handoffs {handoffs} | lost {lost} | plain {plain} '
      f'({100.0 * plain / boundaries:.3f}%) | kicks {kicks} | kick/boundary ratio '
      f'{kicks / boundaries:.3f}')
assert plain / boundaries > 0.99, 'prediction 2 failed: boundary comb is law work'
print('prediction 2 HELD: >= 99% of boundaries are plain (certificates + anchor + replan)')
