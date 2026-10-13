# detune_repro.py — independent reproduction of e9f9's detuned false-alarm kill.
# Reimplements the mechanism from scratch (no code taken from e9f9 or its checker):
# two-sided CUSUM on the per-orbit mean of a bounded, detuned (precessing) error
#   e_t = A*sin(2*pi*t/(P*(1+eps))) + iid noise (sigma)
# with e9f9's frozen k=0.01, h=0.03391, P=1234 ticks/orbit, 512 orbits, 200 seeds.
# Predictions (predictions.md P6): eps=1e-3 at A=20 -> ~200/200 false alarms,
# median alarm orbit ~9; eps=1e-4 -> none; eps=0 -> none at any amplitude.
import numpy as np

P, ORBITS, SEEDS = 1234, 512, 200
K, H = 0.01, 0.03391
SIGMA = 0.1  # chosen so the per-orbit noise mean (~sigma/sqrt(P)=0.0028) sits under k,
             # as e9f9's calibration implies; the detune result is insensitive to it.

def cusum_alarm_orbit(m):
    """m: per-orbit means, shape (ORBITS,). Returns 1-based alarm orbit or None."""
    cpos = cneg = 0.0
    for o, x in enumerate(m, start=1):
        cpos = max(0.0, cpos + x - K)
        cneg = max(0.0, cneg - x - K)
        if cpos > H or cneg > H:
            return o
    return None

def arm(A, eps, seeds=SEEDS, sigma=SIGMA):
    rng = np.random.default_rng(20261012)
    t = np.arange(ORBITS * P, dtype=np.float64)
    signal = A * np.sin(2 * np.pi * t / (P * (1.0 + eps))) if A > 0 else 0.0
    alarms = []
    for s in range(seeds):
        e = signal + sigma * rng.standard_normal(t.size)
        m = e.reshape(ORBITS, P).mean(axis=1)
        a = cusum_alarm_orbit(m)
        if a is not None:
            alarms.append(a)
    n = len(alarms)
    med = float(np.median(alarms)) if alarms else float("nan")
    return n, seeds, med

if __name__ == "__main__":
    print(f"detune_repro: P={P} orbits={ORBITS} seeds={SEEDS} k={K} h={H} sigma={SIGMA}")
    for A, eps in [(20.0, 0.0), (20.0, 1e-4), (20.0, 1e-3), (5.0, 1e-2), (1.0, 0.0)]:
        n, s, med = arm(A, eps)
        print(f"A={A:5.1f} eps={eps:.0e}  A*eps={A*eps:.4f}  false-alarms {n}/{s}  median alarm orbit {med}")
