//! How often the lattice bin predicate (`emergent_lattice::law::hit`) wraps its `i128`s in the player's neighbourhood scan,
//! and what it answers when it does. The scan applies it to the pair's separation `d` and relative displacement `w` in units
//! of `reach/2^20`; `hit` squares products of those, so for |d|·|w| beyond 2^63 in its units the squares wrap and the answer is
//! garbage. This probe runs a scripted flight with a finder that, for every pair the original finder tested, also evaluates the
//! predicate in `f64` (the same branches, no wrap) and counts: pairs tested, pairs where an `i128` product wrapped, the wrapped
//! predicate's yes against the true one's, and the encounters the digest hashes that the true predicate would not have found.
//!
//! cargo run --release -p emergent-universe --example hit_wrap [-- <wall seconds> <keys> <level> <seed>]
use emergent_lattice::law::hit;
use emergent_space::orbit::Scalar;
use emergent_universe::ctx::Ctx;
use emergent_universe::encounter::{Encounter, Encounters, ENCOUNTER_LOG2};
use emergent_universe::fleet::Order;
use emergent_universe::num::{sub2, time_of, Res, Tick};
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::sync::Mutex;

/// The predicate in floats, branch for branch.
fn hit_f64(d: [f64; 2], w: [f64; 2], reach: f64) -> bool {
    let dot = |a: [f64; 2], b: [f64; 2]| a[0] * b[0] + a[1] * b[1];
    let (dd, dw, ww, rr) = (dot(d, d), dot(d, w), dot(w, w), reach * reach);
    if dd <= rr {
        dw < 0.0
    } else if ww == 0.0 || dw >= 0.0 {
        false
    } else if -dw >= ww {
        let e = [d[0] + w[0], d[1] + w[1]];
        dot(e, e) <= rr
    } else {
        let cross = d[0] * w[1] - d[1] * w[0];
        cross * cross <= rr * ww
    }
}

/// Whether any product `hit` forms would leave `i128`.
fn wraps(d: [i128; 2], w: [i128; 2], reach: i128) -> bool {
    let big = |a: i128, b: i128| a.checked_mul(b).is_none();
    let dot = |a: [i128; 2], b: [i128; 2]| -> Option<i128> { a[0].checked_mul(b[0])?.checked_add(a[1].checked_mul(b[1])?) };
    let (Some(dd), Some(_), Some(ww)) = (dot(d, d), dot(d, w), dot(w, w)) else { return true };
    let _ = dd;
    let cross = d[0].checked_mul(w[1]).and_then(|x| x.checked_sub(d[1].checked_mul(w[0])?));
    let Some(cross) = cross else { return true };
    big(cross, cross) || big(reach, reach) || big(reach * reach, ww)
}

#[derive(Default)]
struct Tally {
    tested: u64,
    wrapped: u64,
    wrapped_yes: u64,
    wrapped_yes_but_true_no: u64,
    wrapped_no_but_true_yes: u64,
    unwrapped_yes: u64,
    contact_wrapped_yes: u64,
}

struct Probe(Mutex<Tally>);
impl Encounters for Probe {
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter> {
        let mut out = Vec::new();
        let Some(me) = ctx.bodies.binding_at(body, t) else { return out };
        let Ok((x, v)) = me.cartesian(t) else { return out };
        let Ok(h) = time_of(interval, me.clock_exp) else { return out };
        let mut tally = self.0.lock().unwrap();
        for j in 0..ctx.bodies.len() {
            if j == body || !ctx.bodies.alive(j) || t <= ctx.info[j].born {
                continue;
            }
            let Some(other) = ctx.bodies.binding_at(j, t) else { continue };
            if other.doll != me.doll {
                continue;
            }
            let reach = ctx.info[body].radius.add(ctx.info[j].radius).unwrap_or(Scalar::ZERO);
            if reach.is_zero() {
                continue;
            }
            let found = (|| -> Res<Option<(bool, bool, bool, bool)>> {
                let (xj, vj) = other.cartesian(t)?;
                let d = sub2(xj, x)?;
                let w = [vj[0].sub(v[0])?.mul(h)?, vj[1].sub(v[1])?.mul(h)?];
                let q_exp = reach.exponent() as i32 - 20;
                let integers = |a: [Scalar; 2]| -> Res<[i128; 2]> { Ok([a[0].fixed(-q_exp)?, a[1].fixed(-q_exp)?]) };
                let (di, wi) = (integers(d)?, integers(w)?);
                let near = reach.scale(ENCOUNTER_LOG2)?.fixed(-q_exp)?;
                let contact = reach.fixed(-q_exp)?;
                tally.tested += 1;
                let wrap = wraps(di, wi, near);
                let wrapped_answer = hit(di, wi, near);
                let f = |a: [i128; 2]| [a[0] as f64, a[1] as f64];
                let true_answer = hit_f64(f(di), f(wi), near as f64);
                Ok(Some((wrap, wrapped_answer, true_answer, wrapped_answer && hit(di, wi, contact))))
            })();
            if let Ok(Some((wrap, wrapped_answer, true_answer, contact))) = found {
                if wrap {
                    tally.wrapped += 1;
                }
                if wrapped_answer {
                    if wrap {
                        tally.wrapped_yes += 1;
                        tally.contact_wrapped_yes += contact as u64;
                        if !true_answer {
                            tally.wrapped_yes_but_true_no += 1;
                        }
                    } else {
                        tally.unwrapped_yes += 1;
                    }
                    out.push(Encounter { a: body, b: j, t, contact });
                } else if wrap && true_answer {
                    tally.wrapped_no_but_true_yes += 1;
                }
            }
        }
        out
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let seconds: f64 = args.get(1).and_then(|s| s.parse().ok()).unwrap_or(12.0);
    let keys: u8 = args.get(2).and_then(|s| s.parse().ok()).unwrap_or(0);
    let level: u8 = args.get(3).and_then(|s| s.parse().ok()).unwrap_or(0);
    let seed: u64 = args.get(4).and_then(|s| s.parse().ok()).unwrap_or(1);
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, 48).unwrap();
    // The probe is the whole finder (it has no `capture`), so the scans run where they are taken.
    let probe = std::sync::Arc::new(Probe(Mutex::new(Tally::default())));
    struct Shared(std::sync::Arc<Probe>);
    impl Encounters for Shared {
        fn find(&self, c: &Ctx, b: usize, t: Tick, i: Tick) -> Vec<Encounter> {
            self.0.find(c, b, t, i)
        }
    }
    p.u.set_encounters(Box::new(Shared(probe.clone())));
    if keys != 0 {
        p.u.schedule((1.0 * 100.0 / TICK_SECONDS) as i64, word(keys, level)).unwrap();
    }
    let cut = (seconds * 100.0 / TICK_SECONDS) as i64;
    while p.u.now < cut {
        p.u.frame_to(1.0 / 60.0, 100.0, Budget::unlimited(), cut);
    }
    p.u.settle(cut);
    let t = probe.0.lock().unwrap();
    println!(
        "keys {keys} level {level} seed {seed}, {seconds} s: tested {} pairs; {} ({:.1}%) wrapped an i128 product; the predicate said yes {} times on unwrapped products, {} on wrapped ones ({} of them contacts); \
         of the wrapped yeses, {} ({:.0}%) the true predicate says no; the wrapped predicate said no {} times where the true one says yes; the digest hashed {} encounters",
        t.tested,
        t.wrapped,
        100.0 * t.wrapped as f64 / t.tested.max(1) as f64,
        t.unwrapped_yes,
        t.wrapped_yes,
        t.contact_wrapped_yes,
        t.wrapped_yes_but_true_no,
        100.0 * t.wrapped_yes_but_true_no as f64 / t.wrapped_yes.max(1) as f64,
        t.wrapped_no_but_true_yes,
        p.u.stats.encounters,
    );
}
