//! Second author on run 20261011-2028-system-3b42 (checker's named experiments for gold).
//!
//! Base modes `belt` / `coorbital`: byte-identical re-run of the original tube_lattice record
//! (sanity that the base still reproduces in this tree).
//!
//! Mode `straggler` — the frozen same-key rank rule (checker's experiment 1).
//!   Rule (frozen, per key cell, from the memo entry's constants only — no per-body state):
//!     kappa_cell = (1.5*(4*e_hi + 3*e_hi^2) + dn_cell * t_end) / TAU
//!     K_cell     = 1 + ceil(kappa_cell * m)        [capped at m-1]
//!   where e_hi is the cell's upper eccentricity edge, dn_cell = |n(a_lo) - n(a_hi)| over the
//!   cell's a-range (the closure number: the phase fraction shear can close over the horizon),
//!   m = members. Certificate: rank-K neighbours in the mean-longitude-at-epoch (lambda(0))
//!   order, maintained once per epoch = the horizon. Derivation: two same-key bodies can be at
//!   the same true longitude only if |lambda_j(0) - lambda_i(0)| <= 2(e_i+e_j)(1+O(e)) + |dn|*t,
//!   so every real same-key encounter lies within arc kappa*TAU, i.e. rank < K.
//!   Measured on the crate's own `narrow-adversarial` band (uniform varpi, dense, eccentric) at
//!   two quanta (engine: 1 a-cell; closure-matched: 16 a-cells), n in {400,800,1600,3200}, and on
//!   `equal-period-keys` (birth-fixed branch: dn = 0 exactly, the lambda(0) order is permanent).
//!   Instruments: worst required rank fraction kappa_req (must be constant in n), zero misses at
//!   K (soundness), same-key candidates per real encounter (must be constant in n), and a
//!   negative control (K without the closure term must miss).
//!
//! Mode `strongfield` — the (E,L) key order where U(L) may turn (checker's experiment 2).
//!   Exact Schwarzschild turning points (mu = G = c = 1): E^2 = (1-2/r)(1+L^2/r^2); the radial
//!   cubic 2L^2 u^3 - L^2 u^2 + 2u + (E^2-1) = 0 gives r_p = 1/u_3, r_a = 1/u_2 for bound orbits;
//!   p = 2 r_p r_a/(r_p+r_a), e = (r_a-r_p)/(r_a+r_p), U = 1/p. Key = quantized (E, L) (law.md
//!   §tubes: the tube key IS quantized E and L). Per-key constants compiled on a 5x5 sub-grid
//!   clipped to the bound domain (the memo entry "knows its own turning points"). Measured:
//!   (a) does U(L)|E turn in the strong-field bound domain (200 E-columns x 512 L steps)?
//!   (b) radial zero-miss of the conservative key lattice vs the exact per-body tier;
//!   (c) the U-band scan: naive per-column contiguity (Newtonian assumption) vs the memo-table
//!       sweep; Newtonian belt as the positive control.

use emergent_encounters::belt::{make_belt, Rng, Spec};
use emergent_encounters::kepler::Body;
use emergent_encounters::pairs::{cone_pairs, radial_pairs};
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::f64::consts::TAU;
use std::time::Instant;

// ---------------------------------------------------------------------------
// base modes (the original record, verbatim logic)
// ---------------------------------------------------------------------------

struct KeyCell0 {
    rmin: f64,
    rmax: f64,
    members: Vec<u32>,
}

fn lattice0(b: &[Body], a_lo: f64, a_hi: f64, e_span: f64, nca: usize, nce: usize) -> (Vec<u32>, Vec<KeyCell0>) {
    let da = (a_hi - a_lo) / nca as f64;
    let de = e_span / nce as f64;
    let mut keys: Vec<u32> = Vec::with_capacity(b.len());
    let mut cells: Vec<Option<KeyCell0>> = (0..nca * nce).map(|_| None).collect();
    for (i, x) in b.iter().enumerate() {
        let ia = (((x.a - a_lo) / da).floor() as usize).min(nca - 1);
        let ie = ((x.e / de).floor() as usize).min(nce - 1);
        let k = ia * nce + ie;
        keys.push(k as u32);
        let a_c_lo = a_lo + ia as f64 * da;
        let e_c_hi = ((ie + 1) as f64 * de).min(0.99);
        let cell = cells[k].get_or_insert_with(|| KeyCell0 {
            rmin: a_c_lo * (1.0 - e_c_hi),
            rmax: (a_c_lo + da) * (1.0 + e_c_hi),
            members: Vec::new(),
        });
        cell.members.push(i as u32);
    }
    let cells: Vec<KeyCell0> = cells.into_iter().flatten().collect();
    (keys, cells)
}

fn lattice_pairs0(b: &[Body], cells: &[KeyCell0], rho: f64, same_key_rank: usize) -> (Vec<(u32, u32)>, u64, u64) {
    let mut order: Vec<u32> = (0..cells.len() as u32).collect();
    order.sort_by(|&x, &y| cells[x as usize].rmin.total_cmp(&cells[y as usize].rmin));
    let mut pairs = Vec::new();
    let (mut scanned, mut same_key) = (0u64, 0u64);
    for xi in 0..order.len() {
        let cx = &cells[order[xi] as usize];
        if same_key_rank == 0 {
            same_key += (cx.members.len() as u64) * (cx.members.len() as u64 - 1) / 2;
            for ai in 0..cx.members.len() {
                for aj in ai + 1..cx.members.len() {
                    pairs.push((cx.members[ai], cx.members[aj]));
                }
            }
        } else {
            let mut ph: Vec<(f64, u32)> = cx
                .members
                .iter()
                .map(|&i| (b[i as usize].mean_anomaly(0.0) + b[i as usize].pom, i))
                .collect();
            ph.sort_by(|x, y| x.0.total_cmp(&y.0));
            for k in 0..ph.len() {
                for d in 1..=same_key_rank {
                    if k + d < ph.len() {
                        pairs.push((ph[k].1, ph[k + d].1));
                        same_key += 1;
                    }
                }
            }
        }
        for yi in xi + 1..order.len() {
            let cy = &cells[order[yi] as usize];
            if cy.rmin > cx.rmax + 2.0 * rho {
                break;
            }
            if cx.rmin <= cy.rmax + 2.0 * rho {
                for &i in &cx.members {
                    for &j in &cy.members {
                        pairs.push((i, j));
                        scanned += 1;
                    }
                }
            }
        }
    }
    (pairs, scanned, same_key)
}

fn spec(name: &str, n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, keys: usize, orbits: f64, seed: u64) -> Spec {
    Spec { name: name.into(), n, sigma_e, rho, a_lo, a_hi, keys, seed, orbits }
}

// ---------------------------------------------------------------------------
// straggler mode
// ---------------------------------------------------------------------------

struct SCeil {
    members: Vec<u32>,
    /// lambda(0) order: members sorted by mean longitude at the epoch (the tube's phase axis).
    order: Vec<(f64, u32)>,
    m: usize,
    /// Certificate window half-width (radians of mean longitude at the epoch).
    w: f64,
    /// Negative control: window without the closure term.
    w_nocl: f64,
}

fn straggler_run(sp: &Spec, nca: usize, nce: usize) {
    let b = make_belt(sp);
    let t_end = sp.orbits * TAU;
    let da = (sp.a_hi - sp.a_lo) / nca as f64;
    let de = 0.5 / nce as f64;
    let mut map: std::collections::HashMap<(usize, usize), Vec<u32>> = std::collections::HashMap::new();
    for (i, x) in b.iter().enumerate() {
        let ia = (((x.a - sp.a_lo) / da).floor() as usize).min(nca - 1);
        let ie = ((x.e / de).floor() as usize).min(nce - 1);
        map.entry((ia, ie)).or_default().push(i as u32);
    }
    let mut keysorted: Vec<(&(usize, usize), &Vec<u32>)> = map.iter().collect();
    keysorted.sort_by(|a, b| a.0.cmp(b.0));
    let mut cells: Vec<SCeil> = Vec::new();
    let mut birth_fixed_cells = 0usize;
    for ((ia, ie), mut members) in keysorted.into_iter().map(|(k, v)| (*k, v.clone())) {
        members.sort_unstable();
        let a_lo_c = sp.a_lo + ia as f64 * da;
        let a_hi_c = a_lo_c + da;
        let e_hi = ((ie + 1) as f64 * de).min(0.99);
        // Closure number: worst |n_i - n_j| inside the cell (n = a^-1.5 rad per time unit).
        // Birth-fixed keys (one integer period shared by every member) have dn = 0 exactly.
        let same_period = {
            let p0 = b[members[0] as usize].period;
            members.iter().all(|&i| b[i as usize].period == p0)
        };
        let dn = if same_period && sp.keys > 1 {
            birth_fixed_cells += 1;
            0.0
        } else {
            (a_lo_c.powf(-1.5) - a_hi_c.powf(-1.5)).abs()
        };
        // Frozen rule (cell constants only): |lambda_j(0) - lambda_i(0)|_arc <=
        // 1.5*(4 e_hi + 3 e_hi^2)  [equation-of-centre distortion at a shared true longitude]
        // + dn * t_end             [closable shear over the epoch = the horizon].
        let w = (1.5 * (4.0 * e_hi + 3.0 * e_hi * e_hi) + dn * t_end).min(std::f64::consts::PI);
        let w_nocl = (1.5 * (4.0 * e_hi + 3.0 * e_hi * e_hi)).min(std::f64::consts::PI);
        let m = members.len();
        let order: Vec<(f64, u32)> = {
            let mut o: Vec<(f64, u32)> = members
                .iter()
                .map(|&i| ((b[i as usize].mean_anomaly(0.0) + b[i as usize].pom).rem_euclid(TAU), i))
                .collect();
            o.sort_by(|x, y| x.0.total_cmp(&y.0));
            o
        };
        cells.push(SCeil { members, order, m, w, w_nocl });
    }
    // Certificate candidates: same-key pairs within the arc window (sorted phase, two pointers).
    let cand: u64 = cells
        .iter()
        .map(|c| {
            let m = c.m;
            if m < 2 || c.w >= std::f64::consts::PI {
                return (m * (m - 1) / 2) as u64;
            }
            let mut cnt = 0u64;
            for p in 0..m {
                for q in p + 1..m {
                    let gap = c.order[q].0 - c.order[p].0; // q > p, lambda sorted
                    if gap.min(TAU - gap) <= c.w {
                        cnt += 1;
                    }
                }
            }
            cnt
        })
        .sum();
    // Truth on every same-key pair; instruments on the arc window and the rank shadow.
    let t0 = Instant::now();
    let mut tst = TruthStats::default();
    let mut tmp = Vec::new();
    let (mut events, mut worst_rank, mut worst_m, mut misses, mut misses_nocl, mut rank4) =
        (0u64, 0usize, 1usize, 0u64, 0u64, 0u64);
    let mut arc_over_w_max = 0.0f64;
    let mut positions: std::collections::HashMap<u32, usize> = std::collections::HashMap::new();
    for c in cells.iter() {
        let m = c.m;
        if m < 2 {
            continue;
        }
        positions.clear();
        for (p, &(_, i)) in c.order.iter().enumerate() {
            positions.insert(i, p);
        }
        for ai in 0..m {
            for aj in ai + 1..m {
                let (i, j) = (c.members[ai], c.members[aj]);
                let (li, lj) = (b[i as usize].mean_anomaly(0.0) + b[i as usize].pom, b[j as usize].mean_anomaly(0.0) + b[j as usize].pom);
                let d = (lj - li).rem_euclid(TAU);
                let arc = d.min(TAU - d);
                tmp.clear();
                truth_pair(&b[i as usize], &b[j as usize], sp.rho, t_end, &mut tmp, &mut tst);
                for &(_t, _dm) in &tmp {
                    events += 1;
                    let (pi, pj) = (positions[&i], positions[&j]);
                    let cw = (pj + m - pi - 1) % m; // strictly between, clockwise
                    let rank = cw.min(m - 2 - cw);
                    if rank + 1 > worst_rank {
                        worst_rank = rank + 1;
                        worst_m = m;
                    }
                    if arc > c.w {
                        misses += 1;
                        arc_over_w_max = arc_over_w_max.max(arc / c.w);
                    } else {
                        arc_over_w_max = arc_over_w_max.max(arc / c.w);
                    }
                    if arc > c.w_nocl {
                        misses_nocl += 1;
                    }
                    if rank <= 3 {
                        rank4 += 1;
                    }
                }
            }
        }
    }
    let truth_s = t0.elapsed().as_secs_f64();
    let all_pairs: u64 = cells.iter().map(|c| (c.m * (c.m - 1) / 2) as u64).sum();
    let w_max = cells.iter().map(|c| c.w).fold(0.0_f64, f64::max);
    let kappa_req = worst_rank as f64 / worst_m as f64;
    println!(
        "{{\"exp\":\"straggler\",\"spec\":\"{}\",\"n\":{},\"nca\":{},\"de\":{:.4},\"cells\":{},\"birth_fixed\":{},\"members_max\":{},\
\"same_key_pairs\":{},\"events\":{},\"worst_rank\":{},\"worst_m\":{},\"kappa_req\":{:.4},\"w_max\":{:.3},\
\"misses\":{},\"misses_nocl\":{},\"arc_over_w_max\":{:.3},\"rank4_cov\":{:.3},\"cand_scaled\":{},\"all_pairs\":{},\
\"cand_per_enc\":{:.1},\"all_per_enc\":{:.1},\"truth_s\":{:.2}}}",
        sp.name, sp.n, nca, de, cells.len(), birth_fixed_cells, cells.iter().map(|c| c.m).max().unwrap_or(0),
        all_pairs, events, worst_rank, worst_m, kappa_req, w_max,
        misses, misses_nocl, arc_over_w_max,
        if events > 0 { rank4 as f64 / events as f64 } else { 0.0 },
        cand, all_pairs,
        if events > 0 { cand as f64 / events as f64 } else { 0.0 },
        if events > 0 { all_pairs as f64 / events as f64 } else { 0.0 },
        truth_s
    );
    let _ = &tst.evals;
}

// ---------------------------------------------------------------------------
// strongfield mode
// ---------------------------------------------------------------------------

/// Real roots of a u^3 + b u^2 + c u + d (trigonometric method; assumes three real roots).
fn cubic_roots(a: f64, b: f64, c: f64, d: f64) -> Vec<f64> {
    let (bn, cn, dn) = (b / a, c / a, d / a);
    let p = cn - bn * bn / 3.0;
    let q = 2.0 * bn * bn * bn / 27.0 - bn * cn / 3.0 + dn;
    let shift = -bn / 3.0;
    let disc = (q * q / 4.0 + p * p * p / 27.0).max(0.0);
    let s = disc.sqrt();
    let _ = s;
    // Three real roots: u_k = 2 sqrt(-p/3) cos((acos(3q/(2p) sqrt(-3/p))/... ) - 2 pi k/3)
    let mp = -p / 3.0;
    if mp <= 0.0 {
        return vec![];
    }
    let r = 2.0 * mp.sqrt();
    let arg = (3.0 * q / (p * mp.sqrt())) / 2.0;
    let arg = arg.clamp(-1.0, 1.0);
    let phi = arg.acos();
    let mut out = Vec::with_capacity(3);
    for k in 0..3 {
        out.push(r * ((phi / 3.0) - TAU * k as f64 / 3.0).cos() + shift);
    }
    out.sort_by(|x, y| x.total_cmp(y));
    out
}

/// Exact Schwarzschild turning points (mu=1) from (E, L). None if not bound.
/// Radial cubic 2L^2 u^3 - L^2 u^2 + 2u + (E^2-1) = 0; rad^2 = P(u) > 0 where allowed.
/// For E < 1 a bound orbit has three positive roots u_a < u_p < u_b (u_b is the inner plunge
/// barrier): the orbit is u in [u_a, u_p] — the TWO SMALLEST positive roots.
fn turning_points(e: f64, l: f64) -> Option<(f64, f64)> {
    let l2 = l * l;
    let roots = cubic_roots(2.0 * l2, -l2, 2.0, e * e - 1.0);
    if roots.len() < 3 || e >= 1.0 {
        return None;
    }
    let res_ok = |u: f64| {
        let r = 2.0 * l2 * u * u * u - l2 * u * u + 2.0 * u + (e * e - 1.0);
        let sc = 2.0 * l2 * u * u * u + l2 * u * u + 2.0 * u + (1.0 - e * e);
        r.abs() <= 1e-10 * sc
    };
    let pos: Vec<f64> = roots
        .iter()
        .copied()
        .filter(|&u| u > 1e-12 && res_ok(u))
        .collect();
    if pos.len() < 2 {
        return None;
    }
    let (ua, up) = (pos[0], pos[1]);
    if up <= ua {
        return None;
    }
    Some((1.0 / up, 1.0 / ua)) // (r_p, r_a)
}

/// (L_sep, L_circ) at energy e: roots of (1-e^2) r^2 + (3 e^2 - 4) r + 4 = 0.
fn l_bounds(e: f64) -> Option<(f64, f64)> {
    let a = 1.0 - e * e;
    let b = 3.0 * e * e - 4.0;
    let disc = b * b - 16.0 * a;
    if disc <= 0.0 || a <= 0.0 {
        return None;
    }
    let (r1, r2) = ((-b - disc.sqrt()) / (2.0 * a), (-b + disc.sqrt()) / (2.0 * a));
    if r1 <= 3.0 || r2 <= r1 {
        return None;
    }
    let l_u = r1 / (r1 - 3.0).sqrt();
    let l_c = (r2 * r2 / (r2 - 3.0)).sqrt();
    if l_u >= l_c {
        return None;
    }
    Some((l_u, l_c))
}

#[derive(Clone, Copy)]
struct SfBody {
    e: f64,
    l: f64,
    rp: f64,
    ra: f64,
    p: f64,
    ecc: f64,
}

#[derive(Clone, Copy)]
struct SfCell {
    ie: usize,
    il: usize,
    rp_min: f64,
    ra_max: f64,
    u_lo: f64,
    u_hi: f64,
    e_hi: f64,
    m: u32,
}

fn strongfield(seed: u64, n_target: usize, rho: f64) {
    let t0 = Instant::now();
    // --- belt: sample (r_p, r_a), solve (E, L) in closed form, verify via the cubic.
    let mut rng = Rng(seed);
    let mut bodies: Vec<SfBody> = Vec::with_capacity(n_target);
    let mut tries = 0u64;
    while bodies.len() < n_target && tries < 200 * n_target as u64 {
        tries += 1;
        let rp = 4.6 + 12.0 * rng.f64();
        let ra = rp + 3.0 + 190.0 * rng.f64();
        let num = 2.0 / rp - 2.0 / ra;
        let den = (1.0 - 2.0 / rp) / (rp * rp) - (1.0 - 2.0 / ra) / (ra * ra);
        if den <= 0.0 || num <= 0.0 {
            continue;
        }
        let l2 = num / den;
        let e2 = (1.0 - 2.0 / rp) * (1.0 + l2 / (rp * rp));
        if e2 >= 1.0 || e2 <= 0.0 {
            continue;
        }
        let (e, l) = (e2.sqrt(), l2.sqrt());
        let Some((rp2, ra2)) = turning_points(e, l) else { continue };
        if ((rp2 - rp) / rp).abs() > 1e-9 || ((ra2 - ra) / ra).abs() > 1e-9 {
            continue; // plunge or marginal
        }
        let p = 2.0 * rp * ra / (rp + ra);
        bodies.push(SfBody { e, l, rp, ra, p, ecc: (ra - rp) / (ra + rp) });
    }
    let n = bodies.len();
    let (rp_min_b, ra_max_b) = bodies
        .iter()
        .fold((f64::MAX, f64::MIN), |a, x| (a.0.min(x.rp), a.1.max(x.ra)));
    let (e_lo, e_hi) = bodies.iter().map(|x| x.e).fold((f64::MAX, f64::MIN), |a, x| (a.0.min(x), a.1.max(x)));
    let (l_lo, l_hi) = bodies.iter().map(|x| x.l).fold((f64::MAX, f64::MIN), |a, x| (a.0.min(x), a.1.max(x)));

    // --- (a) does U(L)|E turn? 200 E-columns x 512 L steps across the belt's E-range.
    let (mut cols, mut turns, mut cols_checked) = (0u32, 0u32, 0u32);
    let mut turn_worst_slack = f64::INFINITY;
    let mut turn_example: Option<(f64, f64, f64)> = None;
    for ic in 0..200 {
        let e = e_lo + (e_hi - e_lo) * (ic as f64 + 0.5) / 200.0;
        let Some((lu, lc)) = l_bounds(e) else { continue };
        cols_checked += 1;
        let k = 512;
        let mut us: Vec<f64> = Vec::with_capacity(k);
        for j in 0..k {
            let l = lu * (1.0 + 1e-6) + (lc * (1.0 - 1e-6) - lu * (1.0 + 1e-6)) * j as f64 / (k - 1) as f64;
            if let Some((rp, ra)) = turning_points(e, l) {
                us.push(1.0 / (2.0 * rp * ra / (rp + ra)));
            }
        }
        if us.len() < 8 {
            continue;
        }
        cols += 1;
        let mut dir = 0i32;
        let mut slack = f64::INFINITY;
        let mut l_at_turn = 0.0;
        for w in us.windows(2) {
            let d = w[1] - w[0];
            if d.abs() < 1e-12 {
                continue;
            }
            let s = if d > 0.0 { 1 } else { -1 };
            if dir == 0 {
                dir = s;
            } else if s != dir {
                turns += 1;
                if turn_example.is_none() {
                    turn_example = Some((e, l_at_turn, w[1]));
                }
                break;
            }
            slack = slack.min(d.abs() / w[1].abs().max(1e-12));
        }
        turn_worst_slack = turn_worst_slack.min(slack);
    }

    // --- key lattice on quantized (E, L); per-cell constants compiled on a 5x5 sub-grid
    //     clipped to the bound domain (the memo table's turning points).
    let (ne, nl) = (64usize, 256usize);
    let de = (e_hi - e_lo) / ne as f64;
    let dl = (l_hi - l_lo) / nl as f64;
    let clip = |e: f64, l: f64| -> Option<(f64, f64)> {
        let e = e.clamp(e_lo, e_hi);
        let (lu, lc) = l_bounds(e)?;
        Some((e, l.clamp(lu * (1.0 + 1e-9), lc * (1.0 - 1e-9))))
    };
    let mut cmap: std::collections::HashMap<(usize, usize), SfCell> = std::collections::HashMap::new();
    for x in &bodies {
        let ie = (((x.e - e_lo) / de).floor() as usize).min(ne - 1);
        let il = (((x.l - l_lo) / dl).floor() as usize).min(nl - 1);
        cmap.entry((ie, il)).or_insert_with(|| SfCell {
            ie,
            il,
            rp_min: f64::INFINITY,
            ra_max: f64::NEG_INFINITY,
            u_lo: f64::INFINITY,
            u_hi: f64::NEG_INFINITY,
            e_hi: 0.0,
            m: 0,
        })
        .m += 1;
    }
    let mut violations = 0u64;
    for ((ie, il), cell) in cmap.iter_mut() {
        for ai in 0..5 {
            for al in 0..5 {
                let e = e_lo + (ie.clone() as f64 + ai as f64 / 4.0) * de;
                let l = l_lo + (il.clone() as f64 + al as f64 / 4.0) * dl;
                if let Some((ec, lc)) = clip(e, l) {
                    if let Some((rp, ra)) = turning_points(ec, lc) {
                        let p = 2.0 * rp * ra / (rp + ra);
                        cell.rp_min = cell.rp_min.min(rp);
                        cell.ra_max = cell.ra_max.max(ra);
                        cell.u_lo = cell.u_lo.min(1.0 / p);
                        cell.u_hi = cell.u_hi.max(1.0 / p);
                        cell.e_hi = cell.e_hi.max((ra - rp) / (ra + rp));
                    }
                }
            }
        }
        if cell.rp_min.is_infinite() {
            cell.rp_min = rp_min_b;
            cell.ra_max = ra_max_b;
            cell.u_lo = 0.0;
            cell.u_hi = f64::INFINITY;
        }
    }
    for x in &bodies {
        let ie = (((x.e - e_lo) / de).floor() as usize).min(ne - 1);
        let il = (((x.l - l_lo) / dl).floor() as usize).min(nl - 1);
        let c = &cmap[&(ie, il)];
        let u = 1.0 / x.p;
        if x.rp < c.rp_min - 1e-9 || x.ra > c.ra_max + 1e-9 || u < c.u_lo - 1e-9 || u > c.u_hi + 1e-9 || x.ecc > c.e_hi + 1e-9 {
            violations += 1;
        }
    }
    let cells: Vec<SfCell> = cmap.values().copied().collect();

    // --- exact per-body tier: radial interval overlap +- rho; lattice zero-miss + inflation.
    let mut exact = 0u64;
    let mut missed = 0u64;
    for i in 0..n {
        let ci = &cmap[&((((bodies[i].e - e_lo) / de).floor() as usize).min(ne - 1), (((bodies[i].l - l_lo) / dl).floor() as usize).min(nl - 1))];
        for j in i + 1..n {
            let (xi, xj) = (&bodies[i], &bodies[j]);
            if xi.rp > xj.ra + rho || xj.rp > xi.ra + rho {
                continue;
            }
            exact += 1;
            let cj = &cmap[&((((xj.e - e_lo) / de).floor() as usize).min(ne - 1), (((xj.l - l_lo) / dl).floor() as usize).min(nl - 1))];
            let same = ci.ie == cj.ie && ci.il == cj.il;
            if !same && (ci.rp_min > cj.ra_max + 2.0 * rho || cj.rp_min > ci.ra_max + 2.0 * rho) {
                missed += 1;
            }
        }
    }
    let mut cand: u64 = cells.iter().map(|c| c.m as u64 * (c.m as u64 - 1) / 2).sum();
    for (a_idx, ca) in cells.iter().enumerate() {
        for cb in cells.iter().skip(a_idx + 1) {
            if !(ca.rp_min > cb.ra_max + 2.0 * rho || cb.rp_min > ca.ra_max + 2.0 * rho) {
                cand += ca.m as u64 * cb.m as u64;
            }
        }
    }

    // --- (c) U-band scan: naive per-column L-window (Newtonian contiguity) vs the table sweep.
    let band = |ca: &SfCell, cb: &SfCell| -> f64 {
        ca.u_hi.max(cb.u_hi) * (ca.e_hi + cb.e_hi) + 2.0 * rho * ca.u_hi * cb.u_hi
    };
    let u_close = |ca: &SfCell, cb: &SfCell| -> bool {
        let b = band(ca, cb);
        (cb.u_lo - ca.u_hi).max(ca.u_lo - cb.u_hi) <= b
    };
    // naive: partner cells are within a contiguous L-cell window (same or any E column).
    let lw = |cx: &SfCell| -> usize {
        let mut w = 0usize;
        'outer: loop {
            for cy in cells.iter() {
                if (cy.il as isize - cx.il as isize).abs() <= w as isize {
                    continue; // inside window
                }
                if u_close(cx, cy) {
                    w += 1;
                    continue 'outer;
                }
            }
            break;
        }
        w
    };
    let (mut exact_u, mut naive_miss, mut naive_pairs) = (0u64, 0u64, 0u64);
    for (a_idx, ca) in cells.iter().enumerate() {
        let w = lw(ca);
        for cb in cells.iter().skip(a_idx + 1) {
            if (cb.il as isize - ca.il as isize).abs() <= w as isize {
                naive_pairs += 1;
            }
            if u_close(ca, cb) {
                exact_u += 1;
                if (cb.il as isize - ca.il as isize).abs() > w as isize {
                    naive_miss += 1;
                }
            }
        }
    }
    // table sweep cost: sort by u_lo, two-pointer.
    let mut bylo: Vec<&SfCell> = cells.iter().collect();
    bylo.sort_by(|x, y| x.u_lo.total_cmp(&y.u_lo));
    let mut sweep_cost = 0u64;
    for s in 0..bylo.len() {
        let mut f = s + 1;
        while f < bylo.len() && bylo[f].u_lo <= bylo[s].u_hi + band(bylo[s], bylo[f]) {
            sweep_cost += 1;
            f += 1;
        }
    }
    println!(
        "{{\"exp\":\"strongfield\",\"n\":{},\"rho\":{},\"tries\":{},\"e_range\":[{:.4},{:.4}],\"l_range\":[{:.3},{:.3}],\
\"u_turn_cols\":{}/{}\",\"turn_slack_min\":{:.2e},\"turn_example\":{:?},\"cells\":{},\"cell_violations\":{},\
\"exact_pairs\":{},\"missed\":{},\"cand\":{},\"inflate\":{:.3},\"exact_u_pairs\":{},\"naive_miss\":{},\"naive_pairs\":{},\
\"sweep_cost\":{},\"wall_s\":{:.2}}}",
        n, rho, tries, e_lo, e_hi, l_lo, l_hi, turns, cols, turn_worst_slack, turn_example,
        cells.len(), violations, exact, missed, cand, cand as f64 / exact.max(1) as f64,
        exact_u, naive_miss, naive_pairs, sweep_cost, t0.elapsed().as_secs_f64()
    );
}

/// Newtonian positive control for the U-scan: same structure on a weak-field Kepler belt.
fn strongfield_control() {
    // Newtonian: U = 1/p with p = a(1-e^2) — a pure function of the belt; build the equivalent
    // (E ~ a, L ~ sqrt(p)) lattice and check the naive scan is complete there.
    let sp = spec("ctrl-r1e-2", 2000, 1e-2, 1e-3, 1.0, 1.5, 0, 40.0, 20261150);
    let b = make_belt(&sp);
    // key = quantized (a, L) exactly as the tube would; U = 1/p; e_hi from cells.
    let (a_lo, a_hi) = (sp.a_lo, sp.a_hi);
    let l_of = |x: &Body| (x.p).sqrt();
    let (l_lo, l_hi) = b.iter().map(l_of).fold((f64::MAX, f64::MIN), |a, x| (a.0.min(x), a.1.max(x)));
    let (ne, nl) = (64usize, 256usize);
    let de = (a_hi - a_lo) / ne as f64;
    let dl = (l_hi - l_lo) / nl as f64;
    let mut cmap: std::collections::HashMap<(usize, usize), SfCell> = std::collections::HashMap::new();
    let mut bodies: Vec<SfBody> = Vec::with_capacity(b.len());
    for x in &b {
        let ie = (((x.a - a_lo) / de).floor() as usize).min(ne - 1);
        let il = (((l_of(x) - l_lo) / dl).floor() as usize).min(nl - 1);
        bodies.push(SfBody { e: x.a, l: l_of(x), rp: x.rmin(), ra: x.rmax(), p: x.p, ecc: x.e });
        cmap.entry((ie, il)).or_insert_with(|| SfCell {
            ie, il,
            rp_min: (a_lo + ie as f64 * de) * (1.0 - 0.5),
            ra_max: (a_lo + (ie + 1) as f64 * de) * 1.5,
            u_lo: f64::INFINITY,
            u_hi: f64::NEG_INFINITY,
            e_hi: 0.0,
            m: 0,
        })
        .m += 1;
    }
    for c in cmap.values_mut() {
        c.e_hi = 0.5;
    }
    for x in &bodies {
        let ie = (((x.e - a_lo) / de).floor() as usize).min(ne - 1);
        let il = (((x.l - l_lo) / dl).floor() as usize).min(nl - 1);
        let c = cmap.get_mut(&(ie, il)).unwrap();
        let u = 1.0 / x.p;
        c.u_lo = c.u_lo.min(u);
        c.u_hi = c.u_hi.max(u);
    }
    let cells: Vec<SfCell> = cmap.values().copied().collect();
    let rho = sp.rho;
    let band = |ca: &SfCell, cb: &SfCell| -> f64 {
        ca.u_hi.max(cb.u_hi) * (ca.e_hi + cb.e_hi) + 2.0 * rho * ca.u_hi * cb.u_hi
    };
    let u_close = |ca: &SfCell, cb: &SfCell| -> bool {
        let bd = band(ca, cb);
        (cb.u_lo - ca.u_hi).max(ca.u_lo - cb.u_hi) <= bd
    };
    let lw = |cx: &SfCell| -> usize {
        let mut w = 0usize;
        'outer: loop {
            for cy in cells.iter() {
                if (cy.il as isize - cx.il as isize).abs() <= w as isize {
                    continue;
                }
                if u_close(cx, cy) {
                    w += 1;
                    continue 'outer;
                }
            }
            break;
        }
        w
    };
    let (mut exact_u, mut naive_miss) = (0u64, 0u64);
    for (a_idx, ca) in cells.iter().enumerate() {
        let w = lw(ca);
        for cb in cells.iter().skip(a_idx + 1) {
            if u_close(ca, cb) {
                exact_u += 1;
                if (cb.il as isize - ca.il as isize).abs() > w as isize {
                    naive_miss += 1;
                }
            }
        }
    }
    println!(
        "{{\"exp\":\"strongfield-ctrl\",\"n\":{},\"cells\":{},\"exact_u_pairs\":{},\"naive_miss\":{}}}",
        b.len(), cells.len(), exact_u, naive_miss
    );
}

fn main() {
    let mode = std::env::args().nth(1).unwrap_or_else(|| "belt".into());
    let t_start = Instant::now();
    match mode.as_str() {
        "belt" => {
            let specs = [
                spec("spread-r1e-3", 600, 1e-3, 1e-3, 1.0, 1.5, 0, 40.0, 20261101),
                spec("spread-r3e-2", 600, 3e-2, 1e-3, 1.0, 1.5, 0, 40.0, 20261102),
                spec("hot-s0.1", 600, 0.1, 1e-3, 1.0, 1.5, 0, 40.0, 20261103),
            ];
            for sp in &specs {
                let b = make_belt(sp);
                let radial = radial_pairs(&b, sp.rho);
                let cone = cone_pairs(&b, sp.rho).pairs.len();
                for nca in [256usize, 1024, 4096] {
                    let (keys, cells) = lattice0(&b, sp.a_lo, sp.a_hi, 0.5, nca, 256);
                    let (lp, _scanned, same_key) = lattice_pairs0(&b, &cells, sp.rho, 0);
                    let lset: std::collections::HashSet<(u32, u32)> =
                        lp.iter().map(|&(i, j)| (i.min(j), i.max(j))).collect();
                    let missed = radial.iter().filter(|&&(i, j)| !lset.contains(&(i.min(j), i.max(j)))).count();
                    let occupied = cells.iter().filter(|c| !c.members.is_empty()).count();
                    println!(
                        "{{\"exp\":\"belt\",\"spec\":\"{}\",\"n\":{},\"rho\":{},\"nca\":{},\"cells\":{},\
\"radial_pairs\":{},\"cone_pairs\":{},\"lattice_pairs\":{},\"same_key_pairs\":{},\"missed_radial\":{},\
\"inflate_vs_cone\":{:.3},\"inflate_vs_radial\":{:.3}}}",
                        sp.name, sp.n, sp.rho, nca, occupied, radial.len(), cone, lp.len(), same_key, missed,
                        lp.len() as f64 / cone as f64, lp.len() as f64 / radial.len().max(1) as f64
                    );
                    let _ = &keys;
                }
            }
        }
        "coorbital" => {
            let specs = [
                spec("coorbital", 300, 3e-4, 1e-3, 1.0, 1.0001, 0, 50.0, 20261001 + 9),
                spec("equal-period-keys", 300, 1e-2, 1e-3, 1.0, 1.001, 3, 50.0, 20261001 + 10),
            ];
            for sp in &specs {
                let b = make_belt(sp);
                let radial = radial_pairs(&b, sp.rho);
                let t0 = Instant::now();
                let mut events: Vec<(u32, u32, f64)> = Vec::new();
                let mut tst = TruthStats::default();
                let mut tmp = Vec::new();
                for &(i, j) in &radial {
                    tmp.clear();
                    truth_pair(&b[i as usize], &b[j as usize], sp.rho, sp.orbits * TAU, &mut tmp, &mut tst);
                    events.extend(tmp.iter().map(|&(t, _)| (i, j, t)));
                }
                let truth_s = t0.elapsed().as_secs_f64();
                let ranks: Vec<usize> = events
                    .iter()
                    .map(|&(i, j, t)| {
                        let li = b[i as usize].mean_anomaly(t) + b[i as usize].pom;
                        let lj = b[j as usize].mean_anomaly(t) + b[j as usize].pom;
                        let d = (li - lj).rem_euclid(TAU).min((lj - li).rem_euclid(TAU));
                        b.iter()
                            .enumerate()
                            .filter(|&(k, _)| k != i as usize && k != j as usize)
                            .filter(|&(_, x)| (x.mean_anomaly(t) + x.pom - li).rem_euclid(TAU) <= d)
                            .count()
                    })
                    .collect();
                let worst = ranks.iter().copied().max().unwrap_or(0);
                let cov = |k: usize| ranks.iter().filter(|&&r| r <= k).count();
                println!(
                    "{{\"exp\":\"coorbital\",\"spec\":\"{}\",\"n\":{},\"radial_pairs\":{},\"truth_events\":{},\
\"truth_s\":{:.2},\"rank_le4\":{},\"rank_le8\":{},\"rank_le16\":{},\"rank_le32\":{},\"worst_rank\":{}}}",
                    sp.name, sp.n, radial.len(), events.len(), truth_s, cov(4), cov(8), cov(16), cov(32), worst
                );
            }
        }
        "straggler" => {
            // The checker's scene: narrow-adversarial-like bands (uniform varpi, dense,
            // eccentric), the crate's own seed, 20 orbits.
            for n in [400usize, 800, 1600, 3200] {
                for nca in [1usize, 16] {
                    let sp = spec("narrow-adversarial", n, 0.025, 3e-3, 1.0, 1.0025, 0, 20.0, 20261001 + 8);
                    straggler_run(&sp, nca, 50);
                }
            }
            // Birth-fixed branch: equal integer periods inside a key => dn = 0, permanent order.
            for n in [300usize, 600, 1200] {
                let sp = spec("equal-period-keys", n, 1e-2, 1e-3, 1.0, 1.001, 3, 50.0, 20261001 + 10);
                straggler_run(&sp, 3, 50);
            }
        }
        "strongfield" => {
            strongfield(20261160, 4000, 0.05);
            strongfield_control();
        }
        "smoke" => {
            // plumbing check only (not part of the record)
            let sp = spec("smoke", 120, 0.025, 3e-3, 1.0, 1.0025, 0, 4.0, 20261001 + 8);
            straggler_run(&sp, 1, 50);
            strongfield(20261161, 300, 0.05);
        }
        _ => eprintln!("modes: belt | coorbital | straggler | strongfield | smoke"),
    }
    eprintln!("total_s: {:.2}", t_start.elapsed().as_secs_f64());
}
