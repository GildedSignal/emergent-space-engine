Working...
Check complete. **Grade: gold** — `check.md` written, the author's proposed wiki page carries my correction bracket, tree restored to clean (patch reversed, scratch example removed), nothing else in the run folder touched.

**What I did:**

- **Reproduced every arm** from `work/patch.diff` on a clean tree: plane compile 89.4% (digests identical on/off), belt coast 44.6/44.9% (regen), plus my own burn arm (49.1%) and N=10⁵ (42.5%) — N-flat one decade past the author.
- **Five adversarial cases, all outside the tested range:** grid radii 5/12/23/40 (crossing stays in e∈[0.1,0.3]), e 0.95 (monotone continues, 58–94 µs; e 0.99 refuses at all seven radii), the held-out burn arm, N=10⁵, and a765's exact rtf-100 populations — call counts 1,467/1,737/1,349 regenerate bit-exactly with compile 81.9–84.8%.
- **Upgraded the boundary half from [INFERENCE] to verified:** 7fd3's published patch starts `REBIND_NS` at the universe `rebind()` wrapping `bind_in`, which adds decode/turn/tube/entry beyond `from_state`; their 10⁴ mint count (203,485) matches this audit's calls (203,880) within cadence, and compile absolutes agree.
- **Found two letter-level defects, neither material:** P4's control compares instrumented-on vs instrumented-off (both carry the four `Instant::now()` reads; bounded ~0.1 µs, immaterial), and P5's "kicks identical" was unpassable — the field is load-elastic (my two off/off flights differ 3.6%), so the author's 0.4% on/off delta is noise, with the digest identity being the real (and passing) control.
- **Novelty:** the published page's own contradiction entry named this adjudication as the experiment to gold; HISTORY holds no prior one.

The premise "the rebind has one owner" is dead on evidence: the share is a property of e plus the census boundary, and 7fd3's "the fit is the 74%" consequence is refuted at both regimes (fit 3–9% plane, readouts > fit at belt e). Adoption is a zero-wiring re-ranking: plane → Carlson compile, belt → readouts first.
