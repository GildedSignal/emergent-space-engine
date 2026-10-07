// The event queue's floor — run 20261007-0933-components-2aaa.
//
// Structures (keys are root-clock integer ticks; tie order (t, id) = (time, body id)):
//   heap4  — mirror of crates/space/src/events/calendar.rs: indexed 4-ary heap, one slot
//            per body, keys inline (16 B) + pos[] backpointers (4 B).
//   heap2  — same, arity 2 (a known-worse control).
//   wheel  — hierarchical timing wheel on u64 ticks: 4 levels x 2^16 intrusive
//            doubly-linked buckets, 24 B/slot, nonempty-bitmap skip-ahead, and a due-tick
//            batch drain delivered in id order (keeps the (t,id) contract exactly).
//
// Workload = the universe's per-event queue mix: pop the min, re-insert that slot at
// t + interval (intervals fixed per body, log2-uniform in [lo, hi]).
//
// gcc -O3 -march=native -o bench bench.c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <x86intrin.h>

#define NONE UINT32_MAX

typedef struct { uint64_t t; uint32_t id; } Key;
static inline int kless(Key a, Key b) { return a.t < b.t || (a.t == b.t && a.id < b.id); }

// ---------------------------------------------------------------- indexed heap
typedef struct { Key *heap; uint32_t *pos; size_t n; int arity; } IHeap;

static void ih_place(IHeap *h, size_t p, Key x) { h->heap[p] = x; h->pos[x.id] = (uint32_t)p; }

static void ih_up(IHeap *h, size_t p) {
    Key x = h->heap[p];
    while (p > 0) {
        size_t q = (p - 1) / h->arity;
        if (!kless(x, h->heap[q])) break;
        ih_place(h, p, h->heap[q]);
        p = q;
    }
    ih_place(h, p, x);
}

static void ih_down(IHeap *h, size_t p) {
    Key x = h->heap[p];
    size_t n = h->n;
    for (;;) {
        size_t first = (size_t)h->arity * p + 1;
        if (first >= n) break;
        size_t c = first, lim = first + h->arity;
        if (lim > n) lim = n;
        for (size_t k = first + 1; k < lim; k++) if (kless(h->heap[k], h->heap[c])) c = k;
        if (!kless(h->heap[c], x)) break;
        ih_place(h, p, h->heap[c]);
        p = c;
    }
    ih_place(h, p, x);
}

static void ih_remove_at(IHeap *h, size_t p) {          // mirrors Calendar::remove_at
    h->pos[h->heap[p].id] = NONE;
    Key last = h->heap[--h->n];
    if (p < h->n) {
        ih_place(h, p, last);
        ih_up(h, p);
        ih_down(h, h->pos[last.id]);
    }
}

static inline Key ih_pop_min(IHeap *h) { Key e = h->heap[0]; ih_remove_at(h, 0); return e; }
static inline void ih_insert(IHeap *h, Key x) { h->heap[h->n] = x; h->pos[x.id] = (uint32_t)h->n; h->n++; ih_up(h, h->n - 1); }

// ---------------------------------------------------------------- timing wheel
#define LB 16
#define WW (1u << LB)
#define WMASK (WW - 1)
#define LEV 4

typedef struct { uint64_t t; uint32_t prev, next, lvl; } Slot;   // 24 B

typedef struct {
    Slot *slots; size_t n;
    uint32_t *head;            // LEV * WW
    uint64_t *bm;              // WW/64 nonempty bits, level 0
    uint64_t now;
    uint32_t *deliver; uint32_t dlen, dpos; uint64_t deliver_t;
    uint32_t *scratch;
    size_t chain_max, chain_sum, drains, cascades;
} Wheel;

static inline uint32_t *wh_headp(Wheel *w, uint32_t l, uint32_t b) { return &w->head[(size_t)l * WW + b]; }

static void wh_link(Wheel *w, uint32_t i, uint64_t t) {
    Slot *s = &w->slots[i];
    s->t = t;
    uint32_t l = 0;
    while (l < LEV - 1 && (t >> (l * LB)) - (w->now >> (l * LB)) >= WW) l++;
    uint32_t b = (uint32_t)((t >> (l * LB)) & WMASK);
    s->lvl = l;
    s->prev = NONE;
    s->next = *wh_headp(w, l, b);
    if (s->next != NONE) w->slots[s->next].prev = i;
    *wh_headp(w, l, b) = i;
    if (l == 0) w->bm[b >> 6] |= 1ull << (b & 63);
}

static void wh_unlink(Wheel *w, uint32_t i) {
    Slot *s = &w->slots[i];
    uint32_t b = (uint32_t)((s->t >> (s->lvl * LB)) & WMASK);
    if (s->prev != NONE) w->slots[s->prev].next = s->next;
    else {
        *wh_headp(w, s->lvl, b) = s->next;
        if (s->lvl == 0 && s->next == NONE) w->bm[b >> 6] &= ~(1ull << (b & 63));
    }
    if (s->next != NONE) w->slots[s->next].prev = s->prev;
}

static void wh_cascade(Wheel *w, uint32_t lvl, uint32_t b) {
    w->cascades++;
    uint32_t i = *wh_headp(w, lvl, b);
    *wh_headp(w, lvl, b) = NONE;
    while (i != NONE) {
        uint32_t nxt = w->slots[i].next;
        w->slots[i].prev = w->slots[i].next = NONE;
        wh_link(w, i, w->slots[i].t);      // re-links at a lower level under the new now
        i = nxt;
    }
}

static uint32_t bm_next(Wheel *w, uint32_t from) {
    uint32_t w0 = from >> 6, off = from & 63;
    uint64_t word = w->bm[w0] >> off;
    if (word) return (w0 << 6) + off + (uint32_t)__builtin_ctzll(word);
    for (uint32_t j = w0 + 1; j < WW / 64; j++)
        if (w->bm[j]) return (j << 6) + (uint32_t)__builtin_ctzll(w->bm[j]);
    return NONE;
}

static int cmp_u32(const void *a, const void *b) {
    uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b;
    return (x > y) - (x < y);
}

static void sort_u32_radix(uint32_t *a, size_t n, uint32_t *tmp) {   // LSD, 8-bit passes
    for (int pass = 0; pass < 4; pass++) {
        size_t cnt[256] = {0};
        uint32_t sh = 8 * pass;
        for (size_t i = 0; i < n; i++) cnt[(a[i] >> sh) & 255]++;
        int nb = 0; for (int b = 0; b < 256; b++) if (cnt[b]) nb++;
        if (nb == 1) continue;
        size_t off[256]; off[0] = 0;
        for (int b = 1; b < 256; b++) off[b] = off[b - 1] + cnt[b - 1];
        for (size_t i = 0; i < n; i++) tmp[off[(a[i] >> sh) & 255]++] = a[i];
        memcpy(a, tmp, n * sizeof(uint32_t));
    }
}

static Key wh_pop_min(Wheel *w) {
    if (w->dpos < w->dlen) { Key k = { w->deliver_t, w->deliver[w->dpos++] }; return k; }
    for (;;) {
        uint64_t base = w->now & ~(uint64_t)WMASK;
        uint32_t b = bm_next(w, (uint32_t)(w->now & WMASK));
        if (b != NONE) {
            w->now = base + b;
            uint32_t i = *wh_headp(w, 0, b);
            size_t chain = 0;
            while (i != NONE) { w->deliver[chain++] = i; i = w->slots[i].next; }
            for (size_t j = 0; j < chain; j++) wh_unlink(w, w->deliver[j]);
            if (chain > 1) {
                if (chain <= 32) {                          // insertion sort
                    for (size_t j = 1; j < chain; j++) {
                        uint32_t v = w->deliver[j]; size_t k = j;
                        while (k > 0 && w->deliver[k - 1] > v) { w->deliver[k] = w->deliver[k - 1]; k--; }
                        w->deliver[k] = v;
                    }
                } else sort_u32_radix(w->deliver, chain, w->scratch);
            }
            if (chain > w->chain_max) w->chain_max = chain;
            w->chain_sum += chain; w->drains++;
            w->deliver_t = w->now; w->dlen = (uint32_t)chain; w->dpos = 1;
            Key k = { w->deliver_t, w->deliver[0] };
            return k;
        }
        // nothing due in the rest of this window: enter the next one, cascade down
        w->now = base + WW;
        uint64_t k1 = w->now >> LB;
        wh_cascade(w, 1, (uint32_t)(k1 & WMASK));
        if ((k1 & WMASK) == 0) {
            wh_cascade(w, 2, (uint32_t)((w->now >> (2 * LB)) & WMASK));
            if (((w->now >> (2 * LB)) & WMASK) == 0)
                wh_cascade(w, 3, (uint32_t)((w->now >> (3 * LB)) & WMASK));
        }
    }
}

// ---------------------------------------------------------------- harness
static uint64_t rng_state;
static uint64_t rnd(void) {
    rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17;
    return rng_state;
}

static double now_sec(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static int cmp_dbl(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

typedef struct {
    size_t pops; double ns_mean, p50, p99, p999, mx; uint64_t hash;
    size_t chain_max; double chain_mean; size_t cascades; size_t mem_bytes; int oracle_ok;
} Result;

#define BATCH 64

static void run(const char *stype, size_t N, unsigned lo, unsigned hi, uint64_t seed,
                size_t pops, int oracle_on, Result *r) {
    rng_state = seed * 0x9E3779B97F4A7C15ull + 1;
    uint64_t *interval = malloc(N * sizeof(uint64_t));
    Key *init = malloc(N * sizeof(Key));
    uint64_t *pend = oracle_on ? malloc(N * sizeof(uint64_t)) : NULL;
    for (size_t i = 0; i < N; i++) {
        unsigned k = lo + (unsigned)(rnd() % (hi - lo + 1));
        interval[i] = 1ull << k;
        init[i].t = 1 + rnd() % interval[i];   // stationary phase: due within one interval
        init[i].id = (uint32_t)i;
    }

    IHeap hh = {0}; Wheel ww = {0}; memset(r, 0, sizeof *r);
    if (!strcmp(stype, "wheel")) {
        ww.slots = calloc(N, sizeof(Slot));
        ww.head = malloc((size_t)LEV * WW * sizeof(uint32_t));
        for (size_t i = 0; i < (size_t)LEV * WW; i++) ww.head[i] = NONE;
        ww.bm = calloc(WW / 64, sizeof(uint64_t));
        ww.deliver = malloc(N * sizeof(uint32_t));
        ww.scratch = malloc(N * sizeof(uint32_t));
        ww.now = 0; ww.dlen = ww.dpos = 0; ww.deliver_t = 0;
        for (size_t i = 0; i < N; i++) wh_link(&ww, (uint32_t)i, init[i].t);
        r->mem_bytes = N * sizeof(Slot) + (size_t)LEV * WW * 4 + WW / 8 + N * 4;
    } else {
        hh.arity = !strcmp(stype, "heap4") ? 4 : 2;
        hh.heap = malloc(N * sizeof(Key));
        hh.pos = malloc(N * sizeof(uint32_t));
        memset(hh.pos, 0xFF, N * sizeof(uint32_t));
        hh.n = 0;
        for (size_t i = 0; i < N; i++) ih_insert(&hh, init[i]);
        r->mem_bytes = N * (sizeof(Key) + 4);
    }
    if (oracle_on) for (size_t i = 0; i < N; i++) pend[i] = init[i].t;

    uint64_t hash = 1469598103934665603ull;
    double wall0 = now_sec();

#define POP_HEAP()   ih_pop_min(&hh)
#define POP_WHEEL()  wh_pop_min(&ww)
#define LOOP(POP)                                                                     \
    for (size_t p = 0; p < pops; p++) {                                               \
        Key e = POP();                                                                \
        uint64_t t2 = e.t + interval[e.id];                                           \
        if (oracle_on && p < 20000) {                                                 \
            Key best = { UINT64_MAX, NONE };                                          \
            for (size_t j = 0; j < N; j++)                                            \
                if (pend[j] < best.t || (pend[j] == best.t && (uint32_t)j < best.id)) \
                    { best.t = pend[j]; best.id = (uint32_t)j; }                      \
            if (best.t != e.t || best.id != e.id) {                                   \
                fprintf(stderr, "ORACLE FAIL pop %zu: got (%llu,%u) want (%llu,%u)\n",\
                        p, (unsigned long long)e.t, e.id,                             \
                        (unsigned long long)best.t, best.id);                         \
                exit(9);                                                              \
            }                                                                         \
        }                                                                             \
        hash ^= (unsigned long long)e.t; hash *= 1099511628211ull;                    \
        hash ^= e.id; hash *= 1099511628211ull;                                       \
        if (oracle_on) pend[e.id] = t2;                                               \
        if (is_wheel) wh_link(&ww, e.id, t2);                                        \
        else ih_insert(&hh, (Key){ t2, e.id });                                       \
    }

    wall0 = now_sec();
    int is_wheel = !strcmp(stype, "wheel");
    if (is_wheel) LOOP(POP_WHEEL) else LOOP(POP_HEAP)
    double wall = now_sec() - wall0;
    r->pops = pops; r->hash = hash; r->ns_mean = wall * 1e9 / pops;
    r->oracle_ok = 1;

    free(interval); free(init); free(pend);
    free(hh.heap); free(hh.pos);
    free(ww.slots); free(ww.head); free(ww.bm); free(ww.deliver); free(ww.scratch);
}

// Tail pass: identical loop but timing each BATCH ops with rdtsc, fewer pops.
static void run_tails(const char *stype, size_t N, unsigned lo, unsigned hi, uint64_t seed,
                      size_t pops, Result *r) {
    rng_state = seed * 0x9E3779B97F4A7C15ull + 1;
    uint64_t *interval = malloc(N * sizeof(uint64_t));
    Key *init = malloc(N * sizeof(Key));
    for (size_t i = 0; i < N; i++) {
        unsigned k = lo + (unsigned)(rnd() % (hi - lo + 1));
        interval[i] = 1ull << k;
        init[i].t = 1 + rnd() % interval[i];   // stationary phase: due within one interval
        init[i].id = (uint32_t)i;
    }
    IHeap hh = {0}; Wheel ww = {0};
    if (!strcmp(stype, "wheel")) {
        ww.slots = calloc(N, sizeof(Slot));
        ww.head = malloc((size_t)LEV * WW * sizeof(uint32_t));
        for (size_t i = 0; i < (size_t)LEV * WW; i++) ww.head[i] = NONE;
        ww.bm = calloc(WW / 64, sizeof(uint64_t));
        ww.deliver = malloc(N * sizeof(uint32_t));
        ww.scratch = malloc(N * sizeof(uint32_t));
        ww.now = 0; ww.dlen = ww.dpos = 0;
        for (size_t i = 0; i < N; i++) wh_link(&ww, (uint32_t)i, init[i].t);
    } else {
        hh.arity = !strcmp(stype, "heap4") ? 4 : 2;
        hh.heap = malloc(N * sizeof(Key));
        hh.pos = malloc(N * sizeof(uint32_t));
        memset(hh.pos, 0xFF, N * sizeof(uint32_t));
        hh.n = 0;
        for (size_t i = 0; i < N; i++) ih_insert(&hh, init[i]);
    }
    size_t max_batches = 1 << 13;
    double *bat = malloc(max_batches * sizeof(double));
    size_t nbat = 0;

    // tsc frequency
    uint64_t c0 = __rdtsc(); double w0 = now_sec();
    struct timespec req = { 0, 100000000 }; nanosleep(&req, NULL);
    double mhz = (__rdtsc() - c0) / ((now_sec() - w0) * 1e9);   // cycles per ns

    int is_wheel = !strcmp(stype, "wheel");
    size_t warm = pops / 10;
    for (size_t p = 0; p < warm; p++) {
        Key e = is_wheel ? wh_pop_min(&ww) : ih_pop_min(&hh);
        uint64_t t2 = e.t + interval[e.id];
        if (is_wheel) wh_link(&ww, e.id, t2); else ih_insert(&hh, (Key){ t2, e.id });
    }
    if (!strcmp(stype, "wheel")) { r->chain_max = ww.chain_max; r->chain_mean = ww.drains ? (double)ww.chain_sum / ww.drains : 0; r->cascades = ww.cascades; }

    for (size_t p = 0; p < pops; p += BATCH) {
        uint64_t c0b = __rdtsc();
        for (size_t q = 0; q < BATCH; q++) {
            Key e = is_wheel ? wh_pop_min(&ww) : ih_pop_min(&hh);
            uint64_t t2 = e.t + interval[e.id];
            if (is_wheel) wh_link(&ww, e.id, t2); else ih_insert(&hh, (Key){ t2, e.id });
        }
        if (nbat < max_batches) bat[nbat++] = (double)(__rdtsc() - c0b) / BATCH / mhz;   // ns/op
        else bat[max_batches - 1] += 0; // saturate: stop recording
    }
    if (!strcmp(stype, "wheel")) { if (ww.chain_max > r->chain_max) r->chain_max = ww.chain_max; r->cascades = ww.cascades; }
    qsort(bat, nbat, sizeof(double), cmp_dbl);
    r->p50 = bat[nbat / 2];
    r->p99 = bat[(size_t)(nbat * 0.99)];
    r->p999 = bat[(size_t)(nbat * 0.999)];
    r->mx = bat[nbat - 1];

    free(bat); free(interval); free(init);
    free(hh.heap); free(hh.pos);
    free(ww.slots); free(ww.head); free(ww.bm); free(ww.deliver); free(ww.scratch);
}

int main(int argc, char **argv) {
    if (argc < 7) {
        fprintf(stderr, "usage: bench struct N lo hi seed pops [oracle]\n");
        return 2;
    }
    const char *stype = argv[1];
    size_t N = strtoull(argv[2], NULL, 10);
    unsigned lo = (unsigned)atoi(argv[3]), hi = (unsigned)atoi(argv[4]);
    uint64_t seed = strtoull(argv[5], NULL, 10);
    size_t pops = strtoull(argv[6], NULL, 10);
    int oracle_on = argc > 7 ? atoi(argv[7]) : (N <= 10000 ? 1 : 0);

    Result r = {0};
    run(stype, N, lo, hi, seed, pops, oracle_on, &r);
    size_t tail_pops = pops < 65536 ? pops : 65536;
    Result t = {0};
    run_tails(stype, N, lo, hi, seed, tail_pops, &t);
    r.p50 = t.p50; r.p99 = t.p99; r.p999 = t.p999; r.mx = t.mx;
    r.chain_max = t.chain_max; r.chain_mean = t.chain_mean; r.cascades = t.cascades;

    printf("{\"struct\":\"%s\",\"N\":%zu,\"lo\":%u,\"hi\":%u,\"seed\":%llu,\"pops\":%zu,"
           "\"ns_mean\":%.2f,\"p50\":%.2f,\"p99\":%.2f,\"p999\":%.2f,\"max\":%.2f,"
           "\"hash\":\"%016llx\",\"chain_max\":%zu,\"chain_mean\":%.1f,\"cascades\":%zu,"
           "\"mem_bytes\":%zu,\"oracle\":\"%s\"}\n",
           stype, N, lo, hi, (unsigned long long)seed, r.pops, r.ns_mean, r.p50, r.p99,
           r.p999, r.mx, (unsigned long long)r.hash, r.chain_max, r.chain_mean, r.cascades,
           r.mem_bytes, oracle_on ? "checked" : "off");
    return 0;
}
