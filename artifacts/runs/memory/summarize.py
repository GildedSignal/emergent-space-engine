#!/usr/bin/env python3
"""Compute the frozen marginal physical footprint; truncated runs are never passes."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent

def parse(path):
    text = path.read_text()
    ladder = next((l for l in text.splitlines() if l.startswith('ladder:')), None)
    memory = next((l for l in text.splitlines() if l.startswith('memory: n=')), None)
    if not ladder or not memory:
        return {'file': str(path.relative_to(root)), 'complete': False}
    fields = dict(re.findall(r'(\w+)=([^\s]+)', ladder + ' ' + memory))
    behind = re.search(r'frames behind: (\d+)', text)
    exit_code = re.search(r'runner: exit=(\d+)', text)
    fields['frames_behind'] = int(behind[1]) if behind else None
    fields['runner_exit'] = int(exit_code[1]) if exit_code else None
    fields['file'] = str(path.relative_to(root))
    fields['complete'] = fields['runner_exit'] == 0 and fields['truncated'] == 'false' and int(fields['frames']) in (1200, 12000)
    fields['strict_frame_gate'] = fields['complete'] and fields['frames_behind'] == 0 and int(fields['over']) == 0 and float(fields['lag_s']) == 0 and int(fields['refusals']) == 0
    return fields

result = {}
for phase in ['before', 'after']:
    rows = {}
    for path in sorted((root / phase).glob('n*_*.txt')):
        rows[path.stem] = parse(path)
    for name, row in rows.items():
        if 'end_peak' not in row or not int(row['n']):
            continue
        suffix = name.split('_', 1)[1]
        base = rows.get('n0_' + suffix, {})
        if 'end_peak' in base:
            row['marginal_peak_B_per_body'] = (int(row['end_peak']) - int(base['end_peak'])) / int(row['n'])
            row['marginal_birth_B_per_body'] = (int(row['build_peak']) - int(base['build_peak'])) / int(row['n'])
            row['marginal_note'] = 'full nominal flight' if row['complete'] and base['complete'] else 'INCOMPLETE; not the frozen 200 s measure'
    result[phase] = rows
(root / 'measurements.json').write_text(json.dumps(result, indent=2) + '\n')
for phase, rows in result.items():
    for name, row in rows.items():
        if row.get('n') in ('100000', '1000000'):
            print(phase, name, 'B/body', row.get('marginal_peak_B_per_body'),
                  'complete', row['complete'], 'N1' if name.endswith('20') else 'wave',
                  row.get('strict_frame_gate'), 'max_ms', row.get('max_ms'), 'lag', row.get('lag_s'))
