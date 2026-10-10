//! Second author on 20261010-0100-fermi-c11c (Fermi lens, silver): the checker's named
//! experiment. Open the resolver and attribute the measured per-distinct-kick cost
//! (compile vs bind vs arithmetic vs readout vs forces), then price one amortization on
//! the shipped law — N co-orbital bodies sharing one compiled cycle — against the >= 40x
//! bar (the 1.5 us/kick the 10^9 low-orbit budget needs at rtf 100 on 8 cores).
//!
//! Everything here drives the shipped crates through their public APIs only; no crate is
//! edited. The plane replay replicates xtask's kick_bench loop exactly (same script, same
//! frame cadence), so the replay digest must equal the shipped bench's digest: the
//! attribution then provably covers the same kicks the record measured.
//!
//! Modes:
//!   plane <seed> <seconds> <rtf>      replay + attribution on the shipped plane scene
//!   coorbital <n> <seconds> <rtf> <radius_root>  restricted scene: n ships on one circle
use emergent_space::binding::{IntegerState, Rebinding, Trajectory};
use emergent_space::orbit::{MemoCode, Orbit, OrbitKey, QuantizedMemo, ShapeKey, ShapeMemo};
use emergent_universe::body::{Item, What};
use emergent_universe::ctx::Ctx;
use emergent_universe::fleet::Order;
use emergent_universe::num::{norm2, scale2, sub2, time_of, Error, Res, Tick, V2};
use emergent_universe::scenario::{plane, restricted};
use emergent_universe::{bind, force, step, Budget, Config, Kind, Mass, Universe};
use serde_json::json;
use std::collections::HashSet;
use std::hint::black_box;
use std::time::Instant;

const REPS: usize = 5; // min-of-5 per kick per bucket

/// The kicker's script, copied verbatim from xtask/src/universe/mod.rs (it is private there).
fn script(frame: usize) -> u8 {
    let slot = frame / 240;
    if frame % 240 < 20 {
        [1, 9, 2, 4, 1, 1 | 4, 2, 8][slot % 8]
    } else {
        0
    }
}

/// Sigma-delta quantize, replicated from step.rs (private there): add `dv` to the carry in
/// 2^-16 of the quantum 2^exp, return whole quanta and the new carry.
fn quantize_replica(dv: V2, exp: i16, carry: [i64; 2]) -> Res<([i64; 2], [i64; 2])> {
    let mut out = [0i64; 2];
    let mut rem = carry;
    for c in 0..2 {
        let inc = dv[c].fixed(16 - exp as i32)?;
        let total = carry[c] as i128 + inc;
        out[c] = i64::try_from(total / 65536).map_err(|_| Error::Refused("kick outside the word"))?;
        rem[c] = (total % 65536) as i64;
    }
    Ok((out, rem))
}

/// step.rs's `passage_edge` (pub(crate) there): ships in a child doll compile passages out
/// to twice the doll's edge.
fn passage_edge(ctx: &Ctx, doll: u16) -> Option<emergent_space::orbit::Scalar> {
    (doll != 0).then(|| ctx.dolls[doll as usize].edge.scale(2).ok()).flatten()
}

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
enum Bucket {
    Process,    // the shipped bench's number: whole step::process
    Readout,    // drift readout (tube decode + turn + residual)
    Scalars,    // int -> scalars
    Secondaries, // reading the other bodies' tubes (force inputs)
    Tide,       // the parent's tide (kick path)
    Certs,      // surface / crash certificates (clock path)
    Field,      // force::field / force::acceleration
    Extmath,    // the clock law's time transformation, dv, p_t
    Quantize,   // sigma-delta
    Bind,       // the whole rebind compile: bind::bind
    FromState,  // Rebinding::from_state (fit + compile + phase)
    Compile,    // Orbit::compile / Passage::compile alone (the shareable part)
    MemoHitE,   // warm ShapeMemo (exact key) lookup
    MemoHitQ,   // warm QuantizedMemo (12+12-bit law key) lookup
    Plan,       // the clock path's next-step planning (kepler + ticks)
    Tau,        // rebind's proper-time bookkeeping (orbit_state decodes)
    StepFor,    // step_for (the split's step choice, kick path)
}

const BUCKETS: [Bucket; 17] = [
    Bucket::Process, Bucket::Readout, Bucket::Scalars, Bucket::Secondaries, Bucket::Tide,
    Bucket::Certs, Bucket::Field, Bucket::Extmath, Bucket::Quantize, Bucket::Bind,
    Bucket::FromState, Bucket::Compile, Bucket::MemoHitE, Bucket::MemoHitQ, Bucket::Plan,
    Bucket::Tau, Bucket::StepFor,
];

struct Stats {
    per_kick: Vec<([f64; 17], bool)>, // us, min-of-REPS, one row per distinct kick; bool: leaver
    cycles: u64,
    passages: u64,
    no_rebind: u64,
    clock_path: u64,
    kick_path: u64,
    thrusting: u64,
    exact: HashSet<ShapeKey>,
    quantized: HashSet<u64>,
    digest: blake3::Hasher,
    refused: usize,
}

fn ix(b: Bucket) -> usize {
    BUCKETS.iter().position(|&x| x == b).unwrap()
}

impl Stats {
    fn new() -> Self {
        Self {
            per_kick: Vec::new(),
            cycles: 0, passages: 0, no_rebind: 0, clock_path: 0, kick_path: 0, thrusting: 0,
            exact: HashSet::new(), quantized: HashSet::new(),
            digest: blake3::Hasher::new(), refused: 0,
        }
    }

    fn note_shape(&mut self, t: &Trajectory) {
        let Trajectory::Cycle(c) = t else {
            self.passages += 1;
            return;
        };
        self.cycles += 1;
        let key = c.key();
        if let Ok(k) = ShapeKey::for_orbit(key) {
            self.exact.insert(k);
        }
        if let Ok(c) = MemoCode::encode(key) {
            self.quantized.insert(c.bits());
        }
    }
}


fn min_of<R>(reps: usize, mut f: impl FnMut() -> R) -> f64 {
    let mut best = f64::INFINITY;
    for _ in 0..reps {
        let t0 = Instant::now();
        black_box(f());
        let us = t0.elapsed().as_secs_f64() * 1e6;
        if us < best {
            best = us;
        }
    }
    best
}

/// Attribute one distinct pending ship kick, exactly as the shipped bench sees it, and
/// re-time each sub-phase of the path it took.
fn attribute(u: &Universe, i: usize, made_n: usize, rec0: emergent_universe::body::BodyRec, item: Item, st_stats: &mut Stats) {
    let ctx = u.ctx();
    let t = item.t;
    let mut row = [0.0f64; 17];
    let leaver = i >= made_n;

    // The shipped number first (one faithful call; the Update is the record's).
    let t0 = Instant::now();
    let upd = step::process(&ctx, i, rec0.clone());
    row[ix(Bucket::Process)] = t0.elapsed().as_secs_f64() * 1e6;
    row[ix(Bucket::Process)] = row[ix(Bucket::Process)].min(min_of(REPS, || step::process(&ctx, i, rec0.clone())));
    st_stats.refused += usize::from(upd.kind != step::Resolved::Kick);
    st_stats.digest.update(format!("{i} {item:?} {:?}", upd.rec).as_bytes());
    if let Some(e) = &upd.new_entry {
        st_stats.note_shape(&e.trajectory);
    }

    let d = rec0.b.doll;
    let level = if let What::Kick(l) = item.what { l } else { 0 };
    let thrusting = rec0.thrust.is_some_and(|th| th.keys != 0);
    if thrusting {
        st_stats.thrusting += 1;
    }

    // ---- the path split, as process() takes it ----
    let st = rec0.b.readout(t).expect("readout");
    row[ix(Bucket::Readout)] = min_of(REPS, || rec0.b.readout(t).unwrap());
    let (x, _v) = bind::scalars(&st).expect("scalars");
    row[ix(Bucket::Scalars)] = min_of(REPS, || bind::scalars(&st).unwrap());
    let secs = ctx.secondaries(d, t, i).expect("secondaries");
    row[ix(Bucket::Secondaries)] = min_of(REPS, || ctx.secondaries(d, t, i).unwrap());

    let next: IntegerState;
    let fired: bool;
    if rec0.ext.is_some() {
        st_stats.clock_path += 1;
        // kick_clock (docs/law.md motion v2): the ships of the root doll.
        let sources: Vec<usize> = ctx.sources[d as usize].iter().copied().filter(|&j| j != i).collect();
        row[ix(Bucket::Certs)] = min_of(REPS, || {
            let mut hit = 0;
            for (s, &j) in secs.iter().zip(sources.iter()) {
                if let Some(radius) = ctx.surface_in(j, d).unwrap() {
                    if norm2(sub2(s.pos, x).unwrap()).unwrap() < radius {
                        hit += 1;
                    }
                }
            }
            hit
        });
        let ext0 = rec0.ext.expect("clock-stepped");
        let f = force::field(&secs, x).expect("field");
        row[ix(Bucket::Field)] = min_of(REPS, || force::field(&secs, x).unwrap());
        let w = ext0.time(ext0.y(f.potential).unwrap(), ext0.ds).unwrap();
        row[ix(Bucket::Extmath)] = min_of(REPS, || {
            let e = ext0;
            e.time(e.y(f.potential).unwrap(), e.ds).unwrap()
        });
        let dv = scale2(f.accel, w).expect("dv");
        row[ix(Bucket::Extmath)] += min_of(REPS, || scale2(f.accel, w).unwrap());
        if !thrusting {
            let (dvq, _carry) = quantize_replica(dv, st.velocity_exponent, rec0.carry).expect("quantize");
            row[ix(Bucket::Quantize)] = min_of(REPS, || quantize_replica(dv, st.velocity_exponent, rec0.carry).unwrap());
            let mut ext = ext0;
            ext.add_pt(w.mul(f.rate).unwrap()).expect("pt");
            row[ix(Bucket::Extmath)] += min_of(REPS, || {
                let mut e = ext0;
                e.add_pt(w.mul(f.rate).unwrap()).unwrap()
            });
            next = IntegerState { velocity: [st.velocity[0] + dvq[0], st.velocity[1] + dvq[1]], ..st };
            fired = next.velocity != st.velocity;
        } else {
            // The burn path needs Work::burn's proper-time bookkeeping; the record's plane
            // bench has the player excluded (Kind::Ship only) and no thrusting ship is
            // expected. If one appears, its row keeps the buckets it shares and is counted.
            next = st;
            fired = false;
        }
        if fired {
            let clock_exp = ctx.dolls[d as usize].clock_exp();
            let unit = ctx.tube_unit(i, d).expect("unit");
            let edge = passage_edge(&ctx, d);
            row[ix(Bucket::Bind)] = min_of(REPS, || bind::bind(next, t, clock_exp, edge, unit).unwrap());
            row[ix(Bucket::FromState)] = min_of(REPS, || {
                Rebinding::from_state(next, time_of(t, clock_exp).unwrap(), edge).unwrap()
            });
        }
        // Planning: the next fictitious step from the post-kick state.
        let (x2, v2) = bind::scalars(&next).unwrap();
        let mu = ctx.tube_unit(i, d).unwrap().mu;
        let ext0b = rec0.ext.expect("clock-stepped");
        let y = ext0b
            .y(force::kepler(x2, v2, mu).unwrap().add(ext0b.pt_value().unwrap()).unwrap())
            .unwrap();
        row[ix(Bucket::Plan)] = min_of(REPS, || {
            let e = ext0b;
            e.y(force::kepler(x2, v2, mu).unwrap().add(e.pt_value().unwrap()).unwrap()).unwrap()
        });
        let clock_exp = ctx.dolls[d as usize].clock_exp();
        row[ix(Bucket::Plan)] += min_of(REPS, || {
            let mut e = ext0b;
            e.ticks(e.time(y, e.ds).unwrap(), clock_exp).unwrap()
        });
    } else {
        st_stats.kick_path += 1;
        // The split's kick (leavers, planets' dolls).
        let tide = ctx.tide(d, t).expect("tide");
        row[ix(Bucket::Tide)] = min_of(REPS, || ctx.tide(d, t).unwrap());
        let a = force::acceleration(level, x, &secs, tide).expect("accel");
        row[ix(Bucket::Field)] = min_of(REPS, || force::acceleration(level, x, &secs, tide).unwrap());
        let h = time_of(rec0.interval >> (2 * level as i64), rec0.b.clock_exp).expect("h");
        let dv = scale2(a, h).expect("dv");
        row[ix(Bucket::Extmath)] = min_of(REPS, || {
            let h = time_of(rec0.interval >> (2 * level as i64), rec0.b.clock_exp).unwrap();
            scale2(a, h).unwrap()
        });
        let (dvq, _carry) = quantize_replica(dv, st.velocity_exponent, rec0.carry).expect("quantize");
        row[ix(Bucket::Quantize)] = min_of(REPS, || quantize_replica(dv, st.velocity_exponent, rec0.carry).unwrap());
        next = IntegerState { velocity: [st.velocity[0] + dvq[0], st.velocity[1] + dvq[1]], ..st };
        fired = next.velocity != st.velocity;
        if fired {
            let clock_exp = ctx.dolls[d as usize].clock_exp();
            let unit = ctx.tube_unit(i, d).expect("unit");
            let edge = passage_edge(&ctx, d);
            row[ix(Bucket::Bind)] = min_of(REPS, || bind::bind(next, t, clock_exp, edge, unit).unwrap());
            row[ix(Bucket::FromState)] = min_of(REPS, || {
                Rebinding::from_state(next, time_of(t, clock_exp).unwrap(), edge).unwrap()
            });
        }
    }
    if !fired {
        st_stats.no_rebind += 1;
    }

    // rebind's proper-time bookkeeping: two more decodes of the old binding (orbit_state).
    if fired {
        row[ix(Bucket::Tau)] = min_of(REPS, || {
            rec0.b.orbit_state(t).unwrap();
            rec0.b.orbit_state(rec0.b.event_time).unwrap();
        });
    }
    // the split's step choice (kick path: plan_interval calls step_for on the new binding).
    if rec0.ext.is_none() && fired {
        let new_b = &upd.rec.b;
        let edge = (new_b.doll != 0 && matches!(rec0.kind, Kind::Ship | Kind::Player))
            .then(|| ctx.dolls[new_b.doll as usize].edge);
        row[ix(Bucket::StepFor)] = min_of(REPS, || step::step_for(new_b, ctx.cfg.step_log2, edge).unwrap());
    }

    // ---- the shareable part: the compiled cycle / passage itself ----
    if let Some(e) = &upd.new_entry {
        let edge = passage_edge(&ctx, d);
        match &e.trajectory {
            Trajectory::Cycle(c) => {
                let key: OrbitKey = c.key();
                row[ix(Bucket::Compile)] = min_of(REPS, || Orbit::compile(key).unwrap());
                let mut qm = QuantizedMemo::default();
                let mut sm = ShapeMemo::default();
                qm.get(key).expect("quantized warm");
                sm.get(key).expect("shape warm");
                row[ix(Bucket::MemoHitQ)] = min_of(REPS, || qm.get(key).unwrap().key());
                row[ix(Bucket::MemoHitE)] = min_of(REPS, || sm.get(key).unwrap().key());
            }
            Trajectory::Passage(p) => {
                let key = p.key();
                let r = p.key().periapsis;
                let outer = edge.unwrap_or(r);
                row[ix(Bucket::Compile)] = min_of(REPS, || emergent_space::orbit::Passage::compile(key, outer).unwrap());
            }
        }
    }
    st_stats.per_kick.push((row, leaver));
}

fn percentiles(mut v: Vec<f64>) -> serde_json::Value {
    v.sort_by(f64::total_cmp);
    let at = |p: f64| v.get(((v.len().saturating_sub(1)) as f64 * p).ceil() as usize).copied().unwrap_or(0.0);
    json!({"median": at(0.5), "p99": at(0.99), "mean": v.iter().sum::<f64>() / v.len().max(1) as f64, "samples": v.len()})
}

fn med_of(rows: &[[f64; 17]], bk: Bucket) -> f64 {
    let mut v: Vec<f64> = rows.iter().map(|r| r[ix(bk)]).collect();
    v.sort_by(f64::total_cmp);
    v.get(v.len().saturating_sub(1) / 2).copied().unwrap_or(0.0)
}

const NAMES: [(&str, Bucket); 17] = [
    ("process", Bucket::Process), ("readout", Bucket::Readout), ("scalars", Bucket::Scalars),
    ("secondaries", Bucket::Secondaries), ("tide", Bucket::Tide), ("certs", Bucket::Certs),
    ("field", Bucket::Field), ("extmath", Bucket::Extmath), ("quantize", Bucket::Quantize),
    ("bind", Bucket::Bind), ("from_state", Bucket::FromState), ("compile", Bucket::Compile),
    ("memo_hit_exact", Bucket::MemoHitE), ("memo_hit_quantized", Bucket::MemoHitQ), ("plan", Bucket::Plan),
    ("tau", Bucket::Tau), ("step_for", Bucket::StepFor),
];

fn table_for(rows: &[[f64; 17]]) -> serde_json::Value {
    let proc = med_of(rows, Bucket::Process);
    let mut t = serde_json::Map::new();
    for (name, bk) in NAMES {
        // medians over the rows that filled the bucket (each path fills its own)
        let mut v: Vec<f64> = rows.iter().map(|r| r[ix(bk)]).filter(|x| *x > 0.0).collect();
        v.sort_by(f64::total_cmp);
        let m = v.get(v.len().saturating_sub(1) / 2).copied().unwrap_or(0.0);
        let filled = v.len();
        t.insert(
            name.into(),
            json!({
                "us_median": m,
                "filled": filled,
                "share_of_process_sum": if proc > 0.0 { m * filled as f64 / rows.iter().map(|r| r[ix(Bucket::Process)]).sum::<f64>() } else { 0.0 },
            }),
        );
    }
    // coverage: sum of attributed buckets against the measured process total (means).
    let mean = |bk: Bucket| rows.iter().map(|r| r[ix(bk)]).sum::<f64>() / rows.len().max(1) as f64;
    let attributed: f64 = [Bucket::Readout, Bucket::Scalars, Bucket::Secondaries, Bucket::Tide,
        Bucket::Certs, Bucket::Field, Bucket::Extmath, Bucket::Quantize, Bucket::Bind,
        Bucket::Plan, Bucket::Tau, Bucket::StepFor].iter().map(|b| mean(*b)).sum();
    let process = mean(Bucket::Process);
    json!({
        "kicks": rows.len(),
        "process_us_mean": process,
        "attributed_us_mean": attributed,
        "coverage": if process > 0.0 { attributed / process } else { 0.0 },
        "buckets": t,
    })
}

fn report(st: &Stats, scene: &str, extra: serde_json::Value) {
    let rows_all: Vec<[f64; 17]> = st.per_kick.iter().map(|r| r.0).collect();
    let rows_made: Vec<[f64; 17]> = st.per_kick.iter().filter(|r| !r.1).map(|r| r.0).collect();
    let rows_leaver: Vec<[f64; 17]> = st.per_kick.iter().filter(|r| r.1).map(|r| r.0).collect();
    let mut out = json!({
        "scene": scene,
        "kicks": st.per_kick.len(),
        "clock_path": st.clock_path, "kick_path": st.kick_path,
        "cycles": st.cycles, "passages": st.passages, "no_rebind": st.no_rebind, "thrusting": st.thrusting,
        "refused": st.refused,
        "memo": {
            "exact_shapes": st.exact.len(),
            "quantized_shapes": st.quantized.len(),
            "exact_sharing_kicks_per_shape": st.cycles as f64 / st.exact.len().max(1) as f64,
            "quantized_sharing_kicks_per_shape": st.cycles as f64 / st.quantized.len().max(1) as f64,
        },
        "replay_digest": st.digest.finalize().to_hex().to_string(),
        "attribution_all": table_for(&rows_all),
        "attribution_made": table_for(&rows_made),
        "attribution_leavers": table_for(&rows_leaver),
    });
    if let Some(extra) = extra.as_object() {
        for (k, v) in extra {
            out.as_object_mut().unwrap().insert(k.clone(), v.clone());
        }
    }
    println!("{}", serde_json::to_string_pretty(&out).unwrap());
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mode = args.get(1).map(|s| s.as_str()).unwrap_or("plane");
    match mode {
        "plane" => {
            let seed: u64 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(1);
            let seconds: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(20.0);
            let rtf: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(1.0);
            let p = plane(Config::default(), seed, Order::Sparse, 1, 48).expect("the plane");
            let mut u = p.u;
            let mut st = Stats::new();
            let made_n = u.n_bodies();
            let made_n = u.n_bodies();
            let mut last: Vec<Option<i64>> = vec![None; made_n];
            let mut keys = 0u8;
            let wall = Instant::now();
            for n in 1..=(seconds * 60.0) as usize {
                let now = u.now;
                if keys != script(n) {
                    keys = script(n);
                    u.input(now, keys).expect("input");
                }
                last.resize(u.n_bodies(), None);
                for (i, seen) in last.iter_mut().enumerate() {
                    let rec = u.rec(i);
                    if rec.kind != Kind::Ship || !rec.alive {
                        continue;
                    }
                    let Some(item) = rec.plan.first().copied() else { continue };
                    if !matches!(item.what, What::Kick(_)) || *seen == Some(item.t) {
                        continue;
                    }
                    *seen = Some(item.t);
                    attribute(&u, i, made_n, rec, item, &mut st);
                }
                u.frame(1.0 / 60.0, rtf, Budget::unlimited());
                u.settle(u.now);
                if wall.elapsed().as_secs_f64() > 300.0 {
                    eprintln!("wall guard at frame {n}");
                    break;
                }
            }
            report(&st, "plane", json!({"seed": seed, "rtf": rtf, "seconds": seconds, "made_bodies": made_n, "wall_s": wall.elapsed().as_secs_f64()}));
        }
        "coorbital" => {
            let n: usize = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(64);
            let seconds: f64 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(20.0);
            let rtf: f64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(100.0);
            let radius: i64 = args.get(5).and_then(|s| s.parse().ok()).unwrap_or(2_000_000);
            // N ships on one circle of the root doll (co-orbital: same shape, distinct phase),
            // a planet far out as the secondary that kicks them, as restricted() builds it.
            let ships: Vec<(i64, u32)> = (0..n)
                .map(|i| (radius, (i as u64 * (u32::MAX as u64 + 1) / n as u64) as u32))
                .collect();
            let w = restricted(Mass::ratio(1, 999).unwrap(), 527_000_000, 49_000, &ships, 1).expect("restricted");
            let mut u = w.u;
            let mut st = Stats::new();
            let made_n = u.n_bodies();
            let mut last: Vec<Option<i64>> = vec![None; u.n_bodies()];
            let wall = Instant::now();
            for _n in 1..=(seconds * 60.0) as usize {
                last.resize(u.n_bodies(), None);
                for (i, seen) in last.iter_mut().enumerate() {
                    let rec = u.rec(i);
                    if rec.kind != Kind::Ship || !rec.alive {
                        continue;
                    }
                    let Some(item) = rec.plan.first().copied() else { continue };
                    if !matches!(item.what, What::Kick(_)) || *seen == Some(item.t) {
                        continue;
                    }
                    *seen = Some(item.t);
                    attribute(&u, i, made_n, rec, item, &mut st);
                }
                u.frame(1.0 / 60.0, rtf, Budget::unlimited());
                u.settle(u.now);
                if wall.elapsed().as_secs_f64() > 300.0 {
                    eprintln!("wall guard");
                    break;
                }
            }
            report(&st, "coorbital", json!({"n_ships": n, "radius_root": radius, "rtf": rtf, "seconds": seconds, "wall_s": wall.elapsed().as_secs_f64()}));
        }
        _ => eprintln!("modes: plane <seed> <seconds> <rtf> | coorbital <n> <seconds> <rtf> <radius_root>"),
    }
}
