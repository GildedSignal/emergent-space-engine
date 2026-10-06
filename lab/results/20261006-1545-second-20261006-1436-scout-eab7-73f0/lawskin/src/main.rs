//! Second author on 20261006-1436-scout-eab7: the checker's named gold experiment.
//!
//! Same two arms (baseline: recompute `sections()` for every candidate pair every kick epoch;
//! skin: cached sections + ~20-flop element-space validity + re-setup on drift + widened
//! windows), but driven by **the law's own kick stream** at the plane's cadence
//! (H0190: ~32 kicks per orbit), instead of the scout run's random walk:
//!
//! For a planar belt of test bodies around a dominant mass with a circular, coplanar external
//! perturber (μ_p at a_p) and the central field's 1PN precession, the double-averaged (secular)
//! disturbing function is *axisymmetric*: da = de = 0 exactly, and each body's apsidal line
//! precesses at a rate fixed by its own (a, e). So the law's orbit-averaged kick stream in this
//! scene is **pure differential precession** — the systematic Binet-space shear the scout run's
//! random walk understated (its dossier said so), and the term q-skin named as the killer of
//! wide slack (window width under tangential-pair drift).
//!
//!   ϖ̇_GR   = 3 n rg / (a (1−e²))                        (compiled geodesic precession, 1PN)
//!   ϖ̇_tide = −√(1−e²)/(n a²) · (∂⟨R⟩/∂e)/e              (Lagrange planetary equation)
//!   ⟨R⟩    = (1/4π²) ∫∫ μ_p [1/|r−r_p| − (r·r_p)/a_p³] dM dλ_p
//!            double-averaged on a fixed product grid (deterministic; no RNG), r from Kepler.
//!
//! Arms share the belt, the kick stream (a pure function of (a,e) — bit-identical trivially),
//! the candidate set and the exact per-pair checks; only the setup policy differs. The kick
//! keeps mean anomaly at epoch start (position-continuous in the scout run's sense): a, e,
//! period, tp never change; only pom rotates. Floats explore here (research).
//!
//! Extras over the scout run, per the checker: 32 kicks/orbit cadence; belt / tangential /
//! co-orbital scenes; misses and extras by TRUE multiset difference (not length subtraction);
//! mean cache lifetime in epochs (the mechanism property the horizon ratio hid).

use emergent_encounters::belt::{make_belt, Spec};
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{run_section, Stats};
use emergent_encounters::pairs::{cone_pairs, eps_u, sections, Section};
use std::collections::HashMap;
use std::time::Instant;

const SAFETY: f64 = 3.0;
const TAU: f64 = std::f64::consts::TAU;
/// The plane's cadence (H0190): 32 kicks per orbit of a = 1, one shared global grid.
const KICKS_PER_ORBIT: f64 = 32.0;
const EPOCH: f64 = TAU / KICKS_PER_ORBIT;

#[derive(Clone, Copy, PartialEq)]
enum Arm {
    Baseline,
    Skin,
}

#[derive(Clone, Copy, PartialEq)]
enum Scene {
    Belt,    // the scout run's training belt: a ∈ [0.9, 1.1], σ_e given
    Tang,    // near-circular: tangential-pair stress (q-skin's named killer geometry)
    Coorb,   // a ∈ [0.999, 1.001]: nearly identical orbits, Full sections
}

impl Scene {
    fn band(self) -> (f64, f64) {
        match self {
            Scene::Belt => (0.9, 1.1),
            Scene::Tang => (0.9, 1.1),
            Scene::Coorb => (0.999, 1.001),
        }
    }
    fn name(self) -> &'static str {
        match self {
            Scene::Belt => "belt",
            Scene::Tang => "tang",
            Scene::Coorb => "coorb",
        }
    }
}

struct Totals {
    setups: u64,
    setup_evals: u64,
    run_evals: u64,
    checks: u64,
    queries: u64,
    hits: u64,
    valid_checks: u64,
    cache_hits: u64,
    wall_ms: u128,
    per_epoch_setups: Vec<u64>,
    ncand: usize,
}

struct Cfg {
    arm: Arm,
    scene: Scene,
    n: usize,
    sigma_e: f64,
    rho: f64,
    rg: f64,
    mup: f64,
    ap: f64,
    epochs: usize,
    seed: u64,
    slack: f64,
    widen: f64,
}

/// One evaluation of the disturbing function at particle state (M) and perturber phase (lam).
#[inline]
fn r_perturb(a: f64, e: f64, m: f64, lam: f64, ap: f64) -> f64 {
    // Kepler position from mean anomaly (pericentre at longitude 0; axisymmetry makes pom moot).
    let mut ea = m;
    for _ in 0..8 {
        ea -= (ea - e * ea.sin() - m) / (1.0 - e * ea.cos());
    }
    let x = a * (ea.cos() - e);
    let y = a * (1.0 - e * e).sqrt() * ea.sin();
    let dx = x - ap * lam.cos();
    let dy = y - ap * lam.sin();
    let rr = ap * ap;
    1.0 / dx.hypot(dy) - (x * lam.cos() + y * lam.sin()) / rr
}

/// ⟨R⟩: the double-averaged disturbing function, on a fixed deterministic product grid.
fn avg_r(a: f64, e: f64, mup: f64, ap: f64, nm: usize, nl: usize) -> f64 {
    let mut s = 0.0;
    for im in 0..nm {
        let m = TAU * (im as f64 + 0.5) / nm as f64;
        for il in 0..nl {
            let lam = TAU * (il as f64 + 0.5) / nl as f64;
            s += r_perturb(a, e, m, lam, ap);
        }
    }
    mup * s / (nm * nl) as f64
}

/// ϖ̇ [rad per time unit] for one body: compiled GR precession + orbit-averaged tide.
/// `gr` is the 1PN term; `tide` from the Lagrange equation with the numeric ∂⟨R⟩/∂e.
fn pomdot(b: &Body, rg: f64, mup: f64, ap: f64) -> (f64, f64, f64) {
    let n = b.n; // rad per time unit (a = 1 → n = 1; period = TAU/n time units)
    let sq = (1.0 - b.e * b.e).sqrt();
    let gr = 3.0 * n * rg / (b.a * (1.0 - b.e * b.e));
    // ∂⟨R⟩/∂e / e : even in e, so the small-e limit is 2c2 (finite); δ chosen ≪ typical drift.
    let d_over_e;
    if b.e > 2e-3 {
        let d = 1e-4;
        d_over_e = (avg_r(b.a, b.e + d, mup, ap, 64, 24) - avg_r(b.a, b.e - d, mup, ap, 64, 24)) / (2.0 * d * b.e);
    } else {
        let d = 2e-4;
        let c2 = (avg_r(b.a, d, mup, ap, 64, 24) - avg_r(b.a, 0.0, mup, ap, 64, 24)) / (d * d);
        d_over_e = 2.0 * c2;
    }
    // Prograde, as the secular theory demands for an interior particle under an exterior
    // perturber; the magnitude (what sets churn) is validated against the quadrupole above.
    let tide = sq / (n * b.a * b.a) * d_over_e;
    (gr + tide, gr, tide)
}

/// Cached pair validity (the scout run's, unchanged): both bodies' Binet points within
/// slack·eps_u of the setup snapshot, and (period drift + mirrored periapsis drift) within half
/// the widening. Under the law's stream a, e, period, tp are invariant, so the time term is
/// always 0 here and the geometric term is the whole gate.
fn valid(bi: &Body, bj: &Body, si: &Body, sj: &Body, rho: f64, slack: f64, time_slack_ticks: f64) -> bool {
    let eps = eps_u(bi, bj, rho);
    let geom = |a: &Body, s: &Body| {
        let x = a.binet();
        let y = s.binet();
        (x[0] - y[0]).abs().max((x[1] - y[1]).abs()).max((x[2] - y[2]).abs())
    };
    if geom(bi, si) > slack * eps || geom(bj, sj) > slack * eps {
        return false;
    }
    let tdrift = |a: &Body, s: &Body| {
        let p = a.period as f64;
        let d = (a.tp as i128 - s.tp as i128).rem_euclid(a.period as i128) as f64;
        d.min(p - d) + (p - s.period as f64).abs()
    };
    tdrift(bi, si) <= time_slack_ticks && tdrift(bj, sj) <= time_slack_ticks
}

/// Widen a section's window (w1/w2 ticks) and its check arcs (di/dj time units) by the skin.
fn widen_sec(sec: &mut Section, w_ticks: i64, w_time: f64) {
    sec.w1 += w_ticks;
    sec.w2 += w_ticks;
    sec.di = (sec.di.0 - w_time, sec.di.1 + w_time);
    sec.dj = (sec.dj.0 - w_time, sec.dj.1 + w_time);
}

/// Drive one arm over `epochs` kick epochs (TAU/32 each). Returns the found encounter set.
fn drive(cfg: &Cfg) -> (Vec<(u32, u32, f64)>, Totals) {
    let (a_lo, a_hi) = cfg.scene.band();
    let spec = Spec {
        name: cfg.scene.name().into(),
        n: cfg.n,
        sigma_e: cfg.sigma_e,
        rho: cfg.rho,
        a_lo,
        a_hi,
        keys: 0,
        seed: cfg.seed,
        orbits: 1.0,
    };
    let mut bodies = make_belt(&spec);
    // The law's stream, compiled once per body: a pure function of (a, e), identical in both arms.
    let pomdots: Vec<f64> = bodies.iter().map(|b| pomdot(b, cfg.rg, cfg.mup, cfg.ap).0).collect();
    let cands = cone_pairs(&bodies, cfg.rho).pairs;
    let ncand = cands.len();
    let mut cache: HashMap<(u32, u32), (Vec<Section>, Body, Body)> = HashMap::new();
    let w_ticks = (cfg.widen * cfg.rho * TICKS) as i64;
    let w_time = cfg.widen * cfg.rho;
    let time_slack = 0.5 * cfg.widen * cfg.rho * TICKS;
    let mut t = Totals {
        setups: 0,
        setup_evals: 0,
        run_evals: 0,
        checks: 0,
        queries: 0,
        hits: 0,
        valid_checks: 0,
        cache_hits: 0,
        wall_ms: 0,
        per_epoch_setups: Vec::new(),
        ncand,
    };
    let mut found: Vec<(u32, u32, f64)> = Vec::new();
    let t_start = Instant::now();
    for epoch in 0..cfg.epochs {
        let t0 = epoch as f64 * EPOCH;
        let t1 = t0 + EPOCH;
        if epoch > 0 {
            // One kick: every body's apsidal line advances by its own compiled ϖ̇·dt.
            for (b, g) in bodies.iter_mut().zip(&pomdots) {
                b.pom = (b.pom + g * EPOCH).rem_euclid(TAU);
                b.cp = b.pom.cos();
                b.sp = b.pom.sin();
            }
        }
        let mut ep_setups = 0u64;
        for &(i, j) in &cands {
            let (bi, bj) = (&bodies[i as usize], &bodies[j as usize]);
            let secs: Vec<Section>;
            match cfg.arm {
                Arm::Baseline => {
                    let mut ev = 0u64;
                    secs = sections(bi, bj, cfg.rho, SAFETY, &mut ev);
                    t.setups += 1;
                    t.setup_evals += ev;
                    ep_setups += 1;
                }
                Arm::Skin => {
                    if let Some((cached, si, sj)) = cache.get(&(i, j)) {
                        t.valid_checks += 1;
                        if valid(bi, bj, si, sj, cfg.rho, cfg.slack, time_slack) {
                            secs = cached.clone();
                            t.cache_hits += 1;
                        } else {
                            let mut ev = 0u64;
                            let mut fresh = sections(bi, bj, cfg.rho, SAFETY, &mut ev);
                            for s in fresh.iter_mut() {
                                widen_sec(s, w_ticks, w_time);
                            }
                            cache.insert((i, j), (fresh.clone(), *bi, *bj));
                            t.setups += 1;
                            t.setup_evals += ev;
                            ep_setups += 1;
                            secs = fresh;
                        }
                    } else {
                        let mut ev = 0u64;
                        let mut fresh = sections(bi, bj, cfg.rho, SAFETY, &mut ev);
                        for s in fresh.iter_mut() {
                            widen_sec(s, w_ticks, w_time);
                        }
                        cache.insert((i, j), (fresh.clone(), *bi, *bj));
                        t.setups += 1;
                        t.setup_evals += ev;
                        ep_setups += 1;
                        secs = fresh;
                    }
                }
            }
            let mut st = Stats::default();
            let mut out = Vec::new();
            for sec in &secs {
                run_section(bi, bj, sec, cfg.rho, t0, t1, &mut st, &mut out);
            }
            t.run_evals += st.evals;
            t.checks += st.checks_total();
            t.queries += st.queries;
            t.hits += st.hits_total();
            for (ts, _d) in out {
                found.push((i, j, ts));
            }
        }
        t.per_epoch_setups.push(ep_setups);
    }
    t.wall_ms = t_start.elapsed().as_millis();
    (found, t)
}

/// TRUE multiset difference (the scout run's `extras` was a length difference): each event of
/// `truth` matched to a distinct event of `a` with the same pair and |Δt| < 1e-6.
/// Returns (truth events missing from a, a events not in truth).
fn compare(a: &[(u32, u32, f64)], truth: &[(u32, u32, f64)]) -> (Vec<(u32, u32, f64)>, Vec<(u32, u32, f64)>) {
    let mut used = vec![false; a.len()];
    let mut misses = Vec::new();
    for &(i, j, ts) in truth {
        let mut ok = false;
        for (k, &(pi, pj, pt)) in a.iter().enumerate() {
            if !used[k] && pi == i && pj == j && (pt - ts).abs() < 1e-6 {
                used[k] = true;
                ok = true;
                break;
            }
        }
        if !ok {
            misses.push((i, j, ts));
        }
    }
    let extras = a
        .iter()
        .enumerate()
        .filter(|(k, _)| !used[*k])
        .map(|(_, &(i, j, ts))| (i, j, ts))
        .collect();
    (misses, extras)
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    if a.len() > 1 && a[1] == "validate" {
        // ϖ̇_tide vs the analytic quadrupole (3/4) n μ_p α³ √(1−e²): settles the e-power.
        let (mup, ap) = (1e-3, 5.2);
        for e in [0.001f64, 0.01, 0.05, 0.1, 0.2] {
            let b = Body::new(1.0, e, 0.0, 0.0);
            let (_, gr, tide) = pomdot(&b, 1e-3, mup, ap);
            let per = TAU / b.n; // one orbit of this body, in time units
            let quad = 0.75 * b.n * mup * (1.0 / ap).powi(3);
            println!(
                "e={:5.3} tide/orbit={:10.3e} quad(3/4 nmupa3)={:10.3e} ratio={:7.4} quad*sq={:10.3e} ratio_sq={:7.4} quad/sq={:10.3e} ratio_isq={:7.4} gr/orbit={:10.3e}",
                e,
                tide * per,
                quad * per,
                tide / quad,
                quad * (1.0 - e * e).sqrt() * per,
                tide / (quad * (1.0 - e * e).sqrt()),
                quad / (1.0 - e * e).sqrt() * per,
                tide / (quad / (1.0 - e * e).sqrt()),
                gr * per
            );
        }
        return;
    }
    if a.len() > 1 && a[1] == "diag" {
        // args: diag scene n sigma_e rho rg seed mup ap i j t  — the pair's geometry at time t
        let scene = match a[2].as_str() {
            "belt" => Scene::Belt,
            "tang" => Scene::Tang,
            "coorb" => Scene::Coorb,
            _ => panic!("scene"),
        };
        let (n, se, rho, rg, seed, mup, ap): (usize, f64, f64, f64, u64, f64, f64) = (
            a[3].parse().unwrap(), a[4].parse().unwrap(), a[5].parse().unwrap(),
            a[6].parse().unwrap(), a[7].parse().unwrap(), a[8].parse().unwrap(), a[9].parse().unwrap(),
        );
        let (i, j, t): (usize, usize, f64) = (a[10].parse().unwrap(), a[11].parse().unwrap(), a[12].parse().unwrap());
        let (a_lo, a_hi) = scene.band();
        let mut bodies = make_belt(&Spec {
            name: "d".into(), n, sigma_e: se, rho, a_lo, a_hi, keys: 0, seed, orbits: 1.0,
        });
        for b in bodies.iter_mut() {
            let g = pomdot(b, rg, mup, ap).0;
            b.pom = (b.pom + g * t).rem_euclid(TAU);
            b.cp = b.pom.cos();
            b.sp = b.pom.sin();
        }
        let (bi, bj) = (&bodies[i], &bodies[j]);
        let (x, y) = (bi.binet(), bj.binet());
        let du = (x[0] - y[0]).abs();
        let r = (x[1] - y[1]).hypot(x[2] - y[2]);
        let eps = eps_u(bi, bj, rho);
        println!(
            "t={} pair=({},{}) ai={} aj={} ei={} ej={} pomdiff={} du={} R={} tangency(|du-R|/eps)={} eps_u={} cone_gap/eps={}",
            t, i, j, bi.a, bj.a, bi.e, bj.e, (bi.pom - bj.pom).abs(),
            du, r, (du - r).abs() / eps, eps, ((du - r) / eps),
        );
        return;
    }
    // args: arm scene n sigma_e rho rg epochs seed slack widen [mup ap]
    let cfg = Cfg {
        arm: match a[1].as_str() {
            "baseline" => Arm::Baseline,
            "skin" => Arm::Skin,
            _ => panic!("arm must be baseline|skin"),
        },
        scene: match a[2].as_str() {
            "belt" => Scene::Belt,
            "tang" => Scene::Tang,
            "coorb" => Scene::Coorb,
            _ => panic!("scene must be belt|tang|coorb"),
        },
        n: a[3].parse().unwrap(),
        sigma_e: a[4].parse().unwrap(),
        rho: a[5].parse().unwrap(),
        rg: a[6].parse().unwrap(),
        epochs: a[7].parse().unwrap(),
        seed: a[8].parse().unwrap(),
        slack: a[9].parse().unwrap(),
        widen: a[10].parse().unwrap(),
        mup: a.get(11).map(|s| s.parse().unwrap()).unwrap_or(1e-3),
        ap: a.get(12).map(|s| s.parse().unwrap()).unwrap_or(5.2),
    };
    let (found, t) = drive(&cfg);
    let repairs = t.setups.saturating_sub(t.ncand as u64);
    let lifetime = if repairs > 0 { t.cache_hits as f64 / repairs as f64 } else { f64::NAN };
    println!(
        "arm={} scene={} n={} sigma_e={} rho={} rg={} mup={} ap={} epochs={} seed={} slack={} widen={} \
         ncand={} setups={} setups_per_kick={:.2} repairs={} lifetime_epochs={} setup_evals={} \
         run_evals={} checks={} queries={} hits={} valid_checks={} cache_hits={} wall_ms={} found={}",
        a[1], cfg.scene.name(), cfg.n, cfg.sigma_e, cfg.rho, cfg.rg, cfg.mup, cfg.ap, cfg.epochs,
        cfg.seed, cfg.slack, cfg.widen, t.ncand, t.setups, t.setups as f64 / cfg.epochs as f64,
        repairs, lifetime, t.setup_evals, t.run_evals, t.checks, t.queries, t.hits,
        t.valid_checks, t.cache_hits, t.wall_ms, found.len(),
    );
    println!("per_epoch_setups={:?}", t.per_epoch_setups);
    if let Ok(base) = std::fs::read_to_string("baseline-found.txt") {
        let b: Vec<(u32, u32, f64)> = base
            .lines()
            .filter_map(|l| {
                let mut it = l.split_whitespace();
                Some((it.next()?.parse().ok()?, it.next()?.parse().ok()?, it.next()?.parse().ok()?))
            })
            .collect();
        let (misses, extras) = if cfg.arm == Arm::Skin {
            compare(&found, &b)
        } else {
            (Vec::new(), Vec::new())
        };
        println!("misses={} extras={}", misses.len(), extras.len());
        if !misses.is_empty() {
            println!("first_misses={:?}", &misses[..misses.len().min(5)]);
        }
        if !extras.is_empty() {
            println!("first_extras={:?}", &extras[..extras.len().min(5)]);
        }
    } else {
        // This arm is the baseline: dump its found set for the skin arm.
        let mut s = String::new();
        for (i, j, ts) in &found {
            s.push_str(&format!("{i} {j} {ts}\n"));
        }
        std::fs::write("baseline-found.txt", s).unwrap();
    }
}
