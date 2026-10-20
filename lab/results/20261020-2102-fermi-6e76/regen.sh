#!/bin/sh
# Regenerates every dossier number from a clean tree: applies this run's patch (8994/5f76's
# alloc_scope instrument + the new alloc_bt backtrace namer + the radial with_capacity fix),
# builds, flies the arms, and prints the analysis. ~2 min warm; each process < 150 MB RSS.
set -e
D=$(dirname "$0")
while [ "$D" != / ] && [ ! -f "$D/Cargo.toml" ]; do D=$D/..; done
cd "$D" || exit 1
[ -f Cargo.toml ] || { echo "FATAL: repo root not found" >&2; exit 1; }
R=lab/results/20261020-2102-fermi-6e76
if git apply --check "$R/work/patch.diff" 2>/dev/null; then
  git apply "$R/work/patch.diff"
elif [ -f crates/universe/examples/alloc_bt.rs ]; then
  echo "patch already applied; continuing"
else
  echo "FATAL: patch neither applies nor is applied" >&2; exit 1
fi
mkdir -p /tmp/fermi6e76
cargo build --release -p emergent-universe --example alloc_scope --example alloc_bt 2>&1 | tail -1
B=$(cargo metadata --format-version 1 --no-deps 2>/dev/null | tr ',' '\n' | grep -o '"target_directory":"[^"]*"' | cut -d'"' -f4)/release/examples

echo "=== [1] shipped anchors (A1: coast K=1e4, rtf 2000, 12 ms, 30 s) — expect 11.35 KB/kick, base ~2.06 KB/game-s, player term ~193.4 KB/item, ladder top 57,344 exactly"
# The patch carries the radial fix too: park it, revert radial to shipped, rebuild, measure SHIPPED.
cp crates/universe/src/radial.rs /tmp/fermi6e76/radial-fixed.rs
git checkout -- crates/universe/src/radial.rs
cargo build --release -p emergent-universe --example alloc_scope --example alloc_bt 2>&1 | tail -1
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/fermi6e76/A1.csv timeout 120 "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/fermi6e76/A1.log 2>&1
grep -E "alloc_scope: N=|per fired kick" /tmp/fermi6e76/A1.log
grep " player" /tmp/fermi6e76/A1.log | head -2
python3 -c "
import re
t = open('/tmp/fermi6e76/A1.log').read()
b = int(re.search(r'scope\s+player \(4\): allocs \d+, bytes (\d+)', t).group(1))
rb = int(re.search(r'scope\s+player \(4\): realloc bytes (\d+)', t).group(1))
items = int(re.search(r'items=\[\d+, \d+, \d+, (\d+), \d+\]', t).group(1))
print(f'A1 player term: {(b+rb)/items/1e3:.1f} KB/item over {items} items')"
grep -A22 "size census" /tmp/fermi6e76/A1.log | grep player

echo "=== [2] naming arm (bt-coast: backtrace sites + exact scope-4 size census, 10 s)"
ES_ALLOC_SCOPE=1 ES_BT_EVERY=16 timeout 120 "$B/alloc_bt" 10000 coast 10 2000 12 > /tmp/fermi6e76/bt-coast.log 2>/dev/null
grep -E "alloc_bt: N=|player term" /tmp/fermi6e76/bt-coast.log
sed -n '/exact scope-4/,/site census/p' /tmp/fermi6e76/bt-coast.log
sed -n '/site census/,$p' /tmp/fermi6e76/bt-coast.log | head -22

echo "=== [3] micro-test: the ids ladder sizes are clone+extend (reserve-exact), not doubling; sort_unstable is alloc-free"
mkdir -p /tmp/sorttest
cat > /tmp/sorttest/main.rs <<'EOF'
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};
static LOG: [AtomicUsize; 64] = [const { AtomicUsize::new(0) }; 64];
static I: AtomicUsize = AtomicUsize::new(0);
struct A;
unsafe impl GlobalAlloc for A {
    unsafe fn alloc(&self, l: Layout) -> *mut u8 { let p = System.alloc(l); if l.size() >= 1024 { let i = I.fetch_add(1, Ordering::Relaxed); if i < 64 { LOG[i].store(0x8000_0000 | l.size(), Ordering::Relaxed); } } p }
    unsafe fn dealloc(&self, p: *mut u8, l: Layout) { System.dealloc(p, l) }
    unsafe fn realloc(&self, p: *mut u8, l: Layout, n: usize) -> *mut u8 { let q = System.realloc(p, l, n); if n >= 1024 { let i = I.fetch_add(1, Ordering::Relaxed); if i < 64 { LOG[i].store(n, Ordering::Relaxed); } } q }
}
#[global_allocator]
static G: A = A;
fn dump(tag: &str) { eprintln!("{tag}:"); for c in LOG.iter() { let v = c.load(Ordering::Relaxed); if v != 0 { eprintln!("  {}", if v & 0x8000_0000 != 0 { format!("a {}", v & 0x7fff_ffff) } else { format!("r {v}") }); } } }
fn main() {
    let mode: u8 = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(0);
    let base: Vec<u32> = (0..600).map(|i| (i * 37) % 9_001).collect();
    let bin1: Vec<u32> = (0..768).map(|i| (i * 91) % 9_001).collect();
    let bin2: Vec<u32> = (0..1536).map(|i| (i * 53) % 9_001).collect();
    if mode == 0 {
        let mut ids = base.clone();
        ids.extend_from_slice(&bin1);
        ids.extend_from_slice(&bin2);
        std::hint::black_box(&ids);
        dump("extend-only");
    } else {
        let mut ids = base.clone();
        ids.extend_from_slice(&bin1);
        ids.extend_from_slice(&bin2);
        ids.sort_unstable();
        ids.dedup();
        std::hint::black_box(&ids);
        dump("with-sort");
    }
}
EOF
rustc -O /tmp/sorttest/main.rs -o /tmp/sorttest/st
/tmp/sorttest/st 0 2>&1 | tail -8
/tmp/sorttest/st 1 2>&1 | tail -8

echo "=== [4] the fix arm (A1fix: same flight, radial with_capacity(hit+unbounded)) — expect player term ~180 KB/item, reallocs ~-11%, family B (2,560/5,632/11,776 r) gone from the census"
cp /tmp/fermi6e76/radial-fixed.rs crates/universe/src/radial.rs
cargo build --release -p emergent-universe --example alloc_scope 2>&1 | tail -1
ES_ALLOC_SCOPE=1 ES_ALLOC_CSV=/tmp/fermi6e76/A1fix.csv timeout 120 "$B/alloc_scope" 10000 coast 30 2000 12 > /tmp/fermi6e76/A1fix.log 2>&1
grep -E "alloc_scope: N=|per fired kick" /tmp/fermi6e76/A1fix.log
python3 -c "
import re
t = open('/tmp/fermi6e76/A1fix.log').read()
b = int(re.search(r'scope\s+player \(4\): allocs \d+, bytes (\d+)', t).group(1))
rb = int(re.search(r'scope\s+player \(4\): realloc bytes (\d+)', t).group(1))
r = int(re.search(r'scope\s+player \(4\): allocs \d+, bytes \d+ \([\d.]+ KB\), frees \d+, freed [\d.]+ KB, reallocs (\d+)', t).group(1))
items = int(re.search(r'items=\[\d+, \d+, \d+, (\d+), \d+\]', t).group(1))
print(f'A1fix player term: {(b+rb)/items/1e3:.1f} KB/item over {items} items, reallocs {r}')"
grep -A22 "size census" /tmp/fermi6e76/A1fix.log | grep player
echo "=== compare with dossier.md's four blocks"
