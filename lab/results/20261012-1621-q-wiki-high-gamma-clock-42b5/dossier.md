# Dossier — 20261012-1621-q-wiki-high-gamma-clock-42b5 (lens: compile `high-gamma-clock`)

## Claim (one sentence)

The `high-gamma-clock` page is compiled: of the 8 clustered runs, 4 are on-topic — one gold
(e128: the tube's clock saturates at dt/dτ = 2 from γ ≈ 2, the wall at γ 1761–1803 is the
rebind's k-word `Space(Range)`, the 3% work gate dies above β 0.247) plus scout-a1a4 (the same
tube carries plunge/γ-2000 orbits exactly) and the redteam-efb2 pair (the doll-frame solver
survives γ 2×10⁶) — the other 4 reassign to kick-cadence (2), frame-cost and encounters, and no
other run among all 642 lab branches measures the ship's proper-time clock at high γ.

## Bottleneck

The board's first live question, and the wiki's purpose (Julien, 12 October: runs stop
rediscovering what earlier runs found). Gain: the integrator acts on the clock topic from the
page alone — the gold's numbers, causes, domain and the unmeasured regimes — without opening
dossiers; and four mis-clustered runs reach their own topics' compilers instead of dying here.

## Evidence (regenerable; ~5 s + ~3 s)

- `extract.sh` (this folder) re-extracts **46 fixed strings** — every number quoted on the page —
  from the four on-topic runs' own records on their immutable `claude/lab-<id>` branches:
  46 OK, 0 MISS. It also re-runs the triage that decided nothing was missed: a scan of all
  642 `origin/claude/lab-*` branches over two keyword classes (`gamma|dτ|dtau|proper
  time|time dilation|lorentz|clock`, and `inversion-e128|γ 1,761|dt/dτ|proper-time
  saturat|gate C1|Q48`) → 25 branches with hits, each abstract read and reassigned; none
  measures the ship's clock at high γ.
- Grades verified at source: e128 `Grade: gold` in **both** check.md and check2.md; scout-a1a4,
  redteam-efb2 and its second are `silver` — matching the assignment list. Two **off-topic**
  runs self-report grades that disagree with the list (see below); they do not touch this page.
- Commands: `bash lab/results/20261012-1621-q-wiki-high-gamma-clock-42b5/extract.sh` (~5 s),
  then `bash lab/results/20261012-1621-q-wiki-high-gamma-clock-42b5/regen.sh` (~3 s; diffs the
  check section against `work/extract-expected.txt`).

## Predictions

Written before the page ([predictions.md](predictions.md)). **All five held**: P1 — the 4/4
topic split exactly as predicted; P2 — no missed on-topic run (642 branches scanned); P3 — e128's
two checkers both gold and agreeing on the three headline facts; P4 — every page claim cites one
of the four runs, and the `wt/clock` build appears only as labelled HANDOFF context; P5 — exactly
the two off-topic grade conflicts predicted (q-fermi2-tide-v2-26a7, second-…-inversion-6534-cceb).

## What would make it wrong, cost of adoption, fit

- **Wrong if** a page claim is not supported by its cited record (the checker samples five), or
  if a run exists that never writes dt/dτ, γ, C1 or Q48 yet measures the clock — the triage's
  blind spot. The before-picture numbers (wall γ 1761/1791/1803, deficit curve) go stale the
  moment `wt/clock` merges; the page labels them as the before-picture.
- **Cost of adopting:** publish via `lab/wiki.py apply` (three-way against the seed page; the
  header, `status: open` and the title are the seed's, `updated:` is this run).
- **Fit:** PRINCIPLES 11 ("Text has a cost; one home per kind of text") — the wiki is the one
  home for "what is known per topic"; Julien, 12 October: "maybe we need a karphaty style wiki
  where the current best and directions are clear".

## The lens

A compiler reads checkers' abstracts and trusts their reproductions; it re-derives nothing. What
that may have missed: e128's numbers are the two checkers' (both byte-identical reproductions,
re-measured on the M1 per docs/HANDOFF.md), not re-run here; the 25 triage hits were classified
from abstracts — two of them (fermi-ece4, b-news-gravity-e300) from partial reads, though both
are unambiguously gravity/belt work on any reading; and a compiler lens tends to over-trust the
newest gold — mitigated here by carrying check2's corrections (mechanism, L5 control) onto the
page as refuted lines rather than the author's phrasing.

## Runs that belong elsewhere (for those topics' compilers)

- **kick-cadence**
  - `20261006-0220-q-fermi2-tide-v2-26a7` (listed silver; its check.md self-reports **gold** —
    the topic's compiler should resolve this before using it): the Fermi phase-2 tide reference
    regenerates end to end; the closed kernel −w(3γ²−1), +w; B.frame falls 14.7× per
    n-doubling. *Grade conflict flagged; not used on this page.*
  - `20261008-1613-library-524e` (silver): the tide-kick cadence trigger must fire on an impulse
    quantum (∫g dt), not force change or a clock; 3.4× fewer kicks on the belt, 6.5–16× on
    inclined held-out cases.
- **frame-cost**: `20261008-0234-autoresearch-dd3e` (silver): caching the proper time at the
  binding event (`tau_event`, `readout_with`) cuts the pure kick 36.2→28.9 µs (−20%),
  bit-identical on all configs. (Adjacent: 20261012-1019-autoresearch-c549, −21.7%, and
  20261012-1340-autoresearch-887d — same family, found in my triage, not in the cluster.)
- **encounters**: `20261008-1150-second-20261008-1058-inversion-6534-cceb` (listed silver; its
  check.md self-reports **gold**): the second blind check confirming the crossing-time-rank
  certificate (zero-miss, 3.8 pairs/encounter flat in m, ~9× wall). The run to list is its
  parent, `20261008-1058-inversion-6534`. *Grade conflict flagged.*
- **view**: the redteam-efb2 pair's main findings are view-topic (one-sample-per-pixel aliasing
  from ≈0.02–0.03 orbits/frame; the PASS is convention-carried under photon-count/energy
  readings; the 75–98% "frozen" aggregates are contaminated by the observer's flyby). This page
  cross-lists them with (→ view) markers and keeps only their solver line.
- **note**: scout-a1a4's plunge/capture half could also serve a future tube-law topic; it stays
  here because the board frames the γ ≈ 2,000 refusal under `high-gamma-clock`.
