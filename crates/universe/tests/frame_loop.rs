//! The frame loop's levers move no bit (AGENTS.md: "Every digest bit for bit"; gate F1 is about *when* work happens).
//!
//! **Frozen before the first run.** The player's neighbourhood finder is `crates/universe/src/encounter.rs`'s
//! `PlayerNeighbourhood`: a repeat of the last scan answered once, and scans held for idle time. Against the original,
//! brute-force finder (every body read at every scan, copied here), the same scripted flights must give the same digest,
//! the same encounter log (as far as it is kept) and the same counts, whatever carried them: no budget at all, a wall
//! budget that bites (the scans wait for idle time and the cut's settle answers them), a budget with next to no idle time
//! (they pile up; a digest taken with them held is the digest after they are answered). Control (the test must be able to
//! fail): a finder that reuses the last scan whatever the tick, the interval and the bodies gives another digest.
use emergent_universe::ctx::Ctx;
use emergent_universe::encounter::{Encounter, Encounters, PlayerNeighbourhood, ENCOUNTER_LOG2};
use emergent_universe::fleet::Order;
use emergent_universe::num::{sub2, time_of, Res, Tick};
use emergent_universe::scenario::plane;
use emergent_universe::thrust::word;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use emergent_lattice::law::hit;
use emergent_space::orbit::Scalar;

const RTF: f64 = 100.0;

/// The finder as it was before the filter: every body in the player's doll read at every scan, the predicate on each.
struct Brute;
impl Encounters for Brute {
    fn find(&self, ctx: &Ctx, body: usize, t: Tick, interval: Tick) -> Vec<Encounter> {
        let mut out = Vec::new();
        let Some(me) = ctx.bodies.binding_at(body, t) else { return out };
        let Ok((x, v)) = me.cartesian(t) else { return out };
        let Ok(h) = time_of(interval, me.clock_exp) else { return out };
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
            let found = (|| -> Res<Option<bool>> {
                let (xj, vj) = other.cartesian(t)?;
                let d = sub2(xj, x)?;
                let w = [vj[0].sub(v[0])?.mul(h)?, vj[1].sub(v[1])?.mul(h)?];
                let q_exp = reach.exponent() as i32 - 20;
                let integers = |a: [Scalar; 2]| -> Res<[i128; 2]> { Ok([a[0].fixed(-q_exp)?, a[1].fixed(-q_exp)?]) };
                let (di, wi) = (integers(d)?, integers(w)?);
                let near = reach.scale(ENCOUNTER_LOG2)?.fixed(-q_exp)?;
                if !hit(di, wi, near) {
                    return Ok(None);
                }
                Ok(Some(hit(di, wi, reach.fixed(-q_exp)?)))
            })();
            if let Ok(Some(contact)) = found {
                out.push(Encounter { a: body, b: j, t, contact });
            }
        }
        out
    }
}

/// (name, seed, members, script of (wall second, keys, level)).
fn flights() -> Vec<(&'static str, u64, u64, Vec<(f64, u8, u8)>)> {
    vec![
        ("coast", 1, 48, vec![]),
        ("reverse L15", 1, 48, vec![(1.0, 2, 15)]),
        ("burn, coast, brake L8", 3, 16, vec![(1.0, 2, 8), (3.0, 0, 8), (4.0, 1, 8), (6.0, 0, 8)]),
    ]
}

/// What a flight leaves: the digest at the cut, the encounter log, the counts.
type Outcome = (String, Vec<Encounter>, u64, u64);

fn fly(seed: u64, members: u64, script: &[(f64, u8, u8)], seconds: f64, finder: Option<Box<dyn Encounters>>, budget: Budget) -> (Outcome, usize) {
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, members).unwrap();
    if let Some(f) = finder {
        p.u.set_encounters(f);
    }
    for &(wall, keys, level) in script {
        p.u.schedule((wall * RTF / TICK_SECONDS) as i64, word(keys, level)).unwrap();
    }
    let cut = (seconds * RTF / TICK_SECONDS) as i64;
    let mut held = 0;
    for _ in 0..100_000 {
        if p.u.now >= cut {
            break;
        }
        p.u.frame_to(1.0 / 60.0, RTF, budget, cut);
        held = held.max(p.u.held_scans());
    }
    // Held scans count as answered in the digest, before and after they are.
    let before = p.u.digest();
    p.u.flush_scans();
    assert_eq!(p.u.held_scans(), 0, "a flush answers every held scan");
    assert_eq!(p.u.digest(), before, "a digest taken with scans held is the digest after they are answered");
    p.u.settle(cut);
    ((p.u.digest(), p.u.enc_log.clone(), p.u.stats.encounters, p.u.contacts), held)
}

#[test]
fn the_repeat_and_the_idle_scans_find_what_the_brute_force_finds() {
    for (name, seed, members, script) in flights() {
        let seconds = 6.0;
        let (brute, _) = fly(seed, members, &script, seconds, Some(Box::new(Brute)), Budget::unlimited());
        assert!(brute.2 > 0, "{name}: the flight must have encounters to find");
        let (default, _) = fly(seed, members, &script, seconds, None, Budget::unlimited());
        assert_eq!(default, brute, "{name}: the default finder");
        // A wall budget that bites: the scans are held and answered in idle time and at the cut.
        let (idle, held) = fly(seed, members, &script, seconds, None, Budget::wall(2.0));
        assert_eq!(idle, brute, "{name}: scans held for idle time");
        println!("{name}: {} encounters ({} contacts), at most {held} scans held", brute.2, brute.3);
    }
}

#[test]
fn scans_wait_for_idle_time_and_a_digest_counts_them() {
    // A budget with next to no idle time (0.3 ms a frame, the mandatory items first): the scans pile up, the digest taken
    // with them held is the digest after they are answered, and the cut's digest is still the brute force's.
    let (name, seed, members, script) = flights().remove(1);
    let seconds = 4.0;
    let cut = (seconds * RTF / TICK_SECONDS) as i64;
    let mut p = plane(Config::default(), seed, Order::Sparse, 1, members).unwrap();
    for &(wall, keys, level) in &script {
        p.u.schedule((wall * RTF / TICK_SECONDS) as i64, word(keys, level)).unwrap();
    }
    for _ in 0..400 {
        p.u.frame_to(1.0 / 60.0, RTF, Budget::wall(0.3), cut);
    }
    let held = p.u.held_scans();
    assert!(held > 20, "{name}: with next to no idle time the scans must pile up ({held})");
    let before = p.u.digest();
    p.u.flush_scans();
    assert_eq!(p.u.held_scans(), 0);
    assert_eq!(p.u.digest(), before, "{name}: a digest taken with {held} scans held is the digest after they are answered");
    p.u.settle(cut);
    let (brute, _) = fly(seed, members, &script, seconds, Some(Box::new(Brute)), Budget::unlimited());
    assert_eq!((p.u.digest(), p.u.enc_log.clone(), p.u.stats.encounters, p.u.contacts), brute, "{name}: the cut after held scans");
}

#[test]
fn the_controls_can_fail() {
    let (_, seed, members, script) = flights().remove(2);
    let (brute, _) = fly(seed, members, &script, 6.0, Some(Box::new(Brute)), Budget::unlimited());
    let (sloppy, _) = fly(seed, members, &script, 6.0, Some(Box::new(PlayerNeighbourhood::planted_sloppy_reuse())), Budget::unlimited());
    assert_ne!(sloppy.0, brute.0, "a planted sloppy reuse must be caught by the digest");
}
