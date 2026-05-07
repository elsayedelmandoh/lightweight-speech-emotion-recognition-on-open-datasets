---
description: Commit all changes on the current feature branch and create a PR to main, using the spec artifacts for context.
---

## GitHub Accounts

Available collaborator accounts for commit and PR creation:

| Account | User Name | Email | Usage |
|---------|-----------|-------|-------|
| aang | aang-agent | aangipynb@gmail.com | Agent commits (automation) |
| su | su-agent | fourfdf@gmail.com | Agent commits (automation) |

**To switch accounts before running speckit.pr:**
```bash
git-profile aang-agent   # switch to aang account
git-profile su-agent     # switch to su account
git-profile              # show current active account
```

The current active git user (name and email) will be displayed before pushing.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Commit all staged and unstaged changes on the current feature branch, push to remote, and create a pull request to `main`. The PR title and body are derived from the spec artifacts in the current feature's `specs/` folder.

## Pre-Execution Checks

0. **Display active git account**: Run `git-profile` (with no arguments) to show the current active git user.name and user.email. This is the account that will be used for all commits and the PR. Display this information to the user in the terminal.
   ```bash
   git-profile  # shows current active profile: Name and Email
   ```

1. Run `git rev-parse --abbrev-ref HEAD` to get the current branch.
2. Confirm the branch is NOT `main`. If it is, STOP and tell the user to switch to a feature branch.
3. Determine SPEC_NAME from the current branch using this mapping:
   - Extract the branch slug (last segment after `/`). e.g., `feat/watchlist-monitor-agent` → `watchlist-monitor-agent`
   - Map branch slug to spec folder number:
     - `shared-infrastructure` → `001-shared-infrastructure`
     - `watchlist-monitor-agent` → `002-watchlist-monitor-agent`
     - `nlp-analysis-engine` → `003-nlp-analysis-engine`
     - `graph-detector` → `004-graph-detector`
     - `dfir-forensics` → `005-dfir-forensics`
     - `botnet-c2-simulator` → `006-botnet-c2-simulator`
     - `ops-security` → `007-ops-security`
   - If no match, try to find the best match by listing `specs/*` and matching by slug.
4. Check if `specs/<SPEC_NAME>/` exists. If not, STOP and tell the user the spec folder is missing.
5. Run `git status` to see all changes (staged, unstaged, untracked).
6. If there are NO changes and NO unpushed commits, STOP and tell the user there is nothing to commit or push.

## Branch Naming Convention

Branches follow the pattern: `type/descriptive-name` (no numbers in branch names).

| Category | Prefix | Example |
|----------|--------|---------|
| New feature | `feat/` | `feat/watchlist-monitor-agent` |
| Bug fix | `fix/` | `fix/session-isolation-bug` |
| Documentation | `docs/` | `docs/project-definition` |
| Refactoring | `refactor/` | `refactor/performance-tuning` |
| Routine/chore | `chore/` | `chore/ci-cd-setup` |

Spec folders retain their numbers. The mapping between branch names and spec folders is:
- `feat/shared-infrastructure` ↔ `specs/001-shared-infrastructure/`
- `feat/watchlist-monitor-agent` ↔ `specs/002-watchlist-monitor-agent/`
- `feat/nlp-analysis-engine` ↔ `specs/003-nlp-analysis-engine/`
- `feat/graph-detector` ↔ `specs/004-graph-detector/`
- `feat/dfir-forensics` ↔ `specs/005-dfir-forensics/`
- `feat/botnet-c2-simulator` ↔ `specs/006-botnet-c2-simulator/`
- `chore/ops-security` ↔ `specs/007-ops-security/`

## Execution Steps

### Step 1: Read Spec Context

Read the following files (if they exist) to build PR context:
- `specs/<SPEC_NAME>/spec.md` -- extract the feature description, user stories, and scope
- `specs/<SPEC_NAME>/tasks.md` -- extract task completion summary
- `specs/<SPEC_NAME>/review/` -- find the latest review file, extract overall status

### Step 2: Stage and Commit

1. Run `git status` and `git diff --stat` to understand all changes.
2. Run `git log main..HEAD --oneline` to see existing commits on this branch.
3. Read `.gitignore` and parse all patterns. This is the **authoritative exclusion list**.
4. **STRICT RULE**: NEVER use `git add -f`. If a file is in `.gitignore`, it MUST NOT be committed. No exceptions.
5. Stage only files that are NOT ignored by `.gitignore`. Use `git status` output (which already respects `.gitignore`) as the source of truth:
   - only stage files listed under "Changes not staged for commit" (modified tracked files)
   - only stage files listed under "Changes to be committed" (already staged)
   - do NOT stage files listed under "Untracked files" if they match `.gitignore` patterns
   - to verify a file is safe to add, run: `git check-ignore -v <path>` -- if it returns a match, do NOT add it
6. Common files that are typically safe to stage (if they appear as modified tracked files):
   - `src/**/*.py`, `tests/**/*.py` -- code
   - `requirements.txt`, `.env.example`, `.gitignore` -- config
   - `docs/**` -- documentation
7. Create a single commit with a message derived from the spec:
   - format: `feat(s0): <short description from spec.md scope line>`
   - include task completion stats in the commit body

### Step 3: Push to Remote

0. **Verify active git account**: Call `git-profile` again to display the current active user.name and user.email before pushing. This confirms which account will author the commits and PR.

1. Check if the branch has an upstream remote: `git rev-parse --abbrev-ref @{u} 2>/dev/null`
2. If no upstream, push with: `git push -u origin <branch>`
3. If upstream exists, push with: `git push`

### Step 4: Create Pull Request

1. Check if a PR already exists for this branch: `gh pr list --head <branch> --json number`
2. If a PR already exists, update it and print the URL. Do NOT create a duplicate.
3. If no PR exists, create one using `gh pr create` with:

**Title format**: `feat(s0): <feature name from spec.md>`

**Body format** (use HEREDOC):

```
## summary

<2-3 bullet points from spec.md scope and user stories>

## what changed

<list of major implementation modules with brief descriptions>

## spec artifacts

- spec: `specs/<SPEC_NAME>/spec.md`
- tasks: `specs/<SPEC_NAME>/tasks.md` (<completed>/<total> tasks)
- review: `specs/<SPEC_NAME>/review/<latest>.md` (status: <PASS/PARTIAL/FAIL>)

## test results

- <X> passed, <Y> failed
- unit tests: `tests/unit/`
- integration tests: `tests/integration/`

## test plan

- [ ] verify `pytest` passes with 0 failures
- [ ] verify all spec tasks are marked complete in tasks.md
- [ ] verify review report shows PASS status
- [ ] verify .env.example documents all required environment variables

```

4. Print the PR URL when done.

## Hard Rules

- **GITIGNORE IS LAW**: NEVER use `git add -f`. NEVER commit any file or directory listed in `.gitignore`. If `.gitignore` says it is ignored, it does not get committed. period.
- NEVER commit `.env` or files containing credentials
- NEVER force push
- NEVER push to `main` directly
- NEVER create a PR if one already exists for this branch (update instead)
- commit message and PR body MUST be lowercase (project style rule)
- do NOT use em dashes in any content (project style rule)
- if `gh` CLI is not available, STOP and tell the user to install it
- if push fails due to auth, STOP and tell the user to run `! gh auth login`
