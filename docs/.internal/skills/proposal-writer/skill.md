---
name: proposal-writer
description: >
  Write or regenerate the project proposal file (docs/planning/01-proposal.md)
  by synthesizing content from all docs/project-definition/*.md files. Use this
  skill whenever the user says "write my proposal", "generate the proposal",
  "create proposal.md", "fill in the proposal", "write docs/planning/01-proposal.md",
  or anything implying they want the planning proposal written from the
  project-definition docs. Also trigger if the user says "my project-definition
  docs are ready, now write the proposal" or similar. Always overwrites the
  existing 01-proposal.md with a freshly synthesized version.
---

# proposal-writer

read the `docs/project-definition/` files and synthesize them into a complete `docs/planning/01-proposal.md`. this is a content synthesis task — read carefully, extract real signal, write clearly. the output is a hybrid document: executive-readable summary on top, technical depth in the body.

## step 1 — read all source files

read each of these files in order:

| file | what to extract |
|------|-----------------|
| `docs/project-definition/01-problem.md` | problem statement, context, who is affected, why now, constraints |
| `docs/project-definition/02-goal.md` | primary goal, success criteria, non-goals |
| `docs/project-definition/03-solution.md` | approach, key design decisions, trade-offs, assumptions |
| `docs/project-definition/04-dataset.md` | data sources, format, preprocessing, known issues |
| `docs/project-definition/05-constraints.md` | what to do / not do, bias risks, misuse risks, compliance |
| `docs/project-definition/06-stack.md` | tech stack, libraries, environment requirements |
| `docs/project-definition/07-architecture.md` | system components, data flow, key decisions |
| `docs/project-definition/08-workflow.md` | development process, common commands |
| `docs/project-definition/09-structure.md` | directory layout, key files |

## step 2 — detect placeholder vs real content

for each file, check whether it contains real project-specific content or is still just template placeholder text.

a file is **placeholder-only** if its non-header content is either:
- the original template prompt text (e.g. "in 2-3 sentences: what exact problem does this project solve?", "- goal 1", "one sentence: what does success look like?")
- completely empty beyond the first line and section headers

a file has **real content** if it has been filled in with actual project-specific text beyond those prompts.

## step 3 — write the proposal

write to `docs/planning/01-proposal.md`. always overwrite if it exists.

**first line must follow the docs-maker format exactly:**
```
docs/planning/01-proposal.md - 01-proposal: business / project proposal
```

then write the full proposal using this exact section structure:

---

### `## executive summary`
source: synthesize from 01-problem + 02-goal + 03-solution

3-5 sentences. written for a non-technical reader — no jargon, no acronyms. answer: what is this project, what problem does it solve, and what does success look like? this is the only section that must stay accessible. if any source files are placeholder-only, write what can be inferred from the available files and flag the rest.

---

### `## problem`
source: 01-problem.md

copy the core problem statement and context. keep it crisp — 2-4 sentences on the problem itself, then a brief note on who is affected and why this matters now. do not pad.

---

### `## proposed solution`
source: 03-solution.md

describe the approach in plain language first (2-3 sentences), then go technical. include the key design decisions and explain the reasoning behind them. mention alternatives considered and why they were rejected, if the source file has this.

---

### `## technical approach`
source: 07-architecture.md + 06-stack.md

describe the system architecture: components, data flow, and the stack. include the core technologies and why they were chosen. a short ascii diagram is fine if the source has one.

---

### `## data strategy`
source: 04-dataset.md

data sources, format, preprocessing pipeline, splits, and any known issues. if no data file exists in the project (e.g. pure api project), write "not applicable" and note why.

---

### `## constraints & ethics`
source: 05-constraints.md

**header must use `&` not "and": write `## constraints & ethics` exactly.**

what this project must do, and what it must never do. cover the key ethical constraints, bias risks, misuse scenarios, and any regulatory notes. keep it specific — not generic ethics boilerplate.

---

### `## resources required`
source: 06-stack.md + 07-architecture.md

what is needed to build and run this project: compute, storage, team, external services, licensing. be specific where the source files allow.

---

### `## risks`
source: 05-constraints.md (misuse risks) + 03-solution.md (trade-offs)

use a markdown table:
```
| risk | likelihood | impact | mitigation |
|------|-----------|--------|------------|
```
pull real risks from the source files. do not invent generic risks.

---

### `## success metrics`
source: 02-goal.md (success criteria + primary goal)

specific, measurable criteria. if the source file has them, use them exactly. if not, derive them from the goal statement and flag as estimated.

---

### `## incomplete sections`
only include this section if one or more source files were placeholder-only.

list exactly which sections were skipped and which source files need to be filled in:
```
the following sections could not be fully written because the source files
contain placeholder text only:

- [section name]: needs docs/project-definition/XX-filename.md
```

---

## tone rules

- executive summary: plain english, no jargon, 3-5 sentences max
- rest of the document: technical and precise. write like a senior ai engineer documenting a real project
- no filler phrases: "exciting", "innovative", "cutting-edge", "leverage", "synergy"
- no padding. if a section is thin because the source is thin, keep it short and say so
- active voice. short sentences. no em dashes.

## output

write the file directly to `docs/planning/01-proposal.md`. confirm to the user with a one-line summary of what was written and which sections (if any) were skipped.
