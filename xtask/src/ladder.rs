//! Scale ladder v7 (scenarios/scale-ladder-v7.json): every lattice mode climbs the frozen rungs
//! under es-lattice-relativistic-v1. Each (mode, track, rung) runs in its own child process.
//! Every advance runs in units of `unit_ops` charged operations and every unit is timed.
//! Correctness: exact oracles (pair oracle, independent gas reference, all-pairs audit),
//! ledgers, mode invariance against the chronon reference, and budget invariance.
use crate::behave::sample::Rng;
use crate::measure::{drive, peak_rss, percentile};
use crate::{gas, lattice};
use emergent_lattice::{chronon::Chronon, relativity, worlds, Body, Kind, Law, Response, Stepper, World};
use serde_json::{json, Value};
use std::{
    collections::HashMap,
    fs,
    path::Path,
    process::{Command as Process, Stdio},
    time::{Duration, Instant},
};
type Result<T> = super::Result<T>;

const MANIFEST: &[u8] = include_bytes!("../../scenarios/scale-ladder-v7.json");

fn manifest() -> Result<Value> {
    Ok(serde_json::from_slice(MANIFEST)?)
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

/// Integer description of an independent inertial disc: position p (units),
/// velocity n / D (units per tick).
#[derive(Clone, Copy)]
pub(crate) struct Disc {
    pub(crate) p: [i128; 2],
    pub(crate) n: [i128; 2],
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

/// The execution modes. A mode that is not built yet reports NOT_ATTEMPTED.
fn make(mode: &str, w: World, keep: bool) -> std::result::Result<Box<dyn Stepper>, String> {
    match mode {
        "chronon" => Chronon::new(w, keep).map(|c| Box::new(c) as Box<dyn Stepper>).map_err(|e| e.to_string()),
        "event" => emergent_lattice_event::EventCore::new(w, keep).map(|c| Box::new(c) as Box<dyn Stepper>).map_err(|e| e.to_string()),
        "metal" => emergent_lattice_metal::MetalChronon::new(w, keep).map(|c| Box::new(c) as Box<dyn Stepper>).map_err(|e| e.to_string()),
        "hybrid" => crate::hybrid::Hybrid::new(w, keep).map(|c| Box::new(c) as Box<dyn Stepper>),
        "regions" => crate::regions::Regions::new(w, keep).map(|c| Box::new(c) as Box<dyn Stepper>),
        _ => Err(format!("mode {mode} not built yet")),
    }
}

fn discs_of(w: &World) -> Vec<Disc> {
    w.bodies.iter().map(|b| Disc { p: [(b.x[0] / w.q) as i128, (b.x[1] / w.q) as i128], n: [b.k[0] as i128, b.k[1] as i128] }).collect()
}

/// v4's X3 generator (ladder.rs x_crowded) as a lattice world.
fn crowded(n: u64, track: &Value, m: &Value) -> (World, i64) {
    let den = m["velocity_denominator"].as_i64().unwrap_or(1024);
    let radius = track["radius"].as_i64().unwrap_or(1);
    let s = track["spacing"].as_i64().unwrap_or(16) as i128;
    let half = (n / 2) as i128;
    let width = half * s;
    let speed = (den / 4) as i64;
    let mut rng = Rng(m["seed"].as_u64().unwrap_or(1) ^ n ^ 0xC0);
    let mut bodies = Vec::new();
    let mut push = |p: [i128; 2], k: [i64; 2]| {
        let id = bodies.len() as u64 + 1;
        bodies.push(Body::new(id, [p[0] as i64 * den, p[1] as i64 * den], k, 1, radius * den, Response::Pass));
    };
    for i in 0..half {
        let p = [i * s, rng.range(0, width)];
        push(p, [0, -speed]);
    }
    for j in 0..half {
        let dir = if rng.next() % 2 == 0 { 1 } else { -1 };
        let p = [rng.range(0, width), 2 * width + j * s];
        push(p, [dir * speed, 0]);
    }
    (World::new(den, None, bodies).expect("crowded world"), (4 * width) as i64)
}

/// Genesis world, horizon and the gas description (for the independent reference).
fn setup(track: &Value, i: usize, m: &Value) -> Result<(World, i64, Option<gas::Gas>)> {
    let seed = m["seed"].as_u64().unwrap_or(1);
    let den = m["velocity_denominator"].as_i64().unwrap_or(1024);
    let size = |k: &str| track[k][i].as_u64().ok_or("rung index");
    let (w, h, g) = match track["id"].as_str().unwrap_or("") {
        "X1-relative-motion" => {
            let area = track["area_per_body"].as_i64().unwrap_or(1_000_000);
            (worlds::random(size("bodies")?, area, den, track["radius"].as_i64().unwrap_or(1), seed, Response::Pass), track["horizon"].as_i64().unwrap_or(4096), None)
        }
        "X2-horizon" => {
            let area = track["area_per_body"].as_i64().unwrap_or(1_000_000);
            let n = track["bodies"].as_u64().unwrap_or(4096);
            (worlds::random(n, area, den, track["radius"].as_i64().unwrap_or(1), seed, Response::Pass), size("horizons")? as i64, None)
        }
        "X3-crowded-axes" => {
            let (w, h) = crowded(size("bodies")?, track, m);
            (w, h, None)
        }
        "C1-packed-stop-cascade" => (
            worlds::packed(size("bodies")?, track["grid_spacing"].as_i64().unwrap_or(8), track["jitter"].as_i64().unwrap_or(2), den, track["radius"].as_i64().unwrap_or(1), seed),
            track["horizon"].as_i64().unwrap_or(128),
            None,
        ),
        "C2-trapped-gas" | "X5-carry-endurance" => {
            let n = if track["id"] == "C2-trapped-gas" { size("bodies")? } else { track["bodies"].as_u64().unwrap_or(64) };
            let h = if track["id"] == "C2-trapped-gas" { track["horizon"].as_i64().unwrap_or(1024) } else { size("horizons")? as i64 };
            let (fill, q, vmax) = (track["fill"].as_f64().unwrap_or(0.1), track["quantum"].as_i64().unwrap_or(1024), track["vmax_units"].as_i64().unwrap_or(256));
            (worlds::gas(n, fill, q, vmax, seed), h, Some(gas::world(n, fill, q as i128, vmax as i128, seed)))
        }
        "C3-mixed-invariance" => (worlds::mixed(size("bodies")?, track["quantum"].as_i64().unwrap_or(512), seed), track["horizon"].as_i64().unwrap_or(2048), None),
        "C4-near-c-mixed" => {
            let q = track["quantum"].as_i64().unwrap_or(512);
            let mut w = worlds::mixed(size("bodies")?, q, seed);
            let lim = (95 * q / 100) as i128;
            for b in &mut w.bodies {
                b.response = Response::Bounce;
                b.k = [b.k[0] * 19 / 10, b.k[1] * 19 / 10];
                while (b.k[0] as i128).pow(2) + (b.k[1] as i128).pow(2) > lim * lim {
                    b.k = [b.k[0] * 9 / 10, b.k[1] * 9 / 10];
                }
            }
            (w, track["horizon"].as_i64().unwrap_or(2048), None)
        }
        "G1-galaxy-clusters" | "G2-galaxy-span" => {
            let g1 = track["id"] == "G1-galaxy-clusters";
            let n = if g1 { size("bodies")? } else { track["bodies"].as_u64().unwrap_or(65536) };
            let clusters = if g1 { size("clusters")? } else { track["clusters"].as_u64().unwrap_or(64) };
            let span = if g1 { track["span_bits"].as_u64().unwrap_or(30) } else { size("spans")? } as u32;
            let q = track["quantum"].as_i64().unwrap_or(256);
            let w = worlds::galaxy(n, clusters, span, q, seed).map_err(|e| format!("RANGE: {}", e.0))?;
            (w, track["horizon"].as_i64().unwrap_or(1024), None)
        }
        other => return Err(format!("track {other} has no lattice generator").into()),
    };
    let w = match m["law"].as_str() {
        Some("Relativistic") => w.with_law(Law::Relativistic)?,
        Some("RelativisticV1") => w.with_law(Law::RelativisticV1)?,
        _ => w,
    };
    Ok((w, h, g))
}

fn contact_pairs(s: &dyn Stepper) -> Vec<(u64, u64)> {
    let mut v: Vec<_> = s.log().events.iter().filter(|e| e.kind == Kind::Contact).map(|e| (e.a, e.b)).collect();
    v.sort_unstable();
    v.dedup();
    v
}

/// Child: one (mode, track, rung). Prints the JSON row as the last stdout line.
pub fn rung(args: Vec<String>) -> Result<()> {
    let mut m = manifest()?;
    let (mode, track_id) = (args.first().ok_or("mode")?.clone(), args.get(1).ok_or("track")?.clone());
    let i: usize = args.get(2).ok_or("rung index")?.parse()?;
    let profile = args.get(3).map(String::as_str).unwrap_or("quick");
    let c = caps(&m, profile);
    m["caps"] = c.clone();
    let track = m["tracks"].as_array().ok_or("tracks")?.iter().find(|t| t["id"] == track_id.as_str()).ok_or("unknown track")?.clone();
    if track_id == "X4-near-miss-lattice" {
        println!("{}", json!({"status": "NOT_SUPPORTED", "limiter": "groups (families) are not in the lattice laws yet"}));
        return Ok(());
    }
    let t = Instant::now();
    let (w0, horizon, g) = match setup(&track, i, &m) {
        Ok(v) => v,
        Err(e) if e.to_string().starts_with("RANGE: ") => {
            let why = e.to_string();
            println!("{}", json!({"status": "NOT_SUPPORTED", "limiter": format!("coordinate range: {} (needs wide region origins, docs/universe-quanta.md stage 3)", &why[7..])}));
            return Ok(());
        }
        Err(e) => return Err(e),
    };
    let n = w0.bodies.len() as u64;
    let unit_ops = m["units"]["unit_ops"].as_u64().unwrap_or(4096);
    let pair_ticks = n as f64 * n as f64 / 2.0 * horizon as f64;
    let reference_ok = g.is_some() && pair_ticks <= c["reference_max_pair_ticks"].as_f64().unwrap_or(5e7);
    let pass_track = track["response"] == "Pass";
    let keep = pass_track || reference_ok || (track_id == "C1-packed-stop-cascade" && n <= 1024);
    let mut s = match make(&mode, w0.clone(), keep) {
        Ok(s) => s,
        Err(e) => {
            println!("{}", json!({"status": "NOT_ATTEMPTED", "limiter": e}));
            return Ok(());
        }
    };
    let setup_ms = t.elapsed().as_secs_f64() * 1e3;
    let wall = c["wall_seconds_per_rung"].as_f64().unwrap_or(120.0);
    let d = drive(s.as_mut(), horizon, unit_ops, wall, c["peak_rss_bytes"].as_u64().unwrap_or(u64::MAX));
    let mut units = d.units_ms.clone();
    units.sort_by(|a, b| a.total_cmp(b));
    let max_unit = units.last().copied().unwrap_or(0.0);
    let target = m["units"]["target_max_unit_ms"].as_f64().unwrap_or(5.0);
    let met = s.metrics().clone();
    let mut correct = json!({});
    let mut ok = d.complete;
    if d.complete {
        let w = s.world();
        let den = w0.q as i128;
        match track["response"].as_str().unwrap_or("") {
            "Pass" => {
                let discs = discs_of(&w0);
                let reach = 2 * track["radius"].as_i64().unwrap_or(1) as i128;
                let mine = contact_pairs(s.as_ref());
                let oracle = if track_id == "X3-crowded-axes" { vec![] } else { oracle_pairs(&discs, den, reach, horizon as i128) };
                let brute = if n <= 4096 { Some(brute_pairs(&discs, den, reach, horizon as i128) == oracle) } else { None };
                ok &= mine == oracle && brute != Some(false);
                correct = json!({"contacts": mine.len(), "oracle_contacts": oracle.len(), "equal": mine == oracle, "brute_force_agrees": brute});
            }
            "Stop" => {
                correct["contacts"] = json!(s.log().contacts);
                if mode == "chronon" && n <= c["audit_max_bodies"].as_u64().unwrap_or(64) {
                    let (bw, blog) = lattice::all_pairs(w0.clone(), horizon);
                    let eq = bw == w && blog.sorted() == s.log().sorted();
                    correct["all_pairs_audit_equal"] = json!(eq);
                    ok &= eq;
                }
            }
            "Bounce" if w.law.subluminal() => {
                let (t0, t1, cr) = (relativity::total(&w0), relativity::total(&w), relativity::carried(&w));
                let energy_ok = t1[0] - t0[0] == cr[0];
                let momentum_ok = (0..2).all(|a| t1[1 + a] - t0[1 + a] + w.wall_momentum[a] as i128 == cr[1 + a]);
                let q2 = (w.q as i128).pow(2);
                let below_c = w.bodies.iter().all(|b| (b.k[0] as i128).pow(2) + (b.k[1] as i128).pow(2) < q2);
                let gmax = w0.bodies.iter().chain(&w.bodies).map(|b| relativity::gamma(b.k, w.q)).max().unwrap_or(relativity::F);
                let mmax = w.bodies.iter().map(|b| b.mass).max().unwrap_or(1);
                // The law's 4-momentum scale: F in v0, 2Q in v1 (carry_bound in the manifest).
                let scale = if w.law == Law::RelativisticV1 { 2.0 * w.q as f64 } else { relativity::F as f64 };
                let bound = 64.0 * scale * mmax as f64 * (gmax as f64 / relativity::F as f64).powi(3);
                let max_carry = w.bodies.iter().flat_map(|b| [b.residual, b.carry[0], b.carry[1]]).map(|v| v.unsigned_abs()).max().unwrap_or(0) as f64;
                let contained = w.container.is_none_or(|cont| {
                    let kmax1 = w.bodies.iter().map(|b| b.k[0].abs().max(b.k[1].abs())).max().unwrap_or(0);
                    w.bodies.iter().all(|b| (0..2).all(|a| b.x[a] >= cont.min[a] - kmax1 && b.x[a] <= cont.max[a] + kmax1))
                });
                ok &= energy_ok && momentum_ok && below_c && max_carry <= bound && contained;
                correct = json!({"contacts": s.log().contacts, "walls": s.log().walls, "energy_ledger_exact": energy_ok, "momentum_ledger_exact": momentum_ok,
                    "below_c": below_c, "max_carry": max_carry, "carry_bound": bound, "gamma_max": gmax as f64 / relativity::F as f64, "contained": contained});
                if reference_ok {
                    let (eq, detail) = lattice::gas_rel_equal(g.as_ref().expect("gas"), horizon, &w, s.log());
                    correct["reference_equal"] = json!(eq);
                    correct["reference"] = detail;
                    ok &= eq;
                }
            }
            "Bounce" => {
                let (e0, e1) = (w0.energy(), w.energy());
                let (p0, p1) = (w0.momentum(), w.momentum());
                let energy_ok = e1 - e0 == w.residual();
                let momentum_ok = p1[0] - p0[0] + w.wall_momentum[0] as i128 == 0 && p1[1] - p0[1] + w.wall_momentum[1] as i128 == 0;
                let kmax0 = w0.bodies.iter().map(|b| b.k[0].abs().max(b.k[1].abs())).max().unwrap_or(0) as i128;
                let max_res = w.bodies.iter().map(|b| (b.residual as i128).abs()).max().unwrap_or(0);
                let residual_ok = max_res * max_res <= 128 * kmax0 * kmax0;
                let kmax1 = w.bodies.iter().map(|b| b.k[0].abs().max(b.k[1].abs())).max().unwrap_or(0);
                let cont = w.container.expect("gas box");
                let contained = w.bodies.iter().all(|b| (0..2).all(|a| b.x[a] >= cont.min[a] - kmax1 && b.x[a] <= cont.max[a] + kmax1));
                let v4_inside = w.bodies.iter().all(|b| (0..2).all(|a| b.x[a] >= cont.min[a] && b.x[a] <= cont.max[a]));
                ok &= energy_ok && momentum_ok && residual_ok && contained;
                correct = json!({"contacts": s.log().contacts, "walls": s.log().walls, "energy_ledger_exact": energy_ok, "momentum_ledger_exact": momentum_ok,
                    "max_residual": max_res as f64, "residual_bound": (128.0 * (kmax0 * kmax0) as f64).sqrt(), "contained": contained, "centres_inside_box": v4_inside,
                    "energy_drift_relative": (e1 - e0) as f64 / e0 as f64});
                if reference_ok {
                    let (eq, detail) = lattice::gas_reference_equal(g.as_ref().expect("gas"), horizon, &w, s.log());
                    correct["reference_equal"] = json!(eq);
                    correct["reference"] = detail;
                    ok &= eq;
                }
            }
            _ => correct["contacts"] = json!(s.log().contacts),
        }
        // Mode invariance against the chronon reference.
        if mode != "chronon" && n as f64 * horizon as f64 <= c["mode_invariance_max_body_ticks"].as_f64().unwrap_or(2e7) {
            let mut r = Chronon::new(w0.clone(), false)?;
            r.run_to(horizon);
            let eq = r.outcome() == s.outcome();
            correct["chronon_digests_equal"] = json!(eq);
            ok &= eq;
        }
        // Budget invariance.
        if n <= c["budget_invariance_max_bodies"].as_u64().unwrap_or(1024) {
            let mut all = true;
            for b in m["budget_invariance_unit_ops"].as_array().into_iter().flatten() {
                let b = b.as_u64().unwrap_or(64);
                if b == unit_ops {
                    continue;
                }
                let mut r = make(&mode, w0.clone(), false)?;
                while r.tick() < horizon {
                    r.advance(horizon, b);
                }
                all &= r.outcome() == s.outcome();
            }
            correct["budget_invariance"] = json!(all);
            ok &= all;
        }
    }
    let fired = met.fired.max(1) as f64;
    let row = json!({
        "mode": mode, "status": if ok { "PASS" } else { "FAIL" },
        "limiter": d.limiter.clone().or_else(|| if ok { None } else { Some("correctness".into()) }),
        "bodies": n, "horizon": horizon, "correctness": correct,
        "setup_ms": setup_ms, "advance_ms": d.advance_ms, "ticks_reached": s.tick(),
        "chronons_per_second": s.tick() as f64 / (d.advance_ms / 1e3).max(1e-9),
        "units": d.units_ms.len(), "unit_ops": unit_ops,
        "unit_ms_p50": percentile(&units, 0.5), "unit_ms_p99": percentile(&units, 0.99), "unit_ms_max": max_unit,
        "units_over_target": units.iter().filter(|&&u| u > target).count(),
        "smoothness": if max_unit <= target { "SMOOTH" } else { "JANK" },
        "ops": met.ops, "predicates": met.predicates, "fired": met.fired,
        "ops_per_event": met.ops as f64 / fired, "predicates_per_op": met.predicates as f64 / met.ops.max(1) as f64,
        "metrics": serde_json::to_value(&met)?,
        "cores_used": d.cpu_s / (d.advance_ms / 1e3).max(1e-9),
        "cores_available": std::thread::available_parallelism().map(|n| n.get()).unwrap_or(1),
        "peak_rss_bytes": peak_rss(),
    });
    println!("{}", serde_json::to_string(&row)?);
    Ok(())
}

fn rung_count(track: &Value) -> usize {
    ["bodies", "horizons", "lanes_per_axis", "spans"].iter().find_map(|k| track[*k].as_array().map(Vec::len)).unwrap_or(0)
}

fn rung_size(track: &Value, i: usize) -> f64 {
    ["bodies", "horizons", "lanes_per_axis", "spans"].iter().find_map(|k| track[*k].as_array().and_then(|a| a[i].as_f64())).unwrap_or(0.0)
}

/// Frozen track gates (step exit criteria) over the climbed rows.
fn gates(m: &Value, rows: &[Value]) -> Value {
    let g = &m["track_gates"];
    let mut out = serde_json::Map::new();
    let passing = |mode: &str, track: &str| -> Vec<&Value> {
        rows.iter().filter(|r| r["mode"] == mode && r["track"] == track && r["status"] == "PASS").collect()
    };
    let mut flat = vec![];
    for mode in g["cost_per_event_flat"]["modes"].as_array().into_iter().flatten().filter_map(Value::as_str) {
        for track in g["cost_per_event_flat"]["tracks"].as_array().into_iter().flatten().filter_map(Value::as_str) {
            let p = passing(mode, track);
            let v = match (p.first(), p.last()) {
                (Some(a), Some(b)) if p.len() >= 2 => {
                    let growth = b["ops_per_event"].as_f64().unwrap_or(f64::MAX) / a["ops_per_event"].as_f64().unwrap_or(1.0);
                    json!({"mode": mode, "track": track, "growth": growth, "status": if growth <= g["cost_per_event_flat"]["max_growth"].as_f64().unwrap_or(2.0) { "PASS" } else { "FAIL" }})
                }
                _ => json!({"mode": mode, "track": track, "status": "NOT_ATTEMPTED", "limiter": "fewer than two passing rungs"}),
            };
            flat.push(v);
        }
    }
    out.insert("cost_per_event_flat".into(), json!(flat));
    let mut useful = vec![];
    for mode in g["useful_work"]["modes"].as_array().into_iter().flatten().filter_map(Value::as_str) {
        let min = g["useful_work"]["min_predicates_per_op"].as_f64().unwrap_or(0.5);
        let rs: Vec<&Value> = rows.iter().filter(|r| r["mode"] == mode && r["status"] == "PASS" && r["fired"].as_u64().unwrap_or(0) >= 1000).collect();
        let worst = rs.iter().map(|r| r["predicates_per_op"].as_f64().unwrap_or(0.0)).fold(f64::MAX, f64::min);
        useful.push(if rs.is_empty() {
            json!({"mode": mode, "status": "NOT_ATTEMPTED"})
        } else {
            json!({"mode": mode, "worst_predicates_per_op": worst, "status": if worst >= min { "PASS" } else { "FAIL" }})
        });
    }
    out.insert("useful_work".into(), json!(useful));
    let mut smooth = vec![];
    for mode in g["smooth"]["modes"].as_array().into_iter().flatten().filter_map(Value::as_str) {
        let rs: Vec<&Value> = rows.iter().filter(|r| r["mode"] == mode && r["status"] == "PASS").collect();
        let jank: Vec<String> = rs.iter().filter(|r| r["smoothness"] != "SMOOTH").map(|r| format!("{} {}", r["track"].as_str().unwrap_or("?"), r["size"])).collect();
        smooth.push(if rs.is_empty() {
            json!({"mode": mode, "status": "NOT_ATTEMPTED"})
        } else {
            json!({"mode": mode, "status": if jank.is_empty() { "PASS" } else { "FAIL" }, "jank_rungs": jank})
        });
    }
    out.insert("smooth".into(), json!(smooth));
    if let Some(gm) = g.get("gas_one_million") {
        let n = gm["bodies"].as_f64().unwrap_or(1048576.0);
        let hit: Vec<&str> = rows.iter().filter(|r| r["track"] == gm["track"] && r["size"].as_f64() == Some(n) && r["status"] == "PASS").filter_map(|r| r["mode"].as_str()).collect();
        out.insert("gas_one_million".into(), json!({"status": if hit.is_empty() { "FAIL" } else { "PASS" }, "passing_modes": hit}));
    }
    if let Some(gm) = g.get("galaxy_one_million") {
        let n = gm["bodies"].as_f64().unwrap_or(1048576.0);
        let hit: Vec<&str> = rows.iter().filter(|r| r["track"] == gm["track"] && r["size"].as_f64() == Some(n) && r["status"] == "PASS").filter_map(|r| r["mode"].as_str()).collect();
        out.insert("galaxy_one_million".into(), json!({"status": if hit.is_empty() { "FAIL" } else { "PASS" }, "passing_modes": hit}));
    }
    if let Some(es) = g.get("empty_space_free") {
        let mut v = vec![];
        for mode in es["modes"].as_array().into_iter().flatten().filter_map(Value::as_str) {
            let p = passing(mode, es["track"].as_str().unwrap_or(""));
            v.push(match (p.first(), p.last()) {
                (Some(a), Some(b)) if p.len() >= 2 => {
                    let growth = b["advance_ms"].as_f64().unwrap_or(f64::MAX) / a["advance_ms"].as_f64().unwrap_or(1.0).max(1e-9);
                    json!({"mode": mode, "spans": [a["size"], b["size"]], "growth": growth, "status": if growth <= es["max_growth"].as_f64().unwrap_or(1.5) { "PASS" } else { "FAIL" }})
                }
                _ => json!({"mode": mode, "status": "NOT_ATTEMPTED", "limiter": "fewer than two passing spans"}),
            });
        }
        out.insert("empty_space_free".into(), json!(v));
    }
    Value::Object(out)
}

/// Parent: for each mode, climb every track until a rung fails.
pub fn run(out: &Path, modes: &[String], only: Option<&str>, profile: &str) -> Result<Value> {
    let m = manifest()?;
    let c = caps(&m, profile);
    let exe = std::env::current_exe()?;
    let wall = c["wall_seconds_per_rung"].as_f64().unwrap_or(120.0);
    let rss_cap = c["peak_rss_bytes"].as_f64().unwrap_or(f64::MAX);
    let budget = c["ladder_seconds"].as_f64().unwrap_or(f64::MAX);
    let start = Instant::now();
    let mut rows: Vec<Value> = Vec::new();
    for mode in modes {
        for track in m["tracks"].as_array().ok_or("tracks")? {
            let id = track["id"].as_str().unwrap_or("?");
            if only.is_some_and(|o| o != id) {
                continue;
            }
            let mut previous: Option<(f64, f64)> = None;
            let mut failed: Option<String> = None;
            for i in 0..rung_count(track) {
                let size = rung_size(track, i);
                let base = json!({"mode": mode, "track": id, "rung": i, "size": size});
                let skip = |limiter: String| {
                    let mut r = base.clone();
                    r["status"] = json!("NOT_ATTEMPTED");
                    r["limiter"] = json!(limiter);
                    r
                };
                if let Some(f) = &failed {
                    rows.push(skip(f.clone()));
                    continue;
                }
                if start.elapsed().as_secs_f64() > budget {
                    rows.push(skip(format!("ladder time budget {budget} s ({profile} profile)")));
                    continue;
                }
                if let Some((ps, prss)) = previous {
                    if track["bodies"].is_array() && prss * size / ps > rss_cap {
                        rows.push(skip(format!("projected peak RSS {:.0} MB over cap", prss * size / ps / 1e6)));
                        failed = Some("an earlier rung failed".into());
                        continue;
                    }
                }
                eprintln!("v7 {mode} {id} #{i} (size {size})");
                let started = Instant::now();
                let mut child = Process::new(&exe).args(["ladder7-rung", mode, id, &i.to_string(), profile]).stdout(Stdio::piped()).stderr(Stdio::inherit()).spawn()?;
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
                for (k, v) in base.as_object().into_iter().flatten() {
                    value[k] = v.clone();
                }
                value["child_wall_s"] = json!(started.elapsed().as_secs_f64());
                match value["status"].as_str() {
                    Some("PASS") => {}
                    Some("NOT_ATTEMPTED") | Some("NOT_SUPPORTED") => failed = Some(value["limiter"].as_str().unwrap_or("not attempted").to_string()),
                    _ => failed = Some("an earlier rung failed".into()),
                }
                previous = value["peak_rss_bytes"].as_f64().map(|rss| (size, rss));
                rows.push(value);
                fs::write(out.join("rows.partial.json"), serde_json::to_vec_pretty(&rows)?)?;
            }
        }
    }
    Ok(json!({
        "schema": 7, "manifest": "scenarios/scale-ladder-v7.json", "profile": profile, "modes": modes,
        "ladder_seconds": start.elapsed().as_secs_f64(),
        "manifest_blake3": blake3::hash(MANIFEST).to_hex().to_string(),
        "provenance": provenance(),
        "gates": gates(&m, &rows),
        "rows": rows,
        "accounting": "Each (mode, track, rung) ran in a fresh child process; peak RSS is that process's getrusage maximum. Every unit of unit_ops charged operations was timed. Oracles, audits and invariance reruns run after the timed advance and are excluded from advance_ms.",
    }))
}

/// Revision, working-tree state and machine of a ladder run.
pub fn provenance() -> Value {
    let shell = |program: &str, args: &[&str]| {
        Process::new(program)
            .args(args)
            .output()
            .ok()
            .filter(|o| o.status.success())
            .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
            .unwrap_or_default()
    };
    let diff = Process::new("git").args(["diff", "HEAD"]).output().map(|o| o.stdout).unwrap_or_default();
    json!({"revision": shell("git", &["rev-parse", "HEAD"]), "working_tree_status": shell("git", &["status", "--porcelain"]),
        "working_tree_diff_hash": blake3::hash(&diff).to_hex().to_string(),
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "unix_seconds": std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).map(|d| d.as_secs()).unwrap_or(0),
        "rustc": shell("rustc", &["--version"]), "hardware": shell("sysctl", &["-n", "machdep.cpu.brand_string"]),
        "memory_bytes": shell("sysctl", &["-n", "hw.memsize"]), "manifest_hash": blake3::hash(MANIFEST).to_hex().to_string()})
}
