// The GPU half of MetalChronon. One chronon = kmax, plan, [clear, bin: only when the cell
// side changed], scan_reduce, scan_sums, scan_final, scatter (the snapshot), pairs
// (detection), advance (wall set, and binning for the next chronon), then the response:
// tally, classify, [rel_mom: relativistic laws], resolve_pair (isolated contacts),
// listargs, hook × HOOKS, mark, resolve (larger components), unmark; every 64 chronons,
// prune. Many chronons share one command
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
    long q;
    uint n, wbits, hmask, has_box, pair_cap, nblocks;
    uint resolve;  // resolve contacts here (no CPU-side consumed filter; Q ≤ 2^15 under v0)
    uint log_cap;
    uint step;  // chronon index in this command buffer
    uint pad;
};

// The world's law, fixed when the pipelines are built so each keeps only its own bounce:
// 0 Newtonian (law::resolve), 1 relativistic v0 and 2 relativistic v1 (relativity::resolve_law;
// the versions differ only in the fixed-point 4-momentum, `fourm`).
constant uint LAW [[function_constant(0)]];

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
                  uint T [[threads_per_threadgroup]],
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
    // Stride by the group's real size: dispatch_threads makes the last group partial (n mod 256
    // threads, the only group below 256 bodies), and up to TGHITS hits are buffered in it.
    for (uint h = t; h < k; h += T) {
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

// Indirect grid sizes: every event (hits then walls), and eight threads per hit (rel_mom).
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
    args[15] = (8 * hits + 255) / 256; args[16] = 1; args[17] = 1;
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

// Incidences per body (first ADJ recorded), distinct bodies, labels initialised to self; and
// under the relativistic laws the bounce's first stage for every hit.
// Stage 1 of the relativistic bounce (defined with it below).
static inline void rel_prep_one(uint e, uint a, uint b, device const long2* pos, device Dyn* dy, constant Params& p,
                                device const uint* mass, device long* rel);

kernel void classify(device Ctl* ctl [[buffer(4)]],
                     constant Params& p [[buffer(5)]],
                     device const uint* walls [[buffer(12)]],
                     device const uint2* out [[buffer(14)]],
                     device Dyn* dy [[buffer(3)]],
                     device atomic_uint* label [[buffer(24)]],
                     device Step* steps [[buffer(25)]],
                     device uint* adj [[buffer(26)]],
                     device const long2* pos [[buffer(0)]],
                     device const uint* mass [[buffer(10)]],
                     device long* rel [[buffer(30)]],
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
    // The relativistic bounce's first stage while this hit's bodies are at hand.
    if (LAW != 0 && m == 2) rel_prep_one(e, a, b, pos, dy, p, mass, rel);
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

// ---- The relativistic bounce (relativity.rs), exact ------------------------------------------
// Signed 128-bit integers from two 64-bit halves. An operation that could overflow clears
// `ok`, and the caller hands the component to the CPU, which follows the reference's own
// path (big integers if need be).
struct w128 {
    ulong lo, hi;
};

static inline w128 w_of(long v) {
    w128 r;
    r.lo = ulong(v);
    r.hi = v < 0 ? ~0ul : 0ul;
    return r;
}
static inline bool w_neg(w128 a) { return (a.hi >> 63) != 0; }
static inline bool w_zero(w128 a) { return (a.lo | a.hi) == 0; }
static inline bool w_lt(w128 a, w128 b) { return long(a.hi) < long(b.hi) || (a.hi == b.hi && a.lo < b.lo); }
static inline w128 w_add(w128 a, w128 b, thread bool& ok) {
    w128 r;
    r.lo = a.lo + b.lo;
    r.hi = a.hi + b.hi + ulong(r.lo < a.lo);
    ok = ok && (((a.hi ^ r.hi) & (b.hi ^ r.hi)) >> 63) == 0;
    return r;
}
static inline w128 w_minus(w128 a, thread bool& ok) {
    ok = ok && !(a.hi == (1ul << 63) && a.lo == 0);
    w128 r;
    r.lo = ~a.lo + 1;
    r.hi = ~a.hi + ulong(r.lo == 0);
    return r;
}
static inline w128 w_sub(w128 a, w128 b, thread bool& ok) { return w_add(a, w_minus(b, ok), ok); }
// Exact signed 64 × 64.
static inline w128 w_mul(long a, long b) {
    ulong ua = ulong(a), ub = ulong(b);
    w128 r;
    r.lo = ua * ub;
    r.hi = mulhi(ua, ub) - (a < 0 ? ub : 0ul) - (b < 0 ? ua : 0ul);
    return r;
}
// Checked signed 128 × 64 (magnitudes up to 2^127 − 1).
static inline w128 w_mul(w128 a, long b, thread bool& ok) {
    bool na = w_neg(a), nb = b < 0;
    w128 m = na ? w_minus(a, ok) : a;
    ulong ub = nb ? ~ulong(b) + 1 : ulong(b);
    ulong c = mulhi(m.lo, ub);
    w128 r;
    r.lo = m.lo * ub;
    r.hi = c + m.hi * ub;
    ok = ok && mulhi(m.hi, ub) == 0 && r.hi >= c && (r.hi >> 63) == 0;
    return na != nb ? w_minus(r, ok) : r;
}
// The value if it is below 2^62 in magnitude (so squares and sums of three stay in 126 bits).
static inline long w_small(w128 a, thread bool& ok) {
    long v = long(a.lo);
    ok = ok && a.hi == (v < 0 ? ~0ul : 0ul) && v > -(1l << 62) && v < (1l << 62);
    return v;
}
static inline float w_float(w128 a) {
    bool n = w_neg(a), ok = true;
    w128 m = n ? w_minus(a, ok) : a;
    float f = float(m.hi) * 0x1p64f + float(m.lo);
    return n ? -f : f;
}
// ⌊num/den⌋ for den > 0 when the quotient is small (a velocity). With IEEE rounding the float
// quotient is within about 2^-21 relative of the true one (two conversions and an add per
// operand, one division); a fractional part clear of the (|q| + 1)·2^-16 margin decides both
// the floor and that den does not divide num. Near an integer the exact 128-bit check runs.
static inline long w_floor(w128 num, w128 den, thread bool& exact, thread bool& ok) {
    float qr = w_float(num) / w_float(den), qf = floor(qr), margin = (fabs(qr) + 1.0f) * 0x1p-16f;
    if (!(fabs(qf) < 0x1p24f)) {
        ok = false;
        return 0;
    }
    long qv = long(qf);
    if (qr - qf > margin && qr - qf < 1.0f - margin) {
        exact = false;
        return qv;
    }
    w128 r = w_sub(num, w_mul(den, qv, ok), ok);
    for (uint i = 0; i < 3 && w_neg(r); ++i) {
        qv -= 1;
        r = w_add(r, den, ok);
    }
    for (uint i = 0; i < 3 && !w_lt(r, den); ++i) {
        qv += 1;
        r = w_sub(r, den, ok);
    }
    ok = ok && !w_neg(r) && w_lt(r, den);
    exact = w_zero(r);
    return qv;
}

// Γ(k) = ⌊√⌊F²Q²/s⌋⌋, s = Q² − |k|², F = 2^16 (relativity::gamma): the largest g with
// g²·s ≤ F²Q² (equivalent for integers), from a float estimate and exact steps. Q ≤ 2^15
// keeps F²Q² < 2^62 and g < 2^31.
static inline long gam(long2 k, long q, thread bool& ok) {
    long s = q * q - (k.x * k.x + k.y * k.y);
    if (s <= 0) {
        ok = false;
        return 0;
    }
    // lo = g²s and hi = (g+1)²s bracket F²Q² once g is right; unit steps update both.
    w128 lim = w_of((q * q) << 32);
    long g = clamp(long(65536.0f * float(q) * rsqrt(float(s))), 1l, (1l << 31) - 2);
    bool dummy = true;
    w128 lo = w_mul(g * g, s);
    for (uint round = 0; round < 2; ++round) {
        for (uint i = 0; i < 4; ++i) {
            w128 hi = w_add(lo, w_of((2 * g + 1) * s), dummy);
            if (w_lt(lim, lo)) {
                --g;
                lo = w_sub(lo, w_of((2 * g + 1) * s), dummy);
            } else if (!w_lt(lim, hi)) {
                ++g;
                lo = hi;
            } else {
                ok = ok && g > 0;
                return g;
            }
        }
        // Far off (only near c at large Q): one float Newton step on the exact residual.
        g = clamp(g + long(rint(w_float(w_sub(lim, lo, dummy)) / (2.0f * float(g) * float(s)))), 1l, (1l << 31) - 2);
        lo = w_mul(g * g, s);
    }
    ok = false;
    return g;
}

// v0 fixed-point 4-momentum (E, px, py) = m·Γ·(Q, k), required below 2^60 (|p| < E) so the
// sums and differences below stay exact in 64 bits.
static inline long3 fourm0(uint m, long2 k, long q, thread bool& ok) {
    long g = long(m) * gam(k, q, ok);  // < 2^47
    ok = ok && g < (1l << 60) / q;
    return long3(g * q, g * k.x, g * k.y);
}

// ---- v1 square roots: ⌊t/√s⌋ for t ≥ 0, s ≥ 1, the largest v with v²·s ≤ t² -------------
// (equivalent for integers: v ≤ t/√s ⟺ v²s ≤ t²). A float estimate, then exact brackets
// v²s ≤ t² < (v+1)²s; unit steps, and far off (near c) a float Newton step on the exact
// residual. Nothing is rounded: a bracket not found in two rounds hands the contact to the CPU.

// Unsigned 96-bit values as 32-bit limbs (a lowest): 32-bit multiplies are native, 64-bit
// ones are emulated.
struct u96 {
    uint a, b, c;
};
// v²·s for v, s < 2^32 (below 2^96).
static inline u96 sqs(uint v, uint s) {
    uint l = v * v, h = mulhi(v, v);
    uint l1 = mulhi(l, s), h0 = h * s;
    u96 r;
    r.a = l * s;
    r.b = l1 + h0;
    r.c = mulhi(h, s) + uint(r.b < l1);
    return r;
}
// x + y, for sums below 2^96.
static inline u96 u96_add(u96 x, u96 y) {
    u96 r;
    r.a = x.a + y.a;
    uint c0 = uint(r.a < x.a);
    r.b = x.b + y.b;
    uint c1 = uint(r.b < x.b);
    r.b += c0;
    c1 += uint(r.b < c0);
    r.c = x.c + y.c + c1;
    return r;
}
static inline bool u96_lt(u96 x, u96 y) {
    return x.c != y.c ? x.c < y.c : x.b != y.b ? x.b < y.b : x.a < y.a;
}
// float(x − y), subtracting exactly first.
static inline float u96_diff(u96 x, u96 y) {
    bool neg = u96_lt(x, y);
    u96 p = neg ? y : x, q = neg ? x : y;
    uint a = p.a - q.a, ba = uint(p.a < q.a);
    uint b = p.b - q.b, bb = uint(p.b < q.b) + uint(b < ba);
    b -= ba;
    float f = float(p.c - q.c - bb) * 0x1p64f + float(b) * 0x1p32f + float(a);
    return neg ? -f : f;
}

// t ≤ 2^31 and s < 2^32 (Q ≤ 2^10 for every v1 root): v ≤ t, so v + 1 < 2^32 and every
// product fits 96 bits.
static inline long root32(uint t, uint s, float rs, thread bool& ok) {
    u96 t2 = {t * t, mulhi(t, t), 0};
    // First the window {v, v + 1} half a unit below the float estimate, with the brackets
    // v²s, (v+1)²s = v²s + (2v+1)s and (v+2)²s = (v+1)²s + (2v+3)s (below 2^95): no division,
    // no branch. The estimate is within about 2^-22 relative, so this settles every root up to
    // 2^21 or so (the energies of a gas at Q = 2^10 are 2^21 to 2^22).
    uint v = uint(clamp(float(t) * rs - 0.5f, 0.0f, float(t)));
    uint vs0 = v * s, vs1 = mulhi(v, s);                                  // v·s
    u96 d1 = u96_add(u96{vs0 << 1, (vs1 << 1) | (vs0 >> 31), vs1 >> 31}, u96{s, 0, 0});  // (2v+1)s
    u96 d2 = u96_add(d1, u96{s << 1, s >> 31, 0});                        // (2v+3)s
    u96 b0 = sqs(v, s), b1 = u96_add(b0, d1), b2 = u96_add(b1, d2);
    if (!u96_lt(t2, b0)) {
        if (u96_lt(t2, b1)) return v;
        if (u96_lt(t2, b2)) return v + 1;
    }
    for (uint i = 0; i < 8; ++i) {
        u96 lo = sqs(v, s);
        bool below = !u96_lt(t2, lo);  // v²s ≤ t²
        if (below && u96_lt(t2, sqs(v + 1, s))) return v;
        // A unit step toward the root; far off (near c, where the float estimate is 2^-22
        // relative) a float Newton step on the exact residual, the update in integers.
        float dv = u96_diff(t2, lo) / (2.0f * float(max(v, 1u)) * float(s));
        long step = fabs(dv) < 2.0f ? (below ? 1l : -1l) : long(rint(clamp(dv, -0x1p33f, 0x1p33f)));
        v = uint(clamp(long(v) + step, 0l, long(t)));
    }
    ok = false;
    return 0;
}

// t ≤ 2^61 and s ≤ 2^40 (Q ≤ 2^20): t² < 2^123, and every bracket near the root stays below
// 2^124 (checked all the same).
static inline long root_wide(long t, long s, float rs, thread bool& ok) {
    w128 t2 = w_mul(t, t);
    long v = clamp(long(min(float(t) * rs, float(t))), 0l, t);
    bool fine = true;
    for (uint i = 0; i < 8 && fine; ++i) {
        w128 r = w_sub(t2, w_mul(w_mul(v, v), s, fine), fine);  // t² − v²s
        bool below = !w_neg(r);
        if (below && w_lt(r, w_mul(2 * v + 1, s)) && fine) return v;  // t² < (v+1)²s
        float dv = w_float(r) / (2.0f * float(max(v, 1l)) * float(s));
        long step = fabs(dv) < 2.0f ? (below ? 1l : -1l) : long(rint(clamp(dv, -0x1p62f, 0x1p62f)));
        v = clamp(v + step, 0l, t);
    }
    ok = false;
    return 0;
}

static inline long root(long t, long s, float rs, thread bool& ok) {
    return t <= (1l << 31) && s < (1l << 32) ? root32(uint(t), uint(s), rs, ok) : root_wide(t, s, rs, ok);
}

// v1 fixed-point 4-momentum (relativity::four_momentum_v1): per unit mass E = ⌊2Q³/√s⌋ and
// p_c = sgn(k_c)·⌊2Q²|k_c|/√s⌋, s = Q² − |k|², times m; E below 2^60 (|p_c| ≤ E) as in v0.
// Q ≤ 2^20 (the law's range), |k_c| ≤ Q.
static inline long3 fourm1(uint m, long2 k, long q, thread bool& ok) {
    long q2 = q * q, s = q2 - (k.x * k.x + k.y * k.y);
    if (s <= 0 || q > (1l << 20)) {
        ok = false;
        return 0;
    }
    float rs = rsqrt(float(s));
    long e = root(2 * q * q2, s, rs, ok);
    long px = root(2 * q2 * abs(k.x), s, rs, ok), py = root(2 * q2 * abs(k.y), s, rs, ok);
    // m ≤ 2^32 and e < 2^62: the float product bounds m·e within 2^-22, far inside 2^59 < 2^60.
    ok = ok && float(e) * float(m) < 0x1p59f;
    long M = long(m);
    return long3(M * e, M * (k.x < 0 ? -px : px), M * (k.y < 0 ? -py : py));
}

// The world's relativistic 4-momentum.
static inline long3 fourm(uint m, long2 k, long q, thread bool& ok) {
    return LAW == 2 ? fourm1(m, k, q, ok) : fourm0(m, k, q, ok);
}

constant uint REL_EXCH = 0, REL_NONE = 1, REL_CPU = 2;

// The floors of one side's targets q·x/e and q·y/e, where (e, x, y) = T·p − 2S·n exactly
// (Tf and S2f are T and 2S within 2^-23 relative, scaled by 2^-64), decided in floats when
// an error bound allows; false leaves them to the exact 128-bit path. Every float operation
// here is IEEE (no fast math): a product of two rounded inputs is within 2^-22 relative of
// the exact one, so each part v of (e, x, y) is within err = 2^-20·(|T·p| + |2S·n|) (2^-21.4
// with its difference; a factor of 3 to spare). With v_e clear of zero (|v_e| > 4·err_e, so e
// has v_e's sign), |x/e − v_x/v_e| ≤ (err_x/|v_e| + |v_x/v_e|·err_e/|v_e|)/(1 − err_e/|v_e|);
// twice that times q, plus 2^-21 of the quotient (its two roundings, a division of up to 2.5
// ulp included) and 2^-20, must leave the target's float inside one open unit interval: then
// its floor is exact and the target is not an integer. Ratios only, so nothing overflows.
static inline bool float_floors(long q, float Tf, float S2f, long3 pv, long3 nv, thread long2& f) {
    float3 a = Tf * float3(pv), b = S2f * float3(nv), v = a - b;
    float3 err = (fabs(a) + fabs(b)) * 0x1p-20f;
    if (!(fabs(v.x) > 4.0f * err.x)) return false;
    float ve = fabs(v.x), re = err.x / ve, fq = float(q);
    float2 w = (v.x < 0 ? -v.yz : v.yz) / ve;  // e > 0 after normalising, as the exact path does
    float2 tf = fq * w;
    float2 bound = 2.0f * (fq * (err.yz / ve + fabs(w) * re) / (1.0f - re) + fabs(tf) * 0x1p-21f) + 0x1p-20f;
    float2 fl = floor(tf);
    if (!all(fabs(tf) < 0x1p22f) || !all(tf - bound > fl) || !all(tf + bound < fl + 1.0f)) return false;
    f = long2(fl);
    return true;
}

// Candidate slot z of a pair: 0..3 body a's (fl, fl), (fl, ce), (ce, fl), (ce, ce) around its
// target, 4..7 body b's, as positions relative to the floors `fl` (a.x, a.y, b.x, b.y).
static inline long2 slot(long4 fl, uint z) {
    return (z < 4 ? fl.xy : fl.zw) + long2((z >> 1) & 1, z & 1);
}

// Stage 1 of relativity::resolve for one bouncer pair: the 4-momenta (P their sum), the
// Minkowski reflection targets Q·p'/E' with p' ∝ T·p ∓ 2S·N, and the floor/ceil slots
// strictly inside the light cone (`valid` bits; a ceil equal to its floor repeats a point,
// which the reference skips). REL_NONE: no exchange; REL_CPU: a checked range was left.
static inline uint rel_setup(long q, long2 d, uint ma, uint mb, long2 ka, long2 kb, thread long3& P, thread long4& fl,
                             thread uint& valid) {
    long2 w = kb - ka;
    if (d.x * w.x + d.y * w.y >= 0 || d.x * d.x + d.y * d.y == 0) return REL_NONE;
    bool ok = true;
    long3 pa = fourm(ma, ka, q, ok), pb = fourm(mb, kb, q, ok);
    if (!ok) return REL_CPU;
    // P (parts below 2^61); N = (d·P_p, P_E·d), each part below 2^62 so T = N·N and
    // S = pa·N (Minkowski) fit 126 bits.
    P = pa + pb;
    w128 A = w_add(w_mul(d.x, P.y), w_mul(d.y, P.z), ok);
    long n0 = w_small(A, ok), n1 = w_small(w_mul(P.x, d.x), ok), n2 = w_small(w_mul(P.x, d.y), ok);
    if (!ok) return REL_CPU;
    w128 T = w_sub(w_sub(w_mul(n0, n0), w_mul(n1, n1), ok), w_mul(n2, n2), ok);
    w128 S = w_sub(w_sub(w_mul(pa.x, n0), w_mul(pa.y, n1), ok), w_mul(pa.z, n2), ok);
    if (!ok) return REL_CPU;
    if (w_zero(S) || w_zero(T)) return REL_NONE;
    w128 S2 = w_add(S, S, ok);
    // T and 2S scaled by 2^-64 (exactly), so the float products below stay under 2^126.
    float Tf = w_float(T) * 0x1p-64f, S2f = w_float(S2) * 0x1p-64f;
    valid = 0;
    for (uint side = 0; side < 2 && ok; ++side) {
        long3 pv = side == 0 ? pa : pb;
        long sg = side == 0 ? 1 : -1;
        bool ex = false, ey = false;
        long2 f = 0;
        if (!float_floors(q, Tf, S2f, pv, long3(n0, n1, n2) * sg, f)) {
            w128 e = w_sub(w_mul(T, pv.x, ok), w_mul(S2, n0 * sg, ok), ok);
            w128 x = w_sub(w_mul(T, pv.y, ok), w_mul(S2, n1 * sg, ok), ok);
            w128 y = w_sub(w_mul(T, pv.z, ok), w_mul(S2, n2 * sg, ok), ok);
            x = w_mul(x, q, ok);
            y = w_mul(y, q, ok);
            if (w_neg(e)) {
                e = w_minus(e, ok);
                x = w_minus(x, ok);
                y = w_minus(y, ok);
            }
            if (!ok || w_zero(e)) return REL_CPU;
            f = long2(w_floor(x, e, ex, ok), w_floor(y, e, ey, ok));
        }
        if (side == 0) fl.xy = f; else fl.zw = f;
        for (uint z = 0; z < 4; ++z) {
            long2 c = f + long2(z >> 1, z & 1);
            bool keep = ((z >> 1) == 0 || !ex) && ((z & 1) == 0 || !ey) && c.x * c.x + c.y * c.y < q * q;
            valid |= uint(keep) << (side * 4 + z);
        }
    }
    return ok && (valid & 15) != 0 && (valid >> 4) != 0 ? REL_EXCH : REL_CPU;
}

// Candidate 4-momenta in the stage-2 scratch or a thread array, flat longs (E, px, py) per
// slot: arrays of 64-bit vectors miscompiled here (lost or misplaced components). E < 0
// marks a momentum that left its checked range (a valid one has E ≥ 0).
static inline long3 mom_of(device const long* m, uint z) {
    return long3(m[3 * z], m[3 * z + 1], m[3 * z + 2]);
}
static inline long3 mom_of(thread const long* m, uint z) {
    return long3(m[3 * z], m[3 * z + 1], m[3 * z + 2]);
}
static inline long3 mom_or_fail(long3 f, bool ok) {
    return ok ? f : long3(-1, 0, 0);
}

// a² for a < 2^32, from native 32-bit multiplies.
static inline ulong sq32(uint a) {
    return as_type<ulong>(uint2(a * a, mulhi(a, a)));
}
// |r|² exactly for |r_c| < 2^62 (else clears ok): in 64 bits when every |r_c| < 2^31 (three
// squares below 2^62 each), else in 128.
static inline w128 score_of(long3 r, thread bool& ok) {
    ok = ok && all(abs(r) < (1l << 62));
    if (all(abs(r) < (1l << 31))) {
        uint3 u = uint3(abs(r));
        w128 w;
        w.lo = sq32(u.x) + sq32(u.y) + sq32(u.z);
        w.hi = 0;
        return w;
    }
    return w_add(w_add(w_mul(r.x, r.x), w_mul(r.y, r.y), ok), w_mul(r.z, r.z), ok);
}

// Stage 3: the pair of candidates minimising |owed + e|², e the 4-momentum rounding error;
// the first strict minimum in the reference's order; both unchanged only if nothing else.
// a's carries `oa` absorb e. Every 4-momentum part and carry is below 2^60, so e and
// owed + e are exact in 64 bits; the squares need |owed + e| < 2^62.
template <typename M>
static inline bool rel_pick(thread long2& ka, thread long2& kb, thread long3& oa, long3 ob, long3 P, long4 fl, uint valid, M m) {
    bool ok = all(abs(oa) < (1l << 60)) && all(abs(ob) < (1l << 60));
    uint va = valid & 15, vb = valid >> 4;
    bool allowed = popcount(va) * popcount(vb) == 1, found = false;
    w128 best = w_of(0);
    long3 E = 0, owed = oa + ob;
    uint si = 0, sj = 4;
    for (uint i = 0; i < 4; ++i) {
        if (((va >> i) & 1) == 0) continue;
        long3 fa = mom_of(m, i);
        ok = ok && fa.x >= 0;
        for (uint j = 4; j < 8; ++j) {
            if (((vb >> (j - 4)) & 1) == 0 || (!allowed && all(slot(fl, i) == ka) && all(slot(fl, j) == kb))) continue;
            long3 fb = mom_of(m, j);
            ok = ok && fb.x >= 0;
            long3 e = fa + fb - P;
            w128 score = score_of(owed + e, ok);
            if (!found || w_lt(score, best)) {
                found = true;
                best = score;
                E = e;
                si = i;
                sj = j;
            }
        }
    }
    if (!ok) return false;
    if (!found) return true;
    oa += E;  // below 2^62 in magnitude
    ka = slot(fl, si);
    kb = slot(fl, sj);
    return true;
}

// relativity::resolve for one bouncer pair, all stages in one thread (larger components).
// Leaders of many components share a SIMD group, so one thread per component (not eight
// cooperating) keeps the lanes busy: measured faster.
static inline bool rel_bounce(long q, long2 d, uint ma, uint mb, thread long2& ka, thread long2& kb, thread long3& oa, long3 ob) {
    long3 P = 0;
    long4 fl = 0;
    uint valid = 0, st = rel_setup(q, d, ma, mb, ka, kb, P, fl, valid);
    if (st != REL_EXCH) return st == REL_NONE;
    long m[24];  // (E, px, py) per slot
    for (uint z = 0; z < 8; ++z) {
        bool ok = true;
        long3 f = ((valid >> z) & 1) != 0 ? fourm(z < 4 ? ma : mb, slot(fl, z), q, ok) : long3(0);
        f = mom_or_fail(f, ok);
        m[3 * z] = f.x;
        m[3 * z + 1] = f.y;
        m[3 * z + 2] = f.z;
    }
    return rel_pick(ka, kb, oa, ob, P, fl, valid, m);
}

// relativity::resolve for one bouncer pair from its staged scratch r (rel_bounce's outcome
// when the pair's velocities are the ones it was staged with).
static inline bool rel_staged(device const long* r, thread long2& ka, thread long2& kb, thread long3& oa, long3 ob) {
    uint vs = uint(r[7]), st = (vs >> 8) & 255;
    if (st != REL_EXCH) return st == REL_NONE;
    return rel_pick(ka, kb, oa, ob, long3(r[0], r[1], r[2]), long4(r[3], r[4], r[5], r[6]), vs & 255, r + 8);
}

// Scratch of the staged bounce of a hit, flat (see mom_of):
// P (E, px, py) at 0, floors at 3, valid | state << 8 | m_a << 16 | m_b << 40 at 7, slot
// momenta from 8, 3 each.
constant uint REL_LONGS = 32;

// Stage 1, run by classify for every hit (isolation is known only once classify is done, and
// whether both bodies bounce is checked by the consumers): resolve_pair uses the scratch of
// isolated pairs of bouncers, resolve that of larger components' bouncer contacts whose bodies
// have not bounced yet. The masses ride along for rel_mom.
static inline void rel_prep_one(uint e, uint a, uint b, device const long2* pos, device Dyn* dy, constant Params& p,
                                device const uint* mass, device long* rel) {
    uint ma = mass[a], mb = mass[b];
    long2 xa = pos[a], xb = pos[b], ka = dy[a].k, kb = dy[b].k;
    long3 P = 0;
    long4 fl = 0;
    uint valid = 0, st = rel_setup(p.q, xb - xa, ma, mb, ka, kb, P, fl, valid);
    device long* r = rel + e * REL_LONGS;
    r[0] = P.x;
    r[1] = P.y;
    r[2] = P.z;
    r[3] = fl.x;
    r[4] = fl.y;
    r[5] = fl.z;
    r[6] = fl.w;
    r[7] = long(valid | st << 8) | long(ma) << 16 | long(mb) << 40;  // masses < 2^17 (law.rs MAX_MASS)
}

// Stage 2: one candidate 4-momentum per thread (eight per pair).
kernel void rel_mom(device Ctl* ctl [[buffer(4)]],
                    constant Params& p [[buffer(5)]],
                    device const uint* mass [[buffer(10)]],
                    device const uint2* out [[buffer(14)]],
                    device long* rel [[buffer(30)]],
                    uint t [[thread_position_in_grid]]) {
    uint e = t / 8, z = t % 8;
    if (e >= atomic_load_explicit(&ctl->npairs, memory_order_relaxed)) return;
    device long* r = rel + e * REL_LONGS;
    long vs = r[7];
    if (((vs >> 8) & 255) != REL_EXCH || ((vs >> z) & 1) == 0) return;
    bool ok = true;
    long3 f = fourm(uint(z < 4 ? (vs >> 16) & 0xffffff : vs >> 40), slot(long4(r[3], r[4], r[5], r[6]), z), p.q, ok);
    f = mom_or_fail(f, ok);
    r[8 + 3 * z] = f.x;
    r[9 + 3 * z] = f.y;
    r[10 + 3 * z] = f.z;
}

// The Newtonian bounce (law::resolve) of one pair: `oa`, `ob` carry the energy; a's absorbs
// the pair's error.
static inline bool bounce(long2 d, uint ma, uint mb, thread long2& ka, thread long2& kb, thread long3& oa, long3 ob) {
    long en = 0, carry = oa.x;
    bool ok = impulse(d, ma, mb, ka, kb, oa.x + ob.x, en, carry);
    oa.x = carry;
    return ok;
}

// Momentum a wall takes from a bouncer flipping component ax: 2·m·k (Newtonian), 2·p
// (relativistic).
static inline long wall_take(constant Params& p, uint m, long2 k, uint ax, thread bool& ok) {
    if (LAW == 0) return long(m) * 2 * k[ax];
    long3 f = fourm(m, k, p.q, ok);
    return 2 * (ax == 0 ? f.y : f.z);
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
                         device long2* car [[buffer(15)]],
                         device const long* rel [[buffer(30)]],
                         uint e [[thread_position_in_grid]]) {
    uint np = atomic_load_explicit(&ctl->npairs, memory_order_relaxed);
    uint nw = atomic_load_explicit(&ctl->nwalls, memory_order_relaxed);
    uint a = 0, b = 0, fa = 0, fb = 0, ra = 0, rb = 0, ma = 0, mb = 0;
    long2 ka = 0, kb = 0, xa = 0, xb = 0, pa = 0, pb = 0;
    long ea = 0, eb = 0;
    bool mine = e < np;
    if (mine) {
        a = out[e].x;
        b = out[e].y;
        // Every gather at once: they are independent, and nearly every hit is an isolated
        // pair of bouncers.
        uint na = count_of(dy, a), nb = count_of(dy, b);
        fa = rf[a];
        fb = rf[b];
        ka = dy[a].k;
        kb = dy[b].k;
        ea = dy[a].res;
        eb = dy[b].res;
        ra = dy[a].rev;
        rb = dy[b].rev;
        if (LAW == 0) {
            xa = pos[a];
            xb = pos[b];
            ma = mass[a];
            mb = mass[b];
        } else {
            pa = car[a];
            pb = car[b];
        }
        mine = na == 1 && nb == 1;
    }
    uint other = uint(!mine && e < np + nw);
    uint lpre = simd_prefix_exclusive_sum(other), ltot = simd_sum(other), lbase = 0;
    if (simd_is_first() && ltot != 0) lbase = atomic_fetch_add_explicit(&ctl->nlist, ltot, memory_order_relaxed);
    lbase = simd_broadcast_first(lbase) + lpre;
    if (other != 0) list[lbase] = e;
    long2 oa = ka, ob = kb;
    long3 ca = 0;
    uint rva = 0, rvb = 0;
    bool ok = mine;
    if (mine) {
        if ((fa & BOUNCE) != 0 && (fb & BOUNCE) != 0) {
            if (LAW == 0) {
                ca = long3(ea, 0, 0);
                ok = bounce(xb - xa, ma, mb, ka, kb, ca, long3(eb, 0, 0));
            } else {
                // Stages 1 and 2 ran in classify and rel_mom.
                ca = long3(ea, pa);
                device const long* r = rel + e * REL_LONGS;
                uint vs = uint(r[7]), st = (vs >> 8) & 255;
                ok = st == REL_NONE || (st == REL_EXCH && rel_pick(ka, kb, ca, long3(eb, pb), long3(r[0], r[1], r[2]),
                                                                    long4(r[3], r[4], r[5], r[6]), vs & 255, r + 8));
            }
        }
        if ((fa & STOP) != 0) ka = 0;
        if ((fb & STOP) != 0) kb = 0;
        rva = ra + uint(any(ka != oa));
        rvb = rb + uint(any(kb != ob));
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
    if ((fa & BOUNCE) != 0 && (fb & BOUNCE) != 0) {
        dy[a].res = ca.x;
        if (LAW != 0) car[a] = ca.yz;
    }
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
                    device long2* car [[buffer(15)]],
                    device const long* rel [[buffer(30)]],
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
    long WE0[MAXB];  // energy carries
    long2 WP[MAXB];  // momentum carries (relativistic)
    uint cw = 0;
    for (uint q = 0; q < nb; ++q) {
        K[q] = K0[q] = dy[B[q]].k;
        WE0[q] = dy[B[q]].res;
        WP[q] = LAW == 0 ? long2(0) : car[B[q]];
    }
    bool ok = true;
    for (uint z = 0; z < npc && ok; ++z) {
        uint a = out[P[z]].x, b = out[P[z]].y, ia = 0, ib = 0;
        for (uint q = 0; q < nb; ++q) {
            if (B[q] == a) ia = q;
            if (B[q] == b) ib = q;
        }
        if ((rf[a] & BOUNCE) == 0 || (rf[b] & BOUNCE) == 0) continue;
        cw |= (1u << ia) | (1u << ib);
        long3 wa = long3(WE0[ia], WP[ia]);
        long3 wb = long3(WE0[ib], WP[ib]);
        if (LAW == 0) {
            ok = bounce(pos[b] - pos[a], mass[a], mass[b], K[ia], K[ib], wa, wb);
        } else if (all(K[ia] == K0[ia]) && all(K[ib] == K0[ib])) {
            // Both bodies still move as at the chronon's start: classify and rel_mom staged
            // this contact's reflection and candidate momenta (for every hit, isolated or
            // not); only the pick depends on the carries so far.
            ok = rel_staged(rel + P[z] * REL_LONGS, K[ia], K[ib], wa, wb);
        } else {
            ok = rel_bounce(p.q, pos[b] - pos[a], mass[a], mass[b], K[ia], K[ib], wa, wb);
        }
        WE0[ia] = wa.x;
        WP[ia] = wa.yz;
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
        long r2 = rf[x] & RADIUS;
        long2 y = pos[x];
        long2 lo = long2(p.bmin_x + r2, p.bmin_y + r2), hi = long2(p.bmax_x - r2, p.bmax_y - r2);
        for (uint ax = 0; ax < 2; ++ax) {
            if ((y[ax] <= lo[ax] && K[q][ax] < 0) || (y[ax] >= hi[ax] && K[q][ax] > 0)) {
                WM[q][ax] = wall_take(p, mass[x], K[q], ax, ok);
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
        if ((cw >> q) & 1) {
            dy[x].res = WE0[q];
            if (LAW != 0) car[x] = WP[q];
        }
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

// Test hook (gpu.rs `v1_momenta`): the v1 4-momentum of each (m, kx, ky), flat (see mom_of):
// io[4i..4i+3] holds (m, kx, ky, 0) in and (E, px, py, fail) out.
kernel void fourm1_probe(constant Params& p [[buffer(5)]],
                         device long* io [[buffer(30)]],
                         uint i [[thread_position_in_grid]]) {
    if (i >= p.n) return;
    device long* r = io + 4 * i;
    bool ok = true;
    long3 f = fourm1(uint(r[0]), long2(r[1], r[2]), p.q, ok);
    r[0] = f.x;
    r[1] = f.y;
    r[2] = f.z;
    r[3] = long(!ok);
}

// Test hook (gpu.rs `float_floors_probe`): float_floors on (T, 2S, p, n) given as 64-bit parts
// io[12i..12i+11] = (T.lo, T.hi, S2.lo, S2.hi, pE, px, py, n0, n1, n2, q, 0) in and
// (decided, fx, fy) at the start out.
kernel void floors_probe(constant Params& p [[buffer(5)]],
                         device long* io [[buffer(30)]],
                         uint i [[thread_position_in_grid]]) {
    if (i >= p.n) return;
    device long* r = io + 12 * i;
    w128 T, S2;
    T.lo = ulong(r[0]);
    T.hi = ulong(r[1]);
    S2.lo = ulong(r[2]);
    S2.hi = ulong(r[3]);
    long2 f = 0;
    bool decided = float_floors(r[10], w_float(T) * 0x1p-64f, w_float(S2) * 0x1p-64f, long3(r[4], r[5], r[6]), long3(r[7], r[8], r[9]), f);
    r[0] = long(decided);
    r[1] = f.x;
    r[2] = f.y;
}
