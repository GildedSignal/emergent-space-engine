//! Trapped gas (H0159): an independent integer reference for the lattice's elastic law.
//!
//! The reference shares no code with the engine. It steps every tick over every pair in
//! integers scaled by the response quantum Q (positions ×Q, velocities ×Q, energies ×2Q²)
//! and applies the same written rules: contacts only between approaching bouncers, walls
//! reflect outward motion, simultaneous pairs resolve in id order,
//! resolved one pair at a time from the velocities earlier pairs left (sequential impulses),
//! momentum rounded to the lcm(m_a, m_b)/Q lattice with the energy carry, and a contact is
//! consumed for the pair's post-batch revisions.
use std::collections::{BTreeMap, BTreeSet};

pub struct Gas {
    pub q: i128,
    pub side: i128,
    pub radius: i128,
    /// Positions (units) and velocities (units of 1/Q), mass 1.
    pub bodies: Vec<([i128; 2], [i128; 2])>,
}

/// N bodies on a jittered grid inside a square box at packing fraction `fill`.
pub fn world(n: u64, fill: f64, q: i128, vmax_units: i128, seed: u64) -> Gas {
    let radius = 1;
    let side = ((n as f64 * std::f64::consts::PI / fill).sqrt()).ceil() as i128;
    let per_row = (n as f64).sqrt().ceil() as i128;
    let cell = side / per_row;
    let mut s = seed ^ n ^ 0x6A5;
    let mut next = move || {
        s = s.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = s;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    };
    let mut range = |lo: i128, hi: i128| lo + (next() as u128 % (hi - lo + 1) as u128) as i128;
    let jitter = ((cell - 2 * radius - 1) / 2).clamp(0, 1);
    let bodies = (0..n as i128)
        .map(|i| {
            let p = [
                (i % per_row) * cell + cell / 2 + range(-jitter, jitter),
                (i / per_row) * cell + cell / 2 + range(-jitter, jitter),
            ];
            let v = [range(-vmax_units, vmax_units), range(-vmax_units, vmax_units)];
            (p, v)
        })
        .collect();
    Gas { q, side, radius, bodies }
}

#[derive(Clone)]
struct Particle {
    x: [i128; 2],
    k: [i128; 2],
    m: i128,
    rev: u64,
    residual: i128,
}

pub struct Reference {
    pub events: Vec<(i128, String, Vec<u64>)>,
    /// Per body (id order): position ×Q, velocity ×Q, energy residual ×2Q², revision.
    pub finals: Vec<([i128; 2], [i128; 2], i128, u64)>,
    pub wall_momentum: [i128; 2],
}

fn floor_div(a: i128, b: i128) -> i128 {
    let (d, m) = (a / b, a % b);
    if m != 0 && ((m < 0) != (b < 0)) { d - 1 } else { d }
}
fn ceil_div(a: i128, b: i128) -> i128 {
    -floor_div(-a, b)
}
fn gcd(a: i128, b: i128) -> i128 {
    if b == 0 { a.abs() } else { gcd(b, a % b) }
}

pub fn reference(g: &Gas, horizon: i128) -> Reference {
    let q = g.q;
    let mut ps: Vec<Particle> = g
        .bodies
        .iter()
        .map(|(p, v)| Particle { x: [p[0] * q, p[1] * q], k: *v, m: 1, rev: 0, residual: 0 })
        .collect();
    let n = ps.len();
    let reach = 2 * g.radius * q;
    let (lo, hi) = (g.radius * q, (g.side - g.radius) * q);
    let mut consumed: BTreeSet<(usize, usize, u64, u64)> = BTreeSet::new();
    let mut events = Vec::new();
    let mut wall_momentum = [0i128; 2];
    let (mut dbg_pair, mut dbg_multi, mut dbg_multi_batches, mut dbg_batches, mut dbg_skipped) = (0i128, 0i128, 0u64, 0u64, 0u64);
    for t in 1..=horizon {
        // Detect in bin (t-1, t] with the velocities valid during it.
        let mut pairs = Vec::new();
        for a in 0..n {
            for b in a + 1..n {
                if consumed.contains(&(a, b, ps[a].rev, ps[b].rev)) {
                    continue;
                }
                let d = [ps[b].x[0] - ps[a].x[0], ps[b].x[1] - ps[a].x[1]];
                let w = [ps[b].k[0] - ps[a].k[0], ps[b].k[1] - ps[a].k[1]];
                let dd = d[0] * d[0] + d[1] * d[1];
                let dw = d[0] * w[0] + d[1] * w[1];
                let ww = w[0] * w[0] + w[1] * w[1];
                let hit = if dd <= reach * reach {
                    dw < 0
                } else if ww == 0 || dw >= 0 {
                    false
                } else if -dw >= ww {
                    let e = [d[0] + w[0], d[1] + w[1]];
                    e[0] * e[0] + e[1] * e[1] <= reach * reach
                } else {
                    let cross = d[0] * w[1] - d[1] * w[0];
                    cross * cross <= reach * reach * ww
                };
                if hit {
                    pairs.push((a, b));
                }
            }
        }
        for p in ps.iter_mut() {
            p.x = [p.x[0] + p.k[0], p.x[1] + p.k[1]];
        }
        let mut walls = BTreeSet::new();
        for (i, p) in ps.iter().enumerate() {
            if (0..2).any(|c| (p.k[c] < 0 && p.x[c] <= lo) || (p.k[c] > 0 && p.x[c] >= hi)) {
                walls.insert(i);
            }
        }
        if pairs.is_empty() && walls.is_empty() {
            continue;
        }
        // Respond at t from pre-batch states.
        let mut bodies: BTreeSet<usize> = BTreeSet::new();
        for &(a, b) in &pairs {
            bodies.insert(a);
            bodies.insert(b);
        }
        let mut work: BTreeMap<usize, i128> = bodies.iter().map(|&i| (i, ps[i].residual)).collect();
        let mut delta: BTreeMap<usize, [i128; 2]> = BTreeMap::new();
        let mut pair_errors = 0i128;
        let energy = |m: i128, k: [i128; 2]| m * (k[0] * k[0] + k[1] * k[1]);
        for &(a, b) in &pairs {
            // Sequential impulses: start from the velocities earlier pairs of this batch left.
            let cur = |i: usize, delta: &BTreeMap<usize, [i128; 2]>| {
                let dv = delta.get(&i).copied().unwrap_or([0, 0]);
                [ps[i].k[0] + dv[0], ps[i].k[1] + dv[1]]
            };
            let (ka, kb) = (cur(a, &delta), cur(b, &delta));
            let d = [ps[b].x[0] - ps[a].x[0], ps[b].x[1] - ps[a].x[1]];
            let w = [kb[0] - ka[0], kb[1] - ka[1]];
            let dot = d[0] * w[0] + d[1] * w[1];
            let dd = d[0] * d[0] + d[1] * d[1];
            if dot >= 0 || dd == 0 {
                dbg_skipped += 1;
                continue;
            }
            let (ma, mb) = (ps[a].m, ps[b].m);
            let lcm = ma / gcd(ma, mb) * mb;
            // Momentum to a in lattice steps lcm/Q: d·2·ma·mb·dot / ((ma+mb)·dd·lcm).
            let den = (ma + mb) * dd * lcm;
            let num = [d[0] * 2 * ma * mb * dot, d[1] * 2 * ma * mb * dot];
            let exact_nonzero = num[0] != 0 || num[1] != 0;
            let mut cands: Vec<[i128; 2]> = Vec::new();
            for x in [floor_div(num[0], den), ceil_div(num[0], den)] {
                for y in [floor_div(num[1], den), ceil_div(num[1], den)] {
                    let c = [x, y];
                    if !cands.contains(&c) && !(c == [0, 0] && exact_nonzero) {
                        cands.push(c);
                    }
                }
            }
            let owed = work[&a] + work[&b];
            let mut best: Option<(i128, [i128; 2], [i128; 2], i128)> = None;
            for c in cands {
                let da = [c[0] * (lcm / ma), c[1] * (lcm / ma)];
                let db = [-c[0] * (lcm / mb), -c[1] * (lcm / mb)];
                let e = energy(ma, [ka[0] + da[0], ka[1] + da[1]]) + energy(mb, [kb[0] + db[0], kb[1] + db[1]])
                    - energy(ma, ka)
                    - energy(mb, kb);
                let score = (owed + e).abs();
                if best.as_ref().is_none_or(|(s, ..)| score < *s) {
                    best = Some((score, da, db, e));
                }
            }
            let (_, da, db, e) = best.expect("at least one candidate");
            *work.get_mut(&a).unwrap() += e;
            pair_errors += e;
            let ea = delta.entry(a).or_insert([0, 0]);
            *ea = [ea[0] + da[0], ea[1] + da[1]];
            let eb = delta.entry(b).or_insert([0, 0]);
            *eb = [eb[0] + db[0], eb[1] + db[1]];
        }
        let mut batch_error = 0i128;
        for (&i, dv) in &delta {
            let k = ps[i].k;
            batch_error += energy(ps[i].m, [k[0] + dv[0], k[1] + dv[1]]) - energy(ps[i].m, k);
        }
        if let Some(&first) = bodies.iter().next() {
            *work.get_mut(&first).unwrap() += batch_error - pair_errors;
        }
        if !pairs.is_empty() {
            dbg_batches += 1;
            dbg_pair += pair_errors;
            if batch_error != pair_errors { dbg_multi_batches += 1; }
            dbg_multi += batch_error - pair_errors;
        }
        for (&i, &res) in &work {
            ps[i].residual = res;
        }
        let affected: BTreeSet<usize> = delta.keys().copied().chain(walls.iter().copied()).collect();
        for i in affected {
            let old = ps[i].k;
            let mut k = old;
            if let Some(dv) = delta.get(&i) {
                k = [k[0] + dv[0], k[1] + dv[1]];
            }
            if walls.contains(&i) {
                for c in 0..2 {
                    if (ps[i].x[c] <= lo && k[c] < 0) || (ps[i].x[c] >= hi && k[c] > 0) {
                        wall_momentum[c] += ps[i].m * 2 * k[c];
                        k[c] = -k[c];
                    }
                }
            }
            if k != old {
                ps[i].k = k;
                ps[i].rev += 1;
            }
        }
        for &(a, b) in &pairs {
            consumed.insert((a, b, ps[a].rev, ps[b].rev));
            events.push((t, "contact".to_string(), vec![a as u64 + 1, b as u64 + 1]));
        }
        for &i in &walls {
            events.push((t, "wall".to_string(), vec![i as u64 + 1]));
        }
    }
    events.sort();
    if std::env::var("GAS_DEBUG").is_ok() {
        let e0: i128 = g.bodies.iter().map(|(_, v)| v[0] * v[0] + v[1] * v[1]).sum();
        eprintln!("batches {dbg_batches} multi-contact batches {dbg_multi_batches} skipped pairs {dbg_skipped}; energy x2Q^2: initial {e0} pair-rounding {dbg_pair} multi-contact remainder {dbg_multi}");
    }
    Reference {
        events,
        finals: ps.iter().map(|p| (p.x, p.k, p.residual, p.rev)).collect(),
        wall_momentum,
    }
}
