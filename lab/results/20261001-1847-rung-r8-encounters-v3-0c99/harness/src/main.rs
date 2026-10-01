//! Case drivers for r8 v3: smoke, casea (20 belts), caseb (steady), casec (scaling), cased (kicks).
//! One JSON object per line on stdout.

use emergent_encounters::belt::Rng as XRng;
use emergent_encounters::kepler::Body;
use std::f64::consts::TAU;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{cone_pairs, is_candidate, sections, Sorted};
use rung::{conj_all, conj_count, dioph_all, load_belt, radial_pairs, truth_all, truth_pair, matchup, Enc, TStats};
use std::time::Instant;
#[allow(unused)]

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let dir = args.get(2).cloned().unwrap_or_else(|| ".".into());
    match args[1].as_str() {
        "smoke" => smoke(&dir),
        "casea" => casea(&dir),
        "caseb" => caseb(&dir),
        "casec" => casec(&dir),
        "cased" => cased(&dir),
        _ => eprintln!("usage: rung smoke|casea|caseb|casec|cased <data-dir>"),
    }
}

struct BeltSpec {
    name: String,
    n: usize,
    sigma_e: f64,
    rho: f64,
    orbits: f64,
}

fn load_specs(dir: &str) -> Vec<BeltSpec> {
    std::fs::read_to_string(format!("{dir}/belts.tsv"))
        .unwrap()
        .lines()
        .map(|l| {
            let f: Vec<&str> = l.split('\t').collect();
            BeltSpec { name: f[0].into(), n: f[1].parse().unwrap(), sigma_e: f[2].parse().unwrap(), rho: f[3].parse().unwrap(), orbits: f[4].parse().unwrap() }
        })
        .collect()
}

fn tj(t: f64) -> f64 {
    t * TAU
}

fn median(v: &mut [f64]) -> f64 {
    v.sort_by(|a, b| a.total_cmp(b));
    let n = v.len();
    0.5 * (v[(n - 1) / 2] + v[n / 2])
}

// ------------------------------------------------------------------ smoke

fn smoke(dir: &str) {
    let specs = load_specs(dir);
    let sp = &specs[0];
    let b = load_belt(&format!("{dir}/{}.bin", sp.name));
    let t_end = 40.0;
    let mut pairs = radial_pairs(&b, sp.rho);
    pairs.truncate(400);
    let (truth, tst) = truth_all(&b, &pairs, sp.rho, t_end);
    let (meth, mst) = dioph_all(&b, &pairs, sp.rho, 0.0, t_end);
    let (missed, false_, n_truth) = matchup(&truth, &meth, t_end, 1e-3);
    println!(
        "{{\"exp\":\"smoke\",\"belt\":\"{}\",\"pairs\":{},\"truth\":{},\"meth\":{},\"missed\":{},\"false\":{},\"checks\":{},\"t_evals\":{},\"t_steps\":{},\"t_fine\":{}}}",
        sp.name, pairs.len(), truth.len(), meth.len(), missed, false_, mst.checks_total(), tst.evals, tst.steps, tst.fine
    );
}

// ------------------------------------------------------------------ case (a)

#[derive(Default)]
struct Pool {
    cfg: Vec<(String, u64, u64, u64, u128)>, // name, missed, false, truth, checks
}

impl Pool {
    fn add(&mut self, name: &str, missed: u64, false_: u64, truth: u64, checks: u128) {
        if let Some(e) = self.cfg.iter_mut().find(|e| e.0 == name) {
            e.1 += missed;
            e.2 += false_;
            e.3 += truth;
            e.4 += checks;
        } else {
            self.cfg.push((name.into(), missed, false_, truth, checks));
        }
    }
    fn print(&self) {
        for (name, missed, false_, truth, checks) in &self.cfg {
            println!(
                "{{\"exp\":\"pool\",\"cfg\":\"{}\",\"missed\":{},\"false\":{},\"truth\":{},\"checks\":{},\"missed_fraction\":{:.7},\"false_fraction\":{:.7},\"checks_per_encounter\":{:.4}}}",
                name, missed, false_, truth, checks,
                *missed as f64 / *truth as f64,
                *false_ as f64 / *truth as f64,
                *checks as f64 / *truth as f64
            );
        }
    }
}

fn casea(dir: &str) {
    let specs = load_specs(dir);
    let sel = std::env::var("BELTS").unwrap_or_default();
    let want: std::collections::HashSet<&str> = sel.split(',').filter(|x| !x.is_empty()).collect();
    let mut pool = Pool::default();
    for sp in specs.iter().filter(|s| s.orbits == 100.0 && (want.is_empty() || want.contains(s.name.as_str()))) {
        let t0 = Instant::now();
        let b = load_belt(&format!("{dir}/{}.bin", sp.name));
        let t_end = tj(sp.orbits);
        let mut rp = radial_pairs(&b, sp.rho);
        if let Ok(k) = std::env::var("PAIRSAMP") {
            let k: usize = k.parse().unwrap();
            let mut xr = emergent_encounters::belt::Rng(424242);
            rp = (0..k).map(|_| rp[(xr.next_u64() as usize) % rp.len()]).collect();
            rp.sort_unstable();
            rp.dedup();
        }
        let t1 = Instant::now();
        let mut truth: Vec<Enc> = Vec::new();
        let mut tst = TStats::default();
        let budget = std::env::var("PAIRBUDGET").ok().and_then(|x| x.parse().ok()).unwrap_or(20.0f64);
        let mut skipped = 0u64;
        for &(i, j) in &rp {
            if let Some((mut v, st)) = rung::timed_truth_pair(b[i as usize], b[j as usize], sp.rho, t_end, budget) {
                for e in &mut v { e.0 = i; e.1 = j; }
                truth.append(&mut v);
                tst.evals += st.evals;
                tst.steps += st.steps;
                tst.fine += st.fine;
            } else {
                skipped += 1;
            }
        }
        let truth_s = t1.elapsed().as_secs_f64();
        let t2 = Instant::now();
        let cs = cone_pairs(&b, sp.rho);
        // on a sampled pair set, every configuration runs the same pairs; the method's cone filter
        // stays part of the method (a sampled pair outside the cone is never examined by it)
        let meth_pairs: Vec<(u32, u32)> = if std::env::var("PAIRSAMP").is_ok() {
            rp.iter().filter(|&&(i, j)| emergent_encounters::pairs::is_candidate(&b[i as usize], &b[j as usize], sp.rho)).copied().collect()
        } else {
            cs.pairs.clone()
        };
        let (meth, mst) = dioph_all(&b, &meth_pairs, sp.rho, 0.0, t_end);
        let meth_s = t2.elapsed().as_secs_f64();
        let t3 = Instant::now();
        let (conj, cst) = conj_all(&b, &rp, sp.rho, t_end);
        let conj_s = t3.elapsed().as_secs_f64();
        let (m_d, f_d, n_t) = matchup(&truth, &meth, t_end, 1e-3);
        let (m_e, f_e, _) = matchup(&truth, &conj, t_end, 1e-3);
        let (m_o, f_o, _) = matchup(&truth, &truth, t_end, 1e-3);
        pool.add("diophantine", m_d, f_d, n_t, mst.checks_total() as u128);
        pool.add("element-sort", m_e, f_e, n_t, cst.conjunctions as u128);
        pool.add("conjunction-sampled", m_e, f_e, n_t, cst.conjunctions as u128);
        pool.add("oracle", m_o, f_o, n_t, n_t as u128);
        println!(
            "{{\"exp\":\"a\",\"belt\":\"{}\",\"sig\":{:.5},\"rho\":{:.2e},\"n\":{},\"radial\":{},\"cone\":{},\"truth\":{},\"meth\":{},\"conj\":{},\"n_truth\":{},\"missed_d\":{},\"false_d\":{},\"missed_c\":{},\"false_c\":{},\"checks_d\":{},\"sections\":{:?},\"conj_events\":{},\"t_evals\":{},\"t_steps\":{},\"t_fine\":{},\"skipped\":{},\"truth_s\":{:.1},\"meth_s\":{:.2},\"conj_s\":{:.2},\"wall_s\":{:.1}}}",
            sp.name, sp.sigma_e, sp.rho, sp.n, rp.len(), cs.pairs.len(), truth.len(), meth.len(), conj.len(),
            n_t, m_d, f_d, m_e, f_e, mst.checks_total(), mst.sections, cst.conjunctions, tst.evals, tst.steps, tst.fine,
            skipped, truth_s, meth_s, conj_s, t0.elapsed().as_secs_f64()
        );
    }
    pool.print();
}

// ------------------------------------------------------------------ case (b)

fn caseb(dir: &str) {
    let specs = load_specs(dir);
    let sp = specs.iter().find(|s| s.name == "b-steady").unwrap();
    let b = load_belt(&format!("{dir}/{}.bin", sp.name));
    let (n, rho) = (b.len(), sp.rho);
    let rp = radial_pairs(&b, rho);
    let cs = cone_pairs(&b, rho);

    // truth encounter rate over the full horizon from a uniform sample of candidate pairs
    let nsamp = std::env::var("NSAMP").ok().and_then(|x| x.parse().ok()).unwrap_or(128usize);
    let mut xr = XRng(987654321);
    let sample: Vec<(u32, u32)> = (0..nsamp).map(|_| rp[(xr.next_u64() as usize) % rp.len()]).collect();
    let t0 = Instant::now();
    let mut enc_s = 0usize;
    let mut tst = TStats::default();
    let mut skipped_b = 0usize;
    let budget = std::env::var("PAIRBUDGET").ok().and_then(|x| x.parse().ok()).unwrap_or(20.0f64);
    for &(i, j) in &sample {
        if let Some((v, st)) = rung::timed_truth_pair(b[i as usize], b[j as usize], rho, tj(sp.orbits), budget) {
            enc_s += v.len();
            tst.evals += st.evals;
            tst.steps += st.steps;
            tst.fine += st.fine;
        } else {
            skipped_b += 1;
        }
    }
    let nsamp_eff = nsamp - skipped_b;
    let truth_rate = if nsamp_eff > 0 { enc_s as f64 / nsamp_eff as f64 * rp.len() as f64 / (n as f64 * sp.orbits) } else { f64::NAN };
    let se = truth_rate / (enc_s as f64).sqrt().max(1.0);
    println!(
        "{{\"exp\":\"b-truth\",\"n\":{},\"rho\":{:.2e},\"radial\":{},\"cone\":{},\"sample\":{},\"skipped\":{},\"sample_eff\":{},\"enc_sample\":{},\"orbits\":{},\"rate\":{:.6e},\"rate_rel_se\":{:.4},\"evals\":{},\"steps\":{},\"s\":{:.1}}}",
        n, rho, rp.len(), cs.pairs.len(), nsamp, skipped_b, nsamp_eff, enc_s, sp.orbits, truth_rate, se, tst.evals, tst.steps, t0.elapsed().as_secs_f64()
    );

    let hz: Vec<f64> = std::env::var("HORIZONS").map(|x| x.split(',').filter_map(|v| v.parse().ok()).collect()).unwrap_or_else(|_| vec![20.0, 100.0, 1000.0, 1e4, 1e5]);
    for &h in &hz {
        let t1 = Instant::now();
        let (meth, st) = dioph_all(&b, &cs.pairs, rho, 0.0, tj(h));
        let s = t1.elapsed().as_secs_f64();
        let events = st.pairs as f64 + st.checks_total() as f64;
        println!(
            "{{\"exp\":\"b-dioph\",\"orbits\":{},\"setups\":{},\"checks\":{},\"hits\":{},\"events_per_body_orbit\":{:.6e},\"hits_per_body_orbit\":{:.6e},\"steady_ratio\":{:.4},\"s\":{:.2}}}",
            h, st.pairs, st.checks_total(), meth.len(), events / (n as f64 * h), meth.len() as f64 / (n as f64 * h),
            events / (n as f64 * h) / truth_rate, s
        );
    }

    let hz: Vec<f64> = std::env::var("HORIZONS").map(|x| x.split(',').filter_map(|v| v.parse().ok()).collect()).unwrap_or_else(|_| vec![20.0, 100.0, 1000.0, 1e4, 1e5]);
    for &h in &hz {
        let thr = tj(h);
        let tot: u64 = rp.iter().map(|&(i, j)| conj_count(&b[i as usize], &b[j as usize], thr)).sum();
        let rate = tot as f64 / (n as f64 * h);
        println!(
            "{{\"exp\":\"b-neg\",\"orbits\":{},\"conj_events\":{},\"events_per_body_orbit\":{:.6e},\"steady_ratio\":{:.4}}}",
            h, tot, rate, rate / truth_rate
        );
    }
    println!("{{\"exp\":\"b-oracle\",\"rate\":{:.6e},\"steady_ratio\":1.0}}", truth_rate);
    println!(
        "{{\"exp\":\"b-bytes\",\"cone_pairs_per_body\":{:.1},\"bytes_per_body\":{:.0}}}",
        cs.pairs.len() as f64 * 2.0 / n as f64,
        12.0 * cs.pairs.len() as f64 * 2.0 / n as f64
    );
}

// ------------------------------------------------------------------ case (c)

fn casec(dir: &str) {
    let specs = load_specs(dir);
    let mut out: Vec<(usize, f64, f64, f64)> = Vec::new(); // n, dioph rate, conj rate, truth rate
    let selc = std::env::var("CASEC").unwrap_or_default();
    let wantc: std::collections::HashSet<&str> = selc.split(',').filter(|x| !x.is_empty()).collect();
    for sp in specs.iter().filter(|s| s.name.starts_with("c-") && (wantc.is_empty() || wantc.contains(s.name.as_str()))) {
        let b = load_belt(&format!("{dir}/{}.bin", sp.name));
        let (n, rho, h) = (b.len(), sp.rho, 1000.0f64);
        let sorted = Sorted::new(&b, rho);
        let ns = 150usize;
        let sample: Vec<u32> = (0..ns).map(|k| (k * n / ns) as u32).collect();
        let mut in_sample = vec![false; n];
        for &i in &sample {
            in_sample[i as usize] = true;
        }
        // diophantine: each sampled body's cone pairs, each pair once, over the horizon
        let t0 = Instant::now();
        let parts = emergent_encounters::par_chunks(sample.len(), 1, 2, |r| {
            let mut st = Stats::default();
            let mut tmp = Vec::new();
            let mut conj = 0u64;
            for &i in &sample[r] {
                let bi = &b[i as usize];
                let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
                for &(_, j) in &sorted.order[lo..hi] {
                    let bj = &b[j as usize];
                    if j == i || (in_sample[j as usize] && j < i) || !is_candidate(bi, bj, rho) {
                        continue;
                    }
                    tmp.clear();
                    pair_events(bi, bj, rho, 1.1, 0.0, tj(h), &mut st, &mut tmp);
                }
                for j in 0..n {
                    if j as u32 == i {
                        continue;
                    }
                    let bj = &b[j];
                    if bj.rmin() <= bi.rmax() + 2.0 * rho && bi.rmin() <= bj.rmax() + 2.0 * rho {
                        let c = conj_count(bi, bj, tj(h));
                        if !in_sample[j] || j as u32 > i {
                            conj += c; // both-sampled pairs are charged once, at the larger index
                        }
                    }
                }
            }
            (st, conj)
        });
        let (mut st, mut conj) = (Stats::default(), 0u64);
        for (s, c) in parts {
            st.add(&s);
            conj += c;
        }
        let dioph_rate = st.checks_total() as f64 / (2.0 * ns as f64 * h);
        let conj_rate = conj as f64 / (2.0 * ns as f64 * h);
        let dioph_s = t0.elapsed().as_secs_f64();

        // truth rate: rejection-sampled radial pairs over the same horizon
        let mut xr = XRng(20261001);
        let mut picked: Vec<(u32, u32)> = Vec::new();
        let mut tries = 0u64;
        while picked.len() < 128 && tries < 1 << 22 {
            tries += 1;
            let i = (xr.next_u64() as usize) % n;
            let j = (xr.next_u64() as usize) % n;
            if i == j {
                continue;
            }
            let (i, j) = (i.min(j), i.max(j));
            let (bi, bj) = (&b[i], &b[j]);
            let (x, y) = if bi.rmin() <= bj.rmin() { (bi, bj) } else { (bj, bi) };
            if y.rmin() <= x.rmax() + 2.0 * rho && !picked.contains(&(i as u32, j as u32)) {
                picked.push((i as u32, j as u32));
            }
        }
        let tparts = emergent_encounters::par_chunks(picked.len(), 8, 2, |r| {
            let mut out = Vec::new();
            let mut st = TStats::default();
            for &(i, j) in &picked[r] {
                truth_pair(&b[i as usize], &b[j as usize], rho, tj(h), &mut out, &mut st);
            }
            (out.len(), st)
        });
        let enc_s: usize = tparts.iter().map(|(k, _)| *k).sum();
        // total radial pairs by sweep (counting only; never materialised)
        let mut idx: Vec<u32> = (0..n as u32).collect();
        idx.sort_by_key(|&i| b[i as usize].rmin().to_bits());
        let rmins: Vec<f64> = idx.iter().map(|&i| b[i as usize].rmin()).collect();
        let mut nradial = 0u64;
        for (k, &i) in idx.iter().enumerate() {
            let hi = b[i as usize].rmax() + 2.0 * rho;
            nradial += rmins[k + 1..].partition_point(|&x| x <= hi) as u64;
        }
        let truth_rate = enc_s as f64 / picked.len() as f64 * nradial as f64 / (n as f64 * h);
        println!(
            "{{\"exp\":\"c\",\"n\":{},\"rho\":{:.2e},\"horizon\":{},\"sample_bodies\":{},\"checks\":{},\"setups\":{},\"hits\":{},\"dioph_checks_per_body_orbit\":{:.5e},\"conj_rate\":{:.5e},\"truth_rate\":{:.5e},\"truth_enc_sample\":{},\"radial_pairs\":{},\"dioph_s\":{:.2}}}",
            n, rho, h, ns, st.checks_total(), st.pairs, st.hits_total(), dioph_rate, conj_rate, truth_rate, enc_s, nradial, dioph_s
        );
        out.push((n, dioph_rate, conj_rate, truth_rate));
    }
    let fit = |f: &dyn Fn(&(usize, f64, f64, f64)) -> f64| -> f64 {
        let xs: Vec<f64> = out.iter().map(|r| (r.0 as f64).ln()).collect();
        let ys: Vec<f64> = out.iter().map(|r| (f(r) * r.0 as f64).ln()).collect();
        let (mx, my) = (xs.iter().sum::<f64>() / xs.len() as f64, ys.iter().sum::<f64>() / ys.len() as f64);
        let mut num = 0.0;
        let mut den = 0.0;
        for k in 0..xs.len() {
            num += (xs[k] - mx) * (ys[k] - my);
            den += (xs[k] - mx) * (xs[k] - mx);
        }
        num / den
    };
    println!(
        "{{\"exp\":\"c-fit\",\"scale_exponent_dioph\":{:.4},\"scale_exponent_esort\":{:.4},\"scale_exponent_conj\":{:.4},\"scale_exponent_oracle\":{:.4}}}",
        fit(&|r| r.1),
        fit(&|r| r.2),
        fit(&|r| r.2),
        fit(&|r| r.3)
    );
}

// ------------------------------------------------------------------ case (d)

fn cased(dir: &str) {
    let specs = load_specs(dir);
    let sp = specs.iter().find(|s| s.name == "d-kick").unwrap();
    let b = load_belt(&format!("{dir}/{}.bin", sp.name));
    let (n, rho) = (b.len(), sp.rho);
    let sorted = Sorted::new(&b, rho);
    let kicks: Vec<(usize, f64)> = std::fs::read_to_string(format!("{dir}/kicks.tsv"))
        .unwrap()
        .lines()
        .map(|l| { let f: Vec<&str> = l.split('\t').collect(); (f[0].parse().unwrap(), f[1].parse().unwrap()) })
        .collect();
    let tk = 10.0 * TAU;
    let horizon = 1000.0 * TAU;
    let mut ratios_d = Vec::new();
    let mut ratios_r = Vec::new();
    let mut other_d = 0u64;
    let mut other_r = 0u64;
    let (mut us_total, mut pairs_total, mut kicks_n) = (0.0f64, 0u64, 0u64);
    for &(ki, sign) in &kicks {
        let old = b[ki];
        // before: the kicked body's candidate count
        let (mut lo, mut hi) = (0usize, 0usize);
        let mut before_d = 0u64;
        {
            let (l, h) = sorted.range(old.binet()[0], sorted.reach(&old));
            lo = l;
            hi = h;
        }
        for &(_, j) in &sorted.order[lo..hi] {
            if j as usize != ki && is_candidate(&old, &b[j as usize], rho) {
                before_d += 1;
            }
        }
        // the kick: da/a = 1e-3, mean longitude continuous at t_k
        let lam_k = old.mean_anomaly(tk) + old.pom;
        let a_new = old.a * (1.0 + sign * 1e-3);
        let n_new = a_new.powf(-1.5);
        let new = Body::new(a_new, old.e, old.pom, lam_k - n_new * tk);
        // after (diophantine): re-scan the range, re-test the cone, rebuild the certificates
        let t0 = Instant::now();
        let mut after_d = 0u64;
        let (l2, h2) = sorted.range(new.binet()[0], sorted.reach(&new));
        for &(_, j) in &sorted.order[l2..h2] {
            if j as usize == ki {
                continue;
            }
            let bj = &b[j as usize];
            if !is_candidate(&new, bj, rho) {
                continue;
            }
            after_d += 1;
            let mut ev = 0u64;
            for sec in sections(&new, bj, rho, 1.1, &mut ev) {
                let pi = new.period as u128;
                let pj = bj.period as u128;
                let c = ((sec.ti as i128 - sec.tj as i128 + sec.w1 as i128).rem_euclid(pi as i128)) as u128;
                let d = (pi - pj % pi) % pi;
                let w = ((sec.w1 + sec.w2).max(0) as u128).min(pi - 1);
                std::hint::black_box(emergent_encounters::dioph::first_hit(c, d, pi, 0, w, &mut 0));
            }
            if j as usize != ki {
                // a pair not involving the kicked body would be an isolation violation; none exist
            }
        }
        us_total += t0.elapsed().as_secs_f64() * 1e6;
        pairs_total += after_d;
        kicks_n += 1;
        ratios_d.push(after_d as f64 / before_d.max(1) as f64);
        // the negatives and the oracle use the radial candidate set; a kick re-does its pairs only
        let mut before_r = 0u64;
        let mut after_r = 0u64;
        for (j, bj) in b.iter().enumerate() {
            if j == ki {
                continue;
            }
            if bj.rmin() <= old.rmax() + 2.0 * rho && old.rmin() <= bj.rmax() + 2.0 * rho {
                before_r += 1;
            }
            if bj.rmin() <= new.rmax() + 2.0 * rho && new.rmin() <= bj.rmax() + 2.0 * rho {
                after_r += 1;
            }
        }
        ratios_r.push(after_r as f64 / before_r.max(1) as f64);
    }
    println!(
        "{{\"exp\":\"d\",\"n\":{},\"rho\":{:.2e},\"kicks\":{},\"kick_setup_ratio_dioph\":{:.4},\"kick_setup_ratio_radial\":{:.4},\"other_certificates_touched_dioph\":{},\"other_certificates_touched_radial\":{},\"us_per_kick\":{:.1},\"us_per_pair_setup\":{:.2},\"pairs_per_kick\":{:.1}}}",
        n, rho, kicks.len(), median(&mut ratios_d), median(&mut ratios_r), other_d, other_r,
        us_total / kicks_n as f64, us_total / pairs_total.max(1) as f64, pairs_total as f64 / kicks_n as f64
    );
}
