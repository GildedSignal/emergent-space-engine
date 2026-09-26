//! Independent reference for the relativistic bounce (es-lattice-relativistic-v0) on the
//! trapped gas. Shares no code with crates/lattice: every tick over every pair, in checked
//! i128 (it panics rather than overflow), following the written rule:
//! Γ(k) = ⌊F·Q/√(Q² − |k|²)⌋ with F = 2^16; 4-momentum (m·Γ·Q, m·Γ·k); a contact reflects
//! both 4-momenta in the Minkowski hyperplane orthogonal to N = (d·P, E·d); floor/ceil
//! candidates strictly inside the light cone; the candidate pair minimising |owed + e|²,
//! never keeping both velocities; the error joins the lower id's carries; walls flip and
//! record 2·p; a contact is consumed at the post-batch revisions.
//!
//! v1 (es-lattice-relativistic-v1) changes only the 4-momentum, written here from its rule:
//! per unit mass E = ⌊2Q³/√(Q² − |k|²)⌋ and p_c = sgn(k_c)·⌊2Q²|k_c|/√(Q² − |k|²)⌋.
use crate::gas::Gas;
use std::collections::{BTreeMap, BTreeSet};

const F: i128 = 1 << 16;

#[derive(Clone)]
struct Ship {
    x: [i128; 2],
    k: [i128; 2],
    rev: u64,
    carry: [i128; 3],
}

pub struct RelReference {
    pub events: Vec<(i128, String, Vec<u64>)>,
    /// Per ship: position, velocity, energy carry, momentum carry, revision.
    pub finals: Vec<([i128; 2], [i128; 2], i128, [i128; 2], u64)>,
    pub wall_momentum: [i128; 2],
}

fn isqrt(n: i128) -> i128 {
    assert!(n >= 0);
    let mut x = (n as f64).sqrt() as i128;
    while x * x > n {
        x -= 1;
    }
    while (x + 1) * (x + 1) <= n {
        x += 1;
    }
    x
}

fn gamma(q: i128, k: [i128; 2]) -> i128 {
    let s = q * q - k[0] * k[0] - k[1] * k[1];
    assert!(s > 0, "reference: a ship reached c");
    isqrt(F * F * q * q / s)
}

fn p4(q: i128, k: [i128; 2], v1: bool) -> [i128; 3] {
    if v1 {
        // ⌊√(N²/s)⌋ = ⌊N/√s⌋: the floor of a square root of a floor is exact.
        let s = q * q - k[0] * k[0] - k[1] * k[1];
        assert!(s > 0, "reference: a ship reached c");
        let e = isqrt(mul(mul(4, mul(q * q, q * q)), q * q) / s);
        let p = |c: i128| c.signum() * isqrt(mul(mul(4, mul(q * q, q * q)), c * c) / s);
        return [e, p(k[0]), p(k[1])];
    }
    let g = gamma(q, k); // unit masses in the gas
    [g * q, g * k[0], g * k[1]]
}

fn mul(a: i128, b: i128) -> i128 {
    a.checked_mul(b).expect("reference arithmetic exceeds i128")
}

fn fl(n: i128, d: i128) -> i128 {
    let (n, d) = if d < 0 { (-n, -d) } else { (n, d) };
    n.div_euclid(d)
}

fn ce(n: i128, d: i128) -> i128 {
    -fl(-n, d)
}

/// Lattice candidates around Q·p'_s/p'_0, inside the light cone, in floor/ceil order.
fn around(q: i128, v: [i128; 3]) -> Vec<[i128; 2]> {
    let (nx, ny, e) = (mul(q, v[1]), mul(q, v[2]), v[0]);
    let mut out = Vec::new();
    for x in [fl(nx, e), ce(nx, e)] {
        for y in [fl(ny, e), ce(ny, e)] {
            if !out.contains(&[x, y]) && x * x + y * y < q * q {
                out.push([x, y]);
            }
        }
    }
    out
}

pub fn reference(g: &Gas, horizon: i128, v1: bool) -> RelReference {
    let p4 = |q: i128, k: [i128; 2]| p4(q, k, v1);
    let q = g.q;
    let mut ships: Vec<Ship> = g.bodies.iter().map(|(p, v)| Ship { x: [p[0] * q, p[1] * q], k: *v, rev: 0, carry: [0; 3] }).collect();
    let n = ships.len();
    let reach = 2 * g.radius * q;
    let (lo, hi) = (g.radius * q, (g.side - g.radius) * q);
    let mut consumed: BTreeSet<(usize, usize, u64, u64)> = BTreeSet::new();
    let mut events = Vec::new();
    let mut wall_momentum = [0i128; 2];
    for t in 1..=horizon {
        let mut pairs = Vec::new();
        for a in 0..n {
            for b in a + 1..n {
                if consumed.contains(&(a, b, ships[a].rev, ships[b].rev)) {
                    continue;
                }
                let d = [ships[b].x[0] - ships[a].x[0], ships[b].x[1] - ships[a].x[1]];
                let w = [ships[b].k[0] - ships[a].k[0], ships[b].k[1] - ships[a].k[1]];
                let (dd, dw, ww) = (d[0] * d[0] + d[1] * d[1], d[0] * w[0] + d[1] * w[1], w[0] * w[0] + w[1] * w[1]);
                let hit = if dd <= reach * reach {
                    dw < 0
                } else if ww == 0 || dw >= 0 {
                    false
                } else if -dw >= ww {
                    let e = [d[0] + w[0], d[1] + w[1]];
                    e[0] * e[0] + e[1] * e[1] <= reach * reach
                } else {
                    let c = d[0] * w[1] - d[1] * w[0];
                    c * c <= reach * reach * ww
                };
                if hit {
                    pairs.push((a, b));
                }
            }
        }
        for s in ships.iter_mut() {
            s.x = [s.x[0] + s.k[0], s.x[1] + s.k[1]];
        }
        let walls: BTreeSet<usize> = (0..n)
            .filter(|&i| (0..2).any(|c| (ships[i].k[c] < 0 && ships[i].x[c] <= lo) || (ships[i].k[c] > 0 && ships[i].x[c] >= hi)))
            .collect();
        if pairs.is_empty() && walls.is_empty() {
            continue;
        }
        let before: BTreeMap<usize, [i128; 2]> = pairs.iter().flat_map(|&(a, b)| [a, b]).chain(walls.iter().copied()).map(|i| (i, ships[i].k)).collect();
        for &(a, b) in &pairs {
            let d = [ships[b].x[0] - ships[a].x[0], ships[b].x[1] - ships[a].x[1]];
            let w = [ships[b].k[0] - ships[a].k[0], ships[b].k[1] - ships[a].k[1]];
            if d[0] * w[0] + d[1] * w[1] >= 0 || d[0] * d[0] + d[1] * d[1] == 0 {
                continue;
            }
            let (pa, pb) = (p4(q, ships[a].k), p4(q, ships[b].k));
            let tot = [pa[0] + pb[0], pa[1] + pb[1], pa[2] + pb[2]];
            // N = (d·P, E·d); Minkowski dot X·Y = X0Y0 − X1Y1 − X2Y2.
            let nv = [mul(d[0], tot[1]) + mul(d[1], tot[2]), mul(tot[0], d[0]), mul(tot[0], d[1])];
            let mdot = |x: [i128; 3], y: [i128; 3]| mul(x[0], y[0]) - mul(x[1], y[1]) - mul(x[2], y[2]);
            let (nn, pn) = (mdot(nv, nv), mdot(pa, nv));
            if nn == 0 || pn == 0 {
                continue;
            }
            // T·p' = T·p ∓ 2(p_a·N)·N for a and b respectively.
            let pa2 = [0, 1, 2].map(|i| mul(nn, pa[i]) - mul(2 * pn, nv[i]));
            let pb2 = [0, 1, 2].map(|i| mul(nn, pb[i]) + mul(2 * pn, nv[i]));
            let (ca, cb) = (around(q, pa2), around(q, pb2));
            let owed = [0, 1, 2].map(|i| ships[a].carry[i] + ships[b].carry[i]);
            let only = ca.len() * cb.len() == 1;
            let mut best: Option<(i128, [i128; 2], [i128; 2], [i128; 3])> = None;
            for x in &ca {
                for y in &cb {
                    if !only && *x == ships[a].k && *y == ships[b].k {
                        continue;
                    }
                    let (qa, qb) = (p4(q, *x), p4(q, *y));
                    let e = [0, 1, 2].map(|i| qa[i] + qb[i] - tot[i]);
                    let score: i128 = (0..3).map(|i| (owed[i] + e[i]) * (owed[i] + e[i])).sum();
                    if best.as_ref().is_none_or(|(s, ..)| score < *s) {
                        best = Some((score, *x, *y, e));
                    }
                }
            }
            let (_, x, y, e) = best.expect("a candidate pair");
            for i in 0..3 {
                ships[a].carry[i] += e[i];
            }
            ships[a].k = x;
            ships[b].k = y;
        }
        for &i in &walls {
            for c in 0..2 {
                let k = ships[i].k;
                if (ships[i].x[c] <= lo && k[c] < 0) || (ships[i].x[c] >= hi && k[c] > 0) {
                    wall_momentum[c] += 2 * p4(q, k)[1 + c];
                    ships[i].k[c] = -k[c];
                }
            }
        }
        for (&i, old) in &before {
            if ships[i].k != *old {
                ships[i].rev += 1;
            }
        }
        for &(a, b) in &pairs {
            consumed.insert((a, b, ships[a].rev, ships[b].rev));
            events.push((t, "contact".to_string(), vec![a as u64 + 1, b as u64 + 1]));
        }
        for &i in &walls {
            events.push((t, "wall".to_string(), vec![i as u64 + 1]));
        }
    }
    events.sort();
    RelReference {
        events,
        finals: ships.iter().map(|s| (s.x, s.k, s.carry[0], [s.carry[1], s.carry[2]], s.rev)).collect(),
        wall_momentum,
    }
}
