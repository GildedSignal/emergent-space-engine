# Emergent Space: how we work

**First read [docs/PRINCIPLES.md](docs/PRINCIPLES.md)** (the goal and Julien's philosophy, always on), then `docs/HANDOFF.md` (state, plan, in flight), then `cargo xtask history list`. The only live checkout is `~/Research/emergent-space`, branch `main`; the private remote is `GildedSignal/emergent-space-engine`. Codex, GLM/OMP and Cursor load the heading-check skill (card `docs/CARD.md`). Do not pass `--no-skills`.

## Truth

- **Laws are versioned.** Canonical outcomes are exact and independent of cache, partition, observation, schedule and hardware. Floats never decide them.
- **Certificates need independent, adversarial checks.** A laboratory result never counts as integrated qualification.
- **Gates are frozen before the first run and never weakened after.** Failures stay machine-readable. Gates judge a representation; they never size it: first derive the representation native to the operations at stake (Julien: "we know we have a fish, we need to find its water").
- **Evidence.**
  - Measure before claiming, and never strawman.
  - Build the simplest falsifying test first ("even baby spartans started small"), then climb a ladder of rungs, each roughly 10× harder: extremes and chaotic scenes, until one fails ([test-ladder](docs/test-ladder.md)). A test that cannot fail is a control.
  - A failed expectation is not automatically a failed method: diagnose which one broke (H0183).
- **Tests.** Each finishes within 60 s. Measure the way the player will run it: heat and load are part of reality, not noise to sidestep. Record the state (thermal, power, swap, load) so runs compare honestly. At this stage, think in orders of magnitude; don't polish what may be replaced.

## Team

- **Skunk Works, physics first** (Julien, 30 September: the SR-71's way). Speed to the finished product is the measure, and overhead costs the integrator's attention. The integrator reads code and gate output, not reports; reports are minimal; each builder tests its own product; the product flies early (Julien plays the slice as soon as it exists). At least 60% of each Claude and Astra window goes to the plan's steps, and no process change lands without a physics merge since the last one.
- **Comparative advantage, and spend every provider's usage.** Check it with `get_usage` for Claude, the rollout `rate_limits` for Codex, and `omp usage` for GLM.
  - **Claude Opus**, the integrator: taste and divergent thinking, judgement, contracts, adjudication, merges, the journal. It never builds as a sub-agent.
  - **gpt-6.1-sol:** most of the building (close to Astra, about 5× cheaper).
  - **gpt-6-astra:** reserved for the hard, convergent, math-like work: exact algorithms, proofs. It consumes tokens fastest, and every Astra token is one Sol cannot spend (opportunity cost; the same holds for Opus against Sonnet), so reviews and audits go to Sol or Sonnet.
  - **Claude Sonnet**, as sub-agents: the Claude-side builder, including every judge of OpenAI's modules.
  - **GLM 5.3,** the [lab](lab/README.md): autonomy of inquiry and no authority. Many GLMs with lenses choose their own experiments, run as cloud routines only (never on Julien's machine), and are each checked by an independent GLM. Only gold reaches the integrator. Pre-freeze red-teams and probes run there too.
  - **Read-only thinking agents,** before one-way doors only. Their briefs stay outside the repo.
- **A players protect the work.**
  - The tiers, highest first: Opus ≈ Astra, then Sonnet, then Sol, then GLM. Whoever builds a module, contract or gate owns it.
  - Lower tiers report findings that name the invariant at stake, and never edit higher-tier work. Their doc patches may add or delete lines but never reword existing ones.
  - Julien owns his principles: models propose changes and never reword them.
  - A judge is built by a strong model from a different family than what it judges. Disagreements are adjudicated, never auto-fixed.
- **Before any freeze,** one GLM red-team and the cheapest falsifying probe must have run. The red-team attacks the premise against PRINCIPLES.md before it attacks the letter.
- **Guards against drift and sunk cost.**
  - Every specialist prompt begins with PRINCIPLES.md's goal and philosophy, verbatim.
  - No time estimates: progress is a rough % and principles. A step whose builder passes no new gate across two consecutive work windows stops and is re-derived from the goal instead of extended.
  - Every statement of Julien's enters the register in PRINCIPLES.md, and stays until it is followed or disproven with evidence.
- **Specialists** work in `/private/tmp/emergent-wt-<task>` on `wt/<task>`, and job files live in `artifacts/runs/<id>/`. The integrator merges, then deletes the branch and worktree. Heavy work that needs neither Metal nor timing may run in a cloud session.

## Workspace

- **Start clean, build messy-ish, finish clean.** Archive before a phase and simplify after it works. Before retiring anything, list what it did well and where that goes. Retired code lives in `~/Research/emergent-space-archive`: never build or edit it there. Bring something back deliberately, with a journal entry.
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

Originals of Julien's context: `docs/reference/` and `assets/reference/`. PRINCIPLES.md governs; later steering refines it through its register.
The aesthetic, in Julien's words: "use real materials, don't make it overly saturated and contrasted use more the color style of sinbad"; "it's moody"; observed versus implied gets a "different patina"; "not steampunk is NOT the goal".
