/* The kick's floor, measured. Not the plane's law: the information-mandatory part of one kick,
 * done in the design's own form (representation.md thesis 3: a kick is an addition).
 *
 * A kick on a body held as packed state does exactly:
 *   read the body's record (16 B), evaluate the perturbing field at it (per source:
 *   r^2, a table reciprocal + 2 Newton steps, a direction multiply), add the integer
 *   delta with a sigma-delta carry, write the record back (16 B).
 *
 * Variants:
 *   -b B  bodies (records are 16 B: E, L, phase, carry, packed u32s)
 *   -o    order: 0 = body-ordered (streaming), 1 = causal-queue order (random body per event)
 *   -f    include the 3-source field evaluation per kick (u32 fixed point)
 *   -d    also report pure memory traffic (no field, no add beyond the delta)
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + ts.tv_nsec;
}

/* reciprocal table for the field: 2^16 entry table of 1/x^(3/2)-shaped u32 reciprocals,
 * corrected by two Newton steps in u64 — the cheap-arithmetic stand-in for gm/r^3. */
static uint32_t recip_tab[1 << 16];
static void recip_init(void) {
    for (uint32_t i = 0; i < (1u << 16); i++) {
        double x = 1.0 + (double)i / (double)(1u << 16); /* r^2 in [1,4) */
        recip_tab[i] = (uint32_t)(1.0 / (x * x * __builtin_sqrt(x)) * 2147483648.0);
    }
}
static inline uint32_t inv_sqrt_cub(uint32_t r2_hi, uint32_t r2_lo) {
    /* index the table by the top 16 bits of r2, correct twice (Newton on y ~= r^-3). */
    uint32_t y = recip_tab[r2_hi >> 16];
    uint64_t r = ((uint64_t)r2_hi << 32) | r2_lo; /* r2 in 64.0 */
    for (int i = 0; i < 2; i++) {
        /* y' = y*(5 - r*y^2*y)/2 in 2^32 scale, saturating to low bits (order of magnitude is enough) */
        __uint128_t y2 = (__uint128_t)y * y >> 32;
        __uint128_t ry2 = (__uint128_t)r * (uint64_t)y2 >> 32;
        __uint128_t t = (5ull << 32) - (uint64_t)ry2;
        y = (uint32_t)((__uint128_t)y * (uint64_t)t >> 33);
    }
    return y;
}

typedef struct { uint32_t e, l, ph, carry; } rec_t; /* 16 B */

int main(int argc, char **argv) {
    uint64_t bodies = 1 << 20;
    int order = 0, field = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-b")) bodies = strtoull(argv[++i], 0, 10);
        else if (!strcmp(argv[i], "-o")) order = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-f")) field = 1;
    }
    recip_init();
    rec_t *recs = aligned_alloc(64, bodies * sizeof(rec_t));
    uint32_t *queue = malloc(bodies * sizeof(uint32_t)); /* causal order: random body ids */
    uint64_t rng = 0x9e3779b97f4a7c15ull;
    for (uint64_t i = 0; i < bodies; i++) {
        recs[i] = (rec_t){ (uint32_t)i, (uint32_t)(i * 2654435761u), (uint32_t)(i ^ (i >> 13)), (uint32_t)i };
        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
        queue[i] = (uint32_t)(rng % bodies);
    }
    /* three perturbing sources, u32 positions (the plane's doll: a planet, a moon, the parent tide) */
    uint32_t sx[3] = {0x12345678u, 0x7ea3b1f0u, 0x0badc0deu}, sy[3] = {0x5a5a5a5au, 0x13579bdfu, 0x2468ace0u};
    uint64_t acc = 0; /* sink so nothing is optimised away */
    uint64_t t0 = now_ns();
    for (uint64_t k = 0; k < bodies; k++) {
        uint64_t idx = order ? queue[k] : k;
        rec_t *r = &recs[idx];
        uint32_t dvx = (uint32_t)k >> 8, dvy = (uint32_t)(k * 3) >> 8;
        if (field) {
            for (int s = 0; s < 3; s++) {
                uint64_t dx = (uint64_t)(sx[s] - r->ph) * (sx[s] - r->ph);
                uint64_t dy = (uint64_t)(sy[s] - r->e) * (sy[s] - r->e);
                uint32_t inv = inv_sqrt_cub((uint32_t)(dx >> 32), (uint32_t)dx) ^ inv_sqrt_cub((uint32_t)(dy >> 32), (uint32_t)dy);
                dvx += (uint32_t)(((uint64_t)inv * (sx[s] - r->ph)) >> 32) >> 8;
                dvy += (uint32_t)(((uint64_t)inv * (sy[s] - r->e)) >> 32) >> 8;
            }
        }
        uint64_t c = (uint64_t)r->carry + dvy; /* the sigma-delta carry, as the law's own */
        r->l += dvx;
        r->ph = (uint32_t)c;
        r->carry = (uint32_t)(c >> 16);
        r->e += dvx ^ dvy;
        acc += r->e;
    }
    uint64_t t1 = now_ns();
    printf("{\"bodies\":%llu,\"bytes\":%llu,\"order\":%s,\"field\":%s,\"ns_per_kick\":%.2f,\"sink\":%llu}\n",
           (unsigned long long)bodies, (unsigned long long)(bodies * sizeof(rec_t)),
           order ? "causal-random" : "body-stream", field ? "3-source" : "none",
           (double)(t1 - t0) / (double)bodies, (unsigned long long)(acc & 1));
    return 0;
}
