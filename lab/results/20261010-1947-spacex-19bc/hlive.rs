//! `xtask universe --hlive`: distinctions created per game-second (H_live's creation side),
//! measured on the plane's own scene by pure replay (the kick-bench's trick: resolve each
//! distinct pending ship item against the exact snapshot; the plane applies the real update).
//!
//! What creates live distinguishing information per body: rebinds (a fired kick, a handoff, a
//! decision with a burn) each store a new tube and retire the old binding to history; carried
//! (sub-quantum) kicks store nothing but the bounded carry. The information content of the kick
//! stream is the empirical entropy of the applied integer increments dv.
use super::{script, Session};
use emergent_space::{binding::Trajectory, orbit::MemoCode, ShapeKey};
use emergent_universe::{body::What, step, Budget, Kind};
use serde_json::json;
use std::collections::{HashMap, HashSet};
use std::time::Instant;

#[derive(Default)]
struct Shapes {
    cycles: u64,
    exact: HashSet<ShapeKey>,
    quantized: HashSet<u64>,
}
impl Shapes {
    fn note(&mut self, t: &Trajectory) {
        let Trajectory::Cycle(c) = t else { return };
        self.cycles += 1;
        if let Ok(k) = ShapeKey::for_orbit(c.key()) {
            self.exact.insert(k);
        }
        if let Ok(c) = MemoCode::encode(c.key()) {
            self.quantized.insert(c.bits());
        }
    }
}
fn entropy_of<'a, I: Iterator<Item = &'a u64>>(counts: I, total: u64) -> f64 {
    if total == 0 {
        return 0.0;
    }
    -counts.map(|&c| {
        let p = c as f64 / total as f64;
        p * p.log2()
    }).sum::<f64>()
}

fn entropy(counts: &HashMap<i64, u64>, total: u64) -> f64 {
    entropy_of(counts.values(), total)
}
pub(super) fn run(mut s: Session, seconds: f64) -> crate::Result<u8> {
    let machine_before = crate::measure::machine_state("before");
    let made_n = s.n_bodies();
    let mut last: Vec<Option<i64>> = vec![None; made_n];
    // Event counts, split plane-made vs fleet-handed-out members (index >= made_n).
    let mut kinds = [0u64; 8]; // Kick, Open, Boundary, Handoff, Lost, Refused (Resolved order + pad)
    let mut fired = [0u64; 2]; // rebinding kicks (a Segment retired): [made, leavers]
    let mut carried = [0u64; 2]; // kicks that fired nothing (no rebind)
    let mut rebinds = [0u64; 2]; // all rebinds (any cause): retired segments
    let mut segs = [0u64; 2]; // retired segments
    let mut new_entries = [0u64; 2];
    let mut dv_joint: HashMap<(i64, i64), u64> = HashMap::new();
    let mut dv_marg: [HashMap<i64, u64>; 2] = [HashMap::new(), HashMap::new()];
    let mut dv_abs_p99: Vec<i64> = Vec::new();
    let mut clock_kicks = 0u64;
    let mut shapes = Shapes::default();
    let mut ship_seconds = 0.0f64;
    let mut samples: Vec<serde_json::Value> = Vec::new();
    let mut digest = blake3::Hasher::new();
    let wall = Instant::now();
    let mut frames = 0usize;
    let mut keys = 0u8;
    let game_s_per_frame = s.rtf / 60.0;
    for n in 1..=(seconds * 60.0) as usize {
        if wall.elapsed().as_secs_f64() >= 55.0 {
            return Err("hlive replay exceeded 55 s; no complete result".into());
        }
        let now = s.p.u.now;
        if keys != script(n) {
            keys = script(n);
            s.p.u.input(now, keys).map_err(|e| format!("input: {e:?}"))?;
        }
        let ships = (0..s.n_bodies()).filter(|&i| matches!(s.p.u.rec(i).kind, Kind::Ship)).count();
        ship_seconds += ships as f64 * game_s_per_frame;
        last.resize(s.n_bodies(), None);
        for (i, seen) in last.iter_mut().enumerate() {
            let rec = s.p.u.rec(i);
            if rec.kind != Kind::Ship || !rec.alive {
                continue;
            }
            let Some(item) = rec.plan.first().copied() else { continue };
            if *seen == Some(item.t) {
                continue;
            }
            *seen = Some(item.t);
            let upd = step::process(&s.p.u.ctx(), i, rec);
            let pop = usize::from(i >= made_n);
            kinds[upd.kind as usize % 8] += 1;
            let reb = upd.retired.len();
            rebinds[pop] += usize::from(reb > 0) as u64;
            segs[pop] += reb as u64;
            if upd.new_entry.is_some() {
                new_entries[pop] += 1;
                if let Some(e) = &upd.new_entry {
                    shapes.note(&e.trajectory);
                }
            }
            if matches!(item.what, What::Kick(_)) {
                if reb > 0 {
                    fired[pop] += 1;
                    let k = upd.rec.b.kick;
                    if k.clock {
                        clock_kicks += 1;
                    } else if k.len != 0 {
                        let key = (k.dv[0], k.dv[1]);
                        *dv_joint.entry(key).or_default() += 1;
                        *dv_marg[0].entry(k.dv[0]).or_default() += 1;
                        *dv_marg[1].entry(k.dv[1]).or_default() += 1;
                        dv_abs_p99.push(k.dv[0].abs().max(k.dv[1].abs()));
                    }
                } else {
                    carried[pop] += 1;
                }
            }
            digest.update(format!("{i} {item:?} {:?}", upd.rec).as_bytes());
        }
        s.p.u.frame(1.0 / 60.0, s.rtf, Budget::unlimited());
        s.p.u.settle(s.p.u.now);
        frames = n;
        if n % 120 == 0 {
            samples.push(json!({
                "frame": n, "game_s": (n as f64 * game_s_per_frame).round(2),
                "ships": ships, "bodies": s.n_bodies(),
                "bytes_per_body": s.bytes_per_body(), "catalogue_live": s.catalogue_live(),
            }));
        }
    }
    let game_s = frames as f64 * game_s_per_frame;
    let per = |c: u64, pop: usize| if ship_seconds > 0.0 { c as f64 / ship_seconds } else { 0.0 };
    let total_kicks = fired[0] + fired[1] + carried[0] + carried[1];
    let n_dv: u64 = dv_joint.values().sum();
    dv_abs_p99.sort_unstable();
    let entropy_joint = entropy_of(dv_joint.values(), n_dv);
    // per-ship-second rates
    let rates = json!({
        "rebind_kicks_per_ship_s": [per(fired[0], 0), per(fired[1], 1)],
        "carried_kicks_per_ship_s": [per(carried[0], 0), per(carried[1], 1)],
        "rebinds_per_ship_s": [per(rebinds[0], 0), per(rebinds[1], 1)],
        "segments_per_ship_s": [per(segs[0], 0), per(segs[1], 1)],
        "catalogue_entries_per_ship_s": [per(new_entries[0], 0), per(new_entries[1], 1)],
    });
    // Information created: the entropy of the applied increment stream is the floor for what any
    // store must distinguish; each rebind also stores a periapsis time (its tick is predictable
    // from the plan, so 0 bits) and moves the tube key (counted by the catalogue rate).
    let bits_per_ship_s = entropy_joint * (fired[0] as f64 + fired[1] as f64) / ship_seconds.max(1.0);
    println!("{}", serde_json::to_string_pretty(&json!({
        "scope": "H_live creation side: distinct pending ship items resolved by pure replay on deterministic plane snapshots; resolver cost excluded from rates (rates are per game-second)",
        "seed": s.seed, "rtf": s.rtf, "frames": frames, "game_seconds": game_s, "ship_seconds": ship_seconds,
        "events_by_kind": {"kick": kinds[0], "open": kinds[1], "boundary": kinds[2], "handoff": kinds[3], "lost": kinds[4], "refused": kinds[5]},
        "fired_vs_carried": {"fired": fired, "carried": carried, "fire_rate": if total_kicks > 0 { (fired[0] as f64 + fired[1] as f64) / total_kicks as f64 } else { 0.0 }},
        "rates": rates,
        "increment_information": {
            "samples": n_dv, "clock_kicks_excluded": clock_kicks,
            "entropy_bits_per_fired_kick": entropy_joint,
            "entropy_bits_marginal": [entropy(&dv_marg[0], n_dv), entropy(&dv_marg[1], n_dv)],
            "distinct_dv_pairs": dv_joint.len(), "abs_dv_p50": dv_abs_p99.get(dv_abs_p99.len() / 2).copied(), "abs_dv_p99": dv_abs_p99.get((dv_abs_p99.len() as f64 * 0.99) as usize).copied(),
            "bits_per_ship_s": bits_per_ship_s,
        },
        "memo": shapes.json(),
        "store_samples": samples,
        "replay_digest": digest.finalize().to_hex().to_string(),
        "digest": s.digest_at_cut().1, "machine_before": machine_before,
        "machine_after": crate::measure::machine_state("after"), "wall_seconds": wall.elapsed().as_secs_f64()
    }))?);
    Ok(0)
}
