//! Boundary between the frozen judge's vocabulary and the shipmem implementation.
use super::super::{belt, memory};
use emergent_shipmem::belt::{Body, Population, Spec};

pub(super) fn birth(spec: &belt::BeltSpec, n: u64, seed: u64) -> Option<Box<dyn belt::Belt>> {
    let spec = Spec {
        p_lo: spec.p_lo.try_into().ok()?,
        p_bits: spec.p_bits.try_into().ok()?,
        sigma_milli: spec.sigma_milli.try_into().ok()?,
        e_bits: spec.e_bits.try_into().ok()?,
        e_cap: spec.e_cap.try_into().ok()?,
        w_bits: spec.w_bits.try_into().ok()?,
        t_bits: spec.t_bits.try_into().ok()?,
    };
    Population::birth(spec, n, seed).map(|b| Box::new(b) as Box<dyn belt::Belt>)
}
pub(super) fn restore(bytes: &[u8]) -> Option<Box<dyn belt::Belt>> {
    Population::restore(bytes).map(|b| Box::new(b) as Box<dyn belt::Belt>)
}
impl belt::Belt for Population {
    fn len(&self) -> u64 {
        self.len()
    }
    fn body(&self, i: u64) -> belt::Body {
        let b = self.body(i);
        belt::Body {
            p: b.p,
            e: b.e,
            w: b.w,
            t: b.t,
        }
    }
    fn scar(&mut self, i: u64, b: belt::Body) {
        self.scar(
            i,
            Body {
                p: b.p,
                e: b.e,
                w: b.w,
                t: b.t,
            },
        );
    }
    fn store(&self) -> Vec<u8> {
        self.store()
    }
    fn bytes_used(&self) -> u64 {
        self.bytes_used()
    }
    fn form(&self) -> belt::Form {
        belt::Form::Program {
            info_bytes: Population::INFO_BYTES,
        }
    }
}

/// Build the actual frozen population recipe and count the chosen lossless representation.
/// No floor or gate threshold enters this measurement.
pub(super) fn bytes_per_body(scene: &memory::MemoryScene) -> Option<f64> {
    use emergent_shipmem::{
        codec::Enc,
        pop::{ladder, Pop, Rung},
        program::Program,
        shelf::{Kind, Shelf},
    };
    if scene.members == 0 || scene.populations == 0 || scene.members > 1 << 20 {
        return None;
    }
    let rung = match scene.rung {
        memory::Rung::Kicked(x) if (0.0..=1.0).contains(&x) => Rung::Rate(x),
        memory::Rung::Kicked(_) => return None,
        memory::Rung::Poisson => Rung::Poisson,
        memory::Rung::Random => Rung::Random,
    };
    let mut enc = Enc::new(true);
    let mut shelves = Vec::new();
    let mut programs = Vec::new();
    for g in 0..scene.populations {
        let (mut members, _, prog) = ladder(rung, scene.members, g as u64);
        programs.push(prog.map(|p| Program::with_prog(&members, 5, p, &mut enc).bytes()));
        if shelves.last().is_none_or(|s: &Shelf| s.n >= 1 << 20) {
            shelves.push(Shelf::new(5, 128, Pop::Convoy.orders(), true));
        }
        shelves
            .last_mut()?
            .add_group(&mut members, Kind::Slot { grid: 0 });
    }
    for s in &mut shelves {
        s.shrink();
    }
    let n = scene.members.checked_mul(scene.populations)? as f64;
    let packed = shelves.iter().map(Shelf::bytes).sum::<usize>() as f64 / n;
    Some(
        programs
            .iter()
            .map(|p| {
                p.map_or(packed * scene.members as f64, |bytes| {
                    (bytes as f64).min(packed * scene.members as f64)
                })
            })
            .sum::<f64>()
            / n,
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::behave::{space::Space, Law};
    #[test]
    fn space_reaches_the_production_belt_with_exact_history() {
        let law = Space::default();
        let mut b = law.belt_birth(&belt::SPEC, 8192, 42).unwrap();
        let pristine: Vec<_> = (0..b.len()).map(|i| b.body(i)).collect();
        for i in [7000, 1, 7000, 18] {
            b.scar(
                i,
                belt::Body {
                    p: u64::MAX,
                    e: 0,
                    w: 1,
                    t: 0,
                },
            );
        }
        let bytes = b.store();
        let round = law.belt_restore(&bytes).unwrap();
        assert_eq!(round.store(), bytes);
        for i in 0..b.len() {
            assert_eq!(round.body(i), b.body(i));
            if ![7000, 1, 18].contains(&i) {
                assert_eq!(b.body(i), pristine[i as usize]);
            }
        }
        assert!(matches!(b.form(), belt::Form::Program { info_bytes: 34 }));
        assert!(law
            .belt_birth(
                &belt::BeltSpec {
                    p_bits: 64,
                    ..belt::SPEC
                },
                10,
                0
            )
            .is_none());
    }
    #[test]
    fn extreme_seeds_keep_independent_columns_under_the_frozen_statistics() {
        let runs = [0, u64::MAX, 0u64.wrapping_sub(0x9E37_79B9_7F4A_7C15)].map(|seed| belt::Run {
            log2n: 20,
            seed,
            thorough: false,
        });
        let g = belt::judge(&Space::default(), &runs);
        assert!(g.pass, "{}", g.detail);
    }
    #[test]
    fn a_small_measurement_counts_both_supported_memory_forms() {
        for rung in [
            memory::Rung::Kicked(0.0),
            memory::Rung::Kicked(0.1),
            memory::Rung::Random,
        ] {
            let s = memory::MemoryScene {
                rung,
                members: 4096,
                populations: 1,
            };
            let bytes = bytes_per_body(&s).unwrap();
            assert!(bytes.is_finite() && bytes > 0.0);
        }
    }
}
