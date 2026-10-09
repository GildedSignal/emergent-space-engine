//! Second-author run 20261009-1504: the checker's named gold experiment for 20261009-1345-system-136a.
//!
//! Measure the periapsis (varpi) rotation and the (a, e) element drift that the encounters crate's
//! cached `sections()` actually tolerate, on the shipped belt, against exact re-setup — plus the
//! wall-clock cost of one `sections()` re-setup (the quantity the cache amortizes).
//!
//! All physics runs through the shipped crate (`emergent_encounters`): `make_belt`, `cone_pairs`,
//! `sections`, `run_section`, `truth_pair`, `par_chunks`. The only new code is the drift
//! application and the cached-vs-exact matchup. One JSON object per line on stdout; metrics2.json
//! at the end. Encounters at rho = 1e-4 are ~1 per 2000 candidate pairs, so every sweep runs the
//! FULL candidate population (no sampling): pairs whose exact run has no events cannot miss any
//! and skip the cached run.

use emergent_encounters::belt::{make_belt, Spec};
use emergent_encounters::kepler::Body;
use emergent_encounters::method::run_section;
use emergent_encounters::pairs::{cone_pairs, sections, Section};
use emergent_encounters::truth::{truth_pair, TruthStats};
use emergent_encounters::par_chunks;
use std::f64::consts::TAU;
use std::time::Instant;

const RHO: f64 = 1e-4;
const SAFETY: f64 = 1.1; // main.rs's SAFETY
const T1: f64 = 20.0 * TAU; // horizon: 20 orbits of a = 1
const THREADS: usize = 4;
const MATCH_TOL: f64 = 1e-3; // conjunctions are >= ~40 time units apart

#[derive(Clone, Copy)]
struct Ev {
    t: f64,
    kind: usize,
}

/// The shipped method on (bi, bj) over [0, T1], events tagged by section kind.
/// `cached` = reuse those sections (no re-setup); None = exact re-setup (the reference).
fn method_events(bi: &Body, bj: &Body, cached: Option<&[Section]>, evals: &mut u64) -> Vec<Ev> {
    let mut out: Vec<Ev> = Vec::new();
    let owned: Vec<Section>;
    let list: &[Section] = match cached {
        Some(s) => s,
        None => {
            owned = sections(bi, bj, RHO, SAFETY, evals);
            &owned
        }
    };
    let mut st = Default::default();
    for sec in list {
        let mut raw: Vec<(f64, f64)> = Vec::new();
        run_section(bi, bj, sec, RHO, 0.0, T1, &mut st, &mut raw);
        for (t, _) in raw {
            out.push(Ev { t, kind: sec.kind as usize });
        }
    }
    out.sort_by(|a, b| a.t.total_cmp(&b.t));
    let mut keep: Vec<Ev> = Vec::with_capacity(out.len());
    for e in out {
        if keep.is_empty() || (e.t - keep.last().unwrap().t).abs() > 1e-7 {
            keep.push(e);
        }
    }
    keep
}

/// Drift one body: rotate its periapsis by dpom, scale a and e by (1+da_rel), (1+de_rel).
/// lam0 (mean longitude at t=0) is held fixed: the body stays where it was at the cutover, the
/// orbit label moves — the physical situation of a cache reuse after slow drift. The integer
/// period is kept exactly when a does not move.
fn drifted(b: &Body, dpom: f64, da_rel: f64, de_rel: f64) -> Body {
    let m0 = TAU * ((b.period - b.tp) as f64) / (b.period as f64);
    let lam0 = (m0 + b.pom) % TAU;
    let pom = (b.pom + dpom) % TAU;
    let e = (b.e * (1.0 + de_rel)).clamp(1e-9, 0.999);
    if da_rel == 0.0 {
        Body::with_period(b.period, e, pom, lam0)
    } else {
        Body::new(b.a * (1.0 + da_rel), e, pom, lam0)
    }
}

/// missed-by-kind (exact events no cache event matched) and extra (cache events unmatched).
fn matchup(exact: &[Ev], cache: &[Ev]) -> ([u32; 3], u32) {
    let mut missed_kind = [0u32; 3];
    let mut used = vec![false; cache.len()];
    let mut ci = 0usize;
    for e in exact {
        while ci + 1 < cache.len() && cache[ci + 1].t < e.t {
            ci += 1;
        }
        let mut hit = false;
        let mut k = ci;
        while k < cache.len() && cache[k].t <= e.t + MATCH_TOL {
            if e.t - MATCH_TOL <= cache[k].t && !used[k] {
                used[k] = true;
                hit = true;
                break;
            }
            k += 1;
        }
        if !hit {
            missed_kind[e.kind] += 1;
        }
    }
    (missed_kind, used.iter().filter(|&&u| !u).count() as u32)
}

fn jarr3(v: &[u32; 3]) -> String {
    format!("[{},{},{}]", v[0], v[1], v[2])
}

#[derive(Default)]
struct Sweep {
    tag: String,
    pairs: u64,
    pairs_with_events: u64,
    exact_events: u64,
    cache_events: u64,
    missed: [u32; 3],
    extra: u32,
    pairs_with_miss: u32,
    /// pairs that had exact events (capped), for the truth control
    event_pairs: Vec<(u32, u32)>,
    frag: Vec<String>,
}

fn sweep(tag: &str, belt: &[Body], pairs: &[(u32, u32)], dpom: f64, da: f64, de: f64) -> Sweep {
    let t = Instant::now();
    let parts = par_chunks(pairs.len(), 16384, THREADS, |range| {
        let mut s = Sweep::default();
        for &p in &pairs[range] {
            let (i, j) = (p.0 as usize, p.1 as usize);
            let bi = drifted(&belt[i], dpom, da, de);
            let bj = &belt[j];
            let mut ev = 0u64;
            let ex = method_events(&bi, bj, None, &mut ev);
            s.pairs += 1;
            if ex.is_empty() {
                continue;
            }
            s.pairs_with_events += 1;
            if s.event_pairs.len() < 64 {
                s.event_pairs.push(p);
            }
            let nom = sections(&belt[i], &belt[j], RHO, SAFETY, &mut ev);
            let ca = method_events(&bi, bj, Some(&nom), &mut ev);
            let (mi, x) = matchup(&ex, &ca);
            let miss: u32 = mi.iter().sum();
            s.exact_events += ex.len() as u64;
            s.cache_events += ca.len() as u64;
            for q in 0..3 {
                s.missed[q] += mi[q];
            }
            s.extra += x;
            if miss > 0 {
                s.pairs_with_miss += 1;
                s.frag.push(format!(
                    "{{\"tag\":\"{}\",\"i\":{},\"j\":{},\"missed\":{},\"by_kind\":{},\"extra\":{}}}",
                    tag, i, j, miss, jarr3(&mi), x
                ));
            }
        }
        s
    });
    let mut tot = Sweep::default();
    tot.tag = tag.into();
    for p in parts {
        tot.pairs += p.pairs;
        tot.pairs_with_events += p.pairs_with_events;
        tot.exact_events += p.exact_events;
        tot.cache_events += p.cache_events;
        tot.extra += p.extra;
        tot.pairs_with_miss += p.pairs_with_miss;
        for q in 0..3 {
            tot.missed[q] += p.missed[q];
        }
        for e in p.event_pairs {
            if tot.event_pairs.len() < 64 {
                tot.event_pairs.push(e);
            }
        }
        tot.frag.extend(p.frag);
    }
    let row = format!(
        "{{\"sweep\":\"{}\",\"dpom\":{:.4e},\"da_rel\":{:.4e},\"de_rel\":{:.4e},\"pairs\":{},\"pairs_with_events\":{},\"exact_events\":{},\"cache_events\":{},\"missed\":{},\"extra\":{},\"pairs_with_miss\":{},\"seconds\":{:.1}}}",
        tag,
        dpom,
        da,
        de,
        tot.pairs,
        tot.pairs_with_events,
        tot.exact_events,
        tot.cache_events,
        jarr3(&tot.missed),
        tot.extra,
        tot.pairs_with_miss,
        t.elapsed().as_secs_f64()
    );
    println!("{}", row);
    tot
}

fn main() {
    let spec = Spec {
        name: "belt".into(),
        n: 4096,
        sigma_e: 0.1,
        rho: RHO,
        a_lo: 0.9,
        a_hi: 1.1,
        keys: 0,
        seed: 1,
        orbits: 20.0,
    };
    let belt = make_belt(&spec);
    let t0 = Instant::now();
    let scan = cone_pairs(&belt, RHO);
    let pairs = scan.pairs;
    let t_cone = t0.elapsed().as_secs_f64();
    println!(
        "{{\"phase\":\"belt\",\"bodies\":{},\"cone_pairs\":{},\"cone_scanned\":{},\"cone_seconds\":{:.3}}}",
        belt.len(),
        pairs.len(),
        scan.scanned,
        t_cone
    );

    let mut rows: Vec<String> = Vec::new();
    let mut all_sweeps: Vec<Sweep> = Vec::new();

    // ---- varpi ladder over the full candidate population ----
    let varpi_ladder: [f64; 8] = [
        0.0, 2.4e-4, 5e-4, 1e-3, 2e-3, 3e-3, 5e-3, 1.5e-2,
    ];
    for &dpom in &varpi_ladder {
        let tag = format!("varpi_{:.4e}", dpom);
        all_sweeps.push(sweep(&tag, &belt, &pairs, dpom, 0.0, 0.0));
    }

    // ---- radial ladder (e-only, then a+e corner) ----
    let radial_ladder: [(f64, f64); 4] = [
        (0.0, 2.44e-4),         // half k-bucket
        (0.0, 4.883e-4),        // one bucket ln-width ln(1+2^-11)
        (1e-4, 2.44e-4),        // corner
        (2.44e-4, 2.44e-4),     // worst corner: a and e each half bucket
    ];
    for &(da, de) in &radial_ladder {
        let tag = format!("radial_{:.4e}_{:.4e}", da, de);
        all_sweeps.push(sweep(&tag, &belt, &pairs, 0.0, da, de));
    }

    // ---- truth control: exact re-setup vs brute-force truth, on pairs that had events ----
    {
        let ctrl: Vec<(&str, f64, f64, f64)> = vec![
            ("varpi_0.0000e0", 0.0, 0.0, 0.0),
            ("varpi_2.4000e-4", 2.4e-4, 0.0, 0.0),
            ("varpi_1.5000e-2", 1.5e-2, 0.0, 0.0),
        ];
        for (tag, dpom, da, de) in ctrl {
            let s = all_sweeps.iter().find(|s| s.tag == tag).unwrap();
            let n = s.event_pairs.len().min(48);
            let mut missed = 0u32;
            let mut truth_events = 0u32;
            let mut exact_events = 0u32;
            for &p in &s.event_pairs[..n] {
                let (i, j) = (p.0 as usize, p.1 as usize);
                let bi = drifted(&belt[i], dpom, da, de);
                let bj = &belt[j];
                let mut ev = 0u64;
                let ex = method_events(&bi, bj, None, &mut ev);
                let mut tr: Vec<(f64, f64)> = Vec::new();
                let mut ts = TruthStats::default();
                truth_pair(&bi, bj, RHO, T1, &mut tr, &mut ts);
                truth_events += tr.len() as u32;
                exact_events += ex.len() as u32;
                let tex: Vec<Ev> = tr.iter().map(|&(t, _)| Ev { t, kind: 0 }).collect();
                let (mi, _) = matchup(&tex, &ex);
                missed += mi.iter().sum::<u32>();
            }
            let row = format!(
                "{{\"control\":\"truth_vs_exact_setup\",\"sweep\":\"{}\",\"pairs\":{},\"truth_events\":{},\"exact_events\":{},\"missed_by_exact_setup\":{}}}",
                tag, n, truth_events, exact_events, missed
            );
            println!("{}", row);
            rows.push(row);
        }
    }

    // ---- wall-clock: sections() re-setup cost per candidate pair (the amortized quantity) ----
    {
        let ntim = 100_000usize;
        let stride = (pairs.len() / ntim).max(1);
        let mut times: Vec<f64> = Vec::with_capacity(ntim);
        let mut evs: Vec<u64> = Vec::with_capacity(ntim);
        for p in pairs.iter().step_by(stride) {
            let (i, j) = (p.0 as usize, p.1 as usize);
            let t = Instant::now();
            let mut e = 0u64;
            let _ = sections(&belt[i], &belt[j], RHO, SAFETY, &mut e);
            times.push(t.elapsed().as_secs_f64() * 1e6);
            evs.push(e);
        }
        times.sort_by(|a, b| a.total_cmp(b));
        evs.sort();
        let evs_f: Vec<f64> = evs.iter().map(|x| *x as f64).collect();
        let q = |v: &Vec<f64>, p: f64| v[((v.len() as f64 - 1.0) * p) as usize];
        // query cost that remains per pair per 20 orbits (the baseline the setup adds to)
        let t = Instant::now();
        let mut qev = 0u64;
        for p in pairs.iter().step_by(stride) {
            let (i, j) = (p.0 as usize, p.1 as usize);
            let _ = method_events(&belt[i], &belt[j], None, &mut qev);
        }
        let run_secs = t.elapsed().as_secs_f64();
        let row = format!(
            "{{\"phase\":\"sections_wall_clock\",\"pairs\":{},\"us_med\":{:.2},\"us_p90\":{:.2},\"us_p99\":{:.2},\"us_max\":{:.2},\"evals_med\":{},\"evals_p99\":{},\"method20orbits_us_med\":{:.1}}}",
            times.len(),
            q(&times, 0.5),
            q(&times, 0.9),
            q(&times, 0.99),
            times[times.len() - 1],
            q(&evs_f, 0.5),
            q(&evs_f, 0.99),
            run_secs / times.len() as f64 * 1e6
        );
        println!("{}", row);
        rows.push(row);
    }

    for s in &all_sweeps {
        rows.push(format!(
            "{{\"sweep\":\"{}\",\"pairs\":{},\"pairs_with_events\":{},\"exact_events\":{},\"missed\":{},\"extra\":{},\"pairs_with_miss\":{}}}",
            s.tag,
            s.pairs,
            s.pairs_with_events,
            s.exact_events,
            jarr3(&s.missed),
            s.extra,
            s.pairs_with_miss
        ));
    }

    let mut f = std::fs::File::create("metrics2.json").unwrap();
    use std::io::Write;
    writeln!(f, "[{}]", rows.join(",\n")).unwrap();
    let mut fl = std::fs::File::create("exp2_fragile.jsonl").unwrap();
    for s in &all_sweeps {
        for line in &s.frag {
            writeln!(fl, "{}", line).unwrap();
        }
    }
    println!("{{\"phase\":\"done\"}}");
}
