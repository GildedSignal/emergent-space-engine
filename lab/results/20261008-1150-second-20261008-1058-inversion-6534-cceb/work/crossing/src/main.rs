//! Inversion probe (20261008-1058): two concentrated coplanar lanes that cross.
//! Lane A: near-circular (a≈1, e~1e-4). Lane B: eccentric stream (a≈1.1, e≈0.12, coherent ϖ)
//! whose annulus crosses lane A. Every A×B orbit pair crosses ⇒ the cone tier cannot prune;
//! the group-envelope tier cannot separate crossing lanes; the phase-neighbour route
//! (same-orbit concentration) does not apply across orbits. What does tier 2 cost?
//!
//! Modes (one JSON per line): verify m | block m ab|aa|bb | cluster m | cone m

use emergent_encounters::belt::Rng;
use emergent_encounters::kepler::{Body, TICKS};
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
        "xcorr" => {
            // Corridor attribution, in longitude and in time, over method encounters
            // on the full A×B product: distance to the shared star (the published
            // invariant) vs distance to each B body's own crossing, and the passage-time
            // mismatch |t_A(theta_k) - t_B(theta_k)| the rank certificate windows on.
            let scene = args[3].clone();
            let e_b = scene_eb(&scene);
            let t0 = Instant::now();
            let b = lanes_scene(m, e_b);
            let g = scene_geo(&b, m);
            let pairs = block_pairs(m, "ab");
            let (meth, st) = method_all(&b, &pairs);
            let meth_s = t0.elapsed().as_secs_f64();
            let stars = [g.ts, -g.ts];
            let (mut dm, mut dob, mut doa, mut dt) = (Vec::new(), Vec::new(), Vec::new(), Vec::new());
            for e in &meth {
                if e.2 <= 0.05 || e.2 >= T_END - 0.05 {
                    continue;
                }
                let lon = |k: u32| {
                    let s = b[k as usize].state(e.2);
                    s[1].atan2(s[0])
                };
                let (la, lb) = (lon(e.0), lon(e.1));
                let near = |l: f64| stars.iter().map(|&s| wrap_pi(l - s).abs()).fold(f64::INFINITY, f64::min);
                dm.push(near(la).max(near(lb)));
                let bk = &b[e.1 as usize];
                let tp = own_crossing(bk, 1.0, 1.0).0;
                let tm = own_crossing(bk, 1.0, -1.0).0;
                let th = if wrap_pi(lb - tp).abs() < wrap_pi(lb - tm).abs() { tp } else { tm };
                dob.push(wrap_pi(lb - th).abs());
                doa.push(wrap_pi(la - th).abs());
                dt.push((nearest_passage(&b[e.0 as usize], th, e.2)
                    - nearest_passage(bk, th, e.2))
                    .abs());
            }
            let (a50, a90, a99, amax) = q4(&mut dm);
            let (b50, b90, b99, bmax) = q4(&mut dob);
            let (c50, c90, c99, cmax) = q4(&mut doa);
            let (d50, d90, d99, dmax) = q4(&mut dt);
            println!(
                "{{\"exp\":\"xcorr\",\"scene\":\"{}\",\"m\":{},\"hits\":{},\"spread\":{:.5},\"sin_g\":{:.5},\"rho_over_sing\":{:.5},\"dmean_50\":{:.5},\"dmean_90\":{:.5},\"dmean_99\":{:.5},\"dmean_max\":{:.5},\"dmean_beyond_0p15\":{},\"downb_50\":{:.5},\"downb_90\":{:.5},\"downb_99\":{:.5},\"downb_max\":{:.5},\"downa_50\":{:.5},\"downa_90\":{:.5},\"downa_99\":{:.5},\"downa_max\":{:.5},\"dt_50\":{:.5},\"dt_90\":{:.5},\"dt_99\":{:.5},\"dt_max\":{:.5},\"evals\":{},\"method_s\":{:.2},\"wall_s\":{:.2}}}",
                scene, m, dm.len(), g.spread, g.sin_g, RHO / g.sin_g,
                a50, a90, a99, amax, dm.iter().filter(|&&x| x > 0.15).count(),
                b50, b90, b99, bmax, c50, c90, c99, cmax, d50, d90, d99, dmax,
                st.evals, meth_s, t0.elapsed().as_secs_f64()
            );
        }
        "xcert" => {
            // The exit, built: candidate pairs from the crossing-time rank, exact checks
            // only there, zero-miss vs truth over the full product (truth = 1).
            let variant = args[3].clone();
            let scene = args[4].clone();
            let want_truth: bool = args[5].parse().unwrap();
            let e_b = scene_eb(&scene);
            let t0 = Instant::now();
            let b = lanes_scene(m, e_b);
            let g = scene_geo(&b, m);
            let (pairs, raw_n, s_min, s_max, s_mean, gen_s) = xcert_pairs(&b, m, &variant, &g);
            let t1 = Instant::now();
            let (meth, mst) = method_all(&b, &pairs);
            let check_s = t1.elapsed().as_secs_f64();
            let inside = |t: f64| t > 0.05 && t < T_END - 0.05;
            let hits = meth.iter().filter(|e| inside(e.2)).count().max(1) as f64;
            let mut extra = String::new();
            if want_truth {
                let t2 = Instant::now();
                let all = block_pairs(m, "ab");
                let (truth, _tst) = truth_all(&b, &all);
                let truth_s = t2.elapsed().as_secs_f64();
                let (missed, false_, matched, dup) = matchup(&truth, &meth, 1e-3);
                let mut tp: Vec<(u32, u32)> = truth
                    .iter()
                    .filter(|e| inside(e.2))
                    .map(|e| (e.0, e.1))
                    .collect();
                tp.sort_unstable();
                tp.dedup();
                let mut cover = 0usize;
                for p in &tp {
                    if pairs.binary_search(p).is_ok() {
                        cover += 1;
                    }
                }
                extra = format!(
                    ",\"truth_enc\":{},\"truth_s\":{:.1},\"matched\":{},\"missed\":{},\"false\":{},\"dup\":{},\"truth_pairs\":{},\"truth_pairs_in_cert\":{},\"truth_pairs_missed\":{}",
                    truth.len(), truth_s, matched, missed, false_, dup, tp.len(), cover, tp.len() - cover
                );
            }
            println!(
                "{{\"exp\":\"xcert\",\"variant\":\"{}\",\"scene\":\"{}\",\"m\":{},\"spread\":{:.5},\"sin_g\":{:.5},\"da\":{:.2e},\"s_min\":{:.5},\"s_max\":{:.5},\"s_mean\":{:.5},\"raw_cand\":{},\"pairs\":{},\"pairs_per_hit\":{:.1},\"raw_per_hit\":{:.1},\"evals\":{},\"evals_per_hit\":{:.1},\"checks\":{},\"hits\":{},\"gen_s\":{:.2},\"check_s\":{:.2},\"us_per_hit\":{:.1},\"wall_s\":{:.2}{}}}",
                variant, scene, m, g.spread, g.sin_g, g.da, s_min, s_max, s_mean,
                raw_n, pairs.len(), pairs.len() as f64 / hits, raw_n as f64 / hits,
                mst.evals, mst.evals as f64 / hits, mst.checks_total(), hits as usize,
                gen_s, check_s, (gen_s + check_s) * 1e6 / hits, t0.elapsed().as_secs_f64(), extra
            );
        }
        _ => panic!("verify|block|cluster|cone|xcorr|xcert"),
    }
}

// ---------------------------------------------------------------------------
// Second author (20261008-1150): the exit the checker named — a crossing-time-rank
// certificate — plus the corridor measured in time (attribution), and incidence
// knobs (steep / near-tangent) as held-out scenes for the derived window rule.
// ---------------------------------------------------------------------------

/// Margin on every derived (never fitted) half-width.
const MARGIN: f64 = 1.5;

fn scene_eb(scene: &str) -> f64 {
    match scene {
        "frozen" => 0.12,
        "steep" => 0.35,
        "tangent" => 0.092,
        _ => panic!("scene: frozen|steep|tangent"),
    }
}

/// Same stream as `lanes` when e_b = 0.12 (identical draws); B's eccentricity is a knob.
fn lanes_scene(m: usize, e_b: f64) -> Vec<Body> {
    let mut ra = Rng(0x5EED_0001);
    let mut rb = Rng(0x5EED_0002);
    let mut b = Vec::with_capacity(2 * m);
    for _ in 0..m {
        let a = 1.0 + 2e-4 * ra.f64();
        let e = rayleigh(&mut ra, 1e-4);
        b.push(Body::new(a, e, TAU * ra.f64(), TAU * ra.f64()));
    }
    for _ in 0..m {
        let a = 1.1 + 2e-4 * rb.f64();
        let e = e_b + 1e-5 * (rb.f64() - 0.5);
        let pom = 0.04 * (rb.f64() - 0.5);
        b.push(Body::new(a, e, pom, TAU * rb.f64()));
    }
    b
}

/// A B body's own crossing with the circle r = r_ref (the A annulus centre):
/// (crossing longitude, dr/dlambda there, dlambda/dt there).
fn own_crossing(bk: &Body, r_ref: f64, sign: f64) -> (f64, f64, f64) {
    let c = ((bk.p / r_ref - 1.0) / bk.e).clamp(-1.0, 1.0);
    let theta = bk.pom + sign * c.acos();
    let s = bk.at_longitude(theta);
    let rdot = (s[0] * s[2] + s[1] * s[3]) / r_ref;
    let lamdot = (s[0] * s[3] - s[1] * s[2]) / (r_ref * r_ref);
    (theta, rdot / lamdot, lamdot)
}

/// Passage times (time units) of longitude theta over (-2, t_end + 2).
fn passages(bk: &Body, theta: f64, t_end: f64) -> Vec<f64> {
    let off = bk.passage_tick(theta) as f64;
    let per = bk.period as f64;
    let lo = -2.0 * TICKS;
    let hi = (t_end + 2.0) * TICKS;
    let mut j = ((lo - off) / per).floor();
    let mut v = Vec::new();
    while off + j * per <= hi {
        v.push((off + j * per) / TICKS);
        j += 1.0;
    }
    v
}

/// The passage of theta nearest to time t (time units).
fn nearest_passage(bk: &Body, theta: f64, t: f64) -> f64 {
    let off = bk.passage_tick(theta) as f64;
    let per = bk.period as f64;
    let j = ((t * TICKS - off) / per).round();
    (off + j * per) / TICKS
}

struct Scene {
    ts: f64,
    spread: f64,
    sin_g: f64,
    da: f64,
    n_a: f64,
}

/// Stars = crossing longitudes of the first B orbit (as the cluster mode); plus the
/// B lane's crossing-longitude dispersion, the incidence angle at the star, lane A's
/// radial half-width and mean motion.
fn scene_geo(b: &[Body], m: usize) -> Scene {
    let c = ((b[m].p - 1.0) / b[m].e).clamp(-1.0, 1.0);
    let ts = c.acos();
    let v = b[m].at_longitude(ts);
    let va = [-ts.sin(), ts.cos()];
    let sin_g = (va[0] * v[3] - va[1] * v[2]).abs() / (v[2] * v[2] + v[3] * v[3]).sqrt();
    let mut spread = 0.0f64;
    for k in m..2 * m {
        for sgn in [1.0, -1.0] {
            let (th, _, _) = own_crossing(&b[k], 1.0, sgn);
            let star = if sgn > 0.0 { ts } else { -ts };
            spread = spread.max(wrap_pi(th - star).abs());
        }
    }
    let da = b[..m]
        .iter()
        .map(|x| (x.rmax() - 1.0).max(1.0 - x.rmin()))
        .fold(0.0f64, f64::max);
    let n_a = b[..m].iter().map(|x| x.n).sum::<f64>() / m as f64;
    Scene { ts, spread, sin_g, da, n_a }
}

/// Sliding-window merge: for each B event (tau, k, s) emit every A passage within s.
fn merge(ta: &[(f64, u32)], ev: &[(f64, u32, f64)], out: &mut Vec<(u32, u32)>) {
    let smax = ev.iter().map(|e| e.2).fold(0.0f64, f64::max);
    let mut ia = 0usize;
    for &(tau, k, s) in ev {
        while ia < ta.len() && ta[ia].0 < tau - smax {
            ia += 1;
        }
        let mut j = ia;
        while j < ta.len() && ta[j].0 <= tau + s {
            if ta[j].0 >= tau - s {
                out.push((ta[j].1, k));
            }
            j += 1;
        }
    }
}

/// The certificate: A×B pairs whose passages of the crossing longitude nearly coincide
/// in time — at the shared star (variant "mean", the checker's literal spec) or at each
/// B body's own crossing with the tight analytic window (variant "own"). Windows are
/// derived from (rho, lane elements) only; nothing is fitted to encounters.
fn xcert_pairs(
    b: &[Body],
    m: usize,
    variant: &str,
    g: &Scene,
) -> (Vec<(u32, u32)>, u64, f64, f64, f64, f64) {
    let t0 = Instant::now();
    let mut raw: Vec<(u32, u32)> = Vec::new();
    let (mut s_min, mut s_max, mut s_sum, mut s_n) = (f64::INFINITY, 0.0f64, 0.0f64, 0u64);
    let mut w_used = 0.0f64;
    for &star in &[g.ts, -g.ts] {
        let mut ta: Vec<(f64, u32)> = Vec::with_capacity(24 * m);
        for i in 0..m {
            for t in passages(&b[i], star, T_END) {
                ta.push((t, i as u32));
            }
        }
        ta.sort_by(|x, y| x.0.total_cmp(&y.0));
        let mut ev: Vec<(f64, u32, f64)> = Vec::with_capacity(24 * m);
        match variant {
            "mean" => {
                let d = g.spread + (RHO + g.da) / g.sin_g + RHO;
                let w = MARGIN * d * (1.0 / g.n_a + 1.0 / b[m].n);
                w_used = w;
                for k in m..2 * m {
                    for t in passages(&b[k], star, T_END) {
                        ev.push((t, k as u32, w));
                    }
                }
            }
            "own" => {
                for k in m..2 * m {
                    let sgn = if star > 0.0 { 1.0 } else { -1.0 };
                    let (th, drdl, lamdot) = own_crossing(&b[k], 1.0, sgn);
                    let tol_b = (RHO + g.da) / drdl.abs().max(1e-12);
                    let s = MARGIN * (tol_b / lamdot + (tol_b + RHO) / g.n_a);
                    let delta = wrap_pi(th - star);
                    for t in passages(&b[k], th, T_END) {
                        ev.push((t - delta / g.n_a, k as u32, s));
                    }
                    s_min = s_min.min(s);
                    s_max = s_max.max(s);
                    s_sum += s;
                    s_n += 1;
                }
            }
            "rank" => {
                // Conjunction-aware window. Necessity chain at the encounter instant:
                //   |lam_A - lam_B| <= 2 rho  (azimuthal component of a rho-separation),
                //   |lam_B - theta_k| <= tol_b (B's radius inside A's annulus +- rho),
                // and t_X = t* - (lam_X - theta_k)/rate_X, so
                //   |t_A - t_B| <= 2 rho / n_a + tol_b * |1/n_a - 1/lamdot_B|.
                // tol_b is the exact half-width of the longitude region where
                // r_B in [1-(da+rho), 1+(da+rho)] (closed form, no linearization).
                for k in m..2 * m {
                    let sgn = if star > 0.0 { 1.0 } else { -1.0 };
                    let th = |r: f64| {
                        b[k].pom + sgn * (((b[k].p / r - 1.0) / b[k].e).clamp(-1.0, 1.0)).acos()
                    };
                    let theta_k = th(1.0);
                    let tol_b = (th(1.0 - RHO - g.da) - theta_k)
                        .abs()
                        .max((th(1.0 + RHO + g.da) - theta_k).abs());
                    let s4 = b[k].at_longitude(theta_k);
                    let lamdot = s4[0] * s4[3] - s4[1] * s4[2]; // / r^2, r = 1 at the crossing
                    let s = MARGIN * (2.0 * RHO / g.n_a + tol_b * (1.0 / g.n_a - 1.0 / lamdot).abs());
                    let delta = wrap_pi(theta_k - star);
                    for t in passages(&b[k], theta_k, T_END) {
                        ev.push((t - delta / g.n_a, k as u32, s));
                    }
                    s_min = s_min.min(s);
                    s_max = s_max.max(s);
                    s_sum += s;
                    s_n += 1;
                }
            }
            _ => panic!("variant: mean|own|rank"),
        }
        ev.sort_by(|x, y| x.0.total_cmp(&y.0));
        merge(&ta, &ev, &mut raw);
    }
    let gen_s = t0.elapsed().as_secs_f64();
    let raw_n = raw.len() as u64;
    raw.sort_unstable();
    raw.dedup();
    if s_n == 0 {
        (s_min, s_max, s_sum) = (w_used, w_used, w_used);
    }
    let s_mean = s_sum / s_n.max(1) as f64;
    (raw, raw_n, s_min, s_max, s_mean, gen_s)
}

fn q4(v: &mut Vec<f64>) -> (f64, f64, f64, f64) {
    v.sort_by(|x, y| x.total_cmp(y));
    let n = v.len();
    let q = |p: f64| v[((n as f64 - 1.0) * p) as usize];
    (q(0.5), q(0.9), q(0.99), v[n - 1])
}
