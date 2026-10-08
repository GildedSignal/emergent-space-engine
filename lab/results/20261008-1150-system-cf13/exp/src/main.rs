//! One certificate, not three: is the phase-neighbour certificate (taleb-09b5) the degenerate
//! readout of the crate's own Binet-cone + Diophantine schedule, with the band width set by the
//! certificate horizon (a work measure, not a tuned trigger)?
//!
//! Scenes: F1 fleet, F2 co-orbital swarm, X two crossing fleets, B belt control.
//! Configs: truth | cone (crate as-is) | band (unified: in-band rank certificate with
//! drift-bound renewals + cross-band cone) | globalrank (negative control: no bands).
//! One JSON line per (scene, config).

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{cone_pairs, radial_pairs};
use emergent_encounters::truth::{truth_pair, TruthStats};
use emergent_encounters::par_chunks;
use std::collections::HashSet;
use std::f64::consts::TAU;

const THREADS: usize = 6;
const SAFETY: f64 = 1.1;
/// Rank margin over the encounter bound |Δλ| ≤ 2(e_i+e_j): 2.5 covers ρ/r and second-order terms.
const RANK_SAFETY: f64 = 2.5;
/// Work cap on drift-bound renewals per band; above it the margin swallows the band (fall back to
/// materializing the band's cone candidates). A work measure, not a physics trigger.
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
        _ => panic!("unknown scene"),
    };
    let mut rng = Rng(0x5EED_2026_1008);
    let (n, rho, orbits): (usize, f64, f64) = match name {
        "F1" => (500, 1e-4, 30.0),
        "F2" => (600, 3e-4, 20.0),
        "X" => (500, 1e-3, 30.0),
        "B" => (1000, 1e-4, 100.0),
        _ => panic!("unknown scene"),
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

/// The unified certificate's in-band part: rank by mean longitude, margin from the drift bound.
/// Returns (pairs, max renewals, max rank margin).
fn band_rank_pairs(b: &[Body], band_of: &[u32], n_bands: u32, t_end: f64) -> (Vec<(u32, u32)>, u64, u64) {
    let mut pairs: HashSet<(u32, u32)> = HashSet::new();
    let mut renewals_max = 0u64;
    let mut margin_max = 0u64;
    for band in 0..n_bands {
        let members: Vec<u32> = (0..b.len() as u32).filter(|&i| band_of[i as usize] == band).collect();
        if members.len() < 2 {
            continue;
        }
        let spacing = TAU / members.len() as f64;
        let nmax = members.iter().map(|&i| b[i as usize].n).fold(f64::MIN, f64::max);
        let nmin = members.iter().map(|&i| b[i as usize].n).fold(f64::MAX, f64::min);
        let dn = nmax - nmin;
        let e_hi = members.iter().map(|&i| b[i as usize].e).fold(0.0, f64::max);
        // Encounters need |Δλ| ≲ 2(e_i+e_j) at the meeting (equal true longitude).
        let k_enc = ((RANK_SAFETY * 2.0 * e_hi) / spacing).ceil() as u64 + 1;
        // Drift bound: relative longitude moves at most dn; renew so ranks move ≤ 1 spacing.
        let need = ((dn * t_end) / spacing).ceil() as u64;
        let renewals = need.clamp(1, MAX_RENEWALS);
        let margin = ((dn * t_end) / (renewals as f64 * spacing)).ceil() as u64;
        renewals_max = renewals_max.max(renewals);
        margin_max = margin_max.max(margin);
        let k = std::env::var("K_OVERRIDE").ok().and_then(|v| v.parse::<u64>().ok()).map_or(k_enc + margin, |ko| ko + margin) as usize;
        let m = members.len();
        for r in 0..renewals {
            let t = t_end * r as f64 / renewals as f64;
            let mut ls: Vec<(f64, u32)> = members.iter().map(|&i| (mean_longitude(&b[i as usize], t), i)).collect();
            ls.sort_by(|x, y| x.0.total_cmp(&y.0));
            for q in 0..m {
                let iq = ls[q].1;
                for s in 1..=k.min(m - 1) {
                    for qq in [(q + s) % m, (q + m - s) % m] {
                        let iq2 = ls[qq].1;
                        if iq == iq2 {
                            continue;
                        }
                        pairs.insert((iq.min(iq2), iq.max(iq2)));
                    }
                }
            }
        }
    }
    (pairs.into_iter().collect(), renewals_max, margin_max)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let owned = args.get(1).cloned().unwrap_or_else(|| "F1".into());
    let scene_name: &str = &owned;
    let sc = scene(scene_name);
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

    // ---------- band (unified certificate) ----------
    let t0 = std::time::Instant::now();
    let us: Vec<f64> = b.iter().map(|x| x.binet()[0]).collect();
    let (u_lo, u_hi) = us.iter().fold((f64::MAX, f64::MIN), |(a, c), &u| (a.min(u), c.max(u)));
    let span = (u_hi - u_lo).max(1e-12);
    // w from: dn(w)·t_end ≤ spacing(w) with dn ≈ 1.5·w·u^2.5 (n = u^1.5) and spacing = TAU/n_band,
    // n_band ≈ n·w/span  =>  w = sqrt(TAU·span / (1.5·u^2.5·t_end·n)).
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
    let (mut pairs, renewals, margin) = band_rank_pairs(b, &band_of, n_bands, t_end);
    // cross-band pairs: the cone, restricted to pairs in different bands
    let same_band = |i: u32, j: u32| band_of[i as usize] == band_of[j as usize];
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
        "{{\"scene\":\"{}\",\"cfg\":\"band\",\"band_w\":{:.3e},\"n_bands\":{},\"renewals\":{},\"margin\":{},\"pairs\":{},\"in_band_kept\":{},\"cross_pairs\":{},\"evals\":{},\"checks\":{},\"hits\":{},\"missed\":{},\"false\":{},\"matched\":{},\"ms\":{}}}",
        sc.name, w, n_bands, renewals, margin, pairs.len(), in_band_kept, cross.len(), st2.evals, st2.checks_total(), st2.hits_total(), missed2, false2, matched2, band_ms
    );

    // ---------- globalrank (negative control: no bands, pure phase sort over all bodies) ----------
    let t0 = std::time::Instant::now();
    let all_one: Vec<u32> = vec![0; b.len()];
    let (gp, _, _) = band_rank_pairs(b, &all_one, 1, t_end);
    let (ev3, st3) = run_pairs(b, &gp, rho, t_end);
    let g_ms = t0.elapsed().as_millis();
    let (missed3, false3, matched3) = matchup(&truth, &ev3, t_end, tol);
    println!(
        "{{\"scene\":\"{}\",\"cfg\":\"globalrank\",\"pairs\":{},\"evals\":{},\"checks\":{},\"missed\":{},\"false\":{},\"matched\":{},\"ms\":{}}}",
        sc.name, gp.len(), st3.evals, st3.checks_total(), missed3, false3, matched3, g_ms
    );
}
