// The GPU half of MetalChronon (es-lattice-elastic-v0). Per chronon: the snapshot (bin,
// scan_reduce, scan_sums, scan_final, scatter), detection (pairs), advance with the wall set,
// then in one-chronon buffers the settling of isolated contacts (tally, classify, settle,
// unmark) and the next chronon's snapshot; `prune` every 64 chronons. Every value is an exact
// integer: gpu.rs checks before each batch that C·(K + 1) ≤ 2^28 (every product below 2^62,
// every narrowed field in range) and that cell coordinates fit i32. In multi-chronon buffers,
// once a chronon emits a pair or a wall the later ones see the counters and do nothing: the
// CPU must respond before the next detection.
#include <metal_stdlib>
using namespace metal;

// Mirrors `Params` in gpu.rs. Scalar longs: a long2 would align to 16 and shift the layout.
struct Params {
    long cell;
    long bmin_x, bmin_y, bmax_x, bmax_y;
    uint n, wbits, hmask, has_box, pair_cap, step, nblocks;
    uint tail;  // this snapshot follows an eventful chronon in the same buffer: ignore halting
    uint fuse;  // advance also bins the new positions (the following snapshot skips bin)
};

// A body's cell and its rank among the bodies binned into the same bucket.
struct Bin {
    packed_int2 c;
    uint rank;
};

struct Ctl {
    atomic_uint npairs;
    atomic_uint nwalls;
    uint go;    // this chronon runs (written by scan_sums)
    uint done;  // chronons of this batch that ran
};

// Detection snapshot at t-1 in bucket order (32 bytes; the scan reads c and idx first).
// Position relative to its cell's corner (in [0, C), C ≤ 2^28), velocity |k_c| ≤ K < 2^14:
// exact when narrowed.
struct Rec {
    int2 c;
    uint idx, mask;  // mask: bit j & 31 set if the table may hold a contact (idx, j)
    uint2 xr;
    short2 k;
    uint rf;  // radius | stop << 30 | bouncer << 31 (below)
};

// rf: radius (exact in 28 bits whenever the GPU path runs: radius ≤ C/2 ≤ 2^27) | flags.
constant uint RADIUS = 0x0fffffffu;
constant uint STOP = 1u << 30;
constant uint BOUNCE = 1u << 31;

// A consumed contact (lower index owns it): partner, own revision, partner revision.
struct Slot {
    uint j, ri, rj;
};

constant uint SLOTS = 8;
constant uint BLOCK = 1024;  // buckets per scan threadgroup (256 threads × 4)

// floor(x / c) for c ≥ 1, as the law's div_euclid. 64-bit `/` is emulated and was two thirds
// of the binning time, so float quotients shrink the remainder (each by ~2^22) and integer
// steps finish; q·c + r = x holds throughout, so the result is exact.
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

static inline int2 cell_of(long2 x, long cell) {
    return int2(fdiv(x.x, cell), fdiv(x.y, cell));
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

static inline bool halted(device Ctl* ctl) {
    return (atomic_load_explicit(&ctl->npairs, memory_order_relaxed) |
            atomic_load_explicit(&ctl->nwalls, memory_order_relaxed)) != 0;
}

static inline void bin_one(long2 x, uint i, device atomic_uint* count, device Bin* bins, constant Params& p) {
    int2 c = cell_of(x, p.cell);
    Bin b;
    b.c = c;
    b.rank = atomic_fetch_add_explicit(&count[bucket(c, p)], 1u, memory_order_relaxed);
    bins[i] = b;
}

kernel void bin(device const long2* pos [[buffer(0)]],
                device atomic_uint* count [[buffer(1)]],
                device Bin* bins [[buffer(2)]],
                device Ctl* ctl [[buffer(4)]],
                constant Params& p [[buffer(5)]],
                uint i [[thread_position_in_grid]]) {
    if (i >= p.n || (p.tail == 0 && halted(ctl))) return;
    bin_one(pos[i], i, count, bins, p);
}

// Bucket starts by reduce-then-scan: block totals, their exclusive scan, then each block's
// local scan plus its offset. 256 threads × 4 buckets per block.
kernel void scan_reduce(device const uint4* count [[buffer(1)]],
                        device Ctl* ctl [[buffer(4)]],
                        constant Params& p [[buffer(5)]],
                        device uint* bsum [[buffer(16)]],
                        threadgroup uint* sh [[threadgroup(0)]],
                        uint t [[thread_position_in_threadgroup]],
                        uint g [[threadgroup_position_in_grid]],
                        uint lane [[thread_index_in_simdgroup]],
                        uint sg [[simdgroup_index_in_threadgroup]]) {
    if (p.tail == 0 && halted(ctl)) return;
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

// One threadgroup; each thread a contiguous run of blocks. Decides whether this chronon
// runs and closes the last bucket (start[H] = n).
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
    if (p.tail == 0 && halted(ctl)) {
        if (t == 0) ctl->go = 0;
        return;
    }
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
    if (t == 0) {
        ctl->go = 1;
        if (p.tail == 0) ctl->done = p.step + 1;
    }
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

// Snapshot into bucket order. In one-chronon buffers it runs right after the previous
// chronon's detection and settling, before the CPU has resolved the remaining contacts, so
// gpu.rs patches the records of the bodies that CPU response changed.
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
    long2 x = pos[i];
    int2 c = int2(q.c);
    Rec rec;
    rec.c = c;
    rec.idx = i;
    rec.mask = mask[i];
    rec.xr = uint2(x - long2(c) * p.cell);
    rec.k = kq[i];
    rec.rf = rf[i];
    recs[start[bucket(c, p)] + q.rank] = rec;
}

// A candidate that passed the box filter: reject it in float when the float values prove
// it cannot hit (not approaching, or its line of motion stays beyond reach), else run the
// exact predicate and append a hit. Float products of |d_c| < 2^29 and |w_c| < 2^15 carry a
// relative error below 2^-22, far inside the 2^-18 margins, so no hit is ever rejected.
static inline void try_pair(int2 d, int2 w, uint reach, uint ia, uint ib, device Ctl* ctl, device uint2* out, uint cap) {
    float2 df = float2(d), wf = float2(w);
    float px = df.x * wf.x, py = df.y * wf.y;
    if (px + py > 0x1p-18f * (fabs(px) + fabs(py))) return;  // dw > 0
    float cx = df.x * wf.y, cy = df.y * wf.x;
    float cross = fabs(cx - cy) - 0x1p-18f * (fabs(cx) + fabs(cy));
    float rf = float(reach), ww = wf.x * wf.x + wf.y * wf.y;
    if (cross > 0 && cross * cross > rf * rf * ww * (1 + 0x1p-18f)) return;  // line beyond reach
    if (hit(d, w, reach)) {
        uint o = atomic_fetch_add_explicit(&ctl->npairs, 1u, memory_order_relaxed);
        if (o < cap) out[o] = uint2(ia, ib);
    }
}

// One thread per record, in bucket (spatial) order. For each of the three rows of cells
// around a, read the records of the row's three buckets (one run unless the torus wraps) and
// keep partners j > i in exactly the 3×3 reference cells (each pair once). Contacts consumed
// at the current revisions are skipped (the mask bit gates the table read); the rest count
// as predicates. A 32-bit necessary condition (|d_c| ≤ reach + |w_c|: the pair must come
// within reach during the bin) drops most of them, a float one most of the rest, so the
// 64-bit predicate runs on few divergent iterations.
kernel void pairs(device Ctl* ctl [[buffer(4)]],
                  constant Params& p [[buffer(5)]],
                  device const uint* start [[buffer(6)]],
                  device const uint* rev [[buffer(9)]],
                  device const Rec* recs [[buffer(11)]],
                  device const Slot* table [[buffer(13)]],
                  device uint2* out [[buffer(14)]],
                  device atomic_uint* pred [[buffer(15)]],
                  threadgroup uint* sh [[threadgroup(0)]],
                  uint s [[thread_position_in_grid]],
                  uint t [[thread_position_in_threadgroup]],
                  uint lane [[thread_index_in_simdgroup]],
                  uint sg [[simdgroup_index_in_threadgroup]],
                  uint nsg [[simdgroups_per_threadgroup]]) {
    uint tested = 0;
    if (s < p.n && ctl->go != 0) {
        Rec a = recs[s];
        int C = int(p.cell);
        uint wmask = (1u << p.wbits) - 1;
        uint hx = (uint(a.c.x) - 1) & wmask;
        bool whole = hx + 2 <= wmask;
        for (int dy = -1; dy <= 1; ++dy) {
            uint hrow = ((uint(a.c.y) + uint(dy)) << p.wbits) & p.hmask;
            for (uint part = 0; part < (whole ? 1u : 3u); ++part) {
                uint h = hrow + (whole ? hx : ((hx + part) & wmask));
                for (uint u = start[h], e = start[h + (whole ? 3 : 1)]; u < e; ++u) {
                    device const Rec& b = recs[u];
                    // Exact adjacency, modulo 2^32 so aliased far cells cannot overflow.
                    uint2 rel = uint2(b.c) - uint2(a.c) + 1;
                    if (rel.x > 2 || rel.y > 2 || b.idx <= a.idx) continue;
                    if ((a.mask >> (b.idx & 31)) & 1) {
                        bool eaten = false;
                        uint ra = rev[a.idx], rb = rev[b.idx];  // live revisions (the response may have moved them)
                        for (uint m = 0; m < SLOTS; ++m) {
                            Slot sl = table[a.idx * SLOTS + m];
                            eaten = eaten || (sl.j == b.idx && sl.ri == ra && sl.rj == rb);
                        }
                        if (eaten) continue;
                    }
                    ++tested;
                    int2 d = int2(b.xr) - int2(a.xr) + (int2(rel) - 1) * C, w = int2(b.k) - int2(a.k);
                    uint reach = (a.rf & RADIUS) + (b.rf & RADIUS);
                    if (uint(abs(d.x)) > reach + uint(abs(w.x)) || uint(abs(d.y)) > reach + uint(abs(w.y))) continue;
                    try_pair(d, w, reach, a.idx, b.idx, ctl, out, p.pair_cap);
                }
            }
        }
    }
    // Predicate count per chronon as a 64-bit (lo, hi) pair with carry, one atomic per
    // threadgroup.
    uint sum = simd_sum(tested);
    if (lane == 0) sh[sg] = sum;
    threadgroup_barrier(mem_flags::mem_threadgroup);
    if (t == 0) {
        uint total = 0;
        for (uint g = 0; g < nsg; ++g) total += sh[g];
        if (total != 0) {
            uint old = atomic_fetch_add_explicit(&pred[2 * p.step], total, memory_order_relaxed);
            if (old + total < old) atomic_fetch_add_explicit(&pred[2 * p.step + 1], 1u, memory_order_relaxed);
        }
    }
}

// Advance to t and collect the wall set there, in index order (coalesced). Runs after
// `pairs`, which reads only the snapshot.
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
    if (p.fuse != 0) bin_one(y, i, count, bins, p);
    uint f = rf[i];
    if (p.has_box != 0 && (f & BOUNCE) != 0) {
        long r = f & RADIUS;
        bool w = (k.x < 0 && y.x <= p.bmin_x + r) || (k.x > 0 && y.x >= p.bmax_x - r) ||
                 (k.y < 0 && y.y <= p.bmin_y + r) || (k.y > 0 && y.y >= p.bmax_y - r);
        if (w) walls[atomic_fetch_add_explicit(&ctl->nwalls, 1u, memory_order_relaxed)] = i;
    }
}

// ---- Settling isolated contacts on the GPU -------------------------------------------------
// A contact whose two bodies are in no other contact and not in the wall set is a connected
// component of its own, and components resolve independently (law.rs). `settle` applies
// law::resolve to such a pair, consumes it and reports it; everything else (and any pair
// whose arithmetic might leave i64) is left to the CPU.

// Result per hit, read by the CPU.
struct Info {
    ulong ida, idb;
    int koa, kna, kob, knb;  // max|k_c| before and after, for the CPU's max|k| histogram
    uint status;             // SETTLED, SETTLED_UNCONSUMED (table row full) or FOR_CPU
    uint pad;
};

constant uint SETTLED = 0, SETTLED_UNCONSUMED = 1, FOR_CPU = 2;

// Indirect grid sizes for the settle kernels: hits and walls, then hits only.
kernel void tally(device Ctl* ctl [[buffer(4)]],
                  constant Params& p [[buffer(5)]],
                  device uint* args [[buffer(23)]]) {
    uint np = atomic_load_explicit(&ctl->npairs, memory_order_relaxed);
    uint nw = atomic_load_explicit(&ctl->nwalls, memory_order_relaxed);
    if (np > p.pair_cap) np = nw = 0;  // truncated: the CPU reruns the chronon
    args[0] = (np + nw + 255) / 256; args[1] = 1; args[2] = 1;
    args[3] = (np + 255) / 256; args[4] = 1; args[5] = 1;
}

static inline uint involved(device Ctl* ctl, device const uint2* out, device const uint* walls,
                            uint i, thread uint& a, thread uint& b) {
    uint np = atomic_load_explicit(&ctl->npairs, memory_order_relaxed);
    uint nw = atomic_load_explicit(&ctl->nwalls, memory_order_relaxed);
    if (i < np) { a = out[i].x; b = out[i].y; return 2; }
    if (i < np + nw) { a = walls[i - np]; return 1; }
    return 0;
}

kernel void classify(device Ctl* ctl [[buffer(4)]],
                     device const uint* walls [[buffer(12)]],
                     device const uint2* out [[buffer(14)]],
                     device atomic_uint* cnt [[buffer(19)]],
                     uint i [[thread_position_in_grid]]) {
    uint a = 0, b = 0, m = involved(ctl, out, walls, i, a, b);
    if (m >= 1) atomic_fetch_add_explicit(&cnt[a], 1u, memory_order_relaxed);
    if (m == 2) atomic_fetch_add_explicit(&cnt[b], 1u, memory_order_relaxed);
}

kernel void unmark(device Ctl* ctl [[buffer(4)]],
                   device const uint* walls [[buffer(12)]],
                   device const uint2* out [[buffer(14)]],
                   device uint* cnt [[buffer(19)]],
                   uint i [[thread_position_in_grid]]) {
    uint a = 0, b = 0, m = involved(ctl, out, walls, i, a, b);
    if (m >= 1) cnt[a] = 0;
    if (m == 2) cnt[b] = 0;
}

// v.div_euclid(den) for den > 0.
static inline long floor_div(long v, long den) {
    long q = v / den;
    return q * den > v ? q - 1 : q;
}

static inline long energy(long m, long2 k) {
    return m * (k.x * k.x + k.y * k.y);
}

static inline int kval(long2 k) {
    return int(max(abs(k.x), abs(k.y)));
}

kernel void settle(device const long2* pos [[buffer(0)]],
                   device long2* vel [[buffer(3)]],
                   device Ctl* ctl [[buffer(4)]],
                   constant Params& p [[buffer(5)]],
                   device short2* kq [[buffer(7)]],
                   device const uint* rf [[buffer(8)]],
                   device uint* rev [[buffer(9)]],
                   device const uint* mass [[buffer(10)]],
                   device Slot* table [[buffer(13)]],
                   device const uint2* out [[buffer(14)]],
                   device uint* mask [[buffer(18)]],
                   device const uint* cnt [[buffer(19)]],
                   device Info* info [[buffer(20)]],
                   device long* res [[buffer(21)]],
                   device const ulong* ids [[buffer(22)]],
                   uint i [[thread_position_in_grid]]) {
    if (i >= atomic_load_explicit(&ctl->npairs, memory_order_relaxed)) return;
    uint a = out[i].x, b = out[i].y;
    Info inf;
    inf.status = FOR_CPU;
    if (cnt[a] != 1 || cnt[b] != 1) { info[i] = inf; return; }
    uint fa = rf[a], fb = rf[b];
    long2 ka = vel[a], kb = vel[b], na = ka, nb = kb;
    long ra = res[a], rb = res[b], e = 0;
    bool bounce = (fa & BOUNCE) != 0 && (fb & BOUNCE) != 0;
    if (bounce) {
        long2 d = pos[b] - pos[a], w = kb - ka;  // |d_c| ≤ reach + |w| < 2^29 after a hit
        long dotp = d.x * w.x + d.y * w.y, dd = d.x * d.x + d.y * d.y;
        if (dotp < 0 && dd != 0) {
            long ma = mass[a], mb = mass[b], x = ma, y = mb;
            while (y != 0) { long r = x % y; x = y; y = r; }
            long lcm = ma / x * mb;
            // Stay in i64: den, num and the carry must be far from 2^63 (float bounds with
            // a factor 4 of slack); otherwise the CPU resolves this pair in i128.
            float lim = 0x1p61f;
            float fden = float(ma + mb) * float(dd) * float(lcm);
            float fnum = float(max(abs(d.x), abs(d.y))) * 2.0f * float(ma) * float(mb) * float(-dotp);
            if (fden >= lim || fnum >= lim || abs(ra) >= (1l << 60) || abs(rb) >= (1l << 60)) {
                info[i] = inf;
                return;
            }
            long den = (ma + mb) * dd * lcm, f = 2 * ma * mb * dotp;
            long2 num = d * f;
            bool nonzero = num.x != 0 || num.y != 0;
            long2 lo = long2(floor_div(num.x, den), floor_div(num.y, den));
            long2 hi = long2(-floor_div(-num.x, den), -floor_div(-num.y, den));
            long2 cands[4];
            uint nc = 0;
            for (uint u = 0; u < 2; ++u) {
                for (uint v = 0; v < 2; ++v) {
                    long2 c = long2(u == 0 ? lo.x : hi.x, v == 0 ? lo.y : hi.y);
                    bool dup = all(c == 0) && nonzero;
                    for (uint q = 0; q < nc; ++q) dup = dup || all(cands[q] == c);
                    if (!dup) cands[nc++] = c;
                }
            }
            long owed = ra + rb, best = 0;
            long e0 = energy(ma, ka) + energy(mb, kb);
            for (uint q = 0; q < nc; ++q) {
                long2 da = cands[q] * (lcm / ma), db = -cands[q] * (lcm / mb);
                long ec = energy(ma, ka + da) + energy(mb, kb + db) - e0;
                long score = abs(owed + ec);
                if (q == 0 || score < best) {
                    best = score;
                    e = ec;
                    na = ka + da;
                    nb = kb + db;
                }
            }
        }
    }
    if ((fa & STOP) != 0) na = 0;
    if ((fb & STOP) != 0) nb = 0;
    inf.ida = ids[a];
    inf.idb = ids[b];
    inf.koa = kval(ka);
    inf.kna = kval(na);
    inf.kob = kval(kb);
    inf.knb = kval(nb);
    uint rva = rev[a] + uint(any(na != ka)), rvb = rev[b] + uint(any(nb != kb));
    if (bounce) res[a] = ra + e;
    vel[a] = na;
    vel[b] = nb;
    kq[a] = short2(na);
    kq[b] = short2(nb);
    rev[a] = rva;
    rev[b] = rvb;
    // A body that revised has only dead contacts in its row: drop them, so its mask stays a
    // tight filter (dead entries never match; the reference keeps them until its prune).
    for (uint m = 0; m < SLOTS; ++m) {
        if (any(na != ka)) table[a * SLOTS + m].j = 0xffffffffu;
        if (any(nb != kb)) table[b * SLOTS + m].j = 0xffffffffu;
    }
    if (any(na != ka)) mask[a] = 0;
    if (any(nb != kb)) mask[b] = 0;
    // Consume at the new revisions in a's row (only this thread touches it): b's own slot,
    // an empty one, or one written at an older revision of a.
    inf.status = SETTLED_UNCONSUMED;
    uint pick = SLOTS;
    for (uint m = 0; m < SLOTS; ++m) {
        Slot s = table[a * SLOTS + m];
        if (s.j == b) { pick = m; break; }
        if (pick == SLOTS && (s.j == 0xffffffffu || s.ri != rva)) pick = m;
    }
    if (pick < SLOTS) {
        Slot s;
        s.j = b;
        s.ri = rva;
        s.rj = rvb;
        table[a * SLOTS + pick] = s;
        mask[a] |= 1u << (b & 31);
        inf.status = SETTLED;
    }
    info[i] = inf;
}


// The reference's pruning of consumed contacts (every 64 chronons): keep an entry only while
// both revisions are current and the pair is approaching; rebuild the masks. The dot product
// is exact in i64 while |d_c|, |w_c| < 2^30; a larger pair is kept and sets `fault`, and
// gpu.rs then prunes on the CPU in i128.
kernel void prune(device const long2* pos [[buffer(0)]],
                  device const long2* vel [[buffer(3)]],
                  constant Params& p [[buffer(5)]],
                  device const uint* rev [[buffer(9)]],
                  device Slot* table [[buffer(13)]],
                  device uint* mask [[buffer(18)]],
                  device atomic_uint* fault [[buffer(24)]],
                  uint i [[thread_position_in_grid]]) {
    if (i >= p.n) return;
    uint m = 0;
    bool far = false;
    for (uint k = 0; k < SLOTS; ++k) {
        Slot s = table[i * SLOTS + k];
        if (s.j == 0xffffffffu) continue;
        long2 d = pos[s.j] - pos[i], w = vel[s.j] - vel[i];
        bool big = any(abs(d) >= (1l << 30)) || any(abs(w) >= (1l << 30));
        far = far || big;
        bool live = s.ri == rev[i] && s.rj == rev[s.j] && !big && d.x * w.x + d.y * w.y < 0;
        if (live || big) {
            m |= 1u << (s.j & 31);
        } else {
            table[i * SLOTS + k].j = 0xffffffffu;
        }
    }
    mask[i] = m;
    if (far) atomic_store_explicit(fault, 1u, memory_order_relaxed);
}
