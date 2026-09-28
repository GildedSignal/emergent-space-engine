# Emergent Space: how we work

Start: `docs/HANDOFF.md` (state and plan), then `cargo xtask history list` and search what's relevant. The only live checkout is `~/Research/emergent-space`, branch `main`; the private remote is `GildedSignal/emergent-space-engine`. Codex, GLM/OMP and Cursor load the heading-check skill (`~/.cursor/skills/heading-check/SKILL.md`, card `cards/emergent-space.md`). Do not pass `--no-skills`.

## Truth

- **Laws are versioned.** Canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware. Floats never decide them.
- **Certificates need independent, adversarial checks.** A laboratory result never counts as integrated qualification.
- **Gates are frozen before the first run and never weakened after.** Failures stay machine-readable.
- **Evidence.**
  - Measure before claiming, and never strawman.
  - Build the simplest falsifying test first ("even baby spartans started small"), then climb a ladder of rungs, each roughly 10× harder: extremes and chaotic scenes, until one fails ([test-ladder](docs/test-ladder.md)). A test that cannot fail is a control.
  - A failed expectation is not automatically a failed method: diagnose which one broke (H0183).
- **Tests.** Each finishes within 60 s. Measure the way the player will run it: heat and load are part of reality, not noise to sidestep. Record the state (thermal, power, swap, load) so runs compare honestly. At this stage, think in orders of magnitude; don't polish what may be replaced.

## Team

- **Physics first.** At least 60% of each Claude and Astra window goes to the plan's steps. There is one process change per week, and none in a week with no physics merge.
- **Comparative advantage, and spend every provider's usage.** Check it with `get_usage` for Claude, the rollout `rate_limits` for Codex, and `omp usage` for GLM.
  - **Claude Opus**, the integrator: judgement, contracts, adjudication, merges, the journal, the hard problems.
  - **gpt-6-astra:** the hardest exact specifics: algorithms, proofs, audits.
  - **Claude Sonnet**, as sub-agents: the default builder for well-scoped builds, harnesses, fixes and fast iteration.
  - **gpt-6-sol:** the overflow builder.
  - **GLM 5.3** (`omp`, in a sandboxed clone): volume without authority. It runs red-teams, probes, sweeps and mutants. Its loops are pull-based: one launches only when at most one finding is waiting.
  - **Read-only thinking agents,** before one-way doors only. Their briefs stay outside the repo.
- **A players protect the work.**
  - The tiers, highest first: Opus ≈ Astra, then Sonnet, then Sol, then GLM. Whoever builds a module, contract or gate owns it.
  - Lower tiers report findings that name the invariant at stake, and never edit higher-tier work. Their doc patches may add or delete lines but never reword existing ones.
  - Julien owns his principles: models propose changes and never reword them.
  - A judge is built by a strong model from a different family than what it judges. Disagreements are adjudicated, never auto-fixed.
- **Before any freeze,** one GLM red-team and the cheapest falsifying probe must have run.
- **Specialists** work in `/private/tmp/emergent-wt-<task>` on `wt/<task>`, and job files live in `artifacts/runs/<id>/`. The integrator merges, then deletes the branch and worktree. Heavy work that needs neither Metal nor timing may run in a cloud session.

## Workspace

- **Start clean, build messy-ish, finish clean.** Archive before a phase and simplify after it works. Retired code lives in `~/Research/emergent-space-archive`: never build or edit it there. Bring something back deliberately, with a journal entry.
- **No stray clones, branches or folders.** Never put a repo in an iCloud-synced folder.

## Text has a cost

Every line is read many times by humans and agents. Text grows unless something forces it down.
- **One home per kind of text:**
  - *Truth now* lives in `docs/HANDOFF.md` (≤ 120 lines) and the specs in `docs/*.md` (≤ 200 lines each). They are rewritten in place and hold no change logs.
  - *History* lives in git and in `docs/HISTORY.md`: one entry per milestone, ≤ 1,500 characters, details in `artifacts/evidence/`. Committed entries are never rewritten; corrections are appended.
  - *How we work* lives in this file, ≤ 60 lines. A new rule must replace or merge an old one.
- **Survive compaction.** Context windows get summarized, so anything that isn't written durably is lost. The integrator keeps HANDOFF's "In flight" table current whenever a job starts or ends: owner, worktree, output path, next action. Intent lives in the handoff and this file, never only in a conversation.
- **Pointers, not copies.** The README, the heading card and agent memory point to the handoff; they never duplicate its state.
- **Write for the corporal.** One reading, no possible misreading: an order that can be misunderstood will be.
- **Delete when built.** A design note is folded into the spec or the code docs once its design exists in code.
- **`cargo xtask history check` enforces these budgets.** The integrator alone appends the journal; specialists return drafts. Commit each entry with its work. Frozen evidence is immutable.

Originals of Julien's context: `docs/reference/` and `assets/reference/`. Read them selectively; later steering governs. The aesthetic is ink, watercolor, ivory, pale blue and astronomical instruments.
