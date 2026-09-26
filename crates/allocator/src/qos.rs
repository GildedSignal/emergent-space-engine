//! Core classes. macOS offers no core pinning; quality of service is the supported way to
//! steer a thread to the performance (user-interactive) or efficiency (utility) cluster.
use serde::Serialize;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize)]
pub enum Class {
    Performance,
    Efficiency,
}

/// Returns whether the OS accepted the request.
pub fn set_current(class: Class) -> bool {
    #[cfg(target_os = "macos")]
    {
        let qos = match class {
            Class::Performance => libc::qos_class_t::QOS_CLASS_USER_INTERACTIVE,
            Class::Efficiency => libc::qos_class_t::QOS_CLASS_UTILITY,
        };
        // SAFETY: plain syscall on the calling thread with a valid class and priority 0.
        unsafe { libc::pthread_set_qos_class_self_np(qos, 0) == 0 }
    }
    #[cfg(not(target_os = "macos"))]
    {
        let _ = class;
        false
    }
}
