//! `--jet-probe`: decompose the plane's rebinding kicks, and measure the reuse the law's
//! re-anchored jet would enjoy. Read-only against the resolver: it replays each distinct
//! pending ship kick through `step::process` (like `--kick-bench`), then times the parts.
use super::{script, Session};
use emergent_space::binding::{IntegerState, Rebinding, Trajectory};
use emergent_space::orbit::{MemoCode, Scalar};
use emergent_universe::bind::bind;
use emergent_universe::body::What;
use emergent_universe::num::time_of;
use emergent_universe::{step, Kind};
use serde_json::json;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Instant;

fn percentiles(mut samples: Vec<f64>) -> serde_json::Value {
    samples.sort_by(f64::total_cmp);
    let at = |p: f64| samples.get(((samples.len().saturating_sub(1)) as f64 * p).ceil() as usize).copied();
    json!({"median": at(0.5), "p99": at(0.99), "samples": samples.len()})
}

fn med(samples: &[f64]) -> f64 {
    let mut v = samples.to_vec();
    v.sort_by(f64::total_cmp);
    v.get(v.len() / 2).copied().unwrap_or(0.0)
}

pub(super) fn run(mut s: Session, seconds: f64) -> crate::Result<u8> {
    let mut last: Vec<Option<i64>> = vec![None; s.n_bodies()];
    let mut keys = 0u8;
    let mut carried = 0u64; // sub-quantum kicks: no rebind, no compile
    let mut passages = 0u64; // rebinds onto a Passage (no cycle: the jet does not apply)
    let mut kick_us: Vec<f64> = Vec::new(); // whole resolver, rebinding kicks
    let mut bind_us: Vec<f64> = Vec::new(); // the wholesale rebind (`bind`) on the same state
    let mut fit_us: Vec<f64> = Vec::new(); // `Rebinding::from_state` alone (the compile)
    let mut read_us: Vec<f64> = Vec::new(); // one readout (proxy for a jet increment's cost)
    // Per body: the run length of consecutive rebinds inside one quantized memo cell.
    let mut cell: HashMap<usize, (Option<u64>, u64)> = HashMap::new(); // body -> (code, run)
    let mut jet_us: Vec<f64> = Vec::new(); // the jet increment (placement+decode+turn+residual, no compile)
    let mut jets_done = 0usize; // increments that renewed (not declined)
    let mut runs: Vec<u64> = Vec::new();
    let mut jet_err_p: Vec<f64> = Vec::new(); // |jet − exact| readout, position, half-interval ahead
    let mut jet_err_v: Vec<f64> = Vec::new(); // same, velocity
    let mut jet_err_fail = 0u64; // readouts that refused
    let mut cells_seen: HashMap<u64, ()> = HashMap::new();
    let mut jets_plane = 0u64; // kicks the plane's own resolver renewed through the jet
    let mut digest = blake3::Hasher::new();
    let wall = Instant::now();
    for n in 1..=(seconds * 60.0) as usize {
        if wall.elapsed().as_secs_f64() >= 55.0 {
            return Err("jet probe exceeded 55 s; no complete result".into());
        }
        let now = s.p.u.now;
        if keys != script(n) {
            keys = script(n);
            s.p.u.input(now, keys).map_err(|e| format!("input: {e:?}"))?;
        }
        last.resize(s.n_bodies(), None);
        for (i, seen) in last.iter_mut().enumerate() {
            let rec = s.p.u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive {
                continue;
            }
            let Some(item) = rec.plan.first().copied() else { continue };
            if !matches!(item.what, What::Kick(_)) || *seen == Some(item.t) {
                continue;
            }
            *seen = Some(item.t);
            let old_entry = Arc::clone(&rec.b.entry);
            let t0 = Instant::now();
            let upd = step::process(&s.p.u.ctx(), i, rec.clone());
            let us = t0.elapsed().as_secs_f64() * 1e6;
            digest.update(format!("{i} {item:?} {:?}", upd.rec).as_bytes());
            if Arc::ptr_eq(&old_entry, &upd.rec.b.entry) {
                // The jet shares the entry it renewed: a shared entry with a changed tube or
                // remainder renewed; one with nothing changed is a sub-quantum kick, carried.
                let renewed = upd.rec.b.residual != rec.b.residual
                    || upd.rec.b.tube.periapsis_angle != rec.b.tube.periapsis_angle
                    || upd.rec.b.tube.periapsis_time.get() != rec.b.tube.periapsis_time.get();
                if !renewed {
                    carried += 1;
                    continue;
                }
                jets_plane += 1;
            }
            // A rebind or a jet renewal happened: this kick bound a trajectory.
            kick_us.push(us);
            let b = &upd.rec.b;
            let t = b.event_time;
            let st = b.readout(t).map_err(|e| format!("readout: {e:?}"))?;
            let doll = b.doll;
            let ctx = s.p.u.ctx();
            let edge = (doll != 0)
                .then(|| ctx.dolls[doll as usize].edge.scale(2).ok())
                .flatten();
            let t1 = Instant::now();
            let again = bind(st, t, b.clock_exp, edge, b.entry.unit);
            bind_us.push(t1.elapsed().as_secs_f64() * 1e6);
            let again = again.map_err(|e| format!("rebind again: {e:?}"))?;
            let t2 = Instant::now();
            let _ = b.readout(t).map_err(|e| format!("readout: {e:?}"))?;
            read_us.push(t2.elapsed().as_secs_f64() * 1e6);
            // The jet increment's actual cost on this same state (the probe's own replay state:
            // the binding the kick started from): placement + decode + turn + residual, no compile.
            if emergent_universe::bind::jet_enabled() {
                let tj = Instant::now();
                let j = emergent_universe::bind::bind_jet(st, t, b.clock_exp, b.entry.unit, &rec.b);
                jet_us.push(tj.elapsed().as_secs_f64() * 1e6);
                jets_done += usize::from(j.is_some());
                // The error law the gates wish to bound: the renewed binding's readout against the
                // exact rebind's, half a kick interval ahead, relative to the state's own scales.
                if let Some(jb) = j {
                    let mk = |x: &emergent_universe::bind::Bound| emergent_universe::bind::Binding {
                        doll: b.doll,
                        tube: x.tube,
                        entry: std::sync::Arc::clone(&x.entry),
                        residual: x.residual,
                        turn: x.turn,
                        units: x.units,
                        clock_exp: b.clock_exp,
                        event_time: t,
                        kick: emergent_universe::bind::Kick::NONE,
                    };
                    let ahead = t + (rec.interval / 2).max(1);
                    if let (Ok(a), Ok(e)) = (mk(&jb).readout(ahead), mk(&again).readout(ahead)) {
                        let rel = |u: &[i64; 2], v: &[i64; 2]| -> f64 {
                            let (du, dv) = ((u[0] - v[0]) as f64, (u[1] - v[1]) as f64);
                            let r = ((v[0] as f64).hypot(v[1] as f64)).max(1.0);
                            (du.hypot(dv)) / r
                        };
                        jet_err_p.push(rel(&a.position, &e.position));
                        jet_err_v.push(rel(&a.velocity, &e.velocity));
                    } else {
                        jet_err_fail += 1;
                    }
                }
            }
            match &again.entry.trajectory {
                Trajectory::Cycle(c) => {
                    let t3 = Instant::now();
                    // The compile alone, on the state the plane compiled (`bind_in`'s call).
                    let units = b.entry.unit;
                    let q = |p: i64| -> Option<i64> {
                        let raw = Scalar::raw(p as i128, 0).ok()?;
                        let tubed = units.to_tube(raw).ok()?;
                        let fixed = tubed.fixed(0).ok()?;
                        i64::try_from(fixed).ok()
                    };
                    let (p0, p1) = (q(st.position[0]), q(st.position[1]));
                    let ev = units.to_tube(time_of(t, b.clock_exp).map_err(|e| format!("time: {e:?}"))?);
                    let ev = ev.map_err(|e| format!("time: {e:?}"))?;
                    let ed = edge.map(|e| units.to_tube(e)).transpose().map_err(|e| format!("edge: {e:?}"))?;
                    if let (Some(p0), Some(p1)) = (p0, p1) {
                        let st_tube = IntegerState { position: [p0, p1], ..st };
                        let _ = Rebinding::from_state(st_tube, ev, ed).map_err(|e| format!("fit: {e:?}"))?;
                        fit_us.push(t3.elapsed().as_secs_f64() * 1e6);
                    }
                    // Cell residence across this body's consecutive rebinds.
                    let code = MemoCode::encode(c.key()).ok().map(|c| c.bits());
                    if let Some(c) = code {
                        cells_seen.insert(c, ());
                    }
                    let e = cell.entry(i).or_insert((None, 0));
                    match (code, e.0) {
                        (Some(c), Some(p)) if c == p => e.1 += 1,
                        (Some(c), _) => {
                            if e.0.is_some() {
                                runs.push(e.1);
                            }
                            *e = (Some(c), 1);
                        }
                        (None, _) => {
                            e.0 = None;
                        }
                    }
                }
                Trajectory::Passage(_) => passages += 1,
            }
        }
        s.p.u.frame(1.0 / 60.0, s.rtf, emergent_universe::Budget::unlimited());
        s.p.u.settle(s.p.u.now);
    }
    for (_, (_, run)) in cell.iter() {
        runs.push(*run);
    }
    runs.sort_unstable();
    let med_runs = runs.get(runs.len() / 2).copied().unwrap_or(0);
    let mean_runs = runs.iter().sum::<u64>() as f64 / runs.len().max(1) as f64;
    let kick_med = med(&kick_us);
    let fit_med = med(&fit_us);
    let read_med = med(&read_us);
    let share = if kick_med > 0.0 { fit_med / kick_med } else { 0.0 };
    let r = med_runs.max(1) as f64;
    let optimistic = kick_med - fit_med + fit_med / r;
    let with_inc = optimistic + read_med;
    println!(
        "{}",
        serde_json::to_string_pretty(&json!({
            "scope": "one replay per distinct pending ship kick at deterministic 60 Hz plane snapshots; decomposition of rebinding kicks only; pure resolver reads, nothing applied",
            "seed": s.seed, "rtf_target": s.rtf, "seconds": seconds,
            "kicks": {"rebinding": kick_us.len(), "carried_subquantum": carried, "passage_rebinds": passages, "jet_renewed_by_resolver": jets_plane},
            "kick_us_resolver": percentiles(kick_us),
            "rebind_us_wholesale": percentiles(bind_us),
            "compile_us_from_state": percentiles(fit_us),
            "readout_us": percentiles(read_us),
            "jet_error_half_interval": if jet_err_p.is_empty() { serde_json::Value::Null } else {
                serde_json::json!({
                    "position_rel": percentiles(jet_err_p.clone()),
                    "velocity_rel": percentiles(jet_err_v.clone()),
                    "readout_failures": jet_err_fail,
                })
            },
            "compile_share_of_kick_median": share,
            "cell_residence": {
                "note": "run length of a body's consecutive rebinding kicks inside one quantized 12+12-bit memo cell",
                "median_run": med_runs, "mean_run": mean_runs, "runs": runs.len(),
            },
            "jet_ceiling": {
                "note": "projected rebinding-kick median if the compile happened only on cell exit and the increment cost one readout; R = median cell run",
                "R": med_runs,
                "optimistic_us": optimistic,
                "with_readout_increment_us": with_inc,
                "factor_optimistic": kick_med / optimistic.max(1e-9),
                "factor_with_increment": kick_med / with_inc.max(1e-9),
            },
            "jet_increment_us": if jet_us.is_empty() { serde_json::Value::Null } else { percentiles(jet_us.clone()) },
            "jet_renewed": jets_done, "jet_declined": jet_us.len() - jets_done,
            "replay_digest": digest.finalize().to_hex().to_string(),
            "digest": s.digest_at_cut().1,
            "wall_seconds": wall.elapsed().as_secs_f64()
        }))?
    );
    Ok(0)
}
