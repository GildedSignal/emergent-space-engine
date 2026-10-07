/* Micro-benchmarks grounding the 1e9 budget (Linux/x86, orders of magnitude only).
 * Single thread throughout; scale by the M1's ~5 effective performance cores in budget.py.
 *   bench fold   — the designed kick's arithmetic: two fixed-point u64 updates (u128 products)
 *                  + one binary-heap push/pop (event-queue reschedule).            [ns/op]
 *   bench bw     — sequential write then read over 1 GiB.                          [GB/s]
 *   bench rand16 — random 16-byte read-modify-write over 1 GiB (a tube in a 16 GB store). [ns/op]
 * Build: cc -O2 -o bench bench.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + 1e-9 * (double)ts.tv_nsec;
}

/* ---------- fixed-point kick arithmetic: E += (dE>>32)*k etc, u128 products ---------- */
static uint64_t kick_arith(uint64_t E, uint64_t L, uint64_t dE, uint64_t dL, uint64_t k) {
    /* two mantissa updates with 64x64->128 products, one shared exponent (law.md: numbers) */
    __uint128_t p1 = (__uint128_t)dE * k;
    __uint128_t p2 = (__uint128_t)dL * k;
    E += (uint64_t)(p1 >> 32);
    L += (uint64_t)(p2 >> 32);
    return E ^ L; /* fold so the compiler cannot elide */
}

/* ---------- tiny binary heap of root-clock keys (time, body id) ---------- */
#define HEAPN 64
static uint64_t hk[HEAPN]; /* key: time<<20 | bodyid, as law.md ties */
static int hn = 0;
static void hpush(uint64_t k) {
    int i = hn++;
    hk[i] = k;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (hk[p] <= hk[i]) break;
        uint64_t t = hk[p]; hk[p] = hk[i]; hk[i] = t; i = p;
    }
}
static uint64_t hpop(void) {
    uint64_t top = hk[0];
    hk[0] = hk[--hn];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < hn && hk[l] < hk[m]) m = l;
        if (r < hn && hk[r] < hk[m]) m = r;
        if (m == i) break;
        uint64_t t = hk[m]; hk[m] = hk[i]; hk[i] = t; i = m;
    }
    return top;
}

static void bench_fold(void) {
    const long N = 10000000;
    uint64_t E = 0x1111222233334444ull, L = 0x5555666677778888ull, acc = 0;
    double t0 = now_s();
    for (long i = 0; i < N; i++) {
        E += (uint64_t)i;
        L ^= (E << 7);
        acc += kick_arith(E, L, 0x0123456789abcdefull, 0xfedcba9876543210ull, (uint64_t)i | 1);
        hpush(((uint64_t)(0x1000 + i) << 20) | (uint64_t)(i & 0xfffff));
        acc ^= hpop();
    }
    double dt = now_s() - t0;
    printf("fold: %.1f ns/op  (%.3g s for %ld ops, checksum %llx)\n",
           dt * 1e9 / N, dt, N, (unsigned long long)acc);
}

static void bench_bw(void) {
    const size_t BYTES = (size_t)1 << 30; /* 1 GiB */
    unsigned char *buf = malloc(BYTES);
    if (!buf) { printf("bw: alloc failed\n"); return; }
    double t0 = now_s();
    memset(buf, 0x5a, BYTES);
    double tw = now_s() - t0;
    uint64_t s = 0;
    double t1 = now_s();
    for (size_t i = 0; i < BYTES; i += 64) s += buf[i];
    double tr = now_s() - t1;
    printf("bw: write %.1f GB/s, read %.1f GB/s  (checksum %llx)\n",
           BYTES / tw / 1e9, BYTES / tr / 1e9, (unsigned long long)s);
    free(buf);
}

static void bench_rand16(void) {
    const size_t BYTES = (size_t)1 << 30;                 /* 1 GiB of 16-byte tubes */
    const size_t SLOTS = BYTES / 16;                      /* 67,108,864 */
    const long N = 10000000;
    uint64_t *buf = malloc(BYTES);
    if (!buf) { printf("rand16: alloc failed\n"); return; }
    for (size_t i = 0; i < SLOTS * 2; i++) buf[i] = (uint64_t)i * 0x9e3779b97f4a7c15ull;
    uint64_t x = 0x243f6a8885a308d3ull; /* xorshift64* indices */
    uint64_t acc = 0;
    double t0 = now_s();
    for (long i = 0; i < N; i++) {
        x ^= x >> 12; x ^= x << 25; x ^= x >> 27;
        size_t s = (size_t)((x * 0x2545F4914F6CDD1Dull) >> 11) % SLOTS; /* uniform */
        uint64_t *t = buf + 2 * s;                          /* read-modify-write 16 B */
        t[0] += (uint64_t)i;                                /* E increment (integer kick) */
        t[1] ^= t[0] >> 3;                                  /* L increment             */
        acc += t[1];
    }
    double dt = now_s() - t0;
    printf("rand16: %.1f ns/op  (%.3g s for %ld ops, checksum %llx)\n",
           dt * 1e9 / N, dt, N, (unsigned long long)acc);
    free(buf);
}

int main(int argc, char **argv) {
    const char *what = argc > 1 ? argv[1] : "all";
    if (!strcmp(what, "fold") || !strcmp(what, "all")) bench_fold();
    if (!strcmp(what, "bw") || !strcmp(what, "all")) bench_bw();
    if (!strcmp(what, "rand16") || !strcmp(what, "all")) bench_rand16();
    return 0;
}
