//! Scout falsifier 20261006-1436-scout-eab7: does a *skin* (cached pair sections with cheap
//! element-space validity) make encounter-window setup cost track geometric churn instead of
//! element changes, with zero missed encounters?
//!
//! Arms share everything (belt, kick sequence, candidates, exact checks); only the window-setup
//! policy differs:
//!   baseline : sections() recomputed for every candidate pair every kick epoch.
//!   skin     : sections cached per pair; a ~10-flop validity check against each body's Binet
//!              point, period and periapsis tick; re-setup only when the drift exceeds the slack.
//!              Cached windows/arcs are widened at setup by (widen_frac * rho) so the superset
//!              stays a superset while the drift is under the slack.
//!   (widen=0 with slack>0 is the negative control: stale windows must miss.)
//!
//! Encounter sets are decided by the crate's exact per-pair checks in every arm; the skin only
//! changes when setups happen, never which exact check decides. Floats explore here (research).

use emergent_encounters::belt::{make_belt, Rng, Spec};
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{run_section, Stats};
use emergent_encounters::pairs::{cone_pairs, eps_u, sections, Section};
use std::collections::HashMap;
use std::time::Instant;

const SAFETY: f64 = 3.0;
const TAU: f64 = std::f64::consts::TAU;

#[derive(Clone, Copy)]
enum Arm {
    Baseline,
    Skin,
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
    n: usize,
    sigma_e: f64,
    rho: f64,
    kappa: f64,
    epochs: usize,
    seed: u64,
    slack: f64, // element drift allowed, in units of the pair's eps_u
    widen: f64, // window/arc widening, in units of rho (time units)
}

/// One kick: bounded random-walk element change, position-continuous (mean anomaly at t kept).
fn kick(b: &Body, t_now: f64, kappa: f64, rng: &mut Rng) -> Body {
    let u = |rng: &mut Rng| 2.0 * rng.f64() - 1.0;
    let a = b.a * (1.0 + kappa * u(rng));
    let e = (b.e + 0.5 * kappa * u(rng)).clamp(1e-9, 0.6);
    let pom = b.pom + TAU * kappa * u(rng);
    let m = b.mean_anomaly(t_now);
    let nb = Body::new(a, e, pom, 0.0);
    let p = nb.period as i128;
    let tp = ((t_now * TICKS - (m / TAU) * p as f64).round() as i128).rem_euclid(p) as u64;
    Body { tp, ..nb }
}

/// Cached pair validity: both bodies' Binet points within slack*eps_u of the setup snapshot,
/// and (period drift + mirrored periapsis drift) within half the window widening.
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

/// Drive one arm over `epochs` kick epochs (one a=1 orbit each). Returns the found encounter set.
fn drive(arm: Arm, cfg: &Cfg) -> (Vec<(u32, u32, f64)>, Totals) {
    let spec = Spec {
        name: "belt".into(),
        n: cfg.n,
        sigma_e: cfg.sigma_e,
        rho: cfg.rho,
        a_lo: 0.9,
        a_hi: 1.1,
        keys: 0,
        seed: cfg.seed,
        orbits: 1.0,
    };
    let mut bodies = make_belt(&spec);
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
        let t0 = epoch as f64 * TAU;
        let t1 = t0 + TAU;
        if epoch > 0 && cfg.kappa > 0.0 {
            // One kick epoch: every body gets one bounded element kick. The stream is keyed by
            // (seed, epoch), so both arms kick identically.
            let mut krng = Rng(cfg.seed ^ 0xBEEF ^ (epoch as u64).wrapping_mul(0x51ED_2701));
            for b in bodies.iter_mut() {
                *b = kick(b, t0, cfg.kappa, &mut krng);
            }
        }
        let mut ep_setups = 0u64;
        for &(i, j) in &cands {
            let (bi, bj) = (&bodies[i as usize], &bodies[j as usize]);
            let secs: Vec<Section>;
            match arm {
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

/// Misses of a vs b (a must find everything b finds), and a's extras.
fn compare(a: &[(u32, u32, f64)], b: &[(u32, u32, f64)]) -> (Vec<(u32, u32, f64)>, usize) {
    let mut idx: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for &(i, j, t) in a {
        idx.entry((i, j)).or_default().push(t);
    }
    let mut misses = Vec::new();
    for &(i, j, t) in b {
        let ok = idx.get(&(i, j)).map_or(false, |ts| ts.iter().any(|&x| (x - t).abs() < 1e-6));
        if !ok {
            misses.push((i, j, t));
        }
    }
    (misses, a.len().saturating_sub(b.len()))
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    // args: arm n sigma_e rho kappa epochs seed slack widen
    let arm = match a[1].as_str() {
        "baseline" => Arm::Baseline,
        "skin" => Arm::Skin,
        _ => panic!("arm must be baseline|skin"),
    };
    let cfg = Cfg {
        n: a[2].parse().unwrap(),
        sigma_e: a[3].parse().unwrap(),
        rho: a[4].parse().unwrap(),
        kappa: a[5].parse().unwrap(),
        epochs: a[6].parse().unwrap(),
        seed: a[7].parse().unwrap(),
        slack: a[8].parse().unwrap(),
        widen: a[9].parse().unwrap(),
    };
    let (found, t) = drive(arm, &cfg);
    let base = std::fs::read_to_string("baseline-found.txt").ok();
    println!(
        "arm={} n={} sigma_e={} rho={} kappa={} epochs={} seed={} slack={} widen={} \
         ncand={} setups={} setup_evals={} run_evals={} checks={} queries={} hits={} \
         valid_checks={} cache_hits={} wall_ms={} found={}",
        a[1], cfg.n, cfg.sigma_e, cfg.rho, cfg.kappa, cfg.epochs, cfg.seed, cfg.slack, cfg.widen,
        t.ncand, t.setups, t.setup_evals, t.run_evals, t.checks, t.queries, t.hits,
        t.valid_checks, t.cache_hits, t.wall_ms, found.len(),
    );
    println!("per_epoch_setups={:?}", t.per_epoch_setups);
    if let Some(base) = base {
        let b: Vec<(u32, u32, f64)> = base
            .lines()
            .filter_map(|l| {
                let mut it = l.split_whitespace();
                Some((it.next()?.parse().ok()?, it.next()?.parse().ok()?, it.next()?.parse().ok()?))
            })
            .collect();
        let (misses, extras) = compare(&found, &b);
        println!("misses={} extras={}", misses.len(), extras);
        if !misses.is_empty() {
            println!("first_misses={:?}", &misses[..misses.len().min(5)]);
        }
    } else {
        // This arm is the baseline: dump its found set for the other arms.
        let mut s = String::new();
        for (i, j, ts) in &found {
            s.push_str(&format!("{i} {j} {ts}\n"));
        }
        std::fs::write("baseline-found.txt", s).unwrap();
    }
}
