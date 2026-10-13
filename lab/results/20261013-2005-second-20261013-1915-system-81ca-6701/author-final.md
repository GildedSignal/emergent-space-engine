Working...
That was a stale duplicate of the same final run — numbers identical to those already recorded in `probe-out.txt`, the dossier, and the wiki page. All artifacts are final:

- `lab/results/20261013-2005-second-20261013-1915-system-81ca-6701/`: `predictions.md` (pre-registered), `dossier.md`, `regen.sh` (probe + mpmath cross-check, both validated end-to-end), `wiki/closed-form-kernel.md`, `probe-out.txt`.
- The probe itself (`crates/space/tests/carlson_compile_probe.rs`, 846 lines) is left in the tree for the runner's patch capture; the shipped crates, gates, and `main` untouched.

**Claim, one sentence**: All three channels of the shipped kick compile are one certified-exact integer Carlson basis — advance, period and proper period verified together to the walk's own channel quanta on 182 strong keys including every attack key (worst 5.3e-10/3.7e-10/3.8e-10, integer = f64 = mpmath = quadrature), priced 18–40 µs flat against the walk's 5.8–374 µs (9.4× cheaper at the leaver tail, 2–3.4× dearer at the two cheapest keys, 0.5–12 kB/shape deleted) — but the readout's crossing table survives its challenger: correct incomplete Carlson reads cost 3–7× the panel table's 4 µs per query, so the walk deletion is a compile-side law change, not a whole-walk deletion.
