#!/usr/bin/env python3
"""Deletion audit + automation-debt count + lookup-budget arithmetic.
Every number in dossier.md section 'Evidence' comes from here.
Run from repo root: python3 lab/results/20261014-1631-library-7f99/work/audit.py"""
import json, re, subprocess, sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
os.chdir(ROOT)
W = 'lab/results/20261014-1631-library-7f99/work'

print('== 1. corpus ==')
hl = [json.loads(l) for l in open(f'{W}/highlights.ndjson')]
books = {(d['t'], d['a']) for d in hl}
print(f'highlights={len(hl)} books={len(books)}')

print('== 2. verbatim anchors (grep -F count, must each be 1) ==')
quotes = {
 'musk_addback': "at least 10% of them, then you didn",  # straight-quote anchor; apostrophe is curly in source
 'musk_automation': "after you have questioned all the requirements and deleted unnecessary parts—before you introduce automation",
 'karpathy_sensor': "Removing radar and ultrasonic sensors and relying solely on vision may make the perception problem easier",
 'asimov_goldenrule': "Do nothing unless you must, and when you must act—hesitate.",
 'feynman_lookup': "when it could be looked up in fifteen minutes",
 'taleb_filter': "simply by establishing a high filter, then picking opportunities that pass such threshold",
}
for k, q in quotes.items():
    n = sum(1 for d in hl if q in (d['x'] or ''))
    src = next(((d['a'], d['t']) for d in hl if q in (d['x'] or '')), None)
    print(f'{k}: {n} | {src[0]} | {src[1][:48]}' if src else f'{k}: 0 NOT FOUND')

# (name, file, regex) — each must match >=1 line
kills = [
 ('cell staircases',       'docs/HISTORY.md', r'killed step-based gravity'),
 ('per-body steps',        'docs/HISTORY.md', 'probe 1 killed the per-body step rule'),
 ('sd16/sd24/sd32',        'docs/HISTORY.md', r'KILL of sd16, sd24 and sd32'),
 ('river refraction',      'docs/HISTORY.md', r'River refraction is killed'),
 ('conjunction kicks',     'docs/HISTORY.md', r'conjunction kicks killed'),
 ('arc kicks g8/g16/half', 'lab/board.md',    r'KILL of arc-integrated kicks'),
 ('nf1/nf2',               'lab/board.md',    r'KILL of nf1 and nf2'),
 ('kick-avg/hill-torus',   'lab/board.md',    r'KILL of kick-avg and hill-torus'),
 ('element-sort/shear-grid/hier-bounds', 'lab/board.md', r'KILL of element-sort, shear-grid and hier-bounds'),
 ('eob-doll',              'lab/board.md',    r'KILL of eob-doll'),
 ('SyMBA float changeover','lab/board.md',    r'SyMBA changeover at a fixed base step is KILLED'),
 ('TRACE',                 'lab/board.md',    r'TRACE is dead'),
 ('kick jet',              'lab/board.md',    r'the jet is retired'),
 ('exact memo lever',      'lab/board.md',    r'the exact memo hits 0%'),
 ('q-secular phasors',     'lab/board.md',    r'zero-kick secular phasors .* are killed'),
 ('encounter-setup deferral','lab/board.md',  r'deferring encounter setup is killed'),
 ('pairwise tier (fleets)','lab/board.md',    r'co-orbital concentration breaks the pairwise candidate tier'),
 ('Wide tightening',       'lab/board.md',    r'drop the "Wide" tightening'),
 ('B12 candidates (14)',   'lab/wiki/b12-statistic.md', r'fourteen candidates dead'),
 ('one-word readout',      'lab/wiki/a-word.md', r'no one-word per-window'),
 ('static memo (B16)',     'lab/board.md',    r'Moving lenses'),
 ('faction thresholds',    'lab/board.md',    r'binary thresholds make faction aggregates'),
 ('binary doll (plane)',   'docs/HISTORY.md', r'the binary doll was killed'),
 ('continuum geodesics as law', 'docs/HISTORY.md', r'exact-floor definition retired to oracle'),
 ('frame tier',            'lab/wiki/nladder.md', r'frame tier deleted'),
 ('metronome cadence',     'docs/HANDOFF.md', r'a per-body clock is still a metronome'),
]
addbacks = [
 ('rotating binary doll (family revived)', 'lab/board.md', r'rotating binary doll'),
 ('two-word completion (in flight)',       'lab/wiki/a-word.md', r'two-word'),
 ('cast exception (anticipated)',          'lab/wiki/nladder.md', r'one kept exception for the cast'),
 ('chronon as test judge (scope-reduced)', 'docs/HANDOFF.md',   r'chronon survives only as a test judge'),
 ('JANUS integer changeover (family revived)', 'lab/board.md', r'bit-reversible \(JANUS\)'),
]
def grep1(f, pat):
    try:
        out = subprocess.run(['grep','-cE',pat,f],capture_output=True,text=True)
        return int(out.stdout.strip() or 0)
    except Exception: return 0
k_ok = 0
for n,f,p in kills:
    c = grep1(f,p); k_ok += (c>0)
    print(f'{"OK " if c else "MISS"} {c:>2} {f}: {n}')
a_ok = 0
for n,f,p in addbacks:
    c = grep1(f,p); a_ok += (c>0)
    print(f'{"OK " if c else "MISS"} {c:>2} {f}: ADD-BACK {n}')
print(f'KILLS={k_ok}/{len(kills)}  LANDED+IN-FLIGHT ADD-BACKS={a_ok}/{len(addbacks)}  ratio={a_ok/max(k_ok,1):.0%}')

print('== 4. automation-debt sites on shipped code ==')
sites = [
 ('radial.rs caps declared',   'crates/universe/src/radial.rs', r'speed_cap: f64'),
 ('radial.rs caps maintained (monotone max)', 'crates/universe/src/radial.rs', r'speed_cap = idx\.speed_cap\.max'),
 ('radial.rs caps consumed (window widened)', 'crates/universe/src/radial.rs', r'\(w\.v \+ idx\.speed_cap\)'),
 ('radial.rs density rule',    'crates/universe/src/radial.rs', r'bodies / 4 \+ 64'),
 ('encounter.rs walk-all fallback', 'crates/universe/src/encounter.rs', r'0\.\.ctx\.bodies\.len\(\)'),
 ('radial.rs hull-of-history widening', 'crates/universe/src/radial.rs', r'old\.lo\.min\(blo\)'),
]
for n,f,p in sites:
    print(f'{"OK " if grep1(f,p) else "MISS"}  {f}: {n}')

print('== 5. lookup budget (b29a recompile vs frame budget) ==')
recompile_p50_us, recompile_p95_us = 38.0, 78.0     # b29a composed event
standing_b_per_body, entry_deletes_b = 1806.0, 520.0 # 0e37; ~800 footprint
frame_ms = 1000.0/30.0
cap_p50 = frame_ms*1000/recompile_p50_us; cap_p95 = frame_ms*1000/recompile_p95_us
belt_reads_per_s, cast_reads_per_s = 0.0, 1.4       # 0e37: belt 0 in flight; cast 1.4/game-s
print(f'frame budget {frame_ms:.1f} ms -> recompile capacity/frame: p50 {cap_p50:.0f}, p95 {cap_p95:.0f}')
print(f'capacity/s at 30 fps: {cap_p95*30:,.0f} (p95); measured demand/s: belt {belt_reads_per_s}, cast {cast_reads_per_s}')
print(f'headroom at p95: {cap_p95*30/max(cast_reads_per_s,1e-9):.0f}x over the cast, unbounded over the belt')
print(f'standing bytes deleted per body (accounted): {entry_deletes_b:.0f} of {standing_b_per_body:.0f}; two-word add-back +24 B = {24/entry_deletes_b:.1%} of the deletion')
