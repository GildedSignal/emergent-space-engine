//! B18 memory (docs/law.md; a requirement from the goal, 8 GB for billions of ships, not a size
//! chosen for a representation). The law reports how many bytes it holds per live body on the
//! population ladder of `crates/shipmem` (research crate, 30 September; `artifacts/runs/opus-shipmem`),
//! counting everything it keeps for the bodies: the tube, the catalogue's share, the event records
//! and the remainders. The judge compares it with the information floor of the same population.
//!
//! - The scenes are the ladder's frozen rungs, read from `crates/shipmem/src/pop.rs` (`ladder`) and
//!   `examples/ladder.rs`: a convoy of 2^20 ships launched every 2^12 time quanta (an exact program),
//!   each ship kicked with probability 0, 1e-4, 1e-3, 1e-2, 1e-1, 0.3 or 1 (the degradation); a convoy
//!   with Poisson launches (no program); ships drawn uniformly over the law's ranges (no structure);
//!   and, for the small-population case where the header of each population matters, 256 populations
//!   of 4096 ships at kicks 0, 1e-2 and 1e-1. A scene is a recipe: the law builds the population from
//!   it (`ladder(rung, members, g)` for g in 0..populations, seed 99).
//! - The floor is the entropy of the draws that made the population, in bits per ship, as the
//!   ladder measured it (`floor_bits` in `ladder.jsonl`, frozen here). Nothing can store a
//!   population losslessly in fewer bits.
//! - PASS iff on every scene the answer is at most 2× the floor plus 2 bytes. An answer under half
//!   the floor is also a failure: a lossless store cannot be there, so it is a claim and not a count.
//!   A law that has not implemented the method fails (the trait default is None), and so does a NaN.
//! - Reported, not gated: the answer scaled to 10^9 bodies, in GB, at the least and the most costly
//!   scene. The law's count is its own; the byte arithmetic that supports it is in the shipmem tests.

use super::{Gate, Law};

/// How a ladder population was made (`pop::Rung`).
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Rung {
    /// An exact convoy program, each ship kicked with this probability.
    Kicked(f64),
    /// Poisson launches, no program.
    Poisson,
    /// Every field uniform over the law's ranges.
    Random,
}

/// One scene of the ladder: `populations` populations of `members` ships each.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct MemoryScene {
    pub rung: Rung,
    pub members: usize,
    pub populations: usize,
}

#[cfg(test)]
impl MemoryScene {
    pub fn bodies(&self) -> usize {
        self.members * self.populations
    }
}

const MILLION: usize = 1 << 20;

/// The frozen ladder: each scene with its measured information floor, in bits per ship.
pub const LADDER: [(MemoryScene, f64); 12] = [
    (MemoryScene { rung: Rung::Kicked(0.0), members: MILLION, populations: 1 }, 0.0001),
    (MemoryScene { rung: Rung::Kicked(1e-4), members: MILLION, populations: 1 }, 0.0068),
    (MemoryScene { rung: Rung::Kicked(1e-3), members: MILLION, populations: 1 }, 0.0610),
    (MemoryScene { rung: Rung::Kicked(1e-2), members: MILLION, populations: 1 }, 0.5762),
    (MemoryScene { rung: Rung::Kicked(1e-1), members: MILLION, populations: 1 }, 5.4785),
    (MemoryScene { rung: Rung::Kicked(0.3), members: MILLION, populations: 1 }, 15.8826),
    (MemoryScene { rung: Rung::Kicked(1.0), members: MILLION, populations: 1 }, 50.0001),
    (MemoryScene { rung: Rung::Poisson, members: MILLION, populations: 1 }, 13.4427),
    (MemoryScene { rung: Rung::Random, members: MILLION, populations: 1 }, 207.9999),
    (MemoryScene { rung: Rung::Kicked(0.0), members: 4096, populations: 256 }, 0.0352),
    (MemoryScene { rung: Rung::Kicked(1e-2), members: 4096, populations: 256 }, 0.6056),
    (MemoryScene { rung: Rung::Kicked(1e-1), members: 4096, populations: 256 }, 5.4702),
];

/// The scene's information floor in bytes per body, from the frozen ladder. None: not a ladder scene.
pub fn floor_bytes(scene: &MemoryScene) -> Option<f64> {
    LADDER.iter().find(|(s, _)| s == scene).map(|(_, bits)| bits / 8.0)
}

/// The limit: twice the floor plus two bytes.
pub fn limit_bytes(floor: f64) -> f64 {
    2.0 * floor + 2.0
}

fn name(scene: &MemoryScene) -> String {
    let rung = match scene.rung {
        Rung::Kicked(x) => format!("kicked {x}"),
        Rung::Poisson => "Poisson".to_string(),
        Rung::Random => "random".to_string(),
    };
    format!("{rung} ({} x {})", scene.populations, scene.members)
}

pub fn b18(law: &dyn Law) -> Gate {
    let (mut ok, mut missing, mut under, mut over) = (0, Vec::new(), Vec::new(), Vec::new());
    let (mut lo, mut hi) = ((f64::INFINITY, String::new()), (0.0f64, String::new()));
    let mut worst_ratio = 0.0f64;
    for (scene, bits) in &LADDER {
        let (floor, label) = (bits / 8.0, name(scene));
        let limit = limit_bytes(floor);
        match law.bytes_per_body(scene).filter(|b| b.is_finite() && *b >= 0.0) {
            None => missing.push(label),
            Some(bytes) if bytes < 0.5 * floor => under.push(format!("{label}: {bytes:.2e} B under the floor of {floor:.2e} B")),
            Some(bytes) if bytes > limit => over.push(format!("{label}: {bytes:.3} B over the limit {limit:.3} B")),
            Some(bytes) => {
                ok += 1;
                worst_ratio = worst_ratio.max(bytes / limit);
                if bytes < lo.0 {
                    lo = (bytes, label.clone());
                }
                if bytes > hi.0 {
                    hi = (bytes, label);
                }
            }
        }
    }
    let pass = ok == LADDER.len();
    let mut detail = format!("memory: {ok}/{} ladder scenes within 2x the information floor + 2 bytes", LADDER.len());
    if pass {
        detail += &format!(", worst {worst_ratio:.3} of the limit; at 1e9 bodies {:.2e} GB ({}) to {:.1} GB ({}) (reported; one byte per body is one GB)", lo.0, lo.1, hi.0, hi.1);
    } else {
        if !missing.is_empty() {
            detail += &format!("; {} not answered ({})", missing.len(), missing.join(", "));
        }
        if !under.is_empty() {
            detail += &format!("; {} below the floor ({})", under.len(), under.join("; "));
        }
        if !over.is_empty() {
            detail += &format!("; {} over the limit ({})", over.len(), over.join("; "));
        }
    }
    Gate { id: "B18", pass, detail, secs: 0.0 }
}

#[cfg(test)]
mod tests {
    use super::super::laws::{Echo, Fault, Planted, Silent};
    use super::*;

    /// echo's floors, but the answer for each scene comes from the closure.
    struct Bytes(Box<dyn Fn(&MemoryScene, f64) -> Option<f64>>);
    impl Law for Bytes {
        fn advance_per_cycle(&self, p: f64, e: f64) -> Option<(f64, f64, f64)> {
            Echo.advance_per_cycle(p, e)
        }
        fn deflection(&self, b: f64) -> Option<f64> {
            Echo.deflection(b)
        }
        fn captured(&self, energy: f64, angular: f64) -> bool {
            Echo.captured(energy, angular)
        }
        fn photon_captured(&self, b: f64) -> bool {
            Echo.photon_captured(b)
        }
        fn long_run(&self, p: f64, e: f64, cycles: usize) -> Vec<(f64, f64, f64, f64)> {
            Echo.long_run(p, e, cycles)
        }
        fn bytes_per_body(&self, scene: &MemoryScene) -> Option<f64> {
            (self.0)(scene, floor_bytes(scene)?)
        }
    }
    fn bytes(f: impl Fn(&MemoryScene, f64) -> Option<f64> + 'static) -> Bytes {
        Bytes(Box::new(f))
    }

    #[test]
    fn the_ladder_is_the_shipmem_ladder_of_twelve_scenes_with_the_measured_floors() {
        assert_eq!(LADDER.len(), 12);
        // 2^20 ships, one population, nine rungs; then 256 populations of 4096 at three of them.
        assert_eq!(LADDER[..9].iter().map(|(s, _)| s.bodies()).collect::<Vec<_>>(), vec![1 << 20; 9]);
        assert_eq!(LADDER[9..].iter().map(|(s, _)| (s.members, s.populations, s.bodies())).collect::<Vec<_>>(), vec![(4096, 256, 1 << 20); 3]);
        // The floor rises with the kicked fraction, from nothing to the 50 bits of a convoy all kicked; random is 208.
        let kicked: Vec<f64> = LADDER[..7].iter().map(|x| x.1).collect();
        assert!(kicked.windows(2).all(|w| w[0] < w[1]) && kicked[0] < 1e-3 && (kicked[6] - 50.0).abs() < 1e-3);
        assert!((LADDER[8].1 - 208.0).abs() < 1e-3 && (LADDER[7].1 - 13.44).abs() < 0.01);
        assert_eq!(floor_bytes(&LADDER[3].0), Some(0.5762 / 8.0));
        assert_eq!(floor_bytes(&MemoryScene { rung: Rung::Poisson, members: 5, populations: 1 }), None);
        assert_eq!(limit_bytes(0.0), 2.0);
    }

    #[test]
    fn echo_sits_on_the_floor_and_passes_with_the_ladder_on_the_line() {
        let g = b18(&Echo);
        assert!(g.pass && g.detail.contains("12/12") && g.detail.contains("at 1e9 bodies"), "{}", g.detail);
        // 26 bytes per body for random ships is 26 GB at 1e9: the floor itself does not fit 8 GB (reported).
        assert!(g.detail.contains("26.0 GB (random"), "{}", g.detail);
    }

    #[test]
    fn the_planted_sixteen_byte_tube_fails_where_the_floor_is_below_seven_bytes() {
        let g = b18(&Planted(Fault::Fat));
        // 16 B exceeds 2·floor + 2 whenever floor < 7 B = 56 bits: every rung except random (26 B) and the all-kicked convoy (6.25 B: limit 14.5).
        assert!(!g.pass && g.detail.contains("over the limit") && g.detail.contains("Poisson") && g.detail.contains("kicked 0 ("), "{}", g.detail);
        assert!(!g.detail.contains("random (1 x"), "{}", g.detail);
    }

    #[test]
    fn two_bytes_of_slack_and_twice_the_floor_are_the_limit_and_nothing_below_half_the_floor_counts() {
        // Exactly the limit passes; a hair over fails on that scene alone.
        assert!(b18(&bytes(|_, f| Some(limit_bytes(f)))).pass);
        let g = b18(&bytes(|s, f| Some(if s.rung == Rung::Random { limit_bytes(f) * 1.001 } else { limit_bytes(f) })));
        assert!(!g.pass && g.detail.contains("1 over the limit") && g.detail.contains("random"), "{}", g.detail);
        // A zero is a claim, not a count: the floor is information, and a lossless store cannot be under it.
        let g = b18(&bytes(|_, _| Some(0.0)));
        assert!(!g.pass && g.detail.contains("below the floor"), "{}", g.detail);
        assert!(b18(&bytes(|_, f| Some(0.5 * f))).pass);
        // Not implemented, a NaN, a negative and one unanswered scene all fail.
        assert!(!b18(&Silent).pass && b18(&Silent).detail.contains("12 not answered"));
        assert!(!b18(&bytes(|_, _| Some(f64::NAN))).pass);
        assert!(!b18(&bytes(|_, _| Some(-1.0))).pass);
        assert!(!b18(&bytes(|s, f| if s.members == 4096 { None } else { Some(f) })).pass);
    }
}
