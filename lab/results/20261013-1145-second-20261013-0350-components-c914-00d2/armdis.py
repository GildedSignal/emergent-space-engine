#!/usr/bin/env python3
"""aarch64 ELF disassembler via capstone: `dis.py <binary> <symbol-or-addr> [max_bytes]`.
Used to read __udivti3 / div_newton on the cross-built arm64 bench."""
import subprocess, sys
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN

binary, target = sys.argv[1], sys.argv[2]
maxb = int(sys.argv[3]) if len(sys.argv) > 3 else 256
out = subprocess.run(["readelf", "-sW", binary], capture_output=True, text=True).stdout
addr, size = None, maxb
for line in out.splitlines():
    p = line.split()
    if len(p) >= 8 and (p[7] == target or p[7].endswith("::" + target) or target in p[7].split(".")[-1:]):
        addr, size = int(p[1], 16), int(p[2], 16)
        break
if addr is None:
    addr = int(target, 16)
ph = subprocess.run(["readelf", "-lW", binary], capture_output=True, text=True).stdout
off = None
for l in ph.splitlines():
    p = l.split()
    if p and p[0] == "LOAD":
        vaddr, foff, fsz = int(p[2], 16), int(p[1], 16), int(p[4], 16)
        if vaddr <= addr < vaddr + fsz:
            off = foff + (addr - vaddr)
if off is None:
    sys.exit("address not in any LOAD")
f = open(binary, "rb").read()
md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
n = 0
for ins in md.disasm(f[off : off + min(size, maxb)], addr):
    print(f"0x{ins.address:x}:\t{ins.mnemonic}\t{ins.op_str}")
    n += 1
print(f"-- {n} instructions", file=sys.stderr)
