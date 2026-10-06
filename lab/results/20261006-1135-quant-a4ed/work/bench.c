/* Event-capacity probe: how many events/s can one core (and the box) sustain
 * when each event touches L cold cache lines, under three access regimes:
 *   stream : L sequential lines/event (hardware prefetch, best case)
 *   gather : L independent random lines/event, interleaved chains (MLP-bound; the
 *            realistic case once the event list is known before the loads issue)
 *   chase  : L random lines/event, one dependent chain (latency-bound worst case)
 * One "event" = L line touches + one integer accumulate on the payload (the
 * trivial compute floor; the real kick's math sits on top of this).
 * Usage: bench <regime> <L> <threads> [bytes_mib] ; ~0.5-1.5 s per measurement.
 */
#define _GNU_SOURCE
#include <stdint.h>
#include <stdio.h>

#include <stdlib.h>
#include <string.h>

#include <time.h>
#include <pthread.h>
#include <sched.h>

static uint64_t rng(uint64_t *s) { *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17; return *s; }

typedef struct { int cpu; const char *regime; int L; uint8_t *buf; size_t nlines; uint64_t seed; uint64_t events; uint64_t sum; double secs; } Arg;

static void pin(int cpu) { cpu_set_t set; CPU_ZERO(&set); CPU_SET(cpu, &set); sched_setaffinity(0, sizeof(set), &set); }

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static void *worker(void *v) {
    Arg *a = (Arg *)v;
    pin(a->cpu);
    const size_t mask = a->nlines - 1; /* nlines is a power of two */
    uint64_t sum = 0, s = a->seed | 1;
    uint32_t iters = strcmp(a->regime, "stream") == 0 ? 20000000u : 8000000u / (uint32_t)a->L;
    double t0 = now();
    if (!strcmp(a->regime, "stream")) {
        uint64_t *p = (uint64_t *)a->buf; size_t mask64 = a->nlines * 8 - 1; size_t idx = (rng(&s) & mask64) & ~7u;
        for (uint32_t i = 0; i < iters; i++) {
            for (int l = 0; l < a->L; l++) { sum += p[idx]; idx = (idx + 8) & mask64; }
            asm volatile("" :: "r"(sum) : "memory");
        }
        a->events = iters;
    } else if (!strcmp(a->regime, "gather")) {
        /* L interleaved independent chains: each event = one hop on each chain,
         * so the L cold lines of one event issue without inter-dependency. */
        enum { S = 16 };
        uint64_t **ch[S]; uint64_t *base = (uint64_t *)a->buf;
        for (int k = 0; k < S; k++) ch[k] = (uint64_t **)(base + ((rng(&s) & mask) & ~7u) * 8);
        for (uint32_t i = 0; i < iters; i++) {
            for (int l = 0; l < a->L && l < S; l++) { sum += *(uint64_t *)ch[l]; ch[l] = (uint64_t **)*ch[l]; }
            asm volatile("" :: "r"(sum) : "memory");
        }
        a->events = iters;
    } else { /* chase: one dependent chain; an "event" = L serial hops */
        uint64_t **p = (uint64_t **)(a->buf + (size_t)((rng(&s) & mask) & ~7u) * 64);
        for (uint32_t i = 0; i < iters; i++) {
            for (int l = 0; l < a->L; l++) p = (uint64_t **)*p;
            sum += *(uint64_t *)p;
            asm volatile("" :: "r"(sum) : "memory");
        }
        a->events = iters;
    }
    a->secs = now() - t0;
    a->sum = sum;
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s stream|gather|chase L threads [mib]\n", argv[0]); return 2; }
    const char *regime = argv[1];
    int L = atoi(argv[2]), nth = atoi(argv[3]);
    size_t mib = argc > 4 ? (size_t)atol(argv[4]) : 512;
    size_t nlines = (mib << 20) / 64;
    while (nlines & (nlines - 1)) nlines &= (nlines - 1); /* round down to power of two */
    if (nlines < 4096) nlines = 4096;
    uint8_t *buf = aligned_alloc(64, nlines * 64);
    if (!buf) { perror("alloc"); return 1; }
    /* one random permutation of line indices, so chains cover the space */
    uint32_t *perm = malloc(nlines * sizeof(uint32_t));
    for (size_t i = 0; i < nlines; i++) perm[i] = (uint32_t)i;
    uint64_t s = 0x9e3779b97f4a7c15ull;
    for (size_t i = nlines - 1; i > 0; i--) { size_t j = rng(&s) % (i + 1); uint32_t t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
    for (size_t i = 0; i < nlines; i++) {
        uint64_t *line = (uint64_t *)(buf + i * 64);
        line[0] = (uint64_t)(buf + (size_t)perm[i] * 64); /* next hop as full line address */
        line[1] = perm[i] * 2654435761u + i;
    }
    free(perm);
    { volatile char sink = 0; for (size_t i = 0; i < nlines * 64; i += 4096) sink += buf[i]; (void)sink; } /* warm faults */

    int cpus[8] = {0, 1, 2, 3, 4, 5, 6, 7};
    pthread_t th[8]; Arg args[8];
    uint64_t tot_events = 0, tot_sum = 0; double max_secs = 0;
    for (int i = 0; i < nth; i++) {
        args[i] = (Arg){.cpu = cpus[i], .regime = regime, .L = L, .buf = buf, .nlines = nlines, .seed = 0x1234 + 7919u * i};
        pthread_create(&th[i], NULL, worker, &args[i]);
    }
    for (int i = 0; i < nth; i++) {
        pthread_join(th[i], NULL);
        tot_events += args[i].events; tot_sum += args[i].sum;
        if (args[i].secs > max_secs) max_secs = args[i].secs;
    }
    double eps = tot_events / max_secs;
    printf("{\"regime\":\"%s\",\"L\":%d,\"threads\":%d,\"mib\":%zu,\"events_per_s\":%.0f,\"ns_per_event\":%.2f,\"sum\":%llu}\n",
           regime, L, nth, mib, eps, 1e9 / eps, (unsigned long long)tot_sum);
    free(buf);
    return 0;
}
