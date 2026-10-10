#!/usr/bin/env python3
"""Probe: does the slack (Verlet-style) skin survive co-orbital concentration?

Event-driven, exact for the regime simulated: between rebuilds a body's skin set
is frozen; relative motion is deterministic shear |n_j - n_i|*dt plus a jitter
walk verified 100x below slack at the intervals involved (sigma_j=3e-7 rad/kick,
intervals >= 500 kicks -> walk sigma ~1.3e-5 vs slack >= 1.6e-3), so the next
rebuild of body i is at t + slack / max_{j in S_i} |n_j - n_i|. Sets are rebuilt
from exact phases at each rebuild event.

Skins: metric (|phase diff| < W = m*belt_spacing) and phase (k nearest along the
orbit, k=4 from taleb-09b5). Formation = phase dispersion 20x tighter than belt
spacing (a fleet). Horizon 100k kicks, N=1000.

Reports: setups/kick/body (amortization) and pair-evals/kick/body (per-kick
candidate cost), and total cost = setups*set_size (rebuild work) + pair-evals.
"""
import numpy as np, json, heapq

N = 1000
HORIZON = 100_000
TWO_PI = 2.0 * np.pi
SP = TWO_PI / N
SIGMA_U = 1e-4
K = 4

def run(skin, m, formation, seed=11):
    r = np.random.default_rng(seed)
    ph0 = r.normal(0, SP / 20, N) if formation else r.uniform(0, TWO_PI, N)
    n = (TWO_PI / 32.0) * (1.0 + r.normal(0, SIGMA_U, N)) / 32.0  # rad/kick
    slack = (m - 1.0) / 2.0 * SP
    W = m * SP

    def build(i, ph):
        d = (ph - ph[i] + np.pi) % TWO_PI - np.pi
        if skin == 'metric':
            idx = np.where(np.abs(d) < W)[0]
        else:
            idx = np.argpartition(np.abs(d), K)[:K]
        idx = idx[idx != i]
        return idx

    ph = ph0.copy()
    # heap of (next_rebuild_time, body)
    events = []
    setups = 0
    pair_evals = 0.0  # accumulated |S_i| * (time until next change of i)
    sizes = np.zeros(N, dtype=int)
    last = np.zeros(N)
    for i in range(N):
        S = build(i, ph); sizes[i] = len(S)
        kmax = np.abs(n[S] - n[i]).max() if len(S) else np.inf
        heapq.heappush(events, (slack / kmax if np.isfinite(kmax) else HORIZON + 1, i))
    t_check = 0.0
    prev_sizes = sizes.copy()
    next_report = 0.0
    # pair-evals accrue continuously; rebuild events change one row
    while events:
        t, i = heapq.heappop(events)
        if t >= HORIZON: break
        step = t - 0.0  # placeholder
        setups += 1
        ph_i = (ph0[i] + n[i] * t) % TWO_PI
        # phases of everyone at time t (exact linear drift)
        ph_t = (ph0 + n * t) % TWO_PI
        # body i sits at ph_i; others at ph_t (consistent)
        S = build(i, ph_t)
        sizes[i] = len(S)
        kmax = np.abs(n[S] - n[i]).max() if len(S) else np.inf
        heapq.heappush(events, (t + (slack / kmax if np.isfinite(kmax) else HORIZON + 1), i))
    # pair-evals: integrate sizes over time exactly via event times
    # redo cheaply: we know setups and can average set sizes at steady state
    # (recompute: time-weighted mean of sizes using event log we didn't keep) --
    # instead run a second pass storing sizes at each event with timestamps
    return setups / HORIZON, sizes.mean()

def run_full(skin, m, formation, seed=11):
    """Same but logs (time, i, new_size) to integrate pair-evals exactly."""
    r = np.random.default_rng(seed)
    ph0 = r.normal(0, SP / 20, N) if formation else r.uniform(0, TWO_PI, N)
    n = (TWO_PI / 32.0) * (1.0 + r.normal(0, SIGMA_U, N)) / 32.0
    slack = (m - 1.0) / 2.0 * SP
    W = m * SP
    def build(i, ph):
        d = (ph - ph[i] + np.pi) % TWO_PI - np.pi
        if skin == 'metric':
            idx = np.where(np.abs(d) < W)[0]
        else:
            idx = np.argpartition(np.abs(d), K)[:K]
        return idx[idx != i]
    ph = ph0.copy()
    events = []
    sizes = np.zeros(N, dtype=int)
    for i in range(N):
        S = build(i, ph); sizes[i] = len(S)
        kmax = np.abs(n[S] - n[i]).max() if len(S) else np.inf
        heapq.heappush(events, (slack / kmax if np.isfinite(kmax) else 1e18, i))
    log = []  # (t, i, old_size, new_size)
    while events:
        t, i = heapq.heappop(events)
        if t >= HORIZON: break
        ph_t = (ph0 + n * t) % TWO_PI
        S = build(i, ph_t)
        log.append((t, i, sizes[i], len(S)))
        sizes[i] = len(S)
        kmax = np.abs(n[S] - n[i]).max() if len(S) else np.inf
        heapq.heappush(events, (t + (slack / kmax if np.isfinite(kmax) else 1e18), i))
    # integrate pair-evals: sizes change only at events
    tot_pairs = 0.0
    t_prev = 0.0
    cur = np.zeros(N, dtype=int)
    for i in range(N):
        S = build(i, ph0); cur[i] = len(S)
    setups = len(log)
    # replay
    cur = np.zeros(N, dtype=int)
    for i in range(N):
        S = build(i, ph0); cur[i] = len(S)
    for (t, i, osz, nsz) in log:
        tot_pairs += cur.sum() * (t - t_prev)
        t_prev = t
        cur[i] = nsz
    tot_pairs += cur.sum() * (HORIZON - t_prev)
    setups_per_kick = setups / HORIZON / N
    pair_per_kick = tot_pairs / HORIZON / N
    return setups_per_kick, pair_per_kick

print(f"{'config':30s} {'setups/kick/body':>17s} {'pair-evals/kick/body':>21s} {'rebuild-work/kick':>19s}")
out = []
for m in (1.5, 2.0, 3.0, 5.0, 8.0):
    for formation in (False, True):
        s, p = run_full('metric', m, formation)
        w = s * p  # each setup rebuilds ~|S| pairs
        tag = f"metric m={m:<4} {'formation' if formation else 'belt':>9s}"
        print(f"{tag:30s} {s:17.5f} {p:21.1f} {w:19.3f}")
        out.append((tag, s, p, w))
for formation in (False, True):
    s, p = run_full('phase', 2.0, formation)
    w = s * p
    tag = f"phase  k=4    {'formation' if formation else 'belt':>9s}"
    print(f"{tag:30s} {s:17.5f} {p:21.1f} {w:19.3f}")
    out.append((tag, s, p, w))
json.dump(out, open('probe_skin_out.json', 'w'), indent=1)
