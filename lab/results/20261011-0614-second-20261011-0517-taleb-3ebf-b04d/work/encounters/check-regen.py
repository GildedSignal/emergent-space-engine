#!/usr/bin/env python3
"""battle.jsonl (this folder, regenerated) vs battle-original.jsonl (frozen parent record):
every field must match byte-for-byte except the four timing fields and headers."""
import json, sys

def load(p):
    return {d['scene']: d for d in (json.loads(l) for l in open(p) if l.strip() and not l.startswith('#'))}

new, old = load('battle.jsonl'), load('battle-original.jsonl')
skip = {'truth_s', 'setup_s', 'meth_s', 'wall_s'}
bad = [(s, k, new[s][k], old[s][k]) for s in old for k in new[s] if k not in skip and new[s][k] != old[s].get(k)]
print(f"scenes: {len(old)}, mismatches (ex timing): {len(bad)}")
for b in bad:
    print('MISMATCH', b)
sys.exit(1 if bad or len(new) != len(old) else 0)
