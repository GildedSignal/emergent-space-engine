//! Scale ladder (docs/test-ladder.md): frozen rungs, each run in its own child process.
//! Correctness is checked against references that do not use the engine's search:
//! an exact integer pair oracle, analytic zero-contact constructions, the engine's
//! exhaustive per-tick predicate audit, replay, and slice-budget invariance.
use emergent_engine::{
    math::{r, Vec2},
    population::Family,
    propagator::Inertial,
    runtime::Body,
    Engine, WorkBudget,
};
use serde_json::{json, Value};
use std::{
    collections::HashMap,
    fs,
    path::Path,
    process::{Command as Process, Stdio},
    time::{Duration, Instant},
};
type Result<T> = super::Result<T>;

const MANIFEST: &[u8] = include_bytes!("../../scenarios/scale-ladder-v4.json");

fn manifest() -> Result<Value> {
    Ok(serde_json::from_slice(MANIFEST)?)
}

pub(crate) fn peak_rss() -> u64 {
    let mut usage = std::mem::MaybeUninit::<libc::rusage>::uninit();
    // SAFETY: getrusage initializes the out pointer on success.
    unsafe {
        if libc::getrusage(libc::RUSAGE_SELF, usage.as_mut_ptr()) == 0 {
            let n = usage.assume_init().ru_maxrss as u64;
            if cfg!(target_os = "macos") {
                n
            } else {
                n * 1024
            }
        } else {
            0
        }
    }
}

/// Process CPU time (user + system) in seconds; cores used = CPU time / wall time.
pub(crate) fn cpu_seconds() -> f64 {
    let mut usage = std::mem::MaybeUninit::<libc::rusage>::uninit();
    // SAFETY: getrusage initializes the out pointer on success.
    unsafe {
        if libc::getrusage(libc::RUSAGE_SELF, usage.as_mut_ptr()) == 0 {
            let u = usage.assume_init();
            let tv = |t: libc::timeval| t.tv_sec as f64 + t.tv_usec as f64 / 1e6;
            tv(u.ru_utime) + tv(u.ru_stime)
        } else {
            0.0
        }
    }
}

/// Manifest caps merged with the chosen profile (quick or full).
pub(crate) fn caps(m: &Value, profile: &str) -> Value {
    let mut c = m["caps"].clone();
    if let (Some(obj), Some(p)) = (c.as_object_mut(), m["profiles"][profile].as_object()) {
        for (k, v) in p {
            obj.insert(k.clone(), v.clone());
        }
    }
    c
}

pub(crate) fn percentile(sorted: &[f64], q: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    sorted[((sorted.len() - 1) as f64 * q).round() as usize]
}

pub(crate) struct Rng(pub(crate) u64);
impl Rng {
    pub(crate) fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    /// Uniform integer in [lo, hi].
    pub(crate) fn range(&mut self, lo: i128, hi: i128) -> i128 {
        lo + (self.next() as u128 % (hi - lo + 1) as u128) as i128
    }
}

/// Integer description of an independent inertial disc: position p (units),
/// velocity n / D (units per tick).
#[derive(Clone, Copy)]
pub(crate) struct Disc {
    pub(crate) p: [i128; 2],
    pub(crate) n: [i128; 2],
}

fn body(id: u64, d: &Disc, den: i128, radius: i128, stop: bool) -> Result<Body> {
    let mut b = Body::new(
        id,
        "ladder",
        Inertial::new(
            0,
            Vec2::new(d.p[0], d.p[1]),
            Vec2 {
                x: r(d.n[0]) / r(den),
                y: r(d.n[1]) / r(den),
            },
        )?,
        r(radius),
        r(1),
    );
    b.stop_on_contact = stop;
    Ok(b)
}

/// Exact: does |dp + dn t / D| <= R for some real t in [0, T]?
fn pair_contact(a: &Disc, b: &Disc, den: i128, reach: i128, horizon: i128) -> bool {
    let p = [den * (b.p[0] - a.p[0]), den * (b.p[1] - a.p[1])];
    let q = [b.n[0] - a.n[0], b.n[1] - a.n[1]];
    let lim = (den * reach) * (den * reach);
    let pp = p[0] * p[0] + p[1] * p[1];
    let qq = q[0] * q[0] + q[1] * q[1];
    if qq == 0 {
        return pp <= lim;
    }
    let s = -(p[0] * q[0] + p[1] * q[1]);
    if s <= 0 {
        pp <= lim
    } else if s >= horizon * qq {
        let e = [p[0] + q[0] * horizon, p[1] + q[1] * horizon];
        e[0] * e[0] + e[1] * e[1] <= lim
    } else {
        let cross = p[0] * q[1] - p[1] * q[0];
        cross * cross <= lim * qq
    }
}

/// Independent of the engine's sweep: uniform grid over swept boxes plus the exact predicate.
pub(crate) fn oracle_pairs(discs: &[Disc], den: i128, reach: i128, horizon: i128) -> Vec<(u64, u64)> {
    let lo = |d: &Disc, k: usize| {
        (den * d.p[k]).min(den * d.p[k] + d.n[k] * horizon) - den * reach
    };
    let hi = |d: &Disc, k: usize| {
        (den * d.p[k]).max(den * d.p[k] + d.n[k] * horizon) + den * reach
    };
    let cell = discs
        .iter()
        .map(|d| (hi(d, 0) - lo(d, 0)).max(hi(d, 1) - lo(d, 1)))
        .max()
        .unwrap_or(1)
        .max(1);
    let mut grid: HashMap<(i128, i128), Vec<usize>> = HashMap::new();
    for (i, d) in discs.iter().enumerate() {
        let key = (lo(d, 0).div_euclid(cell), lo(d, 1).div_euclid(cell));
        grid.entry(key).or_default().push(i);
    }
    let mut out = Vec::new();
    for (&(cx, cy), members) in &grid {
        for dx in -1..=1 {
            for dy in -1..=1 {
                let Some(others) = grid.get(&(cx + dx, cy + dy)) else {
                    continue;
                };
                for &i in members {
                    for &j in others {
                        if i < j && pair_contact(&discs[i], &discs[j], den, reach, horizon) {
                            out.push((i as u64 + 1, j as u64 + 1));
                        }
                    }
                }
            }
        }
    }
    out.sort_unstable();
    out.dedup();
    out
}

pub(crate) fn brute_pairs(discs: &[Disc], den: i128, reach: i128, horizon: i128) -> Vec<(u64, u64)> {
    let mut out = Vec::new();
    for i in 0..discs.len() {
        for j in i + 1..discs.len() {
            if pair_contact(&discs[i], &discs[j], den, reach, horizon) {
                out.push((i as u64 + 1, j as u64 + 1));
            }
        }
    }
    out
}

fn engine_pairs(e: &Engine) -> Vec<(u64, u64)> {
    let mut v: Vec<_> = e
        .sorted_events()
        .into_iter()
        .filter(|ev| ev.kind == "contact")
        .map(|ev| {
            let (a, b) = (ev.subjects[0], ev.subjects[1]);
            (a.min(b), a.max(b))
        })
        .collect();
    v.sort_unstable();
    v.dedup();
    v
}

fn random_world(n: u64, area_per_body: i128, den: i128, reach: i128, seed: u64) -> Vec<Disc> {
    let side = ((n as f64 * area_per_body as f64).sqrt()).ceil() as i128;
    let mut rng = Rng(seed ^ n);
    let mut discs: Vec<Disc> = Vec::with_capacity(n as usize);
    // Reject genesis overlaps with a coarse grid (cell = 4 * reach).
    let cell = 4 * reach;
    let mut occupied: HashMap<(i128, i128), Vec<usize>> = HashMap::new();
    while discs.len() < n as usize {
        let d = Disc {
            p: [rng.range(0, side), rng.range(0, side)],
            n: [rng.range(-den / 2, den / 2), rng.range(-den / 2, den / 2)],
        };
        let key = (d.p[0].div_euclid(cell), d.p[1].div_euclid(cell));
        let clash = (-1..=1).any(|dx| {
            (-1..=1).any(|dy| {
                occupied.get(&(key.0 + dx, key.1 + dy)).is_some_and(|v| {
                    v.iter().any(|&k| {
                        let o = &discs[k];
                        let (x, y) = (o.p[0] - d.p[0], o.p[1] - d.p[1]);
                        x * x + y * y <= (2 * reach) * (2 * reach)
                    })
                })
            })
        });
        if !clash {
            occupied.entry(key).or_default().push(discs.len());
            discs.push(d);
        }
    }
    discs
}

struct Run {
    complete: bool,
    limiter: Option<String>,
    setup_ms: f64,
    advance_ms: f64,
    worst_slice_ms: f64,
    slices: u64,
    ops: usize,
    events: usize,
    cpu_s: f64,
    smooth: Value,
}

/// Advance to `target`. With `smooth`, every call uses the observatory's frame budget and
/// every frame is timed (smoothness over the whole run); otherwise `slice_ops` per call.
fn drive(e: &mut Engine, target: i128, slice_ops: usize, caps: &Value, smooth: Option<&Value>, setup_ms: f64) -> Run {
    let wall = caps["wall_seconds_per_rung"].as_f64().unwrap_or(120.0);
    let rss_cap = caps["peak_rss_bytes"].as_u64().unwrap_or(u64::MAX);
    let ops = smooth.and_then(|s| s["slice_operations"].as_u64()).map_or(slice_ops, |o| o as usize);
    let t0 = Instant::now();
    let cpu0 = cpu_seconds();
    let mut run = Run {
        complete: false,
        limiter: None,
        setup_ms,
        advance_ms: 0.0,
        worst_slice_ms: 0.0,
        slices: 0,
        ops: 0,
        events: 0,
        cpu_s: 0.0,
        smooth: Value::Null,
    };
    let mut frames_us: Vec<f32> = Vec::new();
    loop {
        let s = Instant::now();
        match e.advance(target, WorkBudget::new(ops)) {
            Ok(res) => {
                let us = s.elapsed().as_secs_f64() * 1e6;
                run.worst_slice_ms = run.worst_slice_ms.max(us / 1e3);
                if smooth.is_some() {
                    frames_us.push(us as f32);
                }
                run.slices += 1;
                run.ops += res.operations;
                run.events += res.events;
                if res.complete {
                    run.complete = true;
                    break;
                }
            }
            Err(err) => {
                run.limiter = Some(format!("engine error: {err}"));
                break;
            }
        }
        if run.slices % 64 == 0 {
            if t0.elapsed().as_secs_f64() > wall {
                run.limiter = Some(format!("wall cap {wall} s"));
                break;
            }
            if peak_rss() > rss_cap {
                run.limiter = Some("memory cap".into());
                break;
            }
        }
    }
    run.advance_ms = t0.elapsed().as_secs_f64() * 1e3;
    run.cpu_s = cpu_seconds() - cpu0;
    if let Some(s) = smooth {
        let mut ms: Vec<f64> = frames_us.iter().map(|&u| u as f64 / 1e3).collect();
        ms.sort_by(|a, b| a.total_cmp(b));
        let target_ms = s["target_p99_ms"].as_f64().unwrap_or(5.0);
        let p99 = percentile(&ms, 0.99);
        let over = ms.iter().filter(|&&x| x > target_ms).count();
        run.smooth = json!({"frame_operations": ops, "frames": ms.len(),
            "p50_ms": percentile(&ms, 0.5), "p95_ms": percentile(&ms, 0.95), "p99_ms": p99,
            "max_ms": ms.last().copied().unwrap_or(0.0), "frames_over_target": over,
            "verdict": if ms.is_empty() { "NONE" } else if p99 <= target_ms { "SMOOTH" } else { "JANK" }});
    }
    run
}

fn metric(e: &Engine, name: &str) -> u64 {
    serde_json::to_value(&e.metrics)
        .ok()
        .and_then(|m| m.get(name).and_then(Value::as_u64))
        .unwrap_or(0)
}

fn row(track: &str, param: Value, e: &Engine, run: &Run, correct: Value, pass_extra: bool) -> Value {
    let k = (e.state.bodies.len() + e.state.families.len()).max(1) as u64;
    let compares = metric(e, "aabb_compares");
    let rss = peak_rss();
    let pass = run.complete && pass_extra;
    json!({
        "track": track, "param": param,
        "status": if pass { "PASS" } else { "FAIL" },
        "limiter": run.limiter.clone().or_else(|| if pass { None } else { Some("correctness".into()) }),
        "correctness": correct,
        "descriptions": k, "events": run.events, "operations": run.ops,
        "aabb_compares": compares, "certified_rejections": metric(e, "certified_rejections"),
        "pairs_per_description": compares as f64 / k as f64,
        "setup_ms": run.setup_ms, "advance_ms": run.advance_ms,
        "worst_slice_ms": run.worst_slice_ms, "slices": run.slices, "smoothness": run.smooth,
        "cores_used": run.cpu_s / (run.advance_ms / 1e3).max(1e-9),
        "cores_available": std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1),
        "peak_rss_bytes": rss, "rss_per_description": rss as f64 / k as f64,
        "engine_metrics": serde_json::to_value(&e.metrics).unwrap_or(Value::Null),
    })
}

fn pairs_check(engine: &[(u64, u64)], oracle: &[(u64, u64)]) -> (bool, Value) {
    let missing: Vec<_> = oracle.iter().filter(|p| engine.binary_search(p).is_err()).take(5).collect();
    let extra: Vec<_> = engine.iter().filter(|p| oracle.binary_search(p).is_err()).take(5).collect();
    let ok = engine == oracle;
    (ok, json!({"engine_contacts": engine.len(), "oracle_contacts": oracle.len(), "equal": ok,
                "first_missing": missing, "first_extra": extra}))
}

fn x_random(track: &Value, n: u64, horizon: i128, m: &Value) -> Result<Value> {
    let den = m["velocity_denominator"].as_i64().unwrap_or(1024) as i128;
    let radius = track["radius"].as_i64().unwrap_or(1) as i128;
    let area = track["area_per_body"].as_i64().unwrap_or(1_000_000) as i128;
    let seed = m["seed"].as_u64().unwrap_or(1);
    let t = Instant::now();
    let discs = random_world(n, area, den, 2 * radius, seed);
    let bodies = discs
        .iter()
        .enumerate()
        .map(|(i, d)| body(i as u64 + 1, d, den, radius, false))
        .collect::<Result<Vec<_>>>()?;
    let mut e = Engine::new(seed, bodies, vec![])?;
    let setup = t.elapsed().as_secs_f64() * 1e3;
    let run = drive(&mut e, horizon, m["caps"]["slice_operations"].as_u64().unwrap_or(100_000) as usize, &m["caps"], Some(&m["smoothness"]), setup);
    let t = Instant::now();
    let oracle = oracle_pairs(&discs, den, 2 * radius, horizon);
    let oracle_ms = t.elapsed().as_secs_f64() * 1e3;
    let brute_agrees = if n <= 4096 { Some(brute_pairs(&discs, den, 2 * radius, horizon) == oracle) } else { None };
    let (ok, mut c) = pairs_check(&engine_pairs(&e), &oracle);
    c["oracle_ms"] = json!(oracle_ms);
    c["grid_oracle_equals_brute_force"] = json!(brute_agrees);
    let param = json!({"bodies": n, "horizon": horizon});
    Ok(row(track["id"].as_str().unwrap_or("?"), param, &e, &run, c, ok && brute_agrees != Some(false)))
}

fn x_crowded(track: &Value, n: u64, m: &Value) -> Result<Value> {
    let den = m["velocity_denominator"].as_i64().unwrap_or(1024) as i128;
    let radius = track["radius"].as_i64().unwrap_or(1) as i128;
    let s = track["spacing"].as_i64().unwrap_or(16) as i128;
    let half = (n / 2) as i128;
    let width = half * s; // extent of the vertical strips along x
    let speed = den / 4;
    let horizon = 4 * width; // sideways movers sweep at least the whole width
    let height = width;
    let mut rng = Rng(m["seed"].as_u64().unwrap_or(1) ^ n ^ 0xC0);
    let mut discs = Vec::new();
    for i in 0..half {
        // Thin vertical strips moving down, below y = height.
        discs.push(Disc { p: [i * s, rng.range(0, height)], n: [0, -speed] });
    }
    for j in 0..half {
        // Thin horizontal strips above y = 2 * height, moving left or right across the whole width.
        let dir = if rng.next() % 2 == 0 { 1 } else { -1 };
        discs.push(Disc { p: [rng.range(0, width), 2 * height + j * s], n: [dir * speed, 0] });
    }
    let t = Instant::now();
    let bodies = discs
        .iter()
        .enumerate()
        .map(|(i, d)| body(i as u64 + 1, d, den, radius, false))
        .collect::<Result<Vec<_>>>()?;
    let mut e = Engine::new(m["seed"].as_u64().unwrap_or(1), bodies, vec![])?;
    let setup = t.elapsed().as_secs_f64() * 1e3;
    let run = drive(&mut e, horizon, m["caps"]["slice_operations"].as_u64().unwrap_or(100_000) as usize, &m["caps"], Some(&m["smoothness"]), setup);
    let actual = engine_pairs(&e);
    let oracle_ok = if n <= 4096 { Some(brute_pairs(&discs, den, 2 * radius, horizon).is_empty()) } else { None };
    let ok = actual.is_empty() && oracle_ok != Some(false);
    let c = json!({"expected_contacts": 0, "engine_contacts": actual.len(), "brute_force_confirms_zero": oracle_ok});
    Ok(row(track["id"].as_str().unwrap_or("?"), json!({"bodies": n, "horizon": horizon}), &e, &run, c, ok))
}

fn x_lattice(track: &Value, lanes: i128, m: &Value) -> Result<Value> {
    let members = track["members_per_lane"].as_u64().unwrap_or(1_000_000);
    let gap = track["lane_spacing"].as_i64().unwrap_or(64_000) as i128;
    let horizon = track["horizon"].as_i64().unwrap_or(4096) as i128;
    let radius = track["radius"].as_i64().unwrap_or(1) as i128;
    let half = 32 * members as i128; // 64 * members / 2
    let quarter = r(1) / r(4);
    let mut families = Vec::new();
    let mut first = 1u64;
    for h in 0..lanes {
        // x0 = 3 - 32M keeps (x0 - X + Y - y0) = 3 (mod 64): every crossing misses at 3/sqrt(2).
        families.push(Family::affine(format!("H{h}"), first, members, 0,
            Inertial::new(0, Vec2::new(3 - half, gap * h), Vec2 { x: quarter.clone(), y: r(0) })?,
            Vec2::new(64, 0), r(radius), r(1)));
        first += members;
    }
    for v in 0..lanes {
        families.push(Family::affine(format!("V{v}"), first, members, 0,
            Inertial::new(0, Vec2::new(gap * v, -half), Vec2 { x: r(0), y: quarter.clone() })?,
            Vec2::new(0, 64), r(radius), r(1)));
        first += members;
    }
    let t = Instant::now();
    let mut e = Engine::new(m["seed"].as_u64().unwrap_or(1), vec![], families)?;
    let setup = t.elapsed().as_secs_f64() * 1e3;
    let run = drive(&mut e, horizon, m["caps"]["slice_operations"].as_u64().unwrap_or(100_000) as usize, &m["caps"], Some(&m["smoothness"]), setup);
    let actual = engine_pairs(&e);
    let c = json!({"expected_contacts": 0, "engine_contacts": actual.len(),
                   "member_crossings_in_horizon_per_lane_pair": horizon / 4 / 64 * 2});
    Ok(row(track["id"].as_str().unwrap_or("?"), json!({"lanes_per_axis": lanes, "members_per_lane": members}), &e, &run, c, actual.is_empty()))
}

pub(crate) fn packed(n: u64, track: &Value, m: &Value) -> Result<(Vec<Body>, i128)> {
    let den = m["velocity_denominator"].as_i64().unwrap_or(1024) as i128;
    let g = track["grid_spacing"].as_i64().unwrap_or(8) as i128;
    let jitter = track["jitter"].as_i64().unwrap_or(2) as i128;
    let radius = track["radius"].as_i64().unwrap_or(1) as i128;
    let side = (n as f64).sqrt().ceil() as i128;
    let mut rng = Rng(m["seed"].as_u64().unwrap_or(1) ^ n ^ 0xC1);
    let mut out = Vec::new();
    for i in 0..n as i128 {
        let d = Disc {
            p: [(i % side) * g + rng.range(-jitter, jitter), (i / side) * g + rng.range(-jitter, jitter)],
            n: [rng.range(-den / 2, den / 2), rng.range(-den / 2, den / 2)],
        };
        out.push(body(i as u64 + 1, &d, den, radius, true)?);
    }
    Ok((out, track["horizon"].as_i64().unwrap_or(128) as i128))
}

fn c_packed(track: &Value, n: u64, m: &Value) -> Result<Value> {
    let seed = m["seed"].as_u64().unwrap_or(1);
    let slice = m["caps"]["slice_operations"].as_u64().unwrap_or(100_000) as usize;
    let t = Instant::now();
    let (bodies, horizon) = packed(n, track, m)?;
    let mut e = Engine::new(seed, bodies, vec![])?;
    let setup = t.elapsed().as_secs_f64() * 1e3;
    let run = drive(&mut e, horizon, slice, &m["caps"], Some(&m["smoothness"]), setup);
    let mut c = json!({});
    let mut ok = run.complete;
    if run.complete {
        let digest = e.history_digest(horizon)?;
        let replayed = e.replay()?.history_digest(horizon)?;
        c["replay_equal"] = json!(digest == replayed);
        ok &= digest == replayed;
        if n <= m["caps"]["budget_invariance_max_bodies"].as_u64().unwrap_or(1024) {
            let (bodies, _) = packed(n, track, m)?;
            let mut small = Engine::new(seed, bodies, vec![])?;
            let r2 = drive(&mut small, horizon, 64, &m["caps"], None, 0.0);
            let same = r2.complete && small.history_digest(horizon)? == digest;
            c["budget_64_digest_equal"] = json!(same);
            ok &= same;
        }
        if n <= m["caps"]["audit_max_bodies"].as_u64().unwrap_or(256) {
            let audit = e.independent_inertial_facts(horizon)?;
            let mut actual: Vec<_> = e
                .sorted_events()
                .into_iter()
                .filter(|ev| ev.kind == "contact")
                .map(|ev| (ev.tick, ev.subjects[0].min(ev.subjects[1]), ev.subjects[0].max(ev.subjects[1])))
                .collect();
            actual.sort_unstable();
            actual.dedup();
            c["audit_contacts"] = json!(audit.contacts.len());
            c["engine_contacts"] = json!(actual.len());
            c["audit_equal"] = json!(audit.contacts == actual);
            ok &= audit.contacts == actual;
        }
        c["stopped_bodies"] = json!(e.state.bodies.values().filter(|b| b.segments.len() > 1).count());
    }
    Ok(row(track["id"].as_str().unwrap_or("?"), json!({"bodies": n, "horizon": horizon}), &e, &run, c, ok))
}


fn c_gas(track: &Value, n: u64, horizon: i128, m: &Value) -> Result<Value> {
    let seed = m["seed"].as_u64().unwrap_or(1);
    let quantum = track["quantum"].as_i64().map(|q| q as i128);
    let q = quantum.unwrap_or(track["velocity_quantum_for_setup"].as_i64().unwrap_or(1024) as i128);
    let g = super::gas::world(n, track["fill"].as_f64().unwrap_or(0.1), q, track["vmax_units"].as_i64().unwrap_or(256) as i128, seed);
    let t = Instant::now();
    let mut e = super::gas::engine(&g, seed, quantum)?;
    let setup = t.elapsed().as_secs_f64() * 1e3;
    let run = drive(&mut e, horizon, 64, &m["caps"], Some(&m["smoothness"]), setup);
    let mut c = json!({});
    let mut ok = run.complete;
    if run.complete {
        let inv = super::gas::invariants(&e, &g, horizon);
        let events = e.sorted_events();
        c["contacts"] = json!(events.iter().filter(|x| x.kind == "contact").count());
        c["wall_hits"] = json!(events.iter().filter(|x| x.kind == "wall").count());
        c["contained"] = json!(inv.contained);
        c["momentum_ledger_exact"] = json!(inv.momentum_ledger_exact);
        c["energy_ledger_exact"] = json!(inv.energy_ledger_exact);
        c["energy_drift_relative"] = json!(inv.energy_drift_relative);
        c["max_velocity_bits"] = json!(inv.max_velocity_bits);
        ok &= inv.contained && inv.momentum_ledger_exact && inv.energy_ledger_exact;
        if quantum.is_some() {
            c["max_residual"] = json!(inv.max_residual);
            c["residual_bound"] = json!(inv.residual_bound);
            ok &= inv.max_residual <= inv.residual_bound;
            let pair_ticks = (n as f64) * (n as f64) / 2.0 * horizon as f64;
            if pair_ticks <= m["caps"]["reference_max_pair_ticks"].as_f64().unwrap_or(5e7) {
                let t = Instant::now();
                let reference = super::gas::reference(&g, horizon);
                c["reference_ms"] = json!(t.elapsed().as_secs_f64() * 1e3);
                match super::gas::engine_view(&e, q, horizon) {
                    None => {
                        c["reference_equal"] = json!(false);
                        c["reference_note"] = json!("engine state off the integer lattice");
                        ok = false;
                    }
                    Some(view) => {
                        let ev = view.events == reference.events;
                        let fin = view.finals == reference.finals;
                        let wm = view.wall_momentum == reference.wall_momentum;
                        c["reference_equal"] = json!(ev && fin && wm);
                        c["reference_events"] = json!(reference.events.len());
                        if !ev {
                            let i = view.events.iter().zip(reference.events.iter()).position(|(a, b)| a != b).unwrap_or(view.events.len().min(reference.events.len()));
                            c["first_event_difference"] = json!({"index": i, "engine": format!("{:?}", view.events.get(i)), "reference": format!("{:?}", reference.events.get(i))});
                        }
                        if !fin {
                            let i = view.finals.iter().zip(reference.finals.iter()).position(|(a, b)| a != b).unwrap_or(0);
                            c["first_body_difference"] = json!({"body": i + 1, "engine": format!("{:?}", view.finals.get(i)), "reference": format!("{:?}", reference.finals.get(i))});
                        }
                        ok &= ev && fin && wm;
                    }
                }
            }
        }
        let digest = e.history_digest(horizon)?;
        let replayed = e.replay()?.history_digest(horizon)?;
        c["replay_equal"] = json!(digest == replayed);
        ok &= digest == replayed;
        if n <= m["caps"]["budget_invariance_max_bodies"].as_u64().unwrap_or(256) {
            let mut other = super::gas::engine(&g, seed, quantum)?;
            let r2 = drive(&mut other, horizon, 64, &m["caps"], None, 0.0);
            let same = r2.complete && other.history_digest(horizon)? == digest;
            c["budget_64_digest_equal"] = json!(same);
            ok &= same;
        }
    }
    Ok(row(track["id"].as_str().unwrap_or("?"), json!({"bodies": n, "horizon": horizon}), &e, &run, c, ok))
}

/// Diagnostic, not a rung: the packed stop cascade under several slice budgets.
fn c1_budgets(n: u64, m: &Value) -> Result<Value> {
    let track = m["tracks"].as_array().ok_or("tracks")?.iter().find(|t| t["id"] == "C1-packed-stop-cascade").ok_or("C1")?;
    let seed = m["seed"].as_u64().unwrap_or(1);
    let mut out = Vec::new();
    let mut reference: Option<Vec<(i128, String, Vec<u64>)>> = None;
    for budget in [1_000_000_000usize, 100_000, 1000, 64, 8] {
        let (bodies, horizon) = packed(n, track, m)?;
        let mut e = Engine::new(seed, bodies, vec![])?;
        let run = drive(&mut e, horizon, budget, &m["caps"], None, 0.0);
        let events: Vec<_> = e.sorted_events().into_iter().map(|ev| (ev.tick, ev.kind.clone(), ev.subjects.clone())).collect();
        let first_diff = reference.as_ref().and_then(|r| {
            r.iter().zip(events.iter()).position(|(a, b)| a != b).map(|i| json!({"index": i, "reference": format!("{:?}", r[i]), "this": format!("{:?}", events[i])}))
        });
        let audit = if run.complete && n <= 256 {
            let a = e.independent_inertial_facts(horizon)?;
            let mut mine: Vec<_> = events.iter().filter(|x| x.1 == "contact").map(|x| (x.0, x.2[0].min(x.2[1]), x.2[0].max(x.2[1]))).collect();
            mine.sort_unstable();
            mine.dedup();
            let missing: Vec<_> = a.contacts.iter().filter(|c| mine.binary_search(c).is_err()).take(3).collect();
            let extra: Vec<_> = mine.iter().filter(|c| a.contacts.binary_search(c).is_err()).take(3).collect();
            json!({"audit_contacts": a.contacts.len(), "equal": a.contacts == mine, "first_missing": missing, "first_extra": extra})
        } else {
            Value::Null
        };
        out.push(json!({"budget": budget, "audit": audit, "complete": run.complete, "slices": run.slices, "events": events.len(),
            "contacts": events.iter().filter(|e| e.1 == "contact").count(),
            "digest": if run.complete { e.history_digest(horizon)? } else { String::new() }, "first_diff_vs_largest_budget": first_diff}));
        if reference.is_none() {
            reference = Some(events);
        }
    }
    Ok(json!(out))
}

/// Child process: run one rung and print its JSON row as the last stdout line.
pub fn rung(args: Vec<String>) -> Result<()> {
    let mut m = manifest()?;
    let profile = args.get(2).map(String::as_str).unwrap_or("quick");
    m["caps"] = caps(&m, profile);
    let track_id = args.first().ok_or("track id required")?;
    if track_id == "C1-budgets" {
        let n: u64 = args.get(1).ok_or("bodies")?.parse()?;
        println!("{}", serde_json::to_string_pretty(&c1_budgets(n, &m)?)?);
        return Ok(());
    }
    let index: usize = args.get(1).ok_or("rung index required")?.parse()?;
    let track = m["tracks"].as_array().ok_or("tracks")?.iter().find(|t| t["id"] == track_id.as_str()).ok_or("unknown track")?;
    let value = match track_id.as_str() {
        "X1-relative-motion" => x_random(track, track["bodies"][index].as_u64().ok_or("rung")?, track["horizon"].as_i64().unwrap_or(4096) as i128, &m)?,
        "X2-horizon" => x_random(track, track["bodies"].as_u64().unwrap_or(4096), track["horizons"][index].as_i64().ok_or("rung")? as i128, &m)?,
        "X3-crowded-axes" => x_crowded(track, track["bodies"][index].as_u64().ok_or("rung")?, &m)?,
        "X4-near-miss-lattice" => x_lattice(track, track["lanes_per_axis"][index].as_i64().ok_or("rung")? as i128, &m)?,
        "C1-packed-stop-cascade" => c_packed(track, track["bodies"][index].as_u64().ok_or("rung")?, &m)?,
        "C2-trapped-gas" | "X6-exact-fraction-gas" => c_gas(track, track["bodies"][index].as_u64().ok_or("rung")?, track["horizon"].as_i64().unwrap_or(1024) as i128, &m)?,
        "X5-carry-endurance" => c_gas(track, track["bodies"].as_u64().unwrap_or(64), track["horizons"][index].as_i64().ok_or("rung")? as i128, &m)?,
        _ => return Err("unknown track".into()),
    };
    println!("{}", serde_json::to_string(&value)?);
    Ok(())
}

fn rung_count(track: &Value) -> usize {
    for key in ["bodies", "horizons", "lanes_per_axis"] {
        if let Some(a) = track[key].as_array() {
            return a.len();
        }
    }
    0
}

fn rung_size(track: &Value, i: usize) -> f64 {
    ["bodies", "horizons", "lanes_per_axis"]
        .iter()
        .find_map(|k| track[*k].as_array().and_then(|a| a[i].as_f64()))
        .unwrap_or(0.0)
}

/// Parent: climb every track in its own child processes until a rung fails.
pub fn run(out: &Path, only: Option<&str>, profile: &str) -> Result<Value> {
    let m = manifest()?;
    let c = caps(&m, profile);
    let exe = std::env::current_exe()?;
    let wall = c["wall_seconds_per_rung"].as_f64().unwrap_or(120.0);
    let rss_cap = c["peak_rss_bytes"].as_f64().unwrap_or(f64::MAX);
    let ladder_budget = c["ladder_seconds"].as_f64().unwrap_or(f64::MAX);
    let ladder_start = Instant::now();
    let mut rows = Vec::new();
    for track in m["tracks"].as_array().ok_or("tracks")? {
        let id = track["id"].as_str().unwrap_or("?");
        if only.is_some_and(|o| o != id) {
            continue;
        }
        let mut previous: Option<(f64, f64)> = None; // (size, peak rss)
        let mut failed = false;
        for i in 0..rung_count(track) {
            let size = rung_size(track, i);
            if failed {
                rows.push(json!({"track": id, "rung": i, "size": size, "status": "NOT_ATTEMPTED", "limiter": "an earlier rung failed"}));
                continue;
            }
            if ladder_start.elapsed().as_secs_f64() > ladder_budget {
                rows.push(json!({"track": id, "rung": i, "size": size, "status": "NOT_ATTEMPTED", "limiter": format!("ladder time budget {ladder_budget} s ({profile} profile)")}));
                continue;
            }
            if let (Some((ps, prss)), true) = (previous, m["caps"]["skip_if_projected_rss_over_cap"].as_bool().unwrap_or(false)) {
                if track["bodies"].is_array() && prss * size / ps > rss_cap {
                    rows.push(json!({"track": id, "rung": i, "size": size, "status": "NOT_ATTEMPTED",
                                     "limiter": format!("projected peak RSS {:.0} MB over cap", prss * size / ps / 1e6)}));
                    failed = true;
                    continue;
                }
            }
            eprintln!("rung {id} #{i} (size {size})");
            let started = Instant::now();
            let mut child = Process::new(&exe)
                .args(["ladder-rung", id, &i.to_string(), profile])
                .stdout(Stdio::piped())
                .stderr(Stdio::inherit())
                .spawn()?;
            let kill_after = Duration::from_secs_f64(wall * 3.0 + 20.0);
            let status = loop {
                if let Some(s) = child.try_wait()? {
                    break Some(s);
                }
                if started.elapsed() > kill_after {
                    child.kill()?;
                    child.wait()?;
                    break None;
                }
                std::thread::sleep(Duration::from_millis(50));
            };
            let output = child.wait_with_output()?;
            let text = String::from_utf8_lossy(&output.stdout);
            let mut value = match (status, text.lines().last().and_then(|l| serde_json::from_str::<Value>(l).ok())) {
                (Some(s), Some(v)) if s.success() => v,
                (None, _) => json!({"status": "FAIL", "limiter": format!("killed after {:.0} s (setup, oracle or checks exceeded the outer limit)", kill_after.as_secs_f64())}),
                (Some(s), _) => json!({"status": "FAIL", "limiter": format!("child exited {s}")}),
            };
            value["track"] = json!(id);
            value["rung"] = json!(i);
            value["size"] = json!(size);
            value["child_wall_s"] = json!(started.elapsed().as_secs_f64());
            if value["status"] != "PASS" {
                failed = true;
            }
            previous = value["peak_rss_bytes"].as_f64().map(|rss| (size, rss));
            fs::write(out.join("rows.partial.json"), serde_json::to_vec_pretty(&rows)?)?;
            rows.push(value);
        }
    }
    Ok(json!({
        "schema": 4, "manifest": "scenarios/scale-ladder-v4.json", "profile": profile,
        "ladder_seconds": ladder_start.elapsed().as_secs_f64(),
        "manifest_blake3": blake3::hash(MANIFEST).to_hex().to_string(),
        "provenance": super::bench::provenance(),
        "rows": rows,
        "accounting": "Each rung ran in a fresh child process; peak RSS is that process's getrusage maximum. Wall times are single runs. Oracle and correctness checks run after the timed advance and are excluded from advance_ms.",
    }))
}
