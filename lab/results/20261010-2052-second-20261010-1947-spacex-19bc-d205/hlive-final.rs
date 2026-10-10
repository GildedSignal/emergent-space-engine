//! `xtask universe --hlive`: distinctions created per game-second (H_live), creation side
//! against removal side, measured on the plane's own scene by pure replay (the kick-bench's
//! trick: resolve each distinct pending ship item against the exact snapshot; the plane applies
//! the real update).
//!
//! Creation (the first run of this mode): rebinds (a fired kick, a handoff, a decision with a
//! burn) each store a new tube and retire the old binding to history. The information content
//! of the kick stream is the empirical entropy of the applied integer increments dv, reported
//! at two representation levels (the 24-bit memo key, the exact Q48 key).
//!
//! Removal (this run): two real `shipmem` shelves (the packed-block store) are fed the same
//! rebind stream — every rebind updates the ship's slot, every 120 frames (idle time)
//! `Shelf::compact` seals the hot tier into scars and repacks groups whose scars outgrow a
//! quarter of their blocks. Bytes removed per game-second is reported next to bits created, and
//! the compact wall time replaces the model's "one rebind recompiles a block" duty assumption.
use super::{script, Session};
use emergent_shipmem::shelf::{Kind as ShelfKind, Shelf, Ship};
use emergent_space::{binding::Trajectory, orbit::{MemoCode, ShapeKey}};
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

/// −Σ p log p over counts, folded in sorted count order so the sum is deterministic
/// (HashMap iteration order moved the 15th digit between runs).
fn entropy_of<'a, I: Iterator<Item = &'a u64>>(counts: I, total: u64) -> f64 {
    if total == 0 {
        return 0.0;
    }
    let mut cs: Vec<u64> = counts.copied().collect();
    cs.sort_unstable();
    -cs.into_iter()
        .map(|c| {
            let p = c as f64 / total as f64;
            p * p.log2()
        })
        .sum::<f64>()
}

fn zz(x: i64) -> u64 {
    ((x << 1) ^ (x >> 63)) as u64
}


/// The plane state of one ship at one rebind, as store columns. Exact level (5 cols): the
/// binding's (k, periapsis) at the law's own widths, plus the rebind time. Coarse level
/// (2 cols): the 24-bit memo key alone (fallback for a non-periodic binding: the exact k —
/// counted) — the store the dossier's coarse column describes, where a rebind that keeps the
/// same memo key writes nothing.
fn columns(t: &Trajectory, tick: i64, coarse: bool, fallbacks: &mut u64) -> Ship {
    let key = t.key();
    let cw = match t {
        Trajectory::Cycle(_) => 1,
        Trajectory::Passage(_) => 0,
    };
    let mut s = [0u64; 8];
    if coarse {
        s[0] = match MemoCode::encode(key) {
            Ok(m) => m.bits(),
            Err(_) => {
                *fallbacks += 1;
                key.k
            }
        };
        s[1] = cw;
    } else {
        s[0] = zz(tick);
        s[1] = key.k;
        s[2] = zz(key.periapsis.significand());
        s[3] = zz(key.periapsis.exponent() as i64);
        s[4] = cw;
    }
    s
}


/// The removal side: a real packed-block shelf driven by the rebind stream, with exact
/// bookkeeping of what compaction removes. Deterministic in every count and byte; only the
/// wall µs vary between hosts.
struct Removal {
    shelf: Shelf,
    handles: Vec<Option<u32>>,
    queue: Vec<(usize, Ship)>,
    last: HashMap<usize, Ship>,
    unchanged: u64,
    cols: usize,
    trace: Vec<(f64, usize, u64)>, // per compact: (µs, hot rows sealed, repacks)
    bytes_now: usize,
    us_total: f64,
    bytes_removed_compact: u64,
    added_rebinds: u64,
    added_admits: u64,
    added_compact: u64,
    repacks: u64,
    blocks_rewritten: u64,
    max_step_ns: u64,
    compacts: u64,
    updates: u64,
    skipped: u64,
    inserted: u64,
    compact_ns: Vec<f64>,
}

fn ship_cmp(a: &Ship, b: &Ship, cols: usize) -> std::cmp::Ordering {
    for f in 0..cols {
        match a[f].cmp(&b[f]) {
            std::cmp::Ordering::Equal => {}
            o => return o,
        }
    }
    std::cmp::Ordering::Equal
}

impl Removal {
    fn new(cols: usize) -> Self {
        Self {
            shelf: Shelf::new(cols, 128, vec![[0, 1, 2, 3, 4, 5, 6, 7]], true),
            handles: Vec::new(),
            queue: Vec::new(),
            last: HashMap::new(),
            unchanged: 0,
            trace: Vec::new(),
            bytes_now: 0,
            us_total: 0.0,
            bytes_removed_compact: 0,
            cols,
            added_rebinds: 0,
            added_admits: 0,
            added_compact: 0,
            repacks: 0,
            blocks_rewritten: 0,
            max_step_ns: 0,
            compacts: 0,
            updates: 0,
            skipped: 0,
            inserted: 0,
            compact_ns: Vec::new(),
        }
    }
    /// Queue a body for insertion at the next flush (populations arrive in groups).
    fn admit(&mut self, body: usize, s: Ship) {
        if self.handles.get(body).copied().flatten().is_none() && !self.queue.iter().any(|&(b, _)| b == body) {
            self.queue.push((body, s));
        }
    }
    fn flush(&mut self) {
        if self.queue.is_empty() {
            return;
        }
        let mut batch = std::mem::take(&mut self.queue);
        batch.sort_by(|a, b| ship_cmp(&a.1, &b.1, self.cols));
        let ships: Vec<&(usize, Ship)> = batch.iter().collect();
        let mut members: Vec<Ship> = batch.iter().map(|(_, s)| *s).collect();
        let g0 = self.shelf.add_group(&mut members, ShelfKind::Sorted { order: 0 }).start;
        // Reconstruct handles: rank r lives in the block whose [start, start+n) contains it.
        let mut rank = 0usize;
        let mut per_group: Vec<Vec<(usize, u32)>> = Vec::new();
        let mut gi = 0usize;
        'outer: loop {
            let g = g0 as usize + gi;
            if g >= self.shelf.groups.len() {
                break;
            }
            let gr = self.shelf.groups[g];
            let mut mine = Vec::new();
            for bi in gr.first as usize..(gr.first + gr.nb) as usize {
                let br = self.shelf.blocks[bi];
                for slot in 0..br.n as usize {
                    if rank >= ships.len() {
                        per_group.push(mine);
                        break 'outer;
                    }
                    mine.push((rank, (bi as u32) << 8 | slot as u32));
                    rank += 1;
                }
            }
            per_group.push(mine);
            gi += 1;
            if rank >= ships.len() {
                break;
            }
        }
        let flat: Vec<(usize, u32)> = per_group.into_iter().flatten().collect();
        for (r, handle) in flat {
            let body = ships[r].0;
            if self.handles.len() <= body {
                self.handles.resize(body + 1, None);
            }
            self.handles[body] = Some(handle);
            self.inserted += 1;
        }
        let after = self.shelf.bytes();
        self.added_admits += after.saturating_sub(self.bytes_now) as u64;
        self.bytes_now = after;
    }
    /// One rebind: the ship's slot moves to the hot tier (O(1)); compact does the folding.
    /// A rebind that leaves the stored columns identical creates no distinction, so there is
    /// nothing to store (the memo's own semantics; counted — it cross-checks the memo hit rate).
    fn rebind(&mut self, body: usize, s: Ship) {
        if self.last.get(&body) == Some(&s) {
            self.unchanged += 1;
            return;
        }
        self.last.insert(body, s);
        match self.handles.get(body).copied().flatten() {
            Some(h) => {
                let before = self.shelf.bytes();
                self.shelf.update(h, s);
                self.added_rebinds += self.shelf.bytes().saturating_sub(before) as u64;
                self.bytes_now = self.shelf.bytes();
                self.updates += 1;
            }
            None => self.skipped += 1,
        }
    }
    /// Idle time: fold the hot tier into scars, repack what outgrows its blocks. Timed.
    fn compact(&mut self) {
        let before = self.shelf.bytes();
        let hot_rows = self.shelf.hot.len();
        let t0 = Instant::now();
        let st = self.shelf.compact();
        let ns = t0.elapsed().as_secs_f64() * 1e9;
        self.trace.push((ns / 1e3, hot_rows, st.repacks));
        let after = self.shelf.bytes();
        self.us_total += ns / 1e3;
        self.compact_ns.push(ns / 1e3);
        self.bytes_removed_compact += (before.saturating_sub(after)) as u64;
        self.added_compact += (after.saturating_sub(before)) as u64;
        self.bytes_now = after;
        self.repacks += st.repacks;
        self.blocks_rewritten += st.blocks_rewritten;
        self.max_step_ns = self.max_step_ns.max(st.max_step_ns);
        self.compacts += 1;
    }
    fn queue_len(&self) -> usize {
        self.queue.len()
    }
    /// Has the store never seen this body (not inserted, not queued)?
    fn needs(&self, body: usize) -> bool {
        self.handles.get(body).copied().flatten().is_none()
            && !self.queue.iter().any(|&(b, _)| b == body)
    }
    fn bytes(&self) -> usize {
        self.shelf.bytes()
    }
    fn json(&self, ship_seconds: f64, game_s: f64, rebinds: u64, created_bits_per_ship_s: f64) -> serde_json::Value {
        let per_rebind_us = if self.updates > 0 { self.us_total / self.updates as f64 } else { 0.0 };
        let mut c = self.compact_ns.clone();
        c.sort_by(f64::total_cmp);
        let p50 = c.get((c.len().saturating_sub(1)) * 50 / 100).copied().unwrap_or(0.0);
        json!({
            "cols": self.cols,
            "members": self.inserted,
            "updates": self.updates, "skipped_no_handle": self.skipped,
            "rebinds_seen": rebinds,
            "compacts": self.compacts, "repacks": self.repacks, "blocks_rewritten": self.blocks_rewritten,
            "compact_us_total": self.us_total,
            "compact_us_p50": p50,
            "us_per_rebind_amortized": per_rebind_us,
            "bytes_removed_compact": self.bytes_removed_compact,
            "bytes_added_rebinds": self.added_rebinds,
            "bytes_added_admits": self.added_admits,
            "bytes_added_compact": self.added_compact,
            "bytes_now": self.bytes_now,
            "bytes_removed_per_game_s": if game_s > 0.0 { self.bytes_removed_compact as f64 / game_s } else { 0.0 },
            "bytes_removed_per_ship_s": if ship_seconds > 0.0 { self.bytes_removed_compact as f64 / ship_seconds } else { 0.0 },
            "created_bits_per_ship_s_same_run": created_bits_per_ship_s,
            "duty_scene_us_per_game_s": if game_s > 0.0 { self.us_total / game_s } else { 0.0 },
            "bytes_removed_per_compact_us": if self.us_total > 0.0 { self.bytes_removed_compact as f64 / self.us_total } else { 0.0 },
            "compact_trace_us_rows_repacks": self.trace,
            "duty_cores_at_1e9_ships_linear_scene_scaling": if ship_seconds > 0.0 { self.us_total / ship_seconds * 1e9 / 1e6 } else { 0.0 },
            "duty_cores_at_1e9_from_created_bits_capacity": if self.us_total > 0.0 { (created_bits_per_ship_s / 8.0 * 1e9) / ((self.bytes_removed_compact as f64 / self.us_total) * 1e6) } else { 0.0 },
            "bytes_per_member_now": if self.inserted > 0 { self.bytes_now as f64 / self.inserted as f64 } else { 0.0 },
            "updates": self.updates, "skipped_no_handle": self.skipped, "unchanged_skipped": self.unchanged,
        })
    }
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
    let mut dv_abs: Vec<f64> = Vec::new(); // log2|dv| per component, context only (exponent varies per binding)
    let mut last_exact: HashMap<usize, (i128, i128)> = HashMap::new(); // body -> (k, periapsis Q48)
    let mut last_q: HashMap<usize, u64> = HashMap::new(); // body -> last quantized memo key
    let mut dk: Vec<i128> = Vec::new(); // first differences of the exact shape key, per body
    let mut dp: Vec<i128> = Vec::new();
    let mut q_trans: HashMap<(u64, u64), u64> = HashMap::new(); // quantized-key transitions per body (entropy folds sorted)
    let mut clock_kicks = 0u64;
    let mut shapes = Shapes::default();
    let mut ship_seconds = 0.0f64;
    let mut samples: Vec<serde_json::Value> = Vec::new();
    let mut digest = blake3::Hasher::new();
    let wall = Instant::now();
    let mut frames = 0usize;
    let mut keys = 0u8;
    // The removal side: the same rebind stream into two packed-block shelves.
    let (mut exact, mut coarse) = (Removal::new(5), Removal::new(2));
    let mut fallbacks = [0u64; 2];
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
            // Admit bodies the store has never seen (their binding as of this frame).
            if exact.needs(i) {
                exact.admit(i, columns(&rec.b.entry.trajectory, now, false, &mut fallbacks[0]));
            }
            if coarse.needs(i) {
                coarse.admit(i, columns(&rec.b.entry.trajectory, now, true, &mut fallbacks[1]));
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
                        dv_abs.push((k.dv[0].unsigned_abs() as f64 + 1.0).log2());
                        dv_abs.push((k.dv[1].unsigned_abs() as f64 + 1.0).log2());
                    }
                } else {
                    carried[pop] += 1;
                }
            }
            if let Some(e) = &upd.new_entry {
                if let Trajectory::Cycle(c) = &e.trajectory {
                if let (Ok(exact_k), Ok(q)) = (ShapeKey::for_orbit(c.key()), MemoCode::encode(c.key())) {
                    let key = (exact_k.k as i128, exact_k.compactness.fixed(-48).unwrap_or(0));
                    if let Some(prev) = last_exact.insert(i, key) {
                        if !exact_k.null && prev.0 != 0 {
                            dk.push((key.0 - prev.0).abs());
                            dp.push((key.1 - prev.1).abs());
                        }
                    }
                    if let Some(prev_q) = last_q.insert(i, q.bits()) {
                        *q_trans.entry((prev_q, q.bits())).or_default() += 1;
                    } else {
                        *q_trans.entry((u64::MAX, q.bits())).or_default() += 1;
                    }
                }
                }
            }
            // Removal side: every rebind supersedes the ship's stored state.
            if reb > 0 {
                let t = &upd.rec.b.entry.trajectory;
                exact.rebind(i, columns(t, item.t, false, &mut fallbacks[0]));
                coarse.rebind(i, columns(t, item.t, true, &mut fallbacks[1]));
            }
            digest.update(format!("{i} {item:?} {:?}", upd.rec).as_bytes());
        }
        s.p.u.frame(1.0 / 60.0, s.rtf, Budget::unlimited());
        s.p.u.settle(s.p.u.now);
        frames = n;
        if exact.queue_len() >= 8 {
            exact.flush();
        }
        if coarse.queue_len() >= 8 {
            coarse.flush();
        }
        if n % 120 == 0 {
            exact.flush();
            coarse.flush();
            exact.compact();
            coarse.compact();
            samples.push(json!({
                "frame": n, "game_s": (n as f64 * game_s_per_frame).round(),
                "ships": ships, "bodies": s.n_bodies(),
                "bytes_per_body": s.bytes_per_body(), "catalogue_live": s.catalogue_live(),
                "shelf_exact_bytes": exact.bytes(), "shelf_coarse_bytes": coarse.bytes(),
            }));
        }
    }
    let game_s = frames as f64 * game_s_per_frame;
    let per = |c: u64| if ship_seconds > 0.0 { c as f64 / ship_seconds } else { 0.0 };
    let total_kicks = fired[0] + fired[1] + carried[0] + carried[1];
    let pct = |v: &mut Vec<f64>, p: f64| { v.sort_by(f64::total_cmp); v.get(((v.len().saturating_sub(1)) as f64 * p).ceil() as usize).copied().unwrap_or(0.0) };
    let mut dk_bits: Vec<f64> = dk.iter().map(|&d| ((d.unsigned_abs() as f64) + 1.0).log2()).collect();
    let mut dp_bits: Vec<f64> = dp.iter().map(|&d| ((d.unsigned_abs() as f64) + 1.0).log2()).collect();
    dv_abs.sort_by(f64::total_cmp);
    // Conditional entropy of the quantized (24-bit) memo key: H(next|prev) = H(pair) - H(prev).
    let n_q: u64 = q_trans.values().sum();
    let h_pair = entropy_of(q_trans.values(), n_q);
    let mut prev_hist: HashMap<u64, u64> = HashMap::new();
    for ((a, _), c) in &q_trans { *prev_hist.entry(*a).or_default() += *c; }
    let h_prev = entropy_of(prev_hist.values(), n_q);
    let n_dk = dk.len() as u64;
    let distinct_dk = dk.iter().collect::<std::collections::HashSet<_>>().len();
    let rebind_total = fired[0] as f64 + fired[1] as f64;
    // Bits per rebind, two brackets: (a) the coarse-grained quantized-key conditional entropy
    // (what a 24-bit-key store must distinguish per rebind), (b) the exact first-difference
    // magnitude at the law's own Q48 quantization (an upper bracket on a per-body differencing
    // model; a population program that predicts the drift drives it toward 0).
    let bits_coarse = h_pair - h_prev;
    let dk_p99 = { let mut c = dk_bits.clone(); pct(&mut c, 0.99) };
    let bits_exact_p50 = pct(&mut dk_bits, 0.5) + pct(&mut dp_bits, 0.5);
    let dv_p99 = dv_abs.get(((dv_abs.len() as f64) * 0.99) as usize).copied().unwrap_or(0.0);
    let rates = json!({
        "rebind_kicks_per_ship_s": [per(fired[0]), per(fired[1])],
        "carried_kicks_per_ship_s": [per(carried[0]), per(carried[1])],
        "rebinds_per_ship_s": [per(rebinds[0]), per(rebinds[1])],
        "segments_per_ship_s": [per(segs[0]), per(segs[1])],
        "catalogue_entries_per_ship_s": [per(new_entries[0]), per(new_entries[1])],
    });
    let bits_coarse_per_ship_s = bits_coarse * rebind_total / ship_seconds.max(1.0);
    let bits_exact_per_ship_s = bits_exact_p50 * rebind_total / ship_seconds.max(1.0);
    let info = json!({
        "quantized_key": {"transitions": n_q, "distinct_pairs": q_trans.len(), "entropy_bits_per_rebind_conditional": bits_coarse, "note": "H(next|prev) over the 24-bit memo key per body; the plug-in estimate with few samples per pair biases down, magnitudes cross-check it"},
        "exact_key_first_difference": {"samples": n_dk, "distinct": distinct_dk, "log2_dk_bits_p50": pct(&mut dk_bits, 0.5), "log2_dk_p99": dk_p99, "log2_dp_bits_p50": pct(&mut dp_bits, 0.5), "bits_p50_sum": bits_exact_p50},
        "dv_context_log2_p50": dv_abs.get(dv_abs.len() / 2).copied(), "dv_context_log2_p99": dv_p99,
        "bits_per_ship_s": {"coarse": bits_coarse_per_ship_s, "exact_p50_bracket": bits_exact_per_ship_s},
        "clock_kicks_excluded": clock_kicks,
    });
    println!("{}", serde_json::to_string_pretty(&json!({
        "scope": "H_live creation side (distinct pending ship items resolved by pure replay on deterministic plane snapshots; resolver cost excluded from rates) plus the removal side: the same rebind stream into two real shipmem shelves (128-member blocks), compacted every 120 frames",
        "seed": s.seed, "rtf": s.rtf, "frames": frames, "game_seconds": game_s, "ship_seconds": ship_seconds,
        "events_by_kind": {"kick": kinds[0], "open": kinds[1], "boundary": kinds[2], "handoff": kinds[3], "lost": kinds[4], "refused": kinds[5]},
        "fired_vs_carried": {"fired": fired, "carried": carried, "fire_rate": if total_kicks > 0 { (fired[0] as f64 + fired[1] as f64) / total_kicks as f64 } else { 0.0 }},
        "rates": rates,
        "information": info,
        "memo": { "cycles": shapes.cycles, "exact_shapes": shapes.exact.len(), "quantized_shapes": shapes.quantized.len() },
        "removal": {
            "note": "one Shelf per level; every rebind updates the ship's slot (hot tier, O(1)); compact() every 120 frames seals scars and repacks groups whose scars cost more than a quarter of their blocks; bytes/counts deterministic, us host-dependent",
            "model_replaced": "the dossier's duty model assumed one kick-resolver rebind (72 us median) per recompile; us_per_rebind_amortized is the measured replacement",
            "exact": exact.json(ship_seconds, game_s, rebinds[0] + rebinds[1], bits_exact_per_ship_s),
            "coarse": coarse.json(ship_seconds, game_s, rebinds[0] + rebinds[1], bits_coarse_per_ship_s),
            "memo_fallbacks": fallbacks,
        },
        "store_samples": samples,
        "replay_digest": digest.finalize().to_hex().to_string(),
        "digest": s.digest_at_cut().1, "machine_before": machine_before,
        "machine_after": crate::measure::machine_state("after"), "wall_seconds": wall.elapsed().as_secs_f64()
    }))?);
    Ok(0)
}

#[cfg(test)]
mod tests {
    use super::Removal;

    /// A convoy-like synthetic population: periapsis time advances by a constant, the shape
    /// columns jitter by small amounts (the structure shipmem is built for).
    fn convoy(n: u64, cols: usize, seed: u64) -> Vec<[u64; 8]> {
        let mut x = seed | 1;
        let mut next = move || {
            x ^= x << 13;
            x ^= x >> 7;
            x ^= x << 17;
            x
        };
        (0..n)
            .map(|i| {
                let mut s = [0u64; 8];
                s[0] = i * (1 << 12) + next() % 64;
                for f in 1..cols {
                    s[f] = (1u64 << 40) + next() % 512;
                }
                s
            })
            .collect()
    }

    /// The contract the removal-side numbers rest on: the accounting reconciles exactly
    /// (initial + added − removed = final) and the store stays bounded under a sustained kick
    /// stream at the fixed cadence — the premise the duty number claims to defend.
    #[test]
    fn removal_accounting_reconciles_and_stays_bounded() {
        let cols = 5;
        let mut r = Removal::new(cols);
        let pop = convoy(300, cols, 0x5EED);
        for (i, s) in pop.iter().enumerate() {
            r.admit(i, *s);
        }
        r.flush();
        r.compact();
        let initial = r.bytes();
        assert!(initial > 0);
        // 24 rounds: 60 rebinds each (a fifth of the population), compact every round.
        let mut x = 0xdead_beefu64 | 1;
        let mut next = move || {
            x ^= x << 13;
            x ^= x >> 7;
            x ^= x << 17;
            x
        };
        for round in 0..24 {
            for k in 0..60 {
                let body = (next() as usize) % 300;
                let mut s = pop[body];
                s[0] = s[0].wrapping_add(round * 7 + k);
                for f in 1..cols {
                    s[f] = s[f].wrapping_add(next() % 97);
                }
                r.rebind(body, s);
            }
            r.compact();
        }
        let final_bytes = r.bytes();
        // Bounded: scars are folded back; no monotone growth past the packed size's neighbourhood.
        assert!(
            final_bytes <= initial * 2 + 4096,
            "store grew: {initial} -> {final_bytes}"
        );
        // Telescoping accounting: every byte the store gained (admits, rebind hot entries,
        // compaction growth) minus every byte compaction removed is exactly what it holds now.
        assert_eq!(
            r.added_admits as usize + r.added_rebinds as usize + r.added_compact as usize,
            final_bytes + r.bytes_removed_compact as usize,
            "accounting does not reconcile"
        );
        assert!(r.repacks > 0, "no repack ever fired: the removal machinery was never exercised");
        assert!(r.updates == 24 * 60);
    }
}
