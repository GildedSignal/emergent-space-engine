// Kick price: ns, accounted bytes and tail of the law's kick stream.
// Measures the MEMORY floor of applying scheduled integer kicks to body
// state (the 16 B Tube: x,y,vx,vy as 4xi32 quanta), per law.md
// ("32-bit storage words", "kicks are integers of the law").
//
// Variants (identical arithmetic per body: two adds):
//   memcpy      : streaming bandwidth ceiling of this box (read+write).
//   i32/i32w/f64: word width of body+kick records, sorted (sweep) order.
//                 i32  packs the kick record to 12 B; i32w uses 16 B
//                 (one record per 4 B word, line-friendly).
//   shuffled    : same as i32, but kick order permuted (a player's wake).
//   cell_always : K=128 bodies per cell; uniform component applied each epoch.
//   cell_skip   : per-cell sub-quantum accumulator (PRINCIPLES #6): the cell
//                 accumulates the uniform far-field component in an integer
//                 remainder and touches NO body until a quantum crosses.
//                 Exact by construction: applied = (sum(u) - R_final) >> F.
//
// Bytes charged per kick (the DRAM floor when N >> cache):
//   i32  sorted : 12 (kick read) + 16 (body read) + 16 (body writeback) = 44
//   i32w sorted : 16 + 16 + 16 = 48
//   f64  sorted : 24 + 32 + 32 = 88
//   cell_*      : per scheduled epoch 16 (cell record); per touched body 32
//
// Reporting: median sweep (capacity) and per-64Ki-chunk tail across ALL
// sweeps (smoothness). Checksums printed so nothing can be elided.
//
// Build: cc -O3 -march=native -o kickprice kickprice.c
// Run:   ./kickprice [sweeps]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <math.h>

static uint64_t rng_s;
static inline uint64_t u64rand(void) {
    uint64_t x = rng_s;
    x ^= x >> 12; x ^= x << 25; x ^= x >> 27;
    rng_s = x;
    return x * 2685821657736338717ULL;
}
static inline double urand(void) { return (double)(u64rand() >> 11) / 9007199254740992.0; }
static inline int64_t heavy_step(void) { // |u| >= 2^20, sign-symmetric, P(|u|>x) ~ (2^20/x)^3
    double U = urand(); if (U < 1e-6) U = 1e-6;
    return ((u64rand() & 1) ? 1 : -1) * (int64_t)((1.0 / cbrt(U)) * 1048576.0);
}

static double now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1e9 + ts.tv_nsec;
}
static int cmp_u64(const void *a, const void *b) {
    uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b;
    return (x > y) - (x < y);
}
static int cmp_double(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}
#define CHUNKD 65536.0
static void tail(const char *tag, const uint64_t *v, size_t n) {
    uint64_t *w = malloc(n * sizeof(uint64_t));
    memcpy(w, v, n * sizeof(uint64_t));
    qsort(w, n, sizeof(uint64_t), cmp_u64);
    printf("  %-12s p50=%.2f p99=%.2f p99.9=%.2f max=%.2f ns/event\n", tag,
           (double)w[n / 2] / CHUNKD, (double)w[(size_t)(n * 0.99)] / CHUNKD,
           (double)w[(size_t)(n * 0.999)] / CHUNKD, (double)w[n - 1] / CHUNKD);
    free(w);
}

typedef struct { int32_t x, y, vx, vy; } BodyI;             // 16 B Tube
typedef struct { double x, y, vx, vy; } BodyF;              // 32 B
typedef struct { uint32_t id; int32_t dE, dL; } KickI;      // 12 B packed
typedef struct { uint32_t id; int32_t dE, dL, pad; } KickW; // 16 B
typedef struct { uint64_t id; double dE, dL; } KickF;       // 24 B
typedef struct { int64_t R; uint32_t base; int32_t pad; } Cell; // 16 B

#define NB (4u << 20)   /* 4 Mi bodies: 64 MB in i32, past the 32 MiB L3 */
#define K 128           /* bodies per cell (shipmem's packed block) */
#define CHUNK (1u << 16)
#define MAXSW 64

static BodyI *bi; static BodyF *bf; static KickI *ki; static KickW *kw;
static KickF *kf; static Cell *cells; static uint32_t *order;
static uint64_t *chunk_ns;
static double sw_t[MAXSW];

static void report(const char *tag, double bytes_kick, int sweeps) {
    qsort(sw_t, sweeps, sizeof(double), cmp_double);
    double med = sw_t[sweeps / 2];
    printf("%-12s %.2f ns/kick (median sweep; min %.2f)  %.1f GB/s accounted (%.0f B/kick)\n",
           tag, med / NB, sw_t[0] / NB, bytes_kick * NB / med, bytes_kick);
}

int main(int argc, char **argv) {
    int sweeps = argc > 1 ? atoi(argv[1]) : 16;
    if (sweeps < 2 || sweeps > MAXSW) sweeps = 16;
    rng_s = 0x9E3779B97F4A7C15ULL;
    bi = aligned_alloc(64, sizeof(BodyI) * NB);
    bf = aligned_alloc(64, sizeof(BodyF) * NB);
    ki = aligned_alloc(64, sizeof(KickI) * NB);
    kw = aligned_alloc(64, sizeof(KickW) * NB);
    kf = aligned_alloc(64, sizeof(KickF) * NB);
    order = aligned_alloc(64, sizeof(uint32_t) * NB);
    const uint32_t NC = NB / K;
    cells = aligned_alloc(64, sizeof(Cell) * NC);
    chunk_ns = malloc(sizeof(uint64_t) * ((size_t)sweeps * NB / CHUNK + 2));

    for (uint32_t i = 0; i < NB; i++) {
        int32_t dE = (int32_t)(u64rand() >> 33) - (1 << 30), dL = (int32_t)(u64rand() >> 33) - (1 << 30);
        bi[i] = (BodyI){ (int32_t)i, (int32_t)(i ^ 11), dE >> 20, dL >> 20 };
        bf[i] = (BodyF){ i * 0.5, i * 0.25, dE * 1e-9, dL * 1e-9 };
        ki[i] = (KickI){ i, (int32_t)u64rand(), (int32_t)u64rand() };
        kw[i] = (KickW){ i, ki[i].dE, ki[i].dL, 0 };
        kf[i] = (KickF){ i, ki[i].dE * 1.0, ki[i].dL * 1.0 };
        order[i] = i;
    }
    for (uint32_t i = NB - 1; i > 0; i--) { // Fisher-Yates wake permutation
        uint32_t j = (uint32_t)(u64rand() % (i + 1));
        uint32_t t = order[i]; order[i] = order[j]; order[j] = t;
    }
    printf("# bodies=%u cells=%u K=%d sweeps=%d\n", NB, NC, K, sweeps);

    { // memcpy ceiling (pre-faulted, median of 5)
        size_t sz = 1u << 28;
        char *a = aligned_alloc(64, sz), *b = aligned_alloc(64, sz);
        memset(a, 1, sz); memset(b, 1, sz);
        double ts[5];
        for (int r = 0; r < 5; r++) {
            double t0 = now_ns(); memcpy(b, a, sz); ts[r] = now_ns() - t0;
        }
        qsort(ts, 5, sizeof(double), cmp_double);
        printf("memcpy_ceil   %.1f GB/s (read+write, median)\n", 2.0 * sz / ts[2]);
        free(a); free(b);
    }

    size_t ci;
    // i32 sorted (12 B packed kick record) --------------------------------
    for (int s = 0; s < sweeps; s++) {
        double t0 = now_ns(); ci = 0;
        for (uint32_t c = 0; c < NB; c += CHUNK) {
            double c0 = now_ns();
            for (uint32_t i = c; i < c + CHUNK; i++) {
                const KickI *kk = &ki[i];
                BodyI *b = &bi[kk->id];
                b->vx += kk->dE; b->vy += kk->dL;
            }
            chunk_ns[ci++] = (uint64_t)(now_ns() - c0);
        }
        sw_t[s] = now_ns() - t0;
    }
    report("i32_sorted", 44.0, sweeps);
    tail("i32_sorted", chunk_ns, ci);
    // i32w sorted (16 B kick record) ---------------------------------------
    for (int s = 0; s < sweeps; s++) {
        double t0 = now_ns(); ci = 0;
        for (uint32_t c = 0; c < NB; c += CHUNK) {
            double c0 = now_ns();
            for (uint32_t i = c; i < c + CHUNK; i++) {
                const KickW *kk = &kw[i];
                BodyI *b = &bi[kk->id];
                b->vx += kk->dE; b->vy += kk->dL;
            }
            chunk_ns[ci++] = (uint64_t)(now_ns() - c0);
        }
        sw_t[s] = now_ns() - t0;
    }
    report("i32w_sorted", 48.0, sweeps);
    // f64 sorted -----------------------------------------------------------
    for (int s = 0; s < sweeps; s++) {
        double t0 = now_ns(); ci = 0;
        for (uint32_t c = 0; c < NB; c += CHUNK) {
            double c0 = now_ns();
            for (uint32_t i = c; i < c + CHUNK; i++) {
                const KickF *kk = &kf[i];
                BodyF *b = &bf[kk->id];
                b->vx += kk->dE; b->vy += kk->dL;
            }
            chunk_ns[ci++] = (uint64_t)(now_ns() - c0);
        }
        sw_t[s] = now_ns() - t0;
    }
    report("f64_sorted", 88.0, sweeps);
    tail("f64_sorted", chunk_ns, ci);
    // i32 shuffled (wake) --------------------------------------------------
    for (int s = 0; s < sweeps; s++) {
        double t0 = now_ns(); ci = 0;
        for (uint32_t c = 0; c < NB; c += CHUNK) {
            double c0 = now_ns();
            for (uint32_t i = c; i < c + CHUNK; i++) {
                BodyI *b = &bi[order[i]];
                b->vx += ki[i].dE; b->vy += ki[i].dL;
            }
            chunk_ns[ci++] = (uint64_t)(now_ns() - c0);
        }
        sw_t[s] = now_ns() - t0;
    }
    report("i32_shuffled", 44.0, sweeps);
    tail("i32_shuffled", chunk_ns, ci);
    {
        uint64_t s1 = 0, s2 = 0;
        for (uint32_t i = 0; i < NB; i++) {
            s1 += (uint64_t)(uint32_t)bi[i].vx + (uint64_t)(uint32_t)bi[i].vy;
            s2 += (uint64_t)(bf[i].vx * 1024) + (uint64_t)(bf[i].vy * 1024);
        }
        printf("checksums i32=%llx f64=%llx\n", (unsigned long long)s1, (unsigned long long)s2);
    }

    // cell uniform component: always vs sub-quantum accumulator ------------
    // q = 2^F (one velocity-word quantum). The typical step is q/s (scaled
    // down from heavy_step's minimum 2^F), heavy tail kept: most steps are
    // sub-quantum exactly when the far field is weak relative to the word.
    const int F = 20;
    const uint32_t EPOCHS = 512; // 512 x 32768 scheduled cell-epochs
    for (int s_idx = 0; s_idx < 4; s_idx++) {
        const double s_q[4] = {0.25, 1.0, 4.0, 16.0};
        const double s = s_q[s_idx];
        int64_t *ustream = aligned_alloc(64, sizeof(int64_t) * (size_t)EPOCHS * NC);
        if (!ustream) { fprintf(stderr, "oom\n"); return 1; }
        rng_s = 0xDEADBEEF12345678ULL;
        const int64_t sc = (int64_t)(s * 2.0) < 1 ? 1 : (int64_t)(s * 2.0);
        for (size_t i = 0; i < (size_t)EPOCHS * NC; i++) {
            int64_t u = heavy_step() / sc; // typical step ~= 1.5/sc quanta (mean tail factor 3/2)
            ustream[i] = u ? u : 1;
        }
        // skip path: cell accumulator, body touched only on quantum crossing
        memset(cells, 0, sizeof(Cell) * NC);
        for (uint32_t c = 0; c < NC; c++) cells[c].base = c * K;
        uint64_t touched = 0;
        const uint64_t total_epochs = (uint64_t)EPOCHS * NC;
        double t0 = now_ns();
        for (uint32_t e = 0; e < EPOCHS; e++)
            for (uint32_t c = 0; c < NC; c++) {
                Cell *cc = &cells[c];
                cc->R += ustream[(size_t)e * NC + c];
                int64_t d = cc->R >> F;
                if (d) {
                    cc->R -= d << F;
                    BodyI *b = &bi[cc->base];
                    for (int j = 0; j < K; j++) { b[j].vx += (int32_t)d; b[j].vy += (int32_t)d; }
                    touched += K;
                }
            }
        double dt_skip = now_ns() - t0;
        // always path (control): identical stream, remainder taken per epoch
        memset(cells, 0, sizeof(Cell) * NC);
        for (uint32_t c = 0; c < NC; c++) cells[c].base = c * K;
        uint64_t touched_a = 0;
        t0 = now_ns();
        for (uint32_t e = 0; e < EPOCHS; e++)
            for (uint32_t c = 0; c < NC; c++) {
                Cell *cc = &cells[c];
                int64_t d = ustream[(size_t)e * NC + c] >> F;
                if (d) {
                    BodyI *b = &bi[cc->base];
                    for (int j = 0; j < K; j++) { b[j].vx += (int32_t)d; b[j].vy += (int32_t)d; }
                    touched_a += K;
                }
            }
        double dt_always = now_ns() - t0;
        printf("cell s=%5.2f (typ step ~ %.2f q): always=%6.1f ns/epoch  skip=%6.1f ns/epoch  body-touches deleted=%.1f%%\n",
               s, 1.5 / (double)sc, dt_always / total_epochs, dt_skip / total_epochs,
               100.0 * (1.0 - (double)touched / (double)touched_a));
        free(ustream);
    }

    // exactness check of the accumulator law ------------------------------
    {
        rng_s = 0xC0FFEE111ULL;
        const int F2 = 20, ep = 4096;
        int64_t R = 0; int32_t v = 100;
        int64_t *u = malloc(sizeof(int64_t) * ep);
        for (int i = 0; i < ep; i++) u[i] = heavy_step();
        for (int i = 0; i < ep; i++) {
            R += u[i];
            int64_t d = R >> F2;
            if (d) { v += (int32_t)d; R -= d << F2; }
        }
        int64_t tot = 0;
        for (int i = 0; i < ep; i++) tot += u[i];
        int32_t v_ref = 100 + (int32_t)(tot >> F2);
        printf("exactness applied == floor(total/quantum): %s (v=%d ref=%d R=%lld)\n",
               v == v_ref ? "OK" : "FAIL", v, v_ref, (long long)R);
        free(u);
    }
    free(bi); free(bf); free(ki); free(kw); free(kf); free(order);
    free(cells); free(chunk_ns);
    return 0;
}
