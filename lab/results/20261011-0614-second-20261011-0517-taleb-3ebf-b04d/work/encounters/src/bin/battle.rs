//! The battle probe (lab run 20261011-0517-taleb-3ebf). Question: does the phase-neighbour
//! certificate's premise — "every real encounter lies within partner rank k along the orbit"
//! (gold 20261006-0346-taleb-09b5, one formation on one orbit) — survive the game's extreme
//! event, two fleets meeting?
//!
//! Scenes (rho = 1e-3):
//!   f1    one fleet in formation (the gold's regime; control)
//!   ring  a dense ring on one orbit family (the gate's other scene; control)
//!   b1    two equal-period formations on crossing orbits, co-located (a standing battle)
//!   b2    an interception: fleet B drops from a = 1.07 and crosses A's packet at perihelion
//!
//! Per scene: the independent truth (radial pairs, conservative advancement), the window tier
//! (the Diophantine method) on the Binet-cone candidates, and for every truth encounter the
//! partner's rank in (a) each fleet's own phase sort and (b) the union phase sort.

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{cone_pairs, radial_pairs, sections};
use emergent_encounters::truth::{truth_pair, TruthStats};
use emergent_encounters::par_chunks;
use std::f64::consts::{PI, TAU};
use std::time::Instant;

const SAFETY: f64 = 1.1;
const THREADS: usize = 4;
const RHO: f64 = 1e-3;
const TOL: f64 = 1e-3;

type Enc = (u32, u32, f64, f64);

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

/// A fleet in formation: a phase packet of width `w` (mean longitudes) on one orbit family.
/// `pom_c = None`: periapsis directions uniform (a circular-ish patrol); `Some(c)`: clustered.
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

/// The interceptor: a packet on a transfer orbit (a = 1.07, e ~ 0.0655) whose perihelion is at
/// longitude `lam_c`, phased so the fleet is at perihelion (crossing A's orbit) at `t_meet`.
fn transfer(rng: &mut Rng, n: usize, lam_c: f64, t_meet: f64) -> Vec<Body> {
    (0..n)
        .map(|_| {
            let a = 1.07 + 1e-4 * rng.f64();
            let e = 0.0655 + rayleigh(rng, 1e-3, 0.05);
            let pom = wrap(lam_c + jitter(rng, 0.05));
            let period = (TAU * a.powf(1.5) * TICKS).round() as u64; // as Body::new rounds
            let n_mot = TAU * TICKS / period as f64; // rad per time unit, as with_period derives
            let m0 = wrap(-n_mot * t_meet);
            Body::new(a, e, pom, wrap(pom + m0))
        })
        .collect()
}

struct SceneSpec {
    name: String,
    bodies: Vec<Body>,
    fleets: Vec<u8>,
    t_end: f64,
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

fn run(sc: SceneSpec) {
    let t_wall = Instant::now();
    let b = &sc.bodies;
    let t_end = sc.t_end;
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;

    // ---- truth: every radially overlapping pair, dense in time ----
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
    let mut tst = TruthStats::default();
    for (o, s) in parts {
        truth.extend(o);
        tst.add(&s);
    }
    let truth_s = t0.elapsed().as_secs_f64();

    // ---- candidates: the Binet cone ----
    let cone = cone_pairs(b, RHO);
    let cone_set: std::collections::HashSet<(u32, u32)> = cone.pairs.iter().copied().collect();
    let outside_cone = truth
        .iter()
        .filter(|e| inside(e.2) && !cone_set.contains(&(e.0.min(e.1), e.0.max(e.1))))
        .count();
    let (cone_cross, cone_within) = cone
        .pairs
        .iter()
        .partition::<Vec<_>, _>(|&&(i, j)| sc.fleets[i as usize] != sc.fleets[j as usize]);

    // ---- setup cost of the window tier, by pair class ----
    let t0 = Instant::now();
    let setup = |pairs: &[(u32, u32)]| -> (u64, [u64; 3], u64) {
        let parts = par_chunks(pairs.len(), 256, THREADS, |r| {
            let mut evals = 0u64;
            let mut kinds = [0u64; 3];
            let mut secs = 0u64;
            for &(i, j) in &pairs[r] {
                for s in sections(&b[i as usize], &b[j as usize], RHO, SAFETY, &mut evals) {
                    kinds[s.kind as usize] += 1;
                    secs += 1;
                }
            }
            (evals, kinds, secs)
        });
        let mut evals = 0u64;
        let mut kinds = [0u64; 3];
        let mut secs = 0u64;
        for (e, k, s) in parts {
            evals += e;
            for t in 0..3 {
                kinds[t] += k[t];
            }
            secs += s;
        }
        (evals, kinds, secs)
    };
    let (ev_w, kinds_w, secs_w) = setup(&cone_within);
    let (ev_x, kinds_x, secs_x) = setup(&cone_cross);
    let setup_s = t0.elapsed().as_secs_f64();

    // ---- the window tier (method) on all cone candidates ----
    let t0 = Instant::now();
    let parts = par_chunks(cone.pairs.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &cone.pairs[r] {
            tmp.clear();
            pair_events(&b[i as usize], &b[j as usize], RHO, SAFETY, 0.0, t_end, &mut st, &mut tmp);
            out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, st)
    });
    let mut meth = Vec::new();
    let mut mst = Stats::default();
    for (o, s) in parts {
        meth.extend(o);
        mst.add(&s);
    }
    let meth_s = t0.elapsed().as_secs_f64();

    // ---- matchup: what the window tier misses ----
    let mut by_pair: std::collections::HashMap<(u32, u32), Vec<f64>> = std::collections::HashMap::new();
    for e in &meth {
        by_pair.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut enc_total = 0usize;
    let mut enc_cross = 0usize;
    let mut miss_w = 0usize;
    let mut miss_x = 0usize;
    let mut rank_within: Vec<usize> = Vec::new();
    let mut rank_union_all: Vec<usize> = Vec::new();
    let mut rank_union_cross: Vec<usize> = Vec::new();

    // phase sorts: per fleet, and the union
    let lam0 = |x: &Body| wrap(x.mean_anomaly(0.0) + x.pom);
    let nfleets = (*sc.fleets.iter().max().unwrap() + 1) as usize;
    let mut pos_fleet = vec![0usize; b.len()];
    for f in 0..nfleets {
        let mut v: Vec<(f64, usize)> = b
            .iter()
            .enumerate()
            .filter(|(k, _)| sc.fleets[*k] as usize == f)
            .map(|(k, x)| (lam0(x), k))
            .collect();
        v.sort_by(|a, c| a.0.total_cmp(&c.0));
        for (p, (_, k)) in v.iter().enumerate() {
            pos_fleet[*k] = p;
        }
    }
    let mut u: Vec<(f64, usize)> = b.iter().enumerate().map(|(k, x)| (lam0(x), k)).collect();
    u.sort_by(|a, c| a.0.total_cmp(&c.0));
    let mut pos_u = vec![0usize; b.len()];
    for (p, (_, k)) in u.iter().enumerate() {
        pos_u[*k] = p;
    }

    for e in &truth {
        if !inside(e.2) {
            continue;
        }
        enc_total += 1;
        let (i, j) = (e.0 as usize, e.1 as usize);
        let ru = pos_u[i].abs_diff(pos_u[j]);
        rank_union_all.push(ru);
        let seen = by_pair
            .get(&(e.0, e.1))
            .is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < TOL));
        if sc.fleets[i] == sc.fleets[j] {
            rank_within.push(pos_fleet[i].abs_diff(pos_fleet[j]));
            if !seen {
                miss_w += 1;
            }
        } else {
            enc_cross += 1;
            rank_union_cross.push(ru);
            if !seen {
                miss_x += 1;
            }
        }
    }

    let ks: [usize; 9] = [1, 2, 4, 8, 16, 32, 64, 128, 256];
    let caught_fleet: Vec<String> = ks
        .iter()
        .map(|&k| {
            format!(
                "{:.4}",
                rank_within.iter().filter(|&&r| r <= k).count() as f64 / enc_total as f64
            )
        })
        .collect();
    let caught_union: Vec<String> = ks
        .iter()
        .map(|&k| {
            format!(
                "{:.4}",
                rank_union_all.iter().filter(|&&r| r <= k).count() as f64 / enc_total as f64
            )
        })
        .collect();

    let mut rw = rank_within.clone();
    let mut ruc = rank_union_cross.clone();
    let (n_a, n_b) = (sc.fleets.iter().filter(|&&f| f == 0).count(), sc.fleets.iter().filter(|&&f| f == 1).count());
    let x_enc = enc_cross as f64;
    let println_json = |a: &[(&str, String)]| {
        let body: Vec<String> = a.iter().map(|(k, v)| format!("\"{}\":{}", k, v)).collect();
        println!("{{{}}}", body.join(","));
    };
    println_json(&[
        ("scene", format!("\"{}\"", sc.name)),
        ("n_a", n_a.to_string()),
        ("n_b", n_b.to_string()),
        ("orbits", format!("{:.1}", t_end / TAU)),
        ("radial_pairs", radial.len().to_string()),
        ("cone_pairs", cone.pairs.len().to_string()),
        ("cone_scanned", cone.scanned.to_string()),
        ("cone_cross", cone_cross.len().to_string()),
        ("cone_within", cone_within.len().to_string()),
        ("truth_enc", enc_total.to_string()),
        ("truth_cross", enc_cross.to_string()),
        ("outside_cone", outside_cone.to_string()),
        ("miss_window_within", miss_w.to_string()),
        ("miss_window_cross", miss_x.to_string()),
        ("kmax_within", rw.iter().copied().max().unwrap_or(0).to_string()),
        ("kmed_within", median(&mut rw).to_string()),
        ("kmax_union_cross", ruc.iter().copied().max().unwrap_or(0).to_string()),
        ("kmed_union_cross", median(&mut ruc).to_string()),
        ("kp99_union_cross", pct(&mut ruc, 0.99).to_string()),
        ("caught_fleet_k", format!("[{}]", caught_fleet.join(","))),
        ("caught_union_k", format!("[{}]", caught_union.join(","))),
        ("setup_evals_within", ev_w.to_string()),
        ("setup_evals_cross", ev_x.to_string()),
        ("setup_secs_within", secs_w.to_string()),
        ("setup_secs_cross", secs_x.to_string()),
        ("setup_kinds_within", format!("[{},{},{}]", kinds_w[0], kinds_w[1], kinds_w[2])),
        ("setup_kinds_cross", format!("[{},{},{}]", kinds_x[0], kinds_x[1], kinds_x[2])),
        ("setup_evals_per_cross_enc", format!("{:.1}", if x_enc > 0.0 { ev_x as f64 / x_enc } else { 0.0 })),
        ("method_evals", mst.evals.to_string()),
        ("method_checks", mst.checks_total().to_string()),
        ("truth_s", format!("{:.2}", truth_s)),
        ("setup_s", format!("{:.2}", setup_s)),
        ("meth_s", format!("{:.2}", meth_s)),
        ("wall_s", format!("{:.2}", t_wall.elapsed().as_secs_f64())),
    ]);
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let which = args.get(1).map(|s| s.as_str()).unwrap_or("all");
    let s0 = 20261011u64;
    let mut scenes: Vec<SceneSpec> = vec![];
    let mk = |name: String, parts: Vec<(Vec<Body>, u8)>, orbits: f64| SceneSpec {
        name,
        bodies: parts.iter().flat_map(|(v, _)| v.iter().copied()).collect(),
        fleets: parts.iter().flat_map(|(v, f)| std::iter::repeat(*f).take(v.len())).collect(),
        t_end: orbits * TAU,
    };
    if which == "all" || which == "control" {
        let mut rng = Rng(s0 + 1);
        let a = formation(&mut rng, 300, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, 0.5);
        scenes.push(mk("f1-formation".into(), vec![(a, 0)], 20.0));
        let mut rng = Rng(s0 + 2);
        let a = formation(&mut rng, 600, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, TAU);
        scenes.push(mk("ring-dense".into(), vec![(a, 0)], 20.0));
    }
    if which == "all" || which == "b1" {
        for (n, seed) in [(75usize, s0 + 11), (150, s0 + 12), (300, s0 + 13)] {
            let mut rng = Rng(seed);
            let a = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, Some(0.0), 1.0, 0.5);
            let b = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, Some(PI / 2.0), 1.0, 0.5);
            scenes.push(mk(format!("b1-cross-{}", n), vec![(a, 0), (b, 1)], 20.0));
        }
    }
    if which == "all" || which == "b2" {
        for (n, seed) in [(75usize, s0 + 21), (150, s0 + 22), (300, s0 + 23)] {
            let mut rng = Rng(seed);
            let a = formation(&mut rng, n, 1.0, 1e-4, 3e-4, 0.0, None, 1.0, 0.5);
            let b = transfer(&mut rng, n, 1.0, 2.0 * TAU);
            scenes.push(mk(format!("b2-intercept-{}", n), vec![(a, 0), (b, 1)], 6.0));
        }
    }
    for sc in scenes {
        run(sc);
    }
}
