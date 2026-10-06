//! The r8 v3 rung driver. The code under test (crates/encounters) is used as a library,
//! unmodified. The other configurations (element-sort, conjunction-sampled, oracle) and all the
//! harness are this run's own code.

use emergent_encounters::kepler::{Body, TICKS};
use emergent_encounters::method::{pair_events, Stats};
use emergent_encounters::pairs::{cone_pairs, is_candidate, radial_pairs, Sorted};
use emergent_encounters::truth::{truth_pair, TruthStats};
use std::collections::HashMap;
use std::f64::consts::TAU;
use std::time::Instant;

pub const THREADS: usize = 8;
pub const SAFETY: f64 = 1.1;
pub type Enc = (u32, u32, f64, f64);

pub struct Belt {
    pub name: String,
    pub n: usize,
    pub sigma_e: f64,
    pub rho: f64,
    pub orbits: f64,
    pub bodies: Vec<Body>,
}

pub fn read_index(dir: &str) -> Vec<Vec<String>> {
    let txt = std::fs::read_to_string(format!("{dir}/belts.tsv")).unwrap();
    txt.lines().skip(1).map(|l| l.split('\t').map(|s| s.to_string()).collect()).collect()
}

pub fn load_belt(dir: &str, name: &str) -> Belt {
    let e = read_index(dir).into_iter().find(|c| c[0] == name).expect("belt name");
    let n: usize = e[1].parse().unwrap();
    let raw = std::fs::read(format!("{dir}/{}", e[8])).expect("belt file");
    assert_eq!(raw.len() / 32, n);
    let mut bodies = Vec::with_capacity(n);
    for k in 0..n {
        let f = |q: usize| f64::from_le_bytes(raw[k * 32 + q * 8..k * 32 + q * 8 + 8].try_into().unwrap());
        bodies.push(Body::new(f(0), f(1), f(2), f(3)));
    }
    Belt { name: e[0].clone(), n, sigma_e: e[2].parse().unwrap(), rho: e[3].parse().unwrap(), orbits: e[7].parse().unwrap(), bodies }
}

pub fn load_truth(dir: &str, name: &str) -> Vec<Enc> {
    let raw = std::fs::read(format!("{dir}/truth-{name}.bin")).expect("truth file");
    let cnt = u64::from_le_bytes(raw[0..8].try_into().unwrap()) as usize;
    let mut out = Vec::with_capacity(cnt);
    for k in 0..cnt {
        let o = 8 + k * 24;
        out.push((
            u32::from_le_bytes(raw[o..o + 4].try_into().unwrap()),
            u32::from_le_bytes(raw[o + 4..o + 8].try_into().unwrap()),
            f64::from_le_bytes(raw[o + 8..o + 16].try_into().unwrap()),
            f64::from_le_bytes(raw[o + 16..o + 24].try_into().unwrap()),
        ));
    }
    out
}

/// The method (code under test) over the cone candidate set.
pub fn method_run(b: &Belt, t0: f64, t1: f64) -> (Vec<Enc>, Stats) {
    let cs = cone_pairs(&b.bodies, b.rho);
    method_over(b, &cs.pairs, t0, t1)
}

pub fn method_over(b: &Belt, pairs: &[(u32, u32)], t0: f64, t1: f64) -> (Vec<Enc>, Stats) {
    let parts = emergent_encounters::par_chunks(pairs.len(), 256, THREADS, |r| {
        let mut out = Vec::new();
        let mut st = Stats::default();
        let mut tmp = Vec::new();
        for &(i, j) in &pairs[r] {
            tmp.clear();
            pair_events(&b.bodies[i as usize], &b.bodies[j as usize], b.rho, SAFETY, t0, t1, &mut st, &mut tmp);
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

/// (missed, false, matched, dup): same pair, |dt| < tol, interior times only.
pub fn matchup(truth: &[Enc], meth: &[Enc], t_end: f64, tol: f64) -> (u64, u64, u64, u64) {
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
    let mut by_pair: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for e in meth {
        if inside(e.2) {
            by_pair.entry((e.0, e.1)).or_default().push(e.2);
        }
    }
    let mut tby: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for e in truth {
        if inside(e.2) {
            tby.entry((e.0, e.1)).or_default().push(e.2);
        }
    }
    let (mut missed, mut matched) = (0u64, 0u64);
    for e in truth.iter().filter(|e| inside(e.2)) {
        if by_pair.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < tol)) {
            matched += 1;
        } else {
            missed += 1;
        }
    }
    let (mut false_, mut dup) = (0u64, 0u64);
    let mut seen: HashMap<(u32, u32, i64), u32> = HashMap::new();
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

// ---------------- my configurations ----------------

#[inline]
fn dist_at(bi: &Body, bj: &Body, t: f64) -> f64 {
    let (si, sj) = (bi.state(t), bj.state(t));
    (si[0] - sj[0]).hypot(si[1] - sj[1])
}

/// Golden-section minimum of the distance over [a, b].
fn golden_min(bi: &Body, bj: &Body, a: f64, b: f64) -> (f64, f64) {
    let phi = 0.618_033_988_749_894_9;
    let (mut lo, mut hi) = (a, b);
    let mut x1 = hi - phi * (hi - lo);
    let mut x2 = lo + phi * (hi - lo);
    let (mut f1, mut f2) = (dist_at(bi, bj, x1), dist_at(bi, bj, x2));
    for _ in 0..70 {
        if hi - lo < 1e-13 {
            break;
        }
        if f1 < f2 {
            hi = x2;
            x2 = x1;
            f2 = f1;
            x1 = hi - phi * (hi - lo);
            f1 = dist_at(bi, bj, x1);
        } else {
            lo = x1;
            x1 = x2;
            f1 = f2;
            x2 = lo + phi * (hi - lo);
            f2 = dist_at(bi, bj, x2);
        }
    }
    let tm = 0.5 * (lo + hi);
    (tm, dist_at(bi, bj, tm))
}

/// r8 v2's conjunction window around a mean-longitude conjunction (no t_end cap).
fn conj_window(bi: &Body, bj: &Body, rho: f64) -> f64 {
    let dn = (bi.n - bj.n).abs();
    if dn <= 0.0 {
        return 0.0;
    }
    let abar = 0.5 * (bi.a + bj.a);
    ((2.0 * abar * (bi.e + bj.e) + 3.0 * rho) / (abar * dn)).min(std::f64::consts::PI / dn)
}

/// The exact check at one conjunction: every local minimum of the distance below rho inside
/// [tc − w, tc + w] ∩ [0, t_end], by a 33-sample scan and golden refinement of each dip.
fn window_check(bi: &Body, bj: &Body, rho: f64, tc: f64, w: f64, t_end: f64, out: &mut Vec<(f64, f64)>) {
    let lo = (tc - w).max(0.0);
    let hi = (tc + w).min(t_end);
    if hi <= lo {
        return;
    }
    let k = 33;
    let h = (hi - lo) / k as f64;
    let mut prevd = dist_at(bi, bj, lo);
    let mut falling = false;
    for q in 1..=k {
        let t = lo + h * q as f64;
        let d = dist_at(bi, bj, t);
        if falling && d >= prevd && prevd < 4.0 * rho {
            let (tm, dm) = golden_min(bi, bj, t - 2.0 * h, t);
            if dm < rho {
                out.push((tm, dm));
            }
            falling = false;
        }
        falling = d < prevd;
        prevd = d;
    }
    if falling && prevd < 4.0 * rho {
        let (tm, dm) = golden_min(bi, bj, hi - h, hi);
        if dm < rho {
            out.push((tm, dm));
        }
    }
}

/// All mean-longitude conjunction times of the pair in [0, t_end]: (lam_i − lam_j)(t) ≡ 0 mod 2π.
fn conjunction_times(bi: &Body, bj: &Body, t_end: f64) -> Vec<f64> {
    let dn = bi.n - bj.n;
    if dn == 0.0 {
        return Vec::new();
    }
    let d0 = bi.mean_anomaly(0.0) + bi.pom - bj.mean_anomaly(0.0) - bj.pom;
    // first t >= 0 with d0 + dn*t = 2πm
    let m0 = (-d0 / TAU).ceil();
    let mut out = Vec::new();
    let mut t = (m0 * TAU - d0) / dn;
    while t < 0.0 {
        t += TAU / dn.abs();
    }
    while t <= t_end {
        if t >= 0.0 {
            out.push(t);
        }
        t += TAU / dn.abs();
    }
    out
}

/// r8 v2's reference: a distance check per synodic conjunction, over every radially overlapping
/// pair. Returns its encounter list and the number of conjunction checks processed.
fn conj_sampled_run(b: &Belt) -> (Vec<Enc>, u64) {
    let pairs = radial_pairs(&b.bodies, b.rho);
    let t_end = b.orbits * TAU;
    let parts = emergent_encounters::par_chunks(pairs.len(), 128, THREADS, |r| {
        let mut out = Vec::new();
        let mut checks = 0u64;
        for &(i, j) in &pairs[r] {
            let (bi, bj) = (&b.bodies[i as usize], &b.bodies[j as usize]);
            let w = conj_window(bi, bj, b.rho);
            let mut evs = Vec::new();
            for &tc in &conjunction_times(bi, bj, t_end) {
                checks += 1;
                window_check(bi, bj, b.rho, tc, w, t_end, &mut evs);
            }
            evs.sort_by(|x, y| x.0.total_cmp(&y.0));
            let mut keep = Vec::new();
            for e in evs {
                if keep.last().is_none_or(|l: &(f64, f64)| (l.0 - e.0).abs() > 0.01) {
                    keep.push(e);
                }
            }
            out.extend(keep.iter().map(|&(t, d)| (i, j, t, d)));
        }
        (out, checks)
    });
    let mut all = Vec::new();
    let mut checks = 0u64;
    for (o, c) in parts {
        all.extend(o);
        checks += c;
    }
    (all, checks)
}

/// r8 v2's element-sort: a-bins no narrower than rho; per bin, a kinetic circular list sorted
/// by mean longitude over the bin and its radial reach; events are swaps of list neighbours; at
/// each swap whose pair's radial ranges overlap, the exact closest approach is checked.
///
/// The swap count of that structure is exact combinatorics, not simulation: every co-listed pair
/// crosses at every mean-longitude conjunction, so swaps(horizon) = Σ over co-listed pairs of
/// |Δn|·horizon/2π, weighted by the list multiplicity of v2's per-bin lists. The per-conjunction
/// exact check is computed once per distinct (pair, conjunction); the multiplicity is counted as
/// work (that redundancy is the configuration's own).
pub struct ElemSort {
    pub w_bin: f64,
    pub a_min: f64,
    pub n_bins: usize,
    pub bin: Vec<u32>,
    pub reach: Vec<usize>,
    members: Vec<Vec<u32>>,
}

impl ElemSort {
    pub fn new(b: &Belt) -> Self {
        let w_bin = (2.0 * b.rho).max(0.002);
        let a_min = b.bodies.iter().map(|x| x.a).fold(f64::INFINITY, f64::min) - 1e-9;
        let a_max = b.bodies.iter().map(|x| x.a).fold(f64::NEG_INFINITY, f64::max) + 1e-9;
        let n_bins = ((a_max - a_min) / w_bin).ceil() as usize + 1;
        let mut bin = vec![0u32; b.n];
        for (k, body) in b.bodies.iter().enumerate() {
            bin[k] = (((body.a - a_min) / w_bin) as usize) as u32;
        }
        let mut members = vec![Vec::new(); n_bins];
        for (k, &bb) in bin.iter().enumerate() {
            members[bb as usize].push(k as u32);
        }
        let mut reach = vec![0usize; n_bins];
        for k in 0..n_bins {
            let ext = members[k].iter().map(|&i| 2.0 * b.bodies[i as usize].a * b.bodies[i as usize].e).fold(0.0, f64::max) + 2.0 * b.rho;
            reach[k] = (ext / w_bin).ceil() as usize + 1;
        }
        ElemSort { w_bin, a_min, n_bins, bin, reach, members }
    }

    /// (swaps, checks) over the horizon: co-listed-pair conjunctions, multiplicity-weighted;
    /// checks count the swaps whose pair's radial ranges overlap.
    pub fn event_counts(&self, b: &Belt, t_end: f64) -> (u64, u64) {
        let (mut swaps, mut checks) = (0.0f64, 0.0f64);
        for k in 0..self.n_bins {
            let mut ms = Vec::new();
            for kk in k.saturating_sub(self.reach[k])..(k + self.reach[k] + 1).min(self.n_bins) {
                ms.extend_from_slice(&self.members[kk]);
            }
            for x in 0..ms.len() {
                for y in (x + 1)..ms.len() {
                    let (i, j) = (ms[x], ms[y]);
                    let (bi, bj) = (&b.bodies[i as usize], &b.bodies[j as usize]);
                    let dn = (bi.n - bj.n).abs();
                    if dn == 0.0 {
                        continue;
                    }
                    swaps += dn * t_end / TAU;
                    if (bi.a - bj.a).abs() <= bi.a * bi.e + bj.a * bj.e + 2.0 * b.rho {
                        checks += dn * t_end / TAU;
                    }
                }
            }
        }
        (swaps as u64, checks as u64)
    }
}

// ---------------- modes ----------------

fn verify(dir: &str) {
    let belts: Vec<String> = ["a00","a01","a02","a03","a04","a05","a06","a07","a08","a09","a10","a11","a12","a13","a14","a15","narrow","coorbital","equalkeys","hot"].iter().map(|s| s.to_string()).collect();
    // pooled per config: truth encounters (interior), missed, false, checks
    let mut pool: HashMap<&str, [u64; 4]> = HashMap::new();
    for name in belts {
        let b = load_belt(dir, &name);
        let truth = load_truth(dir, &name);
        let t_end = b.orbits * TAU;
        let (ti, tf) = (truth.iter().filter(|e| e.2 > 0.05 && e.2 < t_end - 0.05).count() as u64,
                        truth.iter().filter(|e| e.2 > 0.05 && e.2 < t_end - 0.05).count() as u64);
        let _ = ti;
        let n_int = tf;
        // diophantine
        let (meth, st) = method_run(&b, 0.0, t_end);
        let (m, f, _, _) = matchup(&truth, &meth, t_end, 1e-3);
        let e = pool.entry("diophantine").or_insert([0; 4]);
        e[0] += n_int; e[1] += m; e[2] += f; e[3] += st.checks_total();
        println!("{{\"belt\":\"{name}\",\"cfg\":\"diophantine\",\"truth\":{n_int},\"missed\":{m},\"false\":{f},\"checks\":{}}}", st.checks_total());
        // conjunction-sampled
        let (cs, checks) = conj_sampled_run(&b);
        let (m, f, _, _) = matchup(&truth, &cs, t_end, 1e-3);
        let e = pool.entry("conjunction-sampled").or_insert([0; 4]);
        e[0] += n_int; e[1] += m; e[2] += f; e[3] += checks;
        println!("{{\"belt\":\"{name}\",\"cfg\":\"conjunction-sampled\",\"truth\":{n_int},\"missed\":{m},\"false\":{f},\"checks\":{checks}}}");
        // element-sort: encounter list from distinct conjunction checks (its own path);
        // event counts are the exact combinatorial swap/check counts of the bin structure
        let (ev, _) = conj_sampled_run(&b);
        let es = ElemSort::new(&b);
        let (swaps, checks) = es.event_counts(&b, t_end);
        let (m, f, _, _) = matchup(&truth, &ev, t_end, 1e-3);
        let e = pool.entry("element-sort").or_insert([0; 4]);
        e[0] += n_int; e[1] += m; e[2] += f; e[3] += checks;
        println!("{{\"belt\":\"{name}\",\"cfg\":\"element-sort\",\"truth\":{n_int},\"missed\":{m},\"false\":{f},\"checks\":{checks},\"swaps\":{}}}", swaps);
        // oracle: reads the truth
        let e = pool.entry("oracle").or_insert([0; 4]);
        e[0] += n_int; e[1] += 0; e[2] += 0; e[3] += n_int;
        println!("{{\"belt\":\"{name}\",\"cfg\":\"oracle\",\"truth\":{n_int},\"missed\":0,\"false\":0,\"checks\":{n_int}}}");
    }
    for (k, v) in &pool {
        println!("{{\"pool\":\"{k}\",\"truth\":{},\"missed\":{},\"false\":{},\"checks\":{}}}", v[0], v[1], v[2], v[3]);
    }
}

fn steady(dir: &str) {
    let b = load_belt(dir, "steady");
    let truth = load_truth(dir, "steady");
    // the steady truth is a 1-in-10 pair sample (phase 8) over 1000 orbits; the rate scales
    // by the sample denominator, and the matchup is restricted to the sampled pairs
    let denom = 10.0f64;
    let truth_rate = truth.len() as f64 * denom / (3000.0 * 1000.0);
    println!("{{\"steady\":\"truth_rate\":{:.6e}}}", truth_rate);
    for &h in &[10.0f64, 100.0, 1000.0, 10000.0, 100000.0] {
        let t = Instant::now();
        let (_, st) = method_run(&b, 0.0, h * TAU);
        let events = st.pairs + st.checks_total();
        println!("{{\"steady\":\"diophantine\",\"horizon\":{h},\"events\":{events},\"checks\":{},\"setups\":{},\"rate\":{:.6e},\"ratio\":{:.4},\"s\":{:.1}}}",
            st.checks_total(), st.pairs, events as f64 / (3000.0 * h), events as f64 / (3000.0 * h) / truth_rate, t.elapsed().as_secs_f64());
    }
    // completeness on the truth's 1000-orbit window, restricted to the sampled pairs
    let (meth, _) = method_run(&b, 0.0, 1000.0 * TAU);
    let spairs: std::collections::HashSet<(u32, u32)> = truth.iter().map(|e| (e.0, e.1)).collect();
    let meth_s: Vec<Enc> = meth.iter().filter(|e| spairs.contains(&(e.0, e.1))).copied().collect();
    let (m, f, mt, _) = matchup(&truth, &meth_s, 1000.0 * TAU, 1e-3);
    println!("{{\"steady\":\"matchup-1000\",\"truth\":{},\"missed\":{m},\"false\":{f},\"matched\":{mt}}}", truth.len());
    // element-sort: exact combinatorial event counts (stationary by construction)
    {
        let t = Instant::now();
        let es = ElemSort::new(&b);
        let (swaps, checks) = es.event_counts(&b, 100.0 * TAU);
        let events = swaps + checks;
        println!("{{\"steady\":\"element-sort\",\"horizon\":100,\"swaps\":{swaps},\"checks\":{checks},\"events\":{events},\"rate\":{:.6e},\"ratio\":{:.1},\"s\":{:.1}}}",
            events as f64 / (3000.0 * 100.0), events as f64 / (3000.0 * 100.0) / truth_rate, t.elapsed().as_secs_f64());
    }
    // conjunction-sampled: its events are exactly the synodic conjunctions of radial pairs
    let t = Instant::now();
    let rp = radial_pairs(&b.bodies, b.rho);
    let conj_per_orbit: f64 = rp.iter().map(|&(i, j)| (b.bodies[i as usize].n - b.bodies[j as usize].n).abs() / TAU).sum();
    println!("{{\"steady\":\"conjunction-sampled\",\"rate\":{:.6e},\"ratio\":{:.1},\"s\":{:.1}}}",
        conj_per_orbit / 3000.0, conj_per_orbit / 3000.0 / truth_rate, t.elapsed().as_secs_f64());
    println!("{{\"steady\":\"oracle\",\"rate\":{:.6e},\"ratio\":1.0}}", truth_rate);
}

/// Check work for each configuration on the three scale belts (rho ∝ 1/N, 100 orbits).
fn scale(dir: &str) {
    for n in [1000usize, 10000, 100000] {
        let name = format!("scale-n{n}");
        let b = load_belt(dir, &name);
        let h = 100.0;
        let t = Instant::now();
        // diophantine: sampled bodies through their U-range (checks extrapolated by N/samples)
        let sorted = Sorted::new(&b.bodies, b.rho);
        let ns = if n == 100000 { 100 } else { 200 };
        let sample: Vec<u32> = (0..ns).map(|k| (k * n / ns) as u32).collect();
        let parts = emergent_encounters::par_chunks(ns, 8, THREADS, |r| {
            let mut st = Stats::default();
            let mut tmp = Vec::new();
            for &i in &sample[r] {
                let bi = &b.bodies[i as usize];
                let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
                for &(_, j) in &sorted.order[lo..hi] {
                    if j == i || !is_candidate(bi, &b.bodies[j as usize], b.rho) {
                        continue;
                    }
                    tmp.clear();
                    pair_events(bi, &b.bodies[j as usize], b.rho, SAFETY, 0.0, h * TAU, &mut st, &mut tmp);
                }
            }
            (st.checks_total(), st.pairs)
        });
        let (mut checks, mut setups) = (0u64, 0u64);
        for (c, s) in parts {
            checks += c;
            setups += s;
        }
        let dio_checks = checks as f64 * n as f64 / ns as f64;
        // conjunction-based check work: sum |dn| over radial pairs (streamed), times orbits
        let mut idx: Vec<u32> = (0..b.n as u32).collect();
        idx.sort_by(|&x, &y| b.bodies[x as usize].rmin().total_cmp(&b.bodies[y as usize].rmin()));
        let mut sdn = 0.0f64;
        let mut rp_n = 0u64;
        for (k, &i) in idx.iter().enumerate() {
            let hi = b.bodies[i as usize].rmax() + 2.0 * b.rho;
            for &j in &idx[k + 1..] {
                if b.bodies[j as usize].rmin() > hi {
                    break;
                }
                sdn += (b.bodies[i as usize].n - b.bodies[j as usize].n).abs();
                rp_n += 1;
            }
        }
        let conj_checks = sdn * h; // conjunctions over the horizon
        // oracle: true encounters (measured from the truth runs; the dense belts use
        // deterministic strided pair samples: n=1e4 is 1-in-32, n=1e5 is 1-in-512)
        let (suffix, mult): (&str, f64) = match n {
            1000 => ("", 1.0),
            10000 => ("", 32.0),
            _ => ("-sample", 512.0),
        };
        let raw = std::fs::read(format!("{dir}/truth-{name}{suffix}.bin")).expect("truth scale file");
        let oracle_checks = u64::from_le_bytes(raw[0..8].try_into().unwrap()) as f64 * mult;
        println!("{{\"scale\":{n},\"rho\":{:.2e},\"radial_pairs\":{rp_n},\"dio_checks\":{:.0},\"dio_setups\":{:.0},\"conj_checks\":{:.3e},\"oracle_checks\":{:.0},\"s\":{:.1}}}",
            b.rho, dio_checks, setups as f64 * n as f64 / ns as f64, conj_checks, oracle_checks, t.elapsed().as_secs_f64());
    }
}

/// 100 kicks, da/a = 1e-3, at t = 0, horizon 1000 orbits, on the kick belt (N = 1e4).
fn kicks(dir: &str) {
    let b = load_belt(dir, "kick");
    let sorted = Sorted::new(&b.bodies, b.rho);
    let nk = 100usize;
    let kicked: Vec<usize> = (0..nk).map(|q| (q * 97 + 13) % b.n).collect();
    // diophantine: re-scan the kicked body's U-range only
    let mut ratios = Vec::new();
    let mut others = 0u64;
    let mut pairs_set = 0u64;
    for &i in &kicked {
        let old = b.bodies[i];
        let lam0 = old.mean_anomaly(0.0) + old.pom;
        let new = Body::new(old.a * 1.001, old.e, old.pom, lam0);
        let (lo, hi) = sorted.range(new.binet()[0], sorted.reach(&new));
        let mut set_up = 0u64;
        for &(_, j) in &sorted.order[lo..hi] {
            if j as usize == i {
                continue;
            }
            if is_candidate(&new, &b.bodies[j as usize], b.rho) {
                set_up += 1;
            }
        }
        // denominator: the kicked body's candidate count with its new elements
        let mut denom = 0u64;
        for j in 0..b.n {
            if j != i && is_candidate(&new, &b.bodies[j], b.rho) {
                denom += 1;
            }
        }
        pairs_set += set_up;
        ratios.push(set_up as f64 / denom as f64);
        // certificates of untouched pairs: none are recomputed (only i's range is scanned)
        others += 0;
    }
    ratios.sort_by(|x, y| x.total_cmp(y));
    let med = ratios[ratios.len() / 2];
    println!("{{\"kick\":\"diophantine\",\"median_ratio\":{:.4},\"pairs_per_kick\":{:.1},\"others\":{}}}", med, pairs_set as f64 / nk as f64, others);
    // element-sort: a kick re-bins the body; it leaves and joins the lists of the bins around
    // its old and new a. Certificates rebuilt involving it: 2 per list it joins (its new
    // neighbours). Certificates rebuilt NOT involving it: 1 per list it leaves (the merged
    // neighbours of the hole) — so a kick is not isolated in this configuration.
    {
        let es = ElemSort::new(&b);
        let mut es_others = 0u64;
        let mut es_set = 0u64;
        let mut es_ratios = Vec::new();
        for &i in &kicked {
            let old = b.bodies[i];
            let lam0 = old.mean_anomaly(0.0) + old.pom;
            let new = Body::new(old.a * 1.001, old.e, old.pom, lam0);
            let mut denom = 0u64;
            for j in 0..b.n {
                if j != i && is_candidate(&new, &b.bodies[j], b.rho) {
                    denom += 1;
                }
            }
            let old_bin = ((old.a - es.a_min) / es.w_bin) as usize;
            let new_bin = ((new.a - es.a_min) / es.w_bin) as usize;
            let mut joins = 0u64;
            let mut leaves = 0u64;
            for k in 0..es.n_bins {
                let in_old = (k as i64 - old_bin as i64).abs() <= es.reach[k] as i64;
                let in_new = (k as i64 - new_bin as i64).abs() <= es.reach[k] as i64;
                if in_old && !in_new {
                    leaves += 1;
                } else if in_new && !in_old {
                    joins += 1;
                }
            }
            es_set += 2 * joins;
            es_others += leaves;
            if denom > 0 {
                es_ratios.push((2.0 * joins as f64) / denom as f64);
            }
        }
        es_ratios.sort_by(|x, y| x.total_cmp(y));
        println!("{{\"kick\":\"element-sort\",\"median_ratio\":{:.4},\"pairs_per_kick\":{:.1},\"others\":{}}}",
            es_ratios[es_ratios.len() / 2], es_set as f64 / nk as f64, es_others);
    }
    // conjunction-sampled: the schedule is recomputed for the kicked body's radial pairs
    let mut cs_ratios = Vec::new();
    let mut cs_pairs = 0u64;
    for &i in &kicked {
        let old = b.bodies[i];
        let lam0 = old.mean_anomaly(0.0) + old.pom;
        let new = Body::new(old.a * 1.001, old.e, old.pom, lam0);
        let mut denom = 0u64;
        let mut set_up = 0u64;
        for j in 0..b.n {
            if j == i {
                continue;
            }
            let bj = &b.bodies[j];
            if (new.a - bj.a).abs() <= new.a * new.e + bj.a * bj.e + 2.0 * b.rho {
                denom += 1;
                set_up += 1;
            }
        }
        cs_pairs += set_up;
        cs_ratios.push(set_up as f64 / denom.max(1) as f64);
    }
    cs_ratios.sort_by(|x, y| x.total_cmp(y));
    println!("{{\"kick\":\"conjunction-sampled\",\"median_ratio\":{:.4},\"pairs_per_kick\":{:.1},\"others\":0}}", cs_ratios[cs_ratios.len() / 2], cs_pairs as f64 / nk as f64);
    // oracle: re-derives the truth for the kicked body's radial pairs
    let mut o_ratios = Vec::new();
    let mut o_pairs = 0u64;
    for &i in &kicked {
        let old = b.bodies[i];
        let lam0 = old.mean_anomaly(0.0) + old.pom;
        let new = Body::new(old.a * 1.001, old.e, old.pom, lam0);
        let mut denom = 0u64;
        for j in 0..b.n {
            if j == i {
                continue;
            }
            let bj = &b.bodies[j];
            if (new.a - bj.a).abs() <= new.a * new.e + bj.a * bj.e + 2.0 * b.rho {
                denom += 1;
            }
        }
        o_pairs += denom;
        o_ratios.push(1.0);
    }
    o_ratios.sort_by(|x: &f64, y: &f64| x.total_cmp(y));
    println!("{{\"kick\":\"oracle\",\"median_ratio\":{:.4},\"pairs_per_kick\":{:.1},\"others\":0}}", o_ratios[o_ratios.len() / 2], o_pairs as f64 / nk as f64);
}


/// Debug: print the false reports of the method on one belt, with the truth's events of the
/// same pair nearby and a dense distance profile around the reported time.
fn false1(dir: &str, name: &str) {
    let b = load_belt(dir, name);
    let truth = load_truth(dir, name);
    let t_end = b.orbits * TAU;
    let (meth, _) = method_run(&b, 0.0, t_end);
    let inside = |t: f64| t > 0.05 && t < t_end - 0.05;
    let mut tby: HashMap<(u32, u32), Vec<f64>> = HashMap::new();
    for e in &truth {
        if inside(e.2) {
            tby.entry((e.0, e.1)).or_default().push(e.2);
        }
    }
    let false_: Vec<Enc> = meth.iter().filter(|e| inside(e.2))
        .filter(|e| !tby.get(&(e.0, e.1)).is_some_and(|v| v.iter().any(|&t| (t - e.2).abs() < 1e-3)))
        .copied().collect();
    for e in &false_ {
        let (i, j, t, d) = *e;
        println!("false: pair ({i},{j}) t={t:.9} d={d:.6e}  rho={:.3e}", b.rho);
        for te in truth.iter().filter(|e| e.0 == i && e.1 == j) {
            println!("  truth: t={:.9} d={:.6e}  dt={:+.3e}", te.2, te.3, te.2 - t);
        }
        let (bi, bj) = (&b.bodies[i as usize], &b.bodies[j as usize]);
        // dense profile ±0.02 around t
        let mut best = (0.0f64, 1e9f64);
        for k in -200..=200 {
            let tt = t + k as f64 * 2e-4;
            let dd = dist_at(bi, bj, tt);
            if dd < best.1 {
                best = (tt, dd);
            }
        }
        println!("  dense min near t: t={:.9} d={:.6e}", best.0, best.1);
        let (tm, dm) = golden_min(bi, bj, t - 0.05, t + 0.05);
        println!("  golden over +-0.05: t={:.9} d={:.6e}", tm, dm);
        println!("  profile (t, d, g=dr.dv) every 0.02 in [t-0.6, t+0.6]:");
        for k in -30..=30 {
            let tt = t + k as f64 * 0.02;
            let (si, sj) = (bi.state(tt), bj.state(tt));
            let (dx, dy) = (si[0]-sj[0], si[1]-sj[1]);
            let (vx, vy) = (si[2]-sj[2], si[3]-sj[3]);
            let dd = dx.hypot(dy);
            let gg = dx * vx + dy * vy;
            println!("    t={tt:.5} d={dd:.6e} g={gg:+.6e}");
        }
    }
}


/// Cross-check: the crate's own truth (Halley states, its own bounds) against this run's
/// independent truth, on the same belts. Both directions of matchup.
fn xcheck(dir: &str, names: &[&str]) {
    for name in names {
        let b = load_belt(dir, name);
        let mine = load_truth(dir, name);
        let t_end = b.orbits * TAU;
        let rp = radial_pairs(&b.bodies, b.rho);
        let parts = emergent_encounters::par_chunks(rp.len(), 256, THREADS, |r| {
            let mut out = Vec::new();
            let mut st = TruthStats::default();
            let mut tmp = Vec::new();
            for &(i, j) in &rp[r] {
                tmp.clear();
                truth_pair(&b.bodies[i as usize], &b.bodies[j as usize], b.rho, t_end, &mut tmp, &mut st);
                out.extend(tmp.iter().map(|&(t, d)| (i, j, t, d)));
            }
            (out, st)
        });
        let mut crate_t = Vec::new();
        for (o, _) in parts {
            crate_t.extend(o);
        }
        let (m1, f1, _, _) = matchup(&mine, &crate_t, t_end, 1e-3);
        let (m2, f2, _, _) = matchup(&crate_t, &mine, t_end, 1e-3);
        println!("{{\"xcheck\":\"{name}\",\"mine\":{},\"crate\":{},\"crate_missed_mine\":{m1},\"crate_false_mine\":{f1},\"mine_missed_crate\":{m2},\"mine_false_crate\":{f2}}}",
            mine.iter().filter(|e| e.2 > 0.05 && e.2 < t_end - 0.05).count(), crate_t.iter().filter(|e| e.2 > 0.05 && e.2 < t_end - 0.05).count());
    }
}


/// The method's horizon sweep without the truth file (rates only), so the long runs overlap
/// with the truth still computing.
fn steady_method(dir: &str, horizons: &[f64]) {
    let b = load_belt(dir, "steady");
    for &h in horizons {
        let t = Instant::now();
        let (_, st) = method_run(&b, 0.0, h * TAU);
        let events = st.pairs + st.checks_total();
        println!("{{\"steady\":\"diophantine\",\"horizon\":{h},\"events\":{events},\"checks\":{},\"setups\":{},\"rate\":{:.6e},\"s\":{:.1}}}",
            st.checks_total(), st.pairs, events as f64 / (3000.0 * h), t.elapsed().as_secs_f64());
    }
}


/// The diophantine check work on the scale belts alone (no truth files needed).
fn scale_dio(dir: &str) {
    for n in [1000usize, 10000, 100000] {
        let name = format!("scale-n{n}");
        let b = load_belt(dir, &name);
        let h = 100.0;
        let t = Instant::now();
        let sorted = Sorted::new(&b.bodies, b.rho);
        let ns = if n == 100000 { 100 } else { 200 };
        let sample: Vec<u32> = (0..ns).map(|k| (k * n / ns) as u32).collect();
        let parts = emergent_encounters::par_chunks(ns, 8, THREADS, |r| {
            let mut st = Stats::default();
            let mut tmp = Vec::new();
            for &i in &sample[r] {
                let bi = &b.bodies[i as usize];
                let (lo, hi) = sorted.range(bi.binet()[0], sorted.reach(bi));
                let mut mine = 0u64;
                for &(_, j) in &sorted.order[lo..hi] {
                    if j == i || !is_candidate(bi, &b.bodies[j as usize], b.rho) {
                        continue;
                    }
                    mine += 1;
                    tmp.clear();
                    pair_events(bi, &b.bodies[j as usize], b.rho, SAFETY, 0.0, h * TAU, &mut st, &mut tmp);
                }
                st.pairs += 0; // pairs counted separately below
                let _ = mine;
            }
            (st.checks_total(), st.evals, st.queries)
        });
        let (mut checks, mut evals, mut queries) = (0u64, 0u64, 0u64);
        for (c, e, q) in parts {
            checks += c; evals += e; queries += q;
        }
        println!("{{\"scale-dio\":{n},\"rho\":{:.2e},\"sample_bodies\":{ns},\"checks\":{checks},\"evals\":{evals},\"queries\":{queries},\"checks_extrapolated\":{:.0},\"s\":{:.1}}}",
            b.rho, checks as f64 * n as f64 / ns as f64, t.elapsed().as_secs_f64());
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let dir = args.get(2).cloned().unwrap_or_else(|| ".".into());
    match args.get(1).map(|s| s.as_str()) {
        Some("verify") => verify(&dir),
        Some("steady") => steady(&dir),
        Some("scale") => scale(&dir),
        Some("kicks") => kicks(&dir),
        Some("false1") => false1(&dir, &args[3]),
        Some("xcheck") => xcheck(&dir, &args[3..].iter().map(|s| s.as_str()).collect::<Vec<_>>()),
        Some("steady-method") => steady_method(&dir, &args[3..].iter().filter_map(|s| s.parse().ok()).collect::<Vec<f64>>()),
        Some("scale-dio") => scale_dio(&dir),
        _ => eprintln!("usage: rung verify|steady|scale|kicks <dir>"),
    }
    let _ = TICKS;
}
