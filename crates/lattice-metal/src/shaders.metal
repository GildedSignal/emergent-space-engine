// The GPU half of MetalChronon. One chronon = kmax, plan, [clear, bin: only when the cell
// side changed], scan_reduce, scan_sums, scan_final, scatter (the snapshot), pairs
// (detection), advance (wall set, and binning for the next chronon), then the response:
// tally, classify, resolve_pair (isolated contacts), listargs, hook × HOOKS, mark, resolve
// (larger components), unmark; every 64 chronons, prune. Many chronons share one command
// buffer; the CPU is needed only when a chronon holds a component the GPU may not resolve
// exactly: that chronon sets `halt` and the later ones do nothing.
//
// Every value is an exact integer. `plan` checks C·(K + 1) ≤ 2^28 (every detection product
// below 2^62, every narrowed field in range); gpu.rs checks that cell coordinates fit i32.
#include <metal_stdlib>
using namespace metal;

// Mirrors `Params` in gpu.rs. Scalar longs: a long2 would align to 16 and shift the layout.
struct Params {
    long reach;  // reach_max = 2·max radius
    long bmin_x, bmin_y, bmax_x, bmax_y;
    uint n, wbits, hmask, has_box, pair_cap, nblocks;
    uint resolve;  // resolve contacts here (Newtonian law, no CPU-side consumed filter)
    uint log_cap;
    uint step;  // chronon index in this command buffer
    uint pad;
};

constant uint HALT_CPU = 1, HALT_PAIRS = 2, HALT_P1 = 3;

struct Ctl {
    atomic_uint npairs;  // this chronon's hits and wall-set bodies
    atomic_uint nwalls;
    uint go;             // this chronon runs
    uint done;           // chronons of this buffer that ran
    uint halt;           // HALT_*: the CPU must act before the next chronon
    atomic_uint nlog;    // events in the log
    long cell;           // this chronon's cell side
    atomic_uint nlist;   // events of larger components (the general response's list)
    uint pad;
    long bincell;        // `count` and `bins` hold the bodies binned with this cell (0: none)
};

// Per chronon of a buffer, read by the CPU.
struct Step {
    atomic_uint pred_lo, pred_hi;  // predicate count (64-bit with carry)
    atomic_uint inv;               // distinct bodies in the batch
    atomic_uint kmax;              // max |k_c| over bodies
    uint np, nw;                   // hits and wall-set bodies
    uint log_start;
    uint pad;
};

// A logged event: contact (body indices a < b) or wall (b = EMPTY, momentum given to the
// walls). a = EMPTY marks a reserved slot left unused.
struct Ev {
    uint a, b;
    long wx, wy;
};

// A body's response state in one 32-byte record (the response touches bodies at random, so
// one cache line per body instead of four).
struct Dyn {
    long2 k;         // velocity
    long res;        // energy carry
    uint rev;
    atomic_uint cnt; // events of this chronon's batch the body is in (zero between chronons)
};

// A body's cell and its rank among the bodies binned into the same bucket.
struct Bin {
    packed_int2 c;
    uint rank;
};

// Detection snapshot at t-1 in bucket order (32 bytes: record size dominates the scan).
// Position relative to its cell's corner (in [0, C), C ≤ 2^28), velocity |k_c| ≤ K < 2^14:
// exact when narrowed.
struct Rec {
    int2 c;
    uint idx, mask;  // mask: bit j & 31 set if the table may hold a contact (idx, j)
    uint2 xr;
    short2 k;
    uint rf;  // radius | stop << 30 | bouncer << 31
};

// rf: radius (exact in 28 bits whenever the GPU path runs: radius ≤ C/2 ≤ 2^27) | flags.
constant uint RADIUS = 0x0fffffffu;
constant uint STOP = 1u << 30;
constant uint BOUNCE = 1u << 31;

// A consumed contact (lower index owns it): partner, own revision, partner revision.
struct Slot {
    uint j, ri, rj;
};

constant uint EMPTY = 0xffffffffu;
constant uint SLOTS = 8;
constant uint BLOCK = 1024;  // buckets per scan threadgroup (256 threads × 4)
constant uint ADJ = 4;       // events per body the GPU response follows
constant uint MAXB = 8;      // bodies per component the GPU resolves
constant uint MAXP = 8;      // contacts per component the GPU resolves
constant uint FOR_CPU = 1;

// floor(x / c) for c ≥ 1, as the law's div_euclid. 64-bit `/` is emulated and slow, so
// float quotients shrink the remainder (each by ~2^22) and integer steps finish;
// q·c + r = x holds throughout, so the result is exact.
static inline long fdiv(long x, long c) {
    float fc = float(c);
    long q = 0, r = x;
    while (abs(r) >= 4 * c) {
        long dq = long(floor(float(r) / fc));
        q += dq;
        r -= dq * c;
    }
    while (r < 0) { q -= 1; r += c; }
    while (r >= c) { q += 1; r -= c; }
    return q;
}

// Buckets tile the plane as a 2^wbits × (H >> wbits) torus: neighbouring cells are
// neighbouring buckets, so bucket order is spatial order and the three cells of a row are
// usually three consecutive buckets. Aliased cells share a bucket and are told apart by
// their exact coordinates.
static inline uint bucket(int2 c, constant Params& p) {
    return (uint(c.x) & ((1u << p.wbits) - 1)) | ((uint(c.y) << p.wbits) & p.hmask);
}

// law::hit, branch for branch, on |d_c| < 2^29, |w_c| < 2^15, reach ≤ 2^28.
static inline bool hit(int2 d, int2 w, uint reach) {
    long dd = long(d.x) * d.x + long(d.y) * d.y;
    long dw = long(d.x) * w.x + long(d.y) * w.y;
    long ww = long(w.x) * w.x + long(w.y) * w.y;
    long rr = long(reach) * reach;
    if (dd <= rr) return dw < 0;
    if (ww == 0 || dw >= 0) return false;
    if (-dw >= ww) {
        int2 e = d + w;
        return long(e.x) * e.x + long(e.y) * e.y <= rr;
    }
    long cross = long(d.x) * w.y - long(d.y) * w.x;
    return cross * cross <= rr * ww;
}

// ---- Plan ----------------------------------------------------------------------------------

// max|k_c| over bodies (kq saturates at ±32767, so a fast body fails the plan's check).
kernel void kmax(device Ctl* ctl [[buffer(4)]],
                 constant Params& p [[buffer(5)]],
                 device const short2* kq [[buffer(7)]],
                 device Step* steps [[buffer(25)]],
                 threadgroup uint* sh [[threadgroup(0)]],
                 uint i [[thread_position_in_grid]],
                 uint t [[thread_position_in_threadgroup]],
                 uint lane [[thread_index_in_simdgroup]],
                 uint sg [[simdgroup_index_in_threadgroup]],
                 uint nsg [[simdgroups_per_threadgroup]]) {
    uint v = 0;
    if (i < p.n && ctl->halt == 0) {
        int2 k = int2(kq[i]);
        v = uint(max(abs(k.x), abs(k.y)));
    }
    v = simd_max(v);
    if (lane == 0) sh[sg] = v;
    threadgroup_barrier(mem_flags::mem_threadgroup);
    if (t == 0) {
        uint m = 0;
        for (uint g = 0; g < nsg; ++g) m = max(m, sh[g]);
        if (m != 0) atomic_fetch_max_explicit(&steps[p.step].kmax, m, memory_order_relaxed);
    }
}

// The reference's cell side for this chronon and the precondition that keeps it exact.
// The previous advance already binned the bodies with its cell; bin again (after clearing
// the counts) only when the cell side changed.
kernel void plan(device Ctl* ctl [[buffer(4)]],
                 constant Params& p [[buffer(5)]],
                 device uint* args [[buffer(23)]],
                 device Step* steps [[buffer(25)]]) {
    args[9] = 0; args[10] = 1; args[11] = 1;
    args[12] = 0; args[13] = 1; args[14] = 1;
    if (ctl->halt != 0) {
        ctl->go = 0;
        return;
    }
    long k = atomic_load_explicit(&steps[p.step].kmax, memory_order_relaxed);
    long cell = max(p.reach + 2 * k, 1l);
    if (cell * (k + 1) > (1l << 28)) {
        ctl->halt = HALT_P1;
        ctl->go = 0;
        return;
    }
    if (ctl->bincell != cell) {
        args[9] = (p.n + 255) / 256;
        args[12] = (p.hmask + 1) / 4 / 256;
    }
    ctl->bincell = cell;  // what advance will bin with
    ctl->cell = cell;
    ctl->go = 1;
    ctl->done = p.step + 1;
    atomic_store_explicit(&ctl->npairs, 0u, memory_order_relaxed);
    atomic_store_explicit(&ctl->nwalls, 0u, memory_order_relaxed);
    atomic_store_explicit(&ctl->nlist, 0u, memory_order_relaxed);
    steps[p.step].log_start = atomic_load_explicit(&ctl->nlog, memory_order_relaxed);
}

// ---- Snapshot ------------------------------------------------------------------------------

static inline void bin_one(long2 x, uint i, long cell, device atomic_uint* count, device Bin* bins, constant Params& p) {
    int2 c = int2(fdiv(x.x, cell), fdiv(x.y, cell));
    Bin b;
    b.c = c;
    b.rank = atomic_fetch_add_explicit(&count[bucket(c, p)], 1u, memory_order_relaxed);
    bins[i] = b;
}

kernel void clear(device uint4* count [[buffer(1)]],
                  uint i [[thread_position_in_grid]]) {
    count[i] = uint4(0);
}

kernel void bin(device const long2* pos [[buffer(0)]],
                device atomic_uint* count [[buffer(1)]],
                device Bin* bins [[buffer(2)]],
                device Ctl* ctl [[buffer(4)]],
                constant Params& p [[buffer(5)]],
                uint i [[thread_position_in_grid]]) {
    if (i >= p.n) return;
    bin_one(pos[i], i, ctl->cell, count, bins, p);
}

// Bucket starts by reduce-then-scan: block totals, their exclusive scan, then each block's
// local scan plus its offset. 256 threads × 4 buckets per block.
kernel void scan_reduce(device const uint4* count [[buffer(1)]],
                        device Ctl* ctl [[buffer(4)]],
                        device uint* bsum [[buffer(16)]],
                        threadgroup uint* sh [[threadgroup(0)]],
                        uint t [[thread_position_in_threadgroup]],
                        uint g [[threadgroup_position_in_grid]],
                        uint lane [[thread_index_in_simdgroup]],
                        uint sg [[simdgroup_index_in_threadgroup]]) {
    if (ctl->go == 0) return;
    uint4 v = count[g * (BLOCK / 4) + t];
    uint tot = simd_sum(v.x + v.y + v.z + v.w);
    if (lane == 0) sh[sg] = tot;
    threadgroup_barrier(mem_flags::mem_threadgroup);
    if (t == 0) {
        uint s = 0;
        for (uint k = 0; k < 8; ++k) s += sh[k];
        bsum[g] = s;
    }
}

// One threadgroup; each thread a contiguous run of blocks. Closes the last bucket.
kernel void scan_sums(device Ctl* ctl [[buffer(4)]],
                      constant Params& p [[buffer(5)]],
                      device uint* start [[buffer(6)]],
                      device const uint* bsum [[buffer(16)]],
                      device uint* boff [[buffer(17)]],
                      threadgroup uint* sh [[threadgroup(0)]],
                      uint t [[thread_position_in_threadgroup]],
                      uint T [[threads_per_threadgroup]],
                      uint lane [[thread_index_in_simdgroup]],
                      uint sg [[simdgroup_index_in_threadgroup]],
                      uint nsg [[simdgroups_per_threadgroup]]) {
    if (ctl->go == 0) return;
    uint G = p.nblocks, per = (G + T - 1) / T;
    uint lo = min(t * per, G), hi = min(lo + per, G);
    uint s = 0;
    for (uint b = lo; b < hi; ++b) s += bsum[b];
    uint pre = simd_prefix_exclusive_sum(s);
    uint tot = simd_sum(s);
    if (lane == 0) sh[sg] = tot;
    threadgroup_barrier(mem_flags::mem_threadgroup);
    if (sg == 0) {
        uint x = lane < nsg ? sh[lane] : 0;
        uint e = simd_prefix_exclusive_sum(x);
        if (lane < nsg) sh[lane] = e;
    }
    threadgroup_barrier(mem_flags::mem_threadgroup);
    uint acc = sh[sg] + pre;
    for (uint b = lo; b < hi; ++b) {
        boff[b] = acc;
        acc += bsum[b];
    }
    if (t == T - 1) start[p.hmask + 1] = acc;
}

// Absolute bucket starts; zeroes the counts for the next chronon.
kernel void scan_final(device uint4* count [[buffer(1)]],
                       device Ctl* ctl [[buffer(4)]],
                       device uint4* start [[buffer(6)]],
                       device const uint* boff [[buffer(17)]],
                       threadgroup uint* sh [[threadgroup(0)]],
                       uint t [[thread_position_in_threadgroup]],
                       uint g [[threadgroup_position_in_grid]],
                       uint lane [[thread_index_in_simdgroup]],
                       uint sg [[simdgroup_index_in_threadgroup]]) {
    if (ctl->go == 0) return;
    uint i = g * (BLOCK / 4) + t;
    uint4 v = count[i];
    uint s = v.x + v.y + v.z + v.w;
    uint pre = simd_prefix_exclusive_sum(s);
    uint tot = simd_sum(s);
    if (lane == 0) sh[sg] = tot;
    threadgroup_barrier(mem_flags::mem_threadgroup);
    if (sg == 0) {
        uint x = lane < 8 ? sh[lane] : 0;
        uint e = simd_prefix_exclusive_sum(x);
        if (lane < 8) sh[lane] = e;
    }
    threadgroup_barrier(mem_flags::mem_threadgroup);
    uint a = boff[g] + sh[sg] + pre;
    start[i] = uint4(a, a + v.x, a + v.x + v.y, a + v.x + v.y + v.z);
    count[i] = uint4(0);
}

kernel void scatter(device const long2* pos [[buffer(0)]],
                    device const Bin* bins [[buffer(2)]],
                    device Ctl* ctl [[buffer(4)]],
                    constant Params& p [[buffer(5)]],
                    device const uint* start [[buffer(6)]],
                    device const short2* kq [[buffer(7)]],
                    device const uint* rf [[buffer(8)]],
                    device Rec* recs [[buffer(11)]],
                    device const uint* mask [[buffer(18)]],
                    uint i [[thread_position_in_grid]]) {
    if (i >= p.n || ctl->go == 0) return;
    Bin q = bins[i];
    int2 c = int2(q.c);
    Rec rec;
    rec.c = c;
    rec.idx = i;
    rec.mask = mask[i];
    rec.xr = uint2(pos[i] - long2(c) * ctl->cell);
    rec.k = kq[i];
    rec.rf = rf[i];
    recs[start[bucket(c, p)] + q.rank] = rec;
}

// ---- Detection -----------------------------------------------------------------------------

constant uint TGHITS = 256;  // hits a threadgroup buffers before appending them at once

// A candidate that passed the box filter: reject it in float when the float values prove
// it cannot hit (not approaching, or its line of motion stays beyond reach), else run the
// exact predicate. Float products of |d_c| < 2^29 and |w_c| < 2^15 carry a relative error
// below 2^-22, far inside the 2^-18 margins, so no hit is ever rejected. A hit goes to the
// threadgroup's buffer (one global atomic per threadgroup: a global one per hit serialises).
static inline void try_pair(int2 d, int2 w, uint reach, uint ia, uint ib, device Ctl* ctl, device uint2* out, uint cap,
                            threadgroup uint2* tgbuf, threadgroup atomic_uint* tgn) {
    float2 df = float2(d), wf = float2(w);
    float px = df.x * wf.x, py = df.y * wf.y;
    if (px + py > 0x1p-18f * (fabs(px) + fabs(py))) return;  // dw > 0
    float cx = df.x * wf.y, cy = df.y * wf.x;
    float cross = fabs(cx - cy) - 0x1p-18f * (fabs(cx) + fabs(cy));
    float rf = float(reach), ww = wf.x * wf.x + wf.y * wf.y;
    if (cross > 0 && cross * cross > rf * rf * ww * (1 + 0x1p-18f)) return;  // line beyond reach
    if (hit(d, w, reach)) {
        uint slot = atomic_fetch_add_explicit(tgn, 1u, memory_order_relaxed);
        if (slot < TGHITS) {
            tgbuf[slot] = uint2(ia, ib);
        } else {
            uint o = atomic_fetch_add_explicit(&ctl->npairs, 1u, memory_order_relaxed);
            if (o < cap) out[o] = uint2(ia, ib);
        }
    }
}

// One thread per record, in bucket (spatial) order: the pairs of the 3×3 reference cells,
// each met once (half neighbourhood below). Contacts consumed
// at the current revisions are skipped (the mask bit gates the table read); the rest count
// as predicates. A 32-bit necessary condition (|d_c| ≤ reach + |w_c|: the pair must come
// within reach during the bin) drops most of them, a float one most of the rest.
kernel void pairs(device Ctl* ctl [[buffer(4)]],
                  constant Params& p [[buffer(5)]],
                  device const uint* start [[buffer(6)]],
                  device Dyn* dy [[buffer(3)]],
                  device const Rec* recs [[buffer(11)]],
                  device const Slot* table [[buffer(13)]],
                  device uint2* out [[buffer(14)]],
                  device Step* steps [[buffer(25)]],
                  threadgroup uint* sh [[threadgroup(0)]],
                  uint s [[thread_position_in_grid]],
                  uint t [[thread_position_in_threadgroup]],
                  uint lane [[thread_index_in_simdgroup]],
                  uint sg [[simdgroup_index_in_threadgroup]],
                  uint nsg [[simdgroups_per_threadgroup]]) {
    threadgroup uint2 tgbuf[TGHITS];
    threadgroup atomic_uint tgn;
    threadgroup uint tgbase;
    if (t == 0) atomic_store_explicit(&tgn, 0u, memory_order_relaxed);
    threadgroup_barrier(mem_flags::mem_threadgroup);
    uint tested = 0;
    if (s < p.n && ctl->go != 0) {
        Rec a = recs[s];
        int C = int(ctl->cell);
        uint wmask = (1u << p.wbits) - 1;
        // Half the neighbourhood, so every adjacent pair is met once: a's own cell (partners
        // of higher index) and the forward cells (+1, 0), (-1, +1), (0, +1), (+1, +1). Row 0
        // spans cells x..x+1, row 1 cells x-1..x+1: consecutive buckets unless the torus wraps.
        for (uint row = 0; row < 2; ++row) {
            uint hx = (uint(a.c.x) - row) & wmask, width = 2 + row;
            bool whole = hx + width - 1 <= wmask;
            uint hrow = ((uint(a.c.y) + row) << p.wbits) & p.hmask;
            for (uint part = 0; part < (whole ? 1u : width); ++part) {
                uint h = hrow + (whole ? hx : ((hx + part) & wmask));
                for (uint u = start[h], e = start[h + (whole ? width : 1)]; u < e; ++u) {
                    device const Rec& b = recs[u];
                    // Exact adjacency, modulo 2^32 so aliased far cells cannot overflow.
                    int2 rel = int2(uint2(b.c) - uint2(a.c));
                    if (rel.y != int(row) || rel.x < -int(row) || rel.x > 1) continue;
                    if (row == 0 && rel.x == 0 && b.idx <= a.idx) continue;
                    // The pair in index order (lo < hi): its consumed contacts are in lo's row.
                    bool swap = b.idx < a.idx;
                    uint lo = swap ? b.idx : a.idx, hi = swap ? a.idx : b.idx;
                    if (((swap ? b.mask : a.mask) >> (hi & 31)) & 1) {
                        bool eaten = false;
                        uint rl = dy[lo].rev, rh = dy[hi].rev;
                        for (uint m = 0; m < SLOTS; ++m) {
                            Slot sl = table[lo * SLOTS + m];
                            eaten = eaten || (sl.j == hi && sl.ri == rl && sl.rj == rh);
                        }
                        if (eaten) continue;
                    }
                    ++tested;
                    int2 d = int2(b.xr) - int2(a.xr) + rel * C, w = int2(b.k) - int2(a.k);
                    uint reach = (a.rf & RADIUS) + (b.rf & RADIUS);
                    if (uint(abs(d.x)) > reach + uint(abs(w.x)) || uint(abs(d.y)) > reach + uint(abs(w.y))) continue;
                    // hit is symmetric under (d, w) → (−d, −w).
                    try_pair(swap ? -d : d, swap ? -w : w, reach, lo, hi, ctl, out, p.pair_cap, tgbuf, &tgn);
                }
            }
        }
    }
    // Predicate count as a 64-bit (lo, hi) pair with carry, and the buffered hits, one
    // atomic each per threadgroup.
    uint sum = simd_sum(tested);
    if (lane == 0) sh[sg] = sum;
    threadgroup_barrier(mem_flags::mem_threadgroup);
    uint k = min(atomic_load_explicit(&tgn, memory_order_relaxed), TGHITS);
    if (t == 0) {
        uint total = 0;
        for (uint g = 0; g < nsg; ++g) total += sh[g];
        if (total != 0) {
            uint old = atomic_fetch_add_explicit(&steps[p.step].pred_lo, total, memory_order_relaxed);
            if (old + total < old) atomic_fetch_add_explicit(&steps[p.step].pred_hi, 1u, memory_order_relaxed);
        }
        tgbase = k != 0 ? atomic_fetch_add_explicit(&ctl->npairs, k, memory_order_relaxed) : 0;
    }
    threadgroup_barrier(mem_flags::mem_threadgroup);
    for (uint h = t; h < k; h += 256) {
        if (tgbase + h < p.pair_cap) out[tgbase + h] = tgbuf[h];
    }
}

// Advance to t and collect the wall set there, in index order (coalesced), and bin the new
// positions for the next chronon (valid if its cell side is the same). Runs after `pairs`,
// which reads only the snapshot, and after scan_final zeroed the counts.
kernel void advance(device long2* pos [[buffer(0)]],
                    device atomic_uint* count [[buffer(1)]],
                    device Bin* bins [[buffer(2)]],
                    device Ctl* ctl [[buffer(4)]],
                    constant Params& p [[buffer(5)]],
                    device const short2* kq [[buffer(7)]],
                    device const uint* rf [[buffer(8)]],
                    device uint* walls [[buffer(12)]],
                    uint i [[thread_position_in_grid]]) {
    if (i >= p.n || ctl->go == 0) return;
    long2 k = long2(kq[i]), y = pos[i] + k;
    pos[i] = y;
    bin_one(y, i, ctl->cell, count, bins, p);
    uint f = rf[i];
    if (p.has_box != 0 && (f & BOUNCE) != 0) {
        long r = f & RADIUS;
        bool w = (k.x < 0 && y.x <= p.bmin_x + r) || (k.x > 0 && y.x >= p.bmax_x - r) ||
                 (k.y < 0 && y.y <= p.bmin_y + r) || (k.y > 0 && y.y >= p.bmax_y - r);
        if (w) walls[atomic_fetch_add_explicit(&ctl->nwalls, 1u, memory_order_relaxed)] = i;
    }
}

// ---- Response ------------------------------------------------------------------------------
// The batch splits into connected components (bodies linked by contacts; a wall-set body
// joins its own), and components resolve independently (law.rs). Each component is labelled
// by its smallest body index, then its leader applies law::resolve to it: contacts in index
// order, sequential impulses in i64 guarded against overflow, stops, walls. A component the
// GPU cannot follow or bound (too large, a label not converged, a guard, a full table row
// or log) is left whole to the CPU, which resolves it in i128.

// Indirect grid sizes: every event (hits then walls), then hits only.
kernel void tally(device Ctl* ctl [[buffer(4)]],
                  constant Params& p [[buffer(5)]],
                  device uint* args [[buffer(23)]],
                  device Step* steps [[buffer(25)]]) {
    uint np = atomic_load_explicit(&ctl->npairs, memory_order_relaxed);
    uint nw = atomic_load_explicit(&ctl->nwalls, memory_order_relaxed);
    uint ev = 0, hits = 0;
    if (ctl->go != 0) {
        steps[p.step].np = np;
        steps[p.step].nw = nw;
        if (np > p.pair_cap) {
            ctl->halt = HALT_PAIRS;  // detection truncated: the CPU reruns this chronon
        } else if (np + nw != 0 && p.resolve == 0) {
            ctl->halt = HALT_CPU;
        } else {
            ev = np + nw;
            hits = np;
        }
    }
    args[0] = (ev + 255) / 256; args[1] = 1; args[2] = 1;
    args[3] = (hits + 255) / 256; args[4] = 1; args[5] = 1;
}

// Grid size for the general response: the listed events.
kernel void listargs(device Ctl* ctl [[buffer(4)]],
                     device uint* args [[buffer(23)]]) {
    uint k = ctl->go != 0 ? atomic_load_explicit(&ctl->nlist, memory_order_relaxed) : 0;
    args[6] = (k + 255) / 256; args[7] = 1; args[8] = 1;
}

static inline uint bodies_of(uint e, device Ctl* ctl, device const uint2* out, device const uint* walls,
                             thread uint& a, thread uint& b) {
    uint np = atomic_load_explicit(&ctl->npairs, memory_order_relaxed);
    uint nw = atomic_load_explicit(&ctl->nwalls, memory_order_relaxed);
    if (e < np) { a = out[e].x; b = out[e].y; return 2; }
    if (e < np + nw) { a = walls[e - np]; b = a; return 1; }
    return 0;
}

static inline uint count_of(device Dyn* dy, uint x) {
    return atomic_load_explicit(&dy[x].cnt, memory_order_relaxed);
}

// Incidences per body (first ADJ recorded), distinct bodies, labels initialised to self.
kernel void classify(device Ctl* ctl [[buffer(4)]],
                     constant Params& p [[buffer(5)]],
                     device const uint* walls [[buffer(12)]],
                     device const uint2* out [[buffer(14)]],
                     device Dyn* dy [[buffer(3)]],
                     device atomic_uint* label [[buffer(24)]],
                     device Step* steps [[buffer(25)]],
                     device uint* adj [[buffer(26)]],
                     uint e [[thread_position_in_grid]]) {
    uint a = 0, b = 0, m = bodies_of(e, ctl, out, walls, a, b), first = 0;
    for (uint q = 0; q < m; ++q) {
        uint x = q == 0 ? a : b;
        uint slot = atomic_fetch_add_explicit(&dy[x].cnt, 1u, memory_order_relaxed);
        if (slot == 0) {
            atomic_store_explicit(&label[x], x, memory_order_relaxed);
            ++first;
        }
        if (slot < ADJ) adj[x * ADJ + slot] = e;
    }
    first = simd_sum(first);  // distinct bodies, one atomic per SIMD group
    if (simd_is_first() && first != 0) atomic_fetch_add_explicit(&steps[p.step].inv, first, memory_order_relaxed);
}

// One round of min-label propagation along contacts.
kernel void hook(device Ctl* ctl [[buffer(4)]],
                 device const uint2* out [[buffer(14)]],
                 device atomic_uint* label [[buffer(24)]],
                 device const uint* list [[buffer(29)]],
                 uint i [[thread_position_in_grid]]) {
    if (i >= atomic_load_explicit(&ctl->nlist, memory_order_relaxed)) return;
    uint e = list[i];
    if (e >= atomic_load_explicit(&ctl->npairs, memory_order_relaxed)) return;
    uint a = out[e].x, b = out[e].y;
    uint m = min(atomic_load_explicit(&label[a], memory_order_relaxed), atomic_load_explicit(&label[b], memory_order_relaxed));
    atomic_fetch_min_explicit(&label[a], m, memory_order_relaxed);
    atomic_fetch_min_explicit(&label[b], m, memory_order_relaxed);
}

constant uint BAD = 1u << 31;

// Component sizes (bodies in bits 0..15, contacts in 16..30) and the BAD flag: a contact
// whose ends disagree (labels not converged: both label groups are unfinished) or a body
// with more than ADJ events.
kernel void mark(device Ctl* ctl [[buffer(4)]],
                 device const uint* walls [[buffer(12)]],
                 device const uint2* out [[buffer(14)]],
                 device Dyn* dy [[buffer(3)]],
                 device const uint* label [[buffer(24)]],
                 device const uint* adj [[buffer(26)]],
                 device atomic_uint* comp [[buffer(27)]],
                 device const uint* list [[buffer(29)]],
                 uint i [[thread_position_in_grid]]) {
    if (i >= atomic_load_explicit(&ctl->nlist, memory_order_relaxed)) return;
    uint e = list[i];
    uint a = 0, b = 0, m = bodies_of(e, ctl, out, walls, a, b);
    uint la = label[a], lb = label[b];
    if (la != lb) {
        atomic_fetch_or_explicit(&comp[la], BAD, memory_order_relaxed);
        atomic_fetch_or_explicit(&comp[lb], BAD, memory_order_relaxed);
    }
    if (m == 2) atomic_fetch_add_explicit(&comp[la], 1u << 16, memory_order_relaxed);
    for (uint q = 0; q < m; ++q) {
        uint x = q == 0 ? a : b;
        if (count_of(dy, x) > ADJ) atomic_fetch_or_explicit(&comp[label[x]], BAD, memory_order_relaxed);
        if (adj[x * ADJ] == e) atomic_fetch_add_explicit(&comp[label[x]], 1u, memory_order_relaxed);
    }
}

// v.div_euclid(den) for 0 < den and |v| < 2^60, as fdiv (64-bit `/` is emulated and slow).
static inline long floor_div(long v, long den) {
    float fd = float(den);
    long q = 0, r = v;
    while (abs(r) >= 4 * den) {
        long dq = long(floor(float(r) / fd));
        q += dq;
        r -= dq * den;
    }
    while (r < 0) { q -= 1; r += den; }
    while (r >= den) { q += 1; r -= den; }
    return q;
}

static inline long energy(long m, long2 k) {
    return m * (k.x * k.x + k.y * k.y);
}

static inline short2 narrow(long2 k) {
    return short2(clamp(k, -32767l, 32767l));
}

// The impulse of law::resolve for one bouncer pair in i64: the new velocities and the
// energy error, or false if a guard fails (then the CPU resolves the component in i128).
// Guards (a factor 8 of slack): |k_c| < 2^18, |d_c| < 2^30, carries < 2^60, and float
// bounds on the rounding denominator and numerators below 2^60.
static inline bool impulse(long2 d, uint ua, uint ub, thread long2& ka, thread long2& kb, long owed, thread long& en,
                           thread long& carry_a) {
    if (any(abs(ka) >= (1l << 18)) || any(abs(kb) >= (1l << 18)) || any(abs(d) >= (1l << 30)) ||
        abs(owed) >= (1l << 60) || abs(carry_a) >= (1l << 60)) {
        return false;
    }
    long2 w = kb - ka;
    long dotp = d.x * w.x + d.y * w.y, dd = d.x * d.x + d.y * d.y;
    en = 0;
    if (dotp >= 0 || dd == 0) return true;
    uint x = ua, y = ub;
    while (y != 0) {
        uint t = x % y;
        x = y;
        y = t;
    }
    long ma = ua, mb = ub, la = ub / x, lb = ua / x, lcm = long(ua / x) * ub;  // la = lcm/ma
    float fden = float(ma + mb) * float(dd) * float(lcm);
    float fnum = float(max(abs(d.x), abs(d.y))) * 2.0f * float(ma) * float(mb) * float(-dotp);
    if (fden >= 0x1p60f || fnum >= 0x1p60f) return false;
    long den = (ma + mb) * dd * lcm;
    long2 num = d * (2 * ma * mb * dotp);
    bool nonzero = num.x != 0 || num.y != 0;
    long2 lo = long2(floor_div(num.x, den), floor_div(num.y, den));
    long2 hi = long2(-floor_div(-num.x, den), -floor_div(-num.y, den));
    long e0 = energy(ma, ka) + energy(mb, kb), best = 0;
    long2 na = ka, nb = kb, seen[4];
    uint nc = 0;
    for (uint u = 0; u < 2; ++u) {
        for (uint v = 0; v < 2; ++v) {
            long2 cc = long2(u == 0 ? lo.x : hi.x, v == 0 ? lo.y : hi.y);
            bool dup = all(cc == 0) && nonzero;
            for (uint q = 0; q < nc; ++q) dup = dup || all(seen[q] == cc);
            if (dup) continue;
            seen[nc] = cc;
            long2 da = cc * la, db = -cc * lb;
            long ec = energy(ma, ka + da) + energy(mb, kb + db) - e0;
            long score = abs(owed + ec);
            if (nc == 0 || score < best) {
                best = score;
                en = ec;
                na = ka + da;
                nb = kb + db;
            }
            ++nc;
        }
    }
    carry_a += en;
    ka = na;
    kb = nb;
    return true;
}

// Over every event: isolated contacts (both bodies in no other event: the common case)
// resolve here, one per thread with few registers, log slots reserved once per SIMD group;
// every other event joins the list of the general response.
kernel void resolve_pair(device const long2* pos [[buffer(0)]],
                         device Dyn* dy [[buffer(3)]],
                         device Ctl* ctl [[buffer(4)]],
                         constant Params& p [[buffer(5)]],
                         device short2* kq [[buffer(7)]],
                         device const uint* rf [[buffer(8)]],
                         device const uint* mass [[buffer(10)]],
                         device Slot* table [[buffer(13)]],
                         device const uint2* out [[buffer(14)]],
                         device uint* mask [[buffer(18)]],
                         device uchar* stat [[buffer(20)]],
                         device Ev* log [[buffer(28)]],
                         device uint* list [[buffer(29)]],
                         device const uint* walls [[buffer(12)]],
                         uint e [[thread_position_in_grid]]) {
    uint np = atomic_load_explicit(&ctl->npairs, memory_order_relaxed);
    uint nw = atomic_load_explicit(&ctl->nwalls, memory_order_relaxed);
    uint a = 0, b = 0;
    bool mine = e < np;
    if (mine) {
        a = out[e].x;
        b = out[e].y;
        mine = count_of(dy, a) == 1 && count_of(dy, b) == 1;
    }
    uint other = uint(!mine && e < np + nw);
    uint lpre = simd_prefix_exclusive_sum(other), ltot = simd_sum(other), lbase = 0;
    if (simd_is_first() && ltot != 0) lbase = atomic_fetch_add_explicit(&ctl->nlist, ltot, memory_order_relaxed);
    lbase = simd_broadcast_first(lbase) + lpre;
    if (other != 0) list[lbase] = e;
    long2 ka = 0, kb = 0, oa = 0, ob = 0;
    long ra = 0, en = 0;
    uint fa = 0, fb = 0, rva = 0, rvb = 0;
    bool ok = mine;
    if (mine) {
        fa = rf[a];
        fb = rf[b];
        oa = ka = dy[a].k;
        ob = kb = dy[b].k;
        ra = dy[a].res;
        if ((fa & BOUNCE) != 0 && (fb & BOUNCE) != 0) {
            ok = impulse(pos[b] - pos[a], mass[a], mass[b], ka, kb, ra + dy[b].res, en, ra);
        }
        if ((fa & STOP) != 0) ka = 0;
        if ((fb & STOP) != 0) kb = 0;
        rva = dy[a].rev + uint(any(ka != oa));
        rvb = dy[b].rev + uint(any(kb != ob));
        // Room in a's row: b's own slot, an empty one, or a stale one (every entry is stale
        // once a revises).
        if (ok) {
            bool room = false;
            for (uint m = 0; m < SLOTS; ++m) {
                Slot s = table[a * SLOTS + m];
                room = room || s.j == b || s.j == EMPTY || s.ri != rva;
            }
            ok = room;
        }
    }
    uint want = uint(ok);
    uint pre = simd_prefix_exclusive_sum(want), tot = simd_sum(want);
    uint base = 0;
    if (simd_is_first() && tot != 0) base = atomic_fetch_add_explicit(&ctl->nlog, tot, memory_order_relaxed);
    base = simd_broadcast_first(base) + pre;
    if (ok && base >= p.log_cap) ok = false;
    if (!mine) return;
    atomic_store_explicit(&dy[a].cnt, 0u, memory_order_relaxed);  // only this event touches a, b
    atomic_store_explicit(&dy[b].cnt, 0u, memory_order_relaxed);
    if (!ok) {
        if (want != 0 && base < p.log_cap) log[base].a = EMPTY;  // reserved, unused
        stat[e] = FOR_CPU;
        ctl->halt = HALT_CPU;
        return;
    }
    if ((fa & BOUNCE) != 0 && (fb & BOUNCE) != 0) dy[a].res = ra;
    // A body that revises has only dead contacts: its mask restarts empty (the dead
    // entries stay until reused; they never match).
    if (any(ka != oa)) {
        dy[a].k = ka;
        kq[a] = narrow(ka);
        dy[a].rev = rva;
        mask[a] = 0;
    }
    if (any(kb != ob)) {
        dy[b].k = kb;
        kq[b] = narrow(kb);
        dy[b].rev = rvb;
        mask[b] = 0;
    }
    uint pick = SLOTS;
    for (uint m = 0; m < SLOTS; ++m) if (table[a * SLOTS + m].j == b) pick = m;
    for (uint m = 0; m < SLOTS && pick == SLOTS; ++m) {
        Slot s = table[a * SLOTS + m];
        if (s.j == EMPTY || s.ri != rva) pick = m;
    }
    Slot s;
    s.j = b;
    s.ri = rva;
    s.rj = rvb;
    table[a * SLOTS + pick] = s;
    mask[a] |= 1u << (b & 31);
    stat[e] = 0;
    Ev ev;
    ev.a = a;
    ev.b = b;
    ev.wx = 0;
    ev.wy = 0;
    log[base] = ev;
}

// The leader of each larger component (its root's smallest event) resolves it; see above.
kernel void resolve(device const long2* pos [[buffer(0)]],
                    device Dyn* dy [[buffer(3)]],
                    device Ctl* ctl [[buffer(4)]],
                    constant Params& p [[buffer(5)]],
                    device short2* kq [[buffer(7)]],
                    device const uint* rf [[buffer(8)]],
                    device const uint* mass [[buffer(10)]],
                    device const uint* walls [[buffer(12)]],
                    device Slot* table [[buffer(13)]],
                    device const uint2* out [[buffer(14)]],
                    device uint* mask [[buffer(18)]],
                    device uchar* stat [[buffer(20)]],
                    device const uint* label [[buffer(24)]],
                    device const uint* adj [[buffer(26)]],
                    device const uint* comp [[buffer(27)]],
                    device Ev* log [[buffer(28)]],
                    device const uint* list [[buffer(29)]],
                    uint i [[thread_position_in_grid]]) {
    if (i >= atomic_load_explicit(&ctl->nlist, memory_order_relaxed)) return;
    uint e = list[i];
    uint a0 = 0, b0 = 0;
    bodies_of(e, ctl, out, walls, a0, b0);
    uint np = atomic_load_explicit(&ctl->npairs, memory_order_relaxed);
    uint r = label[a0], c = comp[r];
    if ((c & BAD) != 0 || (c & 0xffffu) > MAXB || ((c >> 16) & 0x7fffu) > MAXP) {
        stat[e] = FOR_CPU;
        ctl->halt = HALT_CPU;
        return;
    }
    uint lead = EMPTY;
    for (uint s = 0; s < count_of(dy, r); ++s) lead = min(lead, adj[r * ADJ + s]);
    if (e != lead) return;

    // Gather the component: bodies (breadth first from the root), contacts, wall events.
    uint B[MAXB], P[MAXP], WE[MAXB];
    uint nb = 1, npc = 0;
    B[0] = r;
    for (uint q = 0; q < MAXB; ++q) WE[q] = EMPTY;
    for (uint q = 0; q < nb; ++q) {
        uint x = B[q];
        for (uint s = 0; s < count_of(dy, x); ++s) {
            uint f = adj[x * ADJ + s];
            if (f >= np) {
                WE[q] = f;
                continue;
            }
            uint2 pr = out[f];
            uint y = pr.x == x ? pr.y : pr.x;
            bool seen = false;
            for (uint z = 0; z < nb; ++z) seen = seen || B[z] == y;
            if (!seen && nb < MAXB) B[nb++] = y;
            bool have = false;
            for (uint z = 0; z < npc; ++z) have = have || P[z] == f;
            if (!have && npc < MAXP) P[npc++] = f;
        }
    }
    // Contacts in canonical (index) order.
    for (uint q = 1; q < npc; ++q) {
        uint f = P[q];
        ulong key = ulong(out[f].x) << 32 | out[f].y;
        uint z = q;
        while (z > 0 && (ulong(out[P[z - 1]].x) << 32 | out[P[z - 1]].y) > key) {
            P[z] = P[z - 1];
            --z;
        }
        P[z] = f;
    }
    long2 K[MAXB], K0[MAXB];
    long W[MAXB];
    uint cw = 0;
    for (uint q = 0; q < nb; ++q) {
        K[q] = K0[q] = dy[B[q]].k;
        W[q] = dy[B[q]].res;
    }
    bool ok = true;
    long en = 0;
    for (uint z = 0; z < npc && ok; ++z) {
        uint a = out[P[z]].x, b = out[P[z]].y, ia = 0, ib = 0;
        for (uint q = 0; q < nb; ++q) {
            if (B[q] == a) ia = q;
            if (B[q] == b) ib = q;
        }
        if ((rf[a] & BOUNCE) == 0 || (rf[b] & BOUNCE) == 0) continue;
        cw |= (1u << ia) | (1u << ib);
        long carry = W[ia];
        ok = impulse(pos[b] - pos[a], mass[a], mass[b], K[ia], K[ib], W[ia] + W[ib], en, carry);
        W[ia] = carry;
    }
    if (ok) {
        for (uint z = 0; z < npc; ++z) {
            for (uint q = 0; q < nb; ++q) {
                uint x = B[q];
                if ((x == out[P[z]].x || x == out[P[z]].y) && (rf[x] & STOP) != 0) K[q] = 0;
            }
        }
    }
    // Walls: flip each outward component that is still outward.
    long2 WM[MAXB];
    uint nwc = 0;
    for (uint q = 0; q < nb; ++q) {
        WM[q] = 0;
        if (!ok || WE[q] == EMPTY) continue;
        ++nwc;
        uint x = B[q];
        long r2 = rf[x] & RADIUS, m = mass[x];
        long2 y = pos[x];
        long2 lo = long2(p.bmin_x + r2, p.bmin_y + r2), hi = long2(p.bmax_x - r2, p.bmax_y - r2);
        for (uint ax = 0; ax < 2; ++ax) {
            if ((y[ax] <= lo[ax] && K[q][ax] < 0) || (y[ax] >= hi[ax] && K[q][ax] > 0)) {
                WM[q][ax] = m * 2 * K[q][ax];
                K[q][ax] = -K[q][ax];
            }
        }
    }
    // Every contact is consumed in its lower body's row: check there is room first (every
    // entry of a body that revises is stale).
    uint RV[MAXB];
    for (uint q = 0; q < nb; ++q) RV[q] = dy[B[q]].rev + uint(any(K[q] != K0[q]));
    for (uint z = 0; z < npc && ok; ++z) {
        uint a = out[P[z]].x, ia = 0;
        if (z > 0 && out[P[z - 1]].x == a) continue;  // each row once, at its first contact
        for (uint q = 0; q < nb; ++q) if (B[q] == a) ia = q;
        // Contacts with a slot of their own reuse it; the others need an empty or stale slot
        // that no contact of this row owns.
        uint need = 0, room = 0;
        for (uint y = z; y < npc && out[P[y]].x == a; ++y) {
            bool own = false;
            for (uint m = 0; m < SLOTS; ++m) own = own || table[a * SLOTS + m].j == out[P[y]].y;
            need += uint(!own);
        }
        for (uint m = 0; m < SLOTS; ++m) {
            Slot s = table[a * SLOTS + m];
            bool mine = false;
            for (uint y = z; y < npc && out[P[y]].x == a; ++y) mine = mine || s.j == out[P[y]].y;
            room += uint(!mine && (s.j == EMPTY || s.ri != RV[ia]));
        }
        ok = need <= room;
    }
    uint nev = npc + nwc, base = 0;
    if (ok) {
        base = atomic_fetch_add_explicit(&ctl->nlog, nev, memory_order_relaxed);
        if (base + nev > p.log_cap) {
            for (uint z = base; z < min(base + nev, p.log_cap); ++z) log[z].a = EMPTY;  // unused
            ok = false;
        }
    }
    if (!ok) {
        for (uint z = 0; z < npc; ++z) stat[P[z]] = FOR_CPU;
        for (uint q = 0; q < nb; ++q) if (WE[q] != EMPTY) stat[WE[q]] = FOR_CPU;
        ctl->halt = HALT_CPU;
        return;
    }
    for (uint q = 0; q < nb; ++q) {
        uint x = B[q];
        if ((cw >> q) & 1) dy[x].res = W[q];
        if (any(K[q] != K0[q])) {
            dy[x].k = K[q];
            kq[x] = narrow(K[q]);
            dy[x].rev = RV[q];
            mask[x] = 0;
        }
    }
    uint o = base;
    for (uint z = 0; z < npc; ++z) {
        uint a = out[P[z]].x, b = out[P[z]].y, ia = 0, ib = 0;
        for (uint q = 0; q < nb; ++q) {
            if (B[q] == a) ia = q;
            if (B[q] == b) ib = q;
        }
        uint pick = SLOTS;
        for (uint m = 0; m < SLOTS; ++m) if (table[a * SLOTS + m].j == b) pick = m;
        for (uint m = 0; m < SLOTS && pick == SLOTS; ++m) {
            Slot s = table[a * SLOTS + m];
            bool mine = false;
            for (uint y = 0; y < npc; ++y) mine = mine || (out[P[y]].x == a && s.j == out[P[y]].y);
            if (!mine && (s.j == EMPTY || s.ri != RV[ia])) pick = m;
        }
        Slot s;
        s.j = b;
        s.ri = RV[ia];
        s.rj = RV[ib];
        table[a * SLOTS + pick] = s;
        mask[a] |= 1u << (b & 31);
        stat[P[z]] = 0;
        Ev ev;
        ev.a = a;
        ev.b = b;
        ev.wx = 0;
        ev.wy = 0;
        log[o++] = ev;
    }
    for (uint q = 0; q < nb; ++q) {
        if (WE[q] == EMPTY) continue;
        stat[WE[q]] = 0;
        Ev ev;
        ev.a = B[q];
        ev.b = EMPTY;
        ev.wx = WM[q].x;
        ev.wy = WM[q].y;
        log[o++] = ev;
    }
}

// Clear the per-chronon component state of the listed events' bodies (resolve_pair clears
// the isolated contacts' own).
kernel void unmark(device Ctl* ctl [[buffer(4)]],
                   device const uint* walls [[buffer(12)]],
                   device const uint2* out [[buffer(14)]],
                   device Dyn* dy [[buffer(3)]],
                   device uint* comp [[buffer(27)]],
                   device const uint* list [[buffer(29)]],
                   uint i [[thread_position_in_grid]]) {
    if (i >= atomic_load_explicit(&ctl->nlist, memory_order_relaxed)) return;
    uint a = 0, b = 0, m = bodies_of(list[i], ctl, out, walls, a, b);
    for (uint q = 0; q < m; ++q) {
        uint x = q == 0 ? a : b;
        atomic_store_explicit(&dy[x].cnt, 0u, memory_order_relaxed);
        comp[x] = 0;
    }
}

// The reference's pruning of consumed contacts after chronons at multiples of 64 (only if
// this buffer has not halted: a halted chronon is pruned after its CPU response). Keep an
// entry while both revisions are current and the pair approaches; rebuild the masks. Entries
// more than 2^30 apart are kept: they can never be adjacent again (their distance can only
// grow at constant velocities), so keeping them changes nothing.
kernel void prune(device const long2* pos [[buffer(0)]],
                  device Dyn* dy [[buffer(3)]],
                  device Ctl* ctl [[buffer(4)]],
                  constant Params& p [[buffer(5)]],
                  device Slot* table [[buffer(13)]],
                  device uint* mask [[buffer(18)]],
                  uint i [[thread_position_in_grid]]) {
    if (i >= p.n || ctl->halt != 0) return;
    uint m = 0;
    for (uint k = 0; k < SLOTS; ++k) {
        Slot s = table[i * SLOTS + k];
        if (s.j == EMPTY) continue;
        long2 d = pos[s.j] - pos[i], w = dy[s.j].k - dy[i].k;
        bool far = any(abs(d) >= (1l << 30)) || any(abs(w) >= (1l << 30));
        bool live = s.ri == dy[i].rev && s.rj == dy[s.j].rev && (far || d.x * w.x + d.y * w.y < 0);
        if (live) {
            m |= 1u << (s.j & 31);
        } else {
            table[i * SLOTS + k].j = EMPTY;
        }
    }
    mask[i] = m;
}
