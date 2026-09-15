//! I3 memory-kernel / low-rank Volterra compression of retarded GEM
//! collocation. Construction collocates a fixed memory window, then advances
//! later windows from that operator — it does not `interval_compile` over H.
//! Compact-after-the-fact of a finished collocation is not this object.
//! Not `production_law`. Not canonical gravity.

use crate::coupled_source_response::{
    field_acceleration, Body, Charge, ChargeRole, CompileOpts, InitialCondition, IntervalFunction,
    Intervention, ResponseError, Segment, COUPLED_RESPONSE_LAW_ID,
};
use crate::i3_secular::laboratory_circular_pair;
use serde::{Deserialize, Serialize};

/// Position match vs collocation. 1.25% of circular laboratory `a=4`.
/// Declared before this slice's kernel runs. Not the osculating 0.20 band,
/// and not a widened H0132 0.05 accel-fit (that peak was 0.078).
pub const KERNEL_POS_BAND: f64 = 0.05;
/// Remainder: discarded SVD energy of the bootstrap-window Jacobian, and
/// test-time max `|a_kernel − a_collocation|`. Declared before runs.
pub const KERNEL_A_BAND: f64 = 0.05;
/// Maximum admitted numerical rank of the window Jacobian. Full window
/// dimension on a two-light-crossing bootstrap is expected ≤ this.
pub const KERNEL_RANK_MAX: usize = 16;
/// Memory length: two light-crossings of the circular `a=4` pair (`r/c=0.5`).
/// Fixed. Must not grow with H.
pub const KERNEL_MEMORY: f64 = 1.0;
/// March cadence: one light-crossing. Coarser than collocation `τ/2≈0.25`.
pub const KERNEL_STEP: f64 = 0.5;
const KERNEL_SV_REL: f64 = 1e-3;
const KERNEL_CLOSE_R: f64 = 1.0;
const FD_EPS: f64 = 1e-6;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct MemoryKernelResponse {
    pub law_id: String,
    pub horizon: f64,
    pub genesis: InitialCondition,
    pub incoming: Vec<Intervention>,
    pub bootstrap_horizon: f64,
    pub boundary_rank: usize,
    pub jacobian_n: usize,
    pub memory_len: usize,
    pub fill_in: usize,
    pub discarded_energy: f64,
    pub min_r: f64,
    pub charge: Charge,
    pub wall_ns: u128,
    pub max_remainder: f64,
    functions: Vec<IntervalFunction>,
}

/// Nested Charge split for amortization. Reconstruction is charged on eval,
/// not construction.
#[derive(Clone, Copy, Debug)]
pub struct KernelChargeSplit {
    pub bootstrap: u64,
    pub jacobian: u64,
    pub advance: u64,
    pub certificate: u64,
    pub reconstruction: u64,
    pub patch: u64,
    pub fallback: u64,
    pub total: u64,
}

/// Kick-path match vs kicked collocation. Same 0.05 as the quiet kernel;
/// declared before this slice's kick runs. Not a widened quiet band.
pub const KERNEL_KICK_POS_BAND: f64 = 0.05;
pub const KERNEL_KICK_A_BAND: f64 = 0.05;
/// Short collocation patch after a strong kick, then kernel resume.
/// Same 0.05 as quiet/weak-kick; declared before this slice's patch runs.
pub const KERNEL_PATCH_POS_BAND: f64 = 0.05;
/// Collocation length after the kick: one memory window. Not full H.
pub const KERNEL_PATCH_LEN: f64 = 1.0;

impl MemoryKernelResponse {
    pub fn bytes(&self) -> usize {
        serde_json::to_vec(self).map(|b| b.len()).unwrap_or(0)
    }

    pub fn eval(&self, id: u64, t: f64, charge: &mut Charge) -> Result<[f64; 2], ResponseError> {
        charge.reconstruction = charge.reconstruction.saturating_add(1);
        let fun = self
            .functions
            .iter()
            .rev()
            .find(|f| f.body_id == id && t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15)
            .or_else(|| {
                self.functions
                    .iter()
                    .rev()
                    .find(|f| f.body_id == id && f.t0 <= t + 1e-15)
            })
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("memory-kernel has no function for body {id} at t={t}"),
            })?;
        let h = t - fun.t0;
        Ok([
            fun.x0[0] + fun.v0[0] * h + 0.5 * fun.a[0] * h * h,
            fun.x0[1] + fun.v0[1] * h + 0.5 * fun.a[1] * h * h,
        ])
    }

    pub fn stored_funs(&self) -> usize {
        self.functions.len()
    }

    pub fn accel(&self, id: u64, t: f64) -> Result<[f64; 2], ResponseError> {
        let fun = self
            .functions
            .iter()
            .rev()
            .find(|f| f.body_id == id && t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15)
            .ok_or(ResponseError::UnsupportedDomain {
                why: format!("memory-kernel has no accel for body {id} at t={t}"),
            })?;
        Ok(fun.a)
    }

    pub fn state(
        &self,
        id: u64,
        t: f64,
        charge: &mut Charge,
    ) -> Result<([f64; 2], [f64; 2]), ResponseError> {
        charge.reconstruction = charge.reconstruction.saturating_add(1);
        let fun = covering_function(&self.functions, id, t)?;
        let h = t - fun.t0;
        Ok((
            [
                fun.x0[0] + fun.v0[0] * h + 0.5 * fun.a[0] * h * h,
                fun.x0[1] + fun.v0[1] * h + 0.5 * fun.a[1] * h * h,
            ],
            [fun.v0[0] + fun.a[0] * h, fun.v0[1] + fun.a[1] * h],
        ))
    }

    pub fn split(&self) -> KernelChargeSplit {
        charge_split(&self.charge)
    }
}

pub fn compile_memory_kernel_response(
    ic: InitialCondition,
    incoming: Vec<Intervention>,
    horizon: f64,
) -> Result<MemoryKernelResponse, ResponseError> {
    let start = std::time::Instant::now();
    let mut charge = Charge {
        init: 1,
        ..Charge::default()
    };
    if ic.bodies.len() != 2 {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: "entrant / n-body; memory-kernel pair operator refuses; fallback to collocation"
                .into(),
        });
    }
    if horizon + 1e-15 < KERNEL_MEMORY {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!("horizon {horizon} is shorter than memory window {KERNEL_MEMORY}"),
        });
    }
    let r0 = hypot(
        ic.bodies[0].x[0] - ic.bodies[1].x[0],
        ic.bodies[0].x[1] - ic.bodies[1].x[1],
    );
    let v0 = hypot(ic.bodies[0].v[0], ic.bodies[0].v[1])
        + hypot(ic.bodies[1].v[0], ic.bodies[1].v[1]);
    if r0 < KERNEL_CLOSE_R || v0 < 1e-12 {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "close-encounter / radial rest pair (r={r0}, |v|={v0}); fallback to collocation"
            ),
        });
    }
    if !incoming.is_empty() {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: "resonance/forcing kicks; memory-kernel has no event table; fallback to collocation"
                .into(),
        });
    }

    let mut bootstrap_charge = Charge::default();
    let bootstrap = crate::coupled_source_response::compile_source_response_opts(
        ic.clone(),
        vec![],
        KERNEL_MEMORY,
        1.0 / 32.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )
    .map_err(|err| {
        bootstrap_charge.fallback += 1;
        err
    })?;
    bootstrap_charge = bootstrap.charge.clone();
    charge.push_child("bootstrap_window", ChargeRole::RuntimeRequest, bootstrap_charge);

    let boot_funs = bootstrap.interval_functions.clone();
    if boot_funs.len() < 2 {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: "bootstrap window stored no interval functions".into(),
        });
    }

    let mut k_charge = Charge::default();
    let (k_n, k_mat) = window_jacobian(&boot_funs, &mut k_charge)?;
    charge.push_child("window_jacobian", ChargeRole::RuntimeRequest, k_charge);
    if k_n == 0 || k_n > 2 * KERNEL_RANK_MAX {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!("window Jacobian n={k_n} is empty or exceeds 2×rank cap"),
        });
    }
    charge.factorization += 1;
    let (rank, discarded) = svd_rank(&k_mat, k_n, KERNEL_SV_REL);
    let fill_in = k_n * k_n;
    if rank > KERNEL_RANK_MAX {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!("boundary rank {rank} exceeds cap {KERNEL_RANK_MAX}; not a small boundary"),
        });
    }
    if discarded > KERNEL_A_BAND {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "window Jacobian discarded energy {discarded} exceeds band {KERNEL_A_BAND}; not low-rank"
            ),
        });
    }

    let mut functions = boot_funs;
    let mut advance_charge = Charge::default();
    let (memory_len, min_r) = march_kernel(
        &ic,
        &mut functions,
        KERNEL_MEMORY,
        horizon,
        r0,
        &mut advance_charge,
    )?;
    charge.push_child("kernel_advance", ChargeRole::RuntimeRequest, advance_charge);
    if memory_len > 4 * KERNEL_RANK_MAX {
        charge.fallback += 1;
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "memory length {memory_len} grew past 4×rank cap; compression moved work into the boundary"
            ),
        });
    }
    let mut cert = Charge::default();
    cert.verification += 1;
    charge.push_child("certificate", ChargeRole::Certificate, cert);
    Ok(MemoryKernelResponse {
        law_id: COUPLED_RESPONSE_LAW_ID.into(),
        horizon,
        genesis: ic,
        incoming,
        bootstrap_horizon: KERNEL_MEMORY,
        boundary_rank: rank,
        jacobian_n: k_n,
        memory_len,
        fill_in,
        discarded_energy: discarded,
        min_r,
        charge,
        wall_ns: start.elapsed().as_nanos(),
        max_remainder: discarded,
        functions,
    })
}

/// Kernel quiet prefix, apply kicks, resume kernel march. Remainder vs kicked
/// collocation is measured by the caller. Does not mint a keep from a refused
/// remainder; the caller falls back to recouple/collocation.
pub fn compile_kernel_with_kick(
    ic: InitialCondition,
    incoming: Vec<Intervention>,
    horizon: f64,
) -> Result<MemoryKernelResponse, ResponseError> {
    if incoming.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "kernel kick path needs a kick; empty extra is not a skip".into(),
        });
    }
    let t_kick = incoming
        .iter()
        .map(|iv| iv.t)
        .fold(f64::INFINITY, f64::min);
    if t_kick < KERNEL_MEMORY - 1e-12 {
        return Err(ResponseError::UnsupportedDomain {
            why: format!(
                "kick at {t_kick} is inside the bootstrap window; fallback to collocation"
            ),
        });
    }
    if t_kick > horizon + 1e-12 {
        return Err(ResponseError::UnsupportedDomain {
            why: "kick is after the horizon; not this path".into(),
        });
    }
    let mut prefix = compile_memory_kernel_response(ic.clone(), vec![], t_kick)?;
    let mut functions = prefix.functions;
    let mut kick_charge = Charge::default();
    for iv in &incoming {
        apply_kick(&mut functions, iv, &mut kick_charge)?;
    }
    prefix.charge.push_child("kick_apply", ChargeRole::RuntimeRequest, kick_charge);
    let mut advance_charge = Charge::default();
    let r0 = hypot(
        ic.bodies[0].x[0] - ic.bodies[1].x[0],
        ic.bodies[0].x[1] - ic.bodies[1].x[1],
    );
    let (memory_len, min_r) = march_kernel(
        &ic,
        &mut functions,
        t_kick,
        horizon,
        r0.min(prefix.min_r),
        &mut advance_charge,
    )?;
    prefix
        .charge
        .push_child("kernel_advance_suffix", ChargeRole::RuntimeRequest, advance_charge);
    prefix.horizon = horizon;
    prefix.incoming = incoming;
    prefix.memory_len = prefix.memory_len.max(memory_len);
    prefix.min_r = min_r;
    prefix.functions = functions;
    prefix.wall_ns = prefix.wall_ns; // prefix wall only; suffix is nested
    Ok(prefix)
}

/// Suffix collocation from the kernel state at the first kick. Explicit recouple
/// of the kicked tail; not a guessed kernel event.
pub fn recouple_kernel_suffix(
    prefix: &MemoryKernelResponse,
    incoming: &[Intervention],
    horizon: f64,
) -> Result<crate::coupled_source_response::SourceResponse, ResponseError> {
    let t_kick = incoming
        .iter()
        .map(|iv| iv.t)
        .fold(f64::INFINITY, f64::min);
    if !t_kick.is_finite() {
        return Err(ResponseError::UnsupportedDomain {
            why: "recouple suffix needs a kick time".into(),
        });
    }
    let mut recon = Charge::default();
    let mut kicked = ic_from_kernel(prefix, t_kick, &mut recon)?;
    for iv in incoming {
        if (iv.t - t_kick).abs() < 1e-12 {
            if let Some(b) = kicked.bodies.iter_mut().find(|b| b.id == iv.body_id) {
                b.v[0] += iv.delta_v[0];
                b.v[1] += iv.delta_v[1];
            }
        }
    }
    let mut compiled = crate::coupled_source_response::compile_source_response_opts(
        kicked,
        incoming
            .iter()
            .filter(|iv| iv.t > t_kick + 1e-12)
            .cloned()
            .collect(),
        horizon,
        1.0 / 32.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )?;
    compiled.charge.push_child("kernel_prefix_recon", ChargeRole::Reconstruction, recon);
    compiled
        .charge
        .push_child("kernel_prefix", ChargeRole::RuntimeRequest, prefix.charge.clone());
    Ok(compiled)
}

/// Collocate a short window after the kick, then resume the memory-kernel.
/// Not kernel-resume of the same strong Δv (H0135 rejected that). Close-entrant
/// n-body still refuses at the quiet prefix.
pub fn compile_kernel_kick_patch(
    ic: InitialCondition,
    incoming: Vec<Intervention>,
    horizon: f64,
) -> Result<MemoryKernelResponse, ResponseError> {
    if incoming.is_empty() {
        return Err(ResponseError::UnsupportedDomain {
            why: "kick patch needs a kick".into(),
        });
    }
    let t_kick = incoming
        .iter()
        .map(|iv| iv.t)
        .fold(f64::INFINITY, f64::min);
    if t_kick < KERNEL_MEMORY - 1e-12 {
        return Err(ResponseError::UnsupportedDomain {
            why: format!("kick at {t_kick} is inside the bootstrap window; fallback to collocation"),
        });
    }
    let mut prefix = compile_memory_kernel_response(ic.clone(), vec![], t_kick)?;
    let mut recon = Charge::default();
    let mut kicked = ic_from_kernel(&prefix, t_kick, &mut recon)?;
    for iv in &incoming {
        if (iv.t - t_kick).abs() < 1e-12 {
            if let Some(b) = kicked.bodies.iter_mut().find(|b| b.id == iv.body_id) {
                b.v[0] += iv.delta_v[0];
                b.v[1] += iv.delta_v[1];
            }
        }
    }
    let patch_end = (t_kick + KERNEL_PATCH_LEN).min(horizon);
    let later: Vec<Intervention> = incoming
        .iter()
        .filter(|iv| iv.t > t_kick + 1e-12 && iv.t < patch_end - 1e-12)
        .cloned()
        .collect();
    let patch = crate::coupled_source_response::compile_source_response_opts(
        kicked,
        later,
        patch_end,
        1.0 / 32.0,
        CompileOpts {
            store_pair_inverse: false,
        },
    )?;
    let mut functions = prefix.functions;
    functions.extend(patch.interval_functions.clone());
    prefix
        .charge
        .push_child("kernel_prefix_recon", ChargeRole::Reconstruction, recon);
    prefix
        .charge
        .push_child("kick_patch", ChargeRole::RuntimeRequest, patch.charge.clone());
    if patch_end < horizon - 1e-15 {
        let mut advance_charge = Charge::default();
        let r0 = hypot(
            ic.bodies[0].x[0] - ic.bodies[1].x[0],
            ic.bodies[0].x[1] - ic.bodies[1].x[1],
        );
        let (memory_len, min_r) = march_kernel(
            &ic,
            &mut functions,
            patch_end,
            horizon,
            r0.min(prefix.min_r),
            &mut advance_charge,
        )?;
        prefix
            .charge
            .push_child("kernel_advance_suffix", ChargeRole::RuntimeRequest, advance_charge);
        prefix.memory_len = prefix.memory_len.max(memory_len);
        prefix.min_r = min_r;
    }
    prefix.horizon = horizon;
    prefix.incoming = incoming;
    prefix.functions = functions;
    Ok(prefix)
}

pub fn laboratory_tight_pair() -> InitialCondition {
    let mut ic = laboratory_circular_pair();
    ic.bodies[0].x = [-1.5, 0.0];
    ic.bodies[1].x = [1.5, 0.0];
    let a = 3.0;
    let v = (crate::coupled_source_response::G * 2.0 / a).sqrt() / 2.0;
    ic.bodies[0].v = [0.0, -v];
    ic.bodies[1].v = [0.0, v];
    ic
}

fn charge_split(charge: &Charge) -> KernelChargeSplit {
    let child = |name: &str| {
        charge
            .child(name)
            .map(|c| c.charge.ledger_total())
            .unwrap_or(0)
    };
    KernelChargeSplit {
        bootstrap: child("bootstrap_window"),
        jacobian: child("window_jacobian"),
        advance: child("kernel_advance") + child("kernel_advance_suffix"),
        certificate: child("certificate"),
        reconstruction: child("kernel_prefix_recon") + charge.reconstruction,
        patch: child("kick_patch"),
        fallback: charge.fallback,
        total: charge.ledger_total(),
    }
}

fn covering_function(
    functions: &[IntervalFunction],
    id: u64,
    t: f64,
) -> Result<&IntervalFunction, ResponseError> {
    functions
        .iter()
        .rev()
        .find(|f| f.body_id == id && t + 1e-15 >= f.t0 && t <= f.t1 + 1e-15)
        .or_else(|| {
            functions
                .iter()
                .rev()
                .find(|f| f.body_id == id && f.t0 <= t + 1e-15)
        })
        .ok_or(ResponseError::UnsupportedDomain {
            why: format!("memory-kernel has no function for body {id} at t={t}"),
        })
}

fn function_state(fun: &IntervalFunction, t: f64) -> ([f64; 2], [f64; 2]) {
    let h = t - fun.t0;
    (
        [
            fun.x0[0] + fun.v0[0] * h + 0.5 * fun.a[0] * h * h,
            fun.x0[1] + fun.v0[1] * h + 0.5 * fun.a[1] * h * h,
        ],
        [fun.v0[0] + fun.a[0] * h, fun.v0[1] + fun.a[1] * h],
    )
}

fn march_kernel(
    ic: &InitialCondition,
    functions: &mut Vec<IntervalFunction>,
    t_from: f64,
    horizon: f64,
    mut min_r: f64,
    charge: &mut Charge,
) -> Result<(usize, f64), ResponseError> {
    let mut memory_len = functions.len();
    let mut t = t_from;
    while t < horizon - 1e-15 {
        let t_next = (t + KERNEL_STEP).min(horizon);
        let h = t_next - t;
        if h <= 1e-18 {
            break;
        }
        let lookback: Vec<IntervalFunction> = functions
            .iter()
            .filter(|f| f.t1 > t - KERNEL_MEMORY - 1e-12 && f.t0 < t + 1e-12)
            .cloned()
            .collect();
        memory_len = memory_len.max(lookback.len());
        if lookback.len() < 2 {
            charge.fallback += 1;
            return Err(ResponseError::UnsupportedDomain {
                why: format!("memory lookback empty at t={t}; fallback to collocation"),
            });
        }
        let sources = bodies_from_functions(&lookback);
        let mut created: Vec<IntervalFunction> = Vec::new();
        let mut step_x: Vec<[f64; 2]> = Vec::new();
        for body in ic.bodies.iter() {
            let last = covering_function(functions, body.id, t)?;
            let (x, v) = function_state(last, t);
            let t_col = t + 0.5 * h;
            let x_col = [x[0] + v[0] * (t_col - t), x[1] + v[1] * (t_col - t)];
            let a = field_acceleration(&sources, t_col, x_col, v, Some(body.id), charge)?;
            step_x.push(x);
            created.push(IntervalFunction {
                body_id: body.id,
                t0: t,
                t1: t_next,
                x0: x,
                v0: v,
                a,
                mu: body.mu,
            });
            charge.source_evolution += 1;
        }
        if step_x.len() == 2 {
            min_r = min_r.min(hypot(
                step_x[0][0] - step_x[1][0],
                step_x[0][1] - step_x[1][1],
            ));
            if min_r < KERNEL_CLOSE_R {
                charge.fallback += 1;
                return Err(ResponseError::UnsupportedDomain {
                    why: format!("close-encounter during march (r={min_r}); fallback to collocation"),
                });
            }
        }
        functions.extend(created);
        t = t_next;
    }
    Ok((memory_len, min_r))
}

fn apply_kick(
    functions: &mut Vec<IntervalFunction>,
    iv: &Intervention,
    charge: &mut Charge,
) -> Result<(), ResponseError> {
    charge.history += 1;
    let last = covering_function(functions, iv.body_id, iv.t)?.clone();
    let (x, mut v) = function_state(&last, iv.t);
    v[0] += iv.delta_v[0];
    v[1] += iv.delta_v[1];
    functions.push(IntervalFunction {
        body_id: iv.body_id,
        t0: iv.t,
        t1: iv.t,
        x0: x,
        v0: v,
        a: last.a,
        mu: last.mu,
    });
    Ok(())
}

fn ic_from_kernel(
    kernel: &MemoryKernelResponse,
    t: f64,
    charge: &mut Charge,
) -> Result<InitialCondition, ResponseError> {
    let mut bodies = Vec::new();
    for b in &kernel.genesis.bodies {
        let (x, v) = kernel.state(b.id, t, charge)?;
        bodies.push(crate::coupled_source_response::BodyInit {
            id: b.id,
            mu: b.mu,
            x,
            v,
        });
    }
    Ok(InitialCondition {
        genesis_t: t,
        bodies,
    })
}

fn hypot(x: f64, y: f64) -> f64 {
    (x * x + y * y).sqrt()
}

fn bodies_from_functions(funs: &[IntervalFunction]) -> Vec<Body> {
    let mut ids: Vec<u64> = Vec::new();
    for fun in funs {
        if !ids.contains(&fun.body_id) {
            ids.push(fun.body_id);
        }
    }
    ids.into_iter()
        .map(|id| {
            let mut segs: Vec<Segment> = funs
                .iter()
                .filter(|f| f.body_id == id)
                .map(|f| Segment {
                    t0: f.t0,
                    t1: Some(f.t1),
                    x0: f.x0,
                    v: f.v0,
                    a: f.a,
                    mu: f.mu,
                })
                .collect();
            segs.sort_by(|a, b| a.t0.partial_cmp(&b.t0).unwrap());
            Body {
                id,
                segments: segs,
            }
        })
        .collect()
}

fn window_jacobian(
    funs: &[IntervalFunction],
    charge: &mut Charge,
) -> Result<(usize, Vec<f64>), ResponseError> {
    let nfun = funs.len();
    let n = 2 * nfun;
    let mut k_mat = vec![0.0; n * n];
    let sources0 = bodies_from_functions(funs);
    for j in 0..nfun {
        for comp in 0..2 {
            let mut pert = funs.to_vec();
            pert[j].a[comp] += FD_EPS;
            let sources = bodies_from_functions(&pert);
            charge.coefficient_construction += 1;
            for i in 0..nfun {
                if funs[i].body_id == funs[j].body_id {
                    continue;
                }
                let h = funs[i].t1 - funs[i].t0;
                if h <= 1e-18 {
                    continue;
                }
                let t_col = funs[i].t0 + 0.5 * h;
                let x_col = [
                    funs[i].x0[0] + funs[i].v0[0] * 0.5 * h,
                    funs[i].x0[1] + funs[i].v0[1] * 0.5 * h,
                ];
                let a = field_acceleration(
                    &sources,
                    t_col,
                    x_col,
                    funs[i].v0,
                    Some(funs[i].body_id),
                    charge,
                )?;
                let a0 = field_acceleration(
                    &sources0,
                    t_col,
                    x_col,
                    funs[i].v0,
                    Some(funs[i].body_id),
                    charge,
                )?;
                k_mat[2 * i * n + (2 * j + comp)] = (a[0] - a0[0]) / FD_EPS;
                k_mat[(2 * i + 1) * n + (2 * j + comp)] = (a[1] - a0[1]) / FD_EPS;
            }
        }
    }
    Ok((n, k_mat))
}

fn svd_rank(k: &[f64], n: usize, rel: f64) -> (usize, f64) {
    let mut gram = vec![0.0; n * n];
    for i in 0..n {
        for j in 0..n {
            let mut s = 0.0;
            for p in 0..n {
                s += k[p * n + i] * k[p * n + j];
            }
            gram[i * n + j] = s;
        }
    }
    let evals = jacobi_eigenvalues(&mut gram, n);
    let mut sigmas: Vec<f64> = evals.into_iter().map(|λ| λ.max(0.0).sqrt()).collect();
    sigmas.sort_by(|a, b| b.partial_cmp(a).unwrap());
    let smax = sigmas.first().copied().unwrap_or(0.0);
    let thresh = smax * rel;
    let rank = sigmas.iter().filter(|s| **s > thresh).count();
    let total: f64 = sigmas.iter().map(|s| s * s).sum();
    let kept: f64 = sigmas.iter().take(rank).map(|s| s * s).sum();
    let discarded = if total > 1e-18 {
        (1.0 - kept / total).max(0.0)
    } else {
        0.0
    };
    (rank.max(1), discarded)
}

fn jacobi_eigenvalues(a: &mut [f64], n: usize) -> Vec<f64> {
    for _ in 0..32 {
        let mut max_off = 0.0_f64;
        let mut p = 0;
        let mut q = 1;
        for i in 0..n {
            for j in (i + 1)..n {
                let mag = a[i * n + j].abs();
                if mag > max_off {
                    max_off = mag;
                    p = i;
                    q = j;
                }
            }
        }
        if max_off < 1e-14 {
            break;
        }
        let app = a[p * n + p];
        let aqq = a[q * n + q];
        let apq = a[p * n + q];
        let tau = (aqq - app) / (2.0 * apq);
        let sign = if tau >= 0.0 { 1.0 } else { -1.0 };
        let t = if tau.abs() > 1e18 {
            1.0 / (2.0 * tau)
        } else {
            sign / (tau.abs() + (1.0 + tau * tau).sqrt())
        };
        let c = 1.0 / (1.0 + t * t).sqrt();
        let s = t * c;
        for k in 0..n {
            if k == p || k == q {
                continue;
            }
            let aik = a[k * n + p];
            let aiq = a[k * n + q];
            a[k * n + p] = c * aik - s * aiq;
            a[p * n + k] = a[k * n + p];
            a[k * n + q] = s * aik + c * aiq;
            a[q * n + k] = a[k * n + q];
        }
        a[p * n + p] = c * c * app - 2.0 * s * c * apq + s * s * aqq;
        a[q * n + q] = s * s * app + 2.0 * s * c * apq + c * c * aqq;
        a[p * n + q] = 0.0;
        a[q * n + p] = 0.0;
    }
    (0..n).map(|i| a[i * n + i]).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn kernel_gates_are_declared() {
        assert_eq!(KERNEL_POS_BAND, 0.05);
        assert_eq!(KERNEL_A_BAND, 0.05);
        assert_eq!(KERNEL_KICK_POS_BAND, 0.05);
        assert_eq!(KERNEL_KICK_A_BAND, 0.05);
        assert_eq!(KERNEL_PATCH_POS_BAND, 0.05);
        assert_eq!(KERNEL_PATCH_LEN, 1.0);
        assert_eq!(KERNEL_RANK_MAX, 16);
        assert_eq!(KERNEL_MEMORY, 1.0);
        assert_eq!(KERNEL_STEP, 0.5);
    }
}
