//! Frozen regression of the original band-centred map; the new small-excursion
//! generator is judged independently in near_circular.rs. No global certificate.
#[path = "fixtures/reference.rs"]
mod reference;
use emergent_space::*;
#[test]
fn independent_binet_m16_fixtures() {
    // Declared before running the comparison. Per-case failures remain visible.
    let mut worst = [0.0f64; 4];
    let mut failed = Vec::new();
    for (i, &(p, e, phi, t, tau, up, ua, nc)) in reference::REFERENCE.iter().enumerate() {
        let key = Key::darwin(
            (p * 65536.0).round() as u32,
            (e * 1073741824.0).round() as u32,
        )
        .unwrap();
        let c = match compile_variant(key, false) {
            Ok(c) => c,
            Err(err) => {
                failed.push(format!("{i}: {err:?}"));
                continue;
            }
        };
        let errs = [
            (c.increments.phi.get() as f64 / 1073741824.0 - phi).abs(),
            (c.increments.t.get() as f64 / 1048576.0 / t - 1.0).abs(),
            (c.increments.tau.get() as f64 / 1048576.0 / tau - 1.0).abs(),
            (c.start.u_q48() as f64 / 281474976710656.0 / up - 1.0)
                .abs()
                .max((c.apo.u_q48() as f64 / 281474976710656.0 / ua - 1.0).abs()),
        ];
        for j in 0..4 {
            worst[j] = worst[j].max(errs[j]);
        }
        if errs[0] > 2e-4
            || errs[1] > 5e-4
            || errs[2] > 5e-4
            || errs[3] > 2e-4
            || c.crossings.len() != nc
            || !c
                .crossings
                .iter()
                .map(|c| c.band)
                .eq(reference::SEQUENCES[i].iter().copied())
        {
            failed.push(format!(
                "{i}: p={p} e={e} errors={errs:?} crossings={}/{nc}",
                c.crossings.len()
            ));
        }
    }
    println!(
        "reference cases={} worst [angle_abs, time_rel, proper_rel, shape_rel]={worst:?}",
        reference::REFERENCE.len()
    );
    assert!(
        failed.is_empty(),
        "{} of {} fail:\n{}",
        failed.len(),
        reference::REFERENCE.len(),
        failed.join("\n")
    );
}
