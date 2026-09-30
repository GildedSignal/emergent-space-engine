//! Experiments (each run ≤ 60 s): `verify <set>`, `steady <n> <horizons..>`, `scale <n|sigma>`, `kick`.
//! One JSON object per line on stdout.

use emergent_encounters::belt::{make_belt, Spec};
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
        Some("kick") => kick(),
        _ => {
            let _ = run_section;
            eprintln!("usage: encounters verify <a|b|c|long> | steady <n> <rho> <orbits..> | scale <n|sigma> | kick");
        }
    }
}
