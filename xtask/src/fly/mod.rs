//! Flat-space flight. Canonical integers live in `flight`; observation never feeds back.
mod flight;
mod server;
mod view;

pub(crate) fn run(args: Vec<String>) -> crate::Result<u8> {
    server::run(args)
}
