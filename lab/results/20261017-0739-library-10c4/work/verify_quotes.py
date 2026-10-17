#!/usr/bin/env python3
"""Verify every dossier quote is byte-identical to a highlight in the cache."""
import json, sys

rows = [json.loads(l) for l in open('highlights.jsonl')]
QUOTES = {
    'L1 Musk-delete': ('Step one should be to question the requirements',
                       'And then delete, delete, delete', 'Elon Musk'),
    'L2 Musk-automate': ('Always wait until the end of designing a process',
                         'before you introduce automation', 'Elon Musk'),
    'L3 Asimov-masses': ('Psychohistory dealt not with man, but man-masses',
                         'the reaction of a billion is something else again', 'Foundation and Empire'),
    'L4 Asimov-laws': ('The laws of history are as absolute as the laws of physics',
                       'individual variations count for more', 'Foundation and Empire'),
    'L5 TOC': ('will never grow beyond its biggest constraint or bottleneck',
               'The Theory of Constraints', 'Anthony Vicino'),
}
fail = 0
for k, (q1, q2, book) in QUOTES.items():
    hits = [x for x in rows if q1 in x['t'] and q2 in x['t'] and book in x['b'] + x['a']]
    print(('OK  ' if hits else 'MISS'), k, '->', f'{book} | {hits[0]["b"][:40]}' if hits else '')
    fail += not hits
sys.exit(1 if fail else 0)
