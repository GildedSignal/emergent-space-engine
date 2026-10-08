//! Second author on 20261008-1150-system-cf13. The checker killed the in-band scale (rank count
//! from MEAN spacing silently misses 76% of a convoy's encounters) and named the gold experiment:
//! replace it with an ANGULAR window |Δλ| ≤ c·2·e_hi + drift margin, materialized by range search
//! over the sorted longitudes (cost = window × local density), then re-run all four scenes plus
//! CONVOY and a clustered Trojan cloud, 0 missed required; and judge kick locality (r8 v4 case (d)
//! gates: kick_setup_ratio ≤ 1.05, other_certificates_touched = 0).
//!
//! Scenes: F1 fleet, F2 swarm, X crossing fleets, B belt, CONVOY (clustered phase, the killer
//! case), TROJANC (clustered co-orbital cloud). Configs as before: truth | cone | band | globalrank.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{cone_pairs, is_candidate, radial_pairs, Sorted};
use emergent_encounters::truth::{truth_pair, TruthStats};
use emergent_encounters::par_chunks;
use std::collections::HashSet;
use std::f64::consts::TAU;

const THREADS: usize = 6;
const SAFETY: f64 = 1.1;
/// Margin over the encounter bound |Δλ| ≤ 2(e_i+e_j) at a meeting: 2.5 covers ρ/r and the
/// second-order equation of center (same constant as the run being corrected).
const RANK_SAFETY: f64 = 2.5;
/// Work cap on drift-bound renewals per band; above it the drift term swallows the window
/// (half-window ≥ π ⇒ all in-band pairs: the rank path self-destructs, the cone carries).
const MAX_RENEWALS: u64 = 64;

type Enc = (u32, u32, f64, f64);

struct Scene {
    name: &'static str,
    bodies: Vec<Body>,
    rho: f64,
    orbits: f64,
}
fn rayleigh(rng: &mut Rng, s: f64) -> f64 {
    let u = rng.f64();
    s * (-2.0 * (1.0 - u).ln()).sqrt()
}

fn scene(arg: &str) -> Scene {
    let name: &'static str = match arg {
        "F1" => "F1",
        "F2" => "F2",
        "X" => "X",
        "B" => "B",
        "CONVOY" => "CONVOY",
        "TROJANC" => "TROJANC",
        _ => panic!("unknown scene {arg}"),
    };
    let mut rng = Rng(0x5EED_2026_1008);
    let (n, rho, orbits): (usize, f64, f64) = match name {
        "F1" => (500, 1e-4, 30.0),
        "F2" => (600, 3e-4, 20.0),
        "X" => (500, 1e-3, 30.0),
        "B" => (1000, 1e-4, 100.0),
        // the checker's exact killer case: F1's a/e, longitudes clustered in 0.1 rad
        "CONVOY" => (500, 1e-4, 30.0),
        // clustered co-orbital cloud: checker's TROJAN but with λ packed in 0.3 rad
        "TROJANC" => (500, 3e-4, 20.0),
        _ => panic!(),
    };
    let mut bodies = Vec::new();
    match name {
        "F1" => {
            for _ in 0..n {
                let a = 1.0 + 3e-5 * rng.f64();
                let e = rayleigh(&mut rng, 1e-3);
                bodies.push(Body::new(a, e, TAU * rng.f64(), TAU * rng.f64()));
            }
        }
        "F2" => {
            for _ in 0..n {
                let a = 1.0 + 1e-4 * rng.f64();
                let e = rayleigh(&mut rng, 3e-3);
                bodies.push(Body::new(a, e, TAU * rng.f64(), TAU * rng.f64()));
            }
        }
        "X" => {
            for _ in 0..250 {
                let a = 1.0 + 2e-5 * rng.f64();
                let e = 0.20 + rayleigh(&mut rng, 3e-3);
                bodies.push(Body::new(a, e, 0.3, TAU * rng.f64()));
            }
            for _ in 0..250 {
                let a = 1.19 + 2e-5 * rng.f64();
                let e = 0.16 + rayleigh(&mut rng, 3e-3);
                bodies.push(Body::new(a, e, std::f64::consts::PI, TAU * rng.f64()));
            }
        }
        "B" => {
            for _ in 0..n {
                let a = 1.0 + 0.5 * rng.f64();
                let e = rayleigh(&mut rng, 1e-2);
                bodies.push(Body::new(a, e, TAU * rng.f64(), TAU * rng.f64()));
            }
        }
        "CONVOY" => {
            for _ in 0..n {
                let a = 1.0 + 3e-5 * rng.f64();
                let e = rayleigh(&mut rng, 1e-3);
                let m0 = 0.1 * rng.f64();
                let pom = 0.1 * rng.f64();
                bodies.push(Body::new(a, e, pom, m0 + pom));
            }
        }
        "TROJANC" => {
            for _ in 0..n {
                let a = 1.0 + 1e-6 * rng.f64();
                let e = rayleigh(&mut rng, 1e-3);
                let pom = TAU * rng.f64();
                let lam0 = 1.0 + 0.3 * rng.f64();
                bodies.push(Body::new(a, e, pom, lam0));
            }
        }
        _ => unreachable!(),
    }
    Scene { name, bodies, rho, orbits }
}

fn run_pairs(b: &[Body], pairs: &[(u32, u32)], rho: f64, t_end: f64) -> (Vec<Enc>, Stats) {
    let parts = par_chunks(pairs.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &pairs[r] {
            tmp.clear();
            pair_events(&b[i as usize], &b[j as usize], rho, SAFETY, 0.0, t_end, &mut st, &mut tmp);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let mut all = Vec::new();
    let mut st = Stats::default();
    for (o, s) in parts {
        all.extend(o);
        st.add(&s);
    }
    (all, st)
}

fn run_truth(b: &[Body], pairs: &[(u32, u32)], rho: f64, t_end: f64) -> (Vec<Enc>, TruthStats) {
    let parts = par_chunks(pairs.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = TruthStats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &pairs[r] {
            tmp.clear();
            truth_pair(&b[i as usize], &b[j as usize], rho, t_end, &mut tmp, &mut st);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let mut all = Vec::new();
    let mut st = TruthStats::default();
    for (o, s) in parts {
        all.extend(o);
        st.add(&s);
    }
    (all, st)
}

/// (missed, false, matched) with pair+time matching, edges excluded as in the crate's harness.
fn matchup(truth: &[Enc], meth: &[Enc], t_end: f64, tol: f64) -> (usize, usize, usize) {
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
    let mut by_pair: std::collections::HashMap<(u32, u32), Vec<f64>> = std::collections::HashMap::new();
    for e in meth.iter().filter(|e| inside(e.2)) {
        by_pair.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut tby: std::collections::HashMap<(u32, u32), Vec<f64>> = std::collections::HashMap::new();
    for e in truth.iter().filter(|e| inside(e.2)) {
        tby.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut missed = 0;
    let mut matched = 0;
    for e in truth.iter().filter(|e| inside(e.2)) {
        if by_pair.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < tol)) {
            matched += 1;
        } else {
            missed += 1;
        }
    }
    let mut false_ = 0;
    for e in meth.iter().filter(|e| inside(e.2)) {
        if !tby.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < tol)) {
            false_ += 1;
        }
    }
    (missed, false_, matched)
}

fn mean_longitude(x: &Body, t: f64) -> f64 {
    (x.mean_anomaly(t) + x.pom).rem_euclid(TAU)
}

/// The unified certificate's in-band part with the ANGULAR scale the checker specified: pairs are
/// materialized by range search over the sorted mean longitudes with half-window
///   half = RANK_SAFETY·2·e_hi  +  dn·(t_end/renewals),
/// the encounter bound at a meeting plus the drift since the last renewal. Cost is
/// window × local density: a convoy pays its true local density, not the mean one.
/// Renewals: enough that the drift term stays within one encounter window
/// (need = ceil(dn·t_end / w_enc), clamped to MAX_RENEWALS; when the clamp bites, the window
/// swells — at half ≥ π it self-destructs to all in-band pairs and the cone carries).
/// Returns (pairs, max renewals, max half-window).
fn band_window_pairs(b: &[Body], band_of: &[u32], n_bands: u32, t_end: f64) -> (Vec<(u32, u32)>, u64, f64) {
    let w_mul = std::env::var("W_SAFETY").ok().and_then(|v| v.parse::<f64>().ok()).unwrap_or(1.0);
    let mut pairs: HashSet<(u32, u32)> = HashSet::new();
    let mut renewals_max = 0u64;
    let mut half_max = 0.0f64;
    for band in 0..n_bands {
        let members: Vec<u32> = (0..b.len() as u32).filter(|&i| band_of[i as usize] == band).collect();
        if members.len() < 2 {
            continue;
        }
        let nmax = members.iter().map(|&i| b[i as usize].n).fold(f64::MIN, f64::max);
        let nmin = members.iter().map(|&i| b[i as usize].n).fold(f64::MAX, f64::min);
        let dn = nmax - nmin;
        let e_hi = members.iter().map(|&i| b[i as usize].e).fold(0.0, f64::max);
        // Encounter bound: at a meeting the true longitudes are equal, so |Δλ| ≲ 2(e_i+e_j) ≤ 4·e_hi.
        let w_enc = w_mul * RANK_SAFETY * 2.0 * e_hi;
        // Drift bound: relative mean longitude moves at most dn; renew so the drift term stays
        // within one encounter window, capped by the renewal budget.
        let drift_total = dn * t_end;
        let need = if w_enc > 0.0 { (drift_total / w_enc).ceil() as u64 } else { u64::MAX / 2 };
        let renewals = need.clamp(1, MAX_RENEWALS);
        let drift = drift_total / renewals as f64;
        let half = w_enc + drift;
        renewals_max = renewals_max.max(renewals);
        half_max = half_max.max(half);
        if half >= std::f64::consts::PI {
            // self-destruction: the drift bound refuses the tier, materialize everything in-band
            for (s, &i) in members.iter().enumerate() {
                for &j in &members[s + 1..] {
                    pairs.insert((i.min(j), i.max(j)));
                }
            }
            continue;
        }
        for r in 0..renewals {
            let t = t_end * r as f64 / renewals as f64;
            let mut ls: Vec<(f64, u32)> = members.iter().map(|&i| (mean_longitude(&b[i as usize], t), i)).collect();
            ls.sort_by(|x, y| x.0.total_cmp(&y.0));
            let m = ls.len();
            for q in 0..m {
                let (lq, iq) = ls[q];
                // forward circular arc within `half`: counts every pair exactly once
                let mut j = q + 1;
                while j < m && ls[j].0 - lq <= half {
                    let ij = ls[j].1;
                    pairs.insert((iq.min(ij), iq.max(ij)));
                    j += 1;
                }
                let end = lq + half;
                if end >= TAU {
                    let target = end - TAU;
                    let mut jj = 0;
                    while jj < m && ls[jj].0 <= target {
                        if jj != q {
                            let ij = ls[jj].1;
                            pairs.insert((iq.min(ij), iq.max(ij)));
                        }
                        jj += 1;
                    }
                }
            }
        }
    }
    (pairs.into_iter().collect(), renewals_max, half_max)
}

/// Bands over Binet U with the width from the drift bound (unchanged from the run under correction).
fn band_assignment(b: &[Body], t_end: f64) -> (Vec<u32>, u32, f64) {
    let us: Vec<f64> = b.iter().map(|x| x.binet()[0]).collect();
    let (u_lo, u_hi) = us.iter().fold((f64::MAX, f64::MIN), |(a, c), &u| (a.min(u), c.max(u)));
    let span = (u_hi - u_lo).max(1e-12);
    let u_mid = 0.5 * (u_lo + u_hi);
    let mut w = (TAU * span / (1.5 * u_mid.powf(2.5) * t_end * b.len() as f64)).sqrt();
    if w > span {
        w = span;
    }
    let mut n_bands = ((span / w).ceil() as u32).max(1);
    if let Some(nb) = std::env::var("BANDS").ok().and_then(|v| v.parse::<u32>().ok()) {
        n_bands = nb.max(1);
    }
    let w = span / n_bands as f64;
    let band_of: Vec<u32> = us.iter().map(|&u| (((u - u_lo) / w).floor() as u32).min(n_bands - 1)).collect();
    (band_of, n_bands, w)
}

fn scene_mode(name: &str) {
    let sc = scene(name);
    let t_end = sc.orbits * TAU;
    let b = &sc.bodies;
    let rho = sc.rho;
    let tol = 0.02;

    // ---------- truth ----------
    let t0 = std::time::Instant::now();
    let rp = radial_pairs(b, rho);
    let (truth, tst) = run_truth(b, &rp, rho, t_end);
    let truth_ms = t0.elapsed().as_millis();
    let n_truth = truth.iter().filter(|e| e.2 > 0.05 && e.2 < t_end - 0.05).count();
    println!(
        "{{\"scene\":\"{}\",\"cfg\":\"truth\",\"n\":{},\"radial_pairs\":{},\"enc\":{},\"truth_steps\":{},\"truth_ms\":{}}}",
        sc.name, b.len(), rp.len(), n_truth, tst.steps, truth_ms
    );

    // ---------- cone (crate as-is) ----------
    let t0 = std::time::Instant::now();
    let cp = cone_pairs(b, rho);
    let (ev, st) = run_pairs(b, &cp.pairs, rho, t_end);
    let cone_ms = t0.elapsed().as_millis();
    let (missed, false_, matched) = matchup(&truth, &ev, t_end, tol);
    println!(
        "{{\"scene\":\"{}\",\"cfg\":\"cone\",\"pairs\":{},\"scanned\":{},\"evals\":{},\"checks\":{},\"hits\":{},\"sections\":[{},{},{}],\"missed\":{},\"false\":{},\"matched\":{},\"ms\":{}}}",
        sc.name, cp.pairs.len(), cp.scanned, st.evals, st.checks_total(), st.hits_total(),
        st.sections[0], st.sections[1], st.sections[2], missed, false_, matched, cone_ms
    );

    // ---------- band (unified certificate, angular in-band scale) ----------
    let t0 = std::time::Instant::now();
    let (band_of, n_bands, w_band) = band_assignment(b, t_end);
    let (mut pairs, renewals, half) = band_window_pairs(b, &band_of, n_bands, t_end);
    let same_band = |i: u32, j: u32| band_of[i as usize] == band_of[j as usize];
    let cp = cone_pairs(b, rho);
    let cross: Vec<(u32, u32)> = cp.pairs.iter().cloned().filter(|&(i, j)| !same_band(i, j)).collect();
    let in_band_kept = pairs.len();
    for &p in &cross {
        pairs.push(p);
    }
    pairs.sort_unstable();
    pairs.dedup();
    let (ev2, st2) = run_pairs(b, &pairs, rho, t_end);
    let band_ms = t0.elapsed().as_millis();
    let (missed2, false2, matched2) = matchup(&truth, &ev2, t_end, tol);
    println!(
        "{{\"scene\":\"{}\",\"cfg\":\"band\",\"band_w\":{:.3e},\"n_bands\":{},\"renewals\":{},\"half_win\":{:.5},\"pairs\":{},\"in_band_kept\":{},\"cross_pairs\":{},\"evals\":{},\"checks\":{},\"hits\":{},\"missed\":{},\"false\":{},\"matched\":{},\"ms\":{}}}",
        sc.name, w_band, n_bands, renewals, half, pairs.len(), in_band_kept, cross.len(), st2.evals, st2.checks_total(), st2.hits_total(), missed2, false2, matched2, band_ms
    );

    // ---------- globalrank (negative control: no bands, one angular window over everything) ----------
    let t0 = std::time::Instant::now();
    let all_one: Vec<u32> = vec![0; b.len()];
    let (gp, _, ghalf) = band_window_pairs(b, &all_one, 1, t_end);
    let (ev3, st3) = run_pairs(b, &gp, rho, t_end);
    let g_ms = t0.elapsed().as_millis();
    let (missed3, false3, matched3) = matchup(&truth, &ev3, t_end, tol);
    println!(
        "{{\"scene\":\"{}\",\"cfg\":\"globalrank\",\"half_win\":{:.5},\"pairs\":{},\"evals\":{},\"checks\":{},\"missed\":{},\"false\":{},\"matched\":{},\"ms\":{}}}",
        sc.name, ghalf, gp.len(), st3.evals, st3.checks_total(), missed3, false3, matched3, g_ms
    );
}

/// r8 v4 case (d), cheapest decisive part: kicks are LOCAL iff one kick re-sets-up only the
/// kicked body's pairs (ratio vs its cone candidate count ≤ 1.05) and touches no pair
/// certificate between other bodies. We measure the certificate's own bookkeeping: after a kick
/// the affected bands are recomputed; pairs among other bodies that appear or disappear are
/// `other_certificates_touched` (a removal is counted too: conservative upper bound).
/// The kicked body's candidate count: its cone partners (the crate's own candidate rule).
fn cone_partners(b: &[Body], bi: &Body, rho: f64) -> usize {
    let s = Sorted::new(b, rho);
    let reach = s.reach(bi);
    let (lo, hi) = s.range(bi.binet()[0], reach);
    s.order[lo..hi]
        .iter()
        .filter(|&&(_, j)| is_candidate(bi, &b[j as usize], rho))
        .count()
}

fn kick_mode(name: &str) {
    /// Marker for a body that left the phase tier after a kick; the cone carries it.
    const CONE_TIER: u32 = u32::MAX;
    let (mut b, rho, t_end): (Vec<Body>, f64, f64) = match name {
        "KICKBELT" => {
            let mut rng = Rng(0x5EED_2026_1008);
            let mut b = Vec::new();
            for _ in 0..10_000 {
                let a = 1.0 + 0.5 * rng.f64();
                let e = rayleigh(&mut rng, 1e-2);
                b.push(Body::new(a, e, TAU * rng.f64(), TAU * rng.f64()));
            }
            (b, 1e-4, 20.0 * TAU)
        }
        "KICKCONVOY" => {
            let sc = scene("CONVOY");
            (sc.bodies, sc.rho, sc.orbits * TAU)
        }
        _ => panic!("unknown kick scene"),
    };
    let (mut band_of, n_bands, w_band) = band_assignment(&b, t_end);
    let us_lo = b.iter().map(|x| x.binet()[0]).fold(f64::MAX, f64::min);

    let mut rng = Rng(0xC1CADA_2026_1008);
    let mut ratios: Vec<f64> = Vec::new();
    let mut other_touched_total = 0usize;
    let mut other_touched_max = 0usize;
    let mut other_added_total = 0usize;
    let mut band_left = 0usize;
    let mut tier_exit = 0usize;
    let t0 = std::time::Instant::now();
    for _kick in 0..100 {
        let k = (rng.f64() * b.len() as f64) as usize;
        let old = &b[k];
        let sign = if rng.f64() < 0.5 { -1.0 } else { 1.0 };
        let a_new = (old.a * (1.0 + sign * 1e-3)).max(1.0005).min(1.4995);
        let new_body = Body::new(a_new, old.e, old.pom, old.pom + old.mean_anomaly(0.0));
        let band_old = band_of[k];
        // Was k in the phase tier? (a cone-tier body stays in the cone tier)
        let was_in = band_old != CONE_TIER;
        let u_new = new_body.binet()[0];
        let band_new = (((u_new - us_lo) / w_band).floor() as u32).min(n_bands - 1);
        // Tier-exit policy: "fit" keeps the kicked body in the phase tier when it still fits its
        // band's geometric n-envelope (dn ≈ 1.5·w·u^2.5, the drift bound's own formula);
        // "exit" demotes any kicked body to the cone tier — strict locality, its pairs go to the
        // cone until it re-enters at a renewal. In both cases one kick changes no other body's
        // relative drifts; only stay-in-tier kicks can widen a band window (measured).
        let policy_exit = std::env::var("KICK_POLICY").ok().as_deref() == Some("exit");
        let (in_tier, band_now) = if !was_in || policy_exit {
            (false, CONE_TIER)
        } else {
            let others_n: Vec<f64> = (0..b.len())
                .filter(|&i| i != k && band_of[i] == band_old)
                .map(|i| b[i].n)
                .collect();
            let mut sorted = others_n.clone();
            sorted.sort_by(|x, y| x.total_cmp(y));
            let med = sorted[sorted.len() / 2];
            let u_mid = 0.5 * (u_new + b[k].binet()[0]);
            let envelope = 1.5 * w_band * u_mid.powf(2.5);
            let fits = band_new == band_old && (new_body.n - med).abs() <= envelope;
            (fits, if fits { band_new } else { CONE_TIER })
        };
        if was_in && band_new != band_old {
            band_left += 1;
        }
        if was_in && !in_tier {
            tier_exit += 1;
        }
        // Bands whose windows recompute: the one k left, and the one k entered (same one if it stayed).
        let mut affected: Vec<u32> = Vec::new();
        if was_in {
            affected.push(band_old);
        }
        if in_tier {
            if band_new != band_old {
                affected.push(band_new);
            }
        }
        affected.sort_unstable();
        affected.dedup();
        // Window pairs of the affected bands: `kb` is where k sits (CONE_TIER = nowhere),
        // `bk` its body there. Old world: k at band_old with the old elements.
        let windows_of = |bk: Option<&Body>, kb: u32| -> HashSet<(u32, u32)> {
            let mut pairs = HashSet::new();
            for &band in &affected {
                let mut mem: Vec<u32> = (0..b.len() as u32)
                    .filter(|&i| band_of[i as usize] == band && i != k as u32)
                    .collect();
                if band == kb {
                    if bk.is_some() {
                        mem.push(k as u32);
                    }
                }
                if mem.len() < 2 {
                    continue;
                }
                let body_of = |i: u32| -> (f64, f64, f64) {
                    if i == k as u32 {
                        let bk = bk.expect("k in mem");
                        (bk.n, bk.e, 0.0)
                    } else {
                        (b[i as usize].n, b[i as usize].e, 0.0)
                    }
                };
                let nmax = mem.iter().map(|&i| body_of(i).0).fold(f64::MIN, f64::max);
                let nmin = mem.iter().map(|&i| body_of(i).0).fold(f64::MAX, f64::min);
                let e_hi = mem.iter().map(|&i| body_of(i).1).fold(0.0, f64::max);
                let w_enc = RANK_SAFETY * 2.0 * e_hi;
                let dn = nmax - nmin;
                let drift_total = dn * t_end;
                let need = if w_enc > 0.0 { (drift_total / w_enc).ceil() as u64 } else { u64::MAX / 2 };
                let renewals = need.clamp(1, MAX_RENEWALS);
                let drift = drift_total / renewals as f64;
                let half = w_enc + drift;
                let lam = |i: u32, t: f64| -> f64 {
                    if i == k as u32 {
                        mean_longitude(bk.expect("k in mem"), t)
                    } else {
                        mean_longitude(&b[i as usize], t)
                    }
                };
                if half >= std::f64::consts::PI {
                    for (s, &i) in mem.iter().enumerate() {
                        for &j in &mem[s + 1..] {
                            pairs.insert((i.min(j), i.max(j)));
                        }
                    }
                    continue;
                }
                for r in 0..renewals {
                    let t = t_end * r as f64 / renewals as f64;
                    let mut ls: Vec<(f64, u32)> = mem.iter().map(|&i| (lam(i, t), i)).collect();
                    ls.sort_by(|x, y| x.0.total_cmp(&y.0));
                    let m = ls.len();
                    for q in 0..m {
                        let (lq, iq) = ls[q];
                        let mut j = q + 1;
                        while j < m && ls[j].0 - lq <= half {
                            let ij = ls[j].1;
                            pairs.insert((iq.min(ij), iq.max(ij)));
                            j += 1;
                        }
                        let end = lq + half;
                        if end >= TAU {
                            let target = end - TAU;
                            let mut jj = 0;
                            while jj < m && ls[jj].0 <= target {
                                if jj != q {
                                    let ij = ls[jj].1;
                                    pairs.insert((iq.min(ij), iq.max(ij)));
                                }
                                jj += 1;
                            }
                        }
                    }
                }
            }
            pairs
        };
        let p_old = if was_in { windows_of(Some(&b[k]), band_old) } else { HashSet::new() };
        let p_new = windows_of(if in_tier { Some(&new_body) } else { None }, band_now);
        // Other certificates touched: pairs among other bodies that appear (added) or
        // disappear (removed) when the affected bands recompute.
        let mut added = 0usize;
        let mut removed = 0usize;
        for &(i, j) in p_old.symmetric_difference(&p_new) {
            if i != k as u32 && j != k as u32 {
                if p_new.contains(&(i, j)) {
                    added += 1;
                } else {
                    removed += 1;
                }
            }
        }
        other_touched_total += added + removed;
        other_touched_max = other_touched_max.max(added + removed);
        other_added_total += added;
        // Pairs set up for the kicked body: its window pairs plus the cone partners outside them.
        b[k] = new_body;
        let cand = cone_partners(&b, &b[k], rho);
        let mut set_up = p_new.iter().filter(|&&(i, j)| i == k as u32 || j == k as u32).count();
        {
            // cone partners of k that are not already window partners (cross-band, or all if out)
            let s = Sorted::new(&b, rho);
            let reach = s.reach(&b[k]);
            let (lo, hi) = s.range(b[k].binet()[0], reach);
            for &(_, j) in &s.order[lo..hi] {
                let j = j as usize;
                let pair = (k.min(j) as u32, k.max(j) as u32);
                let j_tier = band_of[j] != CONE_TIER;
                let same = in_tier && j_tier && band_of[j] == band_now;
                if j != k && !same && !p_new.contains(&pair) && is_candidate(&b[k], &b[j], rho) {
                    set_up += 1;
                }
            }
        }
        ratios.push(set_up as f64 / cand.max(1) as f64);
        band_of[k] = band_now;
    }
    ratios.sort_by(|x, y| x.total_cmp(y));
    let median = ratios[ratios.len() / 2];
    println!(
        "{{\"scene\":\"{}\",\"cfg\":\"kicks\",\"kicks\":100,\"band_left\":{},\"tier_exit\":{},\"kick_setup_ratio_median\":{:.4},\"kick_setup_ratio_p90\":{:.4},\"kick_setup_ratio_max\":{:.4},\"other_certificates_touched\":{},\"other_added\":{},\"other_certificates_touched_max\":{},\"ms\":{}}}",
        name, band_left, tier_exit, median, ratios[90], ratios[ratios.len() - 1], other_touched_total, other_added_total, other_touched_max, t0.elapsed().as_millis()
    );
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let owned = args.get(1).cloned().unwrap_or_else(|| "F1".into());
    if owned.starts_with("KICK") {
        kick_mode(&owned);
    } else {
        scene_mode(&owned);
    }
}
