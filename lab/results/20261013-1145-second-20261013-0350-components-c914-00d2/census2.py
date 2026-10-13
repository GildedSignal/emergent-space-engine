#!/usr/bin/env python3
"""Executed-mnemonic census for the arm64 div bench (run 00d2, second author).

Difference-based: traces ROUNDS=N and ROUNDS=2N under `qemu -singlestep -d exec`,
subtracts the per-PC histograms (removes startup AND the post-loop exactness
sweep, both of which are ROUNDS-independent), rebases PCs to static vaddrs via
the trace bracket's second field, and disassembles with capstone.

Usage: census2.py <binary> <label> [qemu]"""
import collections, os, subprocess, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

binary, label = sys.argv[1], sys.argv[2]
qemu = sys.argv[3] if len(sys.argv) > 3 else "/tmp/qemu-aarch64-static"
N = 12
DIVS = N * 4096

def hist(mode, rounds):
    env = dict(os.environ, ROUNDS=str(rounds))
    p = subprocess.run(
        [qemu, "-singlestep", "-d", "exec", "-D", "/dev/stdout", binary, mode],
        capture_output=True, text=True, env=env)
    h = collections.Counter()
    for line in p.stdout.splitlines():
        if not line.startswith("Trace "):
            continue
        try:
            brk = line.split("[", 1)[1].split("]")[0]
            pc = int(brk.split("/")[1], 16)
        except (IndexError, ValueError):
            continue
        h[pc] += 1
    return h

ph = subprocess.run(["readelf", "-lW", binary], capture_output=True, text=True).stdout
loads = []
for l in ph.splitlines():
    p = l.split()
    if p and p[0] == "LOAD":
        loads.append((int(p[2], 16), int(p[1], 16), int(p[4], 16)))
f = open(binary, "rb").read()
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
cache = {}

def disasm(addr):
    if addr in cache:
        return cache[addr]
    r = "<unmapped>"
    for vaddr, foff, fsz in loads:
        if vaddr <= addr < vaddr + fsz:
            for ins in md.disasm(f[foff + addr - vaddr : foff + addr - vaddr + 4], addr):
                r = ins.mnemonic
            break
    cache[addr] = r
    return r

mn = collections.Counter()
total = 0
for mode in [label]:
    h12, h24 = hist(mode, N), hist(mode, 2 * N)
    for pc, n in h24.items():
        d = n - h12.get(pc, 0)
        if d > 0:
            mn[disasm(pc)] += d
            total += d
print(f"  census[{label}] {total} guest insns / {DIVS} divs = {total/DIVS:.1f}/div")
for m, n in mn.most_common(14):
    if n / DIVS < 0.1:
        break
    print(f"    {m:10s} {n:9d}  {n/DIVS:7.2f}/div")
