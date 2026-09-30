//! Independent GR oracle: Darwin's full radial-angle integral, composite Simpson.
//! Neither the behave sampler nor its oracle is imported.
use emergent_space::*;
fn gr(p: f64, e: f64) -> f64 {
    let n = 4096;
    let h = std::f64::consts::TAU / n as f64;
    let mut sum = 0.;
    for i in 0..=n {
        let f = (p / (p - 6. - 2. * e * (i as f64 * h).cos())).sqrt();
        sum += f * if i == 0 || i == n {
            1.
        } else if i % 2 == 0 {
            2.
        } else {
            4.
        };
    }
    sum * h / 3. - std::f64::consts::TAU
}
#[test]
fn circular_and_small_excursions_across_bands() {
    let mut worst = 0f64;
    let mut count = 0;
    for p in [
        7., 7.5, 8., 9., 10., 11., 12., 13., 15., 16., 17., 20., 24., 30., 31., 32., 33., 48., 64.,
        100., 128., 200., 256., 512., 1000.,
    ] {
        for e in [0., 1e-6, 1e-3, 0.01, 0.03] {
            let key = Key::darwin(
                (p * 65536f64).round() as u32,
                (e * 1073741824f64).round() as u32,
            )
            .unwrap();
            let c = compile(key).unwrap_or_else(|err| panic!("p={p} e={e}: {err:?}"));
            assert_eq!(c, compile(key).unwrap(), "bit-identical compilation");
            let advance = c.increments.phi.get() as f64 / 1073741824. - std::f64::consts::TAU;
            let expected = gr(p, e);
            let err = (advance / expected - 1.).abs();
            worst = worst.max(err);
            count += 1;
            assert!(
                err <= 0.01,
                "p={p} e={e} advance={advance} GR={expected} relative={err}"
            );
            assert_eq!(
                c.repeat(10000).unwrap().t.get(),
                10000 * c.increments.t.get()
            );
            for fraction in [0, 1, 2, 3, 4, 5, 6] {
                let period = c.increments.t.get();
                let offset = period * fraction / 7;
                let first = c.locate(Words::new(offset)).unwrap();
                let late = c.locate(Words::new(period * 10000 + offset)).unwrap();
                assert_eq!(late.cycle, 10000);
                assert_eq!(late.time_in_cycle, first.time_in_cycle);
                assert_eq!(late.crossing, first.crossing);
            }
        }
    }
    println!("near-circular {count}/{count}, worst relative advance error={worst}");
}
