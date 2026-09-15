//! Diagnostic coupled-compiler adapter.
//!
//! Polls collocation jobs with [`WorkBudget`]. Does not replace inertial
//! [`crate::runtime::Engine::advance`]. Does not report canonical gravity
//! acceptance. Seal, pair-inverse and enclosure remain later I1 work.

use crate::runtime::WorkBudget;
use emergent_law_lab::coupled_source_response::{CoupledCompileJob, JobPoll, ResponseError};

/// Explicit non-acceptance. Increment 1 of I1 is diagnostic only.
pub const CANONICAL_GRAVITY_ACCEPTANCE: &str = "diagnostic-only";

pub fn poll_coupled_job(
    job: &mut CoupledCompileJob,
    budget: &mut WorkBudget,
) -> Result<JobPoll, ResponseError> {
    let mut ops = budget.operations as u64;
    let status = job.poll(&mut ops)?;
    budget.operations = ops as usize;
    Ok(status)
}

#[cfg(test)]
mod tests {
    use super::*;
    use emergent_law_lab::coupled_source_response::laboratory_two_body;

    #[test]
    fn adapter_does_not_report_canonical_gravity() {
        assert_eq!(CANONICAL_GRAVITY_ACCEPTANCE, "diagnostic-only");
        let ic = laboratory_two_body();
        let mut job = CoupledCompileJob::from_genesis(&ic, &[], 3.0).unwrap();
        let mut budget = WorkBudget::new(1);
        let mut pending = 0;
        loop {
            match poll_coupled_job(&mut job, &mut budget).unwrap() {
                JobPoll::Pending => {
                    pending += 1;
                    budget = WorkBudget::new(1);
                }
                JobPoll::Ready => break,
            }
            assert!(pending < 10_000);
        }
        assert!(pending > 0);
        assert!(job.is_ready());
    }
}
