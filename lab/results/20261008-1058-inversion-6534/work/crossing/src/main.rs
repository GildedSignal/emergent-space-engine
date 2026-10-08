//! Inversion probe (20261008-1058): two concentrated coplanar lanes that cross.
//! Lane A: near-circular (a≈1, e~1e-4). Lane B: eccentric stream (a≈1.1, e≈0.12, coherent ϖ)
//! whose annulus crosses lane A. Every A×B orbit pair crosses ⇒ the cone tier cannot prune;
//! the group-envelope tier cannot separate crossing lanes; the phase-neighbour route
//! (same-orbit concentration) does not apply across orbits. What does tier 2 cost?
//!
//! Modes (one JSON per line): verify m | block m ab|aa|bb | cluster m | cone m

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::Body;
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{cone_pairs, is_candidate, radial_pairs, sections};
use emergent_encounters::truth::{truth_pair, TruthStats};
use emergent_encounters::par_chunks;
use std::f64::consts::TAU;
use std::time::Instant;

const RHO: f64 = 1e-3;
const SAFETY: f64 = 1.1;
const THREADS: usize = 4;
const ORBITS: f64 = 20.0;
const T_END: f64 = ORBITS * TAU;

type Enc = (u32, u32, f64, f64);

fn rayleigh(r: &mut Rng, s: f64) -> f64 {
    let u = r.f64();
    (s * (-2.0 * (1.0 - u).ln()).sqrt()).min(0.5)
}

/// A = indices [0,m), B = [m,2m).
fn lanes(m: usize) -> Vec<Body> {
    let mut ra = Rng(0x5EED_0001);
    let mut rb = Rng(0x5EED_0002);
    let mut b = Vec::with_capacity(2 * m);
    for _ in 0..m {
        let a = 1.0 + 2e-4 * ra.f64();
        let e = rayleigh(&mut ra, 1e-4);
        let pom = TAU * ra.f64();
        let lam = TAU * ra.f64();
        b.push(Body::new(a, e, pom, lam));
    }
    for _ in 0..m {
        let a = 1.1 + 2e-4 * rb.f64();
        let e = 0.12 + 1e-5 * (rb.f64() - 0.5);
        let pom = 0.04 * (rb.f64() - 0.5);
        let lam = TAU * rb.f64();
        b.push(Body::new(a, e, pom, lam));
    }
    b
}

fn block_pairs(m: usize, which: &str) -> Vec<(u32, u32)> {
    let mut v = Vec::new();
    match which {
        "ab" => {
            for i in 0..m {
                for j in m..2 * m {
                    v.push((i as u32, j as u32));
                }
            }
        }
        "aa" => {
            for i in 0..m {
                for j in i + 1..m {
                    v.push((i as u32, j as u32));
                }
            }
        }
        "bb" => {
            for i in m..2 * m {
                for j in i + 1..2 * m {
                    v.push((i as u32, j as u32));
                }
            }
        }
        _ => panic!("block: ab|aa|bb"),
    }
    v
}

fn method_all(b: &[Body], pairs: &[(u32, u32)]) -> (Vec<Enc>, Stats) {
    let parts = par_chunks(pairs.len(), 512, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &pairs[r] {
            tmp.clear();
            pair_events(&b[i as usize], &b[j as usize], RHO, SAFETY, 0.0, T_END, &mut st, &mut tmp);
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

fn truth_all(b: &[Body], pairs: &[(u32, u32)]) -> (Vec<Enc>, TruthStats) {
    let parts = par_chunks(pairs.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = TruthStats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &pairs[r] {
            tmp.clear();
            truth_pair(&b[i as usize], &b[j as usize], RHO, T_END, &mut tmp, &mut st);
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

/// missed (truth not matched), false (method not matched), matched, dup — same rule as the crate's.
fn matchup(truth: &[Enc], meth: &[Enc], tol: f64) -> (usize, usize, u64, u64) {
    let inside = |t: f64| t > 0.05 && t < T_END - 0.05;
    let mut by_pair: std::collections::HashMap<(u32, u32), Vec<f64>> = std::collections::HashMap::new();
    for e in meth.iter().filter(|e| inside(e.2)) {
        by_pair.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut tby: std::collections::HashMap<(u32, u32), Vec<f64>> = std::collections::HashMap::new();
    for e in truth.iter().filter(|e| inside(e.2)) {
        tby.entry((e.0, e.1)).or_default().push(e.2);
    }
    let mut missed = 0usize;
    let mut matched = 0u64;
    for e in truth.iter().filter(|e| inside(e.2)) {
        if by_pair.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < tol)) {
            matched += 1;
        } else {
            missed += 1;
        }
    }
    let mut false_ = 0usize;
    let mut dup = 0u64;
    let mut seen: std::collections::HashMap<(u32, u32, i64), u32> = std::collections::HashMap::new();
    for e in meth.iter().filter(|e| inside(e.2)) {
        match tby.get(&(e.0, e.1)).and_then(|v| v.iter().find(|&&t| (t - e.2).abs() < tol)) {
            None => false_ += 1,
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

/// sections() only, over up to `cap` pairs: (setup evals, sections by kind, pairs done).
fn setup_only(b: &[Body], pairs: &[(u32, u32)], cap: usize) -> (u64, [u64; 3], usize) {
    let n = pairs.len().min(cap);
    let parts = par_chunks(n, 4096, THREADS, |r| {
        let mut ev = 0u64;
        let mut kinds = [0u64; 3];
        for &(i, j) in &pairs[r] {
            for s in sections(&b[i as usize], &b[j as usize], RHO, SAFETY, &mut ev) {
                kinds[s.kind as usize] += 1;
            }
        }
        (ev, kinds)
    });
    let mut ev = 0u64;
    let mut kinds = [0u64; 3];
    for (e, k) in parts {
        ev += e;
        for t in 0..3 {
            kinds[t] += k[t];
        }
    }
    (ev, kinds, n)
}

fn wrap_pi(x: f64) -> f64 {
    let mut y = x.rem_euclid(TAU);
    if y > std::f64::consts::PI {
        y -= TAU;
    }
    y
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args[1].clone();
    let m: usize = args[2].parse().unwrap();
    match mode.as_str() {
        "verify" => {
            let t0 = Instant::now();
            let b = lanes(m);
            let pairs = block_pairs(m, "ab");
            let t1 = Instant::now();
            let (truth, tst) = truth_all(&b, &pairs);
            let truth_s = t1.elapsed().as_secs_f64();
            let t2 = Instant::now();
            let (meth, mst) = method_all(&b, &pairs);
            let meth_s = t2.elapsed().as_secs_f64();
            let (missed, false_, matched, dup) = matchup(&truth, &meth, 1e-3);
            let outside_cone = truth
                .iter()
                .filter(|e| !is_candidate(&b[e.0 as usize], &b[e.1 as usize], RHO))
                .count();
            println!(
                "{{\"exp\":\"verify\",\"m\":{},\"pairs\":{},\"truth_enc\":{},\"truth_steps\":{},\"truth_s\":{:.2},\"outside_cone\":{},\"method_enc\":{},\"matched\":{},\"missed\":{},\"false\":{},\"dup\":{},\"evals\":{},\"checks\":{},\"hits\":{},\"method_s\":{:.2},\"wall_s\":{:.2}}}",
                m, pairs.len(), truth.len(), tst.steps, truth_s, outside_cone, meth.len(), matched, missed, false_, dup, mst.evals, mst.checks_total(), mst.hits_total(), meth_s, t0.elapsed().as_secs_f64()
            );
        }
        "block" => {
            let which = args[3].clone();
            let t0 = Instant::now();
            let b = lanes(m);
            let pairs = block_pairs(m, &which);
            let (setup_ev, kinds, setup_n) = setup_only(&b, &pairs, 200_000);
            let t1 = Instant::now();
            let (meth, st) = method_all(&b, &pairs);
            let meth_s = t1.elapsed().as_secs_f64();
            let hits = meth.len() as f64;
            println!(
                "{{\"exp\":\"block\",\"block\":\"{}\",\"m\":{},\"pairs\":{},\"setup_n\":{},\"setup_evals\":{},\"setup_evals_per_pair\":{:.1},\"setup_kinds\":{:?},\"sections\":{:?},\"queries\":{},\"qsteps\":{},\"checks\":{},\"hits\":{},\"evals\":{},\"evals_per_pair\":{:.1},\"evals_per_hit\":{:.0},\"checks_per_hit\":{:.2},\"method_s\":{:.2},\"ns_per_pair\":{:.0},\"wall_s\":{:.2}}}",
                which, m, pairs.len(), setup_n, setup_ev, setup_ev as f64 / setup_n as f64, kinds, st.sections, st.queries, st.qsteps, st.checks_total(), st.hits_total(), st.evals, st.evals as f64 / pairs.len() as f64, st.evals as f64 / hits.max(1.0), st.checks_total() as f64 / hits.max(1.0), meth_s, meth_s * 1e9 / pairs.len() as f64, t0.elapsed().as_secs_f64()
            );
        }
        "cluster" => {
            let t0 = Instant::now();
            let b = lanes(m);
            let pairs = block_pairs(m, "ab");
            let (meth, st) = method_all(&b, &pairs);
            let meth_s = t0.elapsed().as_secs_f64();
            // crossing longitudes of the mean B orbit: r = p/(1+e cos) = 1
            let (pm, em) = (b[m].p, b[m].e);
            let c = ((pm - 1.0) / em).clamp(-1.0, 1.0);
            let ts = c.acos();
            let stars = [ts, -ts];
            let mut dmax: Vec<f64> = Vec::new();
            for e in &meth {
                if e.2 <= 0.05 || e.2 >= T_END - 0.05 {
                    continue;
                }
                let lon = |k: u32| {
                    let s = b[k as usize].state(e.2);
                    s[1].atan2(s[0])
                };
                let near = |k: u32| {
                    stars
                        .iter()
                        .map(|&s| wrap_pi(lon(k) - s).abs())
                        .fold(f64::INFINITY, f64::min)
                };
                dmax.push(near(e.0).max(near(e.1)));
            }
            dmax.sort_by(|x, y| x.total_cmp(y));
            let n = dmax.len();
            let q = |p: f64| dmax[((n as f64 - 1.0) * p) as usize];
            println!(
                "{{\"exp\":\"cluster\",\"m\":{},\"hits\":{},\"theta_star\":{:.4},\"d50\":{:.5},\"d90\":{:.5},\"d99\":{:.5},\"d_max\":{:.5},\"beyond_0p15\":{},\"evals\":{},\"method_s\":{:.2}}}",
                m, n, ts, q(0.5), q(0.9), q(0.99), dmax[n - 1], dmax.iter().filter(|&&x| x > 0.15).count(), st.evals, meth_s
            );
        }
        "cone" => {
            let b = lanes(m);
            let t0 = Instant::now();
            let rp = radial_pairs(&b, RHO);
            let radial_s = t0.elapsed().as_secs_f64();
            let t1 = Instant::now();
            let cs = cone_pairs(&b, RHO);
            let cone_s = t1.elapsed().as_secs_f64();
            let (mut aa, mut ab, mut bb) = (0u64, 0u64, 0u64);
            let (mut raa, mut rab) = (0u64, 0u64);
            for &(i, j) in &cs.pairs {
                match (i < m as u32, j < m as u32) {
                    (true, true) => aa += 1,
                    (false, false) => bb += 1,
                    _ => ab += 1,
                }
            }
            for &(i, j) in &rp {
                if i < m as u32 && j < m as u32 {
                    raa += 1;
                } else if i >= m as u32 && j >= m as u32 {
                } else {
                    rab += 1;
                }
            }
            println!(
                "{{\"exp\":\"cone\",\"m\":{},\"radial_pairs\":{},\"radial_aa\":{},\"radial_ab\":{},\"radial_s\":{:.3},\"cone_pairs\":{},\"cone_aa\":{},\"cone_ab\":{},\"cone_bb\":{},\"scanned\":{},\"cone_s\":{:.3}}}",
                m, rp.len(), raa, rab, radial_s, cs.pairs.len(), aa, ab, bb, cs.scanned, cone_s
            );
        }
        _ => panic!("verify|block|cluster|cone"),
    }
}
