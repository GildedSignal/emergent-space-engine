//! Experiments (each run ≤ 60 s): `verify <set>`, `steady <n> <horizons..>`, `scale <n|sigma>`, `kick`.
//! One JSON object per line on stdout.

use emergent_encounters::belt::{make_belt, Spec, Rng};
use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{pair_events, run_section, Stats};
use emergent_encounters::pairs::{cone_pairs, is_candidate, radial_pairs, sections, Sorted};
use emergent_encounters::truth::{truth_pair, TruthStats};
use emergent_encounters::{dioph, par_chunks};
use std::collections::HashMap;
use std::f64::consts::{PI, TAU};
use std::time::Instant;

const THREADS: usize = 4;
const SAFETY: f64 = 1.1;

type Enc = (u32, u32, f64, f64);

fn spec(name: &str, n: usize, sigma_e: f64, rho: f64, a_lo: f64, a_hi: f64, keys: usize, orbits: f64, seed: u64) -> Spec {
    Spec { name: name.into(), n, sigma_e, rho, a_lo, a_hi, keys, seed, orbits }
}

fn verify_set(set: &str) -> Vec<Spec> {
    let s = 20261001;
    match set {
        "a" => vec![
            spec("r8like-s1e-3-r1e-4", 1000, 1e-3, 1e-4, 1.0, 1.5, 0, 200.0, s + 1),
            spec("r8like-s3e-3-r1e-4", 1000, 3e-3, 1e-4, 1.0, 1.5, 0, 100.0, s + 2),
            spec("r8like-s1e-2-r1e-4", 1000, 1e-2, 1e-4, 1.0, 1.5, 0, 100.0, s + 3),
            spec("r8like-s3e-2-r1e-4", 1000, 3e-2, 1e-4, 1.0, 1.5, 0, 50.0, s + 4),
        ],
        "b" => vec![
            spec("r8like-s1e-3-r1e-3", 1000, 1e-3, 1e-3, 1.0, 1.5, 0, 100.0, s + 5),
            spec("r8like-s1e-2-r1e-3", 1000, 1e-2, 1e-3, 1.0, 1.5, 0, 50.0, s + 6),
            spec("r8like-s3e-2-r3e-5", 1000, 3e-2, 3e-5, 1.0, 1.5, 0, 50.0, s + 7),
        ],
        "c" => vec![
            spec("narrow-adversarial", 400, 0.025, 3e-3, 1.0, 1.0025, 0, 20.0, s + 8),
            spec("coorbital", 300, 3e-4, 1e-3, 1.0, 1.0001, 0, 50.0, s + 9),
            spec("equal-period-keys", 300, 1e-2, 1e-3, 1.0, 1.001, 3, 50.0, s + 10),
        ],
        "d" => vec![
            spec("hot-s0.1-r1e-3", 500, 0.1, 1e-3, 1.0, 1.5, 0, 50.0, s + 12),
            spec("mixed-a0.5-3-s0.2-r1e-3", 400, 0.2, 1e-3, 0.5, 3.0, 0, 50.0, s + 13),
            spec("dense-n3000-s1e-2-r3e-4", 3000, 1e-2, 3e-4, 1.0, 1.5, 0, 20.0, s + 14),
        ],
        "long" => vec![spec("long-1000-orbits", 300, 1e-2, 1e-3, 1.0, 1.5, 0, 1000.0, s + 11)],
        "long10k" => vec![spec("long-10000-orbits", 100, 1e-2, 1e-3, 1.0, 1.5, 0, 10000.0, s + 15)],
        _ => panic!("unknown set"),
    }
}

fn truth_all(b: &[Body], pairs: &[(u32, u32)], rho: f64, t_end: f64) -> (Vec<Enc>, TruthStats) {
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

fn method_all(b: &[Body], pairs: &[(u32, u32)], rho: f64, t0: f64, t1: f64) -> (Vec<Enc>, Stats) {
    let parts = par_chunks(pairs.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &pairs[r] {
            tmp.clear();
            pair_events(&b[i as usize], &b[j as usize], rho, SAFETY, t0, t1, &mut st, &mut tmp);
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

/// (missed, false, matched truth, extra method events matching an already matched truth event)
fn matchup(truth: &[Enc], meth: &[Enc], t_end: f64, tol: f64) -> (Vec<Enc>, Vec<Enc>, u64, u64) {
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
    let mut by_pair: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for e in meth {
        by_pair.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut tby: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for e in truth {
        tby.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut missed = Vec::new();
    let mut matched = 0;
    for e in truth.iter().filter(|e| inside(e.2)) {
        let ok = by_pair.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < tol));
        if ok {
            matched += 1;
        } else {
            missed.push(*e);
        }
    }
    let mut false_ = Vec::new();
    let mut dup = 0;
    let mut seen: HashMap<(u32, u32, i64), u32> = HashMap::new();
    for e in meth.iter().filter(|e| inside(e.2)) {
        match tby.get(&(e.0, e.1)).and_then(|v| v.iter().find(|&&t| (t - e.2).abs() < tol)) {
            None => false_.push(*e),
            Some(&t) => {
                let c = seen.entry((e.0, e.1, (t * 1e6) as i64)).or_insert(0);
                *c += 1;
                if *c > 1 {
                    dup += 1;
                }
            }
        }
    }
    (missed, false_, matched, dup)
}

/// r8 v2's reference sees an encounter only within its conjunction window.
fn r8_sees(bi: &Body, bj: &Body, rho: f64, t: f64, t_end: f64) -> (bool, bool) {
    let dn = bi.n - bj.n;
    let li = bi.mean_anomaly(0.0) + bi.pom;
    let lj = bj.mean_anomaly(0.0) + bj.pom;
    let dlam = (li - lj).rem_euclid(TAU);
    let adn = dn.abs();
    let abar = 0.5 * (bi.a + bj.a);
    let w = ((2.0 * abar * (bi.e + bj.e) + 3.0 * rho) / (abar * adn)).min(PI / adn).min(t_end);
    let off = if dn < 0.0 { dlam } else { TAU - dlam };
    let first = off / adn;
    let conj_less = first > t_end;
    let m = ((t * adn - off) / TAU).floor();
    let mut seen = false;
    for dm in [-1.0, 0.0, 1.0, 2.0] {
        let mm = m + dm;
        if mm < 0.0 {
            continue;
        }
        let tm = (off + TAU * mm) / adn;
        if tm >= 0.0 && tm <= t_end && (t - tm).abs() <= w {
            seen = true;
        }
    }
    (seen, conj_less)
}

fn conjunctions(b: &[Body], pairs: &[(u32, u32)], t_end: f64) -> f64 {
    pairs.iter().map(|&(i, j)| (b[i as usize].n - b[j as usize].n).abs() * t_end / TAU).sum()
}

fn verify(set: &str) {
    for sp in verify_set(set) {
        let t_wall = Instant::now();
        let b = make_belt(&sp);
        let t_end = sp.orbits * TAU;
        let rp = radial_pairs(&b, sp.rho);
        let t0 = Instant::now();
        let cs = cone_pairs(&b, sp.rho);
        let cone_s = t0.elapsed().as_secs_f64();
        let t1 = Instant::now();
        let (truth, tst) = truth_all(&b, &rp, sp.rho, t_end);
        let truth_s = t1.elapsed().as_secs_f64();
        let t2 = Instant::now();
        let (meth, mst) = method_all(&b, &cs.pairs, sp.rho, 0.0, t_end);
        let meth_s = t2.elapsed().as_secs_f64();
        let (missed, false_, matched, dup) = matchup(&truth, &meth, t_end, 1e-3);
        // Truth encounters outside the cone candidate set would mean the cone filter is unsound.
        let outside_cone = truth.iter().filter(|e| !is_candidate(&b[e.0 as usize], &b[e.1 as usize], sp.rho)).count();
        let mut leaked = 0;
        let mut conj_less = 0;
        for e in &truth {
            let (seen, cl) = r8_sees(&b[e.0 as usize], &b[e.1 as usize], sp.rho, e.2, t_end);
            leaked += (!seen) as u64;
            conj_less += cl as u64;
        }
        let conj = conjunctions(&b, &rp, t_end);
        let n_truth = truth.len();
        println!(
            "{{\"exp\":\"verify\",\"belt\":\"{}\",\"n\":{},\"sigma_e\":{},\"rho\":{},\"orbits\":{},\"radial_pairs\":{},\"cone_pairs\":{},\"cone_scanned\":{},\"cone_s\":{:.4},\
\"truth_enc\":{},\"truth_steps\":{},\"truth_fine\":{},\"truth_s\":{:.3},\"truth_outside_cone\":{},\"r8_leaked\":{},\"r8_conjless\":{},\
\"max_util_cross\":{:.4},\"method_enc\":{},\"matched\":{},\"missed\":{},\"false\":{},\"dup\":{},\"sections\":{:?},\"checks\":{:?},\"hits\":{:?},\"queries\":{},\"qsteps\":{},\"evals\":{},\"method_s\":{:.3},\
\"element_sort_swaps\":{:.0},\"wall_s\":{:.2},\"missed_list\":\"{:?}\",\"false_list\":\"{:?}\"}}",
            sp.name, sp.n, sp.sigma_e, sp.rho, sp.orbits, rp.len(), cs.pairs.len(), cs.scanned, cone_s,
            n_truth, tst.steps, tst.fine, truth_s, outside_cone, leaked, conj_less,
            mst.max_util_cross, meth.len(), matched, missed.len(), false_.len(), dup, mst.sections, mst.checks, mst.hits, mst.queries, mst.qsteps, mst.evals, meth_s,
            conj, t_wall.elapsed().as_secs_f64(),
            &missed[..missed.len().min(5)], &false_[..false_.len().min(5)]
        );
    }
}

/// Steady state: the method's events as the horizon grows, against element-sort's swaps.
fn steady(n: usize, rho: f64, horizons: &[f64]) {
    let sp = spec("steady", n, 1e-2, rho, 1.0, 1.5, 0, 0.0, 20261020);
    let b = make_belt(&sp);
    let t0 = Instant::now();
    let cs = cone_pairs(&b, rho);
    let cone_s = t0.elapsed().as_secs_f64();
    let rp_n = radial_pairs(&b, rho).len();
    let es_per_orbit = conjunctions(&b, &cone_pairs(&b, rho).pairs, TAU);
    for &h in horizons {
        let t1 = Instant::now();
        let (meth, st) = method_all(&b, &cs.pairs, rho, 0.0, h * TAU);
        let s = t1.elapsed().as_secs_f64();
        let hits = meth.len() as f64;
        let events = st.pairs as f64 + st.checks_total() as f64;
        println!(
            "{{\"exp\":\"steady\",\"n\":{},\"rho\":{},\"orbits\":{},\"cone_pairs\":{},\"radial_pairs\":{},\"cone_s\":{:.3},\"setups\":{},\"checks\":{},\"hits\":{},\
\"queries\":{},\"qsteps\":{},\"evals\":{},\"events_per_body_orbit\":{:.5},\"hits_per_body_orbit\":{:.6},\"work_per_encounter\":{:.3},\"steady_work_per_encounter\":{:.3},\
\"element_sort_swaps_per_body_orbit\":{:.4},\"method_s\":{:.3},\"ns_per_pair_setup_and_run\":{:.1}}}",
            n, rho, h, cs.pairs.len(), rp_n, cone_s, st.pairs, st.checks_total(), hits, st.queries, st.qsteps, st.evals,
            events / (n as f64 * h), hits / (n as f64 * h), events / hits.max(1.0), st.checks_total() as f64 / hits.max(1.0),
            es_per_orbit / n as f64, s, s * 1e9 / st.pairs as f64
        );
    }
}

/// Pairs counted without being stored (the implicit set): radial overlap, and the cone.
fn count_radial(b: &[Body], rho: f64) -> u64 {
    let mut lo: Vec<(f64, f64)> = b.iter().map(|x| (x.rmin(), x.rmax())).collect();
    lo.sort_by(|x, y| x.0.total_cmp(&y.0));
    let mut n = 0u64;
    for k in 0..lo.len() {
        let hi = lo[k].1 + 2.0 * rho;
        n += (lo[k + 1..].partition_point(|z| z.0 <= hi)) as u64;
    }
    n
}

fn count_cone(b: &[Body], sorted: &Sorted, rho: f64) -> (u64, u64) {
    let parts = par_chunks(sorted.order.len(), 1024, THREADS, |r| {
        let (mut pairs, mut scanned) = (0u64, 0u64);
        for k in r {
            let (u, i) = sorted.order[k];
            let bi = &b[i as usize];
            let reach = sorted.reach(bi);
            for &(uj, j) in &sorted.order[k + 1..] {
                if uj - u > reach {
                    break;
                }
                scanned += 1;
                pairs += is_candidate(bi, &b[j as usize], rho) as u64;
            }
        }
        (pairs, scanned)
    });
    parts.iter().fold((0, 0), |a, x| (a.0 + x.0, a.1 + x.1))
}

/// Setup alone (the range scan, the cone test, the sections and one first-hit query per section),
/// single-threaded on a sample of bodies' full ranges: (pairs, scanned, seconds, qsteps, evals).
fn setup_cost(b: &[Body], sorted: &Sorted, rho: f64, sample: &[u32]) -> (u64, u64, f64, u64, u64, [u64; 3]) {
    let t = Instant::now();
    let (mut pairs, mut scanned, mut qsteps, mut evals) = (0u64, 0u64, 0u64, 0u64);
    let mut kinds = [0u64; 3];
    for &i in sample {
        let bi = &b[i as usize];
        let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
        for &(_, j) in &sorted.order[lo..hi] {
            if j == i {
                continue;
            }
            scanned += 1;
            let bj = &b[j as usize];
            if !is_candidate(bi, bj, rho) {
                continue;
            }
            pairs += 1;
            for sec in sections(bi, bj, rho, SAFETY, &mut evals) {
                kinds[sec.kind as usize] += 1;
                let (pi, pj) = (bi.period as u128, bj.period as u128);
                let c = ((sec.ti as i128 - sec.tj as i128 + sec.w1 as i128).rem_euclid(pi as i128)) as u128;
                let d = (pi - pj % pi) % pi;
                let w = ((sec.w1 + sec.w2).max(0) as u128).min(pi - 1);
                std::hint::black_box(dioph::first_hit(c, d, pi, 0, w, &mut qsteps));
            }
        }
    }
    (pairs, scanned, t.elapsed().as_secs_f64(), qsteps, evals, kinds)
}

fn scale(which: &str, only: Option<f64>) {
    let cases: Vec<Spec> = match which {
        "n" => [1_000usize, 3_000, 10_000, 30_000, 100_000]
            .iter()
            .map(|&n| spec("scale-n", n, 1e-2, 1e-4 * 1e4 / n as f64, 1.0, 1.5, 0, 0.0, 20261030 + n as u64))
            .collect(),
        "sigma" => [1e-3, 3e-3, 1e-2, 3e-2]
            .iter()
            .map(|&s| spec("scale-sigma", 10_000, s, 1e-4, 1.0, 1.5, 0, 0.0, 20261040))
            .collect(),
        _ => panic!(),
    };
    for sp in cases {
        if let Some(x) = only {
            if (which == "n" && sp.n as f64 != x) || (which == "sigma" && sp.sigma_e != x) {
                continue;
            }
        }
        let b = make_belt(&sp);
        let t0 = Instant::now();
        let sorted = Sorted::new(&b, sp.rho);
        let sort_s = t0.elapsed().as_secs_f64();
        let t1 = Instant::now();
        let (npairs, scanned) = count_cone(&b, &sorted, sp.rho);
        let scan_s = t1.elapsed().as_secs_f64();
        let rp = count_radial(&b, sp.rho);
        let ns = sp.n.min(150);
        let sample: Vec<u32> = (0..ns).map(|k| (k * sp.n / ns) as u32).collect();
        let (sp_pairs, sp_scanned, sp_s, sp_q, sp_evals, kinds) = setup_cost(&b, &sorted, sp.rho, &sample);
        let horizon = 1000.0;
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        let t2 = Instant::now();
        let mut hits = 0u64;
        for &i in &sample {
            let bi = &b[i as usize];
            let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
            for &(_, j) in &sorted.order[lo..hi] {
                if j == i || !is_candidate(bi, &b[j as usize], sp.rho) {
                    continue;
                }
                tmp.clear();
                pair_events(bi, &b[j as usize], sp.rho, SAFETY, 0.0, horizon * TAU, &mut st, &mut tmp);
                hits += tmp.len() as u64;
            }
        }
        let run_s = t2.elapsed().as_secs_f64();
        let cb = 2.0 * npairs as f64 / sp.n as f64;
        let hits_pp_orbit = hits as f64 / (st.pairs as f64 * horizon);
        let enc_rate = cb * hits_pp_orbit;
        let es_rate = conjunctions(&b, &cone_pairs_sample(&b, &sorted, sp.rho, &sample), TAU) / ns as f64;
        println!(
            "{{\"exp\":\"scale\",\"which\":\"{}\",\"n\":{},\"sigma_e\":{},\"rho\":{},\"radial_pairs\":{},\"cone_pairs\":{},\"cone_scanned\":{},\"cone_per_body\":{:.2},\"sort_s\":{:.4},\"count_scan_s\":{:.4},\
\"sample_bodies\":{},\"sample_pairs\":{},\"sample_scanned\":{},\"setup_ns_per_pair\":{:.1},\"setup_evals_per_pair\":{:.2},\"setup_sections\":{:?},\"qsteps_per_pair\":{:.2},\
\"hits_per_pair_orbit\":{:.3e},\"enc_per_body_orbit\":{:.4e},\"checks_per_hit\":{:.3},\"run_ns_per_pair_1000_orbits\":{:.1},\"element_sort_swaps_per_body_orbit\":{:.4},\
\"crossover_orbits\":{:.1},\"per_pair_bytes_per_body\":{:.1}}}",
            which, sp.n, sp.sigma_e, sp.rho, rp, npairs, scanned, cb, sort_s, scan_s, ns, sp_pairs, sp_scanned,
            sp_s * 1e9 / sp_pairs.max(1) as f64, sp_evals as f64 / sp_pairs.max(1) as f64, kinds, sp_q as f64 / sp_pairs.max(1) as f64,
            hits_pp_orbit, enc_rate, st.checks_total() as f64 / hits.max(1) as f64, run_s * 1e9 / st.pairs.max(1) as f64, es_rate,
            (cb / 2.0) / es_rate, 12.0 * cb / 2.0
        );
    }
}

/// Each sampled body's partner pairs (both sides), for element-sort's swap rate per body.
fn cone_pairs_sample(b: &[Body], sorted: &Sorted, rho: f64, sample: &[u32]) -> Vec<(u32, u32)> {
    let mut out = Vec::new();
    for &i in sample {
        let bi = &b[i as usize];
        let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
        for &(_, j) in &sorted.order[lo..hi] {
            if j != i && is_candidate(bi, &b[j as usize], rho) {
                out.push((i, j));
            }
        }
    }
    out
}

/// A kick: re-scan the kicked body's range and re-set up its pairs. Also: how many certificates a
/// kick actually changes, and how many a stored slack (the relative period change a silent
/// certificate absorbs over the horizon) would let the re-certification skip.
fn kick() {
    let sp = spec("kick", 10_000, 1e-2, 1e-4, 1.0, 1.5, 0, 0.0, 20261050);
    let b = make_belt(&sp);
    let sorted = Sorted::new(&b, sp.rho);
    let horizon = 1000.0 * TAU;
    let tk = 10.0 * TAU;
    let nk = 100;
    let epss = [1e-9, 1e-7, 1e-5, 1e-3];
    // Old certificates of each kicked body's partners: hits, proposal count, slack budget.
    struct Old {
        j: u32,
        hits: Vec<(f64, f64)>,
        proposals: u64,
        budget: f64,
    }
    let kicked: Vec<usize> = (0..nk).map(|q| (q * 97 + 13) % sp.n).collect();
    let mut olds: Vec<Vec<Old>> = Vec::new();
    for &i in &kicked {
        let old = b[i];
        let (lo, hi) = sorted.range(old.binet()[0], sorted.reach(&old));
        let mut v = Vec::new();
        for &(_, j) in &sorted.order[lo..hi] {
            let bj = &b[j as usize];
            if j as usize == i || !is_candidate(&old, bj, sp.rho) {
                continue;
            }
            let mut hits = Vec::new();
            let mut st = Stats::default();
            pair_events(&old, bj, sp.rho, SAFETY, tk, tk + horizon, &mut st, &mut hits);
            let proposals = st.checks_total();
            let mut budget = f64::INFINITY;
            if proposals == 0 {
                for sec in sections(&old, bj, sp.rho, SAFETY, &mut 0) {
                    let (mut lo_g, mut hi_g) = (0i64, (old.period as i64) / 4);
                    for _ in 0..40 {
                        let mid = (lo_g + hi_g) / 2;
                        let mut s2 = sec.clone();
                        s2.w1 += mid;
                        s2.w2 += mid;
                        let mut st3 = Stats::default();
                        run_section_proposals(&old, bj, &s2, tk, tk + horizon, &mut st3, &mut Vec::new());
                        if st3.checks_total() > 0 {
                            hi_g = mid;
                        } else {
                            lo_g = mid;
                        }
                    }
                    budget = budget.min(lo_g as f64 / (horizon * TICKS));
                }
            } else {
                budget = 0.0;
            }
            v.push(Old { j, hits, proposals, budget });
        }
        olds.push(v);
    }
    let mut silent: Vec<f64> = olds.iter().flatten().filter(|o| o.proposals == 0).map(|o| o.budget).collect();
    silent.sort_by(|x, y| x.total_cmp(y));
    let per_body_min: Vec<f64> = olds.iter().map(|v| v.iter().map(|o| o.budget).filter(|x| *x > 0.0).fold(f64::INFINITY, f64::min)).collect();
    let mut pbm = per_body_min.clone();
    pbm.sort_by(|x, y| x.total_cmp(y));
    let total: usize = olds.iter().map(|v| v.len()).sum();
    let with_proposals = olds.iter().flatten().filter(|o| o.proposals > 0).count();
    let q = |v: &Vec<f64>, f: f64| v[((v.len() as f64 - 1.0) * f) as usize];
    println!(
        "{{\"exp\":\"kick-certificates\",\"n\":{},\"rho\":{},\"horizon_orbits\":1000,\"kicked\":{},\"pairs\":{},\"pairs_with_proposals\":{},\"silent_budget_p01\":{:.3e},\"silent_budget_p10\":{:.3e},\
\"silent_budget_median\":{:.3e},\"per_body_min_budget_median\":{:.3e},\"per_body_min_budget_min\":{:.3e}}}",
        sp.n, sp.rho, nk, total, with_proposals, q(&silent, 0.01), q(&silent, 0.1), q(&silent, 0.5), q(&pbm, 0.5), pbm[0]
    );
    for &eps in &epss {
        let (mut pairs, mut scanned, mut changed, mut flipped, mut skippable, mut skip_violations) = (0u64, 0u64, 0u64, 0u64, 0u64, 0u64);
        let mut secs = 0.0;
        for (k, &i) in kicked.iter().enumerate() {
            let old = b[i];
            let lam_k = old.mean_anomaly(tk) + old.pom;
            let a_new = old.a * (1.0 + eps);
            let n_new = a_new.powf(-1.5);
            let new = Body::new(a_new, old.e, old.pom, lam_k - n_new * tk);
            let rel_dt = (new.period as f64 - old.period as f64).abs() / old.period as f64;
            // The re-certification proper: range scan, cone tests, setups, hits in the horizon. Timed.
            let t0 = Instant::now();
            let (lo, hi) = sorted.range(new.binet()[0], sorted.reach(&new));
            let mut after: HashMap<u32, Vec<(f64, f64)>> = HashMap::new();
            let mut st = Stats::default();
            for &(_, j) in &sorted.order[lo..hi] {
                if j as usize == i {
                    continue;
                }
                scanned += 1;
                let bj = &b[j as usize];
                if !is_candidate(&new, bj, sp.rho) {
                    continue;
                }
                let mut v = Vec::new();
                pair_events(&new, bj, sp.rho, SAFETY, tk, tk + horizon, &mut st, &mut v);
                after.insert(j, v);
            }
            secs += t0.elapsed().as_secs_f64();
            pairs += after.len() as u64;
            for o in &olds[k] {
                let empty = Vec::new();
                let v = after.get(&o.j).unwrap_or(&empty);
                let same = o.hits.len() == v.len() && o.hits.iter().zip(v).all(|(x, y)| (x.0 - y.0).abs() < 1e-3);
                changed += (!same) as u64;
                flipped += (o.hits.is_empty() != v.is_empty()) as u64;
                // A stored slack would skip this pair iff its budget exceeds the kick's drift rate.
                if o.budget > rel_dt * 1.5 {
                    skippable += 1;
                    skip_violations += (!same) as u64;
                }
            }
        }
        println!(
            "{{\"exp\":\"kick\",\"n\":{},\"rho\":{},\"eps\":{:e},\"kicks\":{},\"pairs_per_kick\":{:.1},\"scanned_per_kick\":{:.1},\"us_per_kick\":{:.1},\"us_per_pair\":{:.2},\"horizon_orbits\":1000,\
\"changed_fraction\":{:.4},\"flipped_fraction\":{:.4},\"slack_skippable_fraction\":{:.4},\"slack_skip_violations\":{}}}",
            sp.n, sp.rho, eps, nk, pairs as f64 / nk as f64, scanned as f64 / nk as f64, secs * 1e6 / nk as f64, secs * 1e6 / pairs as f64,
            changed as f64 / total as f64, flipped as f64 / total as f64, skippable as f64 / total as f64, skip_violations
        );
    }
}

/// The query loop of a section without the exact checks: counts proposals in [t0, t1].
fn run_section_proposals(bi: &Body, bj: &Body, sec: &emergent_encounters::pairs::Section, t0: f64, t1: f64, st: &mut Stats, _v: &mut Vec<(f64, f64)>) {
    let pi = bi.period as i128;
    let pj = bj.period as i128;
    let t0t = (t0 * TICKS) as i128;
    let t1t = (t1 * TICKS) as i128;
    let base = sec.tj as i128 + (t0t - sec.tj as i128).div_euclid(pj) * pj;
    let lmax = (t1t - base).div_euclid(pj);
    let w1 = sec.w1 as i128;
    let w = (w1 + sec.w2 as i128).clamp(0, pi - 1);
    let c0 = (sec.ti as i128 - base + w1).rem_euclid(pi);
    let d = (pi - pj.rem_euclid(pi)).rem_euclid(pi);
    if let Some(k) = dioph::first_hit(c0 as u128, d as u128, pi as u128, 0, w as u128, &mut st.qsteps) {
        if (k as i128) <= lmax {
            st.checks[0] += 1;
        }
    }
}

// ---------------------------------------------------------------- tiered experiments

use emergent_encounters::tier::{arm_pair, tiered_arm, tiered_exact, traverse, ArmStats, Tree, TreeStats};

type Ev = (u32, u32, f64, f64);

fn sample_idx(n: usize, ns: usize) -> Vec<u32> {
    (0..ns).map(|k| (k * n / ns) as u32).collect()
}

fn guarded(ev: &[Ev], t1: f64) -> Vec<(u32, u32, f64)> {
    let mut v: Vec<(u32, u32, f64)> = ev
        .iter()
        .filter(|e| e.2 > 0.05 && e.2 < t1 - 0.05)
        .map(|e| (e.0, e.1, e.2))
        .collect();
    v.sort_by(|x, y| x.0.cmp(&y.0).then(x.1.cmp(&y.1)).then(x.2.total_cmp(&y.2)));
    v
}

fn diff(a: &[(u32, u32, f64)], b: &[(u32, u32, f64)], tol: f64) -> usize {
    a.iter().filter(|e| !b.iter().any(|m| m.0 == e.0 && m.1 == e.1 && (m.2 - e.2).abs() < tol)).count()
}

/// One body's base run: exact machinery on every candidate of its U-range.
fn base_body(b: &[Body], sorted: &Sorted, i: u32, rho: f64, t1: f64, st: &mut Stats, out: &mut Vec<Ev>) {
    let bi = &b[i as usize];
    let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
    for &(_, j) in &sorted.order[lo..hi] {
        if j <= i || !is_candidate(bi, &b[j as usize], rho) {
            continue;
        }
        let mut tmp = Vec::new();
        pair_events(bi, &b[j as usize], rho, SAFETY, 0.0, t1, st, &mut tmp);
        out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
    }
}

/// Tier scaling: dilute (rho ∝ 1/N, encounter rate per body fixed) or fixed (rho = 1e-4: the belt
/// densifies, real encounters per body grow ∝ N). Sampled bodies, exact event diff vs base.
fn tier_scale(which: &str, only: Option<f64>) {
    let horizon = 100.0;
    let t1 = horizon * TAU;
    for n in [1_000usize, 10_000, 100_000, 1_000_000] {
        let rho = if which == "dilute" { 1e-4 * 1e4 / n as f64 } else { 1e-4 };
        if let Some(x) = only {
            if n as f64 != x {
                continue;
            }
        }
        let sp = spec("tier", n, 1e-2, rho, 1.0, 1.5, 0, 0.0, 20261100 + n as u64);
        let b = make_belt(&sp);
        let sorted = Sorted::new(&b, rho);
        let ns = if n >= 1_000_000 { 40 } else { 150 };
        let sample = sample_idx(n, ns);
        let mut ast = ArmStats::default();
        let mut xst = Stats::default();
        let mut tmine = Vec::new();
        let mut armed_list: Vec<(u32, f64)> = Vec::new();
        let t0 = Instant::now();
        for &i in &sample {
            armed_list.clear();
            tiered_arm(&b, &sorted.order, i, rho, 1.5, 0.0, t1, |x| sorted.reach(x), &mut ast, &mut armed_list);
        }
        let arm_s = t0.elapsed().as_secs_f64();
        let t0b = Instant::now();
        for &i in &sample {
            armed_list.clear();
            tiered_arm(&b, &sorted.order, i, rho, 1.5, 0.0, t1, |x| sorted.reach(x), &mut ArmStats::default(), &mut armed_list);
            tiered_exact(&b, i, &armed_list, rho, 0.0, t1, &mut xst, &mut tmine);
        }
        let exact_s = t0b.elapsed().as_secs_f64() - arm_s;
        let tier_s = arm_s + exact_s;
        let mut bst = Stats::default();
        let mut tbase = Vec::new();
        let t2 = Instant::now();
        for &i in &sample {
            base_body(&b, &sorted, i, rho, t1, &mut bst, &mut tbase);
        }
        let base_s = t2.elapsed().as_secs_f64();
        let gm = guarded(&tmine, t1);
        let gb = guarded(&tbase, t1);
        let misses = diff(&gb, &gm, 1e-6);
        let extra = diff(&gm, &gb, 1e-6);
        let fires = gm.len() as f64;
        let per = |s: f64| s * 1e6 / ns as f64;
        println!(
            "{{\"exp\":\"tier-scale\",\"which\":\"{}\",\"n\":{},\"rho\":{:.2e},\"horizon_orbits\":{:.0},\"sample\":{},\"cand_per_body\":{:.1},\"arm_tests\":{},\"armed\":{},\"silent\":{},\"arm_sections\":{:?},\"exact_pairs\":{},\"exact_checks\":{},\"exact_evals\":{},\"base_evals\":{},\"fires\":{},\"arm_us_per_body\":{:.1},\"exact_us_per_body\":{:.1},\"base_us_per_body\":{:.1},\"speedup\":{:.1},\"arm_ns_per_test\":{:.0},\"armtests_per_fire\":{:.1},\"armed_div_fires\":{:.2},\"tier_us_per_fire\":{:.1},\"base_us_per_fire\":{:.1},\"misses\":{},\"extra\":{}}}",
            which, n, rho, horizon, ns, ast.tests as f64 / ns as f64, ast.tests, ast.armed, ast.silent, ast.sections,
            xst.pairs, xst.checks_total(), xst.evals, bst.evals, fires as u64, per(arm_s), per(exact_s.max(0.0)), per(base_s),
            base_s / tier_s.max(1e-12), arm_s * 1e9 / (ast.tests.max(1)) as f64,
            if fires > 0.0 { ast.tests as f64 / fires } else { f64::NAN },
            if fires > 0.0 { ast.armed as f64 / fires } else { f64::NAN },
            if fires > 0.0 { per(tier_s) / fires } else { f64::NAN },
            if fires > 0.0 { per(base_s) / fires } else { f64::NAN },
            misses, extra
        );
    }
}

/// Tree statistics over whole populations (leaf-pair granularity, no body pairs).
fn tier_tree() {
    let mut scenarios: Vec<(&str, Vec<Body>, f64)> = Vec::new();
    for (n, tag) in [(10_000usize, "belt-1e4"), (100_000, "belt-1e5"), (1_000_000, "belt-1e6")] {
        let rho = 1e-4 * 1e4 / n as f64;
        let sp = spec("belt", n, 1e-2, rho, 1.0, 1.5, 0, 0.0, 20261100 + n as u64);
        scenarios.push((tag, make_belt(&sp), rho));
    }
    let sp = spec("narrow", 10_000, 1e-2, 1e-4, 1.0, 1.05, 0, 0.0, 20261201);
    scenarios.push(("narrow-1e4", make_belt(&sp), 1e-4));
    let belt_sp = spec("belt", 9_800, 1e-2, 1e-4, 1.0, 1.3, 0, 0.0, 20261202);
    let mut fleet_b = make_belt(&belt_sp);
    let mut fr = Rng(20261203);
    for _ in 0..200 {
        let a = 1.45 + 0.1 * fr.f64();
        let e = 0.25 + 0.1 * fr.f64();
        let pom = 0.5 * fr.f64() - 0.25;
        let lam = TAU * fr.f64();
        fleet_b.push(Body::new(a, e, pom, lam));
    }
    scenarios.push(("fleet-1e4", fleet_b, 1e-4));
    for (name, b, rho) in scenarios {
        let t0 = Instant::now();
        let tree = Tree::new(&b, 32);
        let build_s = t0.elapsed().as_secs_f64();
        let mut st = TreeStats::default();
        let t1i = Instant::now();
        traverse(&tree, &b, rho, false, &mut |_, _| {}, &mut st);
        let trav_s = t1i.elapsed().as_secs_f64();
        println!(
            "{{\"exp\":\"tier-tree\",\"case\":\"{}\",\"n\":{},\"rho\":{:.2e},\"nodes\":{},\"node_tests\":{},\"pruned\":{},\"leafpair_tests\":{},\"node_tests_per_body\":{:.1},\"build_ms\":{:.1},\"trav_ms\":{:.1},\"prune_frac\":{:.3}}}",
            name, b.len(), rho, tree.nodes.len(), st.node_tests, st.pruned, st.leafpair_tests,
            st.node_tests as f64 / b.len() as f64, build_s * 1e3, trav_s * 1e3,
            st.pruned as f64 / st.node_tests.max(1) as f64
        );
    }
}

/// Tier verify: the tiered pipeline against the rigorous truth (conservative advancement).
fn tier_verify() {
    let sp = spec("verify", 600, 1e-2, 1e-4, 1.0, 1.5, 0, 0.0, 20261300);
    let b = make_belt(&sp);
    let t1 = 100.0 * TAU;
    let pairs = radial_pairs(&b, sp.rho);
    let (truth, tst) = truth_all(&b, &pairs, sp.rho, t1);
    let sorted = Sorted::new(&b, sp.rho);
    let mut ast = ArmStats::default();
    let mut xst = Stats::default();
    let mut mine: Vec<Ev> = Vec::new();
    for i in 0..b.len() as u32 {
        let mut armed = Vec::new();
        tiered_arm(&b, &sorted.order, i, sp.rho, 1.5, 0.0, t1, |x| sorted.reach(x), &mut ast, &mut armed);
        tiered_exact(&b, i, &armed, sp.rho, 0.0, t1, &mut xst, &mut mine);
    }
    let gt = guarded(&truth, t1);
    let gm = guarded(&mine, t1);
    let misses = diff(&gt, &gm, 1e-3);
    let extra = diff(&gm, &gt, 1e-3);
    println!(
        "{{\"exp\":\"tier-verify\",\"n\":{},\"rho\":{:.0e},\"horizon_orbits\":100,\"truth_events\":{},\"tier_events\":{},\"truth_steps\":{},\"truth_evals\":{},\"arm_tests\":{},\"armed\":{},\"exact_checks\":{},\"exact_evals\":{},\"misses\":{},\"extra\":{}}}",
        sp.n, sp.rho, gt.len(), gm.len(), tst.steps, tst.evals, ast.tests, ast.armed, xst.checks_total(), xst.evals, misses, extra
    );
}

/// Tier kick: base re-setup vs tree path refresh + slack-guarded re-arming, with exact validation.
fn tier_kick(n: usize) {
    let sp = spec("kick", n, 1e-2, 1e-4, 1.0, 1.5, 0, 0.0, 20261400);
    let b = make_belt(&sp);
    let sorted = Sorted::new(&b, sp.rho);
    let mut tree = Tree::new(&b, 32);
    let horizon = 100.0 * TAU;
    let tk = 10.0 * TAU;
    let nk = 30usize;
    let kicked: Vec<usize> = (0..nk).map(|q| (q * 197 + 13) % sp.n).collect();
    for eps in [1e-7f64, 1e-5, 1e-3] {
        let (mut base_us, mut tier_us, mut rearm, mut skipped, mut viol, mut pathrec, mut flips) =
            (0.0, 0.0, 0u64, 0u64, 0u64, 0usize, 0u64);
        let mut pairs_seen = 0u64;
        for &i in &kicked {
            let old = b[i];
            let lam_k = old.mean_anomaly(tk) + old.pom;
            let a_new = old.a * (1.0 + eps);
            let n_new = a_new.powf(-1.5);
            let new = Body::new(a_new, old.e, old.pom, lam_k - n_new * tk);
            let rel_dt = (new.period as f64 - old.period as f64).abs() / old.period as f64;
            let (lo, hi) = sorted.range(new.binet()[0], sorted.reach(&new));
            let mut cand: Vec<u32> = Vec::new();
            for &(_, j) in &sorted.order[lo..hi] {
                if j as usize != i && is_candidate(&new, &b[j as usize], sp.rho) {
                    cand.push(j);
                }
            }
            pairs_seen += cand.len() as u64;
            // --- base: re-setup and re-run every candidate (their kick() cost model).
            let t0 = Instant::now();
            let mut after_base: Vec<(u32, Vec<(f64, f64)>)> = Vec::new();
            for &j in &cand {
                let mut v = Vec::new();
                pair_events(&new, &b[j as usize], sp.rho, SAFETY, tk, tk + horizon, &mut Stats::default(), &mut v);
                after_base.push((j, v));
            }
            base_us += t0.elapsed().as_secs_f64() * 1e6;
            // --- tiered, timed: path refresh + slack decision (a stored due; recomputed here,
            // stateless) + re-arm of the rest + exact run on the newly armed.
            let t1i = Instant::now();
            let pos = tree.pos[i];
            pathrec += tree.refresh_path(&b, (pos / 32) as usize);
            let mut ast = ArmStats::default();
            let mut decided: Vec<(u32, bool)> = Vec::new();
            for &j in &cand {
                let mut ost = ArmStats::default();
                let (_, due_old) = arm_pair(&old, &b[j as usize], sp.rho, 1.5, tk, tk + horizon, &mut ost);
                let margin = if due_old.is_finite() { (due_old - (tk + horizon)) / horizon } else { f64::INFINITY };
                if ost.armed == 0 && margin > 1.5 * rel_dt {
                    skipped += 1;
                    decided.push((j, false));
                } else {
                    rearm += 1;
                    let on = arm_pair(&new, &b[j as usize], sp.rho, 1.5, tk, tk + horizon, &mut ast).0;
                    if on {
                        pair_events(&new, &b[j as usize], sp.rho, SAFETY, tk, tk + horizon, &mut Stats::default(), &mut Vec::new());
                    }
                    decided.push((j, true));
                }
            }
            tier_us += t1i.elapsed().as_secs_f64() * 1e6;
            // --- validation (untimed): would any slack-skipped pair have changed its hits?
            for &(j, acted) in &decided {
                let now = after_base.iter().find(|e| e.0 == j).map(|e| e.1.clone()).unwrap_or_default();
                if acted {
                    flips += (!now.is_empty()) as u64;
                    continue;
                }
                let mut pre = Vec::new();
                pair_events(&old, &b[j as usize], sp.rho, SAFETY, tk, tk + horizon, &mut Stats::default(), &mut pre);
                let same = pre.len() == now.len() && pre.iter().zip(&now).all(|(x, y)| (x.0 - y.0).abs() < 1e-3);
                viol += (!same) as u64;
            }
        }
        println!(
            "{{\"exp\":\"tier-kick\",\"n\":{},\"rho\":{:.0e},\"eps\":{:.0e},\"kicks\":{},\"cand_per_kick\":{:.0},\"base_us_per_kick\":{:.0},\"tier_us_per_kick\":{:.0},\"speedup\":{:.1},\"path_recompute\":{:.1},\"rearmed\":{},\"slack_skipped\":{},\"skip_violations\":{},\"firing_pairs\":{}}}",
            n, sp.rho, eps, nk, pairs_seen as f64 / nk as f64, base_us / nk as f64, tier_us / nk as f64,
            base_us / tier_us.max(1e-9), pathrec as f64 / nk as f64, rearm, skipped, viol, flips
        );
    }
}

/// Micro-profile of the arm path over a real candidate list.
fn arm_bench() {
    let sp = spec("bench", 10_000, 1e-2, 1e-4, 1.0, 1.5, 0, 0.0, 20261100 + 10_000);
    let b = make_belt(&sp);
    let sorted = Sorted::new(&b, sp.rho);
    let sample = sample_idx(sp.n, 50);
    let mut cands: Vec<(u32, u32)> = Vec::new();
    for &i in &sample {
        let bi = &b[i as usize];
        let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
        for &(_, j) in &sorted.order[lo..hi] {
            if j > i && is_candidate(bi, &b[j as usize], sp.rho) {
                cands.push((i, j));
            }
        }
    }
    let reps = 20;
    let t = Instant::now();
    let mut secs = 0u64;
    for _ in 0..reps {
        for &(i, j) in &cands {
            unsafe { std::hint::black_box(emergent_encounters::tier::arm_sections(&b[i as usize], &b[j as usize], sp.rho, 1.5)).len() };
            secs += 1;
        }
    }
    let s1 = t.elapsed().as_secs_f64() / reps as f64;
    let t = Instant::now();
    for _ in 0..reps {
        for &(i, j) in &cands {
            let bi = &b[i as usize];
            let bj = &b[j as usize];
            let th = bi.pom + 0.7;
            unsafe { std::hint::black_box(bi.passage_tick(th) + bj.passage_tick(th)) };
        }
    }
    let s2 = t.elapsed().as_secs_f64() / reps as f64;
    let t = Instant::now();
    for _ in 0..reps {
        for &(i, j) in &cands {
            let bi = &b[i as usize];
            let bj = &b[j as usize];
            let th = bi.pom + 0.7;
            unsafe { std::hint::black_box(bi.travel(th - 0.05, th) + bj.travel(th, th + 0.05)) };
        }
    }
    let s3 = t.elapsed().as_secs_f64() / reps as f64;
    let mut st = ArmStats::default();
    let t = Instant::now();
    for _ in 0..reps {
        for &(i, j) in &cands {
            unsafe { std::hint::black_box(arm_pair(&b[i as usize], &b[j as usize], sp.rho, 1.5, 0.0, 100.0 * TAU, &mut st)) };
        }
    }
    let s4 = t.elapsed().as_secs_f64() / reps as f64;
    println!(
        "{{\"exp\":\"armbench\",\"pairs\":{},\"arm_sections_ns\":{:.0},\"passage_ticks_ns\":{:.0},\"travel_ns\":{:.0},\"arm_pair_ns\":{:.0},\"qsteps_total\":{}}}",
        cands.len(), s1 * 1e9 / cands.len() as f64, s2 * 1e9 / cands.len() as f64, s3 * 1e9 / cands.len() as f64, s4 * 1e9 / cands.len() as f64, st.qsteps / reps
    );
}

/// Held-out scenarios: a fleet crossing a belt, a narrow belt, a densified belt — event diff vs
/// base on sampled bodies (misses must stay 0), plus arm statistics.
fn tier_heldout() {
    let horizon = 100.0;
    let t1 = horizon * TAU;
    let mut scenarios: Vec<(&str, Vec<Body>, f64)> = Vec::new();
    // Fleet: 200 eccentric, aligned-periapsis bodies crossing a cold belt.
    let belt_sp = spec("belt", 9_800, 1e-2, 1e-4, 1.0, 1.3, 0, 0.0, 20261202);
    let mut fleet_b = make_belt(&belt_sp);
    let mut fr = Rng(20261203);
    for _ in 0..200 {
        let a = 1.45 + 0.1 * fr.f64();
        let e = 0.25 + 0.1 * fr.f64();
        let pom = 0.5 * fr.f64() - 0.25;
        let lam = TAU * fr.f64();
        fleet_b.push(Body::new(a, e, pom, lam));
    }
    scenarios.push(("fleet-crossing-belt", fleet_b, 1e-4));
    let sp = spec("narrow", 10_000, 1e-2, 1e-4, 1.0, 1.05, 0, 0.0, 20261201);
    scenarios.push(("narrow-belt", make_belt(&sp), 1e-4));
    let sp = spec("dense", 30_000, 1e-2, 1e-4, 1.0, 1.5, 0, 0.0, 20261501);
    scenarios.push(("densified-belt-3x", make_belt(&sp), 1e-4));
    for (name, b, rho) in scenarios {
        let sorted = Sorted::new(&b, rho);
        let ns = 150.min(b.len());
        let mut fleet_sample: Vec<u32> = Vec::new();
        if name == "fleet-crossing-belt" {
            // Sample fleet bodies too (the last 200).
            fleet_sample = (9_800..b.len() as u32).step_by(7).collect();
        }
        let mut sample = sample_idx(b.len(), ns);
        sample.extend(fleet_sample.iter());
        let mut ast = ArmStats::default();
        let mut xst = Stats::default();
        let mut tmine = Vec::new();
        let t0 = Instant::now();
        for &i in &sample {
            let mut armed = Vec::new();
            tiered_arm(&b, &sorted.order, i, rho, 1.5, 0.0, t1, |x| sorted.reach(x), &mut ast, &mut armed);
            tiered_exact(&b, i, &armed, rho, 0.0, t1, &mut xst, &mut tmine);
        }
        let tier_s = t0.elapsed().as_secs_f64();
        let mut tbase = Vec::new();
        let t2 = Instant::now();
        for &i in &sample {
            base_body(&b, &sorted, i, rho, t1, &mut Stats::default(), &mut tbase);
        }
        let base_s = t2.elapsed().as_secs_f64();
        let gm = guarded(&tmine, t1);
        let gb = guarded(&tbase, t1);
        let misses = diff(&gb, &gm, 1e-6);
        let extra = diff(&gm, &gb, 1e-6);
        println!(
            "{{\"exp\":\"tier-heldout\",\"case\":\"{}\",\"n\":{},\"rho\":{:.0e},\"sample\":{},\"arm_tests\":{},\"armed\":{},\"fires\":{},\"armtests_per_fire\":{:.1},\"armed_div_fires\":{:.2},\"tier_us_per_body\":{:.1},\"base_us_per_body\":{:.1},\"speedup\":{:.2},\"misses\":{},\"extra\":{}}}",
            name, b.len(), rho, sample.len(), ast.tests, ast.armed, gm.len(),
            if !gm.is_empty() { ast.tests as f64 / gm.len() as f64 } else { f64::NAN },
            if !gm.is_empty() { ast.armed as f64 / gm.len() as f64 } else { f64::NAN },
            tier_s * 1e6 / sample.len() as f64, base_s * 1e6 / sample.len() as f64,
            base_s / tier_s.max(1e-12), misses, extra
        );
    }
}


fn main() {
    let args: Vec<String> = std::env::args().collect();
    match args.get(1).map(|s| s.as_str()) {
        Some("verify") => verify(&args[2]),
        Some("steady") => {
            let n: usize = args[2].parse().unwrap();
            let rho: f64 = args[3].parse().unwrap();
            let hs: Vec<f64> = args[4..].iter().map(|x| x.parse().unwrap()).collect();
            steady(n, rho, &hs)
        }
        Some("scale") => scale(&args[2], args.get(3).map(|x| x.parse().unwrap())),
        Some("tier-scale") => tier_scale(&args[2], args.get(3).map(|x| x.parse().unwrap())),
        Some("tier-tree") => tier_tree(),
        Some("tier-verify") => tier_verify(),
        Some("tier-kick") => tier_kick(args[2].parse().unwrap()),
        Some("armbench") => arm_bench(),
        Some("tier-heldout") => tier_heldout(),
        _ => {
            let _ = run_section;
            eprintln!("usage: encounters verify <a|b|c|long> | steady <n> <rho> <orbits..> | scale <n|sigma> | kick");
        }
    }
}
