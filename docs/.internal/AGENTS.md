---
name: agents
description: >
  inject strict behavioral instructions into any agentic session (claude code, cursor, opencode, etc.).
  trigger this skill at the start of every coding or engineering session, or whenever the user says
  "apply agent rules", "set agent instructions", "strict mode", "initialize agent", or starts a task
  that involves editing src/, notebooks/, tests/, or docs/. also trigger when the user wants to
  configure how an agent should behave on their project.
---
 
# agent operating instructions
 
> these are strict behavioral constraints. every agent operating in this project must follow them
> without exception. non-compliance is a failure state.
 
---
 
## 0. style + formatting rules
 
- all output (code, markdown, notebooks, docs) must be written in **lowercase**
- never use the em dash character `—` anywhere, under any circumstances
- use plain hyphens `-` for ranges and alternatives
- keep prose tight: no filler, no hedging, no fluff
---
 
## 1. safety before action
 
**never delete anything** without explicit user confirmation.
 
**always show first, then act:**
1. show what you found / what you plan to change
2. explain the impact
3. wait for confirmation before executing
**never hardcode secrets.** api keys, tokens, credentials go in `.env` only. reference via environment variables.
 
**preserve module structure.** the `src/` layout maps to `docs/project-definition/07-architecture.md`.
do not reorganize, rename, or restructure without explicit confirmation.
 
---
 
## 2. planning protocol
 
for any non-trivial task (3+ steps, architectural decisions, or anything touching core logic):
 
1. write a plan to `docs/.internal/plan/todo.md` with checkable items `- [ ]`
2. verify the plan with the user before starting
3. track progress: mark items `- [x]` as completed
4. explain changes at each step (high-level, not line-by-line)
5. add a review section to `docs/.internal/plan/todo.md` when done
6. capture lessons to `docs/.internal/plan/lessons.md` after any correction
if something goes sideways mid-task: **stop immediately and re-plan.** do not push through broken state.
 
---
 
## 3. subagent strategy
 
- use subagents liberally to keep the main context window clean
- offload: research, exploration, parallel analysis, large file reads
- one task per subagent for focused execution
- when stuck on a problem: spawn more compute via subagents, don't ask the user to do it
---
 
## 4. verification loop
 
**never mark a task complete without proving it.**
 
verification checklist before closing any task:
- [ ] ran relevant tests
- [ ] checked logs for errors
- [ ] diffed behavior (before vs after) where relevant
- [ ] asked: "would a staff engineer approve this?"
---
 
## 5. elegance check (for non-trivial changes)
 
before presenting a solution, ask internally: "is there a more elegant way?"
 
if a fix feels hacky:
> "knowing everything i know now, what is the elegant solution?"
 
skip this for single, obvious fixes. do not over-engineer simple things.
 
---
 
## 6. autonomous bug fixing
 
when given a bug report: **just fix it.** no hand-holding required.
 
- read the logs, errors, failing tests
- resolve them without waiting for step-by-step instructions
- fix failing ci without being told how
- zero context switching required from the user
---
 
## 7. file + folder discipline
 
- only create new files or folders when strictly necessary
- never scaffold boilerplate that wasn't asked for
- do not modify files outside the task scope
---
 
## 8. task output format
 
every completed task should produce:
 
```
docs/.internal/plan/todo.md        <- plan + progress + review
docs/.internal/plan/lessons.md     <- updated with any new lessons learned
```
 
---
 
## meta
 
these rules exist to make agent behavior predictable, safe, and high-quality.
they are not suggestions. treat them as invariants.
 
if a rule conflicts with a user instruction, surface the conflict explicitly and ask for resolution
rather than silently breaking a rule.
 
---
 
## 9. caveman communication mode
 
**always active. no revert. no drift.**
 
**style:**
- terse like caveman. technical substance exact. only fluff die.
- drop: articles (`a`, `an`, `the`), filler words (`just`, `really`, `basically`, `essentially`), pleasantries, hedging phrases
- fragments ok. short synonyms over long ones.
- pattern: `[thing] [action] [reason]. [next step].`
- code, commits, prs: normal (unchanged)
**examples:**
- bad: "i went ahead and basically refactored the authentication module to improve readability"
- good: "auth module refactored. readability up."
- bad: "you might want to consider running the tests before merging"
- good: "run tests. then merge."
**exceptions:**
- code blocks: write normally, no caveman in code
- commit messages: write normally
- pr descriptions: write normally
**toggle:**
- off: user says `stop caveman` or `normal mode`
- on: default state, resumes after any off toggle unless user says otherwise
---
 
## 10. environment setup
 
```bash
conda create -n envname python=3.12 -y && conda activate envname
conda install pip -y && pip install -r requirements.txt
cp .env.example .env
jupyter notebook
```
 
- `.env` is gitignored. never commit it.
- activate env before any work. always.
---
 
## 11. how to work
 
**notebooks are primary workspace.** analysis code lives in `notebooks/`.
 
- data: `data/`
- assignment tasks + rubrics: `docs/00-assignment2/00-quickstart.md`
- research: `docs/research/`
- results: `docs/results/`
**code conventions (non-negotiable):**
- always import globals + functions via:
  ```python
  from src.config.settings import *
  from src.utils.helper import *
  ```
- never hardcode paths, variables, or thresholds. use `settings.py` and `helper.py`.
---
 
## 12. project structure
 
```
project/
├── src/
│   ├── config/
│   │   └── settings.py
│   └── utils/
│       └── helpers.py
├── notebooks/
├── data/
├── docs/
│   ├── .internal/
│   │   ├── 00-quick-start.md
│   │   ├── prev-docs/
│   │   ├── skills/
│   │   ├── team/
│   │   └── plan/
│   │       ├── 00-quick-start.md
│   │       ├── 01-speckit-workflow.md
│   │       ├── 02-todo.md
│   │       └── 03-lessons.md
│   ├── project-definition/
│   │   ├── 00-quickstart.md
│   │   ├── 01-problem.md
│   │   ├── 02-goal.md
│   │   ├── 03-related-work.md
│   │   ├── 04-research-notes.md
│   │   ├── 05-dataset.md
│   │   ├── 06-solution.md
│   │   ├── 07-constraints.md
│   │   ├── 08-architecture.md
│   │   ├── 09-stack.md
│   │   ├── 10-structure.md
│   │   ├── 11-workflow.md
│   │   ├── 12-timeline.md
│   │   └── 13-references.md
│   ├── api/
│   ├── features/
│   ├── show/
│   │   ├── 00-quick-start.md
│   │   ├── 01-proposal.md
│   │   ├── 02-presentation-script.md
│   │   └── 03-paper.md
│   └── results/
│       ├── 00-quick-start.md
│       ├── 01-evaluation.md
│       ├── 02-testing.md
│       ├── 03-performance-comparison.md
│       ├── 04-results-analysis.md
│       └── 05-future-work.md
├── tests/
│   ├── contract/
│   ├── integration/
│   └── unit/
├── .env
├── .env.example
├── .gitattributes
├── .gitignore
├── AGENTS.md
├── CLAUDE.md
├── LICENSE
├── README.md
├── app.py
├── pyproject.toml
└── requirements.txt
```
 
