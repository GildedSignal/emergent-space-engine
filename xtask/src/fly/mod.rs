//! Flat-space flight. Canonical integers live in `flight`; observation never feeds back.
mod flight;

pub(crate) fn run(_args: Vec<String>) -> crate::Result<u8> {
    Err("fly: flight built; localhost page is the next step".into())
}
