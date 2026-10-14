#!/usr/bin/env python3
"""Insert the digest print (run 5903's certificate cut) into nladder.rs, after the
`let per = ...` line, if not already present. Idempotent; the anchor line is unique."""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "crates/universe/examples/nladder.rs"
src = open(path).read()
if "digest {} at {}" in src or "p.u.digest()" in src:
    print("digest line already present")
    sys.exit(0)
anchor = "    let per = |x: u64| if game_s > 0.0 { x as f64 / bodies as f64 / game_s } else { 0.0 };\n"
assert src.count(anchor) == 1, "anchor not found exactly once"
block = anchor + """    // The certificate cut (lab run 20261014-2012-...-5903): settle to the flight's last presented tick and
    // print the universe's digest — schedule-independent by construction, so it is the same for any build
    // whose candidate sets differ only inside the exact predicate's coverage.
    let cut = p.u.now;
    p.u.settle(cut);
    println!("digest {} at {} (contacts {}, logged {})", p.u.digest(), cut, p.u.contacts, p.u.enc_log.len());
"""
open(path, "w").write(src.replace(anchor, block))
print("digest line inserted")
