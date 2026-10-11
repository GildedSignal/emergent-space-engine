//! The fix probe (second-author run 20261011-0614-second-20261011-0517-taleb-3ebf-b04d).
//! The second checker's named experiment, from the run's own builders (lib = verbatim crate):
//!
//!   A  period-quantization sweep: two-fleet battles (b1 geometry) where both fleets share ONE
//!      exact integer period (the belt `keys` construction, `Body::with_period`) vs a-spread
//!      1e-4 / 1e-3 / 1e-2 (`formation`), plus the quantized knife-edge (fleet B's key one
//!      0.15% off, check1's case). Reports the catching k and how it grows with the horizon:
//!      the point where the union phase sort stops being eternal.
//!   B  the merge-join at the crossing epoch (the missing cross-group tier): b2 interception
//!      scenes re-keyed by predicted longitude at the crossing epoch(s).
//!   C  the honest pair count of the union-sort certificate at k = 8/16/32 (the corrected
//!      "19x" number), on the exact b1 scenes of the parent run.
//!
//! Rank definitions follow the parent run's battle.rs: rank = |position_i - position_j| in a
//! sort by mean longitude at setup (t = 0), except part B's re-keyed sorts, which use the
//! predicted mean longitude at the named epoch. Truth = the crate's conservative-advancement
//! Halley path on all radial pairs (independent of the method's Newton). No window-tier run
//! here: its exactness is the parent record's known side (battle.jsonl, regenerated).

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::pairs::{cone_pairs, radial_pairs};
use emergent_encounters::truth::{truth_pair, TruthStats};
use emergent_encounters::par_chunks;
use std::collections::HashSet;
use std::f64::consts::{PI, TAU};
use std::time::Instant;

const RHO: f64 = 1e-3;
const THREADS: usize = 4;
const KS: [usize; 9] = [1, 2, 4, 8, 16, 32, 64, 128, 256];

fn rayleigh(rng: &mut Rng, sigma: f64, cap: f64) -> f64 {
    let u = rng.f64();
    (sigma * (-2.0 * (1.0 - u).ln()).sqrt()).min(cap)
}

fn wrap(x: f64) -> f64 {
    x.rem_euclid(TAU)
}

fn jitter(rng: &mut Rng, w: f64) -> f64 {
    w * (rng.f64() - rng.f64())
}

/// A fleet in formation (parent run's builder, verbatim): phase packet of width `w` on one
/// orbit family, a uniform in [a0, a0+da] (distinct integer periods when da > 0).
fn formation(
    rng: &mut Rng, n: usize, a0: f64, da: f64, se: f64, e_add: f64,
    pom_c: Option<f64>, lam_c: f64, w: f64,
) -> Vec<Body> {
    (0..n)
        .map(|_| {
            let a = a0 + da * rng.f64();
            let e = rayleigh(rng, se, 0.6) + e_add;
            let pom = match pom_c {
                Some(c) => wrap(c + jitter(rng, 0.3)),
                None => TAU * rng.f64(),
            };
            let lam = wrap(lam_c - 0.5 * w + w * rng.f64());
            Body::new(a, e, pom, lam)
        })
        .collect()
}

/// The belt-`keys` fleet: identical to `formation` except every body is built on ONE exact
/// integer period (`Body::with_period`), so a group shares a single period key and relative
/// mean longitudes are frozen by arithmetic (same period => M_i(t) - M_j(t) constant).
fn formation_q(
    rng: &mut Rng, n: usize, period: u64, se: f64, pom_c: Option<f64>, lam_c: f64, w: f64,
) -> Vec<Body> {
    (0..n)
        .map(|_| {
            let e = rayleigh(rng, se, 0.6);
            let pom = match pom_c {
                Some(c) => wrap(c + jitter(rng, 0.3)),
                None => TAU * rng.f64(),
            };
            let lam = wrap(lam_c - 0.5 * w + w * rng.f64());
            Body::with_period(period, e, pom, lam)
        })
        .collect()
}

/// The interceptor (parent run's builder, verbatim): packet on a = 1.07 transfer orbits,
/// phased so the fleet is at perihelion (crossing A's ring) at `t_meet`.
fn transfer(rng: &mut Rng, n: usize, lam_c: f64, t_meet: f64) -> Vec<Body> {
    const TICKS: f64 = 4_294_967_296.0;
    (0..n)
        .map(|_| {
            let a = 1.07 + 1e-4 * rng.f64();
            let e = 0.0655 + rayleigh(rng, 1e-3, 0.05);
            let pom = wrap(lam_c + jitter(rng, 0.05));
            let period = (TAU * a.powf(1.5) * TICKS).round() as u64;
            let n_mot = TAU * TICKS / period as f64;
            let m0 = wrap(-n_mot * t_meet);
            Body::new(a, e, pom, wrap(pom + m0))
        })
        .collect()
}

struct Scene {
    name: String,
    bodies: Vec<Body>,
    fleets: Vec<u8>,
    t_end: f64,
}

fn mk(name: &str, parts: Vec<(Vec<Body>, u8)>, orbits: f64) -> Scene {
    Scene {
        name: name.into(),
        bodies: parts.iter().flat_map(|(v, _)| v.iter().copied()).collect(),
        fleets: parts.iter().flat_map(|(v, f)| std::iter::repeat(*f).take(v.len())).collect(),
        t_end: orbits * TAU,
    }
}

fn median(v: &mut [usize]) -> usize {
    if v.is_empty() {
        return 0;
    }
    v.sort_unstable();
    v[v.len() / 2]
}

fn pct(v: &mut [usize], p: f64) -> usize {
    if v.is_empty() {
        return 0;
    }
    v.sort_unstable();
    v[((v.len() as f64 - 1.0) * p).round() as usize]
}

/// The independent truth: every radially overlapping pair, dense in time.
fn truth_all(b: &[Body], t_end: f64) -> (Vec<(u32, u32, f64, f64)>, usize, f64) {
    let t0 = Instant::now();
    let radial = radial_pairs(b, RHO);
    let parts = par_chunks(radial.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = TruthStats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &radial[r] {
            tmp.clear();
            truth_pair(&b[i as usize], &b[j as usize], RHO, t_end, &mut tmp, &mut st);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let mut truth = Vec::new();
    for (o, _) in parts {
        truth.extend(o);
    }
    (truth, radial.len(), t0.elapsed().as_secs_f64())
}

/// Positions of bodies in a sort by `key` (deterministic: total_cmp, ties by index).
fn sort_positions(b: &[Body], key: impl Fn(&Body) -> f64) -> Vec<usize> {
    let mut v: Vec<(f64, usize)> = b.iter().enumerate().map(|(k, x)| (key(x), k)).collect();
    v.sort_by(|a, c| a.0.total_cmp(&c.0).then(a.1.cmp(&c.1)));
    let mut pos = vec![0usize; b.len()];
    for (p, (_, k)) in v.iter().enumerate() {
        pos[*k] = p;
    }
    pos
}

fn curve(ranks: &[usize], of: usize) -> String {
    KS.iter()
        .map(|&k| format!("{:.4}", ranks.iter().filter(|&&r| r <= k).count() as f64 / of as f64))
        .collect::<Vec<_>>()
        .join(",")
}

fn pjson(a: &[(&str, String)]) {
    let body: Vec<String> = a.iter().map(|(k, v)| format!("\"{}\":{}", k, v)).collect();
    println!("{{{}}}", body.join(","));
}

// ---------------------------------------------------------------- part A

/// b1 geometry: two interleaved phase packets (width 0.5 at lam_c = 1.0), periapsis
/// directions pi/2 apart, n per fleet. `spread` picks the construction:
///   "q"      both fleets on one exact integer period (belt keys)
///   "k"      A on the a=1 key, B on the a=1.001 key (quantized knife-edge)
///   "1e-4"…  formation() with that a-spread (parent run's b1)
fn scene_a(spread: &str, seed: u64, n: usize, orbits: f64) -> Scene {
    let mut rng = Rng(seed);
    let p1 = Body::new(1.0, 0.0, 0.0, 0.0).period;
    let p2 = Body::new(1.001, 0.0, 0.0, 0.0).period;
    match spread {
        "q" => {
            let a = formation_q(&mut rng, n, p1, 3e-4, Some(0.0), 1.0, 0.5);
            let b = formation_q(&mut rng, n, p1, 3e-4, Some(PI / 2.0), 1.0, 0.5);
            mk(&format!("a-q-H{}", orbits as i64), vec![(a, 0), (b, 1)], orbits)
        }
        "k" => {
            let a = formation_q(&mut rng, n, p1, 3e-4, Some(0.0), 1.0, 0.5);
            let b = formation_q(&mut rng, n, p2, 3e-4, Some(PI / 2.0), 1.0, 0.5);
            mk(&format!("a-k-H{}", orbits as i64), vec![(a, 0), (b, 1)], orbits)
        }
        s => {
            let da: f64 = s.parse().expect("spread must be q, k or a float");
            let a = formation(&mut rng, n, 1.0, da, 3e-4, 0.0, Some(0.0), 1.0, 0.5);
            let b = formation(&mut rng, n, 1.0, da, 3e-4, 0.0, Some(PI / 2.0), 1.0, 0.5);
            mk(&format!("a-{}-H{}", s, orbits as i64), vec![(a, 0), (b, 1)], orbits)
        }
    }
}

fn run_a(sc: Scene, spread: &str) {
    let t_wall = Instant::now();
    let b = &sc.bodies;
    let t_end = sc.t_end;
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;

    let (truth, n_radial, truth_s) = truth_all(b, t_end);

    let cone = cone_pairs(b, RHO);
    let cone_set: HashSet<(u32, u32)> = cone.pairs.iter().copied().collect();
    let outside_cone = truth
        .iter()
        .filter(|e| inside(e.2) && !cone_set.contains(&(e.0.min(e.1), e.0.max(e.1))))
        .count();
    let cone_cross = cone
        .pairs
        .iter()
        .filter(|&&(i, j)| sc.fleets[i as usize] != sc.fleets[j as usize])
        .count();

    // sorts at setup (the parent run's certificate): union and per fleet
    let lam0 = |x: &Body| wrap(x.mean_anomaly(0.0) + x.pom);
    let pos_u = sort_positions(b, lam0);
    let mut pos_fleet = vec![0usize; b.len()];
    for f in 0..2u8 {
        let mut v: Vec<(f64, usize)> = b
            .iter()
            .enumerate()
            .filter(|(k, _)| sc.fleets[*k] == f)
            .map(|(k, x)| (lam0(x), k))
            .collect();
        v.sort_by(|a, c| a.0.total_cmp(&c.0).then(a.1.cmp(&c.1)));
        for (p, (_, k)) in v.iter().enumerate() {
            pos_fleet[*k] = p;
        }
    }

    let mut rank_u_all: Vec<usize> = Vec::new();
    let mut rank_u_cross: Vec<usize> = Vec::new();
    let mut rank_f_within: Vec<usize> = Vec::new();
    let mut enc = 0usize;
    let mut enc_cross = 0usize;
    for e in &truth {
        if !inside(e.2) {
            continue;
        }
        enc += 1;
        let (i, j) = (e.0 as usize, e.1 as usize);
        let ru = pos_u[i].abs_diff(pos_u[j]);
        rank_u_all.push(ru);
        if sc.fleets[i] == sc.fleets[j] {
            rank_f_within.push(pos_fleet[i].abs_diff(pos_fleet[j]));
        } else {
            enc_cross += 1;
            rank_u_cross.push(ru);
        }
    }

    let mut ruc = rank_u_cross.clone();
    let (n_a, n_b) = (
        sc.fleets.iter().filter(|&&f| f == 0).count(),
        sc.fleets.iter().filter(|&&f| f == 1).count(),
    );
    // drift model: relative mean longitude between the fleets' extreme a drifts
    // |dn| ~ 1.5*da per time unit (n = a^-3/2), i.e. TAU*1.5*da per orbit.
    let da_model: f64 = match spread {
        "q" => 0.0,
        "k" => 1e-3,
        s => s.parse().unwrap_or(0.0),
    };
    let drift_rad = TAU * 1.5 * da_model * (t_end / TAU);
    pjson(&[
        ("part", "\"A\"".into()),
        ("scene", format!("\"{}\"", sc.name)),
        ("spread", format!("\"{}\"", spread)),
        ("orbits", format!("{:.0}", t_end / TAU)),
        ("n_a", n_a.to_string()),
        ("n_b", n_b.to_string()),
        ("radial_pairs", n_radial.to_string()),
        ("cone_pairs", cone.pairs.len().to_string()),
        ("cone_cross", cone_cross.to_string()),
        ("truth_enc", enc.to_string()),
        ("truth_cross", enc_cross.to_string()),
        ("outside_cone", outside_cone.to_string()),
        ("kmax_uc", ruc.iter().copied().max().unwrap_or(0).to_string()),
        ("kmed_uc", median(&mut ruc).to_string()),
        ("kp99_uc", pct(&mut ruc, 0.99).to_string()),
        ("caught_uc_k", format!("[{}]", curve(&rank_u_cross, enc_cross.max(1)))),
        ("caught_u_k", format!("[{}]", curve(&rank_u_all, enc.max(1)))),
        ("caught_f_k", format!("[{}]", curve(&rank_f_within, enc.max(1)))),
        ("drift_rad_model", format!("{:.4}", drift_rad)),
        ("truth_s", format!("{:.2}", truth_s)),
        ("wall_s", format!("{:.2}", t_wall.elapsed().as_secs_f64())),
    ]);
}

// ---------------------------------------------------------------- part B

fn run_b(sc: Scene, t_meet: f64) {
    let t_wall = Instant::now();
    let b = &sc.bodies;
    let t_end = sc.t_end;
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;

    let (truth, _n_radial, truth_s) = truth_all(b, t_end);

    let cone = cone_pairs(b, RHO);
    let cone_set: HashSet<(u32, u32)> = cone.pairs.iter().copied().collect();
    let outside_cone = truth
        .iter()
        .filter(|e| inside(e.2) && !cone_set.contains(&(e.0.min(e.1), e.0.max(e.1))))
        .count();

    // cross encounters (the ones no along-orbit sort at setup can catch)
    let cross: Vec<(usize, usize, f64)> = truth
        .iter()
        .filter(|e| inside(e.2) && sc.fleets[e.0 as usize] != sc.fleets[e.1 as usize])
        .map(|e| (e.0 as usize, e.1 as usize, e.2))
        .collect();

    // group B's crossing epochs: every B body is at perihelion at t_meet by construction,
    // so fleet B crosses A's ring at t = t_meet + j*P_B (P_B = fleet-mean period).
    let pb_mean = b
        .iter()
        .zip(&sc.fleets)
        .filter(|(_, &f)| f == 1)
        .map(|(x, _)| x.period as f64)
        .sum::<f64>()
        / b.iter().zip(&sc.fleets).filter(|(_, &f)| f == 1).count() as f64;
    let pb_tu = pb_mean / 4_294_967_296.0; // period in time units
    let mut epochs: Vec<f64> = vec![];
    let mut j = -((t_meet / pb_tu).ceil() as i64);
    loop {
        let t = t_meet + j as f64 * pb_tu;
        if t > t_end - 0.05 {
            break;
        }
        if t > 0.05 {
            epochs.push(t);
        }
        j += 1;
    }

    // sort keys: setup (control), mean longitude at t_meet, true longitude at t_meet,
    // and per-epoch mean longitude (the merge-join at each crossing epoch).
    let lam0 = |x: &Body| wrap(x.mean_anomaly(0.0) + x.pom);
    let key_m = |x: &Body| wrap(lam0(x) + x.n * t_meet);
    let key_t = |x: &Body| {
        let s = x.state_at_mean(x.mean_anomaly(t_meet));
        s[1].atan2(s[0])
    };
    // ordered index lists and exact cross-pair counts within rank k (the merge-join's
    // candidate set; per-epoch counts deduped over epochs)
    let order_of = |key: &dyn Fn(&Body) -> f64| -> Vec<u32> {
        let mut v: Vec<(f64, u32)> = b.iter().enumerate().map(|(k, x)| (key(x), k as u32)).collect();
        v.sort_by(|a, c| a.0.total_cmp(&c.0).then(a.1.cmp(&c.1)));
        v.into_iter().map(|x| x.1).collect()
    };
    let orderm = order_of(&key_m);
    let ordere: Vec<Vec<u32>> = epochs.iter().map(|&e| order_of(&|x| wrap(lam0(x) + x.n * e))).collect();
    let pos0 = sort_positions(b, lam0);
    let posm = sort_positions(b, |x| key_m(x));
    let post = sort_positions(b, key_t);
    let pose: Vec<Vec<usize>> = epochs.iter().map(|&e| sort_positions(b, |x| wrap(lam0(x) + x.n * e))).collect();
    let cross_pairs = |order: &[u32], k: usize, set: &mut HashSet<(u32, u32)>| {
        let n = order.len();
        for p in 0..n {
            for q in p + 1..(p + 1 + k).min(n) {
                let (i, j) = (order[p] as usize, order[q] as usize);
                if sc.fleets[i] != sc.fleets[j] {
                    set.insert((i.min(j) as u32, i.max(j) as u32));
                }
            }
        }
    };
    let count_k = |k: usize| -> (usize, usize) {
        let mut sm: HashSet<(u32, u32)> = HashSet::new();
        cross_pairs(&orderm, k, &mut sm);
        let mut se: HashSet<(u32, u32)> = HashSet::new();
        for ord in &ordere {
            cross_pairs(ord, k, &mut se);
        }
        (sm.len(), se.len())
    };
    let (cp_m32, cp_e32) = count_k(32);
    let (cp_m64, cp_e64) = count_k(64);
    let (cp_m128, cp_e128) = count_k(128);

    let mut r0: Vec<usize> = Vec::new();
    let mut rm: Vec<usize> = Vec::new();
    let mut rt: Vec<usize> = Vec::new();
    let mut re: Vec<usize> = Vec::new();
    let mut d_epoch: Vec<f64> = Vec::new();
    let mut t_orb: Vec<f64> = Vec::new();
    for &(i, j, t) in &cross {
        r0.push(pos0[i].abs_diff(pos0[j]));
        rm.push(posm[i].abs_diff(posm[j]));
        rt.push(post[i].abs_diff(post[j]));
        let (best, bd) = epochs
            .iter()
            .map(|&e| ((t - e).abs(), e))
            .min_by(|a, c| a.0.total_cmp(&c.0))
            .unwrap_or((f64::INFINITY, 0.0));
        d_epoch.push(best);
        t_orb.push(t / TAU);
        let ps = &pose[epochs.iter().position(|&e| e == bd).unwrap_or(0)];
        re.push(ps[i].abs_diff(ps[j]));
    }

    let mut r0s = r0.clone();
    let mut rms = rm.clone();
    let mut rts = rt.clone();
    let mut res = re.clone();
    let des = d_epoch.clone();
    let n = cross.len();
    pjson(&[
        ("part", "\"B\"".into()),
        ("scene", format!("\"{}\"", sc.name)),
        ("n_a", sc.fleets.iter().filter(|&&f| f == 0).count().to_string()),
        ("n_b", sc.fleets.iter().filter(|&&f| f == 1).count().to_string()),
        ("orbits", format!("{:.1}", t_end / TAU)),
        ("truth_cross", n.to_string()),
        ("outside_cone", outside_cone.to_string()),
        ("epochs_orbits", format!("[{}]", epochs.iter().map(|e| format!("{:.3}", e / TAU)).collect::<Vec<_>>().join(","))),
        ("cone_cross", cone.pairs.iter().filter(|&&(i, j)| sc.fleets[i as usize] != sc.fleets[j as usize]).count().to_string()),
        ("cp_km_32_64_128", format!("[{},{},{}]", cp_m32, cp_m64, cp_m128)),
        ("cp_ke_32_64_128", format!("[{},{},{}]", cp_e32, cp_e64, cp_e128)),
        ("d_epoch_max", format!("{:.4}", des.iter().cloned().fold(f64::NEG_INFINITY, f64::max))),
        ("k0_med_max", format!("[{},{}]", median(&mut r0s), r0s.iter().copied().max().unwrap_or(0))),
        ("k0_curve", format!("[{}]", curve(&r0, n.max(1)))),
        ("km_med_max", format!("[{},{}]", median(&mut rms), rms.iter().copied().max().unwrap_or(0))),
        ("km_curve", format!("[{}]", curve(&rm, n.max(1)))),
        ("kt_med_max", format!("[{},{}]", median(&mut rts), rts.iter().copied().max().unwrap_or(0))),
        ("kt_curve", format!("[{}]", curve(&rt, n.max(1)))),
        ("ke_med_max", format!("[{},{}]", median(&mut res), res.iter().copied().max().unwrap_or(0))),
        ("ke_curve", format!("[{}]", curve(&re, n.max(1)))),
        ("truth_s", format!("{:.2}", truth_s)),
        ("wall_s", format!("{:.2}", t_wall.elapsed().as_secs_f64())),
    ]);
}

fn median_f(v: &mut Vec<f64>) -> f64 {
    if v.is_empty() {
        return 0.0;
    }
    v.sort_by(|a, b| a.total_cmp(b));
    v[v.len() / 2]
}

// ---------------------------------------------------------------- part C

/// Unique pairs within linear rank k of the setup union sort, for the parent run's exact
/// b1 scenes (same builders, same seeds): the certificate's candidate-set size.
fn run_c(name: &str, bodies: Vec<Body>) {
    let lam0 = |x: &Body| wrap(x.mean_anomaly(0.0) + x.pom);
    let mut v: Vec<(f64, u32)> = bodies.iter().enumerate().map(|(k, x)| (lam0(x), k as u32)).collect();
    v.sort_by(|a, c| a.0.total_cmp(&c.0).then(a.1.cmp(&c.1)));
    let n = v.len();
    let mut counts = Vec::new();
    for &k in &[8usize, 16, 32] {
        let mut c = 0usize;
        for p in 0..n {
            c += k.min(n - 1 - p);
        }
        counts.push(c);
    }
    pjson(&[
        ("part", "\"C\"".into()),
        ("scene", format!("\"{}\"", name)),
        ("n_total", n.to_string()),
        ("pairs_k8", counts[0].to_string()),
        ("pairs_k16", counts[1].to_string()),
        ("pairs_k32", counts[2].to_string()),
    ]);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let which = args.get(1).map(|s| s.as_str()).unwrap_or("all");
    let sub = args.get(2).map(|s| s.as_str());
    let s0 = 20261014u64;
    let load = std::fs::read_to_string("/proc/loadavg").unwrap_or_default().trim().to_string();
    let mem = std::fs::read_to_string("/proc/meminfo")
        .ok()
        .and_then(|s| s.lines().find(|l| l.starts_with("MemAvailable")).map(|l| l.split_whitespace().nth(1).unwrap_or("?").to_string()))
        .unwrap_or_else(|| "?".into());
    println!("# machine: {} {}; load: {}; mem avail: {} kB", std::env::var("HOSTNAME").unwrap_or_default(), "8 vCPU", load, mem);
    println!("# utc: {}", humantime());

    if which == "all" || which == "a" {
        let spreads: Vec<&str> = match sub {
            Some(s) => vec![s],
            None => vec!["q", "k", "1e-4", "1e-3", "1e-2"],
        };
        for sp in spreads {
            let horizons: &[f64] = if sp == "k" { &[20.0, 80.0] } else { &[5.0, 20.0, 80.0, 320.0] };
            // one fleet pair per spread; identical bodies at every horizon (only t_end varies).
            // The 1e-4 spread is EXACTLY the parent run's b1-cross-150 (its seed): the control.
            let seed: u64 = match sp {
                "1e-4" => 20261011 + 12,
                "q" => s0 + 1,
                "k" => s0 + 2,
                "1e-3" => s0 + 3,
                _ => s0 + 4,
            };
            for &h in horizons {
                run_a(scene_a(sp, seed, 150, h), sp);
            }
        }
    }
    if which == "all" || which == "b" {
        for (n, seed) in [(75usize, 20261011 + 21), (150, 20261011 + 22), (300, 20261011 + 23)] {
            let mut rng = Rng(seed);
            let a = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, 0.5);
            let b = transfer(&mut rng, n, 1.0, 2.0 * TAU);
            run_b(mk(&format!("b2-intercept-{}", n), vec![(a, 0), (b, 1)], 6.0), 2.0 * TAU);
        }
    }
    if which == "all" || which == "c" {
        for (n, seed) in [(75usize, 20261011 + 11), (150, 20261011 + 12), (300, 20261011 + 13)] {
            let mut rng = Rng(seed);
            let a = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, Some(0.0), 1.0, 0.5);
            let b = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, Some(PI / 2.0), 1.0, 0.5);
            run_c(&format!("b1-cross-{}", n), a.iter().chain(b.iter()).copied().collect());
        }
    }
}

fn humantime() -> String {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| {
            let t = d.as_secs() as i64;
            // days since epoch -> UTC date (civil from days, Howard Hinnant's algorithm)
            let days = t.div_euclid(86400);
            let secs = t.rem_euclid(86400);
            let z = days + 719468;
            let era = z.div_euclid(146097);
            let doe = z.rem_euclid(146097);
            let yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
            let y = yoe + era * 400;
            let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
            let mp = (5 * doy + 2) / 153;
            let d = doy - (153 * mp + 2) / 5 + 1;
            let m = if mp < 10 { mp + 3 } else { mp - 9 };
            let y = if m <= 2 { y + 1 } else { y };
            format!("{:04}-{:02}-{:02}T{:02}:{:02}:{:02}Z", y, m, d, secs / 3600, (secs % 3600) / 60, secs % 60)
        })
        .unwrap_or_default()
}
