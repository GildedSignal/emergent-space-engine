//! H_live bench v2 (second-author run 20261009-1858): the bits of live distinguishing information
//! the plane's universe creates per game-second (docs/plane.md "Distinctions created per
//! game-second"; docs/law.md "the allocator reads H_live ... about +62 bits per kick and −60 per
//! reabsorption").
//!
//! v2 fixes over the first run (checker's verdict on 20261009-1754-spacex-c6d8):
//! - `d_peri_time` is FED (the first run never fed it and asserted "never moved" from a dead
//!   instrument);
//! - bits per binding counts every sample of every stream (dv ×2, residual ×4, carry ×2 per
//!   binding; the first run counted each stream once, ~2.2× low);
//! - `--kick-bench` is kept (the first run replaced its match arm);
//! - the digest is byte-identical in construction to the first run's (it always included
//!   `snap.peri`), so the same flight reproduces the same digest.
//!
//! Plus the checker's named experiment: a QUIESCENT BELT scene (the star, the three planets, no
//! moon, no fleet, no player, no input) with per-body program refits. The plane already recompiles
//! a body's orbit program (its tube) at every binding; the journal therefore splits the storage:
//! - DEBT (what the body still owes after the refit): residual ×4, carry ×2, shape-key `k`,
//!   periapsis-angle and periapsis-time deltas — the post-refit record;
//! - CAUSE (the kick's applied quanta, ×2): what a pre-refit journal would store instead.
//! Each stream is summarised by magnitude-class entropy (class entropy + in-class bits + sign),
//! within ~1 bit/field of an ideal per-field coder. A word-width sweep replays the raw per-kick
//! dv through a sigma-delta at coarser velocity quanta to count what a coarser word would fire.
use super::script;
use emergent_space::orbit::Scalar;
use emergent_universe::body::BodyRec;
use emergent_universe::num::s;
use emergent_universe::scenario::{Plane, AU, PLANETS, STAR_RADIUS};
use emergent_universe::{Budget, Config, Kind, OrbitSpec};
use emergent_universe::view::TICK_SECONDS;
use serde_json::json;
use std::time::Instant;

fn err<T, E: std::fmt::Debug>(r: Result<T, E>) -> crate::Result<T> {
    r.map_err(|e| format!("{e:?}").into())
}

/// One signed integer stream (i128 in, so residuals need no clamping).
struct Stream {
    n: u64,
    classes: [u64; 129],
}
impl Default for Stream {
    fn default() -> Self {
        Stream { n: 0, classes: [0; 129] }
    }
}
impl Stream {
    fn add(&mut self, x: i128) {
        let a = x.unsigned_abs();
        self.classes[if a == 0 { 0 } else { (128 - a.leading_zeros()) as usize }] += 1;
        self.n += 1;
    }

    /// Bits per sample under a class-then-uniform code (class entropy, in-class uniform bits,
    /// and a sign bit when nonzero: at most one bit over an ideal two-sided geometric coder).
    fn bits(&self) -> f64 {
        if self.n == 0 {
            return 0.0;
        }
        let p = |c: u64| c as f64 / self.n as f64;
        let mut h = 0.0;
        let mut expect = 0.0;
        for (i, &c) in self.classes.iter().enumerate() {
            if c == 0 {
                continue;
            }
            h -= p(c) * p(c).log2();
            if i > 0 {
                expect += p(c) * (i as f64 + 1.0);
            }
        }
        h + expect
    }
    /// Total bits over all samples (per-sample bits × n): what the stream costs per binding run.
    fn total(&self) -> f64 {
        self.bits() * self.n as f64
    }
    fn p_zero(&self) -> f64 {
        if self.n == 0 { f64::NAN } else { self.classes[0] as f64 / self.n as f64 }
    }
    fn json(&self) -> serde_json::Value {
        json!({"n": self.n, "bits": (self.bits() * 1e3).round() / 1e3, "p_zero": (self.p_zero() * 1e3).round() / 1e3})
    }
}

/// The storage streams of one population (made bodies vs fleet members vs belt bodies).
#[derive(Default)]
struct Pop {
    dv: Stream,       // kick's applied whole velocity quanta, both components (the CAUSE journal)
    res: Stream,      // binding residual (position and velocity offsets), absolute
    carry: Stream,    // sigma-delta carry, absolute
    dk: Stream,       // orbit shape key `k` (Q48 of 1/(1+e)), delta
    dangle: Stream,   // periapsis angle, signed circular delta
    dperi: Stream,    // periapsis time, delta (FED in v2)
    dk_innov: Stream,     // dk minus its per-body slow EMA (gain 1/64): what a program refit cannot absorb
    dangle_innov: Stream, // dangle minus its per-body slow EMA
    dperi_innov: Stream,  // dperi minus its per-body slow EMA (the predictable advance removed)
    bindings: u64,
    events: u64,      // all resolved items between bindings (cadence truth)
    other: u64,       // bindings not made by a kick (creation, handoff, burn flush)
    /// Raw per-kick dv in 2^-16 of the quantum (fired quanta × 65536 + carry delta), per
    /// component, for the word-width sweep. Only frames where at most one kick landed.
    raw: Vec<[i64; 2]>,
}
impl Pop {
    /// The DEBT journal: bits per binding after the per-binding program refit (what the body
    /// still owes): residual + carry + the tube's field deltas.
    fn debt_bits(&self) -> f64 {
        (self.res.total() + self.carry.total() + self.dk.total() + self.dangle.total() + self.dperi.total())
            / self.bindings.max(1) as f64
    }
    /// The DEBT journal after the cheapest per-body program model (slow EMA on each field's
    /// delta): the bound a refit-with-phase-model could reach.
    fn debt_innov_bits(&self) -> f64 {
        (self.res.total() + self.carry.total() + self.dk_innov.total() + self.dangle_innov.total() + self.dperi_innov.total())
            / self.bindings.max(1) as f64
    }
    /// The CAUSE journal: bits per binding of the kick's applied quanta alone.
    fn cause_bits(&self) -> f64 {
        self.dv.total() / self.bindings.max(1) as f64
    }
    /// Both journals together (continuity with the first run's stream set, dperi fed).
    fn both_bits(&self) -> f64 {
        self.debt_bits() + self.cause_bits()
    }
    /// The word-width sweep: replay the raw per-kick dv through a sigma-delta whose quantum is
    /// 2^w coarser, and count fires (a kick that fires nothing is carried, costs no binding).
    fn sweep(&self) -> serde_json::Value {
        let widths = [0u32, 8, 16, 24];
        let fires: Vec<(u32, f64)> = widths
            .iter()
            .map(|&w| {
                let q = 65536i128 << w;
                let mut carry = [0i128; 2];
                let mut fired = 0u64;
                for dv in &self.raw {
                    let mut f = false;
                    for c in 0..2 {
                        carry[c] += dv[c] as i128;
                        let whole = carry[c] / q;
                        if whole != 0 {
                            carry[c] -= whole * q;
                            f = true;
                        }
                    }
                    fired += u64::from(f);
                }
                (w, if self.raw.is_empty() { f64::NAN } else { fired as f64 / self.raw.len() as f64 })
            })
            .collect();
        json!(fires)
    }
}

#[derive(Clone)]
struct Snap {
    ev: i64,
    res: [i128; 4],
    carry: [i64; 2],
    k: u64,
    angle: u32,
    peri: i64,
    events: u64,
    /// Per-body slow exponential means (gain 1/64) of the three delta fields.
    ema: [i64; 3],
}
impl Snap {
    fn of(rec: &BodyRec) -> Self {
        let b = &rec.b;
        let key = b.entry.trajectory.key();
        Snap {
            ev: b.event_time,
            res: [
                b.residual.position[0], b.residual.position[1],
                b.residual.velocity[0], b.residual.velocity[1],
            ],
            carry: rec.carry,
            events: rec.events,
            ema: [0; 3],
            k: key.k,
            angle: b.tube.periapsis_angle,
            peri: b.tube.periapsis_time.get() as i64,
        }
    }
}

/// Journal one frame of every live ship (the plane's own scene: made ships before `made_n`,
/// fleet members after; the belt: every ship).
fn journal(
    u: &emergent_universe::Universe,
    last: &mut Vec<Option<Snap>>,
    made_n: usize,
    made: &mut Pop,
    members: &mut Pop,
    digest: &mut blake3::Hasher,
) {
    last.resize(u.n_bodies(), None);
    for i in 0..u.n_bodies() {
        let rec = u.rec(i);
        if rec.kind != Kind::Ship || !rec.alive {
            continue;
        }
        let snap = Snap::of(&rec);
        let Some(prev) = &last[i] else {
            last[i] = Some(snap);
            continue;
        };
        if snap.ev == prev.ev {
            // No binding this frame. A carry change without a binding is a sub-quantum kick:
            // raw journal fodder for the sweep (at most one kick per frame at these rtf).
            if snap.carry != prev.carry {
                let pop = if i < made_n { &mut *made } else { &mut *members };
                pop.raw.push([
                    (snap.carry[0] - prev.carry[0]),
                    (snap.carry[1] - prev.carry[1]),
                ]);
            }
            continue;
        }
        let pop = if i < made_n { &mut *made } else { &mut *members };
        pop.bindings += 1;
        pop.events += snap.events - prev.events;
        pop.other += u64::from(rec.b.kick.len == 0);
        pop.dv.add(rec.b.kick.dv[0] as i128);
        pop.dv.add(rec.b.kick.dv[1] as i128);
        for j in 0..4 {
            pop.res.add(snap.res[j]);
        }
        pop.carry.add(snap.carry[0] as i128);
        pop.carry.add(snap.carry[1] as i128);
        let d = [
            snap.k.wrapping_sub(prev.k) as i64,
            snap.angle.wrapping_sub(prev.angle) as i32 as i64,
            snap.peri - prev.peri,
        ];
        pop.dk.add(d[0] as i128);
        pop.dangle.add(d[1] as i128);
        pop.dperi.add(d[2] as i128);
        let mut ema = prev.ema;
        for f in 0..3 {
            let innov = d[f] - ema[f];
            match f {
                0 => pop.dk_innov.add(innov as i128),
                1 => pop.dangle_innov.add(innov as i128),
                _ => pop.dperi_innov.add(innov as i128),
            }
            ema[f] += (d[f] - ema[f]) >> 6;
        }
        let mut snap = snap;
        snap.ema = ema;
        // The fired kick's raw dv: whole quanta back in 2^-16 units plus the carry's move.
        pop.raw.push([
            rec.b.kick.dv[0] as i64 * 65536 + (snap.carry[0] - prev.carry[0]),
            rec.b.kick.dv[1] as i64 * 65536 + (snap.carry[1] - prev.carry[1]),
        ]);
        digest.update(
            format!("{i} {} {:?} {:?} {} {} {}", snap.ev, snap.res, snap.carry, snap.k, snap.angle, snap.peri).as_bytes(),
        );
        last[i] = Some(snap);
    }
}

fn per_pop(p: &Pop, n_ships: usize, game_seconds: f64) -> serde_json::Value {
    let ship_seconds = n_ships as f64 * game_seconds;
    json!({
        "ships": n_ships,
        "bindings": p.bindings,
        "non_kick_bindings": p.other,
        "bindings_per_ship_game_second": if ship_seconds > 0.0 { p.bindings as f64 / ship_seconds } else { f64::NAN },
        "items_per_binding": if p.bindings == 0 { 0.0 } else { p.events as f64 / p.bindings as f64 },
        "bits_per_binding": {
            "debt_after_refit": (p.debt_bits() * 1e2).round() / 1e2,
            "debt_after_refit_and_ema": (p.debt_innov_bits() * 1e2).round() / 1e2,
            "cause_dv": (p.cause_bits() * 1e2).round() / 1e2,
            "both": (p.both_bits() * 1e2).round() / 1e2,
        },
        "streams": {
            "dv_quanta": p.dv.json(), "residual": p.res.json(), "carry": p.carry.json(),
            "d_shape_k": p.dk.json(), "d_angle": p.dangle.json(), "d_peri_time": p.dperi.json(),
            "d_shape_k_innov": p.dk_innov.json(), "d_angle_innov": p.dangle_innov.json(), "d_peri_time_innov": p.dperi_innov.json(),
        },
        "raw_kicks_journaled": p.raw.len(),
        "fire_fraction_at_coarser_words": p.sweep(),
        "bits_per_ship_game_second": {
            "debt_after_refit": if ship_seconds > 0.0 { p.debt_bits() * p.bindings as f64 / ship_seconds } else { f64::NAN },
            "cause_dv": if ship_seconds > 0.0 { p.cause_bits() * p.bindings as f64 / ship_seconds } else { f64::NAN },
            "both": if ship_seconds > 0.0 { p.both_bits() * p.bindings as f64 / ship_seconds } else { f64::NAN },
            "debt_after_refit_and_ema": if ship_seconds > 0.0 { p.debt_innov_bits() * p.bindings as f64 / ship_seconds } else { f64::NAN },
        },
    })
}

/// The plane's own scripted scene (the first run's four commands, instrument v2).
pub(super) fn run(mut s: super::session::Session, seconds: f64) -> crate::Result<u8> {
    let machine_before = crate::measure::machine_state("before");
    let made_n = s.n_bodies();
    let (mut made, mut members) = (Pop::default(), Pop::default());
    let mut last: Vec<Option<Snap>> = Vec::new();
    let mut digest = blake3::Hasher::new();
    let start = s.p.u.now;
    let mut frames = 0usize;
    let wall = Instant::now();
    for n in 1..=(seconds * 60.0) as usize {
        if wall.elapsed().as_secs_f64() >= 55.0 {
            return Err("H_live replay exceeded 55 s; no complete result".into());
        }
        let now = s.p.u.now;
        let keys = script(n);
        s.p.u.input(now, keys).map_err(|e| format!("input: {e:?}"))?;
        journal(&s.p.u, &mut last, made_n, &mut made, &mut members, &mut digest);
        s.p.u.frame(1.0 / 60.0, s.rtf, Budget::unlimited());
        s.p.u.settle(s.p.u.now);
        frames = n;
    }
    let game_seconds = (s.p.u.now - start) as f64 * TICK_SECONDS;
    let ships = (0..s.n_bodies())
        .filter(|&i| { let r = s.p.u.rec(i); r.kind == Kind::Ship && r.alive })
        .count();
    let total = made.both_bits() * made.bindings as f64 + members.both_bits() * members.bindings as f64;
    let nb = (made.bindings + members.bindings).max(1) as f64;
    let both = total / nb;
    let debt = (made.debt_bits() * made.bindings as f64 + members.debt_bits() * members.bindings as f64) / nb;
    let cause = (made.cause_bits() * made.bindings as f64 + members.cause_bits() * members.bindings as f64) / nb;
    let rate = total / (ships as f64 * game_seconds);
    println!("{}", serde_json::to_string_pretty(&json!({
        "scope": "one journal entry per rebound ship at deterministic 60 Hz plane snapshots; storage streams; v2 (dperi fed, multiplicities counted)",
        "code": "magnitude-class entropy (class + in-class + sign): within ~1 bit/field of an ideal per-field coder",
        "scene": {"seed": s.seed, "rtf": s.rtf, "frames": frames, "game_seconds": game_seconds,
                  "bodies": s.n_bodies(), "ships": ships, "bytes_per_body": s.bytes_per_body(),
                  "stats": {"kicks": s.stats().kicks, "events": s.stats().events()}},
        "made": per_pop(&made, made_n.min(ships), game_seconds),
        "members": per_pop(&members, ships.saturating_sub(made_n), game_seconds),
        "hlive": {
            "bits_total_both": total,
            "bits_per_binding": {"debt_after_refit": (debt * 1e2).round() / 1e2, "cause_dv": (cause * 1e2).round() / 1e2, "both": (both * 1e2).round() / 1e2},
            "bits_per_ship_game_second": rate,
            "game_seconds_to_64_bits": 64.0 / rate,
            "game_minutes_to_64_bits": 64.0 / rate / 60.0,
        },
        "machine": {"before": machine_before},
        "digest": digest.finalize().to_hex()[..16].to_string(),
    }))?);
    Ok(0)
}

/// A quiescent belt: the star and the three planets of the plane's system (no moon: it cannot
/// reach the belt), `n` ships between 2.1 and 3.5 AU — banded semi-major axis, Rayleigh e,
/// uniform angles and phases, one seeded LCG, nothing engineered. No fleet, no player, no input.
fn belt(seed: u64, threads: usize, n: usize, lo: f64, hi: f64) -> crate::Result<Plane> {
    let mut u = emergent_universe::Universe::new(s(STAR_RADIUS), Config::default());
    u.threads = threads;
    let mut rng = seed ^ 0x5DEECE66D ^ 0xBE17;
    let mut lcg = |rng: &mut u64| {
        *rng = rng.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        (*rng >> 11) as f64 / (1u64 << 53) as f64
    };
    let mut planets = Vec::new();
    let mut names = Vec::new();
    for p in &PLANETS {
        let b = err(u.add_body(
            Kind::Planet,
            OrbitSpec { doll: 0, periapsis: s(p.periapsis), e_q48: p.e_q48, clockwise: false, angle: p.angle, phase: p.phase },
            Scalar::ZERO,
        ))?;
        let surface = err(Scalar::raw(p.radius as i128, -p.mass_log2))?;
        err(u.add_doll(p.name, b, p.mass_log2, surface))?;
        planets.push(b);
        names.push(p.name.to_string());
    }
    let mut ships = Vec::new();
    for j in 0..n {
        // Banded p: 8 bands spanning [lo, hi] AU, ±4% AU jitter within a band.
        let band = (j * 8 / n.max(1)) as f64;
        let a = (lo + (hi - lo) * (band / 8.0 + 0.05 * (lcg(&mut rng) - 0.5))) * AU as f64;
        // Rayleigh e of sigma 0.07.
        let e = 0.07 * (-2.0 * lcg(&mut rng).max(1e-12).ln()).sqrt();
        let id = err(u.add_body(
            Kind::Ship,
            OrbitSpec {
                doll: 0,
                periapsis: s((a * (1.0 - e)) as i64),
                e_q48: (e * (1u64 << 48) as f64) as u64,
                clockwise: false,
                angle: (lcg(&mut rng) * 4294967296.0) as u32,
                phase: (lcg(&mut rng) * 4294967296.0) as u32,
            },
            err(Scalar::raw(34, -10))?,
        ))?;
        ships.push(id);
        names.push(format!("Belt {j}"));
    }
    err(u.start())?;
    Ok(Plane { u, planets, dolls: Vec::new(), moon: usize::MAX, player: usize::MAX, ships, fleet: usize::MAX, names })
}

/// The checker's named experiment: H_live on the quiescent belt, with the plane's per-binding
/// program refit, journaling debt (post-refit record) and cause (applied kick quanta) apart.
pub(super) fn run_belt(seed: u64, threads: usize, n: usize, rtf: f64, seconds: f64, lo: f64, hi: f64) -> crate::Result<u8> {
    let machine_before = crate::measure::machine_state("before");
    let mut p = belt(seed, threads, n, lo, hi)?;
    let made_n = p.u.n_bodies(); // every ship is a belt body (the planets come first)
    let (mut made, mut members) = (Pop::default(), Pop::default());
    let mut last: Vec<Option<Snap>> = Vec::new();
    let mut digest = blake3::Hasher::new();
    let start = p.u.now;
    let mut frames = 0usize;
    let wall = Instant::now();
    for _n in 1..=(seconds * 60.0) as usize {
        if wall.elapsed().as_secs_f64() >= 55.0 {
            return Err(format!(
                "belt replay exceeded 55 s at frame {frames} (game {:.2} s); no complete result",
                (p.u.now - start) as f64 * TICK_SECONDS
            ).into());
        }
        journal(&p.u, &mut last, made_n, &mut made, &mut members, &mut digest);
        p.u.frame(1.0 / 60.0, rtf, Budget::unlimited());
        p.u.settle(p.u.now);
        frames += 1;
    }
    let game_seconds = (p.u.now - start) as f64 * TICK_SECONDS;
    let ships = (0..p.u.n_bodies())
        .filter(|&i| { let r = p.u.rec(i); r.kind == Kind::Ship && r.alive })
        .count();
    let rate_both = made.both_bits() * made.bindings as f64 / (ships as f64 * game_seconds);
    let rate_debt = made.debt_bits() * made.bindings as f64 / (ships as f64 * game_seconds);
    println!("{}", serde_json::to_string_pretty(&json!({
        "scope": "quiescent belt (star + 3 planets, no moon/fleet/player/input); per-binding program refit (the plane rebinds a fresh tube at every binding); debt = post-refit record, cause = applied kick quanta",
        "code": "magnitude-class entropy (class + in-class + sign); multiplicities counted",
        "scene": {"seed": seed, "rtf": rtf, "frames": frames, "game_seconds": game_seconds, "belt_au": [lo, hi],
                  "bodies": p.u.n_bodies(), "ships": ships, "years": game_seconds / 3.156e7,
                  "bytes_per_body": p.u.bytes_per_body(),
                  "stats": {"kicks": p.u.stats.kicks, "events": p.u.stats.events()}},
        "belt": per_pop(&made, ships, game_seconds),
        "hlive": {
            "bits_per_binding": {"debt_after_refit": (made.debt_bits() * 1e2).round() / 1e2, "debt_after_refit_and_ema": (made.debt_innov_bits() * 1e2).round() / 1e2, "cause_dv": (made.cause_bits() * 1e2).round() / 1e2, "both": (made.both_bits() * 1e2).round() / 1e2},
            "bits_per_ship_game_second": {"debt_after_refit": rate_debt, "debt_after_refit_and_ema": made.debt_innov_bits() * made.bindings as f64 / (ships as f64 * game_seconds), "both": rate_both},
            "game_seconds_to_64_bits": 64.0 / rate_both,
            "game_days_to_64_bits": 64.0 / rate_both / 86400.0,
        },
        "machine": {"before": machine_before},
        "digest": digest.finalize().to_hex()[..16].to_string(),
    }))?);
    Ok(0)
}
