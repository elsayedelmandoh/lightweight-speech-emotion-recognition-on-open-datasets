---
name: docs-maker
description: >
  Scaffold a complete docs/ folder structure for the current project, creating
  markdown files with smart templates. Use whenever a user wants to set up project
  documentation, create doc files, scaffold a docs folder, or generate markdown
  templates for a new or existing project. Trigger on phrases like "create my
  docs", "set up documentation", "scaffold docs", "make the docs folder",
  "generate project docs", "initialize docs structure", "create documentation
  files", or "set up my docs". Also trigger if the user says "make docs for my
  project" or anything implying they want a structured docs/ directory created.
---

# docs-maker

scaffold the complete `docs/` folder for the current project using the bundled script. creates missing files only — never overwrites existing ones.

## what to do

1. **identify the project root** — use the current working directory, or wherever the user's project lives. if the user didn't specify and it's ambiguous, ask once.

2. **run the bundled script:**
   ```bash
   python {SKILL_DIR}/scripts/create_docs.py {PROJECT_ROOT}
   ```
   replace `{SKILL_DIR}` with the directory containing this SKILL.md file, and `{PROJECT_ROOT}` with the identified project root path.

3. **report results** clearly to the user:
   - list all files created (with `+` prefix)
   - list all files skipped because they already existed (with `~` prefix)
   - show a summary count

4. **preserve internal tooling** — do not create, modify, or overwrite any
   files inside `docs/.internal/skills` (or any `*.internal/skills` path). if a
   `skills` subfolder exists, skip it and report it as skipped.

## docs structure created

files within each folder are ordered by what a senior ai engineer needs first.

```
docs/

```

note: the `docs/.internal/skills` directory is a repository-managed area and
must never be altered by the scaffolder; treat it as read-only and skip it.

```
docs/
├── .internal/
│   ├── 00-quickstart.md           # internal quickstart and housekeeping
│   └── speckit/                   # internal tooling and speckit artifacts
│       ├── 00-quickstart.md
│       ├── 01-speckit-workflow.md
│       └── 02-plan.md
│   └── speckit/                   # internal tooling and speckit artifacts
│       └── 00-quickstart.md
|
├── research/
│   ├── 00-quickstart.md           # 10-min overview of the research
│   ├── 01-related-work.md         # similar projects & comparisons (landscape first)
│   ├── 02-references.md           # academic references & papers
│   └── 03-research-notes.md       # exploration & learnings
│
├── project-definition/
│   ├── 00-quickstart.md           # 10-min project overview
│   ├── 01-problem.md              # problem statement & context
│   ├── 02-goal.md                 # project goals & objectives
│   ├── 03-solution.md             # proposed solution approach
│   ├── 04-dataset.md              # data sources & specifications
│   ├── 05-constraints.md          # should do / should not do
│   ├── 06-stack.md                # technology stack & dependencies
│   ├── 07-architecture.md         # system design & data flow
│   ├── 08-workflow.md             # development workflow & process
│   └── 09-structure.md            # project directory structure
│
├── planning/
│   ├── 00-quickstart.md           # 10-min overview of planning docs
│   ├── 01-proposal.md             # business/project proposal
│   └── 02-timeline.md             # milestones & schedules
│
├── api/
│   ├── 00-quickstart.md           # 10-min api overview
│   └── 01-api-design.md           # api specifications & contracts
│
├── results/
│   ├── 00-quickstart.md           # 10-min overview of results
│   ├── 01-evaluation.md           # model/solution evaluation metrics
│   ├── 02-testing.md              # testing methodology & results
│   ├── 03-performance-comparison.md  # benchmarks vs. baselines
│   ├── 04-results-analysis.md     # detailed findings & insights
│   └── 05-future-work.md          # next steps & open problems
│
└── presentation/
    ├── 00-quickstart.md           # 10-min overview of presentation materials
    └── 01-presentation-script.md  # slide scripts & talking points
```

## first-line format rule

every created file's first line follows this exact format:
```
{relative_path} - {filename_without_extension}: {description}
```

example: `docs/research/02-references.md - 02-references: academic references & papers`

## Question Checklist — What Makes a Good Question

- **Problem:** Clearly state the problem being solved and its context.
- **Audience:** Specify who will use or benefit from the answer (stakeholders, role, skill level).
- **Expected outcome:** Describe the desired result or decision that should follow.
- **Measurement / Success metric:** Define how success will be measured and which metric(s) matter.
- **Scope & constraints:** Note time, budget, technical, or legal limits.
- **Acceptance criteria:** What counts as “done” or an acceptable answer.
- **Data & dependencies:** List required data, sources, and availability.
- **Risks & assumptions:** Call out key assumptions and failure modes.

### SMART framework

- **S — Specific:** Make the question precise and unambiguous (who, what, where, why).
- **M — Measurable:** Tie the question to data or metrics so progress is observable.
- **A — Action-oriented:** Frame questions to produce actionable next steps or decisions.
- **R — Relevant:** Ensure the question aligns with project goals and stakeholder priorities.
- **T — Time-bound:** Add a timeframe or deadline that constrains the outcome.

### North Star Metric (NSM)

- Define a single NSM that captures the core long-term value the project delivers (for example: "weekly active users", "documents processed per day", "production F1").
- Use the NSM to prioritize which questions matter most and to judge trade-offs between short-term experiments and long-term impact.

### How to use this checklist

- Keep this canonical checklist here and reference it from the problem, goal, and planning docs when drafting questions or proposals.
- When writing a question, fill the checklist fields and map the primary metric to either a SMART target or the NSM.
- Use the acceptance criteria and measurement fields to decide when a question is resolved.

