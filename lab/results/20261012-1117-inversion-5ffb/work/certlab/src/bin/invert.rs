//! Inversion run 20261012-1117: attack the co-orbital phase certificate
//! (wt/cx-b-coorbital-cert, built from lab gold 20261006-0346-taleb-09b5).
//!
//! Three probes:
//! 1. `bounds`  — are the closed-form bounds inside `Neighbours::new`
//!    (`centre = e + 2 asin(e/(1+sqrt(1-e^2)))`, `scale = (1+e)^{3/2}/sqrt(1-e)`)
//!    actually upper bounds? (exhaustive numeric audit)
//! 2. `fuzz`    — sampled-truth soundness fuzz of `phase::group_events`
//!    (candidates + emitted events) over adversarial scenes; tree control on
//!    every scene.
//! 3. `cost`    — the trigger's blind side: `group_events` picks the phase
//!    certificate whenever `reach < pi`, with no cost term. Measured work of
//!    the certificate vs the tree tier in the transition zone.

use certlab::kepler::Body;
use certlab::phase::{self, Neighbours};
use std::collections::BTreeSet;
use std::f64::consts::{PI, TAU};
use std::time::Instant;

fn ur(seed: &mut u64) -> f64 {
    let mut x = *seed;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    *seed = x;
    ((x.wrapping_mul(0x2545F4914F6CDD1D) >> 11) as f64) / ((1u64 << 53) as f64)
}

fn true_anom(e: f64, ea: f64) -> f64 {
    2.0 * ((1.0 + e).sqrt() * (0.5 * ea).sin()).atan2((1.0 - e).sqrt() * (0.5 * ea).cos())
}

// ---------------------------------------------------------------- subcommand 1

fn cmd_bounds() {
    // centre bound: coded >= max_E |f - M| ?
    let mut worst_slack = f64::INFINITY;
    let mut worst_e = 0.0;
    let mut fe_worst_slack = f64::INFINITY; // the |f-E| component alone
    let mut fe_worst_e = 0.0;
    for i in 0..=1966 {
        let e = 0.001 + i as f64 * 0.0005; // up to 0.984
        let mut m_fm = 0.0f64;
        let mut m_fe = 0.0f64;
        let steps = 2_000_000u64;
        for k in 0..steps {
            let ea = TAU * k as f64 / steps as f64;
            let f = true_anom(e, ea);
            let m = ea - e * ea.sin();
            let fm = (f - m).abs();
            let fe = (f - ea).abs();
            if fm > m_fm {
                m_fm = fm;
            }
            if fe > m_fe {
                m_fe = fe;
            }
        }
        let coded = e + 2.0 * (e / (1.0 + (1.0 - e * e).sqrt())).asin();
        let slack = coded - m_fm;
        if slack < worst_slack {
            worst_slack = slack;
            worst_e = e;
        }
        let fe_slack = 2.0 * (e / (1.0 + (1.0 - e * e).sqrt())).asin() - m_fe;
        if fe_slack < fe_worst_slack {
            fe_worst_slack = fe_slack;
            fe_worst_e = e;
        }
    }
    println!(
        "RESULT bounds centre_slack_min={:.3e} at e={:.4} (negative => UNSOUND)",
        worst_slack, worst_e
    );
    println!(
        "RESULT bounds fe_component_slack_min={:.3e} at e={:.4} (negative => component undersized)",
        fe_worst_slack, fe_worst_e
    );
    // scale bound: coded (1+e)^{3/2}/sqrt(1-e) >= max_E dM/df = (1-e cosE)^2/sqrt(1-e^2) ?
    let mut s_worst = f64::INFINITY;
    let mut s_e = 0.0;
    for i in 0..=983 {
        let e = 0.001 + i as f64 * 0.001;
        let mut mx = 0.0f64;
        for k in 0..1_000_000u64 {
            let ea = TAU * k as f64 / 1_000_000.0;
            let v = (1.0 - e * ea.cos()).powi(2) / (1.0 - e * e).sqrt();
            if v > mx {
                mx = v;
            }
        }
        let coded = (1.0 + e).powf(1.5) / (1.0 - e).sqrt();
        if coded - mx < s_worst {
            s_worst = coded - mx;
            s_e = e;
        }
    }
    println!(
        "RESULT bounds scale_slack_min={:.3e} at e={:.4} (negative => UNSOUND)",
        s_worst, s_e
    );
}

// ---------------------------------------------------------------- subcommand 2

struct Scene {
    name: String,
    b: Vec<Body>,
    rho: f64,
    t0: f64,
    t1: f64,
}

fn scene(kind: &str, seed: u64, n: usize) -> Scene {
    let mut s = seed | 1;
    let (b, rho, t0, t1) = match kind {
        // mixed eccentricities inside the certificate's active zone
        // (2*centre + angular < pi), shared period => drift term exactly 0.
        "mixede" => {
            let period = (TAU * 1.0_f64.powf(1.5) * certlab::kepler::TICKS).round() as u64;
            let lead = ur(&mut s) * TAU;
            let mut b = Vec::with_capacity(n);
            for i in 0..n {
                let e = 0.25 + 0.40 * ur(&mut s);
                let pom = ur(&mut s) * TAU;
                // half clustered hard, half spread through the reach shell
                let lam = if i % 2 == 0 {
                    lead + (ur(&mut s) - 0.5) * 0.02
                } else {
                    lead + (ur(&mut s) - 0.5) * 5.4
                };
                b.push(Body::with_period(period, e, pom, lam));
            }
            (b, 0.006, 3.0, 3.1)
        }
        // shared shape, high e: scaled-angular branch, plus large epochs
        "sharedhie" => {
            let period = (TAU * 1.0_f64.powf(1.5) * certlab::kepler::TICKS).round() as u64;
            let e = 0.9;
            let pom = 0.7;
            let lead = ur(&mut s) * TAU;
            let mut b = Vec::with_capacity(n);
            for i in 0..n {
                let lam = if i % 2 == 0 {
                    lead + (ur(&mut s) - 0.5) * 0.01
                } else {
                    lead + (ur(&mut s) - 0.5) * 0.5
                };
                b.push(Body::with_period(period, e, pom, lam));
            }
            let t0 = 1e6 * (1.0 + 90.0 * ur(&mut s));
            (b, 0.002, t0, t0 + 0.08)
        }
        // slow units (a=100), large a-spread: drift term near refusal,
        // full TAU phase spread, sampling affordable.
        "drift" => {
            let mut b = Vec::with_capacity(n);
            let lead = ur(&mut s) * TAU;
            for i in 0..n {
                let (a, lam) = if i % 2 == 0 {
                    (100.0 + 0.05 * (ur(&mut s) - 0.5), lead + (ur(&mut s) - 0.5) * 0.02)
                } else {
                    (85.0 + 30.0 * ur(&mut s), lead + (ur(&mut s) - 0.5) * 5.8)
                };
                let period = (TAU * a.powf(1.5) * certlab::kepler::TICKS).round() as u64;
                let e = 0.02 * ur(&mut s);
                let pom = ur(&mut s) * TAU;
                b.push(Body::with_period(period, e, pom, lam));
            }
            (b, 1.0, 100.0, 2050.0)
        }
        // pairs straddling the 0/TAU seam, separations swept through the
        // certificate's exact boundary (shared shape, e = 0.5).
        "seam" => {
            let period = (TAU * 1.0_f64.powf(1.5) * certlab::kepler::TICKS).round() as u64;
            let e = 0.5;
            let pom = 0.3;
            let rho = 0.003;
            let rmin: f64 = 1.0 * (1.0 - e);
            let ang = 2.0 * (rho / (2.0 * rmin)).asin();
            let scaled = ang * (1.0 + e).powf(1.5) / (1.0 - e).sqrt();
            let mut b = Vec::with_capacity(n);
            let mut i = 0;
            while b.len() + 2 <= n {
                let dm = scaled * (0.4 + 1.2 * (i as f64) / (n as f64 / 2.0));
                // A just below TAU, B just above 0 => the pair sits on the seam
                b.push(Body::with_period(period, e, pom, TAU - 1e-9));
                b.push(Body::with_period(period, e, pom, TAU - 1e-9 + dm));
                i += 1;
            }
            (b, rho, 1.0, 1.0 + 0.5)
        }
        // the certificate's home regime: tight shared-shape ring (their gate)
        "tight" => {
            let period = (TAU * 1.0_f64.powf(1.5) * certlab::kepler::TICKS).round() as u64;
            let e = 0.02;
            let pom = 0.0;
            let mut b = Vec::with_capacity(n);
            for i in 0..n {
                let lam = TAU * i as f64 / n as f64 + 0.1 * ur(&mut s);
                b.push(Body::with_period(period, e, pom, lam));
            }
            (b, 1.5 * TAU / n as f64, 2.0, 2.0 + 0.3)
        }
        _ => panic!("unknown kind"),
    };
    Scene {
        name: format!("{kind}-{seed}"),
        b,
        rho,
        t0,
        t1,
    }
}

/// Sampled truth: every pair whose sampled min distance < 1.02 rho, refined by
/// golden-section around the best sample. Returns (i, j, refined_d, t*).
fn sampled_truth(sc: &Scene) -> Vec<(u32, u32, f64, f64)> {
    let vmax = sc.b.iter().map(|x| x.vmax()).fold(0.0, f64::max);
    let mut dt = sc.rho / (4.0 * vmax);
    let steps = (((sc.t1 - sc.t0) / dt).ceil() as usize).clamp(2, 262144);
    dt = (sc.t1 - sc.t0) / steps as f64;
    let n = sc.b.len();
    // per-sample states
    let mut sx = vec![0.0f64; (steps + 1) * n];
    let mut sy = vec![0.0f64; (steps + 1) * n];
    for k in 0..=steps {
        let t = sc.t0 + k as f64 * dt;
        for (j, bod) in sc.b.iter().enumerate() {
            let st = bod.state(t);
            sx[k * n + j] = st[0];
            sy[k * n + j] = st[1];
        }
    }
    let mut out = Vec::new();
    for i in 0..n {
        for j in (i + 1)..n {
            let mut best = f64::INFINITY;
            let mut bk = 0usize;
            for k in 0..=steps {
                let dx = sx[k * n + i] - sx[k * n + j];
                let dy = sy[k * n + i] - sy[k * n + j];
                let d = dx * dx + dy * dy;
                if d < best {
                    best = d;
                    bk = k;
                }
            }
            if best.sqrt() < 1.02 * sc.rho {
                // golden-section refine on [t_bk - dt, t_bk + dt] clamp
                let lo = sc.t0 + bk as f64 * dt - dt;
                let hi = sc.t0 + bk as f64 * dt + dt;
                let dist = |t: f64| {
                    let (a, c) = (sc.b[i].state(t), sc.b[j].state(t));
                    ((a[0] - c[0]).powi(2) + (a[1] - c[1]).powi(2)).sqrt()
                };
                let (mut a, mut bb) =
                    (lo.max(sc.t0), (sc.t0 + bk as f64 * dt + dt).min(sc.t1));
                let mut c: f64;
                let phi = 0.6180339887498949;
                let mut tbest = sc.t0 + bk as f64 * dt;
                for _ in 0..90 {
                    let d1 = bb - (bb - a) * phi;
                    let d2 = a + (bb - a) * phi;
                    if dist(d1) < dist(d2) {
                        bb = d2;
                    } else {
                        a = d1;
                    }
                    tbest = 0.5 * (a + bb);
                    if bb - a < 1e-14 {
                        break;
                    }
                }
                c = dist(tbest);
                if c > dist(sc.t0 + bk as f64 * dt) {
                    c = dist(sc.t0 + bk as f64 * dt);
                    tbest = sc.t0 + bk as f64 * dt;
                }
                out.push((i as u32, j as u32, c, tbest));
            }
        }
    }
    out
}

fn cmd_fuzz() {
    let kinds = ["mixede", "sharedhie", "drift", "seam", "tight"];
    let per = [10, 6, 6, 6, 4];
    let n = 110usize;
    let mut total_scenes = 0usize;
    let mut total_contacts = 0usize;
    let mut cert_miss = 0usize;
    let mut emit_miss = 0usize;
    let mut tree_miss = 0usize;
    let mut inactive = 0usize;
    for (kind, cnt) in kinds.iter().zip(per.iter()) {
        for k in 0..*cnt {
            let seed = 0x9E3779B97F4A7C15u64
                .wrapping_mul(kind.len() as u64 + 1)
                .wrapping_add(1000 * k as u64 + *cnt as u64);
            let sc = scene(kind, seed, n);
            let truth = sampled_truth(&sc);
            let contacts: Vec<_> = truth
                .iter()
                .filter(|(_, _, d, _)| *d < sc.rho * (1.0 - 1e-9))
                .collect();
            // certificate candidate set
            let cert = Neighbours::new(&sc.b, sc.rho, sc.t0, sc.t1);
            let mut cands = BTreeSet::new();
            let mut reach = f64::NAN;
            let mut maxk = 0usize;
            let mut phase_on = false;
            if let Some(c) = &cert {
                phase_on = true;
                reach = c.reach;
                let (cnt_pairs, k) = c.visit(|i, j| {
                    cands.insert((i.min(j), i.max(j)));
                });
                maxk = k;
                let _ = cnt_pairs;
            } else {
                inactive += 1;
            }
            // emitted events: group_events (whatever tier it picks internally)
            let mut emitted = BTreeSet::new();
            let st = phase::group_events(&sc.b, sc.rho, sc.t0, sc.t1, |i, j, _, _| {
                emitted.insert((i.min(j), i.max(j)));
            });
            // tree control
            let mut tree_emitted = BTreeSet::new();
            phase::tree_events(&sc.b, sc.rho, sc.t0, sc.t1, |i, j, _, _| {
                tree_emitted.insert((i.min(j), i.max(j)));
            });
            let mut cm = 0;
            let mut em = 0;
            let mut tm = 0;
            for (i, j, d, t) in &contacts {
                let pair = (*i, *j);
                if phase_on && !cands.contains(&pair) {
                    cm += 1;
                    println!(
                        "DETAIL cert_miss {} pair=({},{}) d/rho={:.6} t={:.4} reach={:.5}",
                        sc.name,
                        i,
                        j,
                        d / sc.rho,
                        t,
                        reach
                    );
                }
                if !emitted.contains(&pair) {
                    em += 1;
                    println!(
                        "DETAIL emit_miss {} pair=({},{}) d/rho={:.6} phase={}",
                        sc.name,
                        i,
                        j,
                        d / sc.rho,
                        st.phase
                    );
                }
                if !tree_emitted.contains(&pair) {
                    tm += 1;
                    println!(
                        "DETAIL tree_miss {} pair=({},{}) d/rho={:.6}",
                        sc.name,
                        i,
                        j,
                        d / sc.rho
                    );
                }
            }
            cert_miss += cm;
            emit_miss += em;
            tree_miss += tm;
            total_contacts += contacts.len();
            total_scenes += 1;
            println!(
                "RESULT fuzz scene={} phase={} reach={:.5} k={} contacts={} cert_miss={} emit_miss={} tree_miss={}",
                sc.name,
                phase_on,
                if phase_on { reach } else { f64::NAN },
                maxk,
                contacts.len(),
                cm,
                em,
                tm
            );
        }
    }
    println!(
        "RESULT fuzz_total scenes={} contacts={} cert_miss={} emit_miss={} tree_miss={} cert_inactive_scenes={}",
        total_scenes, total_contacts, cert_miss, emit_miss, tree_miss, inactive
    );
}

// ---------------------------------------------------------------- subcommand 3

fn cost_series(tag: &str, es: (f64, f64), sizes: &[usize]) {
    let period = (TAU * certlab::kepler::TICKS).round() as u64; // a = 1 for all
    println!("RESULT cost_series tag={} e_range=[{},{}]", tag, es.0, es.1);
    let mut prev_pairs = 0.0f64;
    let mut prev_n = 0.0f64;
    for &n in sizes {
        let mut s = 0x1234_5678_9ABC_DEF0u64 | (tag.len() as u64);
        let mut b = Vec::with_capacity(n);
        for i in 0..n {
            let e = es.0 + (es.1 - es.0) * ur(&mut s);
            let pom = ur(&mut s) * TAU;
            let lam = ur(&mut s) * TAU;
            b.push(Body::with_period(period, e, pom, lam));
            let _ = i;
        }
        let rho = 0.005;
        let (t0, t1) = (5.0, 5.05);
        // certificate path (what group_events itself chooses); collect the
        // contact set in the same timed pass
        let mut e1 = BTreeSet::new();
        let t = Instant::now();
        let st = phase::group_events(&b, rho, t0, t1, |i, j, _, _| {
            e1.insert((i.min(j), i.max(j)));
        });
        let dt_cert = t.elapsed().as_secs_f64();
        // tree control
        let mut e2 = BTreeSet::new();
        let t = Instant::now();
        let stt = phase::tree_events(&b, rho, t0, t1, |i, j, _, _| {
            e2.insert((i.min(j), i.max(j)));
        });
        let dt_tree = t.elapsed().as_secs_f64();
        let same = e1 == e2;
        let slope = if prev_pairs > 0.0 {
            ((st.neighbours as f64) / prev_pairs).log2() / ((n as f64) / prev_n).log2()
        } else {
            f64::NAN
        };
        println!(
            "RESULT cost tag={} n={} phase={} reach={:.4} k={} cert_pairs={} tree_pairs={} tree_nodes={} contacts={} t_cert={:.4}s t_tree={:.4}s ratio={:.1} exponent={} same_contact_set={}",
            tag,
            n,
            st.phase,
            st.concentration * TAU,
            st.max_k,
            st.neighbours,
            stt.tree.cand,
            stt.tree.node_tests,
            e1.len(),
            dt_cert,
            dt_tree,
            if dt_tree > 0.0 { dt_cert / dt_tree } else { f64::INFINITY },
            slope,
            same
        );
        prev_pairs = st.neighbours as f64;
        prev_n = n as f64;
    }
}

fn cmd_cost() {
    // the certificate's home regime (positive control, linear, from their gate)
    let period = (TAU * certlab::kepler::TICKS).round() as u64;
    for n in [10_000usize, 100_000, 1_000_000] {
        let b: Vec<_> = (0..n)
            .map(|i| Body::with_period(period, 0.02, 0.0, TAU * i as f64 / n as f64))
            .collect();
        let rho = 1.5 * TAU / n as f64;
        let c = Neighbours::new(&b, rho, 0.0, TAU).unwrap();
        let (pairs, k) = c.visit(|_, _| {});
        println!(
            "RESULT cost home_regime n={} pairs={} k={} pairs/n={:.3}",
            n,
            pairs,
            k,
            pairs as f64 / n as f64
        );
    }
    // the transition zone: same period (drift 0), eccentricity spread.
    // Mild spread ("battered fleet") and wide spread (near refusal).
    // the inversion probe: candidate work vs encounter rate. Shrink rho
    // (the encounter tube): reach is rho-independent to first order, so
    // certificate work must NOT track the (vanishing) encounters.
    for rho in [5.0e-3, 5.0e-4, 5.0e-5] {
        let n = 2000usize;
        let mut s = 0x1234_5678_9ABC_DEF0u64;
        let period = (TAU * certlab::kepler::TICKS).round() as u64;
        let mut b = Vec::with_capacity(n);
        for _ in 0..n {
            let e = 0.05 + 0.60 * ur(&mut s);
            let pom = ur(&mut s) * TAU;
            let lam = ur(&mut s) * TAU;
            b.push(Body::with_period(period, e, pom, lam));
        }
        let (t0, t1) = (5.0, 5.05);
        let mut e1 = BTreeSet::new();
        let t = Instant::now();
        let st = phase::group_events(&b, rho, t0, t1, |i, j, _, _| {
            e1.insert((i.min(j), i.max(j)));
        });
        let dt = t.elapsed().as_secs_f64();
        println!(
            "RESULT cost tag=rho-scan n=2000 rho={:e} phase={} cert_pairs={} contacts={} pairs_per_encounter={} t={:.3}s",
            rho,
            st.phase,
            st.neighbours,
            e1.len(),
            if e1.is_empty() { f64::INFINITY } else { st.neighbours as f64 / e1.len() as f64 },
            dt
        );
    }
    // a-spread belt pushing the drift term past pi: the certificate must
    // step aside on its own (reach >= pi => refuse => tree inside group_events).
    println!("RESULT cost_series tag=drift-refuse");
    for n in [1000usize, 4000] {
        let mut s = 0xDEAD_BEEFu64;
        let mut b = Vec::with_capacity(n);
        for _ in 0..n {
            let a = 0.4 + 1.8 * ur(&mut s);
            let period = (TAU * a.powf(1.5) * certlab::kepler::TICKS).round() as u64;
            let e = 0.05 + 0.6 * ur(&mut s);
            let pom = ur(&mut s) * TAU;
            let lam = ur(&mut s) * TAU;
            b.push(Body::with_period(period, e, pom, lam));
        }
        let rho = 0.005;
        let (t0, t1) = (5.0, 5.05);
        let mut e1 = BTreeSet::new();
        let t = Instant::now();
        let st = phase::group_events(&b, rho, t0, t1, |i, j, _, _| {
            e1.insert((i.min(j), i.max(j)));
        });
        let dt = t.elapsed().as_secs_f64();
        println!(
            "RESULT cost tag=drift-refuse n={} phase={} reach_frac={:.3} contacts={} tree_cand={} t={:.4}s",
            n, st.phase, st.concentration, e1.len(), st.tree.cand, dt
        );
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    match args.get(1).map(|s| s.as_str()) {
        Some("bounds") => cmd_bounds(),
        Some("fuzz") => cmd_fuzz(),
        Some("cost") => cmd_cost(),
        _ => {
            eprintln!("usage: invert bounds|fuzz|cost");
            std::process::exit(2);
        }
    }
}
